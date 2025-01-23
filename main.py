from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
import os
from prometheus_client import Gauge, generate_latest, REGISTRY
from prometheus_fastapi_instrumentator import Instrumentator

# Charger le modèle
model = joblib.load('model.pkl')

# Initialiser l'application FastAPI
app = FastAPI()

# Configurer Prometheus
Instrumentator().instrument(app).expose(app)

# Prometheus Gauges
data_drift_gauge = Gauge("data_drift_score", "Score de Data Drift")
concept_drift_gauge = Gauge("concept_drift_score", "Score de Concept Drift")
model_accuracy_gauge = Gauge("model_accuracy", "Précision du modèle")

# Chemins vers les fichiers
CURRENT_DATA_PATH = "current_data.csv"
REFERENCE_DATA_PATH = "diabetes.csv"

# Endpoint pour les prédictions
@app.post("/predict")
async def predict(data: dict):
    try:
        # Convertir les données en DataFrame
        df = pd.DataFrame([data])

        # Enregistrer les données reçues pour les analyses
        df.to_csv(CURRENT_DATA_PATH, mode="a", index=False, header=not os.path.exists(CURRENT_DATA_PATH))

        # Effectuer la prédiction
        prediction = model.predict(df)
        return {"prediction": int(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Fonction pour calculer le Data Drift
def calculate_data_drift(reference_data, current_data):
    # Calcul simple basé sur les moyennes des colonnes (exemple)
    drift_score = ((reference_data.mean() - current_data.mean()) ** 2).sum()
    return drift_score

# Fonction pour calculer la précision du modèle
def calculate_model_performance(reference_data, current_data):
    # Exemple fictif de performance
    return 0.85  # Une précision fixe comme exemple

# Endpoint pour mettre à jour les métriques
@app.get("/update-metrics")
def update_metrics():
    try:
        # Vérifier si le fichier current_data.csv existe
        if not os.path.exists(CURRENT_DATA_PATH):
            raise HTTPException(status_code=404, detail="Aucune donnée courante disponible. Faites des requêtes pour générer des données.")

        # Charger les datasets
        reference_data = pd.read_csv(REFERENCE_DATA_PATH)
        current_data = pd.read_csv(CURRENT_DATA_PATH)

        # Calculer les métriques
        drift_score = calculate_data_drift(reference_data, current_data)
        accuracy_score = calculate_model_performance(reference_data, current_data)

        # Mettre à jour les métriques Prometheus
        data_drift_gauge.set(drift_score)
        model_accuracy_gauge.set(accuracy_score)

        return {"message": "Metrics updated successfully", "data_drift_score": drift_score, "model_accuracy": accuracy_score}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint pour exporter les métriques
@app.get("/metrics")
async def metrics():
    return generate_latest(REGISTRY)







#commande de lancement:
#uvicorn main:app --reload --host 0.0.0.0 --port 8000

# API écoutant sur 0.0.0.0 :
#     Cela signifie que l’API est accessible via toutes les interfaces réseau du PC où elle est exécutée.
#     Par exemple :
#         En local : via http://127.0.0.1:8000 ou http://localhost:8000.
#         Depuis un autre PC du réseau : via l’adresse IP réelle (ex. http://192.168.1.10:8000).
# Depuis un autre PC :
# Si le premier PC a l’adresse IP locale 192.168.1.10, un autre PC du même réseau peut accéder 
# à l’API via http://192.168.1.10:8000.