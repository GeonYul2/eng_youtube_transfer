from airflow import DAG
from airflow.operators.python import PythonOperator
import pendulum
import sys
import os

PROJECT_PATH = r'c:\vscode\eng_youtube_transfer\eng_youtube_transfer'

def youtube_test_task():
    sys.path.append(os.path.join(PROJECT_PATH, 'src'))
    os.chdir(PROJECT_PATH)
    
    from src.monitor import get_latest_videos
    from src.transcript import get_transcript
    from src.generator import generate_prompt_file
    import yaml
    
    # Load Config
    config_path = os.path.join(PROJECT_PATH, 'config', 'config.yaml')
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    channel_id = config['youtube']['channel_id']
    
    print(f"TEST: Fetching 2 latest videos from channel: {channel_id}...")
    videos = get_latest_videos(channel_id, count=2)
    
    if not videos:
        print("No videos found.")
        return

    for video_info in videos:
        print(f"Processing Test Video: {video_info['title']} ({video_info['id']})")
        transcript = get_transcript(video_info['id'])
        
        if transcript:
            output_dir = os.path.join(PROJECT_PATH, 'output')
            result_path = generate_prompt_file(
                video_info['id'], 
                video_info['title'], 
                transcript, 
                output_dir=output_dir
            )
            print(f"SUCCESS: Generated test prompt file: {result_path}")
        else:
            print(f"FAILED: No transcript for {video_info['id']}")

with DAG(
    'youtube_summary_TEST_DAG',
    default_args={'retries': 0},
    description='TEST DAG: Fetches 2 latest videos regardless of history',
    schedule_interval=None, # 수동 실행 전용
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=['test', 'youtube'],
) as dag:

    test_run = PythonOperator(
        task_id='fetch_2_latest_videos_test',
        python_callable=youtube_test_task,
    )
    
    test_run
