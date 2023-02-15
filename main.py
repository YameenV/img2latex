import streamlit as st
from utils import defaultConfig,process_image
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import threading
from typing import Union
import av
from model import model
from PIL import Image
import cv2
import numpy as np
import uuid
from streamlit_option_menu import option_menu

defaultConfig(1)
st.title("Latex Generator")
IMAGENAME = ''

class VideoTransformer(VideoTransformerBase):
    frame_lock: threading.Lock  

    out_image: Union[np.ndarray, None]

    def __init__(self) -> None:
        self.frame_lock = threading.Lock()
        self.out_image = None

    def transform(self, frame: av.VideoFrame) -> np.ndarray:
        out_image = frame.to_ndarray(format="bgr24")

        with self.frame_lock:
            self.out_image = out_image

        height, width, _ = out_image.shape
        x = int(width/4)
        y = int(height/4)
        w = int(width/2)
        h = int(height/2)
        
        out_image = cv2.rectangle(out_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        return out_image
    
def app():

    selected = option_menu(
        None, 
        options=["Scanner","Upload"],
        icons=["webcam", "box-arrow-in-down"],
        menu_icon="cast",
        default_index=1,
        orientation="horizontal")
    
    if selected == "Scanner":
        webcam = st.empty()

        with webcam:
            wrtc = webrtc_streamer(key="snapshot", video_transformer_factory=VideoTransformer)
    
        if wrtc.video_transformer:
            snap = st.button("Snapshot")

            if snap:
                with wrtc.video_transformer.frame_lock:
                    out_image = wrtc.video_transformer.out_image

                if out_image is not None:
                    height, width, _ = out_image.shape
                    x = int(width/4)
                    y = int(height/4)
                    w = int(width/2)
                    h = int(height/2)
                    
                    cropped_image = out_image[y+2:y+h-2, x+2:x+w-2]
                    rgbImage = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(rgbImage)

                    uid = uuid.uuid4().hex
                    filename = f'./images/{uid}.jpg'

                    image.save(filename)
                    global IMAGENAME
                    IMAGENAME = filename
                    webcam.empty()
                        
                else:
                    st.warning("No frames available yet.")
        
        if len(IMAGENAME) > 0:
            st.text("Scaned Image")
            image = Image.open(IMAGENAME)
            display_image = np.array(image)
            st.image(display_image, channels="BGR")

            if image is not None:
                generatedLatex = model(image)
                st.balloons()
                st.text("Generated Latex")
                st.code(generatedLatex, language='latex')
                st.text("Complied Latex")
                st.latex(generatedLatex)

                with st.expander("Download LaTeX code", expanded=False):
                    st.download_button(
                        label="Download LaTeX",
                        data=generatedLatex,
                        file_name="generated_latex.text",
                        mime="text/plain",
                    )

    if selected == "Upload":
        uploaded_file = st.file_uploader('Choose an image file', type=['jpg','png', 'jpeg'])

        if uploaded_file is not None:
            process_image(uploaded_file)
            arrayImage = Image.open(uploaded_file)
            display_image = np.array(arrayImage)

            generatedLatex = model(arrayImage)
            st.balloons()
            st.write("Generated Latex")
            st.code(generatedLatex, language='latex')
            st.write("Complied Latex")
            st.latex(generatedLatex)
            
            with st.expander("Download LaTeX code", expanded=False):
                st.download_button(
                    label="Download LaTeX",
                    data=generatedLatex,
                    file_name="generated_latex.text",
                    mime="text/plain",
                )

if __name__ == "__main__":
    app()