import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

#ce script sert à récupérer les broadcaster_ids des streamers dans le fichier TopStreamerFR.txt

# Vos identifiants
client_id = os.getenv("CLIENT_ID")
access_token = os.getenv("ACCESS_TOKEN")

# En-têtes pour la requête API
headers = {
    'Client-ID': client_id,
    'Authorization': f'Bearer {access_token}'
}

# Lire le fichier original avec les noms des streamers
with open('TopStreamerFR.txt', 'r') as f:
    streamer_names = f.readlines()

# Retirer les sauts de ligne
streamer_names = [name.strip() for name in streamer_names]

# Dictionnaire pour stocker les broadcaster_ids
streamer_ids = {}

# Récupérer les broadcaster_ids
for name in streamer_names:
    params = {
        'login': name.lower()  # Les noms d'utilisateur Twitch sont insensibles à la casse
    }

    response = requests.get(
        'https://api.twitch.tv/helix/users',
        headers=headers,
        params=params
    )

    if response.status_code == 200:
        user_data = json.loads(response.text)['data']
        if user_data:
            streamer_ids[name] = user_data[0]['id']
    else:
        print(f"Erreur lors de la récupération de l'ID pour {name}, code d'état: {response.status_code}")

# Écrire les résultats dans un nouveau fichier
with open('TopStreamerFR_with_ids.txt', 'w') as f:
    for name, streamer_id in streamer_ids.items():
        f.write(f"{name},{streamer_id}\n")

print("Les broadcaster_ids ont été récupérés et stockés dans TopStreamerFR_with_ids.txt")
