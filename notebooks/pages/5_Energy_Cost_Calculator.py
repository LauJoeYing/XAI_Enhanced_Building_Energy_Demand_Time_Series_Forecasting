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

# Add custom CSS for fixed table width
st.markdown("""
<style>
    .fixed-table {
        width: 50%;  /* Adjust the width as needed */
        margin-left: auto;
        margin-right: auto;
    }
</style>
""", unsafe_allow_html=True)

# Streamlit app layout
st.markdown("<p class='custom-chatbot-title'>Energy Cost Calculator</p>", unsafe_allow_html=True)
st.markdown("<div class='rainbow' style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

# User inputs for kWh usage
@st.cache_data
def get_usage(self):
    kWh_usage = st.number_input("Enter your energy consumption in kWh:", min_value=0.0, format="%.2f")
    return kWh_usage

# Energy suppliers and their rates
suppliers = {
    "TNB (Residential)": {
        "rates": [0.218, 0.334, 0.516, 0.546, 0.571],
        "thresholds": [200, 100, 300, 300, float('inf')]
    },
    "TNB (Industrial)": {
        "rates": [0.365, 0.385, 0.395],
        "thresholds": [200, 200, float('inf')]
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

# Cache the calculation
@st.cache_data
def get_costs(kWh_usage):
    results = []
    for supplier, data in suppliers.items():
        cost = calculate_cost(kWh_usage, data["rates"], data["thresholds"])
        results.append({"Supplier": supplier, "Cost (MYR)": cost})
    return pd.DataFrame(results)

# Calculate and display the cost for each supplier
if st.button("Calculate"):
    results_df = get_costs(kWh_usage)
    st.markdown("<div class='fixed-table'>", unsafe_allow_html=True)
    st.write(results_df)
    st.markdown("</div>", unsafe_allow_html=True)

    st.info(
        """
        This calculator is only a guide and based on normal billing cycle.
        This bill calculation is meant to calculate energy consumption only, and does not include other charges such as 1% late payment, Power Factor surcharge, Connected Load Charge (CLC) penalty etc.
        This calculation does not take into account rebates, discounts, or special tariff incentives such as Off Peak Tariff Ride (OPTR), Sunday Tariff Rider (STR) etc*
        """
    )
