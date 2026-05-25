import streamlit as st
import pandas as pd
import numpy as np

# Configure the page layout
st.set_page_config(page_title="Copa Libertadores 2026 Simulator", layout="wide")
st.title("🏆 Copa Libertadores 2026 Simulator")

def get_logo_url(filename):
    return f"https://github.com/jjhurta2/libertadores_simulator/blob/main/{filename}?raw=true"

def create_group_df(data):
    df = pd.DataFrame(data)
    df = df.rename(columns={
        "Position": "Pos", "Played": "GP", "Won": "W", "Drawn": "D", 
        "Lost": "L", "Goals Scored": "GF", "Goals Received": "GA", 
        "Goal Difference": "+/-", "Points": "Points"
    })
    return df[["Pos", "Logo", "Team", "GP", "W", "D", "L", "GF", "GA", "+/-", "Points"]]

# --- DATA ---
groups_data = {
    "Group A": [
        {"Position": 1, "Logo": get_logo_url("flamengo.png"), "Team": "Flamengo", "Played": 5, "Won": 4, "Lost": 0, "Drawn": 1, "Goals Scored": 11, "Goals Received": 2, "Goal Difference": 9, "Points": 13},
        {"Position": 2, "Logo": get_logo_url("dim.png"), "Team": "Independiente Medellín", "Played": 5, "Won": 2, "Lost": 2, "Drawn": 1, "Goals Scored": 6, "Goals Received": 10, "Goal Difference": -4, "Points": 7},
        {"Position": 3, "Logo": get_logo_url("estudiantes.png"), "Team": "Estudiantes de La Plata", "Played": 5, "Won": 1, "Lost": 1, "Drawn": 3, "Goals Scored": 5, "Goals Received": 5, "Goal Difference": 0, "Points": 6},
        {"Position": 4, "Logo": get_logo_url("cusco.png"), "Team": "Cusco FC", "Played": 5, "Won": 0, "Lost": 4, "Drawn": 1, "Goals Scored": 4, "Goals Received": 9, "Goal Difference": -5, "Points": 1}
    ],
    # ... [Keep your groups B-H dictionaries here] ...
}

# --- HARDCODED ODDS (Update these with the Polymarket values) ---
HARDCODED_ODDS = {
    "Lanús vs Mirassol": {"ph": 56.0, "pa": 18.0},
    "Flamengo vs Cusco FC": {"ph": 0.0, "pa": 0.0}, # Fill these in
    "Estudiantes de La Plata vs Independiente Medellín": {"ph": 0.0, "pa": 0.0},
    "Nacional de Football vs Coquimbo Unido": {"ph": 0.0, "pa": 0.0},
    "Universitario vs Deportes Tolima": {"ph": 0.0, "pa": 0.0},
    "Bolívar vs Ind. Rivadavia": {"ph": 0.0, "pa": 0.0},
    "Fluminense FC vs Deportivo La Guaira": {"ph": 0.0, "pa": 0.0},
    "Boca Juniors vs Universidad Católica": {"ph": 0.0, "pa": 0.0},
    "Cruzeiro vs Barcelona S.C.": {"ph": 0.0, "pa": 0.0},
    "Peñarol vs Independiente Santa Fe": {"ph": 0.0, "pa": 0.0},
    "Corinthians vs Platense": {"ph": 0.0, "pa": 0.0},
    "Cerro Porteño vs Sporting Cristal": {"ph": 0.0, "pa": 0.0},
    "Palmeiras vs Junior FC": {"ph": 0.0, "pa": 0.0},
    "LDU Quito vs Always Ready": {"ph": 0.0, "pa": 0.0},
    "Independiente del Valle vs Rosario Central": {"ph": 0.0, "pa": 0.0},
    "Libertad vs Universidad Central": {"ph": 0.0, "pa": 0.0}
}

def get_match_defaults(home, away, group_data):
    h_s = next(t for t in group_data if t["Team"] == home)
    a_s = next(t for t in group_data if t["Team"] == away)
    h_xg = ((h_s["Goals Scored"]/max(1, h_s["Played"])) + (a_s["Goals Received"]/max(1, a_s["Played"])))/2 + 0.2
    a_xg = ((a_s["Goals Scored"]/max(1, a_s["Played"])) + (h_s["Goals Received"]/max(1, h_s["Played"])))/2
    
    match_key = f"{home} vs {away}"
    # If the user hasn't filled in the odds yet, use 0/0 so the user is forced to provide input
    odds = HARDCODED_ODDS.get(match_key, {"ph": 0.0, "pa": 0.0})
    return {"ph": odds["ph"], "pa": odds["pa"], "xgh": float(h_xg), "xga": float(a_xg)}

# --- LOGIC & UI ---
def simulate_match_randomly(ph, pt, pa, xgh, xga):
    p = [ph/100, pt/100, pa/100]
    outcome = np.random.choice(['H', 'D', 'A'], p=p)
    for _ in range(100):
        hg, ag = np.random.poisson(xgh), np.random.poisson(xga)
        if (outcome == 'H' and hg > ag) or (outcome == 'D' and hg == ag) or (outcome == 'A' and hg < ag): return hg, ag
    return (1, 0) if outcome == 'H' else (0, 0) if outcome == 'D' else (0, 1)

# ... [Keep your existing calculate_standings, resolve_ties, and UI logic same as before] ...
