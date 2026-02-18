import streamlit as st
import sqlite3
import os
import requests
from pathlib import Path

# Create database if it doesn't exist
if not Path("business.db").exists():
    import create_database
    create_database.create_database()

st.set_page_config(page_title="Text-to-SQL AI", page_icon="🤖", layout="wide")
st.title("🤖 Text-to-SQL AI Agent")
st.markdown("Ask business questions in natural language and get instant SQL results!")

HF_TOKEN = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_TOKEN")

@st.cache_resource
def get_db():
    conn = sqlite3.connect('business.db', check_same_thread=False)
    return conn

conn = get_db()

# System prompt for SQL generation
SYSTEM_PROMPT = """You are a highly accurate and secure text-to-SQL AI agent. Your task is to translate natural language questions into valid, executable SQL queries for a SQLite database. Do not return any natural language explanations or extra text unless a query cannot be generated. Return only the SQL query itself.

# Database Schema
The database has the following tables and columns:

* `Employees` (`EmployeeID`: int, `Name`: text, `DepartmentID`: int, `Salary`: real)
* `Departments` (`DepartmentID`: int, `DepartmentName`: text)
* `Sales` (`SaleID`: int, `EmployeeID`: int, `ProductID`: int, `SaleDate`: text, `Amount`: real)
* `Products` (`ProductID`: int, `ProductName`: text, `Category`: text)

# Rules
1. Use only the provided schema. Do not guess table or column names.
2. Ensure all generated SQL is syntactically correct for SQLite.
3. Prioritize joins over subqueries when possible.
4. Do not use 'SELECT *'. Specify all necessary columns.
5. If the user asks for data that is not available in the provided schema, respond with "Data not available in the current schema."
6. Ensure queries are read-only and do not attempt to modify the database.

# Examples

User Input: "How many employees are in the Sales department?"
SQL Output: SELECT COUNT(E.EmployeeID) FROM Employees E JOIN Departments D ON E.DepartmentID = D.DepartmentID WHERE D.DepartmentName = 'Sales';

User Input: "What was the total sales amount in Q4 2024?"
SQL Output: SELECT SUM(Amount) FROM Sales WHERE SaleDate >= '2024-10-01' AND SaleDate <= '2024-12-31';"""

with st.sidebar:
    st.header("📊 Database Schema")
    st.markdown("""
**Tables:**
- **Employees**: EmployeeID, Name, DepartmentID, Salary
- **Departments**: DepartmentID, DepartmentName
- **Sales**: SaleID, EmployeeID, ProductID, SaleDate, Amount
- **Products**: ProductID, ProductName, Category
    """)

    st.markdown("---")
    st.markdown("**Example Questions:**")
    st.markdown("""
- How many employees are in Sales?
- What was total sales in Q4 2024?
- Who are the top 3 earners?
- Show all Electronics sales
- Average salary by department
    """)

question = st.text_input(
    "Ask a business question:",
    placeholder="e.g., What was the total sales amount in 2024?"
)

def generate_sql(user_question, token):
    """Generate SQL using HuggingFace API"""
    url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    full_prompt = f"""{SYSTEM_PROMPT}

User Input: "{user_question}"
SQL Output:"""

    payload = {
        "inputs": full_prompt,
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.1,
            "return_full_text": False
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()

        if isinstance(result, list) and len(result) > 0:
            sql = result[0].get('generated_text', '')
            # Clean up SQL
            sql = sql.strip()
            if '```' in sql:
                sql = sql.split('```')[1].replace('sql', '').strip()
            # Take only the first complete SQL statement
            sql = sql.split(';')[0].strip() + ';'
            return sql
        return None
    except Exception as e:
        st.error(f"⚠️ API Error: {str(e)[:100]}")
        return None

if st.button("🔍 Generate SQL & Execute", type="primary"):
    if question:
        with st.spinner("🤖 Generating SQL query..."):
            sql_query = generate_sql(question, HF_TOKEN)

            if not sql_query:
                st.warning("⚠️ No HF_TOKEN found. Using demo mode.")
                sql_query = "SELECT D.DepartmentName, COUNT(E.EmployeeID) as EmployeeCount FROM Employees E JOIN Departments D ON E.DepartmentID = D.DepartmentID GROUP BY D.DepartmentName;"

            if sql_query and "Data not available" not in sql_query:
                st.subheader("📝 Generated SQL Query:")
                st.code(sql_query, language="sql")

                try:
                    with st.spinner("⚡ Executing query..."):
                        cursor = conn.cursor()
                        cursor.execute(sql_query)
                        results = cursor.fetchall()

                        st.subheader("✅ Query Results:")
                        if results:
                            st.success(f"Found {len(results)} result(s)!")

                            # Display as table
                            cols = [d[0] for d in cursor.description]
                            data = [dict(zip(cols, row)) for row in results]
                            st.table(data)
                        else:
                            st.info("Query executed successfully but returned no results.")

                except Exception as e:
                    st.error(f"❌ Query Error: {str(e)}")
                    st.info("The generated SQL may have syntax errors. Try rephrasing your question.")
            else:
                st.warning(sql_query if sql_query else "Could not generate SQL.")
    else:
        st.warning("⚠️ Please enter a question first.")

# Sample data viewers
col1, col2 = st.columns(2)

with col1:
    with st.expander("👥 View Employees"):
        cursor = conn.cursor()
        cursor.execute("SELECT E.EmployeeID, E.Name, D.DepartmentName, E.Salary FROM Employees E JOIN Departments D ON E.DepartmentID = D.DepartmentID LIMIT 5")
        results = cursor.fetchall()
        cols = [d[0] for d in cursor.description]
        st.table([dict(zip(cols, row)) for row in results])

with col2:
    with st.expander("💰 View Recent Sales"):
        cursor = conn.cursor()
        cursor.execute("SELECT S.SaleID, E.Name as Employee, P.ProductName, S.Amount, S.SaleDate FROM Sales S JOIN Employees E ON S.EmployeeID = E.EmployeeID JOIN Products P ON S.ProductID = P.ProductID ORDER BY S.SaleDate DESC LIMIT 5")
        results = cursor.fetchall()
        cols = [d[0] for d in cursor.description]
        st.table([dict(zip(cols, row)) for row in results])

st.markdown("---")
st.caption("🤖 Powered by AI | 🔒 Read-only queries for security")
