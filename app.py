import streamlit as st
import pandas as pd
import numpy as np

# Configure the page layout
st.set_page_config(page_title="Copa Libertadores 2026 Simulator", layout="wide")
st.title("🏆 Copa Libertadores 2026 Simulator")

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

# --- DATA ---
groups_data = {
    "Group A": [
        {"Position": 1, "Logo": get_logo_url("flamengo.png"), "Team": "Flamengo", "Played": 5, "Won": 4, "Lost": 0, "Drawn": 1, "Goals Scored": 11, "Goals Received": 2, "Goal Difference": 9, "Points": 13},
        {"Position": 2, "Logo": get_logo_url("dim.png"), "Team": "Independiente Medellín", "Played": 5, "Won": 2, "Lost": 2, "Drawn": 1, "Goals Scored": 6, "Goals Received": 10, "Goal Difference": -4, "Points": 7},
        {"Position": 3, "Logo": get_logo_url("estudiantes.png"), "Team": "Estudiantes de La Plata", "Played": 5, "Won": 1, "Lost": 1, "Drawn": 3, "Goals Scored": 5, "Goals Received": 5, "Goal Difference": 0, "Points": 6},
        {"Position": 4, "Logo": get_logo_url("cusco.png"), "Team": "Cusco FC", "Played": 5, "Won": 0, "Lost": 4, "Drawn": 1, "Goals Scored": 4, "Goals Received": 9, "Goal Difference": -5, "Points": 1}
    ],
    "Group B": [
        {"Position": 1, "Logo": get_logo_url("coquimbo.png"), "Team": "Coquimbo Unido", "Played": 5, "Won": 3, "Lost": 1, "Drawn": 1, "Goals Scored": 8, "Goals Received": 5, "Goal Difference": 3, "Points": 10},
        {"Position": 2, "Logo": get_logo_url("tolima.png"), "Team": "Deportes Tolima", "Played": 5, "Won": 2, "Lost": 2, "Drawn": 1, "Goals Scored": 7, "Goals Received": 6, "Goal Difference": 1, "Points": 7},
        {"Position": 3, "Logo": get_logo_url("universitario.png"), "Team": "Universitario", "Played": 5, "Won": 1, "Lost": 2, "Drawn": 2, "Goals Scored": 5, "Goals Received": 6, "Goal Difference": -1, "Points": 5},
        {"Position": 4, "Logo": get_logo_url("nacional.png"), "Team": "Nacional de Football", "Played": 5, "Won": 1, "Lost": 2, "Drawn": 2, "Goals Scored": 6, "Goals Received": 9, "Goal Difference": -3, "Points": 5}
    ],
    "Group C": [
        {"Position": 1, "Logo": get_logo_url("rivadavia.png"), "Team": "Ind. Rivadavia", "Played": 5, "Won": 4, "Lost": 0, "Drawn": 1, "Goals Scored": 12, "Goals Received": 5, "Goal Difference": 7, "Points": 13},
        {"Position": 2, "Logo": get_logo_url("bolivar.png"), "Team": "Bolívar", "Played": 5, "Won": 1, "Lost": 2, "Drawn": 2, "Goals Scored": 5, "Goals Received": 5, "Goal Difference": 0, "Points": 5},
        {"Position": 3, "Logo": get_logo_url("fluminense.png"), "Team": "Fluminense FC", "Played": 5, "Won": 1, "Lost": 2, "Drawn": 2, "Goals Scored": 4, "Goals Received": 6, "Goal Difference": -2, "Points": 5},
        {"Position": 4, "Logo": get_logo_url("laguaira.png"), "Team": "Deportivo La Guaira", "Played": 5, "Won": 0, "Lost": 2, "Drawn": 3, "Goals Scored": 5, "Goals Received": 10, "Goal Difference": -5, "Points": 3}
    ],
    "Group D": [
        {"Position": 1, "Logo": get_logo_url("uc.png"), "Team": "Universidad Católica", "Played": 5, "Won": 3, "Lost": 1, "Drawn": 1, "Goals Scored": 7, "Goals Received": 4, "Goal Difference": 3, "Points": 10},
        {"Position": 2, "Logo": get_logo_url("cruzeiro.png"), "Team": "Cruzeiro", "Played": 5, "Won": 2, "Lost": 1, "Drawn": 2, "Goals Scored": 4, "Goals Received": 3, "Goal Difference": 1, "Points": 8},
        {"Position": 3, "Logo": get_logo_url("boca.png"), "Team": "Boca Juniors", "Played": 5, "Won": 2, "Lost": 2, "Drawn": 1, "Goals Scored": 6, "Goals Received": 4, "Goal Difference": 2, "Points": 7},
        {"Position": 4, "Logo": get_logo_url("bsc.png"), "Team": "Barcelona S.C.", "Played": 5, "Won": 1, "Lost": 4, "Drawn": 0, "Goals Scored": 2, "Goals Received": 8, "Goal Difference": -6, "Points": 3}
    ],
    "Group E": [
        {"Position": 1, "Logo": get_logo_url("corinthians.png"), "Team": "Corinthians", "Played": 5, "Won": 3, "Lost": 0, "Drawn": 2, "Goals Scored": 8, "Goals Received": 2, "Goal Difference": 6, "Points": 11},
        {"Position": 2, "Logo": get_logo_url("platense.png"), "Team": "Platense", "Played": 5, "Won": 2, "Lost": 2, "Drawn": 1, "Goals Scored": 6, "Goals Received": 7, "Goal Difference": -1, "Points": 7},
        {"Position": 3, "Logo": get_logo_url("santafe.png"), "Team": "Independiente Santa Fe", "Played": 5, "Won": 1, "Lost": 2, "Drawn": 2, "Goals Scored": 5, "Goals Received": 7, "Goal Difference": -2, "Points": 5},
        {"Position": 4, "Logo": get_logo_url("penarol.png"), "Team": "Peñarol", "Played": 5, "Won": 0, "Lost": 2, "Drawn": 3, "Goals Scored": 4, "Goals Received": 7, "Goal Difference": -3, "Points": 3}
    ],
    "Group F": [
        {"Position": 1, "Logo": get_logo_url("cerroporteno.png"), "Team": "Cerro Porteño", "Played": 5, "Won": 3, "Lost": 1, "Drawn": 1, "Goals Scored": 4, "Goals Received": 2, "Goal Difference": 2, "Points": 10},
        {"Position": 2, "Logo": get_logo_url("palmeiras.png"), "Team": "Palmeiras", "Played": 5, "Won": 2, "Lost": 1, "Drawn": 2, "Goals Scored": 6, "Goals Received": 4, "Goal Difference": 2, "Points": 8},
        {"Position": 3, "Logo": get_logo_url("cristal.png"), "Team": "Sporting Cristal", "Played": 5, "Won": 2, "Lost": 3, "Drawn": 0, "Goals Scored": 6, "Goals Received": 7, "Goal Difference": -1, "Points": 6},
        {"Position": 4, "Logo": get_logo_url("junior.png"), "Team": "Junior FC", "Played": 5, "Won": 1, "Lost": 3, "Drawn": 1, "Goals Scored": 4, "Goals Received": 7, "Goal Difference": -3, "Points": 4}
    ],
    "Group G": [
        {"Position": 1, "Logo": get_logo_url("mirassol.png"), "Team": "Mirassol", "Played": 5, "Won": 4, "Lost": 1, "Drawn": 0, "Goals Scored": 7, "Goals Received": 3, "Goal Difference": 4, "Points": 12},
        {"Position": 2, "Logo": get_logo_url("ldu.png"), "Team": "LDU Quito", "Played": 5, "Won": 3, "Lost": 2, "Drawn": 0, "Goals Scored": 5, "Goals Received": 3, "Goal Difference": 2, "Points": 9},
        {"Position": 3, "Logo": get_logo_url("lanus.png"), "Team": "Lanús", "Played": 5, "Won": 2, "Lost": 3, "Drawn": 0, "Goals Scored": 2, "Goals Received": 7, "Goal Difference": -5, "Points": 6},
        {"Position": 4, "Logo": get_logo_url("alwaysready.png"), "Team": "Always Ready", "Played": 5, "Won": 1, "Lost": 4, "Drawn": 0, "Goals Scored": 5, "Goals Received": 6, "Goal Difference": -1, "Points": 3}
    ],
    "Group H": [
        {"Position": 1, "Logo": get_logo_url("rosariocentral.png"), "Team": "Rosario Central", "Played": 5, "Won": 4, "Lost": 0, "Drawn": 1, "Goals Scored": 9, "Goals Received": 0, "Goal Difference": 9, "Points": 13},
        {"Position": 2, "Logo": get_logo_url("idv.png"), "Team": "Independiente del Valle", "Played": 5, "Won": 3, "Lost": 1, "Drawn": 1, "Goals Scored": 10, "Goals Received": 6, "Goal Difference": 4, "Points": 10},
        {"Position": 3, "Logo": get_logo_url("universidadcentral.png"), "Team": "Universidad Central", "Played": 5, "Won": 2, "Lost": 3, "Drawn": 0, "Goals Scored": 6, "Goals Received": 11, "Goal Difference": -5, "Points": 6},
        {"Position": 4, "Logo": get_logo_url("libertad.png"), "Team": "Libertad", "Played": 5, "Won": 0, "Lost": 5, "Drawn": 0, "Goals Scored": 4, "Goals Received": 12, "Goal Difference": -8, "Points": 0}
    ]
}

