import streamlit as st
import pandas as pd
import numpy as np
import requests

# --- SECURE API KEY ---
def get_api_key():
    try:
        return st.secrets["ODDS_API_KEY"]
    except KeyError:
        st.error("API Key not found! Ensure your .streamlit/secrets.toml file exists.")
        st.stop()

# Configure the page layout
st.set_page_config(page_title="Copa Libertadores 2026 Predictor", layout="wide")
st.title("Copa Libertadores 2026 Predictor")

# --- DATA FORMATTING ---
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

# --- TEAM METADATA (logos only, no standings) ---
teams_meta = {
    "Group A": [
        {"Team": "Flamengo",                    "Logo": get_logo_url("flamengo.png")},
        {"Team": "Independiente Medellín",       "Logo": get_logo_url("dim.png")},
        {"Team": "Estudiantes de La Plata",      "Logo": get_logo_url("estudiantes.png")},
        {"Team": "Cusco FC",                     "Logo": get_logo_url("cusco.png")},
    ],
    "Group B": [
        {"Team": "Coquimbo Unido",               "Logo": get_logo_url("coquimbo.png")},
        {"Team": "Deportes Tolima",              "Logo": get_logo_url("tolima.png")},
        {"Team": "Universitario",                "Logo": get_logo_url("universitario.png")},
        {"Team": "Nacional de Football",         "Logo": get_logo_url("nacional.png")},
    ],
    "Group C": [
        {"Team": "Ind. Rivadavia",               "Logo": get_logo_url("rivadavia.png")},
        {"Team": "Bolívar",                      "Logo": get_logo_url("bolivar.png")},
        {"Team": "Fluminense FC",                "Logo": get_logo_url("fluminense.png")},
        {"Team": "Deportivo La Guaira",          "Logo": get_logo_url("laguaira.png")},
    ],
    "Group D": [
        {"Team": "Universidad Católica",         "Logo": get_logo_url("uc.png")},
        {"Team": "Cruzeiro",                     "Logo": get_logo_url("cruzeiro.png")},
        {"Team": "Boca Juniors",                 "Logo": get_logo_url("boca.png")},
        {"Team": "Barcelona S.C.",               "Logo": get_logo_url("bsc.png")},
    ],
    "Group E": [
        {"Team": "Corinthians",                  "Logo": get_logo_url("corinthians.png")},
        {"Team": "Platense",                     "Logo": get_logo_url("platense.png")},
        {"Team": "Independiente Santa Fe",       "Logo": get_logo_url("santafe.png")},
        {"Team": "Peñarol",                      "Logo": get_logo_url("penarol.png")},
    ],
    "Group F": [
        {"Team": "Cerro Porteño",                "Logo": get_logo_url("cerroporteno.png")},
        {"Team": "Palmeiras",                    "Logo": get_logo_url("palmeiras.png")},
        {"Team": "Sporting Cristal",             "Logo": get_logo_url("cristal.png")},
        {"Team": "Junior FC",                    "Logo": get_logo_url("junior.png")},
    ],
    "Group G": [
        {"Team": "Mirassol",                     "Logo": get_logo_url("mirassol.png")},
        {"Team": "LDU Quito",                    "Logo": get_logo_url("ldu.png")},
        {"Team": "Lanús",                        "Logo": get_logo_url("lanus.png")},
        {"Team": "Always Ready",                 "Logo": get_logo_url("alwaysready.png")},
    ],
    "Group H": [
        {"Team": "Rosario Central",              "Logo": get_logo_url("rosariocentral.png")},
        {"Team": "Independiente del Valle",      "Logo": get_logo_url("idv.png")},
        {"Team": "Universidad Central",          "Logo": get_logo_url("universidadcentral.png")},
        {"Team": "Libertad",                     "Logo": get_logo_url("libertad.png")},
    ],
}

