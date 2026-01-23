# 🧠 Microservicio Data Science — FlightOnTime

> ⚠️ Esta es la **API oficial y activa** del proyecto FlightOnTime.  
> Todas las predicciones deben consumirse desde este servicio.

Este microservicio permite exponer el modelo de Machine Learning entrenado por el equipo de Data Science como una API REST, para que el backend pueda consumirlo sin necesidad de interactuar directamente con el archivo `.joblib`.

---

## 📦 ¿Qué contiene este servicio?

- Modelo serializado: `flight_model_v1.0.5.joblib`
- API en Python (FastAPI)
- Endpoint `/predict`
- Endpoint `/health`
- Validación básica de datos
- Manejo de errores
- Contrato claro de entrada y salida

---

## 🏗️ Estructura del proyecto

```
flight_ds_api/
│
├── ds_api.py
├── models/
│   └── flight_model_v1.0.0.joblib
└── requirements.txt
```

---

## 📥 Clonar y ejecutar

```bash
git clone https://github.com/NatSama2/flight_ds_api
cd flight_ds_api
```

---

## ⬇️ Descargar el modelo (PASO OBLIGATORIO)

Debido al tamaño del archivo, el modelo no está incluido en el repositorio.  
Debes descargarlo manualmente desde el siguiente enlace:

🔗 **Descargar modelo:**  
https://drive.google.com/file/d/1MwLAo6WjdL6uHhcRdHwvo2ju-EXOFsTX/view?usp=drive_link

Una vez descargado:

Asegúrate de que el archivo se llame:

```bash

flight_model_v1.0.5.joblib

```

Colócalo dentro de la carpeta:

```bash

flight_ds_api/models/

```

El proyecto no funcionará sin este archivo.

---

## 🚀 Cómo ejecutar el microservicio

### 1️⃣ Crear entorno (opcional pero recomendado)

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

---

### 2️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Ejecutar el servidor

```bash
uvicorn ds_api:app --reload
```

La API quedará disponible en:

```
http://localhost:8000
```

---

## 📡 Endpoints

### 🔹 Health check

**GET** `/health`

Respuesta:

```json
{
  "status": "ok"
}
```

---

### 🔹 Predicción

**POST** `/predict`

#### Request

```json
{
  "aerolinea": "AZ",
  "origen": "GIG",
  "destino": "GRU",
  "fecha_partida": "2025-11-10T14:30:00",
  "distancia_km": 350
}
```

---

#### Response

```json
{
  "prevision": "Retrasado",
  "probabilidad": 0.78
}
```

---

## 🔌 ¿Cómo se integra con el backend?

El backend (Spring Boot) **NO debe interactuar con el archivo `.joblib` directamente**.

Debe:

1. Recibir el request del usuario
2. Validar datos
3. Enviar el JSON a este microservicio (POST /predict)
4. Recibir la respuesta
5. Retornarla al frontend

### Flujo completo

```
Usuario → Backend (Java) → Microservicio DS (Python) → Modelo → Respuesta
```

---

## ⚠️ Importante

Este microservicio garantiza que:

- El mismo pipeline usado en entrenamiento se use en producción
- No haya errores de columnas
- No haya inconsistencias en el preprocesamiento
- El backend no tenga que manejar ML

---

## 🛠️ Tecnologías

- Python 3.10+
- FastAPI
- Pandas
- Scikit-learn
- Joblib
- Uvicorn

---

## 👩‍💻 Equipo Data Science

- Giselle Cifuentes
- Karen Sofia Rodriguez
- Karen Guerrero González

## 👨‍💻 Equipo Backend Developer

- Daniel Jiménez
- Lester Hartman Myers González
- Jorge Satomi Minami Aguilera
- Rosa Estrella Calderon Rodriguez

---

## 📌 Estado del proyecto

Este microservicio corresponde a una versión MVP. La conexión con el backend está implementada, pero aún puede presentar inestabilidades. La integración definitiva debe realizarse consumiendo este servicio como fuente única de predicción.

---
