import streamlit as st
from PIL import Image
import numpy as np

# ==================================================
# MANUAL DIP FUNCTIONS (No inbuilt DIP library functions used)
# ==================================================

def grayscale(image_pil):
    """Manual Grayscale using luminosity."""
    try:
        img_array = np.array(image_pil.convert("RGB"), dtype=np.float32)
        H, W, _ = img_array.shape
        gray_array = np.zeros((H, W), dtype=np.uint8)
        # Manual loop (required by project constraints)
        for y in range(H):
            for x in range(W):
                R, G, B = img_array[y, x]
                gray_value = 0.299 * R + 0.587 * G + 0.114 * B
                gray_array[y, x] = np.clip(round(gray_value), 0, 255)
        return Image.fromarray(gray_array, mode='L')
    except Exception as e:
        st.error(f"Grayscale Error: {e}")
        return None

def brightness(image_pil, offset):
    """Manual Brightness adjustment (expects grayscale input)."""
    try:
        img_array = np.array(image_pil.convert('L'), dtype=np.int16) # Convert to L, use int16
        bright_array = np.clip(img_array + offset, 0, 255).astype(np.uint8) # Add offset & clamp
        return Image.fromarray(bright_array, mode='L')
    except Exception as e:
        st.error(f"Brightness Error: {e}")
        return None

def box_blur_3x3(image_pil):
    """Manual 3x3 Box Blur (expects grayscale input)."""
    try:
        img_array = np.array(image_pil.convert('L'), dtype=np.float32) # Convert to L, use float32
        H, W = img_array.shape
        blurred_array = np.copy(img_array)
        # Manual loop over inner pixels (border pixels are copied)
        for y in range(1, H - 1):
            for x in range(1, W - 1):
                neighborhood = img_array[y-1:y+2, x-1:x+2]
                blurred_array[y, x] = round(np.mean(neighborhood)) # Calculate average
        return Image.fromarray(np.clip(blurred_array, 0, 255).astype(np.uint8), mode='L')
    except Exception as e:
        st.error(f"Blur Error: {e}")
        return None

# ==================================================
# STREAMLIT WEB APP INTERFACE
# ==================================================

st.set_page_config(page_title="DIP Mini Project", layout="centered") # Centered layout is often simpler
st.title("Manual DIP Pipeline")
st.caption("Basic Enhancement: Grayscale -> Brightness -> Box Blur (Manual Implementation)")

uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg", "bmp"])

if uploaded_file:
    try:
        original_image = Image.open(uploaded_file)

        st.header("1. Original")
        st.image(original_image, caption=f"Original: {uploaded_file.name}", use_container_width=True)

        # --- Pipeline Steps ---
        st.header("2. Pipeline Processing")

        grayscale_image = grayscale(original_image)
        if grayscale_image:
            st.image(grayscale_image, caption='Step 1: Grayscale', use_container_width=True)

            brightness_offset = st.slider("Brightness Offset", -100, 100, 50)
            bright_image = brightness(grayscale_image, brightness_offset)
            if bright_image:
                st.image(bright_image, caption=f'Step 2: Brightness (Offset: {brightness_offset})', use_container_width=True)

                blurred_image = box_blur_3x3(bright_image)
                if blurred_image:
                    st.image(blurred_image, caption='Step 3: Box Blur (Final)', use_container_width=True)
                    st.success("Pipeline Complete!")
                    # Simplified observations
                    st.markdown(f"""
                    **Observations:**
                    *   Manual Grayscale, Brightness (Offset {brightness_offset}), and 3x3 Box Blur applied sequentially.
                    *   Border pixels were not processed by the blur filter.
                    """)
                else: st.warning("Blur step failed.") # Use warning for non-critical failures
            else: st.warning("Brightness step failed.")
        else: st.warning("Grayscale step failed.")

    except Exception as e:
        st.error(f"Image loading/processing error: {e}")
else:
    st.info("Please upload an image.")