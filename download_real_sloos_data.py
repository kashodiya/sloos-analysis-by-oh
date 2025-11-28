#!/usr/bin/env python3
"""
Download Real SLOOS Data from FRED (Federal Reserve Economic Data)

This script downloads actual SLOOS survey data from the St. Louis Federal Reserve's
FRED database and loads it into the SQLite database.
"""

import requests
import pandas as pd
from datetime import datetime
from database import LendingStandard, LoanDemand, get_session

# FRED SLOOS Series Mapping
# Format: 'FRED_CODE': ('Category Name', 'Type', 'Bank Type')

LENDING_STANDARDS_SERIES = {
    # Commercial & Industrial Loans
    'DRTSCILM': ('Commercial & Industrial Loans - Large Firms', 'net_tightening', 'Domestic'),
    'DRTSCIS': ('Commercial & Industrial Loans - Small Firms', 'net_tightening', 'Domestic'),
    
    # Residential Mortgages
    'DRTSSP': ('Residential Mortgages - Prime', 'net_tightening', 'Domestic'),
    
    # Consumer Loans
    'DRTSCLCC': ('Consumer Credit Cards', 'net_tightening', 'Domestic'),
    'STDSAUTO': ('Auto Loans', 'net_tightening', 'Domestic'),
}

LOAN_DEMAND_SERIES = {
    # Commercial & Industrial Loans
    'DRSDCILM': ('Commercial & Industrial Loans - Large Firms', 'net_demand', 'Domestic'),
    'DRSDCIS': ('Commercial & Industrial Loans - Small Firms', 'net_demand', 'Domestic'),
    
    # Residential Mortgages
    'DRSDSP': ('Residential Mortgages - Prime', 'net_demand', 'Domestic'),
    
    # Consumer Loans
    'DRSDCL': ('Consumer Loans - Other', 'net_demand', 'Domestic'),
}


