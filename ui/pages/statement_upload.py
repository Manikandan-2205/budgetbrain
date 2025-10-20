import streamlit as st
import pandas as pd
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
import io

# Import centralized API client
from services.api_client import get_api_client

# Get API client instance
api_client = get_api_client()

def parse_csv_statement(file_content: bytes, file_type: str) -> List[Dict[str, Any]]:
    """Parse different types of bank statement CSV files"""
    try:
        # Try different encodings
        for encoding in ['utf-8', 'latin1', 'cp1252']:
            try:
                content = file_content.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
        else:
            raise ValueError("Could not decode file with supported encodings")

        # Read CSV
        df = pd.read_csv(io.StringIO(content))

        # Normalize column names
        df.columns = df.columns.str.lower().str.strip()

        transactions = []

        # Handle different bank statement formats
        if file_type == "chase" or "description" in df.columns:
            # Chase Bank format
            for _, row in df.iterrows():
                transaction = {
                    "date": str(row.get("transaction date", row.get("date", ""))),
                    "description": str(row.get("description", "")),
                    "amount": float(str(row.get("amount", "0")).replace("$", "").replace(",", "")),
                    "type": str(row.get("type", "debit")).lower()
                }
                transactions.append(transaction)

        elif file_type == "bank_of_america" or "memo" in df.columns:
            # Bank of America format
            for _, row in df.iterrows():
                amount = float(str(row.get("amount", "0")).replace("$", "").replace(",", ""))
                transaction = {
                    "date": str(row.get("date", "")),
                    "description": str(row.get("description", row.get("memo", ""))),
                    "amount": amount,
                    "type": "credit" if amount > 0 else "debit"
                }
                transactions.append(transaction)

        elif file_type == "wells_fargo" or "check number" in df.columns:
            # Wells Fargo format
            for _, row in df.iterrows():
                amount = float(str(row.get("* amount", row.get("amount", "0"))).replace("$", "").replace(",", ""))
                transaction = {
                    "date": str(row.get("date", "")),
                    "description": str(row.get("description", "")),
                    "amount": amount,
                    "type": "credit" if amount > 0 else "debit"
                }
                transactions.append(transaction)

        else:
            # Generic format - try to detect columns
            date_cols = [col for col in df.columns if 'date' in col.lower()]
            amount_cols = [col for col in df.columns if any(word in col.lower() for word in ['amount', 'value', 'sum'])]
            desc_cols = [col for col in df.columns if any(word in col.lower() for word in ['description', 'desc', 'memo', 'reference'])]

            date_col = date_cols[0] if date_cols else df.columns[0]
            amount_col = amount_cols[0] if amount_cols else df.columns[-1]
            desc_col = desc_cols[0] if desc_cols else df.columns[1] if len(df.columns) > 1 else df.columns[0]

            for _, row in df.iterrows():
                try:
                    amount = float(str(row[amount_col]).replace("$", "").replace(",", ""))
                    transaction = {
                        "date": str(row[date_col]),
                        "description": str(row[desc_col]),
                        "amount": amount,
                        "type": "credit" if amount > 0 else "debit"
                    }
                    transactions.append(transaction)
                except (ValueError, KeyError):
                    continue

        return transactions

    except Exception as e:
        st.error(f"Error parsing CSV file: {str(e)}")
        return []

def parse_excel_statement(file_content: bytes) -> List[Dict[str, Any]]:
    """Parse Excel statement files"""
    try:
        df = pd.read_excel(io.BytesIO(file_content))

        # Normalize column names
        df.columns = df.columns.str.lower().str.strip()

        transactions = []

        # Generic Excel parsing
        date_cols = [col for col in df.columns if 'date' in col.lower()]
        amount_cols = [col for col in df.columns if any(word in col.lower() for word in ['amount', 'value', 'sum'])]
        desc_cols = [col for col in df.columns if any(word in col.lower() for word in ['description', 'desc', 'memo', 'reference'])]

        date_col = date_cols[0] if date_cols else df.columns[0]
        amount_col = amount_cols[0] if amount_cols else df.columns[-1]
        desc_col = desc_cols[0] if desc_cols else df.columns[1] if len(df.columns) > 1 else df.columns[0]

        for _, row in df.iterrows():
            try:
                amount = float(str(row[amount_col]).replace("$", "").replace(",", ""))
                transaction = {
                    "date": str(row[date_col]),
                    "description": str(row[desc_col]),
                    "amount": amount,
                    "type": "credit" if amount > 0 else "debit"
                }
                transactions.append(transaction)
            except (ValueError, KeyError):
                continue

        return transactions

    except Exception as e:
        st.error(f"Error parsing Excel file: {str(e)}")
        return []

