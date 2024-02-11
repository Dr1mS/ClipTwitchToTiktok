"""
This script retrieves the top 10 clips of the month for each streamer in the TopStreamerFR_with_ids.txt file
and stores them in the BestClipsOfMonth.json file. The script uses the TopStreamerFR_with_ids.txt file which contains
the streamers and their broadcaster_ids.

Functions:
    print_progress_bar(iteration, total, length=50)
    get_game_name(game_id, headers)
"""
import requests
import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv




# Fonction pour afficher la barre de chargement
def print_progress_bar(iteration, total, length=50):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = "=" * filledLength + "-" * (length - filledLength)
    print(f'\rProgress: |{bar}| {percent}%', end='\r')

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer les valeurs depuis les variables d'environnement
client_id = os.getenv('CLIENT_ID')
access_token = os.getenv('ACCESS_TOKEN')


# En-têtes pour la requête API
headers = {
    'Client-ID': client_id,
    'Authorization': f'Bearer {access_token}'
}

# Lire le fichier avec les noms et broadcaster_ids des streamers
with open('TopStreamerFR_with_ids.txt', 'r') as f:
    lines = f.readlines()

# Calculer la date d'il y a 31 jours (format ISO 8601)
one_week_ago = datetime.now() - timedelta(days=31)
started_at = one_week_ago.isoformat() + "Z"  # Ajout du "Z" pour indiquer l'heure UTC

# Liste pour stocker les meilleurs clips
best_clips = []

# Variable pour suivre le nombre total de streamers
total_streamers = len(lines)

# Variable pour suivre le nombre actuel de streamers traités
current_streamer = 0

# Fonction pour obtenir le nom du jeu à partir de game_id
def get_game_name(game_id, headers):
    game_name = None
    response = requests.get(
        f"https://api.twitch.tv/helix/games?id={game_id}",
        headers=headers
    )

    if response.status_code == 200:
        game_data = json.loads(response.text)['data']
        if game_data:
            game_name = game_data[0]['name']
    return game_name

# Pour chaque streamer, récupérez les 10 meilleurs clips de la semaine
for line in lines:
    # Mettre à jour la barre de chargement
    print_progress_bar(current_streamer, total_streamers)
    
    name, broadcaster_id = line.strip().split(',')
    
    params = {
        'broadcaster_id': broadcaster_id,
        'first': 10,  # On prend jusqu'à 10 clips
        'started_at': started_at  # Clips depuis la date calculée
    }
    
    response = requests.get(
        'https://api.twitch.tv/helix/clips',
        headers=headers,
        params=params
    )
    
    if response.status_code == 200:
        clip_data = json.loads(response.text)['data']
        if clip_data:
            for clip in clip_data:
                game_name = get_game_name(clip['game_id'], headers)
                best_clips.append({
                    'url': clip['url'],
                    'streamer': name,
                    'duration': clip['duration'],
                    'title': clip['title'],
                    'game': game_name,
                })
    else:
        print(f"Erreur lors de la récupération des clips pour {name}, code d'état: {response.status_code}")

    # Mettre à jour le compteur du nombre actuel de streamers traités
    current_streamer += 1

# Écrire les résultats dans un nouveau fichier (format JSON pour la simplicité)
with open('BestClipsOfMonth.json', 'w') as f:
    json.dump(best_clips, f)

# Assurez-vous que la barre de progression est complète à 100% à la fin du traitement
print_progress_bar(total_streamers, total_streamers)
print("\nLes meilleurs clips de la semaine ont été récupérés et stockés dans BestClipsOfMonth.json.")
