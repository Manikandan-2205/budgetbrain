import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, Any, List

# Import centralized API client
from services.api_client import get_api_client

# Get API client instance
api_client = get_api_client()

def get_transactions_data() -> List[Dict[str, Any]]:
    """Fetch transactions data from API"""
    response = api_client.get_transactions(limit=10000)
    if response.get("success"):
        return response.get("data", [])
    else:
        st.error(f"Error fetching transactions: {response.get('message')}")
        return []

def get_accounts_data() -> List[Dict[str, Any]]:
    """Fetch accounts data from API"""
    response = api_client.get_accounts()
    if response.get("success"):
        return response.get("data", [])
    else:
        st.error(f"Error fetching accounts: {response.get('message')}")
        return []

def show_analytics_dashboard():
    """Main analytics dashboard"""
    st.title("📊 Advanced Analytics & Predictions")

    # Fetch data
    transactions = get_transactions_data()
    accounts = get_accounts_data()

    if not transactions:
        st.warning("No transaction data available for analysis.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(transactions)

    # Data preprocessing
    if 'created_at' in df.columns:
        df['created_at'] = pd.to_datetime(df['created_at'])
        df['date'] = df['created_at'].dt.date
        df['month'] = df['created_at'].dt.to_period('M')
        df['year'] = df['created_at'].dt.year
        df['weekday'] = df['created_at'].dt.day_name()

    # Create tabs for different analytics views
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Trends & Patterns",
        "💰 Cash Flow Analysis",
        "🎯 Predictive Analytics",
        "📊 Comparative Analysis",
        "🔮 Future Projections"
    ])

    with tab1:
        show_trends_patterns(df)

    with tab2:
        show_cash_flow_analysis(df)

    with tab3:
        show_predictive_analytics(df)

    with tab4:
        show_comparative_analysis(df)

    with tab5:
        show_future_projections(df)

def show_trends_patterns(df: pd.DataFrame):
    """Show trends and patterns analysis"""
    st.header("📈 Trends & Patterns")

    col1, col2 = st.columns(2)

    with col1:
        # Monthly trends
        monthly_data = df.groupby('month').agg({
            'amount': ['sum', 'count', 'mean']
        }).reset_index()
        monthly_data.columns = ['month', 'total_amount', 'transaction_count', 'avg_amount']

        fig = px.line(monthly_data, x='month', y='total_amount',
                     title='Monthly Transaction Trends',
                     labels={'total_amount': 'Amount ($)', 'month': 'Month'})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Daily patterns
        daily_patterns = df.groupby('weekday')['amount'].agg(['sum', 'count']).reset_index()

        fig = px.bar(daily_patterns, x='weekday', y='sum',
                    title='Spending by Day of Week',
                    labels={'sum': 'Total Amount ($)', 'weekday': 'Day'})
        st.plotly_chart(fig, use_container_width=True)

    # Seasonal analysis
    st.subheader("🌊 Seasonal Analysis")
    if len(df) > 30:  # Need enough data for seasonal analysis
        # Rolling averages
        df_sorted = df.sort_values('created_at')
        df_sorted['rolling_avg_7'] = df_sorted['amount'].rolling(window=7).mean()
        df_sorted['rolling_avg_30'] = df_sorted['amount'].rolling(window=30).mean()

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_sorted['date'], y=df_sorted['rolling_avg_7'],
                                mode='lines', name='7-day average'))
        fig.add_trace(go.Scatter(x=df_sorted['date'], y=df_sorted['rolling_avg_30'],
                                mode='lines', name='30-day average'))
        fig.update_layout(title='Rolling Averages - Trend Analysis',
                         xaxis_title='Date', yaxis_title='Amount ($)')
        st.plotly_chart(fig, use_container_width=True)

