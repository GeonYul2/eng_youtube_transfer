import os

def generate_prompt_file(video_id, video_title, transcript_text, output_dir='output'):
    """
    Reads the SYSTEM_PROMPT.md and the transcript, then generates a complete prompt file
    that the user can copy-paste into ChatGPT.
    """
    
    # Path to the System Prompt
    # Assuming code is running from root, prompts are in prompts/
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Go up one level from src
    # If run from main.py, os.getcwd() might be root. But __file__ is safer relative path.
    # main.py is in root. src/generator.py is in src.
    # So if main.py calls this, we need to find prompts/SYSTEM_PROMPT.md relative to root?
    # Let's rely on relative paths from the execution root (which is usually where main.py is).
    
    prompt_path = os.path.join('prompts', 'SYSTEM_PROMPT.md')
    
    if not os.path.exists(prompt_path):
        return f"Error: System prompt file not found at {prompt_path}"
        
    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            system_prompt = f.read()
    except Exception as e:
        return f"Error reading system prompt: {e}"
        
    # Construct the final content
    # We want to guide the user to paste this entire block.
    
    final_content = f"""
{system_prompt}

---

## 6) 입력 데이터 (Transcript)
**영상 제목**: {video_title}
**영상 ID**: {video_id}

**[Transcript Start]**
{transcript_text}
**[Transcript End]**
    """
    
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Save to file
    filename = f"prompt_{video_id}.txt"
    filepath = os.path.join(output_dir, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(final_content)
        return filepath
    except Exception as e:
        return f"Error saving prompt file: {e}"
