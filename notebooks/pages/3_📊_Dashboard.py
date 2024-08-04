import streamlit as st
from pathlib import Path
import pandas as pd
from streamlit_vizzu import Data, Config, Style
from ipyvizzustory import Story, Slide, Step
import plotly.graph_objects as go

# Set Streamlit layout to wide
st.set_page_config(layout="wide")

# Load custom CSS
base_path = Path(__file__).parent
stylesheet_file_path = (base_path / "../stylesheets/style.css").resolve()
with open(stylesheet_file_path) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Define data types
d_types = {
    "Unnamed: 0": float,
    "building_id": str,
    "meter": str,
    "timestamp": str,
    "meter_reading": float,
    "site_id": str,
    "primary_use": str,
    "square_feet": float,
    "air_temperature": float,
    "cloud_coverage": float,
    "dew_temperature": float,
    "precip_depth_1_hr": float,
    "sea_level_pressure": float,
    "wind_direction": float,
    "wind_speed": float,
    "day": float,
    "month": str,
    "hour": float,
}

# Load dataset
@st.cache_data
def load_dataset(filepath, nrows=None):
    try:
        if nrows:
            df = pd.read_csv(filepath, nrows=nrows, dtype=d_types)
        else:
            df = pd.read_csv(filepath, dtype=d_types)
        return df
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return pd.DataFrame()

