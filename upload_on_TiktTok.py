# Importing necessary modules
from selenium.webdriver.firefox.options import Options
from tiktok_uploader.upload import upload_video
from tiktok_uploader.auth import AuthBackend
import random
import os
import tiktok_uploader
import time
from dotenv import load_dotenv

def read_hashtags(file_path):
    """
    Reads hashtags from a file and returns them as a list of strings.

    Args:
        file_path (str): The path to the file containing hashtags.

    Returns:
        list: A list of hashtags as strings.
    """
    with open(file_path, 'r') as f:
        hashtags = f.readlines()
    return [tag.strip() for tag in hashtags]

def upload_random_video():
    """
    Uploads a random video from a source folder to TikTok.

    The function chooses a random video from a source folder, moves it to a destination folder,
    and uploads it to TikTok with a description containing the video's name and hashtags.
    """
    # Get the source and destination folders from environment variables
    source_folder = os.getenv("SOURCE_FOLDER")
    destination_folder = os.getenv("DESTINATION_FOLDER")

    # Read hashtags from file
    hashtags = read_hashtags("hashtag.txt")
    hashtags_str = " ".join(hashtags)

    # Get all video files in source folder
    all_files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
    video_files = [f for f in all_files if f.endswith(".mp4")]

    # If there are no video files, print a message and return
    if not video_files:
        print("Le stock de vidéos est épuisé, veuillez en ajouter.")
        #wait for input to close
        input()
        return

    # Choose a random video file
    chosen_video = random.choice(video_files)

    # Get the path to the chosen video
    chosen_video_path = os.path.join(destination_folder, chosen_video) 
    chosen_video_pathbis = os.path.join(source_folder, chosen_video) 

    # Get the video's name without the extension
    video_name_without_extension = os.path.splitext(chosen_video)[0]

    # Create the description
    description = f"{video_name_without_extension} {hashtags_str}"

    # Move the video to the destination folder
    os.rename(chosen_video_pathbis, os.path.join(destination_folder, chosen_video)) 

    # Configure the WebDriver
    firefox_options = Options() 

    # Uncomment the following line to run Firefox in headless mode
    #firefox_options.add_argument("--headless")

    # Upload the video
    upload_video(
        chosen_video_path, # The path to the video file
        description=description, # The video's description
        #cookies_list=[], # Uncomment this line to use cookies list instead of cookies file
        cookies='cookies.txt', # The path to the cookies file Commented this line to use cookies list instead of cookies file
        browser='firefox', # The browser to use
        options=firefox_options # The browser options
    )




if __name__ == "__main__":

    # Load environment variables
    load_dotenv()

    # Upload a random video
    upload_random_video()
    

