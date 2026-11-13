import tkinter as tk
import subprocess
import sys
import requests
import Model
import API.infoclimat as infoclimat
import API.main as main


process_api = None

def start_api():
    global process_api

    if process_api is not None and process_api.poll() is None:
        print("Le serveur API est déjà démarré.")
        return

    process_api = subprocess.Popen([
        sys.executable,
        "-m",
        "uvicorn",
        "API.main:app",
        "--host", "127.0.0.1",
        "--port", "8000"
    ])

    print("Démarrage du serveur API...")



def download_meteo():
    try:
        response = requests.post(
            "http://127.0.0.1:8000/api/meteo/import",
            timeout=120
        )

        response.raise_for_status()

        result = response.json()

        print("Importation terminée !")

    except requests.exceptions.RequestException as e:
        print("Erreur lors de l'importation :", e)


root = tk.Tk()
label = tk.Label(root, text="text")

def prediction():
    prediction = Model.entrainerModel()
    label.configure(text = prediction)
    label.pack()
    



buttonAPI = tk.Button(root, text="StartAPI", width=25, command=start_api)
buttonAPI.pack()

buttonDownload = tk.Button(root, text="Télécharger les données", width=25, command=download_meteo)
buttonDownload.pack()

buttonPrediction = tk.Button(root, text="Prediction", width=25, command= Model.entrainerModel)
buttonPrediction.pack()

label.pack()

root.mainloop()

