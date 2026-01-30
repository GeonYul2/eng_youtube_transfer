"""
Generated DAG: pipeline__eng_youtube_process

================================================================================
👶 어린이를 위한 100% 이해 가능 설명서 (Kindergarten Guide) 👶
================================================================================

안녕! 이 파일은 "대본 추출 로봇 (Consumer)"이에요.
이 로봇은 **"영상 준비 끝! (dataset://eng_youtube/videos)"** 푯말이 보여야만 일을 시작해요.

우리가 하려는 일:
1. 📜 **대본 추출 (process_latest_video)**: 준비된 영상에서 전체 대본(Full Script)을 쏙 뽑아내요.

**왜 이렇게 나누었냐고요?**
영상 찾는 로봇(Producer)이랑 대본 뽑는 로봇(Consumer)이 따로 있으면, 
하나가 말썽을 피워도 다른 친구는 안전하거든요!

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
    process_video_pipeline,
)


# Default arguments
default_args = {
    "owner": "geon_yul",
    "retries": 2,
    "retry_delay": timedelta(seconds=300),
}

# Pipeline Definition
with DAG(
    dag_id="pipeline__eng_youtube_process",
    default_args=default_args,
    # 시간이 아니라 '영상 데이터 준비 완료' 신호를 기다려요!
    schedule=[
        Dataset("dataset://eng_youtube/videos"),
    ],
    catchup=False,
    tags=[],
) as dag:

    # Task Definitions

    # 1. Root Tasks (No Group)
    process_latest_video = PythonOperator(
        task_id="process_latest_video",
        python_callable=process_video_pipeline,
        op_kwargs={"video_id": "video_12345"},
        doc_md="""
        ### 📜 대본 추출
        준비된 영상의 전체 대본(Full Script)을 다운로드 및 저장합니다.
        """,
    )

    
