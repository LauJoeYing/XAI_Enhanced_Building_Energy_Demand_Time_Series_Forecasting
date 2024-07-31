import streamlit as st
import pandas as pd

# Set Streamlit layout to wide
st.set_page_config(layout="wide")

# Load custom CSS
with open('path/to/your/style.css') as f:  # Update with the actual path to your CSS file
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Add subheading mentioning supervisor and second marker
st.markdown("<h2 style='text-align: center;'>Supervised by Dr. Preethi Subramanian</h2>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Second Marker: Assoc. Prof. Dr. Imran Medi</h2>", unsafe_allow_html=True)

st.title("Energy Cost Calculator")

# User inputs for kWh usage
kWh_usage = st.number_input("Enter your energy consumption in kWh:", min_value=0.0, format="%.2f")

# Energy suppliers and their rates
suppliers = {
    "TNB (Residential)": {
        "rates": [0.218, 0.334, 0.516, 0.546, 0.571],
        "thresholds": [200, 100, 300, 300, float('inf')]
    },
    "Sarawak Energy": {
        "rates": [0.33, 0.54],
        "thresholds": [150, float('inf')]
    },
    "SESB": {
        "rates": [0.34, 0.51],
        "thresholds": [100, float('inf')]
    }
}

# Function to calculate cost
def calculate_cost(kWh, rates, thresholds):
    cost = 0
    remaining_kWh = kWh
    for rate, threshold in zip(rates, thresholds):
        if remaining_kWh > threshold:
            cost += threshold * rate
            remaining_kWh -= threshold
        else:
            cost += remaining_kWh * rate
            break
    return cost

# Calculate and display the cost for each supplier
if st.button("Calculate"):
    results = []
    for supplier, data in suppliers.items():
        cost = calculate_cost(kWh_usage, data["rates"], data["thresholds"])
        results.append({"Supplier": supplier, "Cost (MYR)": cost})
    
    results_df = pd.DataFrame(results)
    st.write(results_df)