# --- PAST MATCH RESULTS (Matchdays 1–5) ---
# Format: group, home, away, home_score, away_score
past_matches = [
    # GROUP A
    {"group": "Group A", "home": "Flamengo",               "away": "Estudiantes de La Plata",  "home_score": 3, "away_score": 0},
    {"group": "Group A", "home": "Cusco FC",               "away": "Independiente Medellín",   "home_score": 1, "away_score": 2},
    {"group": "Group A", "home": "Flamengo",               "away": "Cusco FC",                 "home_score": 3, "away_score": 1},
    {"group": "Group A", "home": "Independiente Medellín", "away": "Estudiantes de La Plata",  "home_score": 2, "away_score": 1},
    {"group": "Group A", "home": "Flamengo",               "away": "Independiente Medellín",   "home_score": 2, "away_score": 1},
    {"group": "Group A", "home": "Estudiantes de La Plata","away": "Cusco FC",                 "home_score": 1, "away_score": 1},
    {"group": "Group A", "home": "Cusco FC",               "away": "Flamengo",                 "home_score": 1, "away_score": 2},
    {"group": "Group A", "home": "Estudiantes de La Plata","away": "Independiente Medellín",   "home_score": 2, "away_score": 0},
    {"group": "Group A", "home": "Independiente Medellín", "away": "Cusco FC",                 "home_score": 2, "away_score": 1},
    {"group": "Group A", "home": "Estudiantes de La Plata","away": "Flamengo",                 "home_score": 1, "away_score": 1},
    # GROUP B
    {"group": "Group B", "home": "Coquimbo Unido",         "away": "Nacional de Football",     "home_score": 3, "away_score": 1},
    {"group": "Group B", "home": "Deportes Tolima",        "away": "Universitario",            "home_score": 2, "away_score": 1},
    {"group": "Group B", "home": "Coquimbo Unido",         "away": "Deportes Tolima",          "home_score": 2, "away_score": 1},
    {"group": "Group B", "home": "Universitario",          "away": "Nacional de Football",     "home_score": 2, "away_score": 2},
    {"group": "Group B", "home": "Nacional de Football",   "away": "Deportes Tolima",          "home_score": 1, "away_score": 2},
    {"group": "Group B", "home": "Universitario",          "away": "Coquimbo Unido",           "home_score": 1, "away_score": 1},
    {"group": "Group B", "home": "Deportes Tolima",        "away": "Nacional de Football",     "home_score": 2, "away_score": 2},
    {"group": "Group B", "home": "Coquimbo Unido",         "away": "Universitario",            "home_score": 2, "away_score": 1},
    {"group": "Group B", "home": "Nacional de Football",   "away": "Universitario",            "home_score": 0, "away_score": 1},
    {"group": "Group B", "home": "Deportes Tolima",        "away": "Coquimbo Unido",           "home_score": 0, "away_score": 2},
    # GROUP C
    {"group": "Group C", "home": "Ind. Rivadavia",         "away": "Fluminense FC",            "home_score": 3, "away_score": 1},
    {"group": "Group C", "home": "Bolívar",                "away": "Deportivo La Guaira",      "home_score": 1, "away_score": 1},
    {"group": "Group C", "home": "Ind. Rivadavia",         "away": "Bolívar",                  "home_score": 3, "away_score": 1},
    {"group": "Group C", "home": "Fluminense FC",          "away": "Deportivo La Guaira",      "home_score": 1, "away_score": 1},
    {"group": "Group C", "home": "Bolívar",                "away": "Fluminense FC",            "home_score": 1, "away_score": 1},
    {"group": "Group C", "home": "Deportivo La Guaira",    "away": "Ind. Rivadavia",           "home_score": 1, "away_score": 2},
    {"group": "Group C", "home": "Fluminense FC",          "away": "Bolívar",                  "home_score": 1, "away_score": 2},
    {"group": "Group C", "home": "Ind. Rivadavia",         "away": "Deportivo La Guaira",      "home_score": 2, "away_score": 1},
    {"group": "Group C", "home": "Deportivo La Guaira",    "away": "Fluminense FC",            "home_score": 2, "away_score": 1},
    {"group": "Group C", "home": "Bolívar",                "away": "Ind. Rivadavia",           "home_score": 0, "away_score": 2},
    # GROUP D
    {"group": "Group D", "home": "Universidad Católica",   "away": "Boca Juniors",             "home_score": 2, "away_score": 1},
    {"group": "Group D", "home": "Cruzeiro",               "away": "Barcelona S.C.",           "home_score": 1, "away_score": 0},
    {"group": "Group D", "home": "Universidad Católica",   "away": "Cruzeiro",                 "home_score": 1, "away_score": 1},
    {"group": "Group D", "home": "Boca Juniors",           "away": "Barcelona S.C.",           "home_score": 2, "away_score": 0},
    {"group": "Group D", "home": "Boca Juniors",           "away": "Cruzeiro",                 "home_score": 2, "away_score": 1},
    {"group": "Group D", "home": "Barcelona S.C.",         "away": "Universidad Católica",     "home_score": 1, "away_score": 2},
    {"group": "Group D", "home": "Cruzeiro",               "away": "Boca Juniors",             "home_score": 1, "away_score": 1},
    {"group": "Group D", "home": "Universidad Católica",   "away": "Barcelona S.C.",           "home_score": 1, "away_score": 0},
    {"group": "Group D", "home": "Barcelona S.C.",         "away": "Boca Juniors",             "home_score": 1, "away_score": 0},
    {"group": "Group D", "home": "Cruzeiro",               "away": "Universidad Católica",     "home_score": 1, "away_score": 2},
    # GROUP E
    {"group": "Group E", "home": "Corinthians",            "away": "Peñarol",                  "home_score": 2, "away_score": 1},
    {"group": "Group E", "home": "Platense",               "away": "Independiente Santa Fe",   "home_score": 2, "away_score": 2},
    {"group": "Group E", "home": "Corinthians",            "away": "Platense",                 "home_score": 2, "away_score": 1},
    {"group": "Group E", "home": "Independiente Santa Fe", "away": "Peñarol",                  "home_score": 1, "away_score": 1},
    {"group": "Group E", "home": "Peñarol",                "away": "Platense",                 "home_score": 1, "away_score": 1},
    {"group": "Group E", "home": "Independiente Santa Fe", "away": "Corinthians",              "home_score": 1, "away_score": 2},
    {"group": "Group E", "home": "Platense",               "away": "Peñarol",                  "home_score": 2, "away_score": 1},
    {"group": "Group E", "home": "Corinthians",            "away": "Independiente Santa Fe",   "home_score": 2, "away_score": 1},
    {"group": "Group E", "home": "Peñarol",                "away": "Corinthians",              "home_score": 1, "away_score": 1},
    {"group": "Group E", "home": "Independiente Santa Fe", "away": "Platense",                 "home_score": 1, "away_score": 1},
    # GROUP F
    {"group": "Group F", "home": "Cerro Porteño",          "away": "Sporting Cristal",         "home_score": 1, "away_score": 0},
    {"group": "Group F", "home": "Palmeiras",              "away": "Junior FC",                "home_score": 2, "away_score": 1},
    {"group": "Group F", "home": "Cerro Porteño",          "away": "Palmeiras",                "home_score": 1, "away_score": 1},
    {"group": "Group F", "home": "Junior FC",              "away": "Sporting Cristal",         "home_score": 1, "away_score": 2},
    {"group": "Group F", "home": "Palmeiras",              "away": "Sporting Cristal",         "home_score": 2, "away_score": 2},
    {"group": "Group F", "home": "Cerro Porteño",          "away": "Junior FC",                "home_score": 1, "away_score": 0},
    {"group": "Group F", "home": "Sporting Cristal",       "away": "Palmeiras",                "home_score": 2, "away_score": 1},
    {"group": "Group F", "home": "Junior FC",              "away": "Cerro Porteño",            "home_score": 1, "away_score": 2},
    {"group": "Group F", "home": "Sporting Cristal",       "away": "Junior FC",                "home_score": 2, "away_score": 2},
    {"group": "Group F", "home": "Palmeiras",              "away": "Cerro Porteño",            "home_score": 1, "away_score": 1},
    # GROUP G
    {"group": "Group G", "home": "Mirassol",               "away": "Always Ready",             "home_score": 2, "away_score": 1},
    {"group": "Group G", "home": "LDU Quito",              "away": "Lanús",                    "home_score": 2, "away_score": 0},
    {"group": "Group G", "home": "Mirassol",               "away": "LDU Quito",                "home_score": 2, "away_score": 1},
    {"group": "Group G", "home": "Lanús",                  "away": "Always Ready",             "home_score": 0, "away_score": 2},
    {"group": "Group G", "home": "Mirassol",               "away": "Lanús",                    "home_score": 2, "away_score": 0},
    {"group": "Group G", "home": "Always Ready",           "away": "LDU Quito",                "home_score": 1, "away_score": 2},
    {"group": "Group G", "home": "LDU Quito",              "away": "Always Ready",             "home_score": 0, "away_score": 1},
    {"group": "Group G", "home": "Lanús",                  "away": "Mirassol",                 "home_score": 1, "away_score": 2},
    {"group": "Group G", "home": "Always Ready",           "away": "Mirassol",                 "home_score": 1, "away_score": 1},
    {"group": "Group G", "home": "LDU Quito",              "away": "Mirassol",                 "home_score": 1, "away_score": 0},
    # GROUP H
    {"group": "Group H", "home": "Rosario Central",        "away": "Libertad",                 "home_score": 3, "away_score": 0},
    {"group": "Group H", "home": "Independiente del Valle","away": "Universidad Central",      "home_score": 3, "away_score": 1},
    {"group": "Group H", "home": "Rosario Central",        "away": "Independiente del Valle",  "home_score": 2, "away_score": 2},
    {"group": "Group H", "home": "Libertad",               "away": "Universidad Central",      "home_score": 1, "away_score": 2},
    {"group": "Group H", "home": "Independiente del Valle","away": "Libertad",                 "home_score": 2, "away_score": 1},
    {"group": "Group H", "home": "Universidad Central",    "away": "Rosario Central",          "home_score": 1, "away_score": 2},
    {"group": "Group H", "home": "Libertad",               "away": "Independiente del Valle",  "home_score": 1, "away_score": 2},
    {"group": "Group H", "home": "Rosario Central",        "away": "Universidad Central",      "home_score": 2, "away_score": 1},
    {"group": "Group H", "home": "Universidad Central",    "away": "Independiente del Valle",  "home_score": 2, "away_score": 1},
    {"group": "Group H", "home": "Libertad",               "away": "Rosario Central",          "home_score": 2, "away_score": 2},
]

