from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import declarative_base, relationship

engine = create_engine('postgresql+psycopg2://postgres:default@localhost:5432/university_db', echo=True)

Base = declarative_base()


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String(5))

    def __repr__(self):
        return f"Group(id={self.id}, name={self.name})"

association_table = Table(
    "association",
    Base.metadata,
    Column("student_id", ForeignKey("students.id"), primary_key=True),
    Column("course_id", ForeignKey("courses.id"), primary_key=True),
)

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)

    courses = relationship(
        "Course", secondary=association_table, backref="students"
    )

    def __repr__(self):
        return f"Student(id={self.id}, group={self.group_id}, first_name={self.first_name}, last_name={self.last_name})"


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(250), nullable=False)

    def __repr__(self):
        return f"Course(id={self.id}, name={self.name}, description={self.description})"

