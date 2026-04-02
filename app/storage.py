import os
from google import genai
from openai import AsyncOpenAI
from googleapiclient.discovery import build
from dotenv import load_dotenv
from supabase import create_client, Client 

load_dotenv()

# SiliconFlow & Groq Setup (OpenAI SDK used!!)
sf_client = AsyncOpenAI(
    api_key=os.getenv("SILICONFLOW_API_KEY"), 
    base_url="https://api.siliconflow.com/v1"
)
groq1_client = AsyncOpenAI(
    api_key=os.getenv("GROQ1_API_KEY"), 
    base_url="https://api.groq.com/openai/v1"
)
groq2_client = AsyncOpenAI(
    api_key=os.getenv("GROQ2_API_KEY"), 
    base_url="https://api.groq.com/openai/v1"
)

# YouTube API Setup
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube_service = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def get_youtube_videos(query: str):

    # YouTube library က sync ဖြစ်လို့ သူ့ကို function သီးသန့်ထုတ်

    try:

        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        request = youtube.search().list(
            q=query, part='snippet', 
            type='video', maxResults=3
        )
        response = request.execute()

        return [{"title": v['snippet']['title'], "link": f"https://youtu.be/{v['id']['videoId']}"} for v in response['items']]

    except:

        return []
    
# --- Database Setup (Supabase) ---
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def save_chat_to_db(user_id: str, role: str, message: str, agent_type: str):
    try:
        supabase.table("chat_history").insert({
            "user_id": user_id,
            "role": role,
            "message": message,
            "agent_type": agent_type
        }).execute()
    except Exception as e:
        print(f"Error saving to DB: {e}")