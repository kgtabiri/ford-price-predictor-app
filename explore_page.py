# Load required packages
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.metric_cards import style_metric_cards

def style_metric_cards(
    color:str = "#232323",
    background_color: str = "#FFF",
    border_size_px: int = 1,
    border_color: str = "#CCC",
    border_radius_px: int = 5,
    border_left_color: str = "#9AD8E1",
    box_shadow: bool = True,
):

    box_shadow_str = (
        "box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15) !important;"
        if box_shadow
        else "box-shadow: none !important;"
    )
    st.markdown(
        f"""
        <style>
            div[data-testid="metric-container"] {{
                background-color: {background_color};
                border: {border_size_px}px solid {border_color};
                padding: 5% 5% 5% 10%;
                border-radius: {border_radius_px}px;
                border-left: 0.5rem solid {border_left_color} !important;
                color: {color};
                {box_shadow_str}
            }}
             div[data-testid="metric-container"] p {{
              color: {color};
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

df = pd.read_csv('used_cars3.csv')
map_df = pd.read_csv('Book1.csv')

df = df.merge(map_df, on='State')

def show_explore_page():
    st.title("Explore average price and number of listings across states :chart_with_upwards_trend: :bar_chart:")
    st.sidebar.title("Choose base model and year")

    #st.sidebar.markdown("### Choose the base model")
    model = st.sidebar.selectbox('Base Model', list(df['Base Model'].unique()))

    #st.sidebar.markdown("### Choose year of manufacture")
    year = st.sidebar.selectbox('Year', list(sorted(df['Year'].unique())))

    
    filtered_df = df[(df['Year'] == year) & (df['Base Model'] == model)]
    avg_price = filtered_df['Price'].mean()
    min_price = filtered_df['Price'].min()
    max_price = filtered_df['Price'].max()

    st.markdown("**Price statistics for {} {}**".format(year, model))
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Minimum Price", value=f"${min_price:,.2f}")
    col2.metric(label="Maximum Price", value=f"${max_price:,.2f}")
    col3.metric(label="Average Price", value=f"${avg_price:,.2f}")
    # this is used to style the metric card
    style_metric_cards(border_left_color="#DBF227")

    # Bar chart for average price by state
    bar_df = filtered_df.groupby('State')['Price'].mean().reset_index()
    bar_fig = px.bar(bar_df, x='State', y='Price', title='Average Price by State')
    st.plotly_chart(bar_fig)

    # Doughnut chart for top 3 features
    all_features = filtered_df['Features'].tolist()
    feature_counts = pd.Series(all_features).value_counts().nlargest(3)
    doughnut_fig = go.Figure(data=[go.Pie(labels=feature_counts.index, values=feature_counts.values, hole=0.4)])
    doughnut_fig.update_layout(title_text='Top 3 Features', annotations=[dict(text='Features', x=0.5, y=0.5, font_size=20, showarrow=False)])
    st.plotly_chart(doughnut_fig)

    st.markdown("### Location of listings based on model and year")
    st.markdown("Listings for {} {}".format(year, model))

    # Map showing the number of listings per state
    map_df = filtered_df.groupby(['State', 'latitude', 'longitude']).size().reset_index(name='Listings')
    map_fig = px.scatter_mapbox(map_df, lat="latitude", lon="longitude", size="Listings", hover_name="State",
                            hover_data={"latitude": False, "longitude": False},
                            color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=3,
                            title="Number of Listings by State")
    map_fig.update_layout(mapbox_style="carto-positron")
    map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(map_fig)
    
    
    



    #st.title("Explore Software Engineer Salaries")

    #st.write(
     #   """
    ### Stack Overflow Developer Survey 2020
    #"""
    #)