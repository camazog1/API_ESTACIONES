import os
import pytest
from fastapi.testclient import TestClient
from app.main import app  
import math

@pytest.fixture(scope="module")
def test_client():

    client = TestClient(app)
    yield client

def test_create_station(test_client):
    new_station = {
        "name": "Estación de prueba A", 
        "location": ["1.3", "2.1"],  
        "option": 0
    }

    response = test_client.post("/estaciones/", json=new_station)

    if response.status_code != 200:
        print(response.json())

    assert response.status_code == 200

def test_read_stations(test_client):
    new_station = {
        "name": "Estación de prueba B", 
        "location": ["21", "-5.1"],  
        "option": 0
    }

    response = test_client.post("/estaciones/", json=new_station)
    if response.status_code != 200:
        print(response.json())

    assert response.status_code == 200

    response = test_client.get("/estaciones/")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_read_estation_nearest(test_client):
    new_station = {
        "name": "Estación de prueba C", 
        "location": ["1", "-5.1"],  
        "option": 0
    }

    response = test_client.post("/estaciones/", json=new_station)
    if response.status_code != 200:
        print(response.json())

    assert response.status_code == 200

    response = test_client.get("/estaciones/cercana/1")
    assert response.status_code == 200

def test_read_estation_nearest_comparison(test_client):
    response = test_client.get("/estaciones/")
    assert response.status_code == 200
    stations = response.json()

    response1 = test_client.get("/estaciones/cercana/1")
    assert response1.status_code == 200
    estacion_cercana_kd_tree = response1.json()[1]

    estacion_cercana_fuerza_bruta = None
    estacion_referencia = stations[0]
    distancia_minima = float("inf")
    
    for estacion in stations[1:]:
        if estacion != estacion_referencia:
            distancia = math.sqrt(
                (float(estacion["latitude"]) - float(estacion_referencia["latitude"])) ** 2 +
                (float(estacion["longitude"]) - float(estacion_referencia["longitude"])) ** 2)
        
            if distancia < distancia_minima:
                distancia_minima = distancia
                estacion_cercana_fuerza_bruta = estacion

    assert estacion_cercana_kd_tree["id"] == estacion_cercana_fuerza_bruta["id"]
