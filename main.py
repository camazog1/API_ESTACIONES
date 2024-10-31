
from nicegui import ui
import httpx

ui.run()

# Crea una interfaz NiceGUI
@ui.page('/')
def index():
    ui.label('¡Hola desde NiceGUI!')

    # Define un botón que llama a la ruta de FastAPI
    def on_button_click():
        # Realiza una solicitud GET a la ruta de FastAPI
        response = httpx.get("http://localhost:8000/")
        data = response.json()
        # Muestra la respuesta en un mensaje de notificación
        ui.notify(data["message"])

    ui.button('Haz clic aquí', on_click=on_button_click)
