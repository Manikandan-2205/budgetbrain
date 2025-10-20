import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, List, Any


def create_expense_chart(expenses: List[Dict[str, Any]]) -> go.Figure:
    """Create an interactive expense breakdown chart"""
    df = pd.DataFrame(expenses)

    fig = px.pie(
        df,
        values='amount',
        names='category',
        title='Expense Breakdown',
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(showlegend=False)

    return fig


def create_income_chart(income_data: List[Dict[str, Any]]) -> go.Figure:
    """Create an income trend chart"""
    df = pd.DataFrame(income_data)

    fig = px.line(
        df,
        x='date',
        y='amount',
        title='Income Trend',
        markers=True,
        color_discrete_sequence=['#51cf66']
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Amount ($)",
        showlegend=False
    )

    return fig


def create_budget_progress_chart(budget_data: List[Dict[str, Any]]) -> go.Figure:
    """Create a budget progress chart"""
    df = pd.DataFrame(budget_data)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df['category'],
        y=df['spent'],
        name='Spent',
        marker_color='#ff6b6b'
    ))

    fig.add_trace(go.Bar(
        x=df['category'],
        y=df['budget'],
        name='Budget',
        marker_color='#74c0fc'
    ))

    fig.update_layout(
        title='Budget vs Actual Spending',
        xaxis_title="Category",
        yaxis_title="Amount ($)",
        barmode='group'
    )

    return fig


def create_net_worth_chart(net_worth_data: List[Dict[str, Any]]) -> go.Figure:
    """Create a net worth over time chart"""
    df = pd.DataFrame(net_worth_data)

    fig = px.area(
        df,
        x='date',
        y='net_worth',
        title='Net Worth Over Time',
        color_discrete_sequence=['#9775fa']
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Net Worth ($)"
    )

    return fig


def create_transaction_timeline(transactions: List[Dict[str, Any]]) -> go.Figure:
    """Create a transaction timeline chart"""
    df = pd.DataFrame(transactions)
    df['date'] = pd.to_datetime(df['date'])

    # Separate income and expenses
    income_df = df[df['type'] == 'income']
    expense_df = df[df['type'] == 'expense']

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=income_df['date'],
        y=income_df['amount'],
        mode='markers',
        name='Income',
        marker=dict(color='#51cf66', size=8),
        hovertemplate='%{y:.2f}<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=expense_df['date'],
        y=expense_df['amount'],
        mode='markers',
        name='Expenses',
        marker=dict(color='#ff6b6b', size=8),
        hovertemplate='%{y:.2f}<extra></extra>'
    ))

    fig.update_layout(
        title='Transaction Timeline',
        xaxis_title="Date",
        yaxis_title="Amount ($)",
        hovermode='x unified'
    )

    return fig


def create_category_trend_chart(category_trends: List[Dict[str, Any]]) -> go.Figure:
    """Create a category spending trend chart"""
    df = pd.DataFrame(category_trends)

    fig = px.line(
        df,
        x='month',
        y='amount',
        color='category',
        title='Spending Trends by Category',
        markers=True
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Amount ($)"
    )

    return fig
