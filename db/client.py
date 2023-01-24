"""Module provides supabase client"""
import os

from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
url: str = os.environ.get("SUPABASE_URL", "https://gwtmyrphmvdswrbssowi.supabase.co")
key: str = os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd3dG15cnBobXZkc3dyYnNzb3dpIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzQ1Mzc3MDMsImV4cCI6MTk5MDExMzcwM30.44ow3Hhb5qfSWfzPfNHsuRj9Mj7RXGYV27BENA0czLg")
supabase: Client = create_client(url, key, options={'timeout': 10})
