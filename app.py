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
        
        st.write("---") # Visual separator between groups

    # The submit button to trigger the table recalculation
    simulate_button = st.form_submit_button("Simulate Final Standings", type="primary")

if simulate_button:
    st.success("Scores submitted! (Tie-breaker logic coming next)")
    # We will build the recalculation and tie-breaker sorting logic here in the next step.