# --- RENDER TABLES ---
group_items = list(groups_data.items())
for i in range(0, len(group_items), 2):
    c1, c2 = st.columns(2)
    for idx, col in enumerate([c1, c2]):
        if i + idx < len(group_items):
            g_name, g_data = group_items[i + idx]
            with col:
                st.subheader(g_name)
                st.data_editor(create_group_df(g_data), column_config={"Logo": st.column_config.ImageColumn("Logo", help="Team Logo"), "Pos": st.column_config.NumberColumn("Pos", format="%d")}, hide_index=True, use_container_width=True, disabled=True)

st.divider()

# --- HARDCODED ODDS (Update these percentages from Polymarket) ---
HARDCODED_ODDS = {
    "Flamengo vs Cusco FC": {"ph": 85.0, "pa": 5.0}, # Placeholder
    "Estudiantes de La Plata vs Independiente Medellín": {"ph": 45.0, "pa": 30.0},
    "Nacional de Football vs Coquimbo Unido": {"ph": 40.0, "pa": 40.0},
    "Universitario vs Deportes Tolima": {"ph": 40.0, "pa": 40.0},
    "Bolívar vs Ind. Rivadavia": {"ph": 50.0, "pa": 25.0},
    "Fluminense FC vs Deportivo La Guaira": {"ph": 70.0, "pa": 10.0},
    "Boca Juniors vs Universidad Católica": {"ph": 45.0, "pa": 30.0},
    "Cruzeiro vs Barcelona S.C.": {"ph": 60.0, "pa": 20.0},
    "Peñarol vs Independiente Santa Fe": {"ph": 40.0, "pa": 35.0},
    "Corinthians vs Platense": {"ph": 65.0, "pa": 15.0},
    "Cerro Porteño vs Sporting Cristal": {"ph": 50.0, "pa": 25.0},
    "Palmeiras vs Junior FC": {"ph": 70.0, "pa": 10.0},
    "Lanús vs Mirassol": {"ph": 56.0, "pa": 18.0}, # Your provided example
    "LDU Quito vs Always Ready": {"ph": 75.0, "pa": 10.0},
    "Independiente del Valle vs Rosario Central": {"ph": 45.0, "pa": 35.0},
    "Libertad vs Universidad Central": {"ph": 55.0, "pa": 20.0}
}

