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

with st.sidebar:
    st.write("""<p class="custom-nav-item">Contact Me</ap>""", unsafe_allow_html=True)
    st.write("""<a href="mailto:joeying0712@gmail.com" class="custom-nav-item">📧 Email</a>""", unsafe_allow_html=True)
    st.write("""<a href="https://www.linkedin.com/in/laujoeying/" class="custom-nav-item">💼 LinkedIn Profile</a>""", unsafe_allow_html=True)

# Add custom CSS for fixed table width and custom table styling
st.markdown("""
<style>
    .fixed-table {
        width: 50%;  /* Adjust the width as needed */
        margin-left: auto;
        margin-right: auto;
    }
    .custom-dataframe {
        background-color: white;
    }
    .custom-table {
        background-color: white;
        border-collapse: collapse;
        margin: 5px 0;  /* Adjusted margin to reduce spacing */
        font-size: 0.8em;
        font-family: 'Playwrite DE Grund', cursive;
        min-width: 830px;
        max-width: 830px;
    }
    .custom-table th,
    .custom-table td {
        padding: 8px 10px;
    }
    .custom-table thead tr {
        background-color: #009879;
        color: #ffffff;
        text-align: left;
    }
    .custom-table tbody tr {
        border-bottom: 1px solid #dddddd;
    }
    .custom-table tbody tr:nth-of-type(even) {
        background-color: #f3f3f3;
    }
    .custom-table tbody tr:last-of-type {
        border-bottom: 2px solid #009879;
    }
    .custom-table tbody tr.active-row {
        font-weight: bold;
        color: #009879;
    }
</style>
""", unsafe_allow_html=True)

# Streamlit app layout
st.markdown("<h1 class='custom-title'>Energy Cost Calculator</h1>", unsafe_allow_html=True)
st.markdown("<div class='rainbow' style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

st.info(
        """
        This calculator is only a guide and based on normal billing cycle.
        This bill calculation is meant to calculate energy consumption only, and does not include other charges such as 1% late payment, Power Factor surcharge, Connected Load Charge (CLC) penalty etc.
        This calculation does not take into account rebates, discounts, or special tariff incentives such as Off Peak Tariff Ride (OPTR), Sunday Tariff Rider (STR) etc*
        """
    )


# User inputs for kWh usage
if 'kWh_usage' not in st.session_state:
    st.session_state.kWh_usage = 0.0

kWh_usage = st.number_input("Enter your energy consumption in kWh:", min_value=0.0, format="%.2f", value=st.session_state.kWh_usage)

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

# Function to calculate cost with detailed steps
def calculate_cost(kWh, rates, thresholds):
    cost = 0
    remaining_kWh = kWh
    steps = []
    for rate, threshold in zip(rates, thresholds):
        if remaining_kWh > threshold:
            step_cost = threshold * rate
            cost += step_cost
            steps.append(f"{threshold:.1f} kWh * {rate:.3f} MYR = {step_cost:.2f} MYR")
            remaining_kWh -= threshold
        else:
            step_cost = remaining_kWh * rate
            cost += step_cost
            steps.append(f"{remaining_kWh:.1f} kWh * {rate:.3f} MYR = {step_cost:.2f} MYR")
            break
    return cost, steps

# Cache the calculation
@st.cache_data
def get_costs(kWh_usage):
    results = []
    for supplier, data in suppliers.items():
        cost, steps = calculate_cost(kWh_usage, data["rates"], data["thresholds"])
        results.append({"Supplier": supplier, "Cost (MYR)": cost, "Steps": steps})
    return pd.DataFrame(results)

# Calculate and display the cost for each supplier
if st.button("Calculate"):
    st.session_state.kWh_usage = kWh_usage  # Save the input value in session state
    results_df = get_costs(kWh_usage)
    
    st.markdown("<div class='fixed-table'>", unsafe_allow_html=True)
    st.write(f"Energy Consumption: {st.session_state.kWh_usage} kWh")
    st.dataframe(results_df[["Supplier", "Cost (MYR)"]].style.format({"Cost (MYR)": "{:.2f}"}).set_table_attributes('class="custom-dataframe"'))
    st.markdown("</div>", unsafe_allow_html=True)

    for index, row in results_df.iterrows():
        st.write(f"**{row['Supplier']}**")
        calculation_df = pd.DataFrame({"Calculation Steps": row["Steps"]})
        st.markdown("<div class='fixed-table'>", unsafe_allow_html=True)
        st.markdown(calculation_df.to_html(index=False, classes="custom-table"), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    