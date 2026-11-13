import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import httpx
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://www.infoclimat.fr/opendata/"

TOKEN = os.getenv("INFOCLIMAT_TOKEN")
STATION = os.getenv("INFOCLIMAT_STATION")


async def get_weather():

    if not TOKEN or not STATION:
        raise ValueError("Token ou identifiant de station manquant.")

    #On récupère sur la semaine car pas autorisé par API au dessus d'un mois.
    today = datetime.now(ZoneInfo("Europe/Paris")).date()

    end_date = today
    start_date = today - timedelta(days=4)

    params = {
        "method": "get",
        "format": "json",
        "stations[]": STATION,
        "start": start_date.isoformat(),
        "end": end_date.isoformat(),
        "token": TOKEN,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:

        response = await client.get(API_URL, params=params)
        response.raise_for_status()

    try:
        data = response.json()
    except ValueError as exc:
        raise ValueError(
            "Infoclimat n'a pas retourné un JSON valide."
        ) from exc

    if data.get("errors"):
        raise ValueError(
            f"Erreur Infoclimat : {data['errors']}"
        )

    return data