# --- SIMULATOR BACKEND ---
def get_match_defaults(home_team, away_team, group_data):
    h_s = next(t for t in group_data if t["Team"] == home_team)
    a_s = next(t for t in group_data if t["Team"] == away_team)
    h_xg = ((h_s["Goals Scored"] / max(1, h_s["Played"])) + (a_s["Goals Received"] / max(1, a_s["Played"]))) / 2 + 0.2
    a_xg = ((a_s["Goals Scored"] / max(1, a_s["Played"])) + (h_s["Goals Received"] / max(1, h_s["Played"]))) / 2
    
    match_key = f"{home_team} vs {away_team}"
    if match_key in HARDCODED_ODDS:
        return {"ph": HARDCODED_ODDS[match_key]["ph"], "pa": HARDCODED_ODDS[match_key]["pa"], "xgh": float(h_xg), "xga": float(a_xg)}
    return {"ph": 50.0, "pa": 30.0, "xgh": float(h_xg), "xga": float(a_xg)}

def calculate_standings(group_teams, all_group_matches):
    stats = {t["Team"]: {"Played": 0, "Won": 0, "Lost": 0, "Drawn": 0, "Goals Scored": 0, "Goals Received": 0, "Points": 0, "Logo": t["Logo"]} for t in group_teams}
    for m in all_group_matches:
        home, away, hg, ag = m["home"], m["away"], m["home_score"], m["away_score"]
        if home in stats and away in stats:
            stats[home]["Played"] += 1; stats[away]["Played"] += 1
            stats[home]["Goals Scored"] += hg; stats[home]["Goals Received"] += ag
            stats[away]["Goals Scored"] += ag; stats[away]["Goals Received"] += hg
            if hg > ag: stats[home]["Won"] += 1; stats[home]["Points"] += 3; stats[away]["Lost"] += 1
            elif ag > hg: stats[away]["Won"] += 1; stats[away]["Points"] += 3; stats[home]["Lost"] += 1
            else: stats[home]["Drawn"] += 1; stats[away]["Drawn"] += 1; stats[home]["Points"] += 1; stats[away]["Points"] += 1
    for team in stats:
        stats[team]["Goal Difference"] = stats[team]["Goals Scored"] - stats[team]["Goals Received"]
        stats[team]["Team"] = team
    return list(stats.values())

