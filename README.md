# Comparador de Telemetría y Estrategias F1

Proyecto desarrollado con **FastAPI** (backend) y **React** (frontend) para comparar la telemetría y analizar estrategias de pilotos de F1 en diferentes eventos y temporadas.

## Funcionalidades principales

- Comparación gráfica de telemetría (velocidad vs. distancia) entre dos pilotos, evento, año y sesión elegibles.
- Análisis de estrategia de stints y pitstops para cualquier piloto, evento y año disponibles en fastf1.
- Visualización tabular dinámica de stints (compuesto y vueltas) y pitstops (vuelta, entrada, salida).

## Tecnologías utilizadas

- **Backend:** Python 3, FastAPI, FastF1, Pandas
- **Frontend:** React (o tu stack elegido)
- **Visualización:** Recharts/Chart.js (según implementación), tablas dinámicas
- **API REST:** Documentación automática con Swagger (`/docs` de FastAPI)
  
## Estructura del backend

- `main.py`: Contiene los endpoints `/compare` (telemetría) y `/strategy` (stints/pitstops).  
  La lógica de `/strategy` es totalmente compatible incluso con versiones de FastF1 sin método `get_stints`.

## Ejemplo de uso

1. Selecciona dos pilotos, evento, año y sesión en el frontend para visualizar la telemetría comparada durante una vuelta rápida.
2. Consulta la estrategia de stints y pitstops de cualquier piloto en cualquier evento/año disponible.
3. Los datos se obtienen en tiempo real usando FastF1 y se representan automáticamente según elección del usuario.

## Instalación (modo desarrollo)

1. Clona el repositorio:
    ```
    git clone <URL DEL REPO>
    cd <carpeta>
    ```
2. Instala las dependencias Python:
    ```
    pip install fastapi fastf1 uvicorn pandas
    ```
3. Lanza el backend:
    ```
    uvicorn main:app --reload
    ```
4. Lanza el frontend (si es React):
    ```
    npm install
    npm start
    ```
5. Accede a la app en tu navegador y ¡explora telemetría y estrategias dinámicas!

## Créditos y base de datos

- Este proyecto usa la API de datos de F1 abierta **FastF1**.
- Inspirado en prácticas de ciencia de datos y visualización interactiva para análisis deportivo.

---

## Ejemplo de commit en Git

Una vez que agregues/actualices tu README y los archivos modificados, ejecuta en tu terminal:

