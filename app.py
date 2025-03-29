# import os
# import traceback
# from flask import Flask, request, jsonify, send_from_directory
# from werkzeug.utils import secure_filename
# import google.generativeai as genai
# from dotenv import load_dotenv
# import base64
# from flask_cors import CORS

# # Load environment variables
# load_dotenv()

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})  # More permissive CORS

# # Configure upload settings
# UPLOAD_FOLDER = 'uploads'
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# # Ensure upload directory exists
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Configure Gemini API
# try:
#     genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
# except Exception as e:
#     print(f"Error configuring Gemini API: {e}")

# def allowed_file(filename):
#     """Check if the file has an allowed extension"""
#     return '.' in filename and \
#         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/')
# def serve_index():
#     """Serve the index.html file"""
#     return send_from_directory('.', 'index.html')


# @app.route('/ocr', methods=['POST'])
# def perform_ocr():
#     """
#     Perform OCR on uploaded image using Gemini API
#     """
#     try:
#         # Check if file is present in the request
#         if 'image' not in request.files:
#             return jsonify({
#                 'status': 'error',
#                 'message': 'No image file uploaded'
#             }), 400
        
#         file = request.files['image']
        
#         # Check if filename is empty
#         if file.filename == '':
#             return jsonify({
#                 'status': 'error',
#                 'message': 'No selected file'
#             }), 400
        
#         # Check if file is allowed
#         if not file or not allowed_file(file.filename):
#             return jsonify({
#                 'status': 'error',
#                 'message': 'Invalid file type'
#             }), 400
        
#         # Secure the filename
#         filename = secure_filename(file.filename)
        
#         # Save the file
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(filepath)
        
#         try:
#             # Read the image file as base64
#             with open(filepath, 'rb') as image_file:
#                 base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            
#             # Initialize Gemini 1.5 Flash model
#             model = genai.GenerativeModel('gemini-2.0-flash')
            
#             # Prepare image part
#             image_part = {
#                 'mime_type': 'image/jpeg',
#                 'data': base64_image
#             }
            
#             # Generate content with OCR-focused prompt
#             prompt = "Extract all readable text from this image. Provide the full text content exactly as it appears."
            
#             response = model.generate_content([
#                 prompt, 
#                 image_part
#             ])
            
#             # Optional: Remove the file after processing
#             os.remove(filepath)
            
#             # Return the extracted text
#             return jsonify({
#                 'status': 'success',
#                 'full_text': response.text
#             }), 200
        
#         except Exception as e:
#             # Remove the file in case of error
#             if os.path.exists(filepath):
#                 os.remove(filepath)
            
#             # Print full traceback for debugging
#             print(f"Error processing image: {e}")
#             traceback.print_exc()
            
#             return jsonify({
#                 'status': 'error',
#                 'message': f'Error processing image: {str(e)}'
#             }), 500
    
#     except Exception as e:
#         # Print full traceback for debugging
#         print(f"Unexpected error: {e}")
#         traceback.print_exc()
        
#         return jsonify({
#             'status': 'error',
#             'message': f'Unexpected error: {str(e)}'
#         }), 500

# @app.route('/test')
# def test_route():
#     """Simple test route to check server connectivity"""
#     return jsonify({
#         'status': 'success',
#         'message': 'Server is running'
#     })

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5001)
import os
import traceback
import base64
import requests
import google.generativeai as genai
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Google Classroom API Scope
SCOPES = [
    "https://www.googleapis.com/auth/classroom.coursework.students",
    "https://www.googleapis.com/auth/classroom.rosters",  # 🔹 Required to list students
    "https://www.googleapis.com/auth/drive.readonly"  # 🔹 Required if fetching Drive images
]

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

def get_google_service():
    """Authenticate and return a Google Classroom service instance."""
    creds = None

    # Load existing credentials from token.pickle
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # Refresh or request new credentials if necessary
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the new credentials
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("classroom", "v1", credentials=creds)

# def get_student_submission_images(course_id, assignment_id, student_email):
#     """Fetch image attachments from a student's submission using their email address."""
#     try:
#         service = get_google_service()

#         # Step 1: Get student ID from email
#         students = service.courses().students().list(courseId=course_id).execute()

#         student_id = None
#         for student in students.get('students', []):
#             if student['profile']['emailAddress'].lower() == student_email.lower():
#                 student_id = student['userId']
#                 break

