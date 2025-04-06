



import os
import traceback
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import google.generativeai as genai
from dotenv import load_dotenv
import base64
from flask_cors import CORS

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # More permissive CORS

# Configure upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure Gemini API
try:
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
except Exception as e:
    print(f"Error configuring Gemini API: {e}")

def allowed_file(filename):
    """Check if the file has an allowed extension"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def serve_index():
    """Serve the index.html file"""
    return send_from_directory('.', 'index.html')


@app.route('/ocr', methods=['POST'])
def perform_ocr():
    """
    Perform OCR on uploaded image using Gemini API
    """
    try:
        # Check if file is present in the request
        if 'image' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'No image file uploaded'
            }), 400
        
        file = request.files['image']
        
        # Check if filename is empty
        if file.filename == '':
            return jsonify({
                'status': 'error',
                'message': 'No selected file'
            }), 400
        
        # Check if file is allowed
        if not file or not allowed_file(file.filename):
            return jsonify({
                'status': 'error',
                'message': 'Invalid file type'
            }), 400
        
        # Secure the filename
        filename = secure_filename(file.filename)
        
        # Save the file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Read the image file as base64
            with open(filepath, 'rb') as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Initialize Gemini 1.5 Flash model
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            # Prepare image part
            image_part = {
                'mime_type': 'image/jpeg',
                'data': base64_image
            }
            
            # Generate content with OCR-focused prompt
            prompt = "Extract all readable text from this image. Provide the full text content exactly as it appears."
            
            response = model.generate_content([
                prompt, 
                image_part
            ])
            
            # Optional: Remove the file after processing
            os.remove(filepath)
            
            # Return the extracted text
            return jsonify({
                'status': 'success',
                'full_text': response.text
            }), 200
        
        except Exception as e:
            # Remove the file in case of error
            if os.path.exists(filepath):
                os.remove(filepath)
            
            # Print full traceback for debugging
            print(f"Error processing image: {e}")
            traceback.print_exc()
            
            return jsonify({
                'status': 'error',
                'message': f'Error processing image: {str(e)}'
            }), 500
    
    except Exception as e:
        # Print full traceback for debugging
        print(f"Unexpected error: {e}")
        traceback.print_exc()
        
        return jsonify({
            'status': 'error',
            'message': f'Unexpected error: {str(e)}'
        }), 500

@app.route('/test')
def test_route():
    """Simple test route to check server connectivity"""
    return jsonify({
        'status': 'success',
        'message': 'Server is running'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)



