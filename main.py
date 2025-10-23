from fastapi import FastAPI, Query
import fastf1
from fastapi.middleware.cors import CORSMiddleware
import math

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/compare")
def compare_telemetry(
    driver1: str = Query(...),
    driver2: str = Query(...),
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
    driver: str = Query(...),
    event: str = "Monza",
    year: int = 2023, 
    session_type: str = "R"
):
    fastf1.Cache.enable_cache('cache')
    session = fastf1.get_session(year, event, session_type)
    session.load()
    laps = session.laps
    pilot_laps = laps[laps['Driver'] == driver]

    if 'Stint' in laps.columns and 'Compound' in laps.columns:
        stints_pilot = pilot_laps.groupby('Stint').agg({
            'Compound': 'first',
            'LapNumber': 'count'
        }).reset_index().rename(columns={'LapNumber': 'TotalLaps'})
        driver_stints = [{
            'Stint': int(row['Stint']),
            'Compound': row['Compound'],
            'TotalLaps': int(row['TotalLaps'])
        } for _, row in stints_pilot.iterrows()]
    else:
        driver_stints = []

    pitstops = []
    if "PitInTime" in pilot_laps.columns and "PitOutTime" in pilot_laps.columns:
        pitstops = pilot_laps[pilot_laps['PitInTime'].notna()][['LapNumber', 'PitInTime', 'PitOutTime']].to_dict(orient='records')

    return {
        "stints": driver_stints,
        "pitstops": pitstops
    }

@app.get("/mapdata")
def map_data(driver: str, event: str, year: int):
    fastf1.Cache.enable_cache('cache')
    session = fastf1.get_session(year, event, "Q")
    session.load()
    lap = session.laps.pick_drivers(driver).pick_fastest()
    tel = lap.get_car_data().add_distance()
    print("Columnas telemetría:", tel.columns)
    print("Cantidad de filas:", len(tel))
    # Verifica que X y Y están presentes y tienen datos
    if "X" not in tel.columns or "Y" not in tel.columns:
        print("No hay columnas X/Y")
        return {"x": [], "y": [], "speed": []}
    if tel['X'].isna().all() or tel['Y'].isna().all():
        print("Todas las X/Y son NaN")
        return {"x": [], "y": [], "speed": []}
    # Filtra NaNs
    valid = tel[['X', 'Y', 'Speed']].dropna()
    return {
        "x": valid['X'].tolist(),
        "y": valid['Y'].tolist(),
        "speed": valid['Speed'].tolist()
    }


@app.get("/pitscompare")
def pits_compare(drivers: str, event: str, year: int):
    fastf1.Cache.enable_cache('cache')
    session = fastf1.get_session(year, event, "R")
    session.load()
    results = []
    for d in drivers.split(","):
        laps = session.laps[session.laps['Driver'] == d]
        pitlaps = laps[laps['PitInTime'].notna()]
        for _, p in pitlaps.iterrows():
            pit_in = p['PitInTime']
            pit_out = p['PitOutTime']
            duration = None
            if pit_in is not None and pit_out is not None:
                try:
                    duration = (pit_out - pit_in).total_seconds()
                    # Validar que duration sea una cifra válida:
                    if math.isnan(duration) or math.isinf(duration):
                        duration = None
                except Exception:
                    duration = None
            results.append({
                "driver": d,
                "pitlap": int(p['LapNumber']),
                "duration": duration
            })
    return results


@app.get("/delta")
def delta_times(driver1: str, driver2: str, event: str, year: int):
    import numpy as np

    fastf1.Cache.enable_cache('cache')
    session = fastf1.get_session(year, event, "R")
    session.load()
    laps1 = session.laps[session.laps['Driver'] == driver1]
    laps2 = session.laps[session.laps['Driver'] == driver2]
    max_lap1 = int(laps1['LapNumber'].max())
    max_lap2 = int(laps2['LapNumber'].max())
    data = []
    for lapnum in range(1, min(max_lap1, max_lap2)+1):
        l1 = laps1[laps1['LapNumber'] == lapnum]
        l2 = laps2[laps2['LapNumber'] == lapnum]
        def get_seconds(row):
            if row.empty or row['LapTime'].isna().values[0]:
                return None
            val = row['LapTime'].values[0]
            # Si el valor es numpy.timedelta64:
            if isinstance(val, np.timedelta64):
                return float(val / np.timedelta64(1, 's'))
            return val.total_seconds() if hasattr(val, "total_seconds") else None
        time1 = get_seconds(l1)
        time2 = get_seconds(l2)
        delta = (time2 - time1) if time1 is not None and time2 is not None else None
        data.append({
            "lap": lapnum,
            driver1: time1,
            driver2: time2,
            "delta": delta
        })
    return data
