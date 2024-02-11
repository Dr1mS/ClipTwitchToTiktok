import re
import json
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import StaleElementReferenceException
import time
from tqdm import tqdm


#ce script sert à compter le nombre de rires dans les clips et à les sauvegarder dans un fichier 
# json si le nombre de rires est supérieur à 5 pour chaque clip 
# (on peut changer le nombre de rires dans la variable nombreDeRires)
# le script utilise le fichier BestClipsOfMonth.json qui contient les clips des meilleurs streamers du mois
# (on peut changer le fichier dans la ligne 40)
# le script utilise le fichier laugh_patterns.json qui contient les modèles de rire
# (on peut changer le fichier dans la ligne 44)
# le script utilise le fichier TopLaughingClips_Month.json qui contient les clips avec plus de 5 laugh_count
# (on peut changer le fichier dans la ligne 78)





nombreDinstances = 10
nombreDeRires = 5

def process_clip(clip):
    laugh_count = 0
    url = clip['url']
    duration = clip['duration']

    driver = webdriver.Firefox(service=Service(geckodriver_path), options=firefox_options)
    driver.get(url)
    time.sleep(2)
    
    start_time = time.time()

    while time.time() - start_time < duration:
        try:
            chat_elements = driver.find_elements(By.CSS_SELECTOR, 'span.text-fragment[data-a-target="chat-message-text"]:not([data-counted])')

            for elem in chat_elements:
                message = elem.text
                if laugh_re.search(message):
                    laugh_count += 1
                    driver.execute_script("arguments[0].setAttribute('data-counted', 'true')", elem)

            if laugh_count >= nombreDeRires:
                break

            time.sleep(1)
        except StaleElementReferenceException:
            print("StaleElementReferenceException attrapée, en passant à l'itération suivante.")

    driver.quit()

    if laugh_count >= nombreDeRires:
        return {
            'url': url,
            'streamer': clip['streamer'],
            'game': clip['game'],
            'title': clip['title'],
            'duration': clip['duration'],
        }
    else:
        return None


# Lire les modèles de rire depuis le fichier JSON
with open('laugh_patterns.json', 'r') as f:
    data = json.load(f)

# Créer une expression régulière à partir des modèles de rire
laugh_patterns = '|'.join(data['laugh_patterns'])
laugh_re = re.compile(rf'\b({laugh_patterns})\b', re.IGNORECASE)

# Lire les clips depuis le fichier JSON
with open('BestClipsOfMonth.json', 'r') as f:
    clips = json.load(f)

# Configuration initiale du WebDriver
geckodriver_path = './geckodriver.exe'
firefox_options = Options()
firefox_options.add_argument("--headless")

# Liste pour stocker les clips qui ont plus de 5 laugh_count
top_clips = []

# Exécutez le code en parallèle sur plusieurs clips
with concurrent.futures.ThreadPoolExecutor(max_workers=nombreDinstances) as executor:
    future_to_clip = {executor.submit(process_clip, clip): clip for clip in clips}
    for future in tqdm(concurrent.futures.as_completed(future_to_clip), total=len(future_to_clip), desc="Processing clips"):
        clip = future_to_clip[future]
        try:
            result = future.result()
            if result is not None:
                top_clips.append(result)
                print(f"\nClip ajouté de {result['streamer']} \nnom du clip: {result['title']} \nurl: {result['url']} \ndurée: {result['duration']} \n")
        except Exception as e:
            print(f"Une exception {e} a été générée lors du traitement du clip {clip['url']}")

# Sauvegarder les top_clips dans un nouveau fichier JSON
with open('TopLaughingClips_Month.json', 'w') as f:
    json.dump(top_clips, f)

print(f"Les clips avec plus de {nombreDeRires} laugh_count ont été sauvegardés dans TopLaughingClips.json.")

