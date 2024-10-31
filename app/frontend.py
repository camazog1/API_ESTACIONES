from nicegui import ui
import httpx

ui.run()

@ui.page('/')
def index():
    ui.query('body').style('background: #fdfdfd;')
    ui.label('ADMINISTRACIÓN DE ESTACIONES').style('font-size: 2em; color: black; text-align: center; margin-top: 1em; align-self: center;')

    with ui.column().style('align-items: center; justify-content: center; gap: 1.5em; color: #525252;'):

        with ui.row().style('gap: 2em;'):

            with ui.card().style('background: #f5f1f0; width: 400px; height: 400px; text-align: center; padding: 2em; justify-content: center;'):
                ui.label('Añadir nueva estación').style('align-self: center; color: #000000;')
                station_name = ui.input('Nombre de la estación').style('align-self: center;')
                station_latitude = ui.input('Latitud de la estación', placeholder='Ejemplo: 4.6111').style('align-self: center;')
                station_longitude = ui.input('Longitud de la estación', placeholder='Ejemplo: -74.0817').style('align-self: center;')
                station_option = ui.select({0: 'Coordenadas Cartesianas', 1: 'Coordenadas Geográficas'}, value=0).style('align-self: center;')

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

                ui.button('Guardar', on_click=on_button_click).style('align-self: center;')

            with ui.card().style('background: #f5f1f0; width: 400px; height: 400px; text-align: center; padding: 2em; justify-content: center;'):
                ui.label('Ver todas las estaciones').style('align-self: center; color: #000000;')
                skip = ui.input('Desde que ID empezamos').style('align-self: center;')
                limit = ui.input('Cuantos IDs queremos mostrar').style('align-self: center;')
                stations_column = ui.column().style('max-height: 400px; overflow-y: auto; align-self: center;')

                def on_button_click1():
                    stations_column.clear()
                    response = httpx.get(f"http://localhost:8000/estaciones/?skip={int(skip.value)-1}&limit={int(limit.value)}") if skip.value and limit.value else httpx.get("http://localhost:8000/estaciones/")
                    data = response.json()

                    if response.status_code == 200:
                        for estacion in data:
                            with stations_column:
                                with ui.card():
                                    ui.label(f"ID: {estacion['id']}").style('align-self: center;')
                                    ui.label(f"Nombre: {estacion['name']}").style('align-self: center;')
                                    ui.label(f"Latitud: {estacion['latitude']}").style('align-self: center;')
                                    ui.label(f"Longitud: {estacion['longitude']}").style('align-self: center;')
                    else:
                        ui.notify("Error al obtener datos", type='negative')

                ui.button('Mostrar', on_click=on_button_click1).style('align-self: center;').style('align-self: center;')

            with ui.card().style('background: #f5f1f0; width: 400px; height: 400px; text-align: center; padding: 2em; justify-content: center;'):
                ui.label("Buscar estación más cercana").style('align-self: center; color: #000000;')
                station_id = ui.input('ID de la estación').style('align-self: center;').style('align-self: center;')
                station_column = ui.column().style('max-height: 400px; overflow-y: auto; align-self: center;')

                def on_button_click2():
                    station_column.clear()
                    if station_id.value.strip():
                        response = httpx.get(f"http://localhost:8000/estaciones/cercana/{int(station_id.value)}")
                        data = response.json()
                        if response.status_code == 200 and data:
                            with station_column:
                                ui.label(f"ID: {data['stations'][1]['id']}").style('align-self: center;')
                                ui.label(f"Nombre: {data['stations'][1]['name']}").style('align-self: center;')
                                ui.label(f"Latitud: {data['stations'][1]['latitude']}").style('align-self: center;')
                                ui.label(f"Longitud: {data['stations'][1]['longitude']}").style('align-self: center;')
                                ui.label('Distancia:').style('align-self: center; color : blue;')
                                ui.label(f"{data['distance']:.4f} Unidades").style('align-self: center;')
                            ui.notify(f"Estación más cercana a la {data['stations'][0]['name']} es la {data['stations'][1]['name']}", type='positive')
                        else:
                            ui.notify('No se encontraron estaciones para mostrar', type='negative')
                    else:
                        ui.notify('No se especificó ningún ID de estación', type='negative')

                ui.button('Buscar', on_click=on_button_click2).style('align-self: center;')

    with ui.link(target="https://github.com/camazog1/"):
        ui.avatar('img:https://avatars.githubusercontent.com/u/9961503?v=4', color='white')

