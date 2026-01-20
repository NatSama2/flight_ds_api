# ds_api.py
# Microservicio de Data Science para FlightOnTime
# Carga el modelo flight_model_v1.0.1.joblib y expone un endpoint /predict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os

app = FastAPI(title="FlightOnTime DS API", version="1.0.1")

# -------------------------
# Cargar modelo correctamente
# -------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "flight_model_v1.0.1.joblib")

try:
    print("Intentando cargar modelo desde:", MODEL_PATH)
    model = joblib.load(MODEL_PATH)
    print("Modelo cargado correctamente")
except Exception as e:
    print("ERROR REAL CARGANDO MODELO ↓↓↓")
    print(type(e))
    print(e)
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

        # Normalizar texto igual que en entrenamiento
        df["aerolinea"] = df["aerolinea"].str.lower().str.strip()
        df["origen"] = df["origen"].str.lower().str.strip()
        df["destino"] = df["destino"].str.lower().str.strip()

        # One-hot encoding de columnas categóricas
        df = pd.get_dummies(df, columns=["aerolinea", "origen", "destino"], drop_first=True, dtype=int)

        # Alinear columnas con las del modelo
        model_columns = model.named_steps["model"].coef_.shape[1]  # Opción genérica
        if hasattr(model, "feature_names_in_"):
            expected_cols = model.feature_names_in_
            df = df.reindex(columns=expected_cols, fill_value=0)

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
