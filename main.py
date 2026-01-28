import yaml
import time
import schedule
import os
import sys

# Add src to python path so we can import modules from it
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from monitor import check_for_new_video
from transcript import get_transcript
from generator import generate_prompt_file

CONFIG_PATH = os.path.join('config', 'config.yaml')
LAST_VIDEO_FILE = 'last_video_id.txt'

def load_config():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def get_last_video_id():
    if os.path.exists(LAST_VIDEO_FILE):
        with open(LAST_VIDEO_FILE, 'r') as f:
            return f.read().strip()
    return None

def save_last_video_id(video_id):
    with open(LAST_VIDEO_FILE, 'w') as f:
        f.write(video_id)

def job():
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Checking for new videos...")
    try:
        config = load_config()
    except Exception as e:
        print(f"Error loading config: {e}")
        return

    channel_id = config['youtube']['channel_id']
    
    if channel_id == "CHANNEL_ID_HERE":
        print("Please set the Channel ID in config/config.yaml")
        return

    last_video_id = get_last_video_id()
    
    video_info = check_for_new_video(channel_id, last_video_id)
    
    if video_info:
        print(f"New video found: {video_info['title']}")
        
        # Fetch transcript
        print("Fetching transcript...")
        transcript = get_transcript(video_info['id'])
        
        if transcript:
            print("Transcript fetched. Generating prompt file...")
            
            # Generate Prompt File
            result_path = generate_prompt_file(
                video_id=video_info['id'], 
                video_title=video_info['title'], 
                transcript_text=transcript
            )
            
            if "Error" not in result_path:
                print(f"SUCCESS! Prompt file created at: {result_path}")
                print("Copy the content of this file and paste it into ChatGPT.")
                
                # Update last video ID only on success
                save_last_video_id(video_info['id'])
            else:
                print(result_path) # Print error message
                
        else:
            print("Could not fetch transcript.")
    else:
        print("No new videos found.")

def main():
    print("Starting YouTube Summarizer (Agent Mode)...")
    print("Monitor -> Fetch -> Generate Prompt File")
    
    # Run once immediately
    job()
    
    # Schedule
    try:
        config = load_config()
        interval = config['youtube'].get('check_interval_seconds', 3600)
    except:
        interval = 3600

    schedule.every(interval).seconds.do(job)
    
    print(f"Scheduled to check every {interval} seconds.")
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
