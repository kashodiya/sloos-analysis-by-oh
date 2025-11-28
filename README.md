# 📊 SLOOS Interactive Data Analysis Application

A professional interactive data analysis application for the **Senior Loan Officer Opinion Survey (SLOOS)** with real Federal Reserve data and AI-powered insights using AWS Bedrock.

---

## 🚀 Quick Start

### Running the Application

```bash
# Start the application
./run.sh

# Or manually:
uv run streamlit run app.py --server.port=7251 --server.address=0.0.0.0
```

The application will be available at: `http://[YOUR-EC2-IP]:7251`

### Updating SLOOS Data

The application uses **real SLOOS data from FRED** (Federal Reserve Economic Data).

```bash
# Download/update the latest SLOOS data
./update_sloos_data.sh

# Or manually:
uv run python download_real_sloos_data.py
```

---

## 📊 Data Source

This application uses **real SLOOS data** downloaded from the Federal Reserve's FRED database:

### Current Data Coverage:
- **Lending Standards:** 521 records
- **Loan Demand:** 408 records  
- **Date Range:** 1990-Q2 to 2025-Q4
- **Total Records:** 929 real data points

### Available Loan Categories:
1. **Commercial & Industrial Loans** - Large Firms
2. **Commercial & Industrial Loans** - Small Firms
3. **Residential Mortgages** - Prime
4. **Consumer Credit Cards**
5. **Auto Loans**

### Data Updates:
- SLOOS surveys are published **quarterly** by the Federal Reserve
- Run `./update_sloos_data.sh` to download the latest data
- Data is automatically sourced from FRED's public API
- No API key required - uses public FRED data

---

## 🎯 Features

### 1. 📈 Executive Dashboard
- Real-time metrics from Federal Reserve data
- Trend visualizations for lending standards and loan demand
- Key performance indicators
- Interactive charts with Plotly

### 2. 🔍 Data Explorer
- Interactive filtering by date range and loan category
- Lending standards analysis with net tightening metrics
- Loan demand trends
- Detailed data tables
- Export capabilities

### 3. 🤖 AI-Powered Analysis
- **AWS Bedrock integration** (Claude Sonnet 4.5)
- Automated insights generation from real data
- Period-over-period comparisons
- Natural language summaries
- Trend analysis and predictions

### 4. 💾 Data Management
- View current data statistics
- Reload data from FRED
- Database management
- Data quality monitoring

---

## 🛠️ Technical Stack

- **Frontend:** Streamlit
- **Database:** SQLite
- **AI/ML:** AWS Bedrock (Claude Sonnet 4.5)
- **Data Source:** FRED (Federal Reserve Economic Data)
- **Package Manager:** UV
- **Python:** 3.11+
- **Visualization:** Plotly
- **Data Processing:** Pandas

---

## 📁 Project Structure

```
sloos-analysis-by-oh/
├── app.py                          # Main Streamlit application
├── database.py                     # Database models and setup
├── models.py                       # SQLAlchemy models
├── data_ingestion.py              # Data loading utilities
├── download_real_sloos_data.py    # FRED data downloader (REAL DATA)
├── update_sloos_data.sh           # Data update script
├── run.sh                         # Application startup script
├── sloos_data.db                  # SQLite database (with real data)
├── pyproject.toml                 # UV project configuration
└── README.md                      # This file
```

---

## 🔧 Installation & Setup

### Prerequisites
- Python 3.11+
- UV package manager
- AWS credentials (for Bedrock AI features)
- Internet connection (for FRED data download)

### Installation

```bash
# Clone the repository
cd /home/ec2-user/sloos/sloos-analysis-by-oh

# Install dependencies with UV
uv sync

# Download real SLOOS data
./update_sloos_data.sh

# Run the application
./run.sh
```

---

## 📊 Real Data Details

### FRED Series Used

**Lending Standards (Net % Tightening):**
- `DRTSCILM` - C&I Loans to Large/Medium Firms
- `DRTSCIS` - C&I Loans to Small Firms
- `DRTSSP` - Prime Residential Mortgages
- `DRTSCLCC` - Consumer Credit Cards
- `STDSAUTO` - Auto Loans

**Loan Demand (Net % Stronger):**
- `DRSDCILM` - C&I Loans to Large/Medium Firms
- `DRSDCIS` - C&I Loans to Small Firms
- `DRSDSP` - Prime Residential Mortgages
- `DRSDCL` - Other Consumer Loans

### Data Interpretation

**Net Tightening (Lending Standards):**
- **Positive values:** More banks tightening than easing
- **Negative values:** More banks easing than tightening
- **Zero:** No net change

