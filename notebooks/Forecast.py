import streamlit as st
import streamlit_shadcn_ui as ui
import numpy as np
import tensorflow as tf
from joblib import load
import shap
import plotly.express as px
import pandas as pd
from sklearn.preprocessing import StandardScaler
import time
from PIL import Image

# Set Streamlit layout to wide
st.set_page_config(layout="wide")

# Load custom CSS
with open('D:/Downloads/final-year-project/notebooks/stylesheets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Define the expected input shape
time_steps = 6  # Adjust based on your model training
expected_feature_count = 12  # Adjust based on your model training

# Initialize session state for prediction result if not already done
if 'prediction' not in st.session_state:
    st.session_state.prediction = None

if 'shap_values_df' not in st.session_state:
    st.session_state.shap_values_df = None

# Define the input fields and output in columns
st.markdown(
    """
    <div style="text-align:center;position:relative;">
        <img src="https://lh3.googleusercontent.com/d/1oYttFfUcSt37Wojwuea-gW530BRZ0QIz" alt="windmill" style="position:absolute;left:-1rem;bottom:-2.5rem;width:400px;opacity:0.7;">
        <h1 class="title crimson-text-bold">XAI Enhanced Building Energy Demand Forecasting</h1>
        <img src="https://lh3.googleusercontent.com/d/1oYttFfUcSt37Wojwuea-gW530BRZ0QIz" alt="windmill" style="position:absolute;right:-1rem;bottom:-2.5rem;-webkit-transform:scaleX(-1);transform:scaleX(-1);width:400px;opacity:0.7">
    </div
    """,
    unsafe_allow_html=True
)
st.markdown("<div class='rainbow'></div>", unsafe_allow_html=True)

# Create two columns
col1, col2 = st.columns(2, gap="medium")

with col1:
    # Input fields in the left column
    st.markdown("<h2 class='header playwrite-de-grund-regular'>Input Features</h2>", unsafe_allow_html=True)
    air_temperature = st.number_input("Air Temperature", value=0.0, format="%.1f")
    building_id = st.number_input("Building ID", value=0, format="%d")
    cloud_coverage = st.number_input("Cloud Coverage", value=0.0, format="%.1f")
    dew_temperature = st.number_input("Dew Temperature", value=0.0, format="%.1f")
    precip_depth_1_hr = st.number_input("Precipitation in One Hour", value=0.0, format="%.1f")
    primary_use = st.number_input("Primary Use", value=0, format="%d")
    sea_level_pressure = st.number_input("Sea Level Pressure", value=0.0, format="%.1f")
    site_id = st.number_input("Site ID", value=0, format="%d")
    square_feet = st.number_input("Square Feet", value=0.0, format="%.1f")
    wind_direction = st.number_input("Wind Direction", value=0.0, format="%.1f")
    wind_speed = st.number_input("Wind Speed", value=0.0, format="%.1f")
    meter = st.number_input("Meter", value=0, format="%d")

with col2:
    # Output fields in the right column   
    st.markdown("<h2 class='header playwrite-de-grund-regular'>Output</h2>", unsafe_allow_html=True)
    if st.button("Predict"):
        st.toast("Predicting...")
        # Show progress bar once the button is clicked
        progress_bar = st.progress(0)

        # Load the Transformer model
        transformer_model = tf.keras.models.load_model('D:/Downloads/final-year-project/notebooks/models/Transformer_ADAM')

        # Define the function used in the explainer
        def model_predict(data):
            # Reshape data to (batch_size, time_steps, features)
            data_reshaped = data.reshape((-1, time_steps, expected_feature_count))
            return transformer_model.predict(data_reshaped).flatten()

        # Load the saved explainer
        explainer = load('D:/Downloads/final-year-project/notebooks/XAI_Explainer/mean_explainer.joblib')

        # Generate prediction based on input
        input_data = np.array([[air_temperature, building_id, cloud_coverage, dew_temperature, 
                                precip_depth_1_hr, primary_use, sea_level_pressure, site_id, 
                                square_feet, wind_direction, wind_speed, meter]])

        # Repeat input_data to match time steps expected by the model
        input_data = np.repeat(input_data, time_steps, axis=0).reshape((1, time_steps, -1))

        # Generate prediction
        prediction = transformer_model.predict(input_data).flatten()[0]
        st.session_state.prediction = prediction

        # Generate SHAP values for the selected instances
        shap_values = explainer.shap_values(input_data.reshape((1, -1)))
        if isinstance(shap_values, list):
            shap_values = shap_values[0]

        # Reshape SHAP values to original time-series format
        shap_values_reshaped = np.array(shap_values).reshape(1, time_steps, expected_feature_count)

        # Mean of Absolute Values across time steps
        shap_values_mean_abs = np.mean(np.abs(shap_values_reshaped), axis=1)

        # Filter out features with mean SHAP value of 0 before aggregation
        shap_values_filtered = shap_values_mean_abs[:, np.mean(np.abs(shap_values_mean_abs), axis=0) != 0]

        # Aggregate the mean absolute SHAP values across all instances
        shap_values_mean_abs_aggregated = np.mean(shap_values_filtered, axis=0)

        # Create a DataFrame to display SHAP values
        feature_columns_filtered = np.array([
            'air_temperature', 'building_id', 'cloud_coverage', 'dew_temperature', 
            'precip_depth_1_hr', 'primary_use', 'sea_level_pressure', 'site_id', 
            'square_feet', 'wind_direction', 'wind_speed', 'meter'])[np.mean(np.abs(shap_values_mean_abs), axis=0) != 0]

        shap_values_df = pd.DataFrame(shap_values_mean_abs_aggregated, index=feature_columns_filtered, columns=['Mean Absolute SHAP Value'])

        # Remove features with mean SHAP value of 0
        shap_values_df = shap_values_df[shap_values_df['Mean Absolute SHAP Value'] != 0]
        st.session_state.shap_values_df = shap_values_df

        # Update progress bar
        progress_bar.progress(100)

        st.balloons()
        st.toast("Prediction completed!")

    # Display the prediction and SHAP values if available in session state
    if st.session_state.prediction is not None:
        st.write(f"Predicted Energy Demand: {st.session_state.prediction}")

    if st.session_state.shap_values_df is not None:
        st.write(st.session_state.shap_values_df)

        # Plot SHAP summary with Plotly
        fig = px.bar(
            st.session_state.shap_values_df,
            x=st.session_state.shap_values_df.index,
            y='Mean Absolute SHAP Value',
            title='SHAP Summary Plot (Mean of Absolute Values)',
            text='Mean Absolute SHAP Value',
            color='Mean Absolute SHAP Value',
            color_continuous_scale='Turbo'
        )

        # Update layout to show mean SHAP values on each bar
        fig.update_traces(texttemplate='%{text:.4f}', textposition='outside')
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

        st.plotly_chart(fig, use_container_width=True)
