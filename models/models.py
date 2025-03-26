from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    department_id = Column(Integer, ForeignKey("departments.id"))
    job = Column(String(50))
    time = Column(Integer())

    department = relationship("Department", back_populates="users")


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), unique=True)
    description = Column(String(255))

    defect_categories = relationship("DefectCategory", back_populates="department")
    users = relationship("User", back_populates="department")


class Part(Base):
    __tablename__ = "parts"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    department_id =  Column(Integer, ForeignKey("departments.id"))

    defects = relationship("Defect", back_populates="part")
    department = relationship("Department")


class DefectCategory(Base):
    __tablename__ = "defect_categories"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), unique=True)
    department_id = Column(Integer, ForeignKey("departments.id"))

    department = relationship("Department", back_populates="defect_categories")


class Defect(Base):
    __tablename__ = "defects"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), unique=True)
    description = Column(String(255), unique=True)
    part_id = Column(Integer, ForeignKey("parts.id"))
    defect_category_id = Column(Integer, ForeignKey("defect_categories.id"))

    part = relationship("Part", back_populates="defects")
    defect_category = relationship("DefectCategory")


class Quality(Base):
    __tablename__ = "quality"

    id = Column(Integer, primary_key=True)
    pass_fail = Column(Boolean)
    defect_count = Column(Integer)
    part_id = Column(Integer, ForeignKey("parts.id"))

    part = relationship("Part")
