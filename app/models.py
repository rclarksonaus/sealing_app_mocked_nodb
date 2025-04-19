from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

grade_formfit_table = Table(
    'grade_formfit', Base.metadata,
    Column('grade_id', Integer, ForeignKey('grades.id')),
    Column('form_type', String(50))
)

grade_movement_table = Table(
    'grade_movement', Base.metadata,
    Column('grade_id', Integer, ForeignKey('grades.id')),
    Column('movement_type', String(50))
)

class Grade(Base):
    __tablename__ = 'grades'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    temp_min = Column(Float)
    temp_max = Column(Float)
    pressure_min = Column(Float)
    pressure_max = Column(Float)
    usage_score = Column(Float, default=0.0)
    recommended_by = Column(String, nullable=True)

    media_resistance = relationship("MediaResistance", back_populates="grade")
    form_fits = relationship("FormFit", secondary=grade_formfit_table)
    movement_supported = relationship("MovementSupport", secondary=grade_movement_table)

class MediaResistance(Base):
    __tablename__ = 'media_resistance'

    id = Column(Integer, primary_key=True, index=True)
    grade_id = Column(Integer, ForeignKey('grades.id'))
    media_type = Column(String)
    rating = Column(String)
    confidence = Column(String)

    grade = relationship("Grade", back_populates="media_resistance")

class FormFit(Base):
    __tablename__ = 'form_fits'
    id = Column(Integer, primary_key=True)
    form_type = Column(String, unique=True)

class MovementSupport(Base):
    __tablename__ = 'movement_supports'
    id = Column(Integer, primary_key=True)
    movement_type = Column(String, unique=True)
