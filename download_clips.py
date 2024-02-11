import youtube_dl
import os
import json
import time

def download_clip(clip, ydl_opts):
    try:
        url = clip['url']
        streamer = clip['streamer'].replace(" ", "_")
        title = clip['title'].replace(" ", "_")
        game = clip['game'].replace(" ", "_")
        duration = clip['duration']

        filename = f"{streamer}-{game}-{title}-{duration:.2f}.mp4"
        counter = 1
        original_filename = filename

        while os.path.exists(f'{clips_dir}/{filename}'):
            filename = f"{original_filename.split('.')[0]}({counter}).mp4"
            counter += 1

        ydl_opts['outtmpl'] = f'{clips_dir}/{filename}'
        ydl_opts['quiet'] = True

        print(f"Téléchargement en cours de {filename}...")
        # Demarrage de chrono
        start_time = time.time()
        
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            #Le rendre silencieux
            ydl.download([url])
        
        # Temps de fin
        end_time = time.time()
        # Temps total
        total_time = end_time - start_time

        print(f"Téléchargement terminé pour {filename}.\nTemps de téléchargement: {total_time:.2f} secondes\n")

    except Exception as e:
        print(f"Une exception a été levée lors du téléchargement de {url}: {e}")

# Chemin vers le dossier où les clips seront sauvegardés
clips_dir = "E:/clips"

# Vérifier si le dossier 'clips' existe, sinon le créer
if not os.path.exists(clips_dir):
    os.makedirs(clips_dir)

# Charger les données du fichier JSON
try:
    with open('TopLaughingClips_Month.json', 'r') as f:
        clips = json.load(f)
except Exception as e:
    print(f"Erreur lors de la lecture du fichier JSON : {e}")
    exit()

# Options de youtube_dl
ydl_opts = {
    'format': 'best',
    # Ajouter des métadonnées si nécessaire
    # 'postprocessors': [{
    #    'key': 'FFmpegMetadata',
    #    'add_metadata': True
    # }],
}

# Télécharger chaque clip
for clip in clips:
    download_clip(clip, ydl_opts)
