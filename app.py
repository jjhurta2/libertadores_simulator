import streamlit as st
import pandas as pd
import numpy as np

# Configure the page layout
st.set_page_config(page_title="Copa Libertadores 2026 Simulator", layout="wide")
st.title("🏆 Copa Libertadores 2026 Simulator")
st.markdown("Current group stage standings across all 8 groups.")

def get_logo_url(filename):
    return f"https://github.com/jjhurta2/libertadores_simulator/blob/main/{filename}?raw=true"

def create_group_df(data):
    df = pd.DataFrame(data)
    cols = ["Position", "Logo", "Team", "Played", "Won", "Lost", "Drawn", "Goals Scored", "Goals Received", "Goal Difference", "Points"]
    return df[cols]

# Live 2026 Copa Libertadores Data
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

# Render current standings
for group_name, data in groups_data.items():
    st.subheader(group_name)
    df = create_group_df(data)
    st.dataframe(df, column_config={"Logo": st.column_config.ImageColumn("Logo", help="Team Logo"), "Position": st.column_config.NumberColumn("Pos", format="%d")}, hide_index=True, use_container_width=True)

st.divider()

# --- HISTORICAL DATA (Matchdays 1-5) ---
past_matches = [
    {"group": "Group A", "home": "Flamengo", "away": "Estudiantes de La Plata", "home_score": 1, "away_score": 0},
    {"group": "Group A", "home": "Cusco FC", "away": "Independiente Medellín", "home_score": 2, "away_score": 3},
]

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

# --- TIE-BREAKER LOGIC ---
def calculate_standings(group_teams, all_group_matches):
    stats = {team["Team"]: {"Played": 0, "Won": 0, "Lost": 0, "Drawn": 0, "Goals Scored": 0, "Goals Received": 0, "Points": 0, "Logo": team["Logo"]} for team in group_teams}
    for match in all_group_matches:
        home, away, hg, ag = match["home"], match["away"], match["home_score"], match["away_score"]
        if home in stats and away in stats:
            stats[home]["Played"] += 1
            stats[away]["Played"] += 1
            stats[home]["Goals Scored"] += hg
            stats[home]["Goals Received"] += ag
            stats[away]["Goals Scored"] += ag
            stats[away]["Goals Received"] += hg
            if hg > ag:
                stats[home]["Won"] += 1; stats[home]["Points"] += 3; stats[away]["Lost"] += 1
            elif ag > hg:
                stats[away]["Won"] += 1; stats[away]["Points"] += 3; stats[home]["Lost"] += 1
            else:
                stats[home]["Drawn"] += 1; stats[away]["Drawn"] += 1; stats[home]["Points"] += 1; stats[away]["Points"] += 1
    for team in stats:
        stats[team]["Goal Difference"] = stats[team]["Goals Scored"] - stats[team]["Goals Received"]
        stats[team]["Team"] = team
    return list(stats.values())

def resolve_ties(teams_list, all_group_matches):
    points_groups = {}
    for team in teams_list:
        points = team["Points"]
        if points not in points_groups: points_groups[points] = []
        points_groups[points].append(team)
    final_sorted_group = []
    for points in sorted(points_groups.keys(), reverse=True):
        tied_teams = points_groups[points]
        if len(tied_teams) == 1:
            final_sorted_group.append(tied_teams[0])
            continue
        tied_team_names = [t["Team"] for t in tied_teams]
        h2h_matches = [m for m in all_group_matches if m["home"] in tied_team_names and m["away"] in tied_team_names]
        h2h_stats = calculate_standings(tied_teams, h2h_matches)
        for ht in h2h_stats:
            orig = next(t for t in tied_teams if t["Team"] == ht["Team"])
            ht["Total Goal Difference"] = orig["Goal Difference"]
            ht["Total Goals Scored"] = orig["Goals Scored"]
            ht["Original Data"] = orig 
        h2h_stats.sort(key=lambda x: (x["Points"], x["Goal Difference"], x["Goals Scored"], x["Original Data"]["Points"], x["Total Goal Difference"], x["Total Goals Scored"]), reverse=True)
        for sorted_team in h2h_stats:
            final_sorted_group.append(sorted_team["Original Data"])
    for i, team in enumerate(final_sorted_group):
        team["Position"] = i + 1
    return final_sorted_group

