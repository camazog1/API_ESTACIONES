from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, init_db
from .KD_Tree import KDTree

app = FastAPI()
stations_kd_tree = None
init_db() 

def load_stations_into_kd_tree(db):
    global stations_kd_tree
    stations = db.query(models.Station).all()
    print(f"Loaded stations") 
    info_nodes = [((station.latitude, station.longitude), station.id) for station in stations]
    stations_kd_tree = KDTree(info_nodes)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/estaciones/", response_model=schemas.Station)
def create_station(station: schemas.StationCreate, db: Session = Depends(get_db)):
    global stations_kd_tree  
    
    existing_station = db.query(models.Station).filter(models.Station.name == station.name).first()
    if existing_station:
        raise HTTPException(status_code=400, detail="La estación con este nombre ya existe.")

    last_station = create_station_entry(station.name, station.location, station.option)
    latitude, longitude = last_station["location"]

    existing_location = db.query(models.Station).filter(
        (models.Station.latitude == latitude) & (models.Station.longitude == longitude)
    ).first()
    
    if existing_location:
        raise HTTPException(status_code=400, detail="Ya existe una estación en esta ubicación.")

    db_station = models.Station(name=last_station["name"], latitude=latitude, longitude=longitude)

    db.add(db_station)
    db.commit()
    db.refresh(db_station)

    if stations_kd_tree is None:
        load_stations_into_kd_tree(db)
    stations_kd_tree.insert((latitude, longitude), db_station.id)

    return db_station

@app.get("/estaciones/", response_model=list[schemas.Station])
def read_stations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Station).offset(skip).limit(limit).all()

@app.get("/estaciones/cercana/{station_id}", response_model=list[schemas.Station])
def read_station_nearest(station_id: int, db: Session = Depends(get_db)):
    global stations_kd_tree 

    if stations_kd_tree is None:
        load_stations_into_kd_tree(db)

    station = db.query(models.Station).filter(models.Station.id == station_id).first()
    if station is None:
        raise HTTPException(status_code=404, detail="Estación no encontrada")

    nearest_node = stations_kd_tree.nearest_neighbor(stations_kd_tree.root, (station.latitude, station.longitude), station.id)
    
    if nearest_node is None:
        return None

    nearest_station = db.query(models.Station).filter(models.Station.id == nearest_node.id).first()

    if nearest_station is None:
        return None

    response = {
        "id": nearest_station.id,
        "name": nearest_station.name,
        "latitude": nearest_station.latitude,
        "longitude": nearest_station.longitude
    }
    
    return [station, response]

def create_station_entry(name: str, location: dict, option: int):
    if option == 0:
        lat = float(location[0])
        lon = float(location[1])
        return {"name": name, "location": (lat, lon)}
    elif option == 1:
        parts = location[0].split('°')
        degrees = float(parts[0]) 
        orientation = str(parts[1].split("''")[1])
        minutes = float(parts[1].split("'")[0]) 
        seconds = float(parts[1].split("'")[1])
        lat = degrees + (minutes / 60) + (seconds / 3600)

        if orientation == 'S':
            lat = -lat

        parts = location[1].split('°')
        degrees = float(parts[0]) 
        orientation = str(parts[1].split("''")[1])
        minutes = float(parts[1].split("'")[0]) 
        seconds = float(parts[1].split("'")[1])
        lon = degrees + (minutes / 60) + (seconds / 3600)

        if orientation == 'W':
            lon = -lon

        return {"name": name, "location": (lat, lon)}
    