# Function to preprocess data
def preprocess_data(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['cloud_coverage'] = df['cloud_coverage'].astype(str)
    return df

def create_indicator_chart(value, title):
    fig = go.Figure(go.Indicator(
        mode = "number",
        value = value,
        title = {"text": title, 'font': {'size': 15, 'family': 'Georgia'}},
        number = {'font': {'size': 30, 'family': 'Cambria'}},
        domain = {'x': [0, 1], 'y': [0, 1]}
    ))

    fig.update_layout(
        paper_bgcolor='rgba(255, 255, 255, 0.4)',  # White background with 50% opacity
        plot_bgcolor='rgba(255, 255, 255, 0.4)',   # Plot area background with 50% opacity
        width=300, height=300
    )
    return fig

def create_story_one(filtered_df):
    data = Data()
    data.add_df(filtered_df)
    story_one = Story(data=data)
    story_one.set_size("100%", "600px")
    story_one.set_feature("tooltip", True)

    # Define the narrative with multiple slides
    # Slide 1: Overview of Meter Readings by Month
    slide1 = Slide(
        Step(
            Config(
                {
                    "x": ["month"],
                    "y": ["mean(meter_reading)"],
                    "color": "month",
                    "label": "mean(meter_reading)",
                    "title": "Overview: Mean Meter Readings by Month",
                }
            ),
            Style(
                {
                    "paddingLeft": "3em",
                    "plot": {
                        "paddingLeft": "1em",
                        "backgroundColor": "rgba(255, 255, 255, 0.5)",
                        "yAxis": {
                            "label": {
                                "numberScale": "shortScaleSymbolUS",
                                "color": "#000000",
                                "fontSize": "1.5em"
                            },
                            "title": {
                                "color": "#000000",
                                "paddingLeft": "5em",
                                "fontSize": "1.4em"
                            },
                        },
                        "xAxis": {
                            "label": {
                                "numberScale": "shortScaleSymbolUS",
                                "color": "#000000",
                                "fontSize": "1.7em"
                            },
                        },
                        "marker": {
                            "label": {
                                "numberFormat": "prefixed",
                                "maxFractionDigits": "1",
                                "numberScale": "shortScaleSymbolUS",
                                "color": "#000000",
                                "fontSize": "1.2em"
                            },
                            "rectangleSpacing": None,
                            "circleMinRadius": 0.005,
                            "borderOpacity": 1,
                            "colorPalette": "#FFB3BA #FFDFBA #FFFFBA #BAFFC9 #BAE1FF #CBAACB #FFDAC1 #FF9AA2 #B5EAD7 #E2F0CB #FFB7B2 #FFDAC1",
                        },
                    },
                    "fontFamily": "Georgia", 
                    "title": {
                        "color": "#000000",
                        "fontSize": "2.2em"
                    },
                    "subtitle": {
                        "color": "#000000",
                        "fontSize": "1.3em"
                    },
                }
            )
        )
    )
    story_one.add_slide(slide1)

    # Slide 2: Focus on High Consumption using meter reading >= 987.20
    slide2 = Slide(
        Step(
            Data.filter("record['meter_reading'] >= 987.20"),
            Config(
                {
                    "coordSystem": "cartesian",
                    "geometry": "circle",
                    "title": "High Consumption Meter Reading by Month with meter reading >= 987.20",
                    "x": "month",
                    "y": {
                        "set": "mean(meter_reading)",
                        "range": {"min": "auto", "max": "110%"},
                    },
                    "color": "month",
                    "lightness": None,
                    "size": None,
                    "noop": None,
                    "split": False,
                    "align": "none",
                    "orientation": "horizontal",
                    "label": "mean(meter_reading)",
                    "sort": "none",
                }
            ),
            Style(
                {
                    "plot": {
                        "backgroundColor": "rgba(255, 255, 255, 0.5)",
                        "yAxis": {
                            "label": {
                                "numberScale": "shortScaleSymbolUS",
                                "fontSize": "0.9em"
                            }
                        },
                        "xAxis": {
                            "label": {
                                "numberScale": "shortScaleSymbolUS",
                                "fontSize": "0.9em"
                            }
                        },
                        "marker": {
                            "label": {
                                "numberFormat": "prefixed",
                                "maxFractionDigits": "1",
                                "numberScale": "shortScaleSymbolUS",
                                "fontSize": "0.85em"
                            },
                            "rectangleSpacing": 0,
                            "circleMinRadius": 0.02,
                            "borderOpacity": 1,
                            "colorPalette": "#FFB3BA #FFDFBA #FFFFBA #BAFFC9 #BAE1FF #CBAACB #FFDAC1 #FF9AA2 #B5EAD7 #E2F0CB #FFB7B2 #FFDAC1",
                            "guides": {
                                "color": "#A9A9A9",
                                "lineWidth": 5,
                            },
                        },
                    },
                    "fontFamily": "Georgia",
                    "title": {
                        "color": "#000000",
                        "fontSize": "0.9em"
                    },
                }
            )
        )
    )
    story_one.add_slide(slide2)
    return story_one

def create_story_two(filtered_df):
    data = Data()
    data.add_df(filtered_df)
    story_two = Story(data=data)
    story_two.set_size("100%", "600px")
    story_two.set_feature("tooltip", True)

    # Slide 1: Overview of Meter Readings by Cloud Coverage
    slide1 = Slide(
        Step(
            Config(
                {
                    "coordSystem": "polar",
                    "geometry": "rectangle",
                    "x": ["cloud_coverage", "mean(meter_reading)"],
                    "y": {"set": None, "range": {"min": "auto", "max": "auto"}},
                    "color": "cloud_coverage",
                    "title": "Cloud Coverage by Meter Reading",
                    "lightness": None,
                    "size": None,
                    "noop": None,
                    "split": False,
                    "align": "none",
                    "orientation": "vertical",
                    "label": None,
                    "sort": "none",
                }
            ),
            Style(
                {
                    "plot": {
                        "yAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                        "xAxis": {"label": {"numberScale": "shortScaleSymbolUS"}, "title": { "color": "#000000" }},
                        "marker": {
                            "label": {
                                "numberFormat": "prefixed",
                                "maxFractionDigits": "1",
                                "numberScale": "shortScaleSymbolUS",
                            },
                            "rectangleSpacing": None,
                            "circleMinRadius": 0.005,
                            "borderOpacity": 1,
                            "colorPalette": "#FFB3BA #FFDFBA #FFFFBA #BAFFC9 #BAE1FF #CBAACB #FFDAC1 #FF9AA2 #B5EAD7 #E2F0CB #FFB7B2 #FFDAC1",
                        },
                    },
                    "fontFamily": "Georgia",
                    "legend": {
                        "label": {
                            "color": "#000000",
                            "fontSize": "1.5em"
                        },
                    }
                }
            )
        )
    )
    
    story_two.add_slide(slide1)

    # Slide 2: Focus on High Consumption using meter reading >= 987.20
    slide2 = Slide(
        Step(
            Data.filter("record['meter_reading'] >= 987.20"),
            Config(
                {
                    "coordSystem": "polar",
                    "geometry": "rectangle",
                    "x": ["cloud_coverage", "mean(meter_reading)"],
                    "y": {"set": None, "range": {"min": "-200%", "max": "100%"}},
                    "color": "cloud_coverage",
                    "title": "Cloud Coverage by Meter Reading",
                    "lightness": None,
                    "size": None,
                    "noop": None,
                    "split": False,
                    "align": "none",
                    "orientation": "vertical",
                    "label": None,
                    "sort": "none",
                }
            ),
            Style(
                {
                    "plot": {
                        "backgroundColor": "rgba(255, 255, 255, 0.5)",
                        "yAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                        "xAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                        "marker": {
                            "label": {
                                "numberFormat": "prefixed",
                                "maxFractionDigits": "1",
                                "numberScale": "shortScaleSymbolUS",
                            },
                            "rectangleSpacing": None,
                            "circleMinRadius": 0.005,
                            "borderOpacity": 1,
                            "colorPalette": "#FFB3BA #FFDFBA #FFFFBA #BAFFC9 #BAE1FF #CBAACB #FFDAC1 #FF9AA2 #B5EAD7 #E2F0CB #FFB7B2 #FFDAC1",
                        },
                    },
                    "fontFamily": "Georgia",
                    "title": {
                        "color": "#000000",
                        "fontSize": "1.6em"
                    },
                }
            ),
        )
    )

    story_two.add_slide(slide2)

    return story_two

def create_story_three(filtered_df):
    data = Data()
    data.add_df(filtered_df)
    story_three = Story(data=data)
    story_three.set_size("100%", "600px")
    story_three.set_feature("tooltip", True)

    slide1 = Slide(
        Step(
            Config(
                {
                    "coordSystem": "polar",
                    "geometry": "rectangle",
                    "x": "wind_direction_binned",
                    "y": {
                        "set": "mean(meter_reading)",
                        "range": {"min": "auto", "max": "auto"},
                    },
                    "color": None,
                    "lightness": None,
                    "size": None,
                    "noop": None,
                    "split": False,
                    "align": "none",
                    "orientation": "horizontal",
                    "label": None,
                    "sort": "none",
                    "title" : "Meter Reading by Wind Direction",
                }
            ),
            Style(
                {
                    "plot": {
                        "paddingLeft": "3em",
                        "yAxis": {
                            "label": {
                                "numberScale": "shortScaleSymbolUS",
                            },
                            "title": {
                                "color": "#000000"
                            },
                        },
                        "xAxis": {
                            "label": {
                                "numberScale": "shortScaleSymbolUS",
                                "color": "#000000",
                            },
                        },
                        "marker": {
                            "label": {
                                "numberFormat": "prefixed",
                                "maxFractionDigits": "1",
                                "numberScale": "shortScaleSymbolUS",
                            },
                            "rectangleSpacing": None,
                            "circleMinRadius": 0.005,
                            "borderOpacity": 1,
                            "colorPalette": "#C3B1E1",
                        },
                    },
                    "fontFamily": "Georgia",
                    "legend": {
                        "label": {
                            "color": "#000000",
                        },
                    "title": {
                        "color": "#000000",
                        "fontSize": "2.0em"
                    },
                    }
                }
            ),
        )
    )
    story_three.add_slide(slide1)

    slide2 = Slide(
        Step(
            Config(
                {
                    "coordSystem": "cartesian",
                    "geometry": "circle",
                    "x": None,
                    "y": {"set": None, "range": {"min": "auto", "max": "auto"}},
                    "color": "wind_speed_binned",
                    "lightness": None,
                    "size": ["wind_speed", "mean(meter_reading)"],
                    "noop": None,
                    "split": False,
                    "align": "none",
                    "orientation": "horizontal",
                    "label": None,
                    "sort": "none",
                    "title": "Meter Reading by Wind Speed",
                }
            ),
            Style(
                {
                    "plot": {
                        "yAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                        "xAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                        "marker": {
                            "label": {
                                "numberFormat": "prefixed",
                                "maxFractionDigits": "1",
                                "numberScale": "shortScaleSymbolUS",
                            },
                            "rectangleSpacing": None,
                            "circleMinRadius": 0.005,
                            "borderOpacity": 1,
                            "colorPalette": "#FADADD #FFB7B2 #FFDAC1 #FFEBBB #FFFFD1 #D4EFDF #B5EAD7 #C9C9FF #FDFD96 #BFD6FF #E6E6FA",
                        },
                    },
                    "fontFamily": "Georgia",
                    "title": {
                        "color": "#000000",
                        "fontSize": "1.2em"
                    },
                }
            ),
        )
    )
    story_three.add_slide(slide2)

    return story_three

def create_story_four(filtered_df):
    data = Data()
    data.add_df(filtered_df)
    story_four = Story(data=data)
    story_four.set_size("100%", "600px")
    story_four.set_feature("tooltip", True)

    # Slide 1: Overview of Meter Readings by Day
    slide1 = Slide(
        Step(
            Config(
                {
                    "coordSystem": "polar",
                    "geometry": "rectangle",
                    "x": "mean(meter_reading)",
                    "y": {"set": "day_binned", "range": {"min": "-50%", "max": "auto"}},
                    "color": None,
                    "lightness": None,
                    "size": None,
                    "noop": None,
                    "split": False,
                    "align": "none",
                    "orientation": "vertical",
                    "label": None,
                    "sort": "none",
                    "title": "Meter Reading by Hour",
                }
            ),
            Style(
                {
                    "plot": {
                        "yAxis": {
                            "label": {
                                "numberScale": "shortScaleSymbolUS",
                                "color": "#000000",
                            },
                            "title": {
                                "color": "#000000",
                            },
                        },
                        "xAxis": {
                            "label": {
                                "numberScale": "shortScaleSymbolUS",
                                "color": "#000000",
                            },
                            "title": {
                                "color": "#000000",
                            },
                        },
                        "marker": {
                            "label": {
                                "numberFormat": "prefixed",
                                "maxFractionDigits": "1",
                                "numberScale": "shortScaleSymbolUS",
                            },
                            "rectangleSpacing": None,
                            "circleMinRadius": 0.005,
                            "borderOpacity": 1,
                            "colorPalette": "#C1E1C1",
                        },
                    },
                    "fontFamily": "Georgia",
                    "title": {
                        "color": "#000000",
                        "fontSize": "2.2em"
                    },
                }
            ),
        )
    )

    story_four.add_slide(slide1)

    slide2 = Slide(
        Step(
            Data.filter(None),
            Config(
                {
                    "coordSystem": "polar",
                    "geometry": "rectangle",
                    "x": "hour_binned",
                    "y": {
                        "set": "mean(meter_reading)",
                        "range": {"min": "auto", "max": "auto"},
                    },
                    "color": None,
                    "lightness": None,
                    "size": None,
                    "noop": None,
                    "split": False,
                    "align": "none",
                    "orientation": "horizontal",
                    "label": None,
                    "sort": "none",
                    "title": "Meter Reading by Day",
                }
            ),
            Style(
                {
                    "plot": {
                        "yAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                        "xAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                        "marker": {
                            "label": {
                                "numberFormat": "prefixed",
                                "maxFractionDigits": "1",
                                "numberScale": "shortScaleSymbolUS",
                            },
                            "rectangleSpacing": None,
                            "circleMinRadius": 0.005,
                            "borderOpacity": 1,
                            "colorPalette": "#C1E1C1",
                        },
                    },
                    "fontFamily": "Georgia",
                    "title": {
                        "color": "#000000",
                        "fontSize": "1.2em"
                    },
                }
            ),
        )
    )

    story_four.add_slide(slide2)
    return story_four

def create_story_five(filtered_df):
    data = Data()
    data.add_df(filtered_df)
    story_five = Story(data=data)
    story_five.set_size("100%", "600px")
    story_five.set_feature("tooltip", True)

    # Slide 1: Overview of Meter Readings by Day
    slide1 = Slide(
        Step(
            Config(
                {
                    "coordSystem": "polar",
                    "geometry": "rectangle",
                    "x": ["meter", "mean(meter_reading)"],
                    "y": {"set": None, "range": {"min": "-200%", "max": "100%"}},
                    "color": "meter",
                    "lightness": None,
                    "size": None,
                    "noop": None,
                    "split": False,
                    "align": "none",
                    "orientation": "vertical",
                    "label": None,
                    "sort": "none",
                    "title": "Meter Reading by Meter Type",
               }
            ),
            Style(
                {
                    "plot": {
                        "yAxis": {
                            "label": {
                                "numberScale": "shortScaleSymbolUS",
                                "color": "#000000",
                            },
                            "title": {
                                "color": "#000000",
                            },
                        },
                        "xAxis": {
                            "label": {
                                "numberScale": "shortScaleSymbolUS",
                                "color": "#000000",
                            },
                            "title": {
                                "color": "#000000",
                            },
                        },
                        "marker": {
                            "label": {
                                "numberFormat": "prefixed",
                                "maxFractionDigits": "1",
                                "numberScale": "shortScaleSymbolUS",
                                "fontSize": "1.2em"
                            },
                            "rectangleSpacing": None,
                            "circleMinRadius": 0.005,
                            "borderOpacity": 1,
                            "colorPalette": "#f7e7b4 #ffb3ba",
                        },
                    },
                    "fontFamily": "Georgia",
                    "legend": {
                        "label": {
                            "color": "#000000",
                            "fontSize": "1.0em"
                        }
                    },
                }
            ),
        )
    )
    story_five.add_slide(slide1)

    slide2 = Slide(
        Step(
            Config(
                {
                    "coordSystem": "cartesian",
                    "geometry": "rectangle",
                    "x": "primary_use",
                    "y": {
                        "set": "mean(meter_reading)",
                        "range": {"min": "auto", "max": "110%"},
                    },
                    "color": None,
                    "lightness": None,
                    "size": None,
                    "noop": None,
                    "split": False,
                    "align": "none",
                    "orientation": "horizontal",
                    "label": None,
                    "sort": "none",
                    "title": "Meter Reading by Primary Use",
                }
            ),
            Style(
                {
                    "plot": {
                        "paddingLeft": "3em",
                        "yAxis": {
                            "label": {
                                "numberScale": "shortScaleSymbolUS"
                            },
                            "title": {
                                "paddingLeft": "5em",
                            },
                        },
                        "xAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                        "marker": {
                            "label": {
                                "numberFormat": "prefixed",
                                "maxFractionDigits": "1",
                                "numberScale": "shortScaleSymbolUS",
                            },
                            "rectangleSpacing": None,
                            "circleMinRadius": 0.005,
                            "borderOpacity": 1,
                            "colorPalette": "#FFB3BA #FFDFBA #FFFFBA #BAFFC9 #BAE1FF #CBAACB #FFDAC1 #FF9AA2 #B5EAD7 #E2F0CB #FFB7B2 #FFDAC1",
                        },
                    },
                    "fontFamily": "Georgia",
                    "title": {
                        "color": "#000000",
                        "fontSize": "1.2em"
                    },
                }
            ),
        )
    )
    story_five.add_slide(slide2)
    
    return story_five

