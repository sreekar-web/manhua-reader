from flask import Flask, request, jsonify, render_template
from gtts import gTTS
from PIL import Image
import pytesseract 
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
import os

app = Flask(__name__)

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')  # Serves the HTML frontend

# Route to handle OCR
@app.route('/ocr', methods=['POST'])
def ocr():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    # Save uploaded image
    image = request.files['image']
    image_path = os.path.join("static", image.filename)
    image.save(image_path)

    # Perform OCR using Tesseract
    text = pytesseract.image_to_string(Image.open(image_path))
    return jsonify({"text": text, "image_url": image_path})

# Route to handle Text-to-Speech
@app.route('/tts', methods=['POST'])
def tts():
    data = request.json
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Convert text to speech
    tts = gTTS(text=text, lang='en')
    audio_path = os.path.join("static", "output.mp3")
    tts.save(audio_path)
    return jsonify({"audio_url": audio_path})

if __name__ == '__main__':
    app.run(debug=True)
