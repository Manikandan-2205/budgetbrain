import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import json

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

def analyze_spending_patterns(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyze spending patterns and generate insights"""
    insights = {
        "spending_trends": {},
        "budget_suggestions": [],
        "saving_opportunities": [],
        "investment_recommendations": [],
        "risk_assessment": {}
    }

    if df.empty:
        return insights

    # Basic financial metrics
    total_income = df[df['amount'] > 0]['amount'].sum()
    total_expenses = abs(df[df['amount'] < 0]['amount'].sum())
    savings_rate = (total_income - total_expenses) / total_income if total_income > 0 else 0

    # Spending trend analysis
    if len(df) > 7:
        recent_spending = df[df['amount'] < 0].tail(7)['amount'].abs().mean()
        overall_avg = df[df['amount'] < 0]['amount'].abs().mean()

        if recent_spending > overall_avg * 1.2:
            insights["spending_trends"]["warning"] = "Your recent spending is 20% higher than your average. Consider reviewing your expenses."
        elif recent_spending < overall_avg * 0.8:
            insights["spending_trends"]["positive"] = "Great job! Your recent spending is lower than average."

    # Budget suggestions
    if total_expenses > total_income * 0.9:
        insights["budget_suggestions"].append({
            "type": "critical",
            "title": "High Expense Ratio",
            "description": "Your expenses are over 90% of your income. Consider creating a strict budget.",
            "action": "Set spending limits for different categories"
        })

    if savings_rate < 0.1:
        insights["budget_suggestions"].append({
            "type": "warning",
            "title": "Low Savings Rate",
            "description": "You're saving less than 10% of your income. Aim for at least 20%.",
            "action": "Automate transfers to savings account"
        })

    # Saving opportunities
    if 'category_id' in df.columns:
        category_spending = df[df['amount'] < 0].groupby('category_id')['amount'].agg(['sum', 'count']).abs()
        top_categories = category_spending.nlargest(3, 'sum')

        for category, data in top_categories.iterrows():
            if data['sum'] > total_expenses * 0.3:  # If category > 30% of expenses
                insights["saving_opportunities"].append({
                    "category": category,
                    "amount": data['sum'],
                    "percentage": (data['sum'] / total_expenses) * 100,
                    "suggestion": f"Consider reducing spending in {category} by 10-15%"
                })

    # Investment recommendations
    if savings_rate > 0.2:
        insights["investment_recommendations"].append({
            "type": "conservative",
            "title": "High Savings Rate - Consider Investing",
            "description": "You're saving more than 20% of your income. Consider investing some savings.",
            "suggestions": ["Index funds", "Bonds", "High-yield savings"]
        })

    if total_income > 50000:  # Assuming annual income
        insights["investment_recommendations"].append({
            "type": "retirement",
            "title": "Retirement Planning",
            "description": "Consider maxing out retirement accounts like 401(k) or IRA.",
            "suggestions": ["Increase retirement contributions", "Diversify investments"]
        })

    # Risk assessment
    if len(df) > 30:
        monthly_volatility = df.groupby(pd.Grouper(key='created_at', freq='M'))['amount'].std()
        avg_volatility = monthly_volatility.mean()

        if avg_volatility > total_income * 0.1:
            insights["risk_assessment"]["income_volatility"] = "high"
            insights["budget_suggestions"].append({
                "type": "warning",
                "title": "Income Volatility",
                "description": "Your income shows high variability. Consider building an emergency fund.",
                "action": "Save 3-6 months of expenses as emergency fund"
            })
        else:
            insights["risk_assessment"]["income_volatility"] = "stable"

    return insights

def generate_financial_goals(total_income: float, total_expenses: float) -> List[Dict[str, Any]]:
    """Generate personalized financial goals"""
    goals = []

    savings_rate = (total_income - total_expenses) / total_income if total_income > 0 else 0

    # Emergency fund goal
    emergency_fund_months = 6
    monthly_expenses = total_expenses / 12 if total_expenses > 0 else 0
    emergency_fund_target = monthly_expenses * emergency_fund_months

    goals.append({
        "title": "Build Emergency Fund",
        "description": f"Save {emergency_fund_months} months of expenses (${emergency_fund_target:,.0f})",
        "progress": min(0.3, 0.1),  # Assuming some progress
        "timeframe": "6-12 months",
        "priority": "High"
    })

    # Debt reduction (if applicable)
    if total_expenses > total_income:
        goals.append({
            "title": "Reduce Debt",
            "description": "Focus on paying down high-interest debt",
            "progress": 0.0,
            "timeframe": "Ongoing",
            "priority": "High"
        })

    # Investment goal
    if savings_rate > 0.15:
        goals.append({
            "title": "Start Investing",
            "description": "Begin building wealth through investments",
            "progress": 0.0,
            "timeframe": "3-6 months",
            "priority": "Medium"
        })

    # Increase savings rate
    if savings_rate < 0.2:
        target_rate = 0.25
        goals.append({
            "title": "Increase Savings Rate",
            "description": f"Aim for {target_rate*100:.0f}% savings rate (currently {savings_rate*100:.1f}%)",
            "progress": savings_rate / target_rate,
            "timeframe": "6 months",
            "priority": "Medium"
        })

    return goals

def show_ai_suggestions():
    """Main AI suggestions dashboard"""
    st.title("🤖 AI-Powered Financial Assistant")

    # Fetch data
    transactions = get_transactions_data()

    if not transactions:
        st.warning("No transaction data available for AI analysis.")
        st.info("💡 **Tip:** Add some transactions to get personalized financial insights!")
        return

    # Convert to DataFrame
    df = pd.DataFrame(transactions)
    if 'created_at' in df.columns:
        df['created_at'] = pd.to_datetime(df['created_at'])

    # Calculate basic metrics
    total_income = df[df['amount'] > 0]['amount'].sum()
    total_expenses = abs(df[df['amount'] < 0]['amount'].sum())

    # Create tabs for different AI insights
    tab1, tab2, tab3, tab4 = st.tabs([
        "🧠 Smart Insights",
        "🎯 Financial Goals",
        "💡 Saving Tips",
        "📈 Investment Advice"
    ])

    with tab1:
        show_smart_insights(df, total_income, total_expenses)

    with tab2:
        show_financial_goals(total_income, total_expenses)

    with tab3:
        show_saving_tips(df, total_expenses)

    with tab4:
        show_investment_advice(total_income, total_expenses)

def show_smart_insights(df: pd.DataFrame, total_income: float, total_expenses: float):
    """Show AI-generated smart insights"""
    st.header("🧠 Smart Financial Insights")

    # Analyze spending patterns
    insights = analyze_spending_patterns(df)

    # Display insights
    if insights["spending_trends"]:
        st.subheader("📊 Spending Trends")
        for key, message in insights["spending_trends"].items():
            if key == "warning":
                st.warning(f"⚠️ {message}")
            elif key == "positive":
                st.success(f"✅ {message}")

    if insights["budget_suggestions"]:
        st.subheader("💰 Budget Recommendations")
        for suggestion in insights["budget_suggestions"]:
            if suggestion["type"] == "critical":
                st.error(f"🚨 **{suggestion['title']}**\n\n{suggestion['description']}\n\n💡 *{suggestion['action']}*")
            elif suggestion["type"] == "warning":
                st.warning(f"⚠️ **{suggestion['title']}**\n\n{suggestion['description']}\n\n💡 *{suggestion['action']}*")
            else:
                st.info(f"💡 **{suggestion['title']}**\n\n{suggestion['description']}\n\n💡 *{suggestion['action']}*")

    if insights["saving_opportunities"]:
        st.subheader("💸 Saving Opportunities")
        for opportunity in insights["saving_opportunities"]:
            st.info(f"**{opportunity['category']}**: ${opportunity['amount']:,.2f} "
                   f"({opportunity['percentage']:.1f}% of expenses)\n\n"
                   f"💡 {opportunity['suggestion']}")

    # Financial health score
    st.subheader("🏥 Financial Health Score")

    savings_rate = (total_income - total_expenses) / total_income if total_income > 0 else 0
    health_score = min(100, (savings_rate * 400))  # Scale savings rate to 0-100

    # Adjust score based on other factors
    if len(df) > 50:
        health_score += 10  # Good transaction history
    if total_income > total_expenses:
        health_score += 10  # Positive cash flow

    health_score = min(100, max(0, health_score))

    # Display score with color coding
    if health_score >= 80:
        st.success(f"🟢 Excellent Financial Health: {health_score:.1f}/100")
    elif health_score >= 60:
        st.warning(f"🟡 Good Financial Health: {health_score:.1f}/100")
    elif health_score >= 40:
        st.warning(f"🟠 Fair Financial Health: {health_score:.1f}/100")
    else:
        st.error(f"🔴 Needs Improvement: {health_score:.1f}/100")

    # Score breakdown
    st.write("**Score Factors:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Savings Rate", f"{savings_rate*100:.1f}%")
    with col2:
        st.metric("Transaction History", "Good" if len(df) > 50 else "Limited")
    with col3:
        cash_flow = "Positive" if total_income > total_expenses else "Negative"
        st.metric("Cash Flow", cash_flow)

def show_financial_goals(total_income: float, total_expenses: float):
    """Show personalized financial goals"""
    st.header("🎯 Your Financial Goals")

    goals = generate_financial_goals(total_income, total_expenses)

    if not goals:
        st.info("Add more financial data to generate personalized goals!")
        return

    for goal in goals:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                st.subheader(f"🎯 {goal['title']}")
                st.write(goal['description'])

            with col2:
                priority_color = {
                    "High": "🔴",
                    "Medium": "🟡",
                    "Low": "🟢"
                }
                st.metric("Priority", f"{priority_color[goal['priority']]} {goal['priority']}")

            with col3:
                st.metric("Timeframe", goal['timeframe'])

            # Progress bar
            progress = goal['progress']
            st.progress(progress)
            st.write(f"Progress: {progress*100:.1f}%")

            st.markdown("---")

def show_saving_tips(df: pd.DataFrame, total_expenses: float):
    """Show personalized saving tips"""
    st.header("💡 Smart Saving Tips")

    tips = []

    # Analyze spending patterns for tips
    if len(df) > 10:
        # Daily spending analysis
        daily_spending = df[df['amount'] < 0].groupby(df['created_at'].dt.date)['amount'].sum().abs()
        avg_daily = daily_spending.mean()

        if avg_daily > 50:
            tips.append({
                "title": "Reduce Daily Spending",
                "description": f"Your average daily spending is ${avg_daily:.2f}. Try reducing small purchases.",
                "potential_savings": avg_daily * 0.1 * 30,  # 10% reduction
                "difficulty": "Easy"
            })

        # Weekend vs weekday spending
        df['is_weekend'] = df['created_at'].dt.dayofweek >= 5
        weekend_spending = df[(df['amount'] < 0) & df['is_weekend']]['amount'].abs().mean()
        weekday_spending = df[(df['amount'] < 0) & ~df['is_weekend']]['amount'].abs().mean()

        if weekend_spending > weekday_spending * 1.5:
            tips.append({
                "title": "Control Weekend Spending",
                "description": f"Your weekend spending is 50% higher than weekdays. Plan weekend activities.",
                "potential_savings": (weekend_spending - weekday_spending) * 4,  # 4 weekend days
                "difficulty": "Medium"
            })

    # General saving tips
    tips.extend([
        {
            "title": "Automate Savings",
            "description": "Set up automatic transfers to savings account on payday.",
            "potential_savings": total_expenses * 0.05,  # 5% of expenses
            "difficulty": "Easy"
        },
        {
            "title": "Use Cash Instead of Cards",
            "description": "Pay with cash to become more aware of spending.",
            "potential_savings": total_expenses * 0.03,  # 3% reduction
            "difficulty": "Easy"
        },
        {
            "title": "Meal Planning",
            "description": "Plan meals for the week to reduce food waste and impulse buying.",
            "potential_savings": 150,  # Average weekly savings
            "difficulty": "Medium"
        }
    ])

    # Display tips
    for tip in tips:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                st.subheader(f"💡 {tip['title']}")
                st.write(tip['description'])

            with col2:
                difficulty_color = {
                    "Easy": "🟢",
                    "Medium": "🟡",
                    "Hard": "🔴"
                }
                st.metric("Difficulty", f"{difficulty_color[tip['difficulty']]} {tip['difficulty']}")

            with col3:
                st.metric("Potential Monthly Savings", f"${tip['potential_savings']:,.0f}")

            st.markdown("---")

def show_investment_advice(total_income: float, total_expenses: float):
    """Show investment recommendations"""
    st.header("📈 Investment Recommendations")

    savings_rate = (total_income - total_expenses) / total_income if total_income > 0 else 0
    monthly_savings = (total_income - total_expenses) / 12 if total_income > total_expenses else 0

    # Risk assessment
    st.subheader("🎲 Risk Profile Assessment")

    risk_questions = [
        "How comfortable are you with investment losses?",
        "What's your investment timeline?",
        "How much do you know about investing?"
    ]

    risk_score = 0
    for question in risk_questions:
        answer = st.selectbox(question,
                            ["Conservative", "Moderate", "Aggressive"],
                            key=f"risk_{question}")
        if answer == "Conservative":
            risk_score += 1
        elif answer == "Moderate":
            risk_score += 2
        else:
            risk_score += 3

    risk_profile = "Conservative" if risk_score <= 4 else "Moderate" if risk_score <= 7 else "Aggressive"

    if risk_profile == "Conservative":
        st.success("🟢 **Conservative Profile**: Focus on capital preservation")
    elif risk_profile == "Moderate":
        st.info("🟡 **Moderate Profile**: Balance growth and safety")
    else:
        st.warning("🔴 **Aggressive Profile**: Higher risk, higher potential returns")

    # Investment recommendations based on profile and financial situation
    st.subheader("💼 Recommended Investment Strategy")

    if monthly_savings < 100:
        st.warning("⚠️ **Build Savings First**: Focus on saving at least $100/month before investing heavily.")
    else:
        if risk_profile == "Conservative":
            st.write("**Recommended Allocation:**")
            st.write("- 60% High-Yield Savings/Bonds")
            st.write("- 30% Index Funds (e.g., S&P 500)")
            st.write("- 10% Individual Stocks (if interested)")

            st.write("**Why this works for you:** Low risk with steady growth")

        elif risk_profile == "Moderate":
            st.write("**Recommended Allocation:**")
            st.write("- 40% Index Funds/ETFs")
            st.write("- 30% Individual Stocks")
            st.write("- 20% Bonds")
            st.write("- 10% Alternative Investments")

            st.write("**Why this works for you:** Balanced approach with growth potential")

        else:  # Aggressive
            st.write("**Recommended Allocation:**")
            st.write("- 50% Growth Stocks/Tech")
            st.write("- 30% Emerging Markets")
            st.write("- 20% Cryptocurrency/Alternatives")

            st.write("**Why this works for you:** Maximum growth potential")

    # Monthly investment calculator
    st.subheader("🧮 Investment Calculator")

    col1, col2 = st.columns(2)

    with col1:
        monthly_investment = st.number_input(
            "Monthly Investment ($)",
            min_value=0,
            value=int(monthly_savings) if monthly_savings > 0 else 100,
            step=50
        )

    with col2:
        expected_return = st.slider(
            "Expected Annual Return (%)",
            min_value=3.0,
            max_value=12.0,
            value=7.0,
            step=0.5
        )

    if st.button("Calculate 10-Year Projection"):
        # Compound interest calculation
        monthly_rate = expected_return / 100 / 12
        months = 10 * 12

        future_value = 0
        for month in range(months):
            future_value = (future_value + monthly_investment) * (1 + monthly_rate)

        total_invested = monthly_investment * months
        total_growth = future_value - total_invested

        st.success(f"**Projected Value after 10 years:** ${future_value:,.2f}")
        st.info(f"**Total Invested:** ${total_invested:,.2f}")
        st.info(f"**Investment Growth:** ${total_growth:,.2f}")

# Main function to be called from the main app
def show_ai_suggestions_page():
    """Entry point for AI suggestions page"""
    show_ai_suggestions()

if __name__ == "__main__":
    show_ai_suggestions_page()