def resolve_ties(teams_list, all_group_matches):
    points_groups = {}
    for team in teams_list:
        p = team["Points"]
        if p not in points_groups: points_groups[p] = []
        points_groups[p].append(team)
    final_sorted_group = []
    for p in sorted(points_groups.keys(), reverse=True):
        tied = points_groups[p]
        if len(tied) == 1: final_sorted_group.append(tied[0]); continue
        names = [t["Team"] for t in tied]
        h2h = [m for m in all_group_matches if m["home"] in names and m["away"] in names]
        stats = calculate_standings(tied, h2h)
        for s in stats:
            orig = next(t for t in tied if t["Team"] == s["Team"])
            s["Total GD"] = orig["Goal Difference"]; s["Total GS"] = orig["Goals Scored"]; s["Original Data"] = orig
        stats.sort(key=lambda x: (x["Points"], x["Goal Difference"], x["Goals Scored"], x["Original Data"]["Points"], x["Total GD"], x["Total GS"]), reverse=True)
        for s in stats: final_sorted_group.append(s["Original Data"])
    for i, t in enumerate(final_sorted_group): t["Position"] = i + 1
    return final_sorted_group

def simulate_match_randomly(ph, pt, pa, xgh, xga):
    p = [ph/100, pt/100, pa/100]
    outcome = np.random.choice(['H', 'D', 'A'], p=p)
    for _ in range(100):
        hg, ag = np.random.poisson(xgh), np.random.poisson(xga)
        if (outcome == 'H' and hg > ag) or (outcome == 'D' and hg == ag) or (outcome == 'A' and hg < ag): return hg, ag
    return (1, 0) if outcome == 'H' else (0, 0) if outcome == 'D' else (0, 1)