# --- LOGIC ---
def calculate_standings(group_teams, all_group_matches):
    logo_map = {t["Team"]: t["Logo"] for t in group_teams}
    stats = {
        t["Team"]: {
            "Played": 0, "Won": 0, "Lost": 0, "Drawn": 0,
            "Goals Scored": 0, "Goals Received": 0, "Points": 0,
            "Logo": logo_map.get(t["Team"], "")
        }
        for t in group_teams
    }
    for m in all_group_matches:
        home, away, hg, ag = m["home"], m["away"], m["home_score"], m["away_score"]
        if home in stats and away in stats:
            stats[home]["Played"] += 1
            stats[away]["Played"] += 1
            stats[home]["Goals Scored"] += hg
            stats[home]["Goals Received"] += ag
            stats[away]["Goals Scored"] += ag
            stats[away]["Goals Received"] += hg
            if hg > ag:
                stats[home]["Won"] += 1
                stats[home]["Points"] += 3
                stats[away]["Lost"] += 1
            elif ag > hg:
                stats[away]["Won"] += 1
                stats[away]["Points"] += 3
                stats[home]["Lost"] += 1
            else:
                stats[home]["Drawn"] += 1
                stats[away]["Drawn"] += 1
                stats[home]["Points"] += 1
                stats[away]["Points"] += 1
    for team in stats:
        stats[team]["Goal Difference"] = stats[team]["Goals Scored"] - stats[team]["Goals Received"]
        stats[team]["Team"] = team
    return list(stats.values())

