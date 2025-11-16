# Proyecto de Microservicios AEMET

Una API RESTful construida con Flask y Docker que expone datos meteorológicos, geográficos y demográficos de municipios españoles, utilizando la API de AEMET OpenData.

## Arquitectura

Este proyecto sigue una arquitectura de microservicios, orquestada con Docker Compose. Cada servicio se ejecuta en su propio contenedor Docker y se comunican a través de una red interna.

- **Servicio Base (`getmunicipio`):** Proporciona datos básicos desde un fichero local.
- **Servicio Geográfico (`getgeomunicipio`):** Proporciona datos de latitud/longitud desde AEMET.
- **Servicio Meteorológico (`getmeteomunicipio`):** Proporciona datos del tiempo actual desde AEMET.
- **Servicio Demográfico (`getdemomunicipio`):** Proporciona datos demográficos desde un fichero local y la API de AEMET.
- **Servicio Orquestador (`getvariosmunicipio`):** Combina las respuestas de los otros servicios.

## Prerrequisitos

- Python
- Docker
  
## Cómo Empezar

Sigue estos pasos para levantar el entorno completo en tu máquina local.

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/tu-usuario/aemet-microservices-api.git
    cd aemet-microservices-api
    ```

2.  **Configura las variables de entorno:**
    Crea un fichero `.env`
    
    Ahora, edita el fichero `.env` y añade tu [API Key de AEMET](https://opendata.aemet.es/centrodedescargas/altaUsuario):
    ```
    AEMET_API_KEY="eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOi..."
    ```

4.  **Construye y levanta los contenedores:**
    ```bash
    docker-compose up --build
    ```

¡Listo! Los servicios estarán disponibles en los puertos `5001` a `5005` de tu `localhost`.

## Endpoints de la API

Aquí tienes algunos ejemplos de cómo usar la API:

- **Obtener datos básicos:** `GET http://localhost:5001/cordoba`
- **Obtener datos geográficos:** `GET http://localhost:5002/cordoba/geo`
- **Orquestar servicios:** `GET http://localhost:5005/cordoba/geo/demo`

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el fichero [LICENSE](LICENSE) para más detalles.
