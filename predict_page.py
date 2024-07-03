import streamlit as st
import pickle
import numpy as np
from xgboost import XGBRegressor

census_divisions = {
    "New England": ["CT", "ME", "MA", "NH", "RI", "VT"],
    "Mid-Atlantic": ["NJ", "NY", "PA"],
    "East North Central": ["IL", "IN", "MI", "OH", "WI"],
    "West North Central": ["IA", "KS", "MN", "MO", "NE", "ND", "SD"],
    "South Atlantic": ["DE", "FL", "GA", "NC", "SC", "VA", "WV"],
    "East South Central": ["AL", "KY", "MS", "TN"],
    "West South Central": ["AR", "LA", "OK", "TX"],
    "Mountain": ["AZ", "CO", "ID", "MT", "NV", "NM", "UT", "WY"],
    "Pacific": ["AK", "CA", "OR", "WA"]
}

# Load in trained model with label encoders
def load_model():
    try:
        with open('price_predictor.pkl', 'rb') as file:
            data = pickle.load(file)
        return data
    except FileNotFoundError:
        st.error("The model file 'price_predictor.pkl' was not found.")
        return None
    except pickle.UnpicklingError:
        st.error("The model file 'price_predictor.pkl' could not be unpickled.")
        return None
#def load_model():
 #   with open('price_predictor.pkl', 'rb') as file:
  #      data = pickle.load(file)
   # return data

data = load_model()

predictor = data["model"]
le_year = data["le_year"]
le_divs = data["le_divs"]
le_state = data["le_state"]
le_manuf = data["le_manuf"]
le_model = data["le_model"]
le_feats = data["le_feats"]

def show_predict_page():
    st.title("Used Ford Vehicle Price Prediction :dollar: :car: ")

    st.write("""### Please provide some information to predict the price""")

    # Create tables for categories of categorical variables
    divisions = (
        "South Atlantic", "Pacific",
        "West North Central", "Mid-Atlantic",
        "Mountain", "East North Central",
        "New England", "West South Central",
        "East South Central"
    )

    states = (
        'MD', 'CA', 'HI', 'GA', 'KS', 'FL', 'MO', 'VA', 'OR', 'WA', 'PA',
       'NJ', 'ID', 'AZ', 'NE', 'MI', 'RI', 'TX', 'UT', 'NY', 'WI', 'MA',
       'SC', 'NC', 'CO', 'MT', 'KY', 'VT', 'IL', 'AL', 'TN', 'NV', 'IN',
       'MS', 'NM', 'CT', 'IA', 'OH', 'NH', 'MN', 'OK', 'ME', 'AR', 'DE',
       'WV', 'ND', 'LA', 'WY', 'AK', 'SD', 'DC'
    )

    manufacturer = ("US", "Outside US")

    base_models = (
        'Taurus', 'Focus', 'Fusion', 'Fiesta', 'C-Max', 'Escape', 'Five',
       'Edge', 'ZX2', 'Mustang', 'F-150', 'Explorer', 'Transit', 'Super',
       'Freestyle', 'Expedition', 'E-Series', 'Freestar', 'Ranger',
       'Escort', 'Crown', 'Windstar', 'Club', 'Contour', 'Flex',
       'Thunderbird', 'Excursion'
    )

    features = (
        'Regular', 'S', 'SE', 'Hatchback', 'Sedan', '4dr', 'Hybrid',
       'Titanium', 'SEL', '5dr', 'FWD', '2dr', '3dr', 'Platinum', '4WD',
       'ST', 'Convertible', '2WD', 'Coupe', 'XL', 'V6', 'Fastback', 'RWD',
       'XLS', 'Base', 'EcoBoost', 'Limited', 'SPORT', 'XLT', 'Sport',
       'AWD', 'SuperCab', 'Police', 'SuperCrew', 'SHO', '5.4L', '119"',
       'GT', 'LTD', '4.6L', 'Eddie', 'Lariat', 'RS', 'Fleet', '137"',
       'King', 'FX4', "'07", '2010', 'Shelby', 'SVT', '2005', 'Edge',
       'EL', 'Raptor'
    )

    # Select features for price prediction
    division = st.selectbox("US Census Division", list(census_divisions.keys()))
    state = st.selectbox("State", census_divisions[division]) # Show only states that are in the selected division
    manufacturer = st.selectbox("Manufacturer", manufacturer)
    base_model = st.selectbox("Base Model", base_models)
    feature = st.selectbox("Feature", features)
    year = st.slider("Year of manufacture", 1997, 2018, 1997)
    mileage = st.number_input("Mileage", min_value=5, max_value=400000, value=1000)

    ok = st.button("Calculate Price")
    if ok:
        X = np.array([[year, mileage, state, manufacturer, base_model, feature, division]])
        # use label encoders to convert categorical columns to numeric
        X[:, 0] = le_year.transform(X[:,0])
        X[:, 2] = le_state.transform(X[:,2])
        X[:, 3] = le_manuf.transform(X[:,3])
        X[:, 4] = le_model.transform(X[:,4])
        X[:, 5] = le_feats.transform(X[:,5])
        X[:, 6] = le_divs.transform(X[:,6])
        X = X.astype(float)

        # Predict price and convert to original units
        price = predictor.predict(X)
        st.subheader(f"The estimated price is ${np.exp(price[0]):.2f}")