**Net Demand:**
- **Positive values:** More banks reporting stronger demand
- **Negative values:** More banks reporting weaker demand
- **Zero:** No net change

---

## 🤖 AI Analysis Features

The application uses **AWS Bedrock with Claude Sonnet 4.5** to provide:

1. **Automated Insights:** AI analyzes trends and patterns in real SLOOS data
2. **Period Comparisons:** Compare different time periods with AI-generated summaries
3. **Trend Detection:** Identify significant changes in lending standards or demand
4. **Natural Language Summaries:** Convert complex data into readable insights
5. **Predictive Analysis:** Understand potential future trends based on historical patterns

### AWS Configuration
- **Region:** us-east-1
- **Model:** anthropic.claude-sonnet-4-5-20250929-v1:0
- **Authentication:** EC2 IAM role (no credentials needed)

---

## 📘 Understanding SLOOS

### What is SLOOS?

The **Senior Loan Officer Opinion Survey on Bank Lending Practices (SLOOS)** is a **quarterly survey** conducted by the **Federal Reserve** to gather insights from senior loan officers at large domestic and foreign banks operating in the U.S.

### Why is SLOOS Important?

SLOOS is a **leading indicator** of credit conditions and economic sentiment. It is widely used by:

- **Central banks** to inform monetary policy
- **Economists** to assess financial stability
- **Investors and analysts** to anticipate credit cycles
- **Regulators** to monitor systemic risk

### Key Use Cases:
- Detecting **tightening or easing** of credit
- Understanding **sector-specific lending trends**
- Gauging **risk appetite** in the banking system
- Anticipating **recessions or recoveries** based on credit availability

---

## 🔗 External Resources

- 🔗 [SLOOS Main Page – Federal Reserve](https://www.federalreserve.gov/data/sloos.htm)
- 🔗 [FRED SLOOS Data](https://fred.stlouisfed.org/searchresults?st=SLOOS)
- 🔗 [Federal Reserve Data Download](https://www.federalreserve.gov/datadownload)

---

## 🚀 Usage Examples

### Example 1: View Latest Trends
1. Navigate to **Executive Dashboard**
2. View the latest survey date and metrics
3. Analyze trend charts for different loan categories

### Example 2: Compare Time Periods
1. Go to **AI Analysis** → **Period Comparison**
2. Select two date ranges (e.g., 2020-2021 vs 2023-2024)
3. Click "Compare Periods"
4. Review AI-generated insights

### Example 3: Export Data
1. Navigate to **Data Explorer**
2. Filter by loan category and date range
3. View detailed tables
4. Export data for further analysis

---

## 📝 Maintenance

### Updating Data

The Federal Reserve publishes SLOOS data quarterly. To update:

```bash
./update_sloos_data.sh
```

This will:
1. Download the latest data from FRED
2. Clear old data
3. Load new data into the database
4. Display a summary

### Database Management

The SQLite database is located at `sloos_data.db`. To reset:

```bash
rm sloos_data.db
uv run python download_real_sloos_data.py
```

---

## 🐛 Troubleshooting

### Application won't start
```bash
# Check if port 7251 is in use
netstat -tuln | grep 7251

# Kill existing process
pkill -f "streamlit.*7251"

# Restart
./run.sh
```

### Data download fails
```bash
# Check internet connectivity
curl -I https://fred.stlouisfed.org

# Try manual download
uv run python download_real_sloos_data.py
```

### AI features not working
- Verify AWS credentials are configured
- Check EC2 IAM role has Bedrock permissions
- Ensure region is set to us-east-1

---

## 📊 Data Quality

All data in this application comes directly from the Federal Reserve's FRED database:
- ✅ **Official source:** Federal Reserve Economic Data
- ✅ **Real data:** No synthetic or simulated data
- ✅ **Historical accuracy:** Data from 1990 to present
- ✅ **Quarterly updates:** Matches Fed publication schedule
- ✅ **Verified:** Cross-referenced with Fed publications

---

## 📄 License

This project is for educational and research purposes.

---

## 🙏 Acknowledgments

- **Federal Reserve** for publishing SLOOS data
- **FRED** (Federal Reserve Economic Data) for data access
- **AWS Bedrock** for AI capabilities
- **Streamlit** for the application framework

---

## 📧 Support

For issues or questions:
1. Check the troubleshooting section
2. Review FRED documentation
3. Verify AWS Bedrock configuration

---

**Built with real Federal Reserve data for professional SLOOS analysis** 📊
