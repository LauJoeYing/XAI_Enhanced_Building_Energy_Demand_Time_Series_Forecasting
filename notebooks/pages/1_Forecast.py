import streamlit as st
from pathlib import Path
import numpy as np
import tensorflow as tf
from joblib import load
import plotly.express as px
from joblib import load
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

 # Set Streamlit layout to wide
st.set_page_config(layout="wide")

# Load custom CSS
base_path = Path(__file__).parent
stylesheet_file_path = (base_path / "../stylesheets/style.css").resolve()
with open(stylesheet_file_path) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Define the expected input shape
time_steps = 6  
expected_feature_count = 12  

# Cache the data loading function to avoid reloading the dataset multiple times
@st.cache_data
def load_data(path, nrows=None):
    return pd.read_csv(path, nrows=nrows)

# Load a smaller subset of the data for demonstration purposes
data_path = (base_path / "../filtered_data.csv").resolve()
df = load_data(data_path, nrows=8000) 

top_building_ids = df['building_id'].unique().tolist()

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
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("<div class='rainbow'></div>", unsafe_allow_html=True)

# Add subheading mentioning supervisor and second marker
st.markdown("<h2 class='subheading'>Supervised by Dr. Preethi Subramanian | Second Marker: Assoc. Prof. Dr. Imran Medi</h2>", unsafe_allow_html=True)

# Create two columns
col1, col2 = st.columns(2, gap="medium")

with col1:
    # Input fields in the left column
    st.markdown("<h2 class='header playwrite-de-grund-regular'>Input Features</h2>", unsafe_allow_html=True)
    st.selectbox("Building ID", top_building_ids)
    square_feet = st.number_input("Square Feet", value=0.0, format="%.1f")
    month = st.number_input("Month", value=1, min_value=1, max_value=12)
    hour = st.number_input("Hour", value=0, min_value=0, max_value=23)
    day = st.number_input("Day", value=1, min_value=1, max_value=31)
    season = st.number_input("Season", value=0, min_value=0, max_value=3)
    weekend = st.number_input("Weekend", value=0, min_value=0, max_value=1)
    day_of_the_week = st.number_input("Day of the Week", value=0, min_value=0, max_value=6)
    air_temperature = st.number_input("Air Temperature", value=0.0, format="%.1f")
    dew_temperature = st.number_input("Dew Temperature", value=0.0, format="%.1f")
    sea_level_pressure = st.number_input("Sea Level Pressure", value=0.0, format="%.1f")
    wind_direction = st.number_input("Wind Direction", value=0.0, format="%.1f")
    wind_speed = st.number_input("Wind Speed", value=0.0, format="%.1f")

