import streamlit as st
import pandas as pd
import numpy as np
import requests
import unicodedata

# ... [Keep your existing logo functions and groups_data structure] ...

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_polymarket_events():
    """
    A robust fetcher that uses a browser-like User-Agent and handles
    potential API blocks by failing silently and returning an empty list 
    instead of throwing an error.
    """
    url = "https://gamma-api.polymarket.com/events"
    # Essential: Cloudflare blocks default Python user-agents.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        # Request with a timeout to prevent the app from hanging
        response = requests.get(url, params={"active": "true"}, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            # Handle the specific Polymarket JSON structure
            return data if isinstance(data, list) else data.get("data", [])
        else:
            return []
    except Exception as e:
        st.sidebar.error(f"API Connection Blocked: {e}")
        return []

def get_match_defaults(home_team, away_team, group_data, poly_events):
    """
    The 'Fail-Safe' Logic: 
    1. Calculate analytic xG (Always works)
    2. Attempt API lookup (If it fails, the defaults remain)
    """
    # 1. Analytic Proxy (Your safe fallback)
    h_s = next(t for t in group_data if t["Team"] == home_team)
    a_s = next(t for t in group_data if t["Team"] == away_team)
    h_xg = ((h_s["Goals Scored"]/max(1, h_s["Played"])) + (a_s["Goals Received"]/max(1, a_s["Played"])))/2 + 0.2
    a_xg = ((a_s["Goals Scored"]/max(1, a_s["Played"])) + (h_s["Goals Received"]/max(1, h_s["Played"])))/2
    
    defaults = {"ph": 50.0, "pa": 30.0, "xgh": h_xg, "xga": a_xg, "api_found": False}
    
    # 2. Try the API
    if poly_events:
        for event in poly_events:
            title = event.get("title", "")
            if is_team_match(home_team, title) and is_team_match(away_team, title):
                # Search markets
                markets = event.get("markets", [])
                for market in markets:
                    outcomes = market.get("outcomes", [])
                    prices = market.get("outcomePrices", [])
                    if len(outcomes) >= 2:
                        ph, pa = 0, 0
                        for i, o in enumerate(outcomes):
                            p = float(prices[i]) * 100
                            if is_team_match(home_team, o): ph = p
                            elif is_team_match(away_team, o): pa = p
                        if ph > 0 and pa > 0:
                            defaults.update({"ph": ph, "pa": pa, "api_found": True})
                            return defaults
    return defaults

# ... [Keep the rest of your H2H, resolve_ties, and UI logic same as before] ...
