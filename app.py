from flask import Flask, request, jsonify
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from flask import Flask, request, jsonify, send_from_directory
from google.auth.transport.requests import Request
import os
import pickle

app = Flask(__name__)

SCOPES = ["https://www.googleapis.com/auth/classroom.student-submissions.me.readonly"]

def get_google_service():
    """Authenticate and return a Google Classroom service instance."""
    creds = None

    # Load existing credentials
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # Refresh or request new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("classroom", "v1", credentials=creds)


@app.route('/fetch-text-answer', methods=['GET'])
def fetch_text_answer():
    """Fetch and return a student's short answer submission."""
    course_id = request.args.get('course_id')
    assignment_id = request.args.get('assignment_id')
    student_id = request.args.get('student_id')

    if not course_id or not assignment_id or not student_id:
        return jsonify({'status': 'error', 'message': 'Missing parameters'})

    try:
        service = get_google_service()
        
        # Fetch student submissions
        submissions_response = service.courses().courseWork().studentSubmissions().list(
            courseId=course_id,
            courseWorkId=assignment_id
        ).execute()

        submissions = submissions_response.get('studentSubmissions', [])

        for submission in submissions:
            if submission.get('userId') == student_id and 'shortAnswerSubmission' in submission:
                answer_text = submission['shortAnswerSubmission'].get('answer', 'No answer provided.')
                return jsonify({'status': 'success', 'answer': answer_text})

        return jsonify({'status': 'error', 'message': 'No short answer found for this student.'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': f"Error fetching submission: {str(e)}"})


@app.route('/')
def serve_index():
    """Serve the frontend HTML."""
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(port=5001, debug=True)
