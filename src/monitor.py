import feedparser

def check_for_new_video(channel_id, last_video_id=None):
    """
    Checks the YouTube RSS feed for the latest video.
    Returns a dictionary with video details if a new video is found, else None.
    """
    rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    print(f"Checking RSS feed: {rss_url}")
    feed = feedparser.parse(rss_url)
    
    if not feed.entries:
        print("No entries found in RSS feed.")
        return None
        
    latest_entry = feed.entries[0]
    video_id = latest_entry.yt_videoid
    
    print(f"Latest video ID: {video_id}")

    if video_id != last_video_id:
        return {
            'id': video_id,
            'title': latest_entry.title,
            'link': latest_entry.link,
            'published': latest_entry.published
        }
    
    return None

def get_latest_videos(channel_id, count=2):
    """
    Fetches the last N videos from the YouTube RSS feed.
    """
    rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    print(f"Fetching latest {count} videos from: {rss_url}")
    feed = feedparser.parse(rss_url)
    
    if not feed.entries:
        return []
        
    videos = []
    for entry in feed.entries[:count]:
        videos.append({
            'id': entry.yt_videoid,
            'title': entry.title,
            'link': entry.link,
            'published': entry.published
        })
    return videos