def create_story_six(filtered_df):
    data = Data()
    data.add_df(filtered_df)
    story_six = Story(data=data)
    story_six.set_size("100%", "600px")
    story_six.set_feature("tooltip", True)

    # Slide 1: Overview of Meter Readings by Day
    slide1 = Slide(
        Step(
            Config(
                {
                    "coordSystem": "cartesian",
                    "geometry": "area",
                    "x": "air_temperature_binned",
                    "y": {
                        "set": "mean(meter_reading)",
                        "range": {"min": "auto", "max": "110%"},
                    },
                    "color": None,
                    "lightness": None,
                    "size": None,
                    "noop": None,
                    "split": False,
                    "align": "none",
                    "orientation": "horizontal",
                    "label": None,
                    "sort": "none",
                    "title": "Meter Reading by Air Temperature",
                }
            ),
            Style(
                {
                    "plot": {
                        "paddingLeft": "3em",
                        "yAxis": {
                            "label": {
                                "numberScale": "shortScaleSymbolUS",
                                "color": "#000000",
                            },
                            "title": {
                                "color": "#000000",
                                "paddingLeft": "5em",
                            },
                        },
                        "xAxis": {
                            "label": {
                                "numberScale": "shortScaleSymbolUS",
                                "color": "#000000",
                            },
                            "title": {
                                "color": "#000000",
                            },
                        },
                        "marker": {
                            "label": {
                                "numberFormat": "prefixed",
                                "maxFractionDigits": "1",
                                "numberScale": "shortScaleSymbolUS",
                            },
                            "rectangleSpacing": None,
                            "circleMinRadius": 0.005,
                            "borderOpacity": 1,
                            "colorPalette": "#AEC6CF",
                        },
                    },
                    "fontFamily": "Georgia",
                }
            ),
        )
    )
    story_six.add_slide(slide1)

    slide2 = Slide(
        Step(
            Config(
                {
                    "coordSystem": "cartesian",
                    "geometry": "rectangle",
                    "x": "dew_temperature_binned",
                    "y": {
                        "set": "mean(meter_reading)",
                        "range": {"min": "auto", "max": "110%"},
                    },
                    "color": None,
                    "lightness": None,
                    "size": None,
                    "noop": None,
                    "split": False,
                    "align": "none",
                    "orientation": "horizontal",
                    "label": None,
                    "sort": "none",
                    "title": "Meter Reading by Dew Temperature",
                }
            ),
            Style(
                {
                    "plot": {
                        "yAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                        "xAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                        "marker": {
                            "label": {
                                "numberFormat": "prefixed",
                                "maxFractionDigits": "1",
                                "numberScale": "shortScaleSymbolUS",
                            },
                            "rectangleSpacing": None,
                            "circleMinRadius": 0.005,
                            "borderOpacity": 1,
                            "colorPalette": "#AEC6CF",
                        },
                    },
                    "fontFamily": "Georgia",
                    "title": {
                        "color": "#000000",
                        "fontSize": "1.2em"
                    },
                }
            ),
        )
    )
    story_six.add_slide(slide2)
    return story_six


