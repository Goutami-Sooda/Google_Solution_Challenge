from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Student, Assignment

engine = create_engine('sqlite:///evaluator.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Create dummy students
student1 = Student(name='Alice')
student2 = Student(name='Bob')
session.add_all([student1, student2])
session.commit()

# Create dummy assignments
assignment1 = Assignment(student_id=student1.id, content='Solve the equation x + 5 = 10', rubric='Correctness of the solution', evaluation_feedback='Correct solution', grade='A')
assignment2 = Assignment(student_id=student1.id, content='Explain the concept of gravity', rubric='Clarity and accuracy of explanation', evaluation_feedback='Good explanation, but could be more detailed', grade='B')
assignment3 = Assignment(student_id=student2.id, content='Write a program to print "Hello, world!"', rubric='Correctness and efficiency of the code', evaluation_feedback='Correct code', grade='A')
session.add_all([assignment1, assignment2, assignment3])
session.commit()

print('Database initialized with dummy data')
