import io
from enum import Enum

import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
from qrcode.image.svg import SvgImage
from PIL import Image

import streamlit as st

st.set_page_config(page_title="QR Code Generator", layout="centered")

st.title("QR Code Generator — Python + Streamlit")
st.write("Create PNG or SVG QR codes, choose size, error correction and optionally overlay a logo.")


class Format(str, Enum):
    PNG = "PNG"
    SVG = "SVG"


# --- Inputs ---
data = st.text_area("Data / URL to encode", value="https://example.com", height=120)
col1, col2 = st.columns(2)
with col1:
    out_format = st.selectbox("Output format", [Format.PNG.value, Format.SVG.value])
    box_size = st.slider("Box size (controls image scale)", min_value=2, max_value=20, value=10)
with col2:
    border = st.slider("Border (boxes)", min_value=0, max_value=10, value=4)
    ec_str = st.selectbox("Error correction", ["L (7%)", "M (15%)", "Q (25%)", "H (30%)"])
    ec_map = {"L (7%)": ERROR_CORRECT_L, "M (15%)": ERROR_CORRECT_M, "Q (25%)": ERROR_CORRECT_Q, "H (30%)": ERROR_CORRECT_H}
    error_correction = ec_map[ec_str]

st.markdown("---")
logo_file = st.file_uploader("Optional: upload a logo/image to embed in the center (PNG/JPG) — recommended <= 30% of QR size", type=["png", "jpg", "jpeg"])

generate_btn = st.button("Generate QR Code")

def make_qr_png(data: str, box_size: int, border: int, error_correction, fill_color="black", back_color="white", logo_img: Image.Image | None = None):
    qr = qrcode.QRCode(
        import io
        from enum import Enum
        from typing import Optional

        import qrcode
        from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
        from qrcode.image.svg import SvgImage
        from PIL import Image

        import streamlit as st

        st.set_page_config(page_title="QR Code Generator", layout="centered")

        st.title("QR Code Generator — Python + Streamlit")
        st.write("Create PNG or SVG QR codes, choose size, error correction and optionally overlay a logo.")


        class Format(str, Enum):
            PNG = "PNG"
            SVG = "SVG"


        # --- Inputs ---
        data = st.text_area("Data / URL to encode", value="https://example.com", height=120)
        col1, col2 = st.columns(2)
        with col1:
            out_format = st.selectbox("Output format", [Format.PNG.value, Format.SVG.value])
            box_size = st.slider("Box size (controls image scale)", min_value=2, max_value=20, value=10)
        with col2:
            border = st.slider("Border (boxes)", min_value=0, max_value=10, value=4)
            ec_str = st.selectbox("Error correction", ["L (7%)", "M (15%)", "Q (25%)", "H (30%)"])
            ec_map = {"L (7%)": ERROR_CORRECT_L, "M (15%)": ERROR_CORRECT_M, "Q (25%)": ERROR_CORRECT_Q, "H (30%)": ERROR_CORRECT_H}
            error_correction = ec_map[ec_str]

        st.markdown("---")
        logo_file = st.file_uploader("Optional: upload a logo/image to embed in the center (PNG/JPG) — recommended <= 30% of QR size", type=["png", "jpg", "jpeg"])

        generate_btn = st.button("Generate QR Code")
