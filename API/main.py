
import httpx

from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from API.infoclimat import get_weather
from Database.database import engine, Base, get_db
from Database.table import ObservationMeteo


#Création des tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="API Météo",
    description="Données météo provenant d'Infoclimat",
    version="1.0.0"
)


@app.get("/")
async def home():
    return {
        "message": "API météo opérationnelle"
    }


#Récupération des données météo
@app.get("/api/meteo")
async def meteo():
    try:
        data = await get_weather()
        return data

    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Erreur API Infoclimat : {str(exc)}"
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


#Importation des données dans SQLite
@app.post("/api/meteo/import")
async def importer_meteo(db: Session = Depends(get_db)):

    try:
        #Récupération des données Infoclimat
        data = await get_weather()

        hourly = data.get("hourly", {})

        if not isinstance(hourly, dict):
            raise ValueError("Format des données horaires invalide.")

        nombre_importe = 0
        nombre_doublons = 0

        for station_id, observations in hourly.items():

            if station_id.startswith("_"):
                continue

            #Parcours des observations horaires
            for item in observations:

                date_obs = datetime.strptime(
                    item["dh_utc"],
                    "%Y-%m-%d %H:%M:%S"
                )

                #Vérification des doublons
                existe = db.query(ObservationMeteo).filter(
                    ObservationMeteo.station == station_id,
                    ObservationMeteo.date_observation == date_obs
                ).first()

                if existe:
                    nombre_doublons += 1
                    continue

                #Création de l'observation
                observation = ObservationMeteo(
                    station=station_id,
                    date_observation=date_obs,
                    temperature=item.get("temperature"),
                    pression=item.get("pression"),
                    humidite=item.get("humidite"),
                    point_de_rosee=item.get("point_de_rosee"),
                    vent_moyen=item.get("vent_moyen"),
                    vent_rafales=item.get("vent_rafales"),
                    vent_direction=item.get("vent_direction"),
                    pluie_1h=item.get("pluie_1h"),
                    pluie_3h=item.get("pluie_3h")
                )

                db.add(observation)
                nombre_importe += 1

        #Enregistrement dans SQLite
        db.commit()

        return {
            "message": "Importation terminée",
            "observations_importees": nombre_importe,
            "doublons_ignores": nombre_doublons
        }

    except httpx.HTTPError as exc:
        db.rollback()
        raise HTTPException(
            status_code=502,
            detail=f"Erreur API Infoclimat : {str(exc)}"
        )

    except ValueError as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )

    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'importation : {str(exc)}"
        )
