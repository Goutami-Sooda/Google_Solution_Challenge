import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def get_evaluation_feedback(content, rubric):
    prompt = f"Evaluate the following assignment based on the rubric:\nAssignment: {content}\nRubric: {rubric}\n\nProvide feedback and a grade."
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
    )
    feedback = chat_completion.choices[0].message.content
    grade = "A"  # Placeholder - can be extracted from the feedback if needed
    return feedback, grade

def get_personalized_feedback(feedback_history):
    history_str = "\n".join(feedback_history)
    prompt = f"Analyze the following feedback history and provide personalized advice:\n{history_str}\n\nWhat topics should the student focus on?"

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
    )
    personalized_feedback = chat_completion.choices[0].message.content
    return personalized_feedback
