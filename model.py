from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from tokenizers import Tokenizer
import streamlit as st


def model(image):

    progressText = st.empty()
    
    progressText.write("Loading Status:- Processing is Started .......")
    processor = TrOCRProcessor.from_pretrained("microsoft/trocr-small-printed",use_fast=False)
    progressText.write("Loading Status:- Processor is loaded .......")
    visionModel = VisionEncoderDecoderModel.from_pretrained("yhshin/latex-ocr")
    progressText.write("Loading Status:- Vision Model is loaded .......")
    tokenizer = Tokenizer.from_file("./tokenizer-wordlevel.json")
    progressText.write("Loading Status:- Tokenizer is loaded .......")

    pixel_values = processor(image, return_tensors="pt").pixel_values
    progressText.write("Loading Status:- Image is Processed .......")
    generated_ids = visionModel.generate(pixel_values)
    progressText.write("Loading Status:- Vector is Generated .......")
    generated_text = tokenizer.decode_batch(generated_ids.tolist(), skip_special_tokens=True)[0]
    progressText.write("Loading Status:- Latex is Generated .......")
    generated_text = generated_text.replace(" ", "")
    progressText.write("Loading Status:- Latex is Processed .......")
    progressText.empty()

    return generated_text

if __name__ == "__main__":
    model()