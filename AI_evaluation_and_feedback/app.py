from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from database import get_db, Student, Assignment
from llm_interface import get_evaluation_feedback, get_personalized_feedback
from sqlalchemy.orm import Session
load_dotenv(dotenv_path=".env")

app = Flask(__name__)

@app.route('/evaluate', methods=['POST'])
def evaluate_assignment():
    data = request.get_json()
    student_id = data['student_id']
    assignment_content = data['assignment_content']
    rubric = data['rubric']

    db: Session = next(get_db())

    # 1. Evaluate Current Assignment
    evaluation_feedback, grade = get_evaluation_feedback(assignment_content, rubric)

    # 2. Save Assignment to Database
    db_assignment = Assignment(student_id=student_id, content=assignment_content, rubric=rubric, evaluation_feedback=evaluation_feedback, grade=grade)
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)

    # 3. Generate Personalized Feedback
    # Retrieve all evaluation_feedback entries for the student
    feedback_history = [a.evaluation_feedback for a in db.query(Assignment).filter(Assignment.student_id == student_id).all()]
    personalized_feedback = get_personalized_feedback(feedback_history)

    return jsonify({
        'evaluation_feedback': evaluation_feedback,
        'grade': grade,
        'personalized_feedback': personalized_feedback
    }), 200

@app.route('/assignments/<int:student_id>', methods=['GET'])
def get_assignments(student_id):
    db: Session = next(get_db())
    assignments = db.query(Assignment).filter(Assignment.student_id == student_id).all()
    assignment_list = []
    for assignment in assignments:
        assignment_list.append({
            'id': assignment.id,
            'content': assignment.content,
            'rubric': assignment.rubric,
            'submission_date': assignment.submission_date.isoformat(),
            'evaluation_feedback': assignment.evaluation_feedback,
            'grade': assignment.grade
        })
    return jsonify(assignment_list), 200

if __name__ == '__main__':
    app.run(debug=True)