class RealSLOOSDataDownloader:
    """Download and process real SLOOS data from FRED"""
    
    def __init__(self):
        self.base_url = "https://fred.stlouisfed.org/graph/fredgraph.csv"
        self.session = get_session()
        self.downloaded_data = {}
        
    def download_series(self, series_code):
        """Download a single FRED series as CSV"""
        try:
            url = f"{self.base_url}?id={series_code}"
            response = requests.get(url, timeout=15)
            
            if response.status_code == 200:
                df = pd.read_csv(pd.io.common.StringIO(response.text))
                df.columns = ['date', 'value']
                df['date'] = pd.to_datetime(df['date'])
                df['value'] = pd.to_numeric(df['value'], errors='coerce')
                df = df.dropna()
                
                print(f"✅ Downloaded {series_code}: {len(df)} observations")
                return df
            else:
                print(f"❌ Failed to download {series_code}: HTTP {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error downloading {series_code}: {e}")
            return None
    
    def download_all_series(self):
        """Download all SLOOS series from FRED"""
        print("=" * 80)
        print("DOWNLOADING REAL SLOOS DATA FROM FRED")
        print("=" * 80)
        
        print("\n📊 Downloading Lending Standards Data...")
        for code, (category, data_type, bank_type) in LENDING_STANDARDS_SERIES.items():
            df = self.download_series(code)
            if df is not None:
                self.downloaded_data[code] = {
                    'data': df,
                    'category': category,
                    'type': data_type,
                    'bank_type': bank_type,
                    'series_type': 'lending_standards'
                }
        
        print("\n📈 Downloading Loan Demand Data...")
        for code, (category, data_type, bank_type) in LOAN_DEMAND_SERIES.items():
            df = self.download_series(code)
            if df is not None:
                self.downloaded_data[code] = {
                    'data': df,
                    'category': category,
                    'type': data_type,
                    'bank_type': bank_type,
                    'series_type': 'loan_demand'
                }
        
        print(f"\n✅ Successfully downloaded {len(self.downloaded_data)} series")
        return len(self.downloaded_data) > 0
    
    def clear_existing_data(self):
        """Clear existing sample data from database"""
        try:
            print("\n🗑️  Clearing existing sample data...")
            self.session.query(LendingStandard).delete()
            self.session.query(LoanDemand).delete()
            self.session.commit()
            print("✅ Existing data cleared")
            return True
        except Exception as e:
            print(f"❌ Error clearing data: {e}")
            self.session.rollback()
            return False
    
    def load_to_database(self):
        """Load downloaded data into SQLite database"""
        if not self.downloaded_data:
            print("❌ No data to load")
            return False
        
        print("\n💾 Loading data into database...")
        
        records_added = 0
        
        for code, info in self.downloaded_data.items():
            df = info['data']
            category = info['category']
            bank_type = info['bank_type']
            series_type = info['series_type']
            
            for _, row in df.iterrows():
                survey_date = row['date'].date()
                net_value = row['value']
                
                if series_type == 'lending_standards':
                    # For lending standards, net_tightening is the value
                    # We'll estimate the components (this is a simplification)
                    if net_value > 0:
                        tightened_pct = min(100, abs(net_value) + 50)
                        eased_pct = max(0, 50 - abs(net_value))
                    else:
                        tightened_pct = max(0, 50 - abs(net_value))
                        eased_pct = min(100, abs(net_value) + 50)
                    
                    unchanged_pct = max(0, 100 - tightened_pct - eased_pct)
                    
                    record = LendingStandard(
                        survey_date=survey_date,
                        loan_category=category,
                        standard_type='Overall Standards',
                        tightened_pct=tightened_pct,
                        eased_pct=eased_pct,
                        unchanged_pct=unchanged_pct,
                        net_tightening=net_value,
                        bank_type=bank_type
                    )
                    self.session.add(record)
                    records_added += 1
                    
                elif series_type == 'loan_demand':
                    # For loan demand, net_demand is the value
                    if net_value > 0:
                        stronger_pct = min(100, abs(net_value) + 50)
                        weaker_pct = max(0, 50 - abs(net_value))
                    else:
                        stronger_pct = max(0, 50 - abs(net_value))
                        weaker_pct = min(100, abs(net_value) + 50)
                    
                    unchanged_pct = max(0, 100 - stronger_pct - weaker_pct)
                    
                    record = LoanDemand(
                        survey_date=survey_date,
                        loan_category=category,
                        stronger_pct=stronger_pct,
                        weaker_pct=weaker_pct,
                        unchanged_pct=unchanged_pct,
                        net_demand=net_value,
                        bank_type=bank_type
                    )
                    self.session.add(record)
                    records_added += 1
        
        try:
            self.session.commit()
            print(f"✅ Successfully loaded {records_added} records into database")
            return True
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            self.session.rollback()
            return False
    
    def get_summary(self):
        """Get summary of loaded data"""
        try:
            lending_count = self.session.query(LendingStandard).count()
            demand_count = self.session.query(LoanDemand).count()
            
            if lending_count > 0:
                min_date = self.session.query(LendingStandard.survey_date).order_by(
                    LendingStandard.survey_date).first()[0]
                max_date = self.session.query(LendingStandard.survey_date).order_by(
                    LendingStandard.survey_date.desc()).first()[0]
                
                categories = self.session.query(LendingStandard.loan_category).distinct().all()
                category_count = len(categories)
                
                print("\n" + "=" * 80)
                print("DATA SUMMARY")
                print("=" * 80)
                print(f"📊 Lending Standards Records: {lending_count}")
                print(f"📈 Loan Demand Records: {demand_count}")
                print(f"📅 Date Range: {min_date} to {max_date}")
                print(f"🏦 Loan Categories: {category_count}")
                print("\nCategories:")
                for cat in categories:
                    print(f"  - {cat[0]}")
                print("=" * 80)
                
        except Exception as e:
            print(f"❌ Error getting summary: {e}")
    
    def close(self):
        """Close database session"""
        self.session.close()


def main():
    """Main execution function"""
    print("\n" + "=" * 80)
    print("REAL SLOOS DATA DOWNLOADER")
    print("Downloading data from FRED (Federal Reserve Economic Data)")
    print("=" * 80 + "\n")
    
    downloader = RealSLOOSDataDownloader()
    
    try:
        # Step 1: Download all series
        if not downloader.download_all_series():
            print("\n❌ Failed to download data")
            return False
        
        # Step 2: Clear existing sample data
        if not downloader.clear_existing_data():
            print("\n❌ Failed to clear existing data")
            return False
        
        # Step 3: Load real data into database
        if not downloader.load_to_database():
            print("\n❌ Failed to load data into database")
            return False
        
        # Step 4: Show summary
        downloader.get_summary()
        
        print("\n✅ SUCCESS! Real SLOOS data has been loaded into the database.")
        print("🚀 You can now use the application with real Federal Reserve data!\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False
        
    finally:
        downloader.close()


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
