import streamlit as st
import sqlite3
import os
import uuid
from pathlib import Path
from datetime import datetime

# Create business database if it doesn't exist
if not Path("business.db").exists():
    import create_database
    create_database.create_database()

# Initialize session ID for training tracking
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Training data collection functions
def log_query(user_query, generated_sql, execution_success, execution_result, error_message, model_used="keyword-based"):
    """Log query to training database"""
    try:
        conn_train = sqlite3.connect('training_data.db')
        cursor = conn_train.cursor()
        cursor.execute('''
            INSERT INTO query_logs
            (user_query, generated_sql, execution_success, execution_result, error_message, session_id, model_used)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_query, generated_sql, execution_success, str(execution_result)[:500] if execution_result else None,
              error_message, st.session_state.session_id, model_used))
        query_log_id = cursor.lastrowid
        conn_train.commit()
        conn_train.close()
        return query_log_id
    except Exception as e:
        st.warning(f"Training logging unavailable: {str(e)[:50]}")
        return None

def save_feedback(query_log_id, feedback_type, corrected_sql=None, comment=None):
    """Save user feedback to training database"""
    try:
        conn_train = sqlite3.connect('training_data.db')
        cursor = conn_train.cursor()
        cursor.execute('''
            INSERT INTO user_feedback
            (query_log_id, feedback_type, corrected_sql, feedback_comment)
            VALUES (?, ?, ?, ?)
        ''', (query_log_id, feedback_type, corrected_sql, comment))
        conn_train.commit()
        conn_train.close()
        return True
    except Exception as e:
        st.error(f"Could not save feedback: {str(e)[:50]}")
        return False

def get_training_stats():
    """Get training data statistics"""
    try:
        conn_train = sqlite3.connect('training_data.db')
        cursor = conn_train.cursor()
        cursor.execute('SELECT COUNT(*) FROM query_logs')
        total_queries = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM user_feedback WHERE feedback_type = "positive"')
        positive = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM user_feedback WHERE feedback_type = "negative"')
        negative = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM verified_examples')
        verified = cursor.fetchone()[0]
        conn_train.close()
        return {
            'total_queries': total_queries,
            'positive_feedback': positive,
            'negative_feedback': negative,
            'verified_examples': verified
        }
    except:
        return None

st.set_page_config(page_title="Text-to-SQL AI", page_icon="🤖", layout="wide")
st.title("🤖 Text-to-SQL AI Agent")
st.markdown("Ask questions about businesses across **8 industries** | **AI Training Enabled**")

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

    # Training Statistics
    st.markdown("---")
    st.header("🤖 AI Training Stats")
    training_stats = get_training_stats()
    if training_stats:
        st.metric("Total Queries", training_stats['total_queries'])
        col1, col2 = st.columns(2)
        with col1:
            st.metric("👍", training_stats['positive_feedback'])
        with col2:
            st.metric("👎", training_stats['negative_feedback'])

        total_feedback = training_stats['positive_feedback'] + training_stats['negative_feedback']
        if total_feedback > 0:
            satisfaction = (training_stats['positive_feedback'] / total_feedback * 100)
            st.progress(satisfaction / 100)
            st.caption(f"Satisfaction: {satisfaction:.1f}%")

        st.metric("✅ Verified", training_stats['verified_examples'])
        st.caption(f"Session: {st.session_state.session_id[:8]}...")
    else:
        st.info("Training system initializing...")

question = st.text_input("🔍 Ask about any company or industry:", placeholder="Which companies are in Technology?")

if st.button("🚀 Generate SQL & Execute", type="primary"):
    if question:
        q_lower = question.lower()
        execution_success = False
        error_message = None
        results = None
        query_log_id = None

        # Generate SQL with company names included (keyword-based)
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

        # Execute query and collect results
        try:
            cursor = conn.cursor()
            cursor.execute(sql_query)
            results = cursor.fetchall()
            execution_success = True

            st.subheader("✅ Results:")
            if results:
                st.success(f"Found {len(results)} result(s)!")
                cols = [d[0] for d in cursor.description]
                st.table([dict(zip(cols, row)) for row in results])
            else:
                st.info("No results found.")
        except Exception as e:
            execution_success = False
            error_message = str(e)
            st.error(f"Error: {error_message}")

        # Log query for training
        result_str = f"{len(results)} rows" if execution_success and results else None
        query_log_id = log_query(
            user_query=question,
            generated_sql=sql_query,
            execution_success=1 if execution_success else 0,
            execution_result=result_str,
            error_message=error_message,
            model_used="keyword-based-v1"
        )

        # Feedback UI (only if query was logged)
        if query_log_id:
            st.markdown("---")
            st.subheader("🤖 Help Train Our AI")
            st.write("Was this SQL query helpful? Your feedback improves our AI!")

            col1, col2, col3 = st.columns([1, 1, 3])

            with col1:
                if st.button("👍 Helpful", key=f"pos_{query_log_id}", help="This query was correct and useful"):
                    if save_feedback(query_log_id, "positive"):
                        st.success("✅ Thanks! Feedback saved.")
                        st.rerun()

            with col2:
                if st.button("👎 Not Helpful", key=f"neg_{query_log_id}", help="This query needs improvement"):
                    if save_feedback(query_log_id, "negative"):
                        st.warning("📝 Thanks! We'll improve this.")
                        st.rerun()

            with col3:
                with st.expander("✏️ Suggest Better SQL (Optional)"):
                    corrected_sql = st.text_area(
                        "Enter improved SQL:",
                        value=sql_query,
                        key=f"corr_{query_log_id}",
                        height=100
                    )
                    feedback_comment = st.text_input(
                        "Comment (optional):",
                        key=f"comm_{query_log_id}",
                        placeholder="Why is this better?"
                    )
                    if st.button("Submit Correction", key=f"submit_{query_log_id}"):
                        if save_feedback(query_log_id, "correction", corrected_sql, feedback_comment):
                            st.success("✅ Correction submitted! Very helpful for training.")
                            st.rerun()
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

st.caption("🤖 AI-Powered SQL | 🔒 Read-Only | 🌐 Multi-Industry Database | 📊 Training Data Collection Enabled")
