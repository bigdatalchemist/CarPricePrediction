import pickle
import pandas as pd
import streamlit as st

# ✅ Load Model, Encoder, and Column Names
model = pickle.load(open("model.pkl", "rb"))
encoder = pickle.load(open("encoder.pkl", "rb"))
all_columns = pickle.load(open("columns.pkl", "rb"))  # Ensure correct feature order

# ✅ Function to preprocess input
def preprocess_input(input_data):
    df_input = pd.DataFrame([input_data])  # Convert dict to DataFrame

    # 🔹 Convert categorical to numeric
    door_map = {'two': 2, 'four': 4}
    cylinder_map = {'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'eight': 8, 'twelve': 12}
    df_input['doornumber'] = df_input['doornumber'].map(door_map)
    df_input['cylindernumber'] = df_input['cylindernumber'].map(cylinder_map)

    # 🔹 Apply encoding
    input_encoded = encoder.transform(df_input)

    # 🔹 Convert to DataFrame and reorder columns
    input_df = pd.DataFrame(input_encoded, columns=all_columns)

    return input_df

# ✅ Streamlit UI
st.title("Car Price Prediction App")

# 🎯 User Inputs
user_input = {
    "symboling": st.number_input("Symboling", min_value=-2, max_value=3, value=0),
    "fueltype": st.selectbox("Fuel Type", ["gas", "diesel"]),
    "aspiration": st.selectbox("Aspiration", ["std", "turbo"]),
    "doornumber": st.selectbox("Door Number", ["two", "four"]),
    "carbody": st.selectbox("Car Body", ["convertible", "hatchback", "sedan", "wagon", "hardtop"]),
    "drivewheel": st.selectbox("Drive Wheel", ["rwd", "fwd", "4wd"]),
    "enginelocation": st.selectbox("Engine Location", ["front", "rear"]),
    "wheelbase": st.number_input("Wheelbase"),
    "carlength": st.number_input("Car Length"),
    "carwidth": st.number_input("Car Width"),
    "carheight": st.number_input("Car Height"),
    "curbweight": st.number_input("Curb Weight"),
    "enginetype": st.selectbox("Engine Type", ["dohc", "ohcv", "ohc", "l", "rotor"]),
    "cylindernumber": st.selectbox("Cylinder Number", ["two", "three", "four", "five", "six", "eight", "twelve"]),
    "enginesize": st.number_input("Engine Size"),
    "fuelsystem": st.selectbox("Fuel System", ["mpfi", "2bbl", "1bbl", "spdi", "4bbl"]),
    "boreratio": st.number_input("Bore Ratio"),
    "stroke": st.number_input("Stroke"),
    "compressionratio": st.number_input("Compression Ratio"),
    "horsepower": st.number_input("Horsepower"),
    "peakrpm": st.number_input("Peak RPM"),
    "citympg": st.number_input("City MPG"),
    "highwaympg": st.number_input("Highway MPG"),
}

if st.button("Predict Price"):
    # ✅ Preprocess input and predict
    input_df = preprocess_input(user_input)
    prediction = model.predict(input_df)[0]

    # ✅ Display prediction
    st.success(f"Estimated Car Price: ${prediction:,.2f}")
