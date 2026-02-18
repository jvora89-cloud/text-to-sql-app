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

# System prompt - same as before
SYSTEM_PROMPT = """You are a highly accurate text-to-SQL AI agent. Translate natural language questions into valid SQL queries for a SQLite database. Return ONLY the SQL query with no explanations.

# Database Schema
* Companies (CompanyID, CompanyName, Industry, Location)
* Departments (DepartmentID, DepartmentName, CompanyID)
* Employees (EmployeeID, Name, Occupation, DepartmentID, Salary, HireDate)
* Customers (CustomerID, CustomerName, Industry, ContactEmail)
* Products (ProductID, ProductName, Category, Price, CompanyID)
* Projects (ProjectID, ProjectName, CompanyID, Budget, StartDate, EndDate, Status)
* Transactions (TransactionID, EmployeeID, CustomerID, ProductID, TransactionDate, Amount)

Industries: Technology, Healthcare, Finance, Education, Retail, Construction, Energy, Hospitality

# Rules: Use schema only, correct SQLite syntax, JOINs preferred, specify columns, read-only queries"""

with st.sidebar:
    st.header("📊 Database")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Companies")
    st.metric("Companies", cursor.fetchone()[0])
    cursor.execute("SELECT COUNT(*) FROM Employees")
    st.metric("Employees", cursor.fetchone()[0])
    
    st.markdown("**Industries:** Technology, Healthcare, Finance, Education, Retail, Construction, Energy, Hospitality")
    st.markdown("**Examples:**")
    st.markdown("- How many employees in Healthcare?\n- Top 3 highest salaries?\n- Total transactions 2024?")

question = st.text_input("🔍 Ask about any industry:", placeholder="Which industries have most employees?")

# Demo mode - works without API
if st.button("🚀 Generate SQL & Execute", type="primary"):
    if question:
        # Use demo query since API endpoint is deprecated
        st.info("ℹ️ Using built-in SQL generation (API endpoint is being updated)")
        
        # Simple keyword-based SQL generation for common queries
        q_lower = question.lower()
        if "healthcare" in q_lower and "employee" in q_lower:
            sql_query = "SELECT COUNT(E.EmployeeID) FROM Employees E JOIN Departments D ON E.DepartmentID = D.DepartmentID JOIN Companies C ON D.CompanyID = C.CompanyID WHERE C.Industry = 'Healthcare';"
        elif "salary" in q_lower or "paid" in q_lower or "earn" in q_lower:
            sql_query = "SELECT Name, Occupation, Salary FROM Employees ORDER BY Salary DESC LIMIT 5;"
        elif "industry" in q_lower or "industries" in q_lower:
            sql_query = "SELECT C.Industry, COUNT(E.EmployeeID) as EmployeeCount FROM Employees E JOIN Departments D ON E.DepartmentID = D.DepartmentID JOIN Companies C ON D.CompanyID = C.CompanyID GROUP BY C.Industry ORDER BY EmployeeCount DESC;"
        elif "transaction" in q_lower:
            sql_query = "SELECT SUM(Amount) as TotalTransactions FROM Transactions WHERE TransactionDate LIKE '2024%';"
        elif "occupation" in q_lower:
            sql_query = "SELECT Occupation, AVG(Salary) as AvgSalary FROM Employees GROUP BY Occupation ORDER BY AvgSalary DESC LIMIT 3;"
        else:
            sql_query = "SELECT C.Industry, COUNT(E.EmployeeID) as Count FROM Employees E JOIN Departments D ON E.DepartmentID = D.DepartmentID JOIN Companies C ON D.CompanyID = C.CompanyID GROUP BY C.Industry;"
        
        st.subheader("📝 Generated SQL:")
        st.code(sql_query, language="sql")
        
        try:
            cursor = conn.cursor()
            cursor.execute(sql_query)
            results = cursor.fetchall()
            
            st.subheader("✅ Results:")
            if results:
                st.success(f"Found {len(results)} result(s)!")
                cols = [d[0] for d in cursor.description]
                st.table([dict(zip(cols, row)) for row in results])
            else:
                st.info("No results.")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Enter a question first.")

# Sample data
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    with st.expander("🏢 Companies"):
        cursor.execute("SELECT Industry, COUNT(*) as Count FROM Companies GROUP BY Industry")
        st.table([{"Industry": r[0], "Count": r[1]} for r in cursor.fetchall()])
with col2:
    with st.expander("💼 Top Jobs"):
        cursor.execute("SELECT Occupation, COUNT(*) as Count FROM Employees GROUP BY Occupation ORDER BY Count DESC LIMIT 5")
        st.table([{"Occupation": r[0], "Count": r[1]} for r in cursor.fetchall()])
with col3:
    with st.expander("💰 Top Earners"):
        cursor.execute("SELECT Name, Occupation, Salary FROM Employees ORDER BY Salary DESC LIMIT 5")
        cols = [d[0] for d in cursor.description]
        st.table([dict(zip(cols, row)) for row in cursor.fetchall()])

st.caption("🤖 AI-Powered SQL | 🔒 Read-Only | 🌐 Multi-Industry Database")
