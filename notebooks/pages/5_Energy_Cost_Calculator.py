import streamlit as st
import pandas as pd
from pathlib import Path

# Set Streamlit layout to wide
st.set_page_config(layout="wide")

# Load custom CSS
base_path = Path(__file__).parent
stylesheet_file_path = (base_path / "../stylesheets/style.css").resolve()
with open(stylesheet_file_path) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Streamlit app layout
st.markdown("<p class='custom-chatbot-title'>Energy Cost Calculator</p>", unsafe_allow_html=True)
st.markdown("<div class='rainbow' style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

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

# Add notes reminder
st.markdown("""
<div style="margin-top: 2rem;">
    <h4>Notes:</h4>
    <ul>
        <li>This calculator is only a guide and based on normal billing cycle.</li>
        <li>This bill calculation is meant to calculate energy consumption only, and does not include other charges such as 1% late payment, 1.6% Kumpulan Wang Tenaga Boleh Baharu (RE Fund), Power Factor surcharge, Connected Load Charge (CLC) penalty etc.</li>
        <li>This calculation does not take into account rebates, discounts, or special tariff incentives such as Off Peak Tariff Ride (OPTR), Sunday Tariff Rider (STR) etc.</li>
    </ul>
</div>
""", unsafe_allow_html=True)
