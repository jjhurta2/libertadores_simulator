import streamlit as st
import pandas as pd

# Configure the page layout
st.set_page_config(page_title="Copa Libertadores 2026 Simulator", layout="wide")
st.title("🏆 Copa Libertadores 2026 Simulator")
st.markdown("Current group stage standings across all 8 groups.")

# Helper function to generate your specific GitHub raw image URL
def get_logo_url(filename):
    return f"https://github.com/jjhurta2/libertadores_simulator/blob/main/{filename}?raw=true"

# Helper function to format the dataframe
def create_group_df(data):
    df = pd.DataFrame(data)
    
    # Reorder the columns precisely as requested
    cols = [
        "Position", "Logo", "Team", "Played", "Won", "Lost", "Drawn", 
        "Goals Scored", "Goals Received", "Goal Difference", "Points"
    ]
    return df[cols]

# Live 2026 Copa Libertadores Data
groups_data = {
    "Group A": [
        {"Position": 1, "Logo": get_logo_url("flamengo.png"), "Team": "Flamengo", "Played": 5, "Won": 4, "Lost": 0, "Drawn": 1, "Goals Scored": 11, "Goals Received": 2, "Goal Difference": 9, "Points": 13},
        {"Position": 2, "Logo": get_logo_url("medellin.png"), "Team": "Independiente Medellín", "Played": 5, "Won": 2, "Lost": 2, "Drawn": 1, "Goals Scored": 6, "Goals Received": 10, "Goal Difference": -4, "Points": 7},
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
        {"Position": 1, "Logo": get_logo_url("ind_rivadavia.png"), "Team": "Ind. Rivadavia", "Played": 5, "Won": 4, "Lost": 0, "Drawn": 1, "Goals Scored": 12, "Goals Received": 5, "Goal Difference": 7, "Points": 13},
        {"Position": 2, "Logo": get_logo_url("bolivar.png"), "Team": "Bolívar", "Played": 5, "Won": 1, "Lost": 2, "Drawn": 2, "Goals Scored": 5, "Goals Received": 5, "Goal Difference": 0, "Points": 5},
        {"Position": 3, "Logo": get_logo_url("fluminense.png"), "Team": "Fluminense FC", "Played": 5, "Won": 1, "Lost": 2, "Drawn": 2, "Goals Scored": 4, "Goals Received": 6, "Goal Difference": -2, "Points": 5},
        {"Position": 4, "Logo": get_logo_url("la_guaira.png"), "Team": "Deportivo La Guaira", "Played": 5, "Won": 0, "Lost": 2, "Drawn": 3, "Goals Scored": 5, "Goals Received": 10, "Goal Difference": -5, "Points": 3}
    ],
    "Group D": [
        {"Position": 1, "Logo": get_logo_url("catolica.png"), "Team": "Universidad Católica", "Played": 5, "Won": 3, "Lost": 1, "Drawn": 1, "Goals Scored": 7, "Goals Received": 4, "Goal Difference": 3, "Points": 10},
        {"Position": 2, "Logo": get_logo_url("cruzeiro.png"), "Team": "Cruzeiro", "Played": 5, "Won": 2, "Lost": 1, "Drawn": 2, "Goals Scored": 4, "Goals Received": 3, "Goal Difference": 1, "Points": 8},
        {"Position": 3, "Logo": get_logo_url("boca.png"), "Team": "Boca Juniors", "Played": 5, "Won": 2, "Lost": 2, "Drawn": 1, "Goals Scored": 6, "Goals Received": 4, "Goal Difference": 2, "Points": 7},
        {"Position": 4, "Logo": get_logo_url("barcelona_sc.png"), "Team": "Barcelona S.C.", "Played": 5, "Won": 1, "Lost": 4, "Drawn": 0, "Goals Scored": 2, "Goals Received": 8, "Goal Difference": -6, "Points": 3}
    ],
    "Group E": [
        {"Position": 1, "Logo": get_logo_url("corinthians.png"), "Team": "Corinthians", "Played": 5, "Won": 3, "Lost": 0, "Drawn": 2, "Goals Scored": 8, "Goals Received": 2, "Goal Difference": 6, "Points": 11},
        {"Position": 2, "Logo": get_logo_url("platense.png"), "Team": "Platense", "Played": 5, "Won": 2, "Lost": 2, "Drawn": 1, "Goals Scored": 6, "Goals Received": 7, "Goal Difference": -1, "Points": 7},
        {"Position": 3, "Logo": get_logo_url("santa_fe.png"), "Team": "Independiente Santa Fe", "Played": 5, "Won": 1, "Lost": 2, "Drawn": 2, "Goals Scored": 5, "Goals Received": 7, "Goal Difference": -2, "Points": 5},
        {"Position": 4, "Logo": get_logo_url("penarol.png"), "Team": "Peñarol", "Played": 5, "Won": 0, "Lost": 2, "Drawn": 3, "Goals Scored": 4, "Goals Received": 7, "Goal Difference": -3, "Points": 3}
    ],
    "Group F": [
        {"Position": 1, "Logo": get_logo_url("cerro_porteno.png"), "Team": "Cerro Porteño", "Played": 5, "Won": 3, "Lost": 1, "Drawn": 1, "Goals Scored": 4, "Goals Received": 2, "Goal Difference": 2, "Points": 10},
        {"Position": 2, "Logo": get_logo_url("palmeiras.png"), "Team": "Palmeiras", "Played": 5, "Won": 2, "Lost": 1, "Drawn": 2, "Goals Scored": 6, "Goals Received": 4, "Goal Difference": 2, "Points": 8},
        {"Position": 3, "Logo": get_logo_url("sporting_cristal.png"), "Team": "Sporting Cristal", "Played": 5, "Won": 2, "Lost": 3, "Drawn": 0, "Goals Scored": 6, "Goals Received": 7, "Goal Difference": -1, "Points": 6},
        {"Position": 4, "Logo": get_logo_url("junior.png"), "Team": "Junior FC", "Played": 5, "Won": 1, "Lost": 3, "Drawn": 1, "Goals Scored": 4, "Goals Received": 7, "Goal Difference": -3, "Points": 4}
    ],
    "Group G": [
        {"Position": 1, "Logo": get_logo_url("mirassol.png"), "Team": "Mirassol", "Played": 5, "Won": 4, "Lost": 1, "Drawn": 0, "Goals Scored": 7, "Goals Received": 3, "Goal Difference": 4, "Points": 12},
        {"Position": 2, "Logo": get_logo_url("ldu_quito.png"), "Team": "LDU Quito", "Played": 5, "Won": 3, "Lost": 2, "Drawn": 0, "Goals Scored": 5, "Goals Received": 3, "Goal Difference": 2, "Points": 9},
        {"Position": 3, "Logo": get_logo_url("lanus.png"), "Team": "Lanús", "Played": 5, "Won": 2, "Lost": 3, "Drawn": 0, "Goals Scored": 2, "Goals Received": 7, "Goal Difference": -5, "Points": 6},
        {"Position": 4, "Logo": get_logo_url("always_ready.png"), "Team": "Always Ready", "Played": 5, "Won": 1, "Lost": 4, "Drawn": 0, "Goals Scored": 5, "Goals Received": 6, "Goal Difference": -1, "Points": 3}
    ],
    "Group H": [
        {"Position": 1, "Logo": get_logo_url("rosario_central.png"), "Team": "Rosario Central", "Played": 5, "Won": 4, "Lost": 0, "Drawn": 1, "Goals Scored": 9, "Goals Received": 0, "Goal Difference": 9, "Points": 13},
        {"Position": 2, "Logo": get_logo_url("ind_del_valle.png"), "Team": "Independiente del Valle", "Played": 5, "Won": 3, "Lost": 1, "Drawn": 1, "Goals Scored": 10, "Goals Received": 6, "Goal Difference": 4, "Points": 10},
        {"Position": 3, "Logo": get_logo_url("uni_central.png"), "Team": "Universidad Central", "Played": 5, "Won": 2, "Lost": 3, "Drawn": 0, "Goals Scored": 6, "Goals Received": 11, "Goal Difference": -5, "Points": 6},
        {"Position": 4, "Logo": get_logo_url("libertad.png"), "Team": "Libertad", "Played": 5, "Won": 0, "Lost": 5, "Drawn": 0, "Goals Scored": 4, "Goals Received": 12, "Goal Difference": -8, "Points": 0}
    ]
}

