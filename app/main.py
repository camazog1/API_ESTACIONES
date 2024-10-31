from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, init_db
from fastapi.encoders import jsonable_encoder
from .KD_Tree import KDTree

# initialize FastAPI and database
app = FastAPI()
stations_kd_tree = None
init_db() 

# load stations into KDTree
def load_stations_into_kd_tree(db):
    global stations_kd_tree
    stations = db.query(models.Station).all()
    print(f"Loaded stations") 
    info_nodes = [((station.latitude, station.longitude), station.id) for station in stations]
    stations_kd_tree = KDTree(info_nodes)

# get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# create a new station
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

# read all stations
@app.get("/estaciones/", response_model=list[schemas.Station])
def read_stations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Station).offset(skip).limit(limit).all() # query all stations starting from skip and returning limit

# read the nearest station to a given station
@app.get("/estaciones/cercana/{station_id}", response_model=schemas.nearstationresponse)
def read_station_nearest(station_id: int, db: Session = Depends(get_db)):
    global stations_kd_tree 

    # load stations into KDTree if it's not loaded
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
    
    # create response
    current_station = {
        "id":station.id,
        "name":station.name,
        "latitude":station.latitude,
        "longitude":station.longitude
    }

    response = {
        "id": nearest_station.id,
        "name": nearest_station.name,
        "latitude": nearest_station.latitude,
        "longitude": nearest_station.longitude
    }

    complete_response = {
        "stations": [current_station, response],
        "distance": nearest_node.distance
    }
    
    return complete_response

# organizes the location of a station
def create_station_entry(name: str, location: dict, option: int):
    if option == 0:
        # if the location is in cartesian coordinates only convert to float
        lat = float(location[0])
        lon = float(location[1])
        return {"name": name, "location": (lat, lon)}
    elif option == 1:
        # if the location is in geographic coordinates convert to float
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
    