def create_story_seven(filtered_df):
    data = Data()
    
    # Get top 15 highest mean meter_reading by square_feet_binned
    top_15_df = filtered_df.groupby('square_feet_binned').mean().nlargest(15, 'meter_reading').reset_index()
    
    data.add_df(top_15_df)
    story_seven = Story(data=data)
    story_seven.set_size("100%", "600px")
    story_seven.set_feature("tooltip", True)

    slide1 = Slide(
        Step(
            Config(
                {
                    "coordSystem": "cartesian",
                    "geometry": "rectangle",
                    "x": None,
                    "y": {"set": None, "range": {"min": "auto", "max": "auto"}},
                    "color": "square_feet_binned",
                    "lightness": None,
                    "size": ["square_feet_binned", "mean(meter_reading)"],
                    "noop": None,
                    "split": False,
                    "align": "none",
                    "orientation": "horizontal",
                    "label": "square_feet_binned",
                    "sort": "none",
                    "title": "Meter Reading by Square Feet",
                }
            ),
            Style(
                {
                    "plot": {
                        "yAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                        "xAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                        "marker": {
                            "label": {
                                "numberFormat": "prefixed",
                                "maxFractionDigits": "1",
                                "numberScale": "shortScaleSymbolUS",
                                "fontSize": "1.2em"
                            },
                            "rectangleSpacing": None,
                            "circleMinRadius": 0.005,
                            "borderOpacity": 1,
                            "colorPalette": "#A3B1E1 #77D9A8 #FFAB76 #FFE29E #E0B982 #D6C0AE #FF9DAA #D9E97B #B1A05C #FFB591 #CE91CB #FFCAF7 #D997B7 #C9A4FF #D1A8D8 #A2C4FF #96A5D9 #BEC4C4 #D4C6A9 #9DC7B1 #D9C6A9 #A5D0B5 #8BC5A3 #CE97A6 #E2A1C8 #FF9E99",
                        },
                    },
                    "fontFamily": "Georgia",
                    "legend": {
                        "paddingLeft": "0.2em",
                        "label": {
                            "color": "#000000",
                            "fontSize": "1.7em"
                        },
                        "title": {
                            "color": "#000000",
                        }
                    },
                }
            ),
        )
    )
    story_seven.add_slide(slide1)
    return story_seven


