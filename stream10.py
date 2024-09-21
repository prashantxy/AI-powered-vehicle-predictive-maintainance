import streamlit as st
import pandas as pd
from io import StringIO
import requests

# Load the dataset into a DataFrame
data = """s ID,Engine Temp (°C),Oil Pressure (psi),RPM (x1000),Fuel Consumption (L/100km),Battery Voltage (V),Battery Temp (°C),Brake Pad Thickness (mm),Brake Fluid Level (%),Tire Tread Depth (mm),Tire Pressure (psi),Tire Temp (°C),Shock Absorber Condition (%),Ride Height (mm),Transmission Fluid Level (%),Gear Shifts (Count),CO2 Emission (g/km),NOx Emission (ppm),Coolant Level (%),Radiator Condition (%),DTC Count,Electrical System Voltage (V),Last Maintenance Date
Bus_1,90,40,2.5,12.5,13.0,30,8,90,7,32,35,85,140,95,150,120,50,95,90,3,14.0,2024-09-01
Bus_2,85,38,2.7,13.0,12.8,28,9,85,6,30,33,80,142,90,160,115,55,90,88,2,13.8,2024-09-02
Bus_3,92,42,2.8,14.0,13.1,32,7,87,8,31,34,82,138,88,155,125,52,92,89,4,14.1,2024-09-01
Bus_4,88,39,2.4,12.0,12.9,29,6,88,6.5,33,31,78,139,92,148,118,53,93,87,1,13.9,2024-09-03
Bus_5,89,41,2.6,13.5,13.2,31,8,89,7.2,32,36,83,141,94,153,122,51,96,91,3,14.2,2024-09-01
Bus_6,91,40,2.9,13.2,13.0,30,7.5,86,6.8,29,34,81,137,89,152,117,56,91,90,2,14.0,2024-09-02
Bus_7,87,37,2.3,11.8,12.7,28,9,84,6.2,31,32,77,140,91,150,113,54,88,86,1,13.7,2024-09-03
Bus_8,93,43,3.0,14.2,13.3,33,7,90,8,34,37,86,142,96,158,126,50,97,92,4,14.3,2024-09-01
Bus_9,86,36,2.2,12.3,12.6,27,8.5,83,6.4,30,33,79,139,87,149,116,55,89,87,2,13.6,2024-09-02
Bus_10,94,44,3.1,14.5,13.4,34,6.8,92,7.8,35,38,88,143,97,160,128,49,98,93,5,14.4,2024-09-01
Bus_11,88,40,2.5,12.4,13.0,30,8.2,91,7.1,32,36,85,141,96,150,120,51,94,90,3,14.0,2024-09-02
Bus_12,86,38,2.6,12.8,12.9,28,9,85,6.6,31,33,80,139,89,160,115,52,90,88,2,13.9,2024-09-03
Bus_13,91,42,2.9,13.8,13.2,31,7,86,7.3,29,34,82,137,88,153,125,50,91,89,4,14.1,2024-09-01
Bus_14,89,39,2.4,12.1,13.1,29,6.8,88,6.4,32,31,78,140,92,148,118,55,93,87,1,14.0,2024-09-02
Bus_15,92,41,2.7,13.7,13.3,30,8.5,89,7.0,30,35,83,142,94,152,122,53,96,91,3,14.2,2024-09-03
Bus_16,87,40,2.8,13.0,12.7,27,7.2,87,6.9,33,35,81,139,92,149,116,56,90,89,2,13.8,2024-09-01"""

df = pd.read_csv(StringIO(data))

# Title and Header of the App
st.title("🚌 AI-Powered Bus Predictive Maintenance")
st.markdown("""
    This app predicts when a bus will need maintenance based on various bus parameters.
""")

# Sidebar Input Fields for Bus Data
st.sidebar.header("Input Bus Data")
bus_id = st.sidebar.selectbox("Select Bus ID", df['s ID'].unique())
selected_bus = df[df['s ID'] == bus_id].iloc[0]

# Display selected bus data
st.sidebar.subheader("Selected Bus Data")
st.sidebar.write(selected_bus)

# Extract parameters from the selected bus
mileage = selected_bus['RPM (x1000)'] * 1000  # Simulated mileage based on RPM
fuel_consumption = selected_bus['Fuel Consumption (L/100km)'] * 0.264172  # Convert L/100km to gallons
engine_hours = (mileage / 15)  # Assume average speed of 15 mph for engine hours
bus_weight = 15  # Example fixed weight
passengers = st.sidebar.number_input("Number of Passengers", min_value=1, max_value=100, value=50)
oil_level = st.sidebar.slider("Engine Oil Level (%)", min_value=0, max_value=100, value=75)
tire_pressure = selected_bus['Tire Pressure (psi)']

# Bus Data inputted by user
bus_data = {
    "mileage": int(mileage),
    "fuel_consumption": float(fuel_consumption),
    "engine_hours": float(engine_hours),
    "bus_weight": float(bus_weight),
    "passengers": int(passengers),
    "oil_level": int(oil_level),
    "tire_pressure": int(tire_pressure)
}

# Function to call the Relcomp API
def get_maintenance_prediction(bus_data):
    # Replace this URL with your real predictive maintenance API endpoint
    url = 'https://relcomp.p.rapidapi.com/calculate'
    
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "your-rapidapi-key",
        "X-RapidAPI-Host": "relcomp.p.rapidapi.com"
    }

    response = requests.post(url, json=bus_data, headers=headers)
    
    if response.status_code == 200:
        prediction = response.json()
        return prediction.get('maintenance_needed_in_miles', None)
    else:
        return None

# Button to make the prediction
if st.sidebar.button("Predict Maintenance"):
    # Check if the engine oil level is above 80%
    if bus_data['oil_level'] > 80:
        st.warning("⚠️ Maintenance is required due to high engine oil level.")
    else:
        # Get the predicted maintenance from the API
        maintenance_miles = get_maintenance_prediction(bus_data)
        
        if maintenance_miles:
            st.success(f"🛠️ Maintenance is needed in **{maintenance_miles} miles**.")
        else:
            st.error("❌ Maintenance do not required.")

# Displaying the inputted data
st.subheader("Bus Data Summary")
st.write(f"Mileage: {mileage} miles")
st.write(f"Fuel Consumption: {fuel_consumption:.2f} gallons")
st.write(f"Engine Hours: {engine_hours:.2f} hours")
st.write(f"Bus Weight: {bus_weight} tons")
st.write(f"Number of Passengers: {passengers}")
st.write(f"Engine Oil Level: {oil_level}%")
st.write(f"Tire Pressure: {tire_pressure} psi")

# Optional data visualization
st.subheader("Sample Prediction Data")
chart_data = pd.DataFrame({
    'Mileage': [10000, 20000, 30000, 40000, 50000],
    'Predicted Maintenance': [500, 1000, 1500, 2000, 2500]
})
st.line_chart(chart_data)

# Footer
st.markdown("🔧 Powered by ALGOOPTIMA")
