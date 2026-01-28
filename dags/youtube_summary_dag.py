from airflow import DAG
from airflow.operators.python import PythonOperator
from textwrap import dedent
import pendulum
import sys
import os

# Project Path Configuration
# This assumes the project is checked out at this location.
# Please update this path if your project is located elsewhere.
PROJECT_PATH = r'c:\vscode\eng_youtube_transfer\eng_youtube_transfer'

if PROJECT_PATH not in sys.path:
    sys.path.append(os.path.join(PROJECT_PATH, 'src'))

# Import your project modules
# Note: You need to make sure 'src' is importable. 
# We append PROJECT_PATH/src to sys.path inside the task or globally.

def check_and_generate_task():
    # Dynamic import to avoid top-level failures if path issues exist
    sys.path.append(os.path.join(PROJECT_PATH, 'src'))
    sys.path.append(PROJECT_PATH) # for config load which might be relative
    
    # We also need to change cwd so config loading works relative to root
    os.chdir(PROJECT_PATH)
    
    from src.monitor import check_for_new_video
    from src.transcript import get_transcript
    from src.generator import generate_prompt_file
    import yaml
    
    # Load Config
    config_path = os.path.join(PROJECT_PATH, 'config', 'config.yaml')
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
        
    last_video_file = os.path.join(PROJECT_PATH, 'last_video_id.txt')
    
    # helper to get/save last video
    def get_last_id():
        if os.path.exists(last_video_file):
            with open(last_video_file, 'r') as f:
                return f.read().strip()
        return None
        
    def save_last_id(vid):
        with open(last_video_file, 'w') as f:
            f.write(vid)

    channel_id = config['youtube']['channel_id']
    last_id = get_last_id()
    
    print(f"Checking for new videos on channel: {channel_id}...")
    video_info = check_for_new_video(channel_id, last_id)
    
    if video_info:
        print(f"New video found: {video_info['title']}")
        transcript = get_transcript(video_info['id'])
        
        if transcript:
            output_dir = os.path.join(PROJECT_PATH, 'output')
            result_path = generate_prompt_file(
                video_info['id'], 
                video_info['title'], 
                transcript, 
                output_dir=output_dir
            )
            print(f"Generated prompt file: {result_path}")
            save_last_id(video_info['id'])
            
            # Git Push Automation
            try:
                import subprocess
                print("Pushing to GitHub...")
                # Add the new file
                subprocess.run(['git', 'add', result_path], check=True, cwd=PROJECT_PATH)
                # Commit
                commit_msg = f"Add prompt for video: {video_info['id']}"
                subprocess.run(['git', 'commit', '-m', commit_msg], check=True, cwd=PROJECT_PATH)
                # Push
                subprocess.run(['git', 'push'], check=True, cwd=PROJECT_PATH)
                print("Successfully pushed to GitHub!")
            except Exception as e:
                print(f"Git Push failed: {e}")
        else:
            print("No transcript found.")
    else:
        print("No new videos found.")

with DAG(
    'youtube_summary_agent',
    default_args={
        'retries': 1,
    },
    description='Checks YouTube for new videos and generates summary prompts',
    schedule_interval='@daily',
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=['youtube', 'agent'],
) as dag:

    run_check = PythonOperator(
        task_id='check_youtube_and_generate',
        python_callable=check_and_generate_task,
    )
    
    run_check
