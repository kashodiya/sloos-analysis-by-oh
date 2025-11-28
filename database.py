from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class SurveyResponse(Base):
    __tablename__ = 'survey_responses'
    
    id = Column(Integer, primary_key=True)
    survey_date = Column(Date, nullable=False)
    question_id = Column(String(100), nullable=False)
    question_text = Column(Text)
    category = Column(String(100))
    loan_type = Column(String(100))
    bank_type = Column(String(50))
    response_value = Column(Float)
    response_text = Column(Text)
    net_percentage = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class LendingStandard(Base):
    __tablename__ = 'lending_standards'
    
    id = Column(Integer, primary_key=True)
    survey_date = Column(Date, nullable=False)
    loan_category = Column(String(100), nullable=False)
    standard_type = Column(String(100))
    tightened_pct = Column(Float)
    eased_pct = Column(Float)
    unchanged_pct = Column(Float)
    net_tightening = Column(Float)
    bank_type = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

class LoanDemand(Base):
    __tablename__ = 'loan_demand'
    
    id = Column(Integer, primary_key=True)
    survey_date = Column(Date, nullable=False)
    loan_category = Column(String(100), nullable=False)
    stronger_pct = Column(Float)
    weaker_pct = Column(Float)
    unchanged_pct = Column(Float)
    net_demand = Column(Float)
    bank_type = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

class AnalysisCache(Base):
    __tablename__ = 'analysis_cache'
    
    id = Column(Integer, primary_key=True)
    query_hash = Column(String(64), unique=True, nullable=False)
    query_text = Column(Text, nullable=False)
    analysis_result = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_database(db_path='sloos_data.db'):
    engine = create_engine(f'sqlite:///{db_path}')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return engine, Session

def get_session(db_path='sloos_data.db'):
    engine = create_engine(f'sqlite:///{db_path}')
    Session = sessionmaker(bind=engine)
    return Session()
