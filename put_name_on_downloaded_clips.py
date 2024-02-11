# Import necessary libraries
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ColorClip
from moviepy.config import change_settings
import os

# Set the path to the ImageMagick binary
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})

# Set the directory where the named clips will be saved
clips_named_dir = "E:/clips_named"

# Create a list to keep track of resources that need to be closed
resources_to_close = []

# Create the 'clips_named' directory if it doesn't exist
if not os.path.exists(clips_named_dir):
    os.makedirs(clips_named_dir)

# Iterate through all the files in the 'clips' directory
for filename in os.listdir('E:/clips'):
    try:
        # Skip files that are not mp4 videos
        if not filename.endswith('.mp4'):
            continue

        # Extract the streamer's name, game, title and duration from the filename
        parts = filename[:-4].split('-')

        # If the filename is not in the correct format, skip it
        if len(parts) < 4:
            print(f"Incorrect filename format: {filename}")
            continue

        # Assign the extracted values to variables
        streamer, game, title, duration = [part.strip() for part in parts[:4]]

        # Open the video file
        video_path = f"E:/clips/{filename}"
        video = VideoFileClip(video_path)
        resources_to_close.append(video)

        # Resize the video to fit the TikTok dimensions (1080x1920)
        tiktok_width, tiktok_height = 1080, 1920
        new_width = tiktok_width
        new_height = int(video.h * (new_width / video.w))
        
        resized_video = video.resize(height=new_height, width=new_width)
        y_centered = (tiktok_height - new_height) // 2
        
        # Set the position of the text clips
        y_title = y_centered // 2
        y_streamer = y_centered + new_height + (y_centered // 2)
        
        # Create the text clips
        txt_title = TextClip(title, fontsize=18, color="white").set_position(('center', y_title + 65)).set_duration(video.duration)
        txt_streamer = TextClip(streamer, fontsize=32, color="black", bg_color="white").set_position(('center', y_streamer)).set_duration(video.duration)
        txt_game = TextClip(game, fontsize=32, color="white").set_position(('center', y_title)).set_duration(video.duration)
        
        # Create a black clip to use as a background
        black_clip = ColorClip(size=(tiktok_width, tiktok_height), color=(0,0,0)).set_duration(video.duration)

        # Combine the video and text clips
        final_video = CompositeVideoClip([black_clip, resized_video.set_position(('center', y_centered)), txt_title, txt_streamer, txt_game])
        resources_to_close.append(final_video)

        # Set the filename for the named clip
        named_filename = f"{streamer}-{title}-{game}-{duration}.mp4"
        final_video_path = f"{clips_named_dir}/{named_filename}"

        # Save the final clip
        final_video.write_videofile(final_video_path, codec="libx264")

    except Exception as e:
        # If an error occurs, print an error message and continue with the next file
        print(f"An error occurred for file {filename}: {e}")

    finally:
        # Close all resources that were opened during the iteration
        for resource in resources_to_close:
            try:
                resource.close()
            except Exception as e:
                print(f"An error occurred while releasing resources: {e}")
