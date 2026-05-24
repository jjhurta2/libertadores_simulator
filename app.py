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

# --- SIMULATOR SECTION ---
st.header("🔮 Matchday 6 Simulator")
st.markdown("Enter the scores for the final matches. The tables will update automatically based on your tie-breaker rules.")

# Dictionary to store the match predictions
predictions = {}

# Create a form so the app doesn't refresh on every single number change
with st.form("simulator_form"):
    for group_name, data in groups_data.items():
        st.subheader(group_name)
        
        # We assume the remaining matches are Team 1 vs Team 2, and Team 3 vs Team 4
        match_1_home = data[0]["Team"]
        match_1_away = data[1]["Team"]
        
        match_2_home = data[2]["Team"]
        match_2_away = data[3]["Team"]
        
        # Match 1 UI Layout
        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 3])
        with col1: 
            st.markdown(f"<p style='text-align: right; margin-top: 10px;'><b>{match_1_home}</b></p>", unsafe_allow_html=True)
        with col2: 
            m1_h_score = st.number_input("Home", key=f"{group_name}_m1_h", min_value=0, value=0, label_visibility="collapsed")
        with col3: 
            st.markdown("<p style='text-align: center; margin-top: 10px;'>vs</p>", unsafe_allow_html=True)
        with col4: 
            m1_a_score = st.number_input("Away", key=f"{group_name}_m1_a", min_value=0, value=0, label_visibility="collapsed")
        with col5: 
            st.markdown(f"<p style='margin-top: 10px;'><b>{match_1_away}</b></p>", unsafe_allow_html=True)
            
        # Match 2 UI Layout
        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 3])
        with col1: 
            st.markdown(f"<p style='text-align: right; margin-top: 10px;'><b>{match_2_home}</b></p>", unsafe_allow_html=True)
        with col2: 
            m2_h_score = st.number_input("Home", key=f"{group_name}_m2_h", min_value=0, value=0, label_visibility="collapsed")
        with col3: 
            st.markdown("<p style='text-align: center; margin-top: 10px;'>vs</p>", unsafe_allow_html=True)
        with col4: 
            m2_a_score = st.number_input("Away", key=f"{group_name}_m2_a", min_value=0, value=0, label_visibility="collapsed")
        with col5: 
            st.markdown(f"<p style='margin-top: 10px;'><b>{match_2_away}</b></p>", unsafe_allow_html=True)

        # Save inputs to our predictions dictionary
        predictions[group_name] = [
            {"home": match_1_home, "home_score": m1_h_score, "away": match_1_away, "away_score": m1_a_score},
            {"home": match_2_home, "home_score": m2_h_score, "away": match_2_away, "away_score": m2_a_score}
        ]
        
        st.write("---")

    # The submit button to trigger the table recalculation
    simulate_button = st.form_submit_button("Simulate Final Standings", type="primary")

if simulate_button:
    st.success("Scores submitted! (Tie-breaker logic coming next)")
