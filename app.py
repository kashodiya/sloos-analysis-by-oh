import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from database import init_database, get_session, LendingStandard, LoanDemand
from data_ingestion import SLOOSDataIngestion
from bedrock_client import BedrockAnalyzer
from sqlalchemy import func

st.set_page_config(
    page_title="SLOOS Interactive Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        padding: 0 2rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_app():
    """Initialize database and connections"""
    init_database()
    return BedrockAnalyzer(region_name='us-east-1')

@st.cache_data(ttl=3600)
def load_lending_standards_data():
    """Load lending standards data from database"""
    session = get_session()
    query = session.query(LendingStandard).all()
    data = [{
        'survey_date': record.survey_date,
        'loan_category': record.loan_category,
        'tightened_pct': record.tightened_pct,
        'eased_pct': record.eased_pct,
        'unchanged_pct': record.unchanged_pct,
        'net_tightening': record.net_tightening,
        'bank_type': record.bank_type
    } for record in query]
    session.close()
    return pd.DataFrame(data)

@st.cache_data(ttl=3600)
def load_loan_demand_data():
    """Load loan demand data from database"""
    session = get_session()
    query = session.query(LoanDemand).all()
    data = [{
        'survey_date': record.survey_date,
        'loan_category': record.loan_category,
        'stronger_pct': record.stronger_pct,
        'weaker_pct': record.weaker_pct,
        'unchanged_pct': record.unchanged_pct,
        'net_demand': record.net_demand,
        'bank_type': record.bank_type
    } for record in query]
    session.close()
    return pd.DataFrame(data)

def main():
    st.markdown('<div class="main-header">📊 SLOOS Interactive Data Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Senior Loan Officer Opinion Survey - Powered by AWS Bedrock & Claude 3.5 Sonnet</div>', unsafe_allow_html=True)
    
    bedrock_analyzer = initialize_app()
    
    with st.sidebar:
        st.image("https://www.federalreserve.gov/images/fed-logo.png", width=200)
        st.title("Navigation")
        
        page = st.radio(
            "Select Analysis View",
            ["📈 Dashboard", "🔍 Data Explorer", "🤖 AI Analysis", "💾 Data Management"],
            label_visibility="collapsed"
        )
        
        st.divider()
        st.markdown("### About SLOOS")
        st.info("""
        The Senior Loan Officer Opinion Survey provides insights into:
        - Lending standards changes
        - Loan demand trends
        - Credit risk perceptions
        - Economic sentiment
        """)
        
        st.divider()
        st.markdown("### System Info")
        st.caption(f"🤖 Model: Claude 3.5 Sonnet")
        st.caption(f"🗄️ Database: SQLite")
        st.caption(f"☁️ Region: us-east-1")
    
    if page == "📈 Dashboard":
        show_dashboard()
    elif page == "🔍 Data Explorer":
        show_data_explorer()
    elif page == "🤖 AI Analysis":
        show_ai_analysis(bedrock_analyzer)
    elif page == "💾 Data Management":
        show_data_management()

def show_dashboard():
    """Main dashboard with key metrics and visualizations"""
    st.header("📈 Executive Dashboard")
    
    df_lending = load_lending_standards_data()
    df_demand = load_loan_demand_data()
    
    if df_lending.empty:
        st.warning("⚠️ No data available. Please load data from the Data Management page.")
        return
    
    # Ensure survey_date is datetime type
    df_lending['survey_date'] = pd.to_datetime(df_lending['survey_date'])
    df_demand['survey_date'] = pd.to_datetime(df_demand['survey_date'])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        latest_date = df_lending['survey_date'].max()
        st.metric("Latest Survey", latest_date.strftime("%Y-%m-%d") if latest_date else "N/A")
    
    with col2:
        avg_tightening = df_lending[df_lending['survey_date'] == latest_date]['net_tightening'].mean()
        st.metric("Avg Net Tightening", f"{avg_tightening:.1f}%", 
                 delta=f"{avg_tightening - 20:.1f}%" if avg_tightening else None)
    
    with col3:
        avg_demand = df_demand[df_demand['survey_date'] == latest_date]['net_demand'].mean()
        st.metric("Avg Net Demand", f"{avg_demand:.1f}%",
                 delta=f"{avg_demand - 5:.1f}%" if avg_demand else None)
    
    with col4:
        total_categories = df_lending['loan_category'].nunique()
        st.metric("Loan Categories", total_categories)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Net Tightening Trends by Loan Category")
        
        df_trend = df_lending.groupby(['survey_date', 'loan_category'])['net_tightening'].mean().reset_index()
        
        fig = px.line(df_trend, x='survey_date', y='net_tightening', 
                     color='loan_category',
                     title='Lending Standards Over Time',
                     labels={'net_tightening': 'Net Tightening (%)', 'survey_date': 'Survey Date'})
        fig.update_layout(height=400, hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Net Loan Demand by Category")
        
        df_demand_trend = df_demand.groupby(['survey_date', 'loan_category'])['net_demand'].mean().reset_index()
        
        fig = px.line(df_demand_trend, x='survey_date', y='net_demand',
                     color='loan_category',
                     title='Loan Demand Over Time',
                     labels={'net_demand': 'Net Demand (%)', 'survey_date': 'Survey Date'})
        fig.update_layout(height=400, hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    st.subheader("Latest Quarter Snapshot")
    
    col1, col2 = st.columns(2)
    
    with col1:
        latest_lending = df_lending[df_lending['survey_date'] == latest_date].groupby('loan_category')['net_tightening'].mean().sort_values(ascending=False)
        
        fig = go.Figure(go.Bar(
            x=latest_lending.values,
            y=latest_lending.index,
            orientation='h',
            marker=dict(color=latest_lending.values, colorscale='RdYlGn_r')
        ))
        fig.update_layout(
            title='Net Tightening by Category (Latest Quarter)',
            xaxis_title='Net Tightening (%)',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        latest_demand = df_demand[df_demand['survey_date'] == latest_date].groupby('loan_category')['net_demand'].mean().sort_values(ascending=False)
        
        fig = go.Figure(go.Bar(
            x=latest_demand.values,
            y=latest_demand.index,
            orientation='h',
            marker=dict(color=latest_demand.values, colorscale='RdYlGn')
        ))
        fig.update_layout(
            title='Net Demand by Category (Latest Quarter)',
            xaxis_title='Net Demand (%)',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

def show_data_explorer():
    """Detailed data exploration interface"""
    st.header("🔍 Data Explorer")
    
    df_lending = load_lending_standards_data()
    df_demand = load_loan_demand_data()
    
    if df_lending.empty:
        st.warning("⚠️ No data available. Please load data from the Data Management page.")
        return
    
    # Ensure survey_date is datetime type
    df_lending['survey_date'] = pd.to_datetime(df_lending['survey_date'])
    df_demand['survey_date'] = pd.to_datetime(df_demand['survey_date'])
    
    tab1, tab2, tab3 = st.tabs(["Lending Standards", "Loan Demand", "Comparative Analysis"])
    
    with tab1:
        st.subheader("Lending Standards Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected_categories = st.multiselect(
                "Select Loan Categories",
                options=df_lending['loan_category'].unique(),
                default=df_lending['loan_category'].unique()[:3]
            )
        
        with col2:
            selected_bank_type = st.selectbox(
                "Bank Type",
                options=['All'] + list(df_lending['bank_type'].unique())
            )
        
        with col3:
            # Convert to date for date_input widget
            min_date = df_lending['survey_date'].min().date()
            max_date = df_lending['survey_date'].max().date()
            date_range = st.date_input(
                "Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
        
        filtered_df = df_lending[df_lending['loan_category'].isin(selected_categories)]
        if selected_bank_type != 'All':
            filtered_df = filtered_df[filtered_df['bank_type'] == selected_bank_type]
        if len(date_range) == 2:
            # Convert date_range to datetime for comparison
            start_date = pd.Timestamp(date_range[0])
            end_date = pd.Timestamp(date_range[1])
            filtered_df = filtered_df[
                (filtered_df['survey_date'] >= start_date) &
                (filtered_df['survey_date'] <= end_date)
            ]
        
        fig = px.line(filtered_df, x='survey_date', y='net_tightening',
                     color='loan_category',
                     title='Net Tightening Over Time',
                     labels={'net_tightening': 'Net Tightening (%)', 'survey_date': 'Date'})
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(filtered_df.sort_values('survey_date', ascending=False), use_container_width=True)
    
    with tab2:
        st.subheader("Loan Demand Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_categories_demand = st.multiselect(
                "Select Loan Categories",
                options=df_demand['loan_category'].unique(),
                default=df_demand['loan_category'].unique()[:3],
                key='demand_categories'
            )
        
        with col2:
            selected_bank_type_demand = st.selectbox(
                "Bank Type",
                options=['All'] + list(df_demand['bank_type'].unique()),
                key='demand_bank_type'
            )
        
        filtered_demand = df_demand[df_demand['loan_category'].isin(selected_categories_demand)]
        if selected_bank_type_demand != 'All':
            filtered_demand = filtered_demand[filtered_demand['bank_type'] == selected_bank_type_demand]
        
        fig = px.line(filtered_demand, x='survey_date', y='net_demand',
                     color='loan_category',
                     title='Net Loan Demand Over Time',
                     labels={'net_demand': 'Net Demand (%)', 'survey_date': 'Date'})
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(filtered_demand.sort_values('survey_date', ascending=False), use_container_width=True)
    
    with tab3:
        st.subheader("Comparative Analysis")
        
        selected_category = st.selectbox(
            "Select Loan Category for Comparison",
            options=df_lending['loan_category'].unique()
        )
        
        category_lending = df_lending[df_lending['loan_category'] == selected_category]
        category_demand = df_demand[df_demand['loan_category'] == selected_category]
        
        merged_data = pd.merge(
            category_lending[['survey_date', 'net_tightening', 'bank_type']],
            category_demand[['survey_date', 'net_demand', 'bank_type']],
            on=['survey_date', 'bank_type'],
            how='inner'
        )
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=merged_data['survey_date'], y=merged_data['net_tightening'],
                                mode='lines+markers', name='Net Tightening',
                                line=dict(color='red', width=2)))
        fig.add_trace(go.Scatter(x=merged_data['survey_date'], y=merged_data['net_demand'],
                                mode='lines+markers', name='Net Demand',
                                line=dict(color='green', width=2)))
        fig.update_layout(
            title=f'Standards vs Demand: {selected_category}',
            xaxis_title='Date',
            yaxis_title='Percentage (%)',
            hovermode='x unified',
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        
        correlation = merged_data[['net_tightening', 'net_demand']].corr().iloc[0, 1]
        st.metric("Correlation (Tightening vs Demand)", f"{correlation:.3f}")

def show_ai_analysis(bedrock_analyzer):
    """AI-powered analysis using AWS Bedrock"""
    st.header("🤖 AI-Powered Analysis")
    
    df_lending = load_lending_standards_data()
    df_demand = load_loan_demand_data()
    
    if df_lending.empty:
        st.warning("⚠️ No data available. Please load data from the Data Management page.")
        return
    
    # Ensure survey_date is datetime type
    df_lending['survey_date'] = pd.to_datetime(df_lending['survey_date'])
    df_demand['survey_date'] = pd.to_datetime(df_demand['survey_date'])
    
    tab1, tab2, tab3, tab4 = st.tabs(["Executive Summary", "Sentiment Analysis", "Custom Query", "Period Comparison"])
    
    with tab1:
        st.subheader("📋 Executive Summary")
        st.write("Generate an AI-powered executive summary of current SLOOS trends.")
        
        if st.button("Generate Executive Summary", type="primary"):
            with st.spinner("Analyzing data with Claude..."):
                latest_date = df_lending['survey_date'].max()
                recent_data = df_lending[df_lending['survey_date'] == latest_date]
                
                data_summary = f"""
                Latest Survey Date: {latest_date}
                
                Lending Standards Summary:
                {recent_data.groupby('loan_category')['net_tightening'].mean().to_string()}
                
                Average Net Tightening: {recent_data['net_tightening'].mean():.2f}%
                
                Loan Demand Summary:
                {df_demand[df_demand['survey_date'] == latest_date].groupby('loan_category')['net_demand'].mean().to_string()}
                """
                
                summary = bedrock_analyzer.summarize_trends(data_summary)
                st.markdown("### Analysis Results")
                st.markdown(summary)
    
    with tab2:
        st.subheader("💭 Sentiment Analysis")
        
        selected_category = st.selectbox(
            "Select Loan Category",
            options=df_lending['loan_category'].unique(),
            key='sentiment_category'
        )
        
        if st.button("Analyze Sentiment", type="primary"):
            with st.spinner("Performing sentiment analysis..."):
                category_data = df_lending[df_lending['loan_category'] == selected_category]
                recent_trend = category_data.tail(4)
                
                data_summary = f"""
                Loan Category: {selected_category}
                Recent Quarters Net Tightening:
                {recent_trend[['survey_date', 'net_tightening', 'bank_type']].to_string()}
                
                Average Net Tightening (Recent): {recent_trend['net_tightening'].mean():.2f}%
                Trend Direction: {'Increasing' if recent_trend['net_tightening'].iloc[-1] > recent_trend['net_tightening'].iloc[0] else 'Decreasing'}
                """
                
                sentiment = bedrock_analyzer.sentiment_analysis(data_summary, selected_category)
                st.markdown("### Sentiment Analysis Results")
                st.markdown(sentiment)
    
    with tab3:
        st.subheader("❓ Custom Query")
        st.write("Ask any question about the SLOOS data and get AI-powered insights.")
        
        query = st.text_area(
            "Enter your question:",
            placeholder="e.g., How have lending standards for small businesses changed since 2020?",
            height=100
        )
        
        if st.button("Get Answer", type="primary") and query:
            with st.spinner("Processing your query..."):
                data_context = f"""
                Available Data Summary:
                - Date Range: {df_lending['survey_date'].min()} to {df_lending['survey_date'].max()}
                - Loan Categories: {', '.join(df_lending['loan_category'].unique())}
                - Bank Types: {', '.join(df_lending['bank_type'].unique())}
                
                Recent Lending Standards:
                {df_lending.tail(20).to_string()}
                
                Recent Loan Demand:
                {df_demand.tail(20).to_string()}
                """
                
                answer = bedrock_analyzer.custom_query(query, data_context)
                st.markdown("### Answer")
                st.markdown(answer)
    
    with tab4:
        st.subheader("📊 Period Comparison")
        
        col1, col2 = st.columns(2)
        
        with col1:
            min_date = df_lending['survey_date'].min().date()
            max_date = df_lending['survey_date'].max().date()
            period1_dates = st.date_input(
                "Period 1",
                value=(min_date, min_date + timedelta(days=365)),
                key='period1'
            )
        
        with col2:
            period2_dates = st.date_input(
                "Period 2",
                value=(max_date - timedelta(days=365), max_date),
                key='period2'
            )
        
        if st.button("Compare Periods", type="primary"):
            with st.spinner("Comparing periods..."):
                if len(period1_dates) == 2 and len(period2_dates) == 2:
                    period1_data = df_lending[
                        (df_lending['survey_date'] >= pd.Timestamp(period1_dates[0])) &
                        (df_lending['survey_date'] <= pd.Timestamp(period1_dates[1]))
                    ]
                    
                    period2_data = df_lending[
                        (df_lending['survey_date'] >= pd.Timestamp(period2_dates[0])) &
                        (df_lending['survey_date'] <= pd.Timestamp(period2_dates[1]))
                    ]
                    
                    period1_summary = f"""
                    Date Range: {period1_dates[0]} to {period1_dates[1]}
                    Average Net Tightening by Category:
                    {period1_data.groupby('loan_category')['net_tightening'].mean().to_string()}
                    """
                    
                    period2_summary = f"""
                    Date Range: {period2_dates[0]} to {period2_dates[1]}
                    Average Net Tightening by Category:
                    {period2_data.groupby('loan_category')['net_tightening'].mean().to_string()}
                    """
                    
                    comparison = bedrock_analyzer.compare_periods(period1_summary, period2_summary)
                    st.markdown("### Comparison Results")
                    st.markdown(comparison)

def show_data_management():
    """Data management interface"""
    st.header("💾 Data Management")
    
    tab1, tab2 = st.tabs(["Load Data", "Database Status"])
    
    with tab1:
        st.subheader("Load SLOOS Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Real SLOOS Data from FRED")
            st.write("Download and load real SLOOS data from Federal Reserve Economic Data (FRED).")
            st.info("📊 This will download 9 FRED series with 35+ years of real data")
            
            if st.button("Update Real Data from FRED", type="primary"):
                with st.spinner("Downloading real SLOOS data from FRED..."):
                    import subprocess
                    result = subprocess.run(
                        ["uv", "run", "python", "download_real_sloos_data.py"],
                        capture_output=True,
                        text=True
                    )
                    
                    if result.returncode == 0:
                        st.success("✅ Successfully loaded real SLOOS data from FRED!")
                        st.cache_data.clear()
                        st.info("Database now contains real Federal Reserve data")
                    else:
                        st.error(f"❌ Error loading data: {result.stderr}")
            
            st.markdown("---")
            st.markdown("**Data Source:** Federal Reserve Economic Data (FRED)")
            st.markdown("**Series:** 9 FRED series (lending standards & loan demand)")
            st.markdown("**Coverage:** 1990-Q2 to present")
        
        with col2:
            st.markdown("### Data Information")
            st.write("Current data in the database is sourced from FRED.")
            
            st.markdown("#### FRED Series Used:")
            st.markdown("""
            **Lending Standards:**
            - DRTSCILM - C&I Loans (Large Firms)
            - DRTSCIS - C&I Loans (Small Firms)
            - DRTSSP - Prime Mortgages
            - DRTSCLCC - Credit Cards
            - STDSAUTO - Auto Loans
            
            **Loan Demand:**
            - DRSDCILM - C&I Loans (Large Firms)
            - DRSDCIS - C&I Loans (Small Firms)
            - DRSDSP - Prime Mortgages
            - DRSDCL - Consumer Loans
            """)
            
            st.markdown("---")
            st.markdown("🔗 [FRED SLOOS Data](https://fred.stlouisfed.org/searchresults?st=SLOOS)")
            st.markdown("🔗 [Fed SLOOS Page](https://www.federalreserve.gov/data/sloos.htm)")
    
    with tab2:
        st.subheader("Database Status")
        
        ingestion = SLOOSDataIngestion()
        summary = ingestion.get_data_summary()
        ingestion.close()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Lending Standards Records", summary.get('lending_standards_count', 0))
        
        with col2:
            st.metric("Loan Demand Records", summary.get('loan_demand_count', 0))
        
        with col3:
            if summary.get('date_range'):
                date_range = summary['date_range']
                st.metric("Date Range", f"{date_range[0]} to {date_range[1]}")
            else:
                st.metric("Date Range", "No data")
        
        st.divider()
        
        if st.button("Clear All Data", type="secondary"):
            if st.checkbox("I confirm I want to delete all data"):
                session = get_session()
                session.query(LendingStandard).delete()
                session.query(LoanDemand).delete()
                session.commit()
                session.close()
                st.success("All data cleared")
                st.cache_data.clear()

if __name__ == "__main__":
    main()