def resolve_ties(teams_list, all_group_matches):
    points_groups = {}
    for team in teams_list:
        p = team["Points"]
        if p not in points_groups:
            points_groups[p] = []
        points_groups[p].append(team)
    final_sorted_group = []
    for p in sorted(points_groups.keys(), reverse=True):
        tied = points_groups[p]
        if len(tied) == 1:
            final_sorted_group.append(tied[0])
            continue
        names = [t["Team"] for t in tied]
        h2h = [m for m in all_group_matches if m["home"] in names and m["away"] in names]
        stats = calculate_standings(tied, h2h)
        for s in stats:
            orig = next(t for t in tied if t["Team"] == s["Team"])
            s["Total GD"] = orig["Goal Difference"]
            s["Total GS"] = orig["Goals Scored"]
            s["Original Data"] = orig
        stats.sort(
            key=lambda x: (
                x["Points"], x["Goal Difference"], x["Goals Scored"],
                x["Original Data"]["Points"], x["Total GD"], x["Total GS"]
            ),
            reverse=True
        )
        for s in stats:
            final_sorted_group.append(s["Original Data"])
    for i, t in enumerate(final_sorted_group):
        t["Position"] = i + 1
    return final_sorted_group

def get_sorted_standings(group_name):
    """Compute and sort standings for a group from past_matches."""
    group_teams = teams_meta[group_name]
    group_matches = [m for m in past_matches if m["group"] == group_name]
    raw = calculate_standings(group_teams, group_matches)
    raw.sort(key=lambda x: (x["Points"], x["Goal Difference"], x["Goals Scored"]), reverse=True)
    sorted_s = resolve_ties(raw, group_matches)
    return sorted_s

