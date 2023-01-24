"""Module supports CRUD for tradeable asset table"""

from .client import supabase

def create():
    pass

def getByTicker():
    print(supabase)
    # asset = supabase.from("tradeable_asset").select("*")
    # print(asset)


if __name__ == "__main__":
    getByTicker()