def show_cash_flow_analysis(df: pd.DataFrame):
    """Show cash flow analysis"""
    st.header("💰 Cash Flow Analysis")

    # Separate income and expenses
    income_df = df[df['amount'] > 0]
    expense_df = df[df['amount'] < 0].copy()
    expense_df['amount'] = expense_df['amount'].abs()

    col1, col2 = st.columns(2)

    with col1:
        # Income vs Expenses over time
        monthly_flow = df.groupby('month').agg({
            'amount': lambda x: x[x > 0].sum() - abs(x[x < 0].sum())
        }).reset_index()
        monthly_flow.columns = ['month', 'net_flow']

        fig = px.bar(monthly_flow, x='month', y='net_flow',
                    title='Monthly Net Cash Flow',
                    labels={'net_flow': 'Net Flow ($)', 'month': 'Month'},
                    color=monthly_flow['net_flow'].apply(lambda x: 'positive' if x >= 0 else 'negative'),
                    color_discrete_map={'positive': 'green', 'negative': 'red'})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Cash flow distribution
        fig = go.Figure()
        fig.add_trace(go.Box(y=income_df['amount'], name='Income', marker_color='green'))
        fig.add_trace(go.Box(y=expense_df['amount'], name='Expenses', marker_color='red'))
        fig.update_layout(title='Income vs Expense Distribution',
                         yaxis_title='Amount ($)')
        st.plotly_chart(fig, use_container_width=True)

    # Cash flow summary
    st.subheader("💡 Cash Flow Insights")

    total_income = income_df['amount'].sum()
    total_expenses = expense_df['amount'].sum()
    savings_rate = ((total_income - total_expenses) / total_income * 100) if total_income > 0 else 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Income", f"${total_income:,.2f}")
    with col2:
        st.metric("Total Expenses", f"${total_expenses:,.2f}")
    with col3:
        st.metric("Net Savings", f"${total_income - total_expenses:,.2f}")
    with col4:
        st.metric("Savings Rate", f"{savings_rate:.1f}%")

def show_predictive_analytics(df: pd.DataFrame):
    """Show predictive analytics"""
    st.header("🎯 Predictive Analytics")

    if len(df) < 30:
        st.warning("Need at least 30 transactions for meaningful predictions.")
        return

    # Simple linear regression for next month prediction
    df_sorted = df.sort_values('created_at')
    df_sorted['days_since_start'] = (df_sorted['created_at'] - df_sorted['created_at'].min()).dt.days

    # Monthly aggregation for prediction
    monthly_agg = df_sorted.groupby('month').agg({
        'amount': 'sum',
        'days_since_start': 'mean'
    }).reset_index()

    if len(monthly_agg) >= 3:  # Need at least 3 months for trend
        from sklearn.linear_model import LinearRegression

        X = monthly_agg[['days_since_start']]
        y = monthly_agg['amount']

        model = LinearRegression()
        model.fit(X, y)

        # Predict next 3 months
        last_date = df_sorted['created_at'].max()
        future_dates = []
        future_predictions = []

        for i in range(1, 4):
            next_month = last_date + pd.DateOffset(months=i)
            days_since = (next_month - df_sorted['created_at'].min()).days
            prediction = model.predict([[days_since]])[0]
            future_dates.append(next_month.strftime('%Y-%m'))
            future_predictions.append(prediction)

        # Plot predictions
        fig = go.Figure()

        # Historical data
        fig.add_trace(go.Scatter(
            x=monthly_agg['month'].astype(str),
            y=monthly_agg['amount'],
            mode='lines+markers',
            name='Historical Data',
            line=dict(color='blue')
        ))

        # Predictions
        fig.add_trace(go.Scatter(
            x=future_dates,
            y=future_predictions,
            mode='lines+markers',
            name='Predictions',
            line=dict(color='red', dash='dash')
        ))

        fig.update_layout(
            title='Transaction Amount Prediction (Next 3 Months)',
            xaxis_title='Month',
            yaxis_title='Amount ($)',
            showlegend=True
        )

        st.plotly_chart(fig, use_container_width=True)

        # Prediction insights
        st.subheader("🔮 Prediction Insights")

        avg_prediction = np.mean(future_predictions)
        trend = "increasing" if future_predictions[-1] > future_predictions[0] else "decreasing"

        st.write(f"**Average predicted amount for next 3 months:** ${avg_prediction:,.2f}")
        st.write(f"**Trend:** {trend.capitalize()}")
        st.write("**Note:** This is a simple linear regression model. Actual results may vary.")