def simulate_match_randomly(ph, pt, pa, xgh, xga):
    p = [ph / 100, pt / 100, pa / 100]
    outcome = np.random.choice(['H', 'D', 'A'], p=p)
    for _ in range(100):
        hg, ag = np.random.poisson(xgh), np.random.poisson(xga)
        if ((outcome == 'H' and hg > ag) or
                (outcome == 'D' and hg == ag) or
                (outcome == 'A' and hg < ag)):
            return hg, ag
    return (1, 0) if outcome == 'H' else (0, 0) if outcome == 'D' else (0, 1)

# --- API HELPERS ---
TEAM_MAP = {
    "Flamengo": "Flamengo",
    "Independiente Medellín": "Independiente Medellín",
    "Estudiantes de La Plata": "Estudiantes de La Plata",
    "Cusco FC": "Cusco FC",
    "Coquimbo Unido": "Coquimbo Unido",
    "Deportes Tolima": "Deportes Tolima",
    "Universitario": "Club Universitario de Deportes",
    "Nacional de Football": "Club Nacional de Football",
    "Ind. Rivadavia": "Independiente Rivadavia",
    "Bolívar": "Club Bolívar",
    "Fluminense FC": "Fluminense FC",
    "Deportivo La Guaira": "Deportivo La Guaira F.C.",
    "Universidad Católica": "Club Deportivo Universidad Católica",
    "Cruzeiro": "Cruzeiro Esporte Clube",
    "Boca Juniors": "Boca Juniors",
    "Barcelona S.C.": "Barcelona S.C.",
    "Corinthians": "Sport Club Corinthians Paulista",
    "Platense": "Club Atlético Platense",
    "Independiente Santa Fe": "Independiente Santa Fe",
    "Peñarol": "Club Atlético Peñarol",
    "Cerro Porteño": "Club Cerro Porteño",
    "Palmeiras": "SE Palmeiras",
    "Sporting Cristal": "Club Sporting Cristal",
    "Junior FC": "Junior FC",
    "Mirassol": "Mirassol Futebol Clube",
    "LDU Quito": "LDU Quito",
    "Lanús": "Club Atlético Lanús",
    "Always Ready": "Club Always Ready",
    "Rosario Central": "Club Atlético Rosario Central",
    "Independiente del Valle": "Independiente del Valle",
    "Universidad Central": "Universidad Central de Venezuela F.C.",
    "Libertad": "Club Libertad",
}

