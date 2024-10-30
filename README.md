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

La API estará disponible en [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### Manual de Uso

Debes ver algo tal que así:

![1730315274543](image/README/1730315274543.png)

En este apartado se puede ver el `POST/estaciones/`, `GET/estaciones/` y `GET/estaciones/cercana/{station_id}`.

**Para `POST/estaciones/:`**

Desplegamos la vista de `POST/estaciones/` dando click en ella, luego se preciona donde dice `Try it out` en la izquina superior derecha y se vera algo asi:

![1730315683984](image/README/1730315683984.png)

Para ingresar datos tenemos 2 maneras:

1. Ingresar la ubicación en **Coordenadas Cartesianas:**
   * Para esto se dara un nombre y las coordenadas asi:
   * ```json
     {"name": "Nombre Estación",
     "location": [
     "Latitude",
     "Longitude"
     ],
     "option": 0
     }
     ```
   * La `Latitude` y `Longitude` se dan como strings y `option` es `0` indicando que se usan coordenadas cartesianas, ejemplo:
   * ```json
     {"name": "Estación A",
     "location": [
     "43.709212",
     "52.187213"
     ],
     "option": 0
     }
     ```

     > **Advertencia:** Solo se pueden tener maximo `6` decimales para el manejo correcto de coordenadas
     >
2. Ingresar la ubicación en **Coordenadas Geografica:**
   * Para esto se dara un nombre y las coordenadas asi:
   * ```json
     {"name": "Nombre Estación",
     "location": [
     "Latitude",
     "Longitude"
     ],
     "option": 1
     }
     ```
   * La `Latitude` y `Longitude` se dan como strings y `option` es `1` indicando que se usan coordenadas geograficas, ejemplo:
   * ```json
     {"name": "Estación B",
     "location": [
     "60°70'92''N",
     "9°87'45''W"
     ],
     "option": 1
     }
     ```

     > **Advertencia:** Siempre se debe cumplir la notación `xx°xx'xx''x` de `grados`, `minutos`, `segundos` y `orientación` respectivamente.
     >

Una vez dados los datos se presiona en el boton `Execute` en la parte de abajo y en el apartado de `Responses` algo asi:

![1730317039297](image/README/1730317039297.png)

**Para `GET/estaciones/`:**

Desplegamos la vista de `GET/estaciones/` dando click en ella, luego se preciona donde dice `Try it out` en la izquina superior derecha y se vera algo asi:

![1730317190814](image/README/1730317190814.png)

Le damos un `skip` para saber desde que `id` debe empezar a mostrar y un `limit` para saber cuantas estaciones mostrar, finalmente se selecciona `Execute` y vemos el resultado en `Responses`, debe ser algo asi:

![1730317330829](image/README/1730317330829.png)

**Para `GET/estaciones/cercana/{station_id}`:**

Desplegamos la vista de `GET/estaciones/cercana/{station_id}` dando click en ella, luego se preciona donde dice `Try it out` en la izquina superior derecha y se vera algo asi:

![1730317416082](image/README/1730317416082.png)

Se le da la `id` de la estación a la que le queremos buscar la estación más cercana y se selecciona `Execute`, este método usara el `Algoritmo KD-Tree` para encontrar la solución con una complejidad temporal de `O(Log n)`. En el apartado de `Responses` se debe ver algo asi:

![1730317747848](image/README/1730317747848.png)

Nos dara una lista donde el primero elemento es la estación a la que se le busca la más cercana y el segundo elemento es la estación más cercana a ese primer elemento.

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
