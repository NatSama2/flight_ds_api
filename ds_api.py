# ds_api.py
# Microservicio de Data Science para FlightOnTime
# Compatible con flight_model_v1.0.4.joblib

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os

app = FastAPI(title="FlightOnTime DS API", version="1.0.5")

# -------------------------
# Cargar modelo
# -------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "flight_model_v1.0.5.joblib")

try:
    print("Intentando cargar modelo desde:", MODEL_PATH)
    model = joblib.load(MODEL_PATH)
    print("Modelo cargado correctamente")
except Exception as e:
    print("ERROR CARGANDO MODELO ↓↓↓")
    print(type(e))
    print(e)
    model = None

# -------------------------
# DTO de entrada
# -------------------------

class FlightInput(BaseModel):
    aerolinea: str
    origen: str
    destino: str
    fecha_partida: str  # ISO 8601
    distancia_km: float

# -------------------------
# Utils
# -------------------------

def tramo_horario(h: int) -> str:
    if 5 <= h < 12:
        return "mañana"
    elif 12 <= h < 18:
        return "tarde"
    elif 18 <= h < 23:
        return "noche"
    else:
        return "madrugada"

# -------------------------
# Endpoint principal
# -------------------------

@app.post("/predict")
def predict_flight(data: FlightInput):
    if model is None:
        raise HTTPException(status_code=500, detail="Modelo no cargado")

    try:
        # Convertir input a DataFrame
        df = pd.DataFrame([{
            "aerolinea": data.aerolinea.lower().strip(),
            "origen": data.origen.lower().strip(),
            "destino": data.destino.lower().strip(),
            "fecha_partida": data.fecha_partida,
            "distancia_km": data.distancia_km
        }])

        # Parse fecha
        df["fecha_partida"] = pd.to_datetime(df["fecha_partida"], errors="coerce")

        if df["fecha_partida"].isnull().any():
            raise ValueError("Formato de fecha inválido. Usa ISO 8601.")

        # Feature engineering
        df["hora"] = df["fecha_partida"].dt.hour
        df["dia_semana"] = df["fecha_partida"].dt.dayofweek
        df["mes"] = df["fecha_partida"].dt.month
        df["tramo"] = df["hora"].apply(tramo_horario)

        # Mantener solo columnas del modelo
        df_model = df[[
            "aerolinea",
            "origen",
            "destino",
            "distancia_km",
            "hora",
            "dia_semana",
            "mes",
            "tramo"
        ]]

        # Predicción
        proba = model.predict_proba(df_model)[0][1]

        # Threshold de riesgo (decisión de negocio)
        threshold = 0.4
        prevision = "Retrasado" if proba >= threshold else "Puntual"

        return {
            "prevision": prevision,
            "probabilidad": round(float(proba), 2)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------
# Health check
# -------------------------

@app.get("/health")
def health():
    return {"status": "ok"}