def show_comparative_analysis(df: pd.DataFrame):
    """Show comparative analysis"""
    st.header("📊 Comparative Analysis")

    if len(df) < 10:
        st.warning("Need more transaction data for comparative analysis.")
        return

    col1, col2 = st.columns(2)

    with col1:
        # Year-over-year comparison (if available)
        if len(df['year'].unique()) > 1:
            yearly_comparison = df.groupby('year')['amount'].agg(['sum', 'count', 'mean']).reset_index()

            fig = px.bar(yearly_comparison, x='year', y='sum',
                        title='Year-over-Year Comparison',
                        labels={'sum': 'Total Amount ($)', 'year': 'Year'})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Need data from multiple years for year-over-year comparison.")

    with col2:
        # Category analysis (if category data available)
        if 'category_id' in df.columns and df['category_id'].notna().any():
            category_analysis = df.groupby('category_id')['amount'].agg(['sum', 'count']).reset_index()
            category_analysis = category_analysis.sort_values('sum', ascending=False).head(10)

            fig = px.pie(category_analysis, values='sum', names='category_id',
                        title='Top Spending Categories')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Category data not available for analysis.")

    # Performance metrics
    st.subheader("📈 Performance Metrics")

    # Calculate some key metrics
    total_transactions = len(df)
    avg_transaction = df['amount'].mean()
    largest_transaction = df['amount'].max()
    smallest_transaction = df['amount'].min()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Transactions", total_transactions)
    with col2:
        st.metric("Average Transaction", f"${avg_transaction:.2f}")
    with col3:
        st.metric("Largest Transaction", f"${largest_transaction:.2f}")
    with col4:
        st.metric("Smallest Transaction", f"${smallest_transaction:.2f}")

def show_future_projections(df: pd.DataFrame):
    """Show future projections and scenarios"""
    st.header("🔮 Future Projections")

    if len(df) < 50:
        st.warning("Need more transaction data for accurate projections.")
        return

    # Investment projection calculator
    st.subheader("💰 Investment Projection Calculator")

    col1, col2 = st.columns(2)

    with col1:
        initial_investment = st.number_input(
            "Initial Investment Amount ($)",
            min_value=0.0,
            value=1000.0,
            step=100.0
        )

        monthly_contribution = st.number_input(
            "Monthly Contribution ($)",
            min_value=0.0,
            value=100.0,
            step=10.0
        )

    with col2:
        expected_return = st.slider(
            "Expected Annual Return (%)",
            min_value=1.0,
            max_value=15.0,
            value=7.0,
            step=0.5
        ) / 100

        years = st.slider(
            "Investment Period (Years)",
            min_value=1,
            max_value=30,
            value=10
        )

    if st.button("Calculate Projection"):
        # Compound interest calculation
        monthly_rate = expected_return / 12
        months = years * 12

        future_value = initial_investment
        monthly_data = []

        for month in range(months + 1):
            monthly_data.append({
                'month': month,
                'balance': future_value
            })
            future_value = (future_value + monthly_contribution) * (1 + monthly_rate)

        # Create projection chart
        projection_df = pd.DataFrame(monthly_data)

        fig = px.line(projection_df, x='month', y='balance',
                     title=f'Investment Growth Projection ({years} years)',
                     labels={'balance': 'Portfolio Value ($)', 'month': 'Month'})

        # Add markers for yearly points
        yearly_points = projection_df[projection_df['month'] % 12 == 0]
        fig.add_trace(go.Scatter(
            x=yearly_points['month'],
            y=yearly_points['balance'],
            mode='markers+text',
            text=[f"Year {int(m/12)}" for m in yearly_points['month']],
            textposition="top center",
            showlegend=False
        ))

        st.plotly_chart(fig, use_container_width=True)

        # Summary statistics
        final_value = future_value
        total_contributed = initial_investment + (monthly_contribution * months)
        total_growth = final_value - total_contributed

        st.subheader("📊 Projection Summary")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Final Portfolio Value", f"${final_value:,.2f}")
        with col2:
            st.metric("Total Contributed", f"${total_contributed:,.2f}")
        with col3:
            st.metric("Investment Growth", f"${total_growth:,.2f}")
        with col4:
            growth_percentage = (total_growth / total_contributed) * 100
            st.metric("Growth Percentage", f"{growth_percentage:.1f}%")

    # Risk assessment
    st.subheader("⚠️ Risk Assessment")

    risk_level = "Low" if expected_return < 0.05 else "Medium" if expected_return < 0.10 else "High"

    if risk_level == "Low":
        st.success("🟢 Low Risk: Conservative investment approach")
    elif risk_level == "Medium":
        st.warning("🟡 Medium Risk: Balanced investment approach")
    else:
        st.error("🔴 High Risk: Aggressive investment approach")

    st.info("**Disclaimer:** This is a simplified projection. Actual investment returns may vary significantly due to market conditions, fees, taxes, and other factors. Consider consulting with a financial advisor.")

# Main function to be called from the main app
def show_analytics_page():
    """Entry point for analytics page"""
    show_analytics_dashboard()

if __name__ == "__main__":
    show_analytics_page()
