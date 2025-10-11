from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for incoming messages
class Message(BaseModel):
    message: str

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize OpenAI (optional)
if OPENAI_API_KEY:
    from openai import OpenAI
    openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize Supabase client (optional)
supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# System prompt for AgriMind
SYSTEM_PROMPT = """
You are AgriMind, an AI agricultural mentor. Your goal is to educate, advise, and guide users about soil health, sustainable farming, vegetation management, and climate-resilient agriculture. Use clear and actionable language. When possible, recommend specific sustainable practices (e.g., crop rotation, composting, organic fertilizers, or erosion control). Keep answers simple, practical, and regionally adaptable.
"""

@app.get("/")
async def root():
    return {"message": "Welcome to AgriMind AI Agent API", "docs": "/docs", "chat": "/chat"}

@app.post("/chat")
async def chat(message: Message):
    try:
        if OPENAI_API_KEY:
            try:
                # Call OpenAI API
                response = openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": message.message}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
                bot_response = response.choices[0].message.content.strip()
            except Exception as e:
                # Handle API errors (quota, etc.)
                bot_response = f"OpenAI API error: {str(e)}. Please check your OpenAI account billing. For now, here's some general farming advice: Consider sustainable practices like crop rotation, composting, and organic fertilizers for better soil health."
        else:
            # Mock response for demo
            bot_response = "This is a demo response. To get real AI answers, please set up your OpenAI API key in the .env file. For your question about farming, consider sustainable practices like crop rotation and organic fertilizers."

        # Store chat in Supabase (optional, for learning content)
        if supabase:
            # Assuming a table 'chats' with columns: user_message, bot_response
            supabase.table("chats").insert({
                "user_message": message.message,
                "bot_response": bot_response
            }).execute()

        return {"response": bot_response}
    except Exception as e:
        return {"error": str(e)}

# Placeholder for future GIS integration
# TODO: Add route to fetch GIS/remote sensing data for soil and vegetation insights
# Example: @app.get("/gis/{location}")
# def get_gis_data(location: str):
#     # Integrate with GIS API (e.g., Google Earth Engine, Sentinel Hub)
#     # Fetch soil health, vegetation index, etc.
#     # Return data to enhance AI responses with real-time insights
#     pass

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)