def create_story_eight(filtered_df):
    data = Data()
    data.add_df(filtered_df)
    story_eight = Story(data=data)
    story_eight.set_size("100%", "600px")
    story_eight.set_feature("tooltip", True)

    slide1 = Slide(
        Step(
            Config(
                {
                    "coordSystem": "cartesian",
                    "geometry": "circle",
                    "x": {
                        "set": "mean(meter_reading)",
                        "range": {"min": "auto", "max": "110%"},
                    },
                    "y": "precip_depth_1_hr_binned",
                    "color": "precip_depth_1_hr_binned",
                    "lightness": None,
                    "size": None,
                    "noop": None,
                    "split": False,
                    "align": "none",
                    "orientation": "vertical",
                    "label": None,
                    "sort": "none",
                    "title": "Meter Reading by Precipitation (1 hr)",
                }
            ),
            Style(
                {
                    "plot": {
                        "yAxis": {
                            "label": {
                                "numberScale": "shortScaleSymbolUS",
                                "color": "#000000",
                            },
                            "title": {
                                "color": "#000000",
                            },
                        },
                        "xAxis": {
                            "label": {
                                "numberScale": "shortScaleSymbolUS",
                                "color": "#000000",
                            },
                            "title": {
                                "color": "#000000",
                            },
                        },
                        "marker": {
                            "label": {
                                "numberFormat": "prefixed",
                                "maxFractionDigits": "1",
                                "numberScale": "shortScaleSymbolUS",
                            },
                            "rectangleSpacing": 0,
                            "circleMinRadius": 0.02,
                            "borderOpacity": 1,
                            "colorPalette": "#FFB3BA #FFDFBA #FFFFBA #BAFFC9 #BAE1FF #CBAACB #FFDAC1 #FF9AA2 #B5EAD7 #E2F0CB #FFB7B2 #FFDAC1",
                            "guides": {
                                "color": "#A9A9A9",
                                "lineWidth": 5,
                            },
                        },
                    },
                    "fontFamily": "Georgia",
                }
            ),
        )
    )
    story_eight.add_slide(slide1)
    return story_eight


