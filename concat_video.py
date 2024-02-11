from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

# Ce script permet d'assembler les clips en une seule vidéo


# Créez le dossier de sortie s'il n'existe pas
output_folder = "E:/finito"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Transition à utiliser entre les clips
transition = VideoFileClip("E:/transition/TVTransition.mp4")

# Parcourir le dossier des clips et les classer
clips_40 = []
clips_120 = []
for filename in os.listdir("E:/clips_named"):
    if filename.endswith('.mp4'):
        clip_path = f"E:/clips_named/{filename}"
        clip = VideoFileClip(clip_path)
        if clip.duration < 40:
            clips_40.append(clip)
        else:
            clips_120.append(clip)

# Fonction pour assembler et sauvegarder les vidéos
def assemble_and_save(clips, max_duration, folder, transition):
    while len(clips) > 0:
        total_duration = 0
        video_list = []
        streamers = set()
        clips_to_remove = []

        for clip in clips:
            total_duration += clip.duration + 0.15  # +0.15 pour la transition

            if total_duration > max_duration:
                break

            # Réinitialiser la position du clip à son emplacement d'origine
            new_clip = clip.set_position(('center', 'center'))

            video_list.append(new_clip)
            video_list.append(transition)
            streamer_name = os.path.basename(clip.filename).split('-')[0]
            streamers.add(streamer_name)
            clips_to_remove.append(clip)

        if not video_list:  # Si la liste est vide, sortir de la fonction
            return

        final_video = concatenate_videoclips(video_list[:-1])  # Retirer la dernière transition

        streamer_names = " - ".join(streamers)
        final_name = f"{streamer_names} - {int(final_video.duration)}s.mp4"
        final_path = os.path.join(folder, final_name)

        try:
            final_video.write_videofile(final_path, codec="libx264")
        except Exception as e:
            print(f"Une erreur est survenue lors de l'écriture de la vidéo : {e}")

        # Retirer les clips qui ont déjà été traités
        for clip in clips_to_remove:
            clips.remove(clip)

# Assembler et sauvegarder les vidéos de moins de 40 secondes
assemble_and_save(clips_40, 80, output_folder, transition)

# Assembler et sauvegarder les vidéos de plus de 40 secondes
assemble_and_save(clips_120, 130, output_folder, transition)
