import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from database import SurveyResponse, LendingStandard, LoanDemand, get_session
import io

class SLOOSDataIngestion:
    def __init__(self):
        self.base_url = "https://www.federalreserve.gov/data/sloos.htm"
        self.session = get_session()
    
    def fetch_available_data_files(self):
        """Fetch list of available SLOOS data files from Federal Reserve website"""
        try:
            response = requests.get(self.base_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            data_links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                if any(ext in href.lower() for ext in ['.csv', '.xlsx', '.xls']):
                    if not href.startswith('http'):
                        href = f"https://www.federalreserve.gov{href}"
                    data_links.append({
                        'url': href,
                        'text': link.get_text(strip=True),
                        'type': 'csv' if '.csv' in href.lower() else 'excel'
                    })
            
            return data_links
        except Exception as e:
            print(f"Error fetching data files: {e}")
            return []
    
    def load_sample_data(self):
        """
        DEPRECATED: This function loads synthetic sample data.
        
        ⚠️ DO NOT USE - Use real SLOOS data from FRED instead.
        
        To load real data, run:
            ./update_sloos_data.sh
        or
            uv run python download_real_sloos_data.py
        """
        return False, "❌ Sample data is deprecated. Use real SLOOS data from FRED instead. Run: ./update_sloos_data.sh"
    
    def get_data_summary(self):
        """Get summary of data in database"""
        try:
            lending_count = self.session.query(LendingStandard).count()
            demand_count = self.session.query(LoanDemand).count()
            
            if lending_count > 0:
                min_date = self.session.query(LendingStandard.survey_date).order_by(LendingStandard.survey_date).first()[0]
                max_date = self.session.query(LendingStandard.survey_date).order_by(LendingStandard.survey_date.desc()).first()[0]
            else:
                min_date = max_date = None
            
            return {
                'lending_standards_count': lending_count,
                'loan_demand_count': demand_count,
                'date_range': (min_date, max_date) if min_date else None
            }
        except Exception as e:
            return {'error': str(e)}
    
    def close(self):
        self.session.close()
