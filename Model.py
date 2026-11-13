
import json
import sqlite3
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

#la variable est utilisé dans le chargement/entrainement du modèle et pour la prediction.
FEATURES = [
    "temperature",
    "pression",
    "humidite",
    "point_de_rosee",
    "vent_moyen",
    "vent_direction"
]

def predict_next_hour(data, model):

    latest_data = data.sort_index().iloc[[-1]]

    X_prediction = latest_data[FEATURES]


    prediction = model.predict(X_prediction)[0]

    print("\n--- PRÉVISION POUR LA PROCHAINE HEURE ---")
    print("Dernier relevé :", latest_data.index[0])

    if prediction == 1:
        print("Il va pleuvoir dans la prochaine heure.")
    else:
        print("Il ne va pas pleuvoir dans la prochaine heure.")

    return prediction

def entrainerModel():

    #Charger les données
    conn = sqlite3.connect("weather.db")

    data = pd.read_sql_query(
        "SELECT * FROM observations_meteo",
        conn
    )

    conn.close()

    #Préparer les dates
    data["date_observation"] = pd.to_datetime(data["date_observation"])
    data = data.sort_values("date_observation")
    data = data.set_index("date_observation")


    #Pluie pendant l'heure suivante
    target = data["pluie_1h"].copy()
    target.index = target.index - pd.Timedelta(hours=1)

    data["pluie_prochaine_heure"] = target

    #Nettoyer les données
    data = data.dropna(
        subset=FEATURES + ["pluie_prochaine_heure"]
    )

    #Transformer la cible en classification binaire
    data["pluie_prochaine_heure"] = (
        data["pluie_prochaine_heure"] > 0
    ).astype(int)

    X = data[FEATURES]
    y = data["pluie_prochaine_heure"]

    #Entrainement
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        shuffle=False
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    )

    model.fit(X_train, y_train)

    #Évaluer le modèle
    predictions = model.predict(X_test)

    print("\nAccuracy :", accuracy_score(y_test, predictions))
    print("\nRapport de classification :")
    print(classification_report(y_test, predictions))
    print("\nMatrice de confusion :")
    print(confusion_matrix(y_test, predictions))

    #Sauvegarder le modèle
    import joblib
    joblib.dump(model, "modele_pluie.pkl")

    print("\nModèle sauvegardé !")
    return predict_next_hour(data, model)



