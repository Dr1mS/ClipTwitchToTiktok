import re
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import StaleElementReferenceException

import time

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
geckodriver_path = './geckodriver'
firefox_options = Options()
firefox_options.add_argument("--headless")
driver = webdriver.Firefox(service=Service(geckodriver_path), options=firefox_options)

# Liste pour stocker les clips qui ont plus de 5 laugh_count
top_clips = []

# Parcourir chaque clip
for clip in clips:
    url = clip['url']
    duration = clip['duration']
    
    # Ouvrir la page web
    driver.get(url)
    
    # Pause pour permettre le chargement initial de la page
    time.sleep(2)
    
    # Initialiser le compteur
    laugh_count = 0
    
    # Temps de début
    start_time = time.time()
    
   # Boucle pour compter les occurrences pendant la durée du clip
    while time.time() - start_time < duration:
        try:
            chat_elements = driver.find_elements(By.CSS_SELECTOR, 'span.text-fragment[data-a-target="chat-message-text"]:not([data-counted])')
            
            for elem in chat_elements:
                message = elem.text  # Cette ligne peut lever une StaleElementReferenceException
                if laugh_re.search(message):
                    laugh_count += 1
                    driver.execute_script("arguments[0].setAttribute('data-counted', 'true')", elem)

            # Attendre avant la prochaine itération
            time.sleep(1)
            #print(f"Laugh count: {laugh_count}")

            if laugh_count >= 5:
                break
        except StaleElementReferenceException:
            print("StaleElementReferenceException attrapée, en passant à l'itération suivante.")

    # Vérifier si le clip a plus de 5 laugh_count
    if laugh_count >= 5:
        top_clips.append({'url': url,  
                          'streamer': clip['streamer'],
                          'game': clip['game'],
                          'title': clip['title'],
                          'duration': clip['duration'],
                          })
        print(f"Clip ajouté de {clip['streamer']} \nnom du clip: {clip['title']} \nurl: {url} \ndurée: {clip['duration']} \n  ")
    else:
        print(f"Clip non ajouté")

        

# Fermer le navigateur
driver.quit()

# Sauvegarder les top_clips dans un nouveau fichier JSON
with open('TopLaughingClips_Month.json', 'w') as f:
    json.dump(top_clips, f)

print('Les clips avec plus de 5 laugh_count ont été sauvegardés dans TopLaughingClips.json.')
