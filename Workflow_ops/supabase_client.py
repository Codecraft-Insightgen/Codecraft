import os
from supabase import create_client
# from dotenv import load_dotenv

# load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL and KEY be set in the .env file")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)