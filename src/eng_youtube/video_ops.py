"""
Core business logic for YouTube Automation.
Separated from Airflow dependencies to be pure Python.
"""

import logging
import json
import os
import time
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# Default Configuration
DEFAULT_CHANNEL_ID = "UCtoNXlIegvxkvf5Ji8S57Ag"  # @loresowhat
MOCK_VIDEO_ID = "video_12345"

def fetch_latest_videos(channel_id: str = DEFAULT_CHANNEL_ID, limit: int = 5) -> List[str]:
    """
    Simulates fetching the latest videos from a YouTube channel.
    In a real implementation, this would use google-api-python-client.
    """
    logger.info(f"Fetching latest videos for channel: {channel_id}")
    
    # Simulation: specific channel gets specific mock result
    if channel_id == DEFAULT_CHANNEL_ID:
        logger.info("Target channel detected. Returning mock video list.")
        return [MOCK_VIDEO_ID, "video_67890", "video_54321"][:limit]
    
    return [f"mock_video_{i}" for i in range(limit)]

def download_transcript(video_id: str) -> str:
    """
    Simulates downloading a transcript using youtube_transcript_api.
    """
    logger.info(f"Downloading transcript for video: {video_id}")
    
    # Simulation
    time.sleep(1) # Simulate network delay
    if video_id == MOCK_VIDEO_ID:
        return "Hello world. This is a transcript of an interesting engineering video. Today we discuss Airflow."
    
    return f"Simulated transcript content for video {video_id}."

def generate_prompt(video_id: str, transcript: str) -> str:
    """
    Combines the transcript with a system prompt to create the final output.
    """
    system_prompt = """
    You are an expert content summarizer. 
    Please summarize the following YouTube transcript into key takeout points.
    """
    
    final_prompt = f"{system_prompt}\n\nTranscript for {video_id}:\n{transcript}"
    logger.info(f"Generated prompt for video: {video_id} (Length: {len(final_prompt)})")
    return final_prompt

def save_result(video_id: str, content: str, output_dir: str = "output") -> str:
    """
    Saves the generated prompt to a text file.
    """
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"prompt_{video_id}.txt")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
        
    logger.info(f"Saved result to: {filename}")
    return filename

def process_video_pipeline(video_id: str) -> str:
    """
    Orchestration function to run the full flow for a single video.
    Can be called directly by Airflow PythonOperator.
    """
    logger.info(f"Starting pipeline for video: {video_id}")
    
    transcript = download_transcript(video_id)
    prompt_content = generate_prompt(video_id, transcript)
    saved_path = save_result(video_id, prompt_content)
    
    return saved_path
