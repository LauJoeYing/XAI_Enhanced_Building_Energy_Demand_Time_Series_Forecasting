import streamlit as st
from pathlib import Path
import fitz
from io import BytesIO
from PIL import Image

# Load custom CSS
base_path = Path(__file__).parent
stylesheet_file_path = (base_path / "../stylesheets/style.css").resolve()
with open(stylesheet_file_path) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

with st.sidebar:
    st.write("""<p class="custom-nav-item">Contact Me</ap>""", unsafe_allow_html=True)
    st.write("""<a href="mailto:joeying0712@gmail.com" class="custom-nav-item">📧 Email</a>""", unsafe_allow_html=True)
    st.write("""<a href="https://www.linkedin.com/in/laujoeying/" class="custom-nav-item">💼 LinkedIn Profile</a>""", unsafe_allow_html=True)

# Function to convert PDF page to image with higher resolution
def pdf_page_to_image(pdf_document, page_number, zoom=2):
    page = pdf_document.load_page(page_number)
    mat = fitz.Matrix(zoom, zoom)  # Apply zoom factor
    pix = page.get_pixmap(matrix=mat)
    image = Image.open(BytesIO(pix.tobytes("png")))
    return image

#Title of the app
st.markdown("<h1 class='custom-title'>High Energy Consumption Factors</h1>", unsafe_allow_html=True)

# Move the rainbow to the left
st.markdown(
    """
    <div class='rainbow' style='margin-bottom: 2rem; text-align: left;'>
        <!-- Your rainbow content here -->
    </div>
    """,
    unsafe_allow_html=True
)

# Specify the path to the PDF file
pdf_path = (base_path / "../../data/demand_factors.pdf").resolve()

# Open the PDF file
pdf_document = fitz.open(pdf_path)

# Initialize session state to keep track of the current page
if 'page_number' not in st.session_state:
    st.session_state.page_number = 0

# Navigation buttons
col1, col2, col3 = st.columns([1, 1, 1])

if col1.button("Previous"):
    st.session_state.page_number = max(0, st.session_state.page_number - 1)

if col3.button("Next"):
    st.session_state.page_number = min(len(pdf_document) - 1, st.session_state.page_number + 1)

# Display the current page
st.write(f"Page {st.session_state.page_number + 1} of {len(pdf_document)}")
image = pdf_page_to_image(pdf_document, st.session_state.page_number, zoom=2)  # Increase zoom factor for better clarity
st.image(image, use_column_width=True)  # Adjust image to fit the width of the column