@st.cache_data(ttl=3600)
def fetch_odds_from_odds_api():
    api_key = get_api_key()
    url = "https://api.the-odds-api.com/v4/sports/soccer_conmebol_copa_libertadores/odds/"
    params = {"apiKey": api_key, "regions": "us", "markets": "h2h"}
    resp = requests.get(url, params=params)
    return resp.json() if resp.status_code == 200 else []

def get_fair_probabilities(home_team, api_odds_data):
    """Returns (ph, pa, pd) as floats, or fallback (45.0, 30.0, 25.0) if not found."""
    search_name = TEAM_MAP.get(home_team, home_team)
    for match in api_odds_data:
        if not match.get("bookmakers"):
            continue
        if search_name.lower() in match["home_team"].lower():
            try:
                outcomes = match["bookmakers"][0]["markets"][0]["outcomes"]
                odds = {o["name"]: o["price"] for o in outcomes}
                p_home = 1 / odds.get(match["home_team"], 2.0)
                p_away = 1 / odds.get(match["away_team"], 2.0)
                p_draw = 1 / odds.get("Draw", 3.0)
                total = p_home + p_away + p_draw
                return (p_home / total) * 100, (p_away / total) * 100, (p_draw / total) * 100
            except (KeyError, ZeroDivisionError, TypeError):
                break
    # Fallback: use equal probabilities
    return 40.0, 30.0, 30.0

def get_match_defaults(home, away, group_data):
    """Compute default inputs for the match simulator form."""
    h_s = next((t for t in group_data if t["Team"] == home), None)
    a_s = next((t for t in group_data if t["Team"] == away), None)

    # xG defaults based on goals scored/conceded per game
    if h_s and a_s and max(1, h_s["Played"]) and max(1, a_s["Played"]):
        h_xg = ((h_s["Goals Scored"] / max(1, h_s["Played"])) +
                (a_s["Goals Received"] / max(1, a_s["Played"]))) / 2 + 0.2
        a_xg = ((a_s["Goals Scored"] / max(1, a_s["Played"])) +
                (h_s["Goals Received"] / max(1, h_s["Played"]))) / 2
    else:
        h_xg, a_xg = 1.3, 1.0

    # Probability defaults from odds API (safe — always returns numbers now)
    api_data = fetch_odds_from_odds_api()
    ph, pa, pd = get_fair_probabilities(home, api_data)

    return {
        "ph": round(float(ph), 1),
        "pa": round(float(pa), 1),
        "pd": round(float(pd), 1),
        "xgh": round(float(h_xg), 2),
        "xga": round(float(a_xg), 2),
    }

# --- BUILD groups_data FROM PAST MATCHES ---
# This replaces the hardcoded standings with computed ones.
groups_data = {}
for group_name in teams_meta:
    sorted_standings = get_sorted_standings(group_name)
    groups_data[group_name] = sorted_standings

# --- UI: STANDINGS TABLES ---
group_items = list(groups_data.items())
for i in range(0, len(group_items), 2):
    c1, c2 = st.columns(2)
    for idx, col in enumerate([c1, c2]):
        if i + idx < len(group_items):
            g_name, g_data = group_items[i + idx]
            with col:
                st.subheader(g_name)
                st.data_editor(
                    create_group_df(g_data),
                    column_config={
                        "Logo": st.column_config.ImageColumn("Logo", help="Team Logo"),
                        "Pos": st.column_config.NumberColumn("Pos", format="%d"),
                    },
                    hide_index=True,
                    use_container_width=True,
                    disabled=True,
                )

st.divider()
st.header("Matchday 6 Simulator")
mc_iterations = st.number_input("Iterations", value=1000, min_value=100, max_value=50000)

