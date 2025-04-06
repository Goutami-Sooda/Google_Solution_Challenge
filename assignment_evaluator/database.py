from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    assignments = relationship("Assignment", back_populates="student")

class Assignment(Base):
    __tablename__ = 'assignments'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    content = Column(Text)
    rubric = Column(Text)
    submission_date = Column(DateTime, server_default=func.now())
    evaluation_feedback = Column(Text)
    grade = Column(String)
    student = relationship("Student", back_populates="assignments")

engine = create_engine('sqlite:///evaluator.db')
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Example usage (to be implemented):
# def get_student_assignments(db: Session, student_id: int):
#     return db.query(Assignment).filter(Assignment.student_id == student_id).all()

# def create_assignment(db: Session, student_id: int, content: str, rubric: str, evaluation_feedback: str, grade: str):
#     db_assignment = Assignment(student_id=student_id, content=content, rubric=rubric, evaluation_feedback=evaluation_feedback, grade=grade)
#     db.add(db_assignment)
#     db.commit()
#     db.refresh(db_assignment)
#     return db_assignment