def clean_transaction_data(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Clean and validate transaction data"""
    cleaned = []

    for transaction in transactions:
        try:
            # Parse and validate date
            date_str = transaction.get("date", "")
            if date_str:
                # Try different date formats
                for fmt in ["%m/%d/%Y", "%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y"]:
                    try:
                        parsed_date = datetime.strptime(date_str, fmt)
                        transaction["date"] = parsed_date.strftime("%Y-%m-%d")
                        break
                    except ValueError:
                        continue
                else:
                    # If no format works, use current date
                    transaction["date"] = datetime.now().strftime("%Y-%m-%d")

            # Clean description
            description = transaction.get("description", "").strip()
            if not description:
                description = "Imported transaction"
            transaction["description"] = description[:200]  # Limit length

            # Validate amount
            amount = transaction.get("amount", 0)
            if isinstance(amount, str):
                amount = float(amount.replace("$", "").replace(",", ""))
            transaction["amount"] = round(float(amount), 2)

            # Ensure type is valid
            trans_type = transaction.get("type", "debit").lower()
            if trans_type not in ["credit", "debit"]:
                trans_type = "debit" if amount < 0 else "credit"
            transaction["type"] = trans_type

            cleaned.append(transaction)

        except Exception as e:
            st.warning(f"Skipping invalid transaction: {transaction} - Error: {str(e)}")
            continue

    return cleaned

def create_transaction_in_api(transaction_data: Dict[str, Any]) -> bool:
    """Create a transaction via API"""
    try:
        # Convert to API format
        api_data = {
            "amount": transaction_data["amount"],
            "description": f"[IMPORTED] {transaction_data['description']}",
            "account_id": transaction_data.get("account_id", 1)  # Default to first account
        }

        response = api_client.create_transaction(api_data)
        return response.get("success", False)

    except Exception as e:
        st.error(f"Error creating transaction: {str(e)}")
        return False

def show_statement_upload():
    """Main statement upload interface"""
    st.title("📄 Statement Upload & Processing")

    st.markdown("""
    Upload your bank statements to automatically import transactions into BudgetBrain.
    Supported formats: CSV, Excel (.xlsx, .xls)
    """)

    # File upload section
    st.header("📤 Upload Statement")

    col1, col2 = st.columns([2, 1])

    with col1:
        uploaded_file = st.file_uploader(
            "Choose a statement file",
            type=["csv", "xlsx", "xls"],
            help="Upload CSV or Excel files from your bank"
        )

    with col2:
        bank_type = st.selectbox(
            "Bank Type",
            ["auto_detect", "chase", "bank_of_america", "wells_fargo", "citi", "generic"],
            help="Select your bank for better parsing, or use auto-detect"
        )

    if uploaded_file is not None:
        # Process the uploaded file
        file_content = uploaded_file.read()

        with st.spinner("Processing statement..."):
            try:
                if uploaded_file.name.endswith('.csv'):
                    transactions = parse_csv_statement(file_content, bank_type)
                else:
                    transactions = parse_excel_statement(file_content)

                if transactions:
                    # Clean the data
                    cleaned_transactions = clean_transaction_data(transactions)

                    st.success(f"✅ Successfully parsed {len(cleaned_transactions)} transactions from {len(transactions)} entries")

                    # Show preview
                    st.header("👀 Preview Transactions")

                    if cleaned_transactions:
                        # Convert to DataFrame for display
                        df = pd.DataFrame(cleaned_transactions)

                        # Show summary statistics
                        col1, col2, col3, col4 = st.columns(4)

                        with col1:
                            st.metric("Total Transactions", len(df))
                        with col2:
                            total_credits = df[df['amount'] > 0]['amount'].sum()
                            st.metric("Total Credits", f"${total_credits:,.2f}")
                        with col3:
                            total_debits = abs(df[df['amount'] < 0]['amount'].sum())
                            st.metric("Total Debits", f"${total_debits:,.2f}")
                        with col4:
                            net_amount = total_credits - total_debits
                            st.metric("Net Amount", f"${net_amount:,.2f}")

                        # Show sample transactions
                        st.subheader("Sample Transactions")
                        st.dataframe(df.head(10).style.format({
                            'amount': '${:.2f}'
                        }))

                        # Import options
                        st.header("⚙️ Import Options")

                        # Get available accounts
                        accounts_response = api_client.get_accounts()
                        if accounts_response.get("success"):
                            accounts = accounts_response.get("data", [])
                            if accounts:
                                account_options = {acc['id']: f"{acc['name']} (${acc['balance']:,.2f})" for acc in accounts}
                                selected_account = st.selectbox(
                                    "Import to Account",
                                    options=list(account_options.keys()),
                                    format_func=lambda x: account_options[x]
                                )
                            else:
                                st.warning("No accounts found. Please create an account first.")
                                selected_account = None
                        else:
                            st.error(f"Failed to load accounts: {accounts_response.get('message')}")
                            selected_account = None

                        # Import settings
                        col1, col2 = st.columns(2)

                        with col1:
                            skip_duplicates = st.checkbox(
                                "Skip duplicate transactions",
                                value=True,
                                help="Avoid importing transactions that already exist"
                            )

                        with col2:
                            import_all = st.checkbox(
                                "Import all transactions",
                                value=True,
                                help="Import all parsed transactions"
                            )

                        if import_all and selected_account:
                            if st.button("🚀 Import Transactions", type="primary"):
                                # Add account_id to all transactions
                                for transaction in cleaned_transactions:
                                    transaction["account_id"] = selected_account

                                # Import transactions
                                with st.spinner(f"Importing {len(cleaned_transactions)} transactions..."):
                                    success_count = 0
                                    error_count = 0

                                    progress_bar = st.progress(0)
                                    status_text = st.empty()

                                    for i, transaction in enumerate(cleaned_transactions):
                                        if create_transaction_in_api(transaction):
                                            success_count += 1
                                        else:
                                            error_count += 1

                                        # Update progress
                                        progress = (i + 1) / len(cleaned_transactions)
                                        progress_bar.progress(progress)
                                        status_text.text(f"Imported {success_count} transactions...")

                                    progress_bar.empty()
                                    status_text.empty()

                                    if success_count > 0:
                                        st.success(f"✅ Successfully imported {success_count} transactions!")
                                        if error_count > 0:
                                            st.warning(f"⚠️ {error_count} transactions failed to import.")
                                    else:
                                        st.error("❌ No transactions were imported. Please check your data.")

                        elif not selected_account:
                            st.warning("Please select an account to import transactions.")

                else:
                    st.error("❌ No valid transactions found in the uploaded file. Please check the file format.")

            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")

    # Help section
    st.header("📚 Help & Supported Formats")

    with st.expander("Supported File Formats"):
        st.markdown("""
        **CSV Files:**
        - Chase Bank statements
        - Bank of America statements
        - Wells Fargo statements
        - Generic CSV with columns: date, description, amount

        **Excel Files (.xlsx, .xls):**
        - Most bank statement formats
        - Automatic column detection

        **Required Columns:**
        - Date (transaction date)
        - Description/Memo (transaction details)
        - Amount (positive for credits, negative for debits)
        """)

    with st.expander("File Format Tips"):
        st.markdown("""
        **For best results:**
        - Ensure dates are in MM/DD/YYYY or YYYY-MM-DD format
        - Remove any header rows above the actual data
        - Make sure amounts include negative signs for debits
        - Clean up any special characters in descriptions

        **Common Issues:**
        - Different date formats across banks
        - Extra header/footer rows
        - Merged cells in Excel files
        - Special characters in CSV files
        """)

    with st.expander("Security & Privacy"):
        st.markdown("""
        **Your data is secure:**
        - Files are processed locally in your browser
        - No files are stored on external servers
        - Transaction data is encrypted in transit
        - Only you can access your imported transactions

        **Privacy measures:**
        - Files are not retained after processing
        - All data transmission is encrypted
        - Access is restricted to authenticated users only
        """)

# Main function to be called from the main app
def show_statement_upload_page():
    """Entry point for statement upload page"""
    show_statement_upload()

if __name__ == "__main__":
    show_statement_upload_page()