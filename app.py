import streamlit as st
import pandas as pd
import numpy as np
import requests
from scipy.optimize import minimize

# --- SECURE API KEY ---
def get_api_key():
    try:
        return st.secrets["ODDS_API_KEY"]
    except KeyError:
        st.error("API Key not found! Ensure your .streamlit/secrets.toml file exists.")
        st.stop()

st.set_page_config(page_title="Copa Libertadores 2026 Predictor", layout="wide")
st.title("Copa Libertadores 2026 Predictor")

# --- DATA FORMATTING ---
def get_logo_url(filename):
    return f"https://github.com/jjhurta2/libertadores_simulator/blob/main/logos/{filename}?raw=true"

def create_group_df(data):
    df = pd.DataFrame(data)
    df = df.rename(columns={
        "Position": "Pos", "Played": "GP", "Won": "W", "Drawn": "D",
        "Lost": "L", "Goals Scored": "GF", "Goals Received": "GA",
        "Goal Difference": "+/-", "Points": "Points"
    })
    return df[["Pos", "Logo", "Team", "GP", "W", "D", "L", "GF", "GA", "+/-", "Points"]]

# --- TEAM METADATA ---
teams_meta = {
    "Group A": [
        {"Team": "Flamengo",                     "Logo": get_logo_url("flamengo.png")},
        {"Team": "DIM",                          "Logo": get_logo_url("dim.png")},
        {"Team": "Estudiantes",                  "Logo": get_logo_url("estudiantes.png")},
        {"Team": "Cusco",                        "Logo": get_logo_url("cusco.png")},
    ],
    "Group B": [
        {"Team": "Coquimbo Unido",               "Logo": get_logo_url("coquimbo.png")},
        {"Team": "Deportes Tolima",              "Logo": get_logo_url("tolima.png")},
        {"Team": "Universitario",                "Logo": get_logo_url("universitario.png")},
        {"Team": "Nacional",                     "Logo": get_logo_url("nacional.png")},
    ],
    "Group C": [
        {"Team": "Ind. Rivadavia",               "Logo": get_logo_url("rivadavia.png")},
        {"Team": "Bolívar",                      "Logo": get_logo_url("bolivar.png")},
        {"Team": "Fluminense",                   "Logo": get_logo_url("fluminense.png")},
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

# --- TOURNAMENT RANKING (for home/away determination) ---
TOURNAMENT_RANKING = [
    "Flamengo",
    "Ind. Rivadavia",
    "Independiente del Valle",
    "Universidad Católica",
    "Cerro Porteño",
    "LDU Quito",
    "Corinthians",
    "Coquimbo Unido",
    "Rosario Central",
    "Mirassol",
    "Palmeiras",
    "Cruzeiro",
    "Platense",
    "Estudiantes",
    "Deportes Tolima",
    "Fluminense",
]

def get_team_ranking(team_name):
    """Returns rank position (0 = highest). Higher rank plays away first."""
    try:
        return TOURNAMENT_RANKING.index(team_name)
    except ValueError:
        return 999

# --- PAST MATCH RESULTS (All Group Stage Matchdays) ---
past_matches = [
    # GROUP A
    {"group": "Group A", "home": "DIM",                    "away": "Estudiantes",              "home_score": 1, "away_score": 1},
    {"group": "Group A", "home": "Cusco",                  "away": "Flamengo",                 "home_score": 0, "away_score": 2},
    {"group": "Group A", "home": "Estudiantes",            "away": "Cusco",                    "home_score": 2, "away_score": 1},
    {"group": "Group A", "home": "Flamengo",               "away": "DIM",                      "home_score": 4, "away_score": 1},
    {"group": "Group A", "home": "Estudiantes",            "away": "Flamengo",                 "home_score": 1, "away_score": 1},
    {"group": "Group A", "home": "DIM",                    "away": "Cusco",                    "home_score": 1, "away_score": 0},
    {"group": "Group A", "home": "DIM",                    "away": "Flamengo",                 "home_score": 0, "away_score": 3},
    {"group": "Group A", "home": "Cusco",                  "away": "Estudiantes",              "home_score": 1, "away_score": 1},
    {"group": "Group A", "home": "Flamengo",               "away": "Estudiantes",              "home_score": 1, "away_score": 0},
    {"group": "Group A", "home": "Cusco",                  "away": "DIM",                      "home_score": 2, "away_score": 3},
    {"group": "Group A", "home": "Estudiantes",            "away": "DIM",                      "home_score": 1, "away_score": 0},
    {"group": "Group A", "home": "Flamengo",               "away": "Cusco",                    "home_score": 3, "away_score": 0},
    # GROUP B
    {"group": "Group B", "home": "Deportes Tolima",        "away": "Universitario",            "home_score": 0, "away_score": 0},
    {"group": "Group B", "home": "Coquimbo Unido",         "away": "Nacional",                 "home_score": 1, "away_score": 1},
    {"group": "Group B", "home": "Nacional",               "away": "Deportes Tolima",          "home_score": 3, "away_score": 1},
    {"group": "Group B", "home": "Universitario",          "away": "Coquimbo Unido",           "home_score": 0, "away_score": 2},
    {"group": "Group B", "home": "Deportes Tolima",        "away": "Coquimbo Unido",           "home_score": 3, "away_score": 0},
    {"group": "Group B", "home": "Universitario",          "away": "Nacional",                 "home_score": 4, "away_score": 2},
    {"group": "Group B", "home": "Deportes Tolima",        "away": "Nacional",                 "home_score": 3, "away_score": 0},
    {"group": "Group B", "home": "Coquimbo Unido",         "away": "Universitario",            "home_score": 2, "away_score": 1},
    {"group": "Group B", "home": "Coquimbo Unido",         "away": "Deportes Tolima",          "home_score": 3, "away_score": 0},
    {"group": "Group B", "home": "Nacional",               "away": "Universitario",            "home_score": 0, "away_score": 0},
    {"group": "Group B", "home": "Nacional",               "away": "Coquimbo Unido",           "home_score": 1, "away_score": 0},
    {"group": "Group B", "home": "Universitario",          "away": "Deportes Tolima",          "home_score": 0, "away_score": 0},
    # GROUP C
    {"group": "Group C", "home": "Deportivo La Guaira",    "away": "Fluminense",               "home_score": 0, "away_score": 0},
    {"group": "Group C", "home": "Ind. Rivadavia",         "away": "Bolívar",                  "home_score": 1, "away_score": 0},
    {"group": "Group C", "home": "Bolívar",                "away": "Deportivo La Guaira",      "home_score": 1, "away_score": 1},
    {"group": "Group C", "home": "Fluminense",             "away": "Ind. Rivadavia",           "home_score": 1, "away_score": 2},
    {"group": "Group C", "home": "Ind. Rivadavia",         "away": "Deportivo La Guaira",      "home_score": 4, "away_score": 1},
    {"group": "Group C", "home": "Bolívar",                "away": "Fluminense",               "home_score": 2, "away_score": 0},
    {"group": "Group C", "home": "Deportivo La Guaira",    "away": "Bolívar",                  "home_score": 1, "away_score": 1},
    {"group": "Group C", "home": "Ind. Rivadavia",         "away": "Fluminense",               "home_score": 1, "away_score": 1},
    {"group": "Group C", "home": "Fluminense",             "away": "Bolívar",                  "home_score": 2, "away_score": 1},
    {"group": "Group C", "home": "Deportivo La Guaira",    "away": "Ind. Rivadavia",           "home_score": 2, "away_score": 4},
    {"group": "Group C", "home": "Fluminense",             "away": "Deportivo La Guaira",      "home_score": 3, "away_score": 1},
    {"group": "Group C", "home": "Bolívar",                "away": "Ind. Rivadavia",           "home_score": 1, "away_score": 3},
    # GROUP D
    {"group": "Group D", "home": "Barcelona S.C.",         "away": "Cruzeiro",                 "home_score": 0, "away_score": 1},
    {"group": "Group D", "home": "Universidad Católica",   "away": "Boca Juniors",             "home_score": 1, "away_score": 2},
    {"group": "Group D", "home": "Boca Juniors",           "away": "Barcelona S.C.",           "home_score": 3, "away_score": 0},
    {"group": "Group D", "home": "Cruzeiro",               "away": "Universidad Católica",     "home_score": 1, "away_score": 2},
    {"group": "Group D", "home": "Cruzeiro",               "away": "Boca Juniors",             "home_score": 1, "away_score": 0},
    {"group": "Group D", "home": "Barcelona S.C.",         "away": "Universidad Católica",     "home_score": 1, "away_score": 2},
    {"group": "Group D", "home": "Barcelona S.C.",         "away": "Boca Juniors",             "home_score": 1, "away_score": 0},
    {"group": "Group D", "home": "Universidad Católica",   "away": "Cruzeiro",                 "home_score": 0, "away_score": 0},
    {"group": "Group D", "home": "Boca Juniors",           "away": "Cruzeiro",                 "home_score": 1, "away_score": 1},
    {"group": "Group D", "home": "Universidad Católica",   "away": "Barcelona S.C.",           "home_score": 2, "away_score": 0},
    {"group": "Group D", "home": "Boca Juniors",           "away": "Universidad Católica",     "home_score": 0, "away_score": 1},
    {"group": "Group D", "home": "Cruzeiro",               "away": "Barcelona S.C.",           "home_score": 4, "away_score": 0},
    # GROUP E
    {"group": "Group E", "home": "Platense",               "away": "Corinthians",              "home_score": 0, "away_score": 2},
    {"group": "Group E", "home": "Independiente Santa Fe", "away": "Peñarol",                  "home_score": 1, "away_score": 1},
    {"group": "Group E", "home": "Corinthians",            "away": "Independiente Santa Fe",   "home_score": 2, "away_score": 0},
    {"group": "Group E", "home": "Peñarol",                "away": "Platense",                 "home_score": 1, "away_score": 2},
    {"group": "Group E", "home": "Platense",               "away": "Independiente Santa Fe",   "home_score": 2, "away_score": 1},
    {"group": "Group E", "home": "Corinthians",            "away": "Peñarol",                  "home_score": 2, "away_score": 0},
    {"group": "Group E", "home": "Independiente Santa Fe", "away": "Corinthians",              "home_score": 1, "away_score": 1},
    {"group": "Group E", "home": "Platense",               "away": "Peñarol",                  "home_score": 1, "away_score": 1},
    {"group": "Group E", "home": "Independiente Santa Fe", "away": "Platense",                 "home_score": 2, "away_score": 1},
    {"group": "Group E", "home": "Peñarol",                "away": "Corinthians",              "home_score": 1, "away_score": 1},
    {"group": "Group E", "home": "Peñarol",                "away": "Independiente Santa Fe",   "home_score": 0, "away_score": 1},
    {"group": "Group E", "home": "Corinthians",            "away": "Platense",                 "home_score": 0, "away_score": 2},
    # GROUP F
    {"group": "Group F", "home": "Junior FC",              "away": "Palmeiras",                "home_score": 1, "away_score": 1},
    {"group": "Group F", "home": "Sporting Cristal",       "away": "Cerro Porteño",            "home_score": 1, "away_score": 0},
    {"group": "Group F", "home": "Cerro Porteño",          "away": "Junior FC",                "home_score": 1, "away_score": 0},
    {"group": "Group F", "home": "Palmeiras",              "away": "Sporting Cristal",         "home_score": 2, "away_score": 1},
    {"group": "Group F", "home": "Sporting Cristal",       "away": "Junior FC",                "home_score": 2, "away_score": 0},
    {"group": "Group F", "home": "Cerro Porteño",          "away": "Palmeiras",                "home_score": 1, "away_score": 1},
    {"group": "Group F", "home": "Sporting Cristal",       "away": "Palmeiras",                "home_score": 0, "away_score": 2},
    {"group": "Group F", "home": "Junior FC",              "away": "Cerro Porteño",            "home_score": 0, "away_score": 1},
    {"group": "Group F", "home": "Palmeiras",              "away": "Cerro Porteño",            "home_score": 0, "away_score": 1},
    {"group": "Group F", "home": "Junior FC",              "away": "Sporting Cristal",         "home_score": 3, "away_score": 2},
    {"group": "Group F", "home": "Cerro Porteño",          "away": "Sporting Cristal",         "home_score": 2, "away_score": 0},
    {"group": "Group F", "home": "Palmeiras",              "away": "Junior FC",                "home_score": 4, "away_score": 1},
    # GROUP G
    {"group": "Group G", "home": "Always Ready",           "away": "LDU Quito",                "home_score": 0, "away_score": 1},
    {"group": "Group G", "home": "Mirassol",               "away": "Lanús",                    "home_score": 1, "away_score": 0},
    {"group": "Group G", "home": "LDU Quito",              "away": "Mirassol",                 "home_score": 2, "away_score": 0},
    {"group": "Group G", "home": "Lanús",                  "away": "Always Ready",             "home_score": 1, "away_score": 0},
    {"group": "Group G", "home": "Lanús",                  "away": "LDU Quito",                "home_score": 1, "away_score": 0},
    {"group": "Group G", "home": "Mirassol",               "away": "Always Ready",             "home_score": 2, "away_score": 0},
    {"group": "Group G", "home": "Always Ready",           "away": "Lanús",                    "home_score": 4, "away_score": 0},
    {"group": "Group G", "home": "Mirassol",               "away": "LDU Quito",                "home_score": 2, "away_score": 0},
    {"group": "Group G", "home": "Always Ready",           "away": "Mirassol",                 "home_score": 1, "away_score": 2},
    {"group": "Group G", "home": "LDU Quito",              "away": "Lanús",                    "home_score": 2, "away_score": 0},
    {"group": "Group G", "home": "LDU Quito",              "away": "Always Ready",             "home_score": 3, "away_score": 2},
    {"group": "Group G", "home": "Lanús",                  "away": "Mirassol",                 "home_score": 1, "away_score": 0},
    # GROUP H
    {"group": "Group H", "home": "Rosario Central",        "away": "Independiente del Valle",  "home_score": 0, "away_score": 0},
    {"group": "Group H", "home": "Universidad Central",    "away": "Libertad",                 "home_score": 3, "away_score": 1},
    {"group": "Group H", "home": "Libertad",               "away": "Rosario Central",          "home_score": 0, "away_score": 1},
    {"group": "Group H", "home": "Independiente del Valle","away": "Universidad Central",      "home_score": 3, "away_score": 1},
    {"group": "Group H", "home": "Libertad",               "away": "Independiente del Valle",  "home_score": 2, "away_score": 3},
    {"group": "Group H", "home": "Universidad Central",    "away": "Rosario Central",          "home_score": 0, "away_score": 3},
    {"group": "Group H", "home": "Rosario Central",        "away": "Libertad",                 "home_score": 1, "away_score": 0},
    {"group": "Group H", "home": "Universidad Central",    "away": "Independiente del Valle",  "home_score": 2, "away_score": 0},
    {"group": "Group H", "home": "Rosario Central",        "away": "Universidad Central",      "home_score": 4, "away_score": 0},
    {"group": "Group H", "home": "Independiente del Valle","away": "Libertad",                 "home_score": 4, "away_score": 1},
    {"group": "Group H", "home": "Independiente del Valle","away": "Rosario Central",          "home_score": 1, "away_score": 0},
    {"group": "Group H", "home": "Libertad",               "away": "Universidad Central",      "home_score": 0, "away_score": 1},
]

# --- DIXON-COLES ATTACK / DEFENSE RATINGS ---
@st.cache_data(ttl=3600)
def fit_ratings(group_name: str) -> dict:
    matches = [m for m in past_matches if m["group"] == group_name]
    teams   = [t["Team"] for t in teams_meta[group_name]]
    n       = len(teams)
    idx     = {t: i for i, t in enumerate(teams)}

    all_goals = [m["home_score"] for m in matches] + [m["away_score"] for m in matches]
    mu = max(np.mean(all_goals), 0.5)

    def neg_log_likelihood(params):
        attacks  = np.exp(params[:n])
        defenses = np.exp(params[n:2*n])
        home_adv = np.exp(params[2*n])
        attacks  = attacks  / attacks.mean()
        defenses = defenses / defenses.mean()
        nll = 0.0
        for m in matches:
            hi, ai = idx[m["home"]], idx[m["away"]]
            lam_h = attacks[hi] * defenses[ai] * home_adv * mu
            lam_a = attacks[ai] * defenses[hi] * mu
            nll -= (m["home_score"] * np.log(lam_h + 1e-9) - lam_h)
            nll -= (m["away_score"] * np.log(lam_a + 1e-9) - lam_a)
        return nll

    x0 = np.zeros(2 * n + 1)
    result = minimize(neg_log_likelihood, x0, method="L-BFGS-B")

    if result.success or result.fun < neg_log_likelihood(x0):
        params   = result.x
        attacks  = np.exp(params[:n]);  attacks  /= attacks.mean()
        defenses = np.exp(params[n:2*n]); defenses /= defenses.mean()
        home_adv = float(np.exp(params[2*n]))
    else:
        attacks  = np.ones(n)
        defenses = np.ones(n)
        home_adv = 1.15

    return {
        "attack":   {t: float(attacks[i])  for i, t in enumerate(teams)},
        "defense":  {t: float(defenses[i]) for i, t in enumerate(teams)},
        "home_adv": home_adv,
        "mu":       mu,
    }

def dixon_coles_xg(home: str, away: str, ratings: dict) -> tuple:
    a, d, ha, mu = ratings["attack"], ratings["defense"], ratings["home_adv"], ratings["mu"]
    xg_h = a.get(home, 1.0) * d.get(away, 1.0) * ha * mu
    xg_a = a.get(away, 1.0) * d.get(home, 1.0) * mu
    return round(max(0.3, min(xg_h, 5.0)), 2), round(max(0.3, min(xg_a, 5.0)), 2)

def xg_to_probabilities(xgh: float, xga: float, max_goals: int = 8) -> tuple:
    """Convert xG to match outcome probabilities (H, D, A)"""
    from scipy.stats import poisson
    home_win = draw = away_win = 0.0
    for h in range(max_goals + 1):
        for a in range(max_goals + 1):
            p = poisson.pmf(h, xgh) * poisson.pmf(a, xga)
            if h > a:    home_win += p
            elif h == a: draw += p
            else:        away_win += p
    total = home_win + draw + away_win
    return (
        round((home_win / total) * 100, 1),
        round((draw / total) * 100, 1),
        round((away_win / total) * 100, 1),
    )

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
            stats[home]["Played"] += 1;  stats[away]["Played"] += 1
            stats[home]["Goals Scored"]   += hg;  stats[home]["Goals Received"] += ag
            stats[away]["Goals Scored"]   += ag;  stats[away]["Goals Received"] += hg
            if hg > ag:
                stats[home]["Won"] += 1;  stats[home]["Points"] += 3;  stats[away]["Lost"] += 1
            elif ag > hg:
                stats[away]["Won"] += 1;  stats[away]["Points"] += 3;  stats[home]["Lost"] += 1
            else:
                stats[home]["Drawn"] += 1;  stats[away]["Drawn"] += 1
                stats[home]["Points"] += 1;  stats[away]["Points"] += 1
    for team in stats:
        stats[team]["Goal Difference"] = stats[team]["Goals Scored"] - stats[team]["Goals Received"]
        stats[team]["Team"] = team
    return list(stats.values())

def resolve_ties(teams_list, all_group_matches):
    def h2h_sort_key(t):
        return (t["h2h_pts"], t["h2h_gd"], t["h2h_gs"], t["overall_gd"], t["overall_gs"])

    points_groups: dict = {}
    for team in teams_list:
        points_groups.setdefault(team["Points"], []).append(team)

    final_sorted = []
    for p in sorted(points_groups.keys(), reverse=True):
        tied = points_groups[p]
        if len(tied) == 1:
            final_sorted.append(tied[0]); continue
        names = {t["Team"] for t in tied}
        h2h_matches = [m for m in all_group_matches if m["home"] in names and m["away"] in names]
        h2h_by_name = {s["Team"]: s for s in calculate_standings(tied, h2h_matches)}
        enriched = []
        for team in tied:
            h2h = h2h_by_name[team["Team"]]
            enriched.append({**team,
                "h2h_pts": h2h["Points"], "h2h_gd": h2h["Goal Difference"],
                "h2h_gs":  h2h["Goals Scored"],
                "overall_gd": team["Goal Difference"], "overall_gs": team["Goals Scored"]})
        enriched.sort(key=h2h_sort_key, reverse=True)
        final_sorted.extend(enriched)

    for i, t in enumerate(final_sorted):
        t["Position"] = i + 1
    return final_sorted

def get_sorted_standings(group_name):
    group_teams   = teams_meta[group_name]
    group_matches = [m for m in past_matches if m["group"] == group_name]
    raw = calculate_standings(group_teams, group_matches)
    raw.sort(key=lambda x: (x["Points"], x["Goal Difference"], x["Goals Scored"]), reverse=True)
    return resolve_ties(raw, group_matches)

# --- BUILD groups_data FROM PAST MATCHES ---
groups_data = {}
for group_name in teams_meta:
    groups_data[group_name] = get_sorted_standings(group_name)

# --- STANDINGS TABLES ---
group_items = list(groups_data.items())
for i in range(0, len(group_items), 2):
    c1, c2 = st.columns(2)
    for idx, col in enumerate([c1, c2]):
        if i + idx < len(group_items):
            g_name, g_data = group_items[i + idx]
            with col:
                st.subheader(g_name)
                display_df = create_group_df(g_data)
                df_display = display_df.copy()
                df_display['Team'] = df_display.apply(
                    lambda x: f'<div style="display: flex; align-items: center;"><img src="{x["Logo"]}" width="24" style="margin-right: 10px;"> {x["Team"]}</div>', 
                    axis=1
                )
                df_display = df_display.drop(columns=['Logo'])
                html_table = df_display.to_html(escape=False, index=False, justify='left')
                styled_html = f"""
<style>
.custom-table table {{ width: 100%; border-collapse: collapse; font-family: sans-serif; font-size: 14px; margin-bottom: 20px; }}
.custom-table th {{ border-bottom: 1px solid rgba(128, 128, 128, 0.2); padding: 10px 8px; text-align: left; font-weight: 600; color: inherit; }}
.custom-table td {{ border-bottom: 1px solid rgba(128, 128, 128, 0.2); padding: 8px; color: inherit; }}
</style>
<div class="custom-table">
{html_table}
</div>
"""
                st.markdown(styled_html, unsafe_allow_html=True)

st.divider()
st.header("🏆 Knockout Stage Simulator")

# Helper functions
def get_team_logo(team_name):
    return next((t["Logo"] for g in teams_meta for t in teams_meta[g] if t["Team"] == team_name), "")

def get_team_group(team_name):
    return next((g for g in teams_meta if any(t["Team"] == team_name for t in teams_meta[g])), "Group A")

# R16 Bracket
r16_bracket = {
    "A": ("Universidad Católica", "Estudiantes"),
    "H": ("Corinthians", "Rosario Central"),
    "E": ("Flamengo", "Cruzeiro"),
    "D": ("Independiente del Valle", "Deportes Tolima"),
    "B": ("LDU Quito", "Mirassol"),
    "G": ("Cerro Porteño", "Palmeiras"),
    "F": ("Coquimbo Unido", "Platense"),
    "C": ("Ind. Rivadavia", "Fluminense"),
}

qf_bracket = [
    ("A", "H"),  # 0: QF1
    ("E", "D"),  # 1: QF2
    ("B", "G"),  # 2: QF3
    ("F", "C"),  # 3: QF4
]

mc_iterations = st.number_input("Iterations", value=500, min_value=50, max_value=5000, key="r16_iterations")

# Form for predictions
with st.form("r16_form"):
    st.subheader("R16 Match Predictions")
    
    predictions = {}
    
    cols_layout = st.columns(2)
    col_idx = 0
    
    for tie_letter in ["A", "H", "E", "D", "B", "G", "F", "C"]:
        team1, team2 = r16_bracket[tie_letter]
        
        # Determine home/away for Leg 1 based on ranking
        rank1 = get_team_ranking(team1)
        rank2 = get_team_ranking(team2)
        
        if rank1 < rank2:
            leg1_home, leg1_away = team2, team1
        else:
            leg1_home, leg1_away = team1, team2
        
        leg1_home_logo = get_team_logo(leg1_home)
        leg1_away_logo = get_team_logo(leg1_away)
        
        # Get xG estimates and convert to probabilities
        group = get_team_group(leg1_home)
        ratings = fit_ratings(group)
        xgh, xga = dixon_coles_xg(leg1_home, leg1_away, ratings)
        ph, pd, pa = xg_to_probabilities(xgh, xga)
        
        with cols_layout[col_idx % 2]:
            st.markdown(f"**Tie {tie_letter}**")
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:8px;margin:4px 0;">'
                f'<img src="{leg1_home_logo}" width="20"><b>{leg1_home}</b> <span style="color:gray;">(H)</span></div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:8px;margin:4px 0;">'
                f'<img src="{leg1_away_logo}" width="20"><b>{leg1_away}</b> <span style="color:gray;">(A)</span></div>',
                unsafe_allow_html=True
            )
            
            c1, c2, c3 = st.columns(3)
            with c1:
                ph_input = st.number_input(f"H% ({tie_letter})", value=ph, min_value=0.0, max_value=100.0, 
                                   key=f"ph_{tie_letter}", step=1.0)
            with c2:
                pd_input = st.number_input(f"D% ({tie_letter})", value=pd, min_value=0.0, max_value=100.0, 
                                   key=f"pd_{tie_letter}", step=1.0)
            with c3:
                pa_input = st.number_input(f"A% ({tie_letter})", value=pa, min_value=0.0, max_value=100.0, 
                                   key=f"pa_{tie_letter}", step=1.0)
            
            predictions[tie_letter] = {
                "team1": team1, "team2": team2,
                "leg1_home": leg1_home, "leg1_away": leg1_away,
                "ph": ph_input, "pd": pd_input, "pa": pa_input,
                "xgh": xgh, "xga": xga
            }
            st.divider()
        
        col_idx += 1
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        run_simulation = st.form_submit_button("🎯 Simulate Tournament", type="primary", use_container_width=True)

# --- TOURNAMENT SIMULATION ---
if run_simulation:
    try:
        # Initialize counters for all 16 R16 teams
        all_teams = set()
        for _, (t1, t2) in r16_bracket.items():
            all_teams.add(t1)
            all_teams.add(t2)
        
        tournament_results = {team: {"QF": 0, "SF": 0, "Final": 0, "Champion": 0} for team in all_teams}
        
        for sim in range(int(mc_iterations)):
                # R16 simulation - determine QF winners via two-leg ties
                qf_winners = {}
            
                for tie_letter, (team1, team2) in r16_bracket.items():
                pred = predictions[tie_letter]
                leg1_home = pred["leg1_home"]
                leg1_away = pred["leg1_away"]
                leg2_home = leg1_away  # Opposite team hosts leg 2
                leg2_away = leg1_home
            
                # LEG 1
                h_score_l1 = int(np.random.poisson(pred["xgh"]))
                a_score_l1 = int(np.random.poisson(pred["xga"]))
            
                # LEG 2 - get xG for leg 2 matchup
                group = get_team_group(leg2_home)
                ratings2 = fit_ratings(group)
                xgh2, xga2 = dixon_coles_xg(leg2_home, leg2_away, ratings2)
            
                h_score_l2 = int(np.random.poisson(xgh2))
                a_score_l2 = int(np.random.poisson(xga2))
            
                # Aggregate score
                agg_home = h_score_l1 + h_score_l2
                agg_away = a_score_l1 + a_score_l2
            
                if agg_home > agg_away:
                    winner = leg1_home
                elif agg_away > agg_home:
                    winner = leg1_away
                else:
                    # Extra time on Leg 2 with full home advantage
                    # Use ratings from each team's group
                    group_h = get_team_group(leg2_home)
                    group_a = get_team_group(leg2_away)
                    ratings_et_h = fit_ratings(group_h)
                    ratings_et_a = fit_ratings(group_a)
                
                    att_h = ratings_et_h["attack"].get(leg2_home, 1.0)
                    att_a = ratings_et_a["attack"].get(leg2_away, 1.0)
                    def_h = ratings_et_h["defense"].get(leg2_home, 1.0)
                    def_a = ratings_et_a["defense"].get(leg2_away, 1.0)
                    home_adv = (ratings_et_h["home_adv"] + ratings_et_a["home_adv"]) / 2
                    mu = (ratings_et_h["mu"] + ratings_et_a["mu"]) / 2
                
                    xgh_et = att_h * def_a * home_adv * mu * 0.35
                    xga_et = att_a * def_h * mu * 0.35
                
                    et_h = int(np.random.poisson(xgh_et))
                    et_a = int(np.random.poisson(xga_et))
                
                    agg_home += et_h
                    agg_away += et_a
                
                    if agg_home > agg_away:
                        winner = leg1_home
                    elif agg_away > agg_home:
                        winner = leg1_away
                    else:
                        # Penalties - 50/50
                        winner = leg2_home if np.random.random() < 0.5 else leg2_away
            
                qf_winners[tie_letter] = winner
                tournament_results[winner]["QF"] += 1
        
            # QF simulation using bracket pairings
            qf_winners_list = [qf_winners[bracket[0]] for bracket in qf_bracket[0:1]] + \
                              [qf_winners[bracket[1]] for bracket in qf_bracket[0:1]] + \
                              [qf_winners[bracket[0]] for bracket in qf_bracket[1:2]] + \
                              [qf_winners[bracket[1]] for bracket in qf_bracket[1:2]] + \
                              [qf_winners[bracket[0]] for bracket in qf_bracket[2:3]] + \
                              [qf_winners[bracket[1]] for bracket in qf_bracket[2:3]] + \
                              [qf_winners[bracket[0]] for bracket in qf_bracket[3:4]] + \
                              [qf_winners[bracket[1]] for bracket in qf_bracket[3:4]]
        
            # Correct QF order
            qf_list = [
                qf_winners[qf_bracket[0][0]], qf_winners[qf_bracket[0][1]],
                qf_winners[qf_bracket[1][0]], qf_winners[qf_bracket[1][1]],
                qf_winners[qf_bracket[2][0]], qf_winners[qf_bracket[2][1]],
                qf_winners[qf_bracket[3][0]], qf_winners[qf_bracket[3][1]],
            ]
        
            sf_winners = {}
        
            # SF1: Winner of (A vs H) vs Winner of (E vs D)
            team1, team2 = qf_list[0], qf_list[2]
            rank1, rank2 = get_team_ranking(team1), get_team_ranking(team2)
            sf1_home = team2 if rank1 < rank2 else team1
            sf1_away = team1 if rank1 < rank2 else team2
        
            group_sf1_h = get_team_group(sf1_home)
            group_sf1_a = get_team_group(sf1_away)
            ratings_sf1_h = fit_ratings(group_sf1_h)
            ratings_sf1_a = fit_ratings(group_sf1_a)
        
            att_sf1_h = ratings_sf1_h["attack"].get(sf1_home, 1.0)
            att_sf1_a = ratings_sf1_a["attack"].get(sf1_away, 1.0)
            def_sf1_h = ratings_sf1_h["defense"].get(sf1_home, 1.0)
            def_sf1_a = ratings_sf1_a["defense"].get(sf1_away, 1.0)
            home_adv_sf1 = (ratings_sf1_h["home_adv"] + ratings_sf1_a["home_adv"]) / 2
            mu_sf1 = (ratings_sf1_h["mu"] + ratings_sf1_a["mu"]) / 2
        
            xgh_sf1 = att_sf1_h * def_sf1_a * home_adv_sf1 * mu_sf1
            xga_sf1 = att_sf1_a * def_sf1_h * mu_sf1
            xgh_sf1 = round(max(0.3, min(xgh_sf1, 5.0)), 2)
            xga_sf1 = round(max(0.3, min(xga_sf1, 5.0)), 2)
        
            h_score = int(np.random.poisson(xgh_sf1))
            a_score = int(np.random.poisson(xga_sf1))
            sf_winners["SF1"] = sf1_home if h_score > a_score else (sf1_away if a_score > h_score else (sf1_home if np.random.random() < 0.5 else sf1_away))
            tournament_results[sf_winners["SF1"]]["SF"] += 1
        
            # SF2: Winner of (B vs G) vs Winner of (F vs C)
            team1, team2 = qf_list[4], qf_list[6]
            rank1, rank2 = get_team_ranking(team1), get_team_ranking(team2)
            sf2_home = team2 if rank1 < rank2 else team1
            sf2_away = team1 if rank1 < rank2 else team2
        
            group_sf2_h = get_team_group(sf2_home)
            group_sf2_a = get_team_group(sf2_away)
            ratings_sf2_h = fit_ratings(group_sf2_h)
            ratings_sf2_a = fit_ratings(group_sf2_a)
        
            att_sf2_h = ratings_sf2_h["attack"].get(sf2_home, 1.0)
            att_sf2_a = ratings_sf2_a["attack"].get(sf2_away, 1.0)
            def_sf2_h = ratings_sf2_h["defense"].get(sf2_home, 1.0)
            def_sf2_a = ratings_sf2_a["defense"].get(sf2_away, 1.0)
            home_adv_sf2 = (ratings_sf2_h["home_adv"] + ratings_sf2_a["home_adv"]) / 2
            mu_sf2 = (ratings_sf2_h["mu"] + ratings_sf2_a["mu"]) / 2
        
            xgh_sf2 = att_sf2_h * def_sf2_a * home_adv_sf2 * mu_sf2
            xga_sf2 = att_sf2_a * def_sf2_h * mu_sf2
            xgh_sf2 = round(max(0.3, min(xgh_sf2, 5.0)), 2)
            xga_sf2 = round(max(0.3, min(xga_sf2, 5.0)), 2)
        
            h_score = int(np.random.poisson(xgh_sf2))
            a_score = int(np.random.poisson(xga_sf2))
            sf_winners["SF2"] = sf2_home if h_score > a_score else (sf2_away if a_score > h_score else (sf2_home if np.random.random() < 0.5 else sf2_away))
            tournament_results[sf_winners["SF2"]]["SF"] += 1
        
            # Final (neutral ground)
            finalist1, finalist2 = sf_winners["SF1"], sf_winners["SF2"]
            tournament_results[finalist1]["Final"] += 1
            tournament_results[finalist2]["Final"] += 1
        
            group_f1 = get_team_group(finalist1)
            group_f2 = get_team_group(finalist2)
            ratings_f1 = fit_ratings(group_f1)
            ratings_f2 = fit_ratings(group_f2)
        
            att_f1 = ratings_f1["attack"].get(finalist1, 1.0)
            att_f2 = ratings_f2["attack"].get(finalist2, 1.0)
            def_f1 = ratings_f1["defense"].get(finalist1, 1.0)
            def_f2 = ratings_f2["defense"].get(finalist2, 1.0)
            mu_f = (ratings_f1["mu"] + ratings_f2["mu"]) / 2
        
            xgh = att_f1 * def_f2 * 1.0 * mu_f
            xga = att_f2 * def_f1 * 1.0 * mu_f
            xgh = round(max(0.3, min(xgh, 5.0)), 2)
            xga = round(max(0.3, min(xga, 5.0)), 2)
        
            h_score = int(np.random.poisson(xgh))
            a_score = int(np.random.poisson(xga))
        
            if h_score > a_score:
                champion = finalist1
            elif a_score > h_score:
                champion = finalist2
            else:
                # Final ET (neutral ground - no home advantage)
                att_f1_et = ratings_f1["attack"].get(finalist1, 1.0)
                att_f2_et = ratings_f2["attack"].get(finalist2, 1.0)
                def_f1_et = ratings_f1["defense"].get(finalist1, 1.0)
                def_f2_et = ratings_f2["defense"].get(finalist2, 1.0)
            
                xgh_et = att_f1_et * def_f2_et * 1.0 * mu_f * 0.35
                xga_et = att_f2_et * def_f1_et * 1.0 * mu_f * 0.35
            
                et_h = int(np.random.poisson(xgh_et))
                et_a = int(np.random.poisson(xga_et))
            
                if et_h > et_a:
                    champion = finalist1
                elif et_a > et_h:
                    champion = finalist2
                else:
                    # Final penalties - 50/50
                    champion = finalist1 if np.random.random() < 0.5 else finalist2
        
            tournament_results[champion]["Champion"] += 1
    
            # Display results
            st.success("✅ Tournament Simulation Complete!")
            st.divider()
        
            # Create results summary table
            results_data = []
            for team in sorted(tournament_results.keys()):
                champion_pct = (tournament_results[team]['Champion'] / int(mc_iterations)) * 100
                results_data.append({
                    "Team": team,
                    "QF": f"{(tournament_results[team]['QF'] / int(mc_iterations)) * 100:.1f}%",
                    "SF": f"{(tournament_results[team]['SF'] / int(mc_iterations)) * 100:.1f}%",
                    "Final": f"{(tournament_results[team]['Final'] / int(mc_iterations)) * 100:.1f}%",
                    "Champion": f"{champion_pct:.1f}%",
                    "_champion_sort": champion_pct,
                })
        
            if results_data:
                results_df = pd.DataFrame(results_data).sort_values("_champion_sort", ascending=False).drop(columns=["_champion_sort"])
            
                st.subheader("🏆 Tournament Probabilities")
                st.dataframe(results_df, use_container_width=True, hide_index=True)
            else:
                st.error("No results data generated")
    
    except Exception as e:
        st.error(f"Simulation error: {str(e)}")
        import traceback
        st.error(traceback.format_exc())
