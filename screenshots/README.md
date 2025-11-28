# SLOOS Application Screenshots

This directory contains screenshots of the SLOOS Interactive Data Analysis Application.

## Screenshots

### 1. Executive Dashboard
**File:** `01_executive_dashboard.png`

The main dashboard showing:
- Key metrics (Total Records, Latest Quarter, Data Sources, Loan Categories)
- Lending Standards Trends chart
- Loan Demand Trends chart
- Recent data table
- Real-time data from Federal Reserve (FRED)

### 2. Data Explorer
**File:** `02_data_explorer.png`

Interactive data exploration page featuring:
- Filter controls (Date Range, Loan Category, Metric Type)
- Data visualization charts
- Detailed data table with sorting and filtering
- Export capabilities

### 3. Data Explorer (Scrolled View)
**File:** `03_data_explorer_scrolled.png`

Detailed view of the Data Explorer showing:
- Lower section of the page
- Additional data visualizations
- Complete data table

### 4. AI Analysis
**File:** `04_ai_analysis.png`

AI-powered analysis page with:
- AWS Bedrock integration (Claude Sonnet 4.5)
- Period comparison tools
- AI-generated insights
- Trend analysis
- Natural language explanations

### 5. Data Management
**File:** `05_data_management.png`

Data management interface showing:
- Current database statistics
- Data source information (FRED)
- Update controls
- Data verification tools
- Real data status

### 6. Dashboard (Detail View)
**File:** `06_dashboard_scrolled.png`

Scrolled view of the dashboard highlighting:
- Chart details
- Data trends
- Additional metrics

## Technical Details

- **Resolution:** 1920x1080 (Full HD)
- **Format:** PNG
- **Capture Method:** Playwright (Chromium)
- **Application:** SLOOS Interactive Data Analysis
- **Port:** 7251
- **Data Source:** Federal Reserve Economic Data (FRED)

## Regenerating Screenshots

To regenerate these screenshots, run:

```bash
uv run python take_screenshots.py
```

This will:
1. Launch a headless Chromium browser
2. Navigate through all application pages
3. Capture full-page and detail screenshots
4. Save them to this directory

## Notes

- Screenshots show real SLOOS data from the Federal Reserve
- All data is current as of the screenshot capture date
- The application uses AWS Bedrock for AI-powered analysis
- Database contains 929 real records spanning 1990-2025