# --- SIMULATOR SECTION ---
st.header("🔮 Matchday 6 Simulator")
st.markdown("Enter the scores for the final matches. The tables will recalculate using official H2H tie-breaker rules.")

predictions = {}

with st.form("simulator_form"):
    for group_name, fixtures in matchday_6_fixtures.items():
        st.subheader(group_name)
        group_preds = []
        
        for i, (home_team, away_team) in enumerate(fixtures):
            # Row 1: Scores
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 3])
            with col1: st.markdown(f"<p style='text-align: right; margin-top: 10px;'><b>{home_team}</b></p>", unsafe_allow_html=True)
            with col2: h_score = st.number_input("Home Score", key=f"{group_name}_m{i}_h", min_value=0, value=0, label_visibility="collapsed")
            with col3: st.markdown("<p style='text-align: center; margin-top: 10px;'>vs</p>", unsafe_allow_html=True)
            with col4: a_score = st.number_input("Away Score", key=f"{group_name}_m{i}_a", min_value=0, value=0, label_visibility="collapsed")
            with col5: st.markdown(f"<p style='margin-top: 10px;'><b>{away_team}</b></p>", unsafe_allow_html=True)
                
            # Row 2: Analytics
            st.markdown("<p style='font-size: 0.85em; color: gray; margin-bottom: -15px;'>Predictive Metrics (For Monte Carlo)</p>", unsafe_allow_html=True)
            p_col1, p_col2, p_col3, p_col4, p_col5 = st.columns(5)
            with p_col1: ph = st.number_input("Home Win %", key=f"{group_name}_m{i}_ph", min_value=0.0, max_value=100.0, value=50.0, step=1.0, format="%.1f")
            with p_col2: pt = st.number_input("Tie %", key=f"{group_name}_m{i}_pt", min_value=0.0, max_value=100.0, value=20.0, step=1.0, format="%.1f")
            with p_col3: pa = st.number_input("Away Win %", key=f"{group_name}_m{i}_pa", min_value=0.0, max_value=100.0, value=30.0, step=1.0, format="%.1f")
            with p_col4: xgh = st.number_input("Home xG", key=f"{group_name}_m{i}_xgh", min_value=0.0, value=2.0, step=0.1, format="%.2f")
            with p_col5: xga = st.number_input("Away xG", key=f"{group_name}_m{i}_xga", min_value=0.0, value=1.0, step=0.1, format="%.2f")
            
            group_preds.append({
                "group": group_name, "home": home_team, "away": away_team, 
                "home_score": h_score, "away_score": a_score,
                "ph": ph, "pt": pt, "pa": pa, "xgh": xgh, "xga": xga
            })
            st.write("---")
        predictions[group_name] = group_preds

    simulate_button = st.form_submit_button("Simulate Final Standings", type="primary")

if simulate_button:
    st.success("Simulation Complete! Scroll down to see the final standings.")
    st.header("🏁 Simulated Final Standings")
    
    for group_name in groups_data.keys():
        st.subheader(group_name)
        group_past = [m for m in past_matches if m["group"] == group_name]
        group_simulated = predictions[group_name]
        all_matches = group_past + group_simulated
        
        raw_standings = calculate_standings(groups_data[group_name], all_matches)
        sorted_standings = resolve_ties(raw_standings, all_matches)
        
        sim_df = create_group_df(sorted_standings)
        st.dataframe(sim_df, column_config={"Logo": st.column_config.ImageColumn("Logo", help="Team Logo"), "Position": st.column_config.NumberColumn("Pos", format="%d")}, hide_index=True, use_container_width=True)

# --- MONTE CARLO ENGINE ---
st.divider()
st.header("🎲 Monte Carlo Simulator")
st.markdown("Run 10,000 statistical simulations using the **Predictive Metrics** you entered above to calculate the true probability of each team's final placement. *(Note: Please ensure you click 'Simulate Final Standings' above first to lock in any probability changes!)*")

