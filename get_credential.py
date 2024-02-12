import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()


#ce script sert à récupérer le token d'accès pour l'API Twitch

client_id = 
client_secret = 

# Demande pour obtenir le token
response = requests.post(
    'https://id.twitch.tv/oauth2/token',
    params={
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
)

# Vérifiez que la requête a réussi
if response.status_code == 200:
    response_json = response.json()
    access_token = response_json['access_token']
    
    with open('.env', 'a') as f:
        f.write(f"ACCESS_TOKEN={access_token}\n")

    print("Le token d'accès a été récupéré et stocké dans .env")
else:
    print(f"Erreur lors de la demande du token, code d'état: {response.status_code}")