def create_donut_chart(high_consumption_percentage, low_consumption_percentage):
    fig = go.Figure(data=[go.Pie(
        labels=['High Consumption', 'Low Consumption'],
        values=[high_consumption_percentage, low_consumption_percentage],
        hole=.6,
        marker_colors=['#FAA0A0', '#DAFFE7'],
        textinfo='none'
    )])

    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(
                family="Georgia",
                size=12,
                color="black"
            )
        ),
        annotations=[dict(text=f'{high_consumption_percentage:.1f}%', x=0.18, y=0.5, font_size=15, showarrow=False, font=dict(family="Georgia")),
                     dict(text=f'{low_consumption_percentage:.1f}%', x=0.82, y=0.5, font_size=15, showarrow=False, font=dict(family="Georgia"))],
        margin=dict(l=20, r=20, t=20, b=10),  # Smaller size
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot area
        width=300,
        height=300
    )

    return fig

# Load a subset of the dataset to avoid memory issues
file_path = (base_path / "../../data/dashboard_data.csv").resolve()
df = load_dataset(file_path)  # Load data
if df.empty:
    st.error("The dataset is empty or could not be loaded.")
else:
    df = preprocess_data(df)

# Define filters
filters = {}
excluded_columns = ["Unnamed: 0", "building_id", "square_feet_binned", "dew_temperature_binned", "air_temperature_binned", "hour_binned", "day_binned", "wind_direction_binned", "wind_speed_binned", "sea_level_pressure_binned"]

for column in df.columns:
    if column in excluded_columns:
        continue  # Skip the excluded columns
    if column == 'timestamp':
        start_date = df[column].min().date()
        end_date = df[column].max().date()
        filters[column] = st.sidebar.date_input(f"Select {column} range", [start_date, end_date], min_value=start_date, max_value=end_date)
    elif df[column].dtype == 'object' or df[column].nunique() < 20:
        unique_values = df[column].dropna().unique()  # Exclude NaN values from options
        filters[column] = st.sidebar.multiselect(f"Select {column}", options=unique_values, default=unique_values)
    else:
        min_val, max_val = df[column].min(), df[column].max()
        filters[column] = st.sidebar.slider(f"Select {column} range", min_value=float(min_val), max_value=float(max_val), value=(float(min_val), float(max_val)))

