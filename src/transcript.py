from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def get_transcript(video_id):
    """
    Fetches the transcript for a given YouTube video ID.
    Tries to get English transcript (manual or auto-generated).
    Returns the combined text of the transcript.
    """
    try:
        # List available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Try to find English transcript
        # logic: prefer manually created, then generated
        transcript = None
        
        try:
           transcript = transcript_list.find_manually_created_transcript(['en', 'en-US', 'en-GB'])
        except:
           try:
               transcript = transcript_list.find_generated_transcript(['en', 'en-US', 'en-GB'])
           except:
               # If no English, try to translate or just take first available
               print("No direct English transcript found. Attempting fallback...")
               pass

        if not transcript:
             # Fallback: just take the first one found
             transcript = transcript_list.find_transcript(['en']) # specific fallback

        if transcript:
            fetched_transcript = transcript.fetch()
            formatter = TextFormatter()
            text = formatter.format_transcript(fetched_transcript)
            return text
            
    except Exception as e:
        print(f"Error fetching transcript for {video_id}: {e}")
        return None
