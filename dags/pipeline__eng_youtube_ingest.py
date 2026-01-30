"""
Generated DAG: pipeline__eng_youtube_ingest

================================================================================
👶 어린이를 위한 100% 이해 가능 설명서 (Kindergarten Guide) 👶
================================================================================

안녕! 이 파일은 "영상 수집 로봇 (Producer)"이에요.
이 로봇은 유튜브를 감시하다가 새로운 영상이 보이면 냉큼 주워와요.

우리가 하려는 일:
1. 🕵️ **영상 수집 (fetch_videos)**: "새 영상 올라왔나?" 하고 유튜브 채널을 감시해요.

**특별한 비밀**: 
영상을 다 찾으면 **"자, 영상 준비 끝! (dataset://eng_youtube/videos)"** 하고 푯말을 세워요.
그러면 저쪽에서 "대본 뽑는 로봇(Consumer)"이 이 푯말을 보고 달려올 거예요!

"""
from airflow import DAG
import pendulum
from datetime import datetime, timedelta
from airflow.providers.standard.operators.python import PythonOperator
from airflow.datasets import Dataset
import sys
import os

# Import Operator Logic
from eng_youtube.video_ops import (
    fetch_latest_videos,
)


# Default arguments
default_args = {
    "owner": "geon_yul",
    "retries": 2,
    "retry_delay": timedelta(seconds=300),
}

# Pipeline Definition
with DAG(
    dag_id="pipeline__eng_youtube_ingest",
    default_args=default_args,
    schedule="@hourly",
    catchup=False,
    tags=[],
) as dag:

    # Task Definitions

    # 1. Root Tasks (No Group)
    fetch_videos = PythonOperator(
        task_id="fetch_videos",
        python_callable=fetch_latest_videos,
        # 이 작업이 성공하면 'eng_youtube/videos' 데이터셋이 업데이트되었다고 알려줍니다.
        outlets=[
            Dataset("dataset://eng_youtube/videos"),
        ],
        op_kwargs={"channel_id": "UCtoNXlIegvxkvf5Ji8S57Ag", "limit": 3},
        doc_md="""
        ### 🕵️ 영상 수집
        지정된 유튜브 채널에서 최신 영상을 가져와서 DB(혹은 파일)에 저장합니다.
        """,
    )

    
