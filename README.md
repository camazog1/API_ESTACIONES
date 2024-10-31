# API_ESTACIONES

## Descripción

Este proyecto es una API REST desarrollada en FastAPI para la gestión de estaciones. Incluye funcionalidades para crear y listar estaciones, así como para encontrar la estación más cercana a una estación dada. La API se conecta a una base de datos SQL en este caso PostgreSQL y está preparada para una futura ampliación en la que se recibirán datos de estaciones en tiempo real.

## Tabla de Contenidos

- Instalación y Configuación
- Ejecutar el Proyecto
- Migraciones del Proyecto
- Pruebas Unitarias

## Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone https://https://github.com/camazog1/API_ESTACIONES/
cd API_ESTACIONES
```

### 2. Configurar un entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows - venv\Scripts\activate
```

### 3. Instalar requerimientos

```bash
pip install -r requirements.txt
```

### 4. Conección con la base de datos

Para lo siguiente crearemos un archivo llamado `.env` que para mayor seguridad ignoraremos en `.gitignore`, modificaremos este archivo `.env` de la siguiente manera:

```bash
# URL de la base de datos PostgreSQL utilizada durante el desarrollo local de la aplicación
DATABASE_URL = postgresql://usuario:clave@localhost:5432/base_de_datos

# URL de la base de datos PostgreSQL utilizada para ejecutar las pruebas de la aplicación
DATABASE_URL1 = postgresql://usuario:clave@localhost:5432/base_de_datos_de_pruebas

# Configuración de la base de datos PostgreSQL dentro del contenedor Docker
DATABASE_URL2 = postgresql://usuario:clave@db:5432/base_de_datos
POSTGRES_DB = base_de_datos
POSTGRES_USER = usuario
POSTGRES_PASSWORD = clave

# Ruta a la aplicación
PYTHONPATH = ./app
```

## Ejecutar el Proyecto

En este momento es necesario estar en el entorno virtual y en la carpeta `API_ESTACIONES/` aqui ejecuta:

```bash
uvicorn main:app --reload
```

y en otra terminal ejecuta:

```bash
python -m app.frontend
```

Aqui se estaran ejecutando 2 servicios, uno funciona de la misma manera que en el `main` ejecutandose en la [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). y la interface Grafica se ejecutara en [http://127.0.0.1:8080/](http://127.0.0.1:8080/).

> ⚠️ **Advertencia:** En la interface grafica sigue siendo obligatorio el uso de la estructura `xx°xx'xx''x` para la entrega de **Coordenadas Geograficas** donde son `grados`, `minutos`, `segundos` y `orientación`, donde la orientación puede ser `N` o `S` para **Latitud** y `E` o `W` para **Longitud.**

## Migraciones del Proyecto

Las migraciones de base de datos se manejan automáticamente en el código con SQLAlchemy al iniciar el proyecto. No es necesario nada más ya que están integradas en la aplicación. Simplemente, la base de datos debe estar configurada.

## Pruebas Unitarias

En esta parte se usa la `base_de_datos_de_pruebas` para esto ejecuta:

```bash
export TESTING=1 # En Windows - set TESTING=1
```

Esto es para crear una varible de entonor que cambiara de `base_de_datos` a `base_de_datos_de_pruebas` y para el test ejecuta:

```bash
pytest -v
```

Y para finalmente volver a cambiar a `base_de_datos` ejecuta:

```bash
unset TESTING # En Windows - set TESTING=
```

### Descripción de las Pruebas Realizadas

1. **`test_create_station`**:

   - Esta prueba verifica el funcionamiento del endpoint para crear una estación (`POST/estaciones/`).
2. **`test_read_stations`**:

   - Aquí se verifica que el endpoint de listado de estaciones (`GET/estaciones/`) funcione correctamente.
   - Primero, se crea una estación y luego se realiza una solicitud para obtener todas las estaciones.
   - Comprueba que la respuesta sea `200` y que la cantidad de estaciones coincida con el número de estaciones creadas `2`, confirmanPrimero, crea una estación y luego realiza una solicitud para obtener todas las estaciones.do que el listado incluye la nueva estación.
3. **`test_read_estation_nearest`**:

   - Esta prueba verifica el endpoint que encuentra la estación más cercana (`GET/estaciones/cercana/<id>`).
   - Después de crear una estación de prueba adicional, realiza una solicitud para encontrar la estación más cercana a la estación con el `id` especificado, y valida que el endpoint responda correctamente con un código `200`.
4. **`test_read_estation_nearest_comparison`**:

   - Esta prueba realiza una comparación entre el resultado de la estación más cercana obtenida mediante dos métodos diferentes: un algoritmo de fuerza bruta y el método `KD-Tree`.
   - Compara los resultados para asegurarse de que ambos métodos devuelvan la misma estación más cercana, si `KD-Tree` da el mismo que fuerza bruta signifca que funciona de una manera correcta.
