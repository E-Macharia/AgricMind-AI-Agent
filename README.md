# AgriMind - AI Chatbot for Sustainable Farming

AgriMind is an AI-powered chatbot designed to educate and advise on sustainable farming practices, soil health, and climate-resilient agriculture.

## Features

- Conversational AI mentor using OpenAI's GPT model
- Web-based chat interface
- Chat history storage with Supabase
- Modular structure for future GIS/remote sensing integrations

## Setup Instructions

### Prerequisites

- Python 3.8+
- OpenAI API key
- Supabase account and project

### Installation

1. Clone or download the project files.

2. Navigate to the project directory:
   ```
   cd agrimind
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in your API keys:
     - `OPENAI_API_KEY`: Get from [OpenAI](https://platform.openai.com/)
     - `SUPABASE_URL`: Your Supabase project URL
     - `SUPABASE_KEY`: Your Supabase anon/public key

5. Set up Supabase database:
   - Create a new table called `chats` with the following columns:
     - `id` (auto-incrementing primary key)
     - `user_message` (text)
     - `bot_response` (text)
     - `created_at` (timestamp, default to now())

### Running the Application

1. Start the backend server:
   ```
   python main.py
   ```
   The server will run on `http://localhost:8000`

2. Open the frontend:
   - Open `static/index.html` in your web browser, or serve it via a web server.

3. Start chatting! Ask questions about farming practices, soil health, etc.

## Future Enhancements

- **GIS Integration**: Add endpoints to fetch real-time soil and vegetation data from APIs like Google Earth Engine or Sentinel Hub. The placeholder code in `main.py` shows where to implement this.
- **Voice Features**: Integrate speech-to-text and text-to-speech for accessibility.
- **User Authentication**: Add user accounts to personalize advice.
- **Offline Mode**: Cache responses for areas with poor internet.

## API Endpoints

- `POST /chat`: Send a message and receive AI response
  - Body: `{"message": "Your question here"}`
  - Response: `{"response": "AI answer"}`

## Deployment

### Backend (Render)
1. Push this repo to GitHub
2. Go to [render.com](https://render.com) and sign up
3. Create a new Web Service
4. Connect your GitHub repo
5. Set build command: `pip install -r requirements.txt`
6. Set start command: `python main.py`
7. Add environment variables: `OPENAI_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`
8. Deploy!

### Frontend (Vercel)
1. Create a new GitHub repo for the frontend
2. Copy `frontend/` files to the new repo
3. Update `script.js` API_BASE_URL to your Render backend URL
4. Push to GitHub
5. Go to [vercel.com](https://vercel.com) and sign up
6. Import the frontend GitHub repo
7. Deploy!

## Technologies Used

- Backend: FastAPI (Python)
- Frontend: HTML, CSS, JavaScript
- AI: OpenAI API
- Database: Supabase
- Deployment: Render (backend), Vercel (frontend)