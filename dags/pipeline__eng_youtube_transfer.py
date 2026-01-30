"""
Generated DAG: pipeline__eng_youtube_transfer
"""
from airflow import DAG
import pendulum
from datetime import datetime, timedelta

# Operator Imports

from airflow.providers.standard.operators.python import PythonOperator


# Default arguments
default_args = {
    "owner": "geon_yul",
    "retries": 2,
    "retry_delay": timedelta(seconds=300),
}

# Pipeline Definition
with DAG(
    dag_id="pipeline__eng_youtube_transfer",
    default_args=default_args,
    schedule="@hourly",
    catchup=False,
    tags=[],
) as dag:

    # Task Definitions

    # 1. Root Tasks (No Group)

    fetch_videos = PythonOperator(
        task_id="fetch_videos",
        python_callable=lambda: print(
            "Executing eng_youtube.video_ops.fetch_latest_videos"
        ),
        op_kwargs={"channel_id": "UCtoNXlIegvxkvf5Ji8S57Ag", "limit": 3},
    )

    process_latest_video = PythonOperator(
        task_id="process_latest_video",
        python_callable=lambda: print(
            "Executing eng_youtube.video_ops.process_video_pipeline"
        ),
        op_kwargs={"video_id": "video_12345"},
    )

    # 2. Task Groups

    # Dependencies

    fetch_videos >> process_latest_video