mc_iterations = st.number_input("Number of Simulations", min_value=100, max_value=10000, value=1000, step=100)
run_mc = st.button("Run Monte Carlo", type="primary")

def simulate_match_randomly(ph, pt, pa, xgh, xga):
    # 1. Normalize user probability inputs
    total_p = ph + pt + pa
    p_home, p_tie, p_away = (ph/total_p, pt/total_p, pa/total_p) if total_p > 0 else (0.334, 0.333, 0.333)
    
    # 2. Select Outcome based on user's Win/Draw/Loss %
    outcome = np.random.choice(['H', 'D', 'A'], p=[p_home, p_tie, p_away])
    
    # 3. Generate goals using Poisson based on user's xG until they fit the outcome
    for _ in range(100):
        hg = np.random.poisson(xgh)
        ag = np.random.poisson(xga)
        if outcome == 'H' and hg > ag: return hg, ag
        if outcome == 'D' and hg == ag: return hg, ag
        if outcome == 'A' and hg < ag: return hg, ag
        
    # Fallback if the xG provided is mathematically too extreme to fit the probability outcome
    if outcome == 'H': return 1, 0
    if outcome == 'D': return 0, 0
    return 0, 1

if run_mc:
    if not predictions:
        st.warning("Please click the 'Simulate Final Standings' button above to initialize the data before running the Monte Carlo.")
    else:
        progress = st.progress(0)
        status_text = st.empty()
        
        # Results matrix: group -> team -> position -> count
        mc_results = {g: {t["Team"]: {1:0, 2:0, 3:0, 4:0} for t in groups_data[g]} for g in groups_data}
        
        for i in range(mc_iterations):
            for group_name in groups_data.keys():
                group_past = [m for m in past_matches if m["group"] == group_name]
                
                # Simulate Matchday 6 dynamically
                simulated_m6 = []
                for match in predictions[group_name]:
                    hg, ag = simulate_match_randomly(match["ph"], match["pt"], match["pa"], match["xgh"], match["xga"])
                    simulated_m6.append({"home": match["home"], "away": match["away"], "home_score": hg, "away_score": ag})
                    
                all_matches = group_past + simulated_m6
                raw_standings = calculate_standings(groups_data[group_name], all_matches)
                sorted_standings = resolve_ties(raw_standings, all_matches)
                
                for pos, team in enumerate(sorted_standings):
                    mc_results[group_name][team["Team"]][pos + 1] += 1
                    
            if i % (mc_iterations // 10) == 0:
                progress.progress(i / mc_iterations)
                status_text.text(f"Running simulation {i}/{mc_iterations}...")
                
        progress.progress(1.0)
        status_text.text("Simulation Complete!")
        
        # Display the Matrix
        for group_name in groups_data.keys():
            st.subheader(f"{group_name} Probabilities")
            
            res_data = []
            for team_name, positions in mc_results[group_name].items():
                row = {"Team": team_name}
                for pos in [1, 2, 3, 4]:
                    row[f"{pos}º"] = f"{(positions[pos] / mc_iterations) * 100:.1f}%"
                res_data.append(row)
                
            df_res = pd.DataFrame(res_data)
            
            # Sort dataframe mathematically by highest probability of finishing 1st
            df_res["1st_val"] = df_res["1º"].str.rstrip('%').astype(float)
            df_res["2nd_val"] = df_res["2º"].str.rstrip('%').astype(float)
            df_res = df_res.sort_values(by=["1st_val", "2nd_val"], ascending=[False, False])
            df_res = df_res.drop(columns=["1st_val", "2nd_val"])
            
            # Add logos back into the final table
            df_res["Logo"] = df_res["Team"].apply(lambda t: next(item["Logo"] for item in groups_data[group_name] if item["Team"] == t))
            df_res = df_res[["Logo", "Team", "1º", "2º", "3º", "4º"]]
            
            st.dataframe(
                df_res,
                column_config={"Logo": st.column_config.ImageColumn("Logo", help="Team Logo")},
                hide_index=True,
                use_container_width=True
            )