predictions = {}
matchday_6_fixtures = {
    "Group A": [("Flamengo", "Cusco FC"), ("Estudiantes de La Plata", "Independiente Medellín")],
    "Group B": [("Nacional de Football", "Coquimbo Unido"), ("Universitario", "Deportes Tolima")],
    "Group C": [("Bolívar", "Ind. Rivadavia"), ("Fluminense FC", "Deportivo La Guaira")],
    "Group D": [("Boca Juniors", "Universidad Católica"), ("Cruzeiro", "Barcelona S.C.")],
    "Group E": [("Peñarol", "Independiente Santa Fe"), ("Corinthians", "Platense")],
    "Group F": [("Cerro Porteño", "Sporting Cristal"), ("Palmeiras", "Junior FC")],
    "Group G": [("Lanús", "Mirassol"), ("LDU Quito", "Always Ready")],
    "Group H": [("Independiente del Valle", "Rosario Central"), ("Libertad", "Universidad Central")],
}

with st.form("mc_form"):
    for group_name, fixtures in matchday_6_fixtures.items():
        st.markdown(f"#### {group_name}")
        group_preds = []
        match_cols = st.columns(2)
        for i, (home, away) in enumerate(fixtures):
            defaults = get_match_defaults(home, away, groups_data[group_name])
            h_l = next((t["Logo"] for t in groups_data[group_name] if t["Team"] == home), "")
            a_l = next((t["Logo"] for t in groups_data[group_name] if t["Team"] == away), "")
            with match_cols[i]:
                c = st.columns([3, 1, 1, 1, 1, 3])
                with c[0]:
                    st.markdown(
                        f"<div style='display:flex;align-items:center;justify-content:flex-end;margin-top:28px;'>"
                        f"<img src='{h_l}' width='24' height='24' style='margin-right:8px;'>"
                        f"<b style='font-size:0.85em'>{home}</b></div>",
                        unsafe_allow_html=True,
                    )
                with c[1]: ph = st.number_input("H%",  key=f"{group_name}_{i}_ph",  value=defaults["ph"])
                with c[2]: pa = st.number_input("A%",  key=f"{group_name}_{i}_pa",  value=defaults["pa"])
                with c[3]: xgh = st.number_input("HxG", key=f"{group_name}_{i}_xgh", value=defaults["xgh"])
                with c[4]: xga = st.number_input("AxG", key=f"{group_name}_{i}_xga", value=defaults["xga"])
                with c[5]:
                    st.markdown(
                        f"<div style='display:flex;align-items:center;justify-content:flex-start;margin-top:28px;'>"
                        f"<img src='{a_l}' width='24' height='24' style='margin-right:8px;'>"
                        f"<b style='font-size:0.85em'>{away}</b></div>",
                        unsafe_allow_html=True,
                    )
                group_preds.append({
                    "group": group_name, "home": home, "away": away,
                    "ph": ph, "pt": defaults["pd"], "pa": pa, "xgh": xgh, "xga": xga,
                })
        predictions[group_name] = group_preds

    run_mc = st.form_submit_button("Predict", type="primary")

if run_mc:
    mc_results = {
        g: {t["Team"]: {1: 0, 2: 0, 3: 0, 4: 0} for t in groups_data[g]}
        for g in groups_data
    }
    group_past = {g: [m for m in past_matches if m["group"] == g] for g in groups_data}

    for _ in range(int(mc_iterations)):
        for g_name in groups_data.keys():
            sim_m6 = []
            for m in predictions[g_name]:
                hg, ag = simulate_match_randomly(m["ph"], m["pt"], m["pa"], m["xgh"], m["xga"])
                sim_m6.append({"home": m["home"], "away": m["away"], "home_score": hg, "away_score": ag})

            all_matches = group_past[g_name] + sim_m6
            raw_standings = calculate_standings(teams_meta[g_name], all_matches)
            sorted_s = resolve_ties(raw_standings, all_matches)

            for pos, team in enumerate(sorted_s):
                mc_results[g_name][team["Team"]][pos + 1] += 1

    for g_name in groups_data.keys():
        st.subheader(f"{g_name} Matrix")
        df_res = pd.DataFrame([
            {"Team": t, **{f"{p}º": f"{(c / mc_iterations) * 100:.1f}%" for p, c in pos.items()}}
            for t, pos in mc_results[g_name].items()
        ])
        st.dataframe(df_res, hide_index=True, use_container_width=True)
