from supabase import create_client, Client
from dotenv import load_dotenv
import os
from typing import AsyncGenerator

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("Supabase client initialized successfully!")
except Exception as e:
    print("Error initializing Supabase client:", e)
    raise e

def get_supabase()-> AsyncGenerator[Client, None]:
    yield supabase