# Option to exclude NaN values
exclude_nan = st.sidebar.checkbox("Exclude NaN values", value=True)

# Apply filters
filtered_df = df.copy()
for column, filter_val in filters.items():
    if column == 'timestamp':
        start_date, end_date = filter_val
        filtered_df = filtered_df[(filtered_df[column].dt.date >= start_date) & (filtered_df[column].dt.date <= end_date)]
    elif isinstance(filter_val, list):
        filtered_df = filtered_df[filtered_df[column].isin(filter_val)]
    else:
        filtered_df = filtered_df[(filtered_df[column] >= filter_val[0]) & (filtered_df[column] <= filter_val[1])]

# Exclude NaN values if checkbox is selected
if exclude_nan:
    filtered_df = filtered_df.dropna()

# Calculate percentages
total_buildings = filtered_df['building_id'].nunique()
high_consumption_buildings = filtered_df[filtered_df['meter_reading'] >= 987.20]['building_id'].nunique()
low_consumption_buildings = total_buildings - high_consumption_buildings

if total_buildings == 0:
    st.error("No data available for the selected filters.")
else:
    high_consumption_percentage = (high_consumption_buildings / total_buildings) * 100
    low_consumption_percentage = (low_consumption_buildings / total_buildings) * 100

    # Display progress bars
    st.markdown("<h1 class='custom-title'>Building Energy Demand Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<div class='rainbow' style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])

    with col1:
        st.plotly_chart(create_donut_chart(high_consumption_percentage, low_consumption_percentage))

    with col2:
        col21, col22, col23, col24 = st.columns(4)
        with col21:
            st.plotly_chart(create_indicator_chart(filtered_df['square_feet'].mean(), "Mean Square Feet"))
        with col22:
            st.plotly_chart(create_indicator_chart(filtered_df['meter_reading'].mean(), "Mean Meter Reading"))
        with col23:
            st.plotly_chart(create_indicator_chart(filtered_df['air_temperature'].mean(), "Mean Air Temperature"))
        with col24:
            st.plotly_chart(create_indicator_chart(filtered_df['wind_speed'].mean(), "Mean Wind Speed"))

    # Create and display the stories
    story_one = create_story_one(filtered_df)
    story_two = create_story_two(filtered_df)
    story_three = create_story_three(filtered_df)
    story_four = create_story_four(filtered_df)
    story_five = create_story_five(filtered_df)
    story_six = create_story_six(filtered_df)
    story_seven = create_story_seven(filtered_df)
    story_eight = create_story_eight(filtered_df)

    # Save the stories as HTML
    with open("story_one.html", "w") as f:
        f.write(story_one.to_html())
    with open("story_two.html", "w") as f:
        f.write(story_two.to_html())
    with open("story_three.html", "w") as f:
        f.write(story_three.to_html())
    with open("story_four.html", "w") as f:
        f.write(story_four.to_html())
    with open("story_five.html", "w") as f:
        f.write(story_five.to_html())
    with open("story_six.html", "w") as f:
        f.write(story_six.to_html())
    with open("story_seven.html", "w") as f:
        f.write(story_seven.to_html())
    with open("story_eight.html", "w") as f:
        f.write(story_eight.to_html())

    # Display the generated HTML files
    col3, col4 = st.columns(2)
    with col3:
        with open("story_one.html", "r") as f:
            story_one_html = f.read()
        st.components.v1.html(story_one_html, height=650)
    
    with col4:
        with open("story_two.html", "r") as f:
            story_two_html = f.read()
        st.components.v1.html(story_two_html, height=650)
    
    col5, col6 = st.columns(2)
    with col5:
        with open("story_three.html", "r") as f:
            story_three_html = f.read()
        st.components.v1.html(story_three_html, height=650)
    
    with col6:
        with open("story_four.html", "r") as f:
            story_four_html = f.read()
        st.components.v1.html(story_four_html, height=650)
    
    col7, col8 = st.columns(2)
    with col7:
        with open("story_five.html", "r") as f:
            story_five_html = f.read()
        st.components.v1.html(story_five_html, height=650)

    with col8:
        with open("story_six.html", "r") as f:
            story_six_html = f.read()
        st.components.v1.html(story_six_html, height=650)
    
    col9, col10 = st.columns(2)
    with col9:
        with open("story_seven.html", "r") as f:
            story_seven_html = f.read()
        st.components.v1.html(story_seven_html, height=650)

    with col10:
        with open("story_eight.html", "r") as f:
            story_eight_html = f.read()
        st.components.v1.html(story_eight_html, height=650)

# File Upload for Data Visualization
st.markdown("<h2 class='custom-title'>Upload Data for Visualization</h2>", unsafe_allow_html=True)
st.markdown("<div class='rainbow' style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, dtype=d_types)
        st.write("Uploaded Data")
        st.write(df)
        df = preprocess_data(df)
        filtered_df = df.copy()
        story_one = create_story_one(filtered_df)
        story_two = create_story_two(filtered_df)
        story_three = create_story_three(filtered_df)
        story_four = create_story_four(filtered_df)
        story_five = create_story_five(filtered_df)
        story_six = create_story_six(filtered_df)
        story_seven = create_story_seven(filtered_df)
        story_eight = create_story_eight(filtered_df)

        with open("story_one.html", "w") as f:
            f.write(story_one.to_html())
        with open("story_two.html", "w") as f:
            f.write(story_two.to_html())
        with open("story_three.html", "w") as f:
            f.write(story_three.to_html())
        with open("story_four.html", "w") as f:
            f.write(story_four.to_html())
        with open("story_five.html", "w") as f:
            f.write(story_five.to_html())
        with open("story_six.html", "w") as f:
            f.write(story_six.to_html())
        with open("story_seven.html", "w") as f:
            f.write(story_seven.to_html())
        with open("story_eight.html", "w") as f:
            f.write(story_eight.to_html())
        

        col3, col4 = st.columns(2)
        with col3:
            with open("story_one.html", "r") as f:
                story_one_html = f.read()
            st.components.v1.html(story_one_html, height=650)
        
        with col4:
            with open("story_two.html", "r") as f:
                story_two_html = f.read()
            st.components.v1.html(story_two_html, height=650)
        
        col5, col6 = st.columns(2)
        with col5:
            with open("story_three.html", "r") as f:
                story_three_html = f.read()
            st.components.v1.html(story_three_html, height=650)
    
        with col6:
            with open("story_four.html", "r") as f:
                story_four_html = f.read()
            st.components.v1.html(story_four_html, height=650)
        
        col7, col8 = st.columns(2)
        with col7:
            with open("story_five.html", "r") as f:
                story_five_html = f.read()
            st.components.v1.html(story_five_html, height=650)
    
        with col8:
            with open("story_six.html", "r") as f:
                story_six_html = f.read()
            st.components.v1.html(story_six_html, height=650)
        
        col9, col10 = st.columns(2)
        with col9:
            with open("story_seven.html", "r") as f:
                story_seven_html = f.read()
            st.components.v1.html(story_seven_html, height=650)

        with col10:
            with open("story_eight.html", "r") as f:
                story_eight_html = f.read()
            st.components.v1.html(story_eight_html, height=650)

    except Exception as e:
        st.error(f"Error uploading file: {e}")

# Button to reset filters
if st.button('Reset Filters'):
    filtered_df = df.copy()
    story_one = create_story_one(filtered_df)
    story_two = create_story_two(filtered_df)
    story_three = create_story_three(filtered_df)
    story_four = create_story_four(filtered_df)
    story_five = create_story_five(filtered_df)
    story_six = create_story_six(filtered_df)
    story_seven = create_story_seven(filtered_df)
    story_eight = create_story_eight(filtered_df)

    with open("story_one.html", "w") as f:
        f.write(story_one.to_html())
    with open("story_two.html", "w") as f:
        f.write(story_two.to_html())
    with open("story_three.html", "w") as f:
        f.write(story_three.to_html())
    with open("story_four.html", "w") as f:
        f.write(story_four.to_html())
    with open("story_five.html", "w") as f:
        f.write(story_four.to_html())
    with open("story_six.html", "w") as f:
        f.write(story_four.to_html())
    with open("story_seven.html", "w") as f:
        f.write(story_seven.to_html())
    with open("story_eight.html", "w") as f:
        f.write(story_eight.to_html())

    col3, col4 = st.columns(2)
    with col3:
        with open("story_one.html", "r") as f:
            story_one_html = f.read()
        st.components.v1.html(story_one_html, height=650)
    
    with col4:
        with open("story_two.html", "r") as f:
            story_two_html = f.read()
        st.components.v1.html(story_two_html, height=650)
    
    col5, col6 = st.columns(2)
    with col5:
        with open("story_three.html", "r") as f:
            story_three_html = f.read()
        st.components.v1.html(story_three_html, height=650)
    
    with col6:
        with open("story_four.html", "r") as f:
            story_four_html = f.read()
        st.components.v1.html(story_four_html, height=650)
    
    col7, col8 = st.columns(2)
    with col7:
        with open("story_five.html", "r") as f:
            story_three_html = f.read()
        st.components.v1.html(story_five_html, height=650)
    
    with col8:
        with open("story_six.html", "r") as f:
            story_four_html = f.read()
        st.components.v1.html(story_six_html, height=650)
    
    col9, col10 = st.columns(2)
    with col9:
        with open("story_seven.html", "r") as f:
            story_seven_html = f.read()
        st.components.v1.html(story_seven_html, height=650)

    with col10:
        with open("story_eight.html", "r") as f:
            story_eight_html = f.read()
        st.components.v1.html(story_eight_html, height=650)
