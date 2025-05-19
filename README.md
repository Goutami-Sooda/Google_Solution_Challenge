# AI-Powered Student Assignment Evaluation and Feedback Tool Integrated with Google Classroom

This project is a modular MVP that consists of integration with **Google Classroom** to automate the process of fetching student submissions, extracting text using OCR **Gemini API**, evaluating submission and generating personalized feedback using **Groq AI**.

---

## 🚀 Key Features

1. **Google Classroom Integration**
   - Fetch assignments and student submissions using Google Classroom API.
   - Supports multiple classrooms and coursework types.

2. **OCR Text Extraction (Gemini API)**
   - Automatically extracts text from image and PDF attachments in submissions.
   - Supports handwritten and typed content.

3. **AI Evaluation & Personalized Feedback (Groq API)**
   - Compares student answers against a teacher-provided rubrics.
   - Analyzes past performance to detect learning gaps.
   - Generates feedback reports which can be reviewed or auto-mailed to students.

---

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **APIs Used:**  
  - Google Classroom API (submission fetch)  
  - Gemini API (OCR from images/PDFs)  
  - Groq API (AI answer evaluation and feedback)
- **Database:** SQLite (rubrics and feedback history)
- **Frontend:** HTML + JavaScript

---

## 🌐 How to Run

> Each folder/module is self-contained and can run independently.

### 1. Clone the repository

```bash
git clone https://github.com/Yaswanth-Bolla/Google_Solution_Challenge 
cd Google_Solution_Challenge
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies and Run the Individual Flask Apps 

#### Google Classroom Integration

> Add OAuth Credentials: Place your credentials.json inside the google_classroom_integration/ folder. This file contains OAuth 2.0 credentials from your Google Cloud Console.

```bash
cd google_classroom_integration
pip install -r requirements.txt
python script_auth.py
flask run
```

#### OCR Text Extraction

> Add Gemini API Key: Place your API key in .env folder within the OCR_text_extraction/ folder.

```bash
cd OCR_text_extraction
pip install -r requirements.txt
flask run --port=5001
```

#### AI Evaluation & Feedback

> Add Groq API Key: Place your API key in .env folder within the AI_evaluation_and_feedback/ folder.

```bash
cd AI_evaluation_and_feedback
pip install -r requirements.txt
python app.py
```

## Demo Video

**Link:** https://drive.google.com/file/d/1DTp5XKAGl5XU-P_wmADRNWDMEx-0KyB6/view?usp=drive_link


## 📊 Future Enhancements

- Unified teacher dashboard
- Real-time feedback notification and mailing system
- All features integrated into a single prototype

## 🙌 Acknowledgements

A modular MVP built as part of Google Solution Challenge 2025
