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

# --- PAST MATCH RESULTS (All Group Stage Matchdays) ---
past_matches = [
    # GROUP A - all 12 matches
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
    # GROUP B - all 12 matches
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
    # GROUP C - all 12 matches
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
    # GROUP D - all 12 matches
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
    # GROUP E - all 12 matches
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
    # GROUP F - all 12 matches
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
    # GROUP G - all 12 matches
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
    # GROUP H - all 12 matches
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

# Helper function to get team logo
def get_team_logo(team_name):
    return next((t["Logo"] for g in teams_meta for t in teams_meta[g] if t["Team"] == team_name), "")

# Get group for team to compute ratings
def get_team_group(team_name):
    return next((g for g in teams_meta if any(t["Team"] == team_name for t in teams_meta[g])), "Group A")

mc_iterations = st.number_input("Iterations", value=500, min_value=50, max_value=5000, key="r16_iterations")

# R16 Bracket setup
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

qf_bracket = {
    "1": ("A", "H"),
    "2": ("E", "D"),
    "3": ("B", "G"),
    "4": ("F", "C"),
}

sf_bracket = {
    "SF1": ("1", "2"),
    "SF2": ("3", "4"),
}

# Simulation settings form
with st.form("r16_form"):
    st.subheader("R16 Match Predictions")
    
    predictions = {}
    
    cols_layout = st.columns(2)
    col_idx = 0
    
    for tie_letter in ["A", "H", "E", "D", "B", "G", "F", "C"]:
        home, away = r16_bracket[tie_letter]
        h_logo = get_team_logo(home)
        a_logo = get_team_logo(away)
        
        # Get ratings
        group = get_team_group(home)
        ratings = fit_ratings(group)
        xgh, xga = dixon_coles_xg(home, away, ratings)
        
        with cols_layout[col_idx % 2]:
            st.markdown(f"**Tie {tie_letter}**")
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:12px;margin:4px 0;">'
                f'<img src="{h_logo}" width="20"><b>{home}</b></div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:12px;margin:4px 0;">'
                f'<img src="{a_logo}" width="20"><b>{away}</b></div>',
                unsafe_allow_html=True
            )
            
            c1, c2, c3 = st.columns(3)
            with c1:
                ph = st.number_input(f"H% ({tie_letter})", value=50.0, min_value=0.0, max_value=100.0, key=f"ph_{tie_letter}")
            with c2:
                pd = st.number_input(f"D% ({tie_letter})", value=25.0, min_value=0.0, max_value=100.0, key=f"pd_{tie_letter}")
            with c3:
                pa = st.number_input(f"A% ({tie_letter})", value=25.0, min_value=0.0, max_value=100.0, key=f"pa_{tie_letter}")
            
            predictions[tie_letter] = {
                "home": home, "away": away,
                "ph": ph, "pd": pd, "pa": pa,
                "xgh": xgh, "xga": xga
            }
            st.divider()
        
        col_idx += 1
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        run_simulation = st.form_submit_button("🎯 Simulate Tournament", type="primary", use_container_width=True)

# --- TOURNAMENT SIMULATION ---
if run_simulation:
    # Initialize counters
    tournament_results = {team: {"QF": 0, "SF": 0, "Final": 0, "Champion": 0} for tie_teams in r16_bracket.values() for team in tie_teams}
    
    for sim in range(int(mc_iterations)):
        # R16 simulation - determine QF winners
        qf_winners = {}
        
        for tie_letter, (home, away) in r16_bracket.items():
            pred = predictions[tie_letter]
            
            # Simulate match
            h_score = int(np.random.poisson(pred["xgh"]))
            a_score = int(np.random.poisson(pred["xga"]))
            
            # Determine winner
            if h_score > a_score:
                winner = home
            elif a_score > h_score:
                winner = away
            else:
                # 50/50 in case of tie (simplified - no ET/penalties simulation)
                winner = home if np.random.random() < 0.5 else away
            
            qf_winners[tie_letter] = winner
            tournament_results[winner]["QF"] += 1
        
        # QF simulation - determine SF winners
        sf_winners = {}
        
        for qf_id, (tie1, tie2) in qf_bracket.items():
            team1, team2 = qf_winners[tie1], qf_winners[tie2]
            
            # Get ratings for simulation (use team1's group)
            group = get_team_group(team1)
            ratings = fit_ratings(group)
            xgh, xga = dixon_coles_xg(team1, team2, ratings)
            
            # Simulate QF match
            h_score = int(np.random.poisson(xgh))
            a_score = int(np.random.poisson(xga))
            
            winner = team1 if h_score > a_score else (team2 if a_score > h_score else (team1 if np.random.random() < 0.5 else team2))
            
            sf_winners[qf_id] = winner
            tournament_results[winner]["SF"] += 1
        
        # SF simulation - determine finalists
        finalists = []
        
        for sf_id in ["SF1", "SF2"]:
            team = sf_winners[sf_id]
            finalists.append(team)
            tournament_results[team]["Final"] += 1
        
        # Final simulation
        team1, team2 = finalists[0], finalists[1]
        group = get_team_group(team1)
        ratings = fit_ratings(group)
        xgh, xga = dixon_coles_xg(team1, team2, ratings)
        
        h_score = int(np.random.poisson(xgh))
        a_score = int(np.random.poisson(xga))
        
        champion = team1 if h_score > a_score else (team2 if a_score > h_score else (team1 if np.random.random() < 0.5 else team2))
        tournament_results[champion]["Champion"] += 1
    
    # Display results
    st.success("✅ Tournament Simulation Complete!")
    st.divider()
    
    # Create results summary table
    results_data = []
    for team in sorted(tournament_results.keys()):
        results_data.append({
            "Team": team,
            "QF": f"{(tournament_results[team]['QF'] / int(mc_iterations)) * 100:.1f}%",
            "SF": f"{(tournament_results[team]['SF'] / int(mc_iterations)) * 100:.1f}%",
            "Final": f"{(tournament_results[team]['Final'] / int(mc_iterations)) * 100:.1f}%",
            "Champion": f"{(tournament_results[team]['Champion'] / int(mc_iterations)) * 100:.1f}%",
        })
    
    results_df = pd.DataFrame(results_data).sort_values("Champion", key=lambda x: x.str.rstrip('%').astype(float), ascending=False)
    
    st.subheader("🏆 Tournament Probabilities")
    st.dataframe(results_df, use_container_width=True, hide_index=True)
