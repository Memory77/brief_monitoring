Monitoring d'une API de Machine Learning avec Prometheus, Grafana et Evidently
Description

Ce projet met en place un système de monitoring complet pour une API Machine Learning. Il inclut :

    Le suivi des métriques de l'API (taux d'erreur, latence, nombre de requêtes).
    L'analyse des dérives de données (Data Drift) à l'aide de Prometheus.
    La visualisation des métriques dans des tableaux de bord Grafana.
    Le suivi des performances système (CPU, mémoire, espace disque).

Objectifs

    Déployer une API REST avec FastAPI pour la prédiction.
    Collecter les métriques de l'API et des dérives de données.
    Visualiser les performances de l'API et les ressources système.
    Mettre en place un pipeline de monitoring prêt pour un environnement de production.

Fonctionnalités

    Prédictions avec l'API :
        Un endpoint /predict reçoit les données et retourne une prédiction.
    Monitoring de l'API :
        Collecte de métriques (temps de réponse, taux d'erreurs).
    Analyse des dérives des données :
        Suivi des dérives avec des métriques calculées directement (sans générer un rapport HTML).
    Suivi des ressources système :
        Collecte des métriques système via node-exporter.
    Visualisation dans Grafana :
        Création de tableaux de bord pour suivre les performances de l'API et les ressources système.

Architecture

L'application repose sur plusieurs services orchestrés avec Docker Compose :

    API (FastAPI) : Fournit le service de prédiction et expose des métriques Prometheus.
    Prometheus : Collecte les métriques de l'API et des ressources système.
    Grafana : Visualise les métriques dans des tableaux de bord interactifs.
    Node-exporter : Collecte les métriques des ressources système (CPU, mémoire, disque).

Prérequis

    Docker et Docker Compose installés.
    Python 3.9+ pour le développement local.
    Fichier de données de référence pour les prédictions (ex. diabetes.csv).

Installation

    Cloner le projet :

git clone https://github.com/nom_utilisateur/projet_monitoring.git
cd projet_monitoring

Créer un dossier pour les rapports (facultatif) :

mkdir reports

Démarrer les services avec Docker Compose :

    docker-compose up --build

    Accéder aux services :
        API : http://localhost:8000
        Prometheus : http://localhost:9090
        Grafana : http://localhost:3000 (Identifiants par défaut : admin/admin)

Utilisation
1. API
Endpoint /predict

    Effectue une prédiction avec les données fournies.

    Exemple :

curl -X POST "http://localhost:8000/predict" \
-H "Content-Type: application/json" \
-d '{
    "Pregnancies": 1,
    "Glucose": 120,
    "BloodPressure": 70,
    "SkinThickness": 23,
    "Insulin": 94,
    "BMI": 33.6,
    "DiabetesPedigreeFunction": 0.627,
    "Age": 50
}'

Réponse :

    {"prediction": 1}

2. Prometheus
Collecte des métriques :

    Métriques API :
        http_requests_total : Nombre total de requêtes reçues.
        http_request_duration_seconds : Temps de réponse des requêtes.
    Métriques Data Drift :
        data_drift_score : Score de dérive calculé à partir des données actuelles et de référence.

Ajouter les métriques dans prometheus.yml :

global:
  scrape_interval: 5s

scrape_configs:
  - job_name: "fastapi"
    static_configs:
      - targets: ["api:8000"]

  - job_name: "node-exporter"
    static_configs:
      - targets: ["node-exporter:9100"]

3. Grafana

    Connecter Prometheus comme source de données :
        URL de Prometheus : http://prometheus:9090
    Créer ou importer des tableaux de bord :
        Métriques API : Latence, volume de requêtes, taux d'erreurs.
        Métriques système : CPU, mémoire, espace disque.

Structure du Projet

.
├── api/                     # Code de l'API
│   ├── main.py              # Fichier principal de l'API
│   └── requirements.txt     # Dépendances Python
├── prometheus.yml           # Configuration de Prometheus
├── grafana/                 # Fichiers de configuration Grafana (si nécessaires)
├── reports/                 # Dossier pour les rapports
├── docker-compose.yml       # Orchestration des services
├── Dockerfile               # Conteneurisation de l'API
└── README.md                # Documentation du projet

Métriques Disponibles

    API :
        Nombre total de requêtes : http_requests_total
        Temps de réponse des requêtes : http_request_duration_seconds
        Taux d'erreurs : calculé à partir des codes HTTP.
    Dérives des données :
        Score de Data Drift : data_drift_score.
    Système :
        CPU : node_cpu_seconds_total.
        Mémoire : node_memory_MemAvailable_bytes.
        Espace disque : node_filesystem_avail_bytes.
