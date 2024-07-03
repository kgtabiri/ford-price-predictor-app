import streamlit as st
from predict_page import show_predict_page
from explore_page import show_explore_page

st.set_page_config(page_title="Ford Price Predictor", page_icon='Ford-Logo.png', initial_sidebar_state="collapsed")
page = st.sidebar.selectbox("Explore Or Predict", ("Home", "Predict", "Explore"))

if page == "Home":
    st.title("Welcome to the Ford price prediction and exploration application! :dollar: :car: :chart_with_upwards_trend: :bar_chart:")
    st.markdown(
        "This web application allows you to predict the price of used Ford vehicles across" +
        " and to view visualizations average price and number of listings by state. It covers" + 
        " 49 US states.") 
    st.write(" ")
    st.markdown("On the **Predict** page, you will be required to choose the *Census Division*," +
        " *State*, *Base Model*, *Feature*, *Manufacturer*, and *Mileage*. After providing this information, our machine " +
        " learning model provides you with an estimated price.")
    st.write(" ")
    st.markdown(" On the **Explore** page, selecting a *Base model* and *Year* allows you to see the minimum, " +
        " maximum, and average prices for the selected model and year. In addition you will see the average " +
        " price in each state that has a listing for that year-model choice as well as the number of listings" +
        " by state. Lastly the app shows you top 3 feature options available for that car"
        )
elif page == "Predict":
    show_predict_page()
elif page == "Explore":
    show_explore_page()