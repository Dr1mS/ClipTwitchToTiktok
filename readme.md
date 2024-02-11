# TikTok Video Uploader

This project automates the process of uploading videos to TikTok.

## Features

- Reads hashtags from a file and returns them as a list of strings.
- Uploads a random video from a source folder to TikTok with a description containing the video's name and hashtags.

## Getting Started

### Prerequisites

- Python 3
- Selenium WebDriver
- Firefox browser

### Project Guide

This project aims to automate the process of retrieving, processing, and publishing video clips from TikTok. Follow these steps to set up and run the project:

1. Configure TikTok Credentials
In the .env file, configure your TikTok CLIENT_ID and CLIENT_SECRET.
2. Obtain Credentials
Run get_credential.py. This will automatically create an access token for the TikTok API.
3. Configure Cookies
In the cookies.tkt file, add your TikTok cookies. You can obtain these cookies using a Chrome extension or another tool capable of exporting cookies in the "get cookies.txt" format.
4. Select Streamers
In the STREAMER.txt file, add the names of all the streamers from whom you want to retrieve clips.
5. Get Streamer IDs
Run get_streamer_id.py to automatically get the IDs of the streamers.
6. Retrieve Best Clips
Run get_clips_from_streamer_month.py to retrieve the best clips from the streamers.
7. Sort Clips
Use laught_count_multistrading.py to sort the clips based on laugh_pattern.json.
8. Download Clips
Run download_clips.py to download all the clips according to TopLaughingClips_Month.json.
9. Add Names to Downloaded Clips
Use put_name_on_downloaded_clips.py to edit the videos to the TikTok format.
10. Publish on TikTok
Run upload_on_TiktTok.py to publish a random video from the SOURCE_FOLDER to TikTok. The uploaded videos will be in the DESTINATION_FOLDER.
Enjoy automating your TikTok workflow with this project!
