from fastapi import FastAPI, Query
import fastf1
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()  # PRIMERO, define la app

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite TODO durante el test
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/compare")
def compare_telemetry(
    driver1: str = Query(..., alias="driver1"),
    driver2: str = Query(..., alias="driver2"),
    event: str = "Monza", 
    year: int = 2023,
    session_type: str = "Q"
):
    fastf1.Cache.enable_cache('cache')
    session = fastf1.get_session(year, event, session_type)
    session.load()
    lap1 = session.laps.pick_drivers(driver1).pick_fastest()
    lap2 = session.laps.pick_drivers(driver2).pick_fastest()
    tel1 = lap1.get_car_data().add_distance()
    tel2 = lap2.get_car_data().add_distance()
    return {
        "driver1": {
            "name": driver1,
            "distance": tel1['Distance'].tolist(),
            "speed": tel1['Speed'].tolist()
        },
        "driver2": {
            "name": driver2,
            "distance": tel2['Distance'].tolist(),
            "speed": tel2['Speed'].tolist()
        }
    }

@app.get("/strategy")
def driver_strategy(
    driver: str = Query(..., alias="driver"),
    event: str = "Monza",
    year: int = 2023, 
    session_type: str = "R"
):
    fastf1.Cache.enable_cache('cache')
    session = fastf1.get_session(year, event, session_type)
    session.load()
    laps = session.laps.pick_drivers(driver)
    stints = laps.get_stints().to_dict(orient='records')
    pitstops = laps[laps['PitInTime'].notna()][['LapNumber', 'PitInTime', 'PitOutTime']].to_dict(orient='records')
    return {
        "stints": stints,
        "pitstops": pitstops
    }