# Render each group in the app
for group_name, data in groups_data.items():
    st.subheader(group_name)
    df = create_group_df(data)
    
    # Configure Streamlit to render the Logo column as actual images
    st.dataframe(
        df,
        column_config={
            "Logo": st.column_config.ImageColumn("Logo", help="Team Logo"),
            "Position": st.column_config.NumberColumn("Pos", format="%d"),
        },
        hide_index=True,
        use_container_width=True
    )

st.divider()

# --- HISTORICAL DATA (Matchdays 1-5) ---
# To make H2H tie-breakers work, the app needs the real past results. 
# You can fill in the rest of the real scores from online here.
past_matches = [
    # Group A Examples
    {"group": "Group A", "home": "Flamengo", "away": "Estudiantes de La Plata", "home_score": 1, "away_score": 0},
    {"group": "Group A", "home": "Cusco FC", "away": "Independiente Medellín", "home_score": 2, "away_score": 3},
    # ... Add the remaining real Matchday 1-5 results here ...
]

# --- MATCHDAY 6 FIXTURES ---
# The real official fixtures for the final matchday
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

# --- SIMULATOR SECTION ---
st.header("🔮 Matchday 6 Simulator")
st.markdown("Enter the scores for the final matches. The tables will recalculate using official H2H tie-breaker rules.")

predictions = {}

