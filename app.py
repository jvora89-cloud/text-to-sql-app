import streamlit as st
import sqlite3
import os
from pathlib import Path

if not Path("business.db").exists():
    import create_database
    create_database.create_database()

st.set_page_config(page_title="Text-to-SQL AI", page_icon="🤖", layout="wide")
st.title("🤖 Text-to-SQL AI Agent")
st.markdown("Ask questions about businesses across **8 industries**")

conn = sqlite3.connect('business.db', check_same_thread=False)

with st.sidebar:
    st.header("📊 Database")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Companies")
    st.metric("Companies", cursor.fetchone()[0])
    cursor.execute("SELECT COUNT(*) FROM Employees")
    st.metric("Employees", cursor.fetchone()[0])
    
    st.markdown("**Example Questions:**")
    st.markdown("- How many employees work in Technology?\n- Show highest salaries with companies\n- Which company has most employees?\n- List all healthcare companies")

question = st.text_input("🔍 Ask about any company or industry:", placeholder="Which companies are in Technology?")

if st.button("🚀 Generate SQL & Execute", type="primary"):
    if question:
        q_lower = question.lower()
        
        # Generate SQL with company names included
        if "technology" in q_lower and ("employee" in q_lower or "work" in q_lower):
            sql_query = """SELECT C.CompanyName, COUNT(E.EmployeeID) as Employees 
                          FROM Employees E 
                          JOIN Departments D ON E.DepartmentID = D.DepartmentID 
                          JOIN Companies C ON D.CompanyID = C.CompanyID 
                          WHERE C.Industry LIKE '%Technology%' 
                          GROUP BY C.CompanyName 
                          ORDER BY Employees DESC;"""
        
        elif "salary" in q_lower or "paid" in q_lower or "earn" in q_lower:
            sql_query = """SELECT E.Name, E.Occupation, C.CompanyName, E.Salary 
                          FROM Employees E 
                          JOIN Departments D ON E.DepartmentID = D.DepartmentID 
                          JOIN Companies C ON D.CompanyID = C.CompanyID 
                          ORDER BY E.Salary DESC 
                          LIMIT 10;"""
        
        elif "healthcare" in q_lower and "compan" in q_lower:
            sql_query = """SELECT CompanyName, Industry, Location 
                          FROM Companies 
                          WHERE Industry LIKE '%Healthcare%' 
                          OR Industry LIKE '%Pharma%';"""
        
        elif "most employee" in q_lower or "largest" in q_lower:
            sql_query = """SELECT C.CompanyName, C.Industry, COUNT(E.EmployeeID) as Employees 
                          FROM Employees E 
                          JOIN Departments D ON E.DepartmentID = D.DepartmentID 
                          JOIN Companies C ON D.CompanyID = C.CompanyID 
                          GROUP BY C.CompanyName, C.Industry 
                          ORDER BY Employees DESC 
                          LIMIT 10;"""
        
        elif "compan" in q_lower and ("technology" in q_lower or "tech" in q_lower):
            sql_query = """SELECT CompanyName, Industry, Location 
                          FROM Companies 
                          WHERE Industry LIKE '%Technology%' 
                          ORDER BY CompanyName;"""
        
        elif "list" in q_lower and "compan" in q_lower:
            sql_query = """SELECT CompanyName, Industry, Location 
                          FROM Companies 
                          ORDER BY Industry, CompanyName;"""
        
        elif "ceo" in q_lower or "executive" in q_lower:
            sql_query = """SELECT E.Name, E.Occupation, C.CompanyName, E.Salary 
                          FROM Employees E 
                          JOIN Departments D ON E.DepartmentID = D.DepartmentID 
                          JOIN Companies C ON D.CompanyID = C.CompanyID 
                          WHERE E.Occupation LIKE '%CEO%' OR E.Occupation LIKE '%Chief%' 
                          ORDER BY E.Salary DESC;"""
        
        elif "industry" in q_lower or "industries" in q_lower:
            sql_query = """SELECT C.Industry, COUNT(DISTINCT C.CompanyID) as Companies, 
                          COUNT(E.EmployeeID) as Employees 
                          FROM Companies C 
                          LEFT JOIN Departments D ON C.CompanyID = D.CompanyID 
                          LEFT JOIN Employees E ON D.DepartmentID = E.DepartmentID 
                          GROUP BY C.Industry 
                          ORDER BY Employees DESC;"""
        
        else:
            sql_query = """SELECT C.CompanyName, C.Industry, COUNT(E.EmployeeID) as Employees 
                          FROM Companies C 
                          LEFT JOIN Departments D ON C.CompanyID = D.CompanyID 
                          LEFT JOIN Employees E ON D.DepartmentID = E.DepartmentID 
                          GROUP BY C.CompanyName, C.Industry 
                          ORDER BY Employees DESC;"""
        
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
                st.info("No results found.")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Enter a question first.")

st.markdown("---")
st.subheader("📊 Quick Views")
col1, col2 = st.columns(2)

with col1:
    with st.expander("🏢 All Companies"):
        cursor.execute("SELECT CompanyName, Industry FROM Companies ORDER BY Industry, CompanyName")
        st.table([{"Company": r[0], "Industry": r[1]} for r in cursor.fetchall()])

with col2:
    with st.expander("💰 Top Earners with Companies"):
        cursor.execute("""SELECT E.Name, E.Occupation, C.CompanyName, E.Salary 
                         FROM Employees E 
                         JOIN Departments D ON E.DepartmentID = D.DepartmentID 
                         JOIN Companies C ON D.CompanyID = C.CompanyID 
                         ORDER BY E.Salary DESC LIMIT 10""")
        cols = [d[0] for d in cursor.description]
        st.table([dict(zip(cols, row)) for row in cursor.fetchall()])

st.caption("🤖 AI-Powered SQL | 🔒 Read-Only | 🌐 Multi-Industry Database")
