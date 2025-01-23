# #!/bin/bash

curl -X POST "http://10.2.0.188:8000/predict" \
-H "Content-Type: application/json" \
-d '{
    "Pregnancies": 1,
    "Glucose": 20,
    "BloodPressure": 70,
    "SkinThickness": 23,
    "Insulin": 94,
    "BMI": 33.6,
    "DiabetesPedigreeFunction": 0.627,
    "Age": 50
}'


#confirmer que l'API expose bien des métriques, tu peux visiter directement /metrics de l'API 
#ton API a d'autres endpoints comme /predict etc., le /metrics est un endpoint supplémentaire ajouté par l'instrumentation
#curl http://10.2.0.188:8000/metrics