with st.form("simulator_form"):
    for group_name, fixtures in matchday_6_fixtures.items():
        st.subheader(group_name)
        group_preds = []
        
        for i, (home_team, away_team) in enumerate(fixtures):
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 3])
            with col1: 
                st.markdown(f"<p style='text-align: right; margin-top: 10px;'><b>{home_team}</b></p>", unsafe_allow_html=True)
            with col2: 
                h_score = st.number_input("Home", key=f"{group_name}_m{i}_h", min_value=0, value=0, label_visibility="collapsed")
            with col3: 
                st.markdown("<p style='text-align: center; margin-top: 10px;'>vs</p>", unsafe_allow_html=True)
            with col4: 
                a_score = st.number_input("Away", key=f"{group_name}_m{i}_a", min_value=0, value=0, label_visibility="collapsed")
            with col5: 
                st.markdown(f"<p style='margin-top: 10px;'><b>{away_team}</b></p>", unsafe_allow_html=True)
            
            group_preds.append({
                "group": group_name, "home": home_team, "away": away_team, 
                "home_score": h_score, "away_score": a_score
            })
            
        predictions[group_name] = group_preds
        st.write("---")

    simulate_button = st.form_submit_button("Simulate Final Standings", type="primary")

# --- ALGORITHM: TIE-BREAKER LOGIC ---
def calculate_standings(group_teams, all_group_matches):
    """Calculates table stats from scratch based on a list of matches."""
    stats = {team["Team"]: {"Played": 0, "Won": 0, "Lost": 0, "Drawn": 0, "Goals Scored": 0, "Goals Received": 0, "Points": 0, "Logo": team["Logo"]} for team in group_teams}
    
    for match in all_group_matches:
        home, away = match["home"], match["away"]
        hg, ag = match["home_score"], match["away_score"]
        
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
    """Sorts teams using the 6-step tie-breaker rules."""
    # First, group teams by Total Points (Rule 4 fallback)
    points_groups = {}
    for team in teams_list:
        points = team["Points"]
        if points not in points_groups:
            points_groups[points] = []
        points_groups[points].append(team)
    
    final_sorted_group = []
    
    # Sort the point tiers from highest to lowest
    for points in sorted(points_groups.keys(), reverse=True):
        tied_teams = points_groups[points]
        
        if len(tied_teams) == 1:
            final_sorted_group.append(tied_teams[0])
            continue
            
        # We have a tie! Calculate a H2H mini-table (Rules 1, 2, 3)
        tied_team_names = [t["Team"] for t in tied_teams]
        h2h_matches = [m for m in all_group_matches if m["home"] in tied_team_names and m["away"] in tied_team_names]
        
        # Calculate stats ONLY for games between the tied teams
        h2h_stats = calculate_standings(tied_teams, h2h_matches)
        
        # Map original total stats to H2H stats for rules 4, 5, 6
        for ht in h2h_stats:
            orig = next(t for t in tied_teams if t["Team"] == ht["Team"])
            ht["Total Goal Difference"] = orig["Goal Difference"]
            ht["Total Goals Scored"] = orig["Goals Scored"]
            ht["Original Data"] = orig # Keep the aggregate data to display later
            
        # Sort the mini-table based on your 6 criteria
        h2h_stats.sort(key=lambda x: (
            x["Points"],                  # 1. H2H Points
            x["Goal Difference"],         # 2. H2H Goal Difference
            x["Goals Scored"],            # 3. H2H Goals Scored
            x["Original Data"]["Points"], # 4. Total Points (they are tied here, but kept for logic flow)
            x["Total Goal Difference"],   # 5. Total Goal Difference
            x["Total Goals Scored"]       # 6. Total Goals Scored
        ), reverse=True)
        
        for sorted_team in h2h_stats:
            final_sorted_group.append(sorted_team["Original Data"])
            
    # Assign new positions
    for i, team in enumerate(final_sorted_group):
        team["Position"] = i + 1
        
    return final_sorted_group


# --- RENDER SIMULATED RESULTS ---
if simulate_button:
    st.success("Simulation Complete! Scroll down to see the final standings.")
    st.header("🏁 Simulated Final Standings")
    
    for group_name in groups_data.keys():
        st.subheader(group_name)
        
        # Combine real past matches with user's Matchday 6 predictions
        group_past = [m for m in past_matches if m["group"] == group_name]
        group_simulated = predictions[group_name]
        all_matches = group_past + group_simulated
        
        # Calculate new aggregates and apply the tie-breaker sort
        raw_standings = calculate_standings(groups_data[group_name], all_matches)
        sorted_standings = resolve_ties(raw_standings, all_matches)
        
        # Display the newly sorted dataframe
        sim_df = create_group_df(sorted_standings)
        st.dataframe(
            sim_df,
            column_config={
                "Logo": st.column_config.ImageColumn("Logo", help="Team Logo"),
                "Position": st.column_config.NumberColumn("Pos", format="%d"),
            },
            hide_index=True,
            use_container_width=True
        )
