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
st.markdown("Ask questions about businesses across **8 industries** with **20+ occupations**!")

HF_TOKEN = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_TOKEN")

@st.cache_resource
def get_db():
    conn = sqlite3.connect('business.db', check_same_thread=False)
    return conn

conn = get_db()

# System prompt for SQL generation
SYSTEM_PROMPT = """You are a highly accurate text-to-SQL AI agent. Translate natural language questions into valid SQL queries for a SQLite database. Return ONLY the SQL query with no explanations.

# Database Schema

* `Companies` (`CompanyID`: int, `CompanyName`: text, `Industry`: text, `Location`: text)
* `Departments` (`DepartmentID`: int, `DepartmentName`: text, `CompanyID`: int)
* `Employees` (`EmployeeID`: int, `Name`: text, `Occupation`: text, `DepartmentID`: int, `Salary`: real, `HireDate`: text)
* `Customers` (`CustomerID`: int, `CustomerName`: text, `Industry`: text, `ContactEmail`: text)
* `Products` (`ProductID`: int, `ProductName`: text, `Category`: text, `Price`: real, `CompanyID`: int)
* `Projects` (`ProjectID`: int, `ProjectName`: text, `CompanyID`: int, `Budget`: real, `StartDate`: text, `EndDate`: text, `Status`: text)
* `Transactions` (`TransactionID`: int, `EmployeeID`: int, `CustomerID`: int, `ProductID`: int, `TransactionDate`: text, `Amount`: real)

Industries: Technology, Healthcare, Finance, Education, Retail, Construction, Energy, Hospitality

# Rules
1. Use only the provided schema
2. Ensure syntactically correct SQLite queries
3. Use JOINs when needed
4. Specify columns (avoid SELECT *)
5. Read-only queries only
6. Return "Data not available" if schema doesn't support the question

# Examples

User: "How many employees work in Healthcare?"
SQL: SELECT COUNT(E.EmployeeID) FROM Employees E JOIN Departments D ON E.DepartmentID = D.DepartmentID JOIN Companies C ON D.CompanyID = C.CompanyID WHERE C.Industry = 'Healthcare';

User: "What are the top 3 highest-paid occupations?"
SQL: SELECT Occupation, AVG(Salary) as AvgSalary FROM Employees GROUP BY Occupation ORDER BY AvgSalary DESC LIMIT 3;"""

with st.sidebar:
    st.header("📊 Database Overview")

    # Show stats
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Companies")
    companies_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM Employees")
    employees_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(DISTINCT Industry) FROM Companies")
    industries_count = cursor.fetchone()[0]

    st.metric("Companies", companies_count)
    st.metric("Employees", employees_count)
    st.metric("Industries", industries_count)

    st.markdown("---")
    st.markdown("**Industries:**")
    st.markdown("""
    - 💻 Technology
    - 🏥 Healthcare
    - 💰 Finance
    - 📚 Education
    - 🛒 Retail
    - 🏗️ Construction
    - ⚡ Energy
    - 🍽️ Hospitality
    """)

    st.markdown("---")
    st.markdown("**Example Questions:**")
    st.markdown("""
    - How many employees in Healthcare?
    - Top 3 highest-paid occupations?
    - Which company has most projects?
    - Average salary by industry?
    - Total transactions in 2024?
    - List all Software Engineers
    """)

question = st.text_input(
    "🔍 Ask about any industry or occupation:",
    placeholder="e.g., Which industries have the most employees?"
)

def generate_sql(user_question, token):
    """Generate SQL using HuggingFace API"""
    url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    full_prompt = f"""{SYSTEM_PROMPT}

User: "{user_question}"
SQL:"""

    payload = {
        "inputs": full_prompt,
        "parameters": {
            "max_new_tokens": 200,
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
            sql = sql.strip()
            if '```' in sql:
                sql = sql.split('```')[1].replace('sql', '').strip()
            sql = sql.split(';')[0].strip() + ';'
            return sql
        return None
    except Exception as e:
        st.error(f"⚠️ API Error: {str(e)[:100]}")
        return None

if st.button("🚀 Generate SQL & Execute", type="primary"):
    if question:
        with st.spinner("🤖 Generating SQL..."):
            sql_query = generate_sql(question, HF_TOKEN)

            if not sql_query:
                st.warning("⚠️ No HF_TOKEN. Using demo query.")
                sql_query = "SELECT C.Industry, COUNT(E.EmployeeID) as EmployeeCount FROM Employees E JOIN Departments D ON E.DepartmentID = D.DepartmentID JOIN Companies C ON D.CompanyID = C.CompanyID GROUP BY C.Industry ORDER BY EmployeeCount DESC;"

            if sql_query and "Data not available" not in sql_query:
                st.subheader("📝 Generated SQL:")
                st.code(sql_query, language="sql")

                try:
                    with st.spinner("⚡ Executing..."):
                        cursor = conn.cursor()
                        cursor.execute(sql_query)
                        results = cursor.fetchall()

                        st.subheader("✅ Results:")
                        if results:
                            st.success(f"Found {len(results)} result(s)!")
                            cols = [d[0] for d in cursor.description]
                            data = [dict(zip(cols, row)) for row in results]
                            st.table(data)
                        else:
                            st.info("Query executed but no results found.")

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.info("Try rephrasing your question.")
            else:
                st.warning(sql_query if sql_query else "Could not generate SQL.")
    else:
        st.warning("⚠️ Please enter a question.")

# Sample data viewers
st.markdown("---")
st.subheader("📊 Quick Data Views")

col1, col2, col3 = st.columns(3)

with col1:
    with st.expander("🏢 Companies by Industry"):
        cursor = conn.cursor()
        cursor.execute("SELECT Industry, COUNT(*) as Count FROM Companies GROUP BY Industry")
        results = cursor.fetchall()
        st.table([{"Industry": r[0], "Count": r[1]} for r in results])

with col2:
    with st.expander("💼 Top Occupations"):
        cursor = conn.cursor()
        cursor.execute("SELECT Occupation, COUNT(*) as Count FROM Employees GROUP BY Occupation ORDER BY Count DESC LIMIT 5")
        results = cursor.fetchall()
        st.table([{"Occupation": r[0], "Count": r[1]} for r in results])

with col3:
    with st.expander("💰 Highest Salaries"):
        cursor = conn.cursor()
        cursor.execute("SELECT Name, Occupation, Salary FROM Employees ORDER BY Salary DESC LIMIT 5")
        results = cursor.fetchall()
        cols = [d[0] for d in cursor.description]
        st.table([dict(zip(cols, row)) for row in results])

st.markdown("---")
st.caption("🤖 AI-Powered SQL Generation | 🔒 Secure Read-Only Queries | 🌐 Multi-Industry Database")
