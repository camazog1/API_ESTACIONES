
from nicegui import ui
import httpx

ui.run()

@ui.page('/')
def index():

    with ui.row():
        with ui.card():
            ui.label('Añadir nueva estación')
            
            station_name = ui.input('Nombre de la estación')
            station_latitude = ui.input('Latitud de la estación', placeholder='Por ejemplo, 4.6111')
            station_longitude = ui.input('Longitud de la estación', placeholder='Por ejemplo, -74.0817')
            station_option = ui.select({0: 'Coordenadas Cartesianas', 1: 'Coordenadas Geográficas'}, value=0)

            def on_button_click():
                response = httpx.post("http://localhost:8000/estaciones/", json={"name": station_name.value, "location": (station_latitude.value, station_longitude.value), "option": station_option.value})
                data = response.json()
                message = f"""
                ID: {data["id"]};
                Nombre: {data["name"]};
                Latitud: {data["latitude"]};
                Longitud: {data["longitude"]}
                """
                ui.notify('Estación Creada Correctamente', type='positive')
                ui.notify(message)

            ui.button('Guardar', on_click=on_button_click)
        
        with ui.card().style('max-width: 500px;'):
            ui.label('Ver todas las estaciones')
            
            skip = ui.input('Desde que ID empezamos')
            limit = ui.input('Cuantos IDs queremos mostrar')

            stations_column = ui.column().style('max-height: 400px; overflow-y: auto;')

            def on_button_click1():
                stations_column.clear()
                if skip.value.strip() == "" or limit.value.strip() == "":
                    response = httpx.get("http://localhost:8000/estaciones/")
                    ui.notify('No se especificó ningún limite o salto por lo tanto desde 1 hasta 100', type='negative')
                else:
                    response = httpx.get(f"http://localhost:8000/estaciones/?skip={int(skip.value)-1}&limit={int(limit.value)}")
                data = response.json()

                if response.status_code == 200:
                    data = response.json()

                    if data:
                        for estacion in data:
                            with stations_column:
                                with ui.card():
                                    ui.label(f"ID: {estacion['id']}")
                                    ui.label(f"Nombre: {estacion['name']}")
                                    ui.label(f"Latitud: {estacion['latitude']}")
                                    ui.label(f"Longitud: {estacion['longitude']}")
                    else:
                        ui.notify('No se encontraron estaciones para mostrar', type='negative')
                else:
                    ui.notify("Error al obtener datos", type='negative')

            
            ui.button('Mostrar', on_click=on_button_click1)

        with ui.card().style('max-width: 500px;'):
            ui.label("Buscar estación más cercana")
            
            station_id = ui.input('ID de la estación')

            station_column = ui.column().style('max-height: 400px; overflow-y: auto;')
            
            def on_button_click2():
                station_column.clear()

                if station_id.value.strip() == "":
                    ui.notify('No se especificó ningún ID de estación', type='negative')
                    return
                
                response = httpx.get(f"http://localhost:8000/estaciones/cercana/{int(station_id.value)}")
                data = response.json()

                if response.status_code == 200:
                    if data:
                        with station_column:
                            ui.label(f"ID: {data[1]['id']}")
                            ui.label(f"Nombre: {data[1]['name']}")
                            ui.label(f"Latitud: {data[1]['latitude']}")
                            ui.label(f"Longitud: {data[1]['longitude']}")
                            ui.notify(f"Estación más cercana a la {data[0]['name']} es la {data[1]['name']}", type='positive')
                    else:
                        ui.notify('No se encontraron estaciones para mostrar', type='negative')
                else:
                    ui.notify("Error al obtener datos", type='negative')
        
            ui.button('Buscar', on_click=on_button_click2)