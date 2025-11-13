import streamlit as st

st.set_page_config(
    page_title="BFH",
    page_icon="🍱",
)

selected_app = st.sidebar.selectbox("Select a recommendation app.", ["Select an app", "Diet Recommendation", "Diet-Friendly Dish Explorer", "Alternate Recipes"])

if selected_app == "Diet Recommendation":
    print("DEBUG: Selected app is Diet Recommendation")
    import DietRecom
    DietRecom.main()
elif selected_app == "Diet-Friendly Dish Explorer":
    print("DEBUG: Selected app is Recipe Recommendations Based on Dietary Restrictions")
    import restrictions
    restrictions.main()
elif selected_app == "Alternate Recipes":
    print("DEBUG: Selected app is Alternate Recipes")
    import similarity
    similarity.main()
else:
    print("DEBUG: No app selected")
    st.title("Welcome to Better Food Habits!🥗")
    st.markdown("<hr>", unsafe_allow_html=True)
    st.info("Please select an app from the sidebar dropdown.")
    st.markdown(
        """
        Welcome to Better Food Habits! Your personalized nutrition assistant for healthier living. Get tailored meal recommendations, expert insights, and intuitive tracking features to support your wellness goals. Join us today and start your journey towards a healthier you.
        """
    )
    st.write("---")
    st.markdown("<p>Created by: <b>Anirudh and Ayush</b></p>", unsafe_allow_html=True)

