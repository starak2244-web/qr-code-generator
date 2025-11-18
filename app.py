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


def _prepare_logo(logo_stream: Optional[io.BytesIO], max_w: int, max_h: int) -> Optional[Image.Image]:
    if not logo_stream:
        return None
    try:
        logo = Image.open(logo_stream).convert("RGBA")
    except Exception:
        return None
    # Resize preserving aspect ratio
    logo.thumbnail((max_w, max_h), Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.ANTIALIAS)
    return logo


def make_qr_png_bytes(data: str, box_size: int, border: int, error_correction, fill_color="black", back_color="white", logo_img: Optional[Image.Image] = None) -> bytes:
    qr = qrcode.QRCode(
        version=None,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGBA")

    if logo_img:
        qr_w, qr_h = img.size
        # logo already resized by caller to fit within recommended bounds
        lw, lh = logo_img.size
        pos = ((qr_w - lw) // 2, (qr_h - lh) // 2)
        img.paste(logo_img, pos, mask=logo_img)

    out = io.BytesIO()
    img.save(out, format="PNG")
    return out.getvalue()


def make_qr_svg_bytes(data: str, border: int, error_correction) -> bytes:
    qr = qrcode.QRCode(
        version=None,
        error_correction=error_correction,
        box_size=1,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(image_factory=SvgImage)
    out = io.BytesIO()
    img.save(out)
    # SvgImage writes text; ensure bytes
    b = out.getvalue()
    return b


# --- Button ---
generate_btn = st.button("Generate QR Code")

if generate_btn:
    if not data or data.strip() == "":
        st.warning("Please enter some data or URL to encode.")
    else:
        with st.spinner("Generating QR code..."):
            # Prepare logo (if any). For PNG only.
            logo_img = None
            if logo_file is not None:
                # Read uploaded file into BytesIO for PIL
                logo_stream = io.BytesIO(logo_file.read())
                # estimate max logo size based on resulting QR pixel size
                # QR pixel size for PNG = (module_count + 2*border) * box_size
                # We can create a temporary QR to get module_count
                tmp_qr = qrcode.QRCode(version=None, error_correction=error_correction, box_size=box_size, border=border)
                tmp_qr.add_data(data)
                tmp_qr.make(fit=True)
                module_count = tmp_qr.modules_count
                qr_pixel = (module_count + 2 * border) * box_size
                max_logo_w = int(qr_pixel * 0.25)
                max_logo_h = int(qr_pixel * 0.25)
                logo_img = _prepare_logo(logo_stream, max_logo_w, max_logo_h)

            if out_format == Format.PNG.value:
                png_bytes = make_qr_png_bytes(data, box_size, border, error_correction, logo_img=logo_img)
                st.image(png_bytes, use_column_width=False)
                st.download_button("Download PNG", data=png_bytes, file_name="qrcode.png", mime="image/png")

            else:  # SVG
                svg_bytes = make_qr_svg_bytes(data, border, error_correction)
                # Render inline
                try:
                    svg_text = svg_bytes.decode("utf-8")
                except Exception:
                    svg_text = svg_bytes.decode(errors="ignore")
                st.components.v1.html(svg_text, height=300)
                st.download_button("Download SVG", data=svg_bytes, file_name="qrcode.svg", mime="image/svg+xml")

        st.success("QR code generated")