# --- UI ---
st.header("🎲 Matchday 6 Monte Carlo Simulator")
mc_iterations = st.number_input("Iterations", value=1000)
predictions = {}
matchday_6_fixtures = {
    "Group A": [("Flamengo", "Cusco FC"), ("Estudiantes de La Plata", "Independiente Medellín")],
    "Group B": [("Nacional de Football", "Coquimbo Unido"), ("Universitario", "Deportes Tolima")],
    "Group C": [("Bolívar", "Ind. Rivadavia"), ("Fluminense FC", "Deportivo La Guaira")],
    "Group D": [("Boca Juniors", "Universidad Católica"), ("Cruzeiro", "Barcelona S.C.")],
    "Group E": [("Peñarol", "Independiente Santa Fe"), ("Corinthians", "Platense")],
    "Group F": [("Cerro Porteño", "Sporting Cristal"), ("Palmeiras", "Junior FC")],
    "Group G": [("Lanús", "Mirassol"), ("LDU Quito", "Always Ready")],
    "Group H": [("Independiente del Valle", "Rosario Central"), ("Libertad", "Universidad Central")]
}
past_matches = [{"group": "Group A", "home": "Flamengo", "away": "Estudiantes de La Plata", "home_score": 1, "away_score": 0}]

with st.form("mc_form"):
    for group_name, fixtures in matchday_6_fixtures.items():
        st.markdown(f"#### {group_name}")
        group_preds = []
        match_cols = st.columns(2)
        for i, (home, away) in enumerate(fixtures):
            defaults = get_match_defaults(home, away, groups_data[group_name])
            home_logo = next(t["Logo"] for t in groups_data[group_name] if t["Team"] == home)
            away_logo = next(t["Logo"] for t in groups_data[group_name] if t["Team"] == away)
            with match_cols[i]:
                c = st.columns([3, 1, 1, 1, 1, 3])
                with c[0]: st.markdown(f"<div style='display: flex; align-items: center; justify-content: flex-end; margin-top: 28px;'><img src='{home_logo}' width='24' height='24' style='margin-right: 8px;'><b style='font-size:0.85em'>{home}</b></div>", unsafe_allow_html=True)
                with c[1]: ph = st.number_input("H%", key=f"{group_name}_{i}_ph", value=defaults["ph"])
                with c[2]: pa = st.number_input("A%", key=f"{group_name}_{i}_pa", value=defaults["pa"])
                with c[3]: xgh = st.number_input("HxG", key=f"{group_name}_{i}_xgh", value=defaults["xgh"])
                with c[4]: xga = st.number_input("AxG", key=f"{group_name}_{i}_xga", value=defaults["xga"])
                with c[5]: st.markdown(f"<div style='display: flex; align-items: center; justify-content: flex-start; margin-top: 28px;'><img src='{away_logo}' width='24' height='24' style='margin-right: 8px;'><b style='font-size:0.85em'>{away}</b></div>", unsafe_allow_html=True)
                group_preds.append({"group": group_name, "home": home, "away": away, "ph": ph, "pt": max(0, 100-ph-pa), "pa": pa, "xgh": xgh, "xga": xga})
        predictions[group_name] = group_preds
    run_mc = st.form_submit_button("Run Analysis", type="primary")

if run_mc:
    mc_results = {g: {t["Team"]: {1:0, 2:0, 3:0, 4:0} for t in groups_data[g]} for g in groups_data}
    for _ in range(int(mc_iterations)):
        for g_name in groups_data.keys():
            sim_m6 = [{"home": m["home"], "away": m["away"], "home_score": hg, "away_score": ag} for m in predictions[g_name] for hg, ag in [simulate_match_randomly(m["ph"], m["pt"], m["pa"], m["xgh"], m["xga"])]]
            sorted_s = resolve_ties(calculate_standings(groups_data[g_name], [m for m in past_matches if m["group"] == g_name] + sim_m6), sim_m6)
            for pos, team in enumerate(sorted_s): mc_results[g_name][team["Team"]][pos + 1] += 1
    for g_name in groups_data.keys():
        st.subheader(f"{g_name} Matrix")
        df_res = pd.DataFrame([{"Team": t, **{f"{p}º": f"{(c/mc_iterations)*100:.1f}%" for p, c in pos.items()}} for t, pos in mc_results[g_name].items()])
        st.dataframe(df_res, hide_index=True, use_container_width=True)