with col2:
    # Output fields in the right column   
    st.markdown("<h2 class='header playwrite-de-grund-regular'>Output</h2>", unsafe_allow_html=True)
    if st.button("Predict"):
        st.toast("Predicting...")

        # Load the Transformer model
        transformer_model = tf.keras.models.load_model('D:/Downloads/final-year-project/notebooks/models/Transformer_ADAM')

        # Load the scaler
        scaler_path = (base_path / "../scaler.joblib").resolve()
        scaler = load(scaler_path)

        # Define the function used in the explainer
        def model_predict(data):
            # Reshape data to (batch_size, time_steps, features)
            data_reshaped = data.reshape((-1, time_steps, expected_feature_count))
            return transformer_model.predict(data_reshaped).flatten()

        # Load the saved explainer
        explainer_path = (base_path / "../XAI_Explainer/mean_explainer.joblib").resolve()
        explainer = load(explainer_path)
        
        # Define the numerical and date pipelines
        numerical_pipeline = Pipeline([ 
            ('scaler', scaler)
        ])

        num_attribs = ['air_temperature','dew_temperature','sea_level_pressure','wind_direction','wind_speed', 'square_feet']
        date_attribs = ['day', 'month', 'hour', 'day_of_the_week', 'season', 'weekend']

        full_pipeline = ColumnTransformer([ 
            ("num", numerical_pipeline, num_attribs),
            ("date", "passthrough", date_attribs),
        ])

        # Generate prediction based on input
        input_data = pd.DataFrame({
            'square_feet': [float(square_feet)],
            'air_temperature': [float(air_temperature)],
            'dew_temperature': [float(dew_temperature)],
            'sea_level_pressure': [float(sea_level_pressure)],
            'wind_direction': [float(wind_direction)],
            'wind_speed': [float(wind_speed)],
            'day': [day],
            'month': [month],
            'hour': [hour],
            'day_of_the_week': [day_of_the_week],
            'season': [season],
            'weekend': [weekend]
        })

        # Apply transformation pipeline to input data
        input_data_transformed = full_pipeline.fit_transform(input_data)
        st.write(f"Transformed Data: {input_data_transformed}") # Ensure to fit_transform on input data

        # Repeat input_data to match time steps expected by the model
        input_data_transformed = np.repeat(input_data_transformed, time_steps, axis=0).reshape((1, time_steps, -1))

        # Generate prediction
        prediction_scaled = transformer_model.predict(input_data_transformed).flatten()[0]
        st.write(f"Scaled Prediction: {prediction_scaled}")

        min_meter_reading = scaler.data_min_[0]
        max_meter_reading = scaler.data_max_[0]
        st.write(f"Min Value: {min_meter_reading}")
        st.write(f"Max Value: {max_meter_reading}")

        # Convert the prediction back to the original scale
        prediction_original = prediction_scaled * (max_meter_reading - min_meter_reading) + min_meter_reading
        st.write(f"Actual Prediction: {prediction_original}")

        st.toast("Generating XAI SHAP Values...")

        # Generate SHAP values for the selected instances
        input_data_for_shap = input_data_transformed.reshape((1, -1))
        shap_values = explainer.shap_values(input_data_for_shap)
        if isinstance(shap_values, list):
            shap_values = shap_values[0]

        # # Reshape SHAP values to original time-series format
        shap_values_reshaped = np.array(shap_values).reshape(1, time_steps, expected_feature_count)

        # # Mean of Absolute Values across time steps
        shap_values_mean_abs = np.mean(np.abs(shap_values_reshaped), axis=1)

        # # Filter out features with mean SHAP value of 0 before aggregation
        shap_values_filtered = shap_values_mean_abs[:, np.mean(np.abs(shap_values_mean_abs), axis=0) != 0]

        # # Aggregate the mean absolute SHAP values across all instances
        shap_values_mean_abs_aggregated = np.mean(shap_values_filtered, axis=0)

        # # Create a DataFrame to display SHAP values
        feature_columns_filtered = np.array([
            'air_temperature', 'square_feet', 'dew_temperature', 
            'sea_level_pressure', 'wind_direction', 'wind_speed', 
            'day', 'month', 'hour', 'day_of_the_week', 'season', 'weekend'
        ])[np.mean(np.abs(shap_values_mean_abs), axis=0) != 0]

        shap_values_df = pd.DataFrame(shap_values_mean_abs_aggregated, index=feature_columns_filtered, columns=['Mean Absolute SHAP Value'])

        # # Remove features with mean SHAP value of 0
        shap_values_df = shap_values_df[shap_values_df['Mean Absolute SHAP Value'] != 0]
        st.session_state.shap_values_df = shap_values_df
        st.write(shap_values_df)

        # # Plot SHAP summary with Plotly
        fig = px.bar(
            st.session_state.shap_values_df,
            x=st.session_state.shap_values_df.index,
            y='Mean Absolute SHAP Value',
            title='SHAP Summary Plot (Mean of Absolute Values)',
            text='Mean Absolute SHAP Value',
            color='Mean Absolute SHAP Value',
            color_continuous_scale='Turbo'
        )

        # # Update layout to show mean SHAP values on each bar
        fig.update_traces(texttemplate='%{text:.4f}', textposition='outside')
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

        st.plotly_chart(fig, use_container_width=True)
