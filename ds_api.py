# ds_api.py
# Microservicio de Data Science para FlightOnTime
# Carga el modelo flight_model_v1.0.0.joblib y expone un endpoint /predict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI(title="FlightOnTime DS API", version="1.0.0")

# Ruta al modelo
MODEL_PATH = "models/flight_model_v1.0.0.joblib"

# Cargar modelo al iniciar la app
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    print("Error cargando el modelo:", e)
    model = None


# -------------------------
# DTOs (contrato de entrada)
# -------------------------
class FlightInput(BaseModel):
    aerolinea: str
    origen: str
    destino: str
    fecha_partida: str  # ISO 8601: 2025-11-10T14:30:00
    distancia_km: float


# -------------------------
# Endpoint principal
# -------------------------
@app.post("/predict")
def predict_flight(data: FlightInput):
    if model is None:
        raise HTTPException(status_code=500, detail="Modelo no cargado")

    try:
        # Convertir a DataFrame
        df = pd.DataFrame([data.dict()])

        # Predicción
        proba = model.predict_proba(df)[0][1]
        pred = model.predict(df)[0]

        return {
            "prevision": "Retrasado" if int(pred) == 1 else "Puntual",
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