#         if not student_id:
#             return {'status': 'error', 'message': f"No student found with email {student_email}"}

#         # Step 2: Fetch student submissions using student_id
#         submissions = service.courses().courseWork.studentSubmissions().list(
#             courseId=course_id,
#             courseWorkId=assignment_id
#         ).execute()

#         images = []
#         for submission in submissions.get('studentSubmissions', []):
#             if submission.get('userId') == student_id and 'attachments' in submission.get('assignmentSubmission', {}):
#                 for attachment in submission['assignmentSubmission']['attachments']:
#                     if 'driveFile' in attachment:
#                         file_id = attachment['driveFile']['id']
#                         images.append(f"https://drive.google.com/uc?id={file_id}")

#         return {'status': 'success', 'images': images}

#     except Exception as e:
#         return {'status': 'error', 'message': f"Error fetching submissions: {str(e)}"}

import traceback

def get_student_submission_images(course_id, assignment_id, student_email):
    """Fetch image attachments from a student's submission using their email address."""
    try:
        service = get_google_service()

        # Step 1: Get student ID from email
        students = service.courses().students().list(courseId=course_id).execute()

        student_id = None
        for student in students.get('students', []):
            if student['profile']['emailAddress'].lower() == student_email.lower():
                student_id = student['userId']
                break

        if not student_id:
            print(f"DEBUG: No student found with email {student_email}")
            return {'status': 'error', 'message': f"No student found with email {student_email}"}

        print(f"DEBUG: Found student ID: {student_id}")

        # Step 2: Fetch student submissions using student_id
        submissions = service.courses().courseWork.studentSubmissions().list(
            courseId=course_id,
            courseWorkId=assignment_id
        ).execute()

        images = []
        for submission in submissions.get('studentSubmissions', []):
            if submission.get('userId') == student_id and 'attachments' in submission.get('assignmentSubmission', {}):
                for attachment in submission['assignmentSubmission']['attachments']:
                    if 'driveFile' in attachment:
                        file_id = attachment['driveFile']['id']
                        images.append(f"https://drive.google.com/uc?id={file_id}")

        if not images:
            print("DEBUG: No image attachments found in submission.")

        return {'status': 'success', 'images': images}

    except Exception as e:
        print(f"ERROR: {str(e)}")
        traceback.print_exc()  # Print full error details
        return {'status': 'error', 'message': f"Error fetching submissions: {str(e)}"}


def download_image(image_url, filename):
    """Download an image from Google Drive link."""
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            with open(filepath, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return filepath
        return None
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None

def perform_ocr_on_image(image_path):
    """Perform OCR on an image using Gemini API."""
    try:
        with open(image_path, 'rb') as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')

        model = genai.GenerativeModel('gemini-2.0-flash')
        prompt = "Extract all readable text from this image. Provide the full text content exactly as it appears."
        response = model.generate_content([
            prompt, 
            {'mime_type': 'image/jpeg', 'data': base64_image}
        ])

        os.remove(image_path)  # Cleanup
        return response.text if response else "No text detected"
    except Exception as e:
        print(f"Error performing OCR: {e}")
        traceback.print_exc()
        return "OCR failed"

@app.route('/fetch-and-ocr', methods=['GET'])
def fetch_and_ocr():
    """Fetch images from Google Classroom and perform OCR."""
    course_id = request.args.get('course_id')
    assignment_id = request.args.get('assignment_id')
    student_email = request.args.get('student_email')

    if not all([course_id, assignment_id, student_email]):
        return jsonify({'status': 'error', 'message': 'Missing parameters'}), 400

    response = get_student_submission_images(course_id, assignment_id, student_email)
    
    if response['status'] == 'error':
        return jsonify(response), 404

    images = response.get('images', [])
    if not images:
        return jsonify({'status': 'error', 'message': 'No images found'}), 404

    extracted_texts = []
    for idx, img_url in enumerate(images):
        filename = f"submission_{idx}.jpg"
        image_path = download_image(img_url, filename)
        if image_path:
            extracted_text = perform_ocr_on_image(image_path)
            extracted_texts.append(extracted_text)

    return jsonify({'status': 'success', 'extracted_texts': extracted_texts})

@app.route('/')
def serve_index():
    """Serve the frontend HTML."""
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
