# Project Context: YouTube Automated Summarizer (Agent-Assisted)

## Project Goal
To allow a Korean data analyst to quickly digest English data analysis YouTube videos without watching them.
The system automatically detects new videos, fetches transcripts, and prepares a **Prompt File** that the user can feed into a superior LLM (like ChatGPT o1/4o) to get a high-quality Korean summary.

## Core Workflow
1.  **Monitor**: `src/monitor.py` checks the YouTube RSS feed periodically.
2.  **Fetch**: `src/transcript.py` downloads the English transcript of new videos.
3.  **Generate**: `src/generator.py` combines the **System Prompt** (`prompts/SYSTEM_PROMPT.md`) and the **Transcript** into a single `.txt` file in `output/`.
4.  **User Action**: The user copies the content of the `.txt` file and pastes it into ChatGPT.

## Key Files
-   `main.py`: Entry point, orchestrates the loop.
-   `config/config.yaml`: Settings (Channel ID, Interval).
-   `prompts/SYSTEM_PROMPT.md`: The expert persona and instructions for the LLM.
-   `output/`: Where the `prompt_[video_id].txt` files are saved.

## Design Philosophy
-   **No API Costs**: Uses the user's existing generic LLM access (ChatGPT Web) via copy-paste.
-   **High Quality**: Uses a carefully crafted System Prompt to ensure "Principal Data Analyst" level insights.
-   **Automated Detection**: Runs in the background so the user doesn't miss updates.
