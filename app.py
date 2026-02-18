import streamlit as st
import sqlite3
import os
import requests
from pathlib import Path

# Create database if it doesn't exist
if not Path("students.db").exists():
    import create_database
    create_database.create_database()

st.set_page_config(page_title="Text-to-SQL App", page_icon="🗃️", layout="wide")
st.title("🗃️ Text-to-SQL Query App")
st.markdown("Ask questions about student grades in natural language!")

HF_TOKEN = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_TOKEN")

@st.cache_resource
def get_db():
    conn = sqlite3.connect('students.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='students'")
    schema = cursor.fetchone()[0]
    return conn, schema

conn, schema = get_db()

with st.sidebar:
    st.header("📊 Database Info")
    st.code("students: id, name, subject, score, grade")
    st.markdown("**Example:**")
    st.markdown("- Who got the highest score?")
    st.markdown("- Show all grade A students")

question = st.text_input("Enter your question:", placeholder="Who are the top students?")

def generate_sql(prompt, token):
    url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    payload = {"inputs": f"Generate SQL for: {prompt}\nSchema: {schema}\nSQL:", "parameters": {"max_new_tokens": 100, "temperature": 0.1}}
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        r.raise_for_status()
        result = r.json()
        return result[0]['generated_text'] if isinstance(result, list) else ""
    except:
        return "SELECT * FROM students LIMIT 5;"

if st.button("Generate SQL & Execute", type="primary"):
    if question:
        with st.spinner("Generating..."):
            sql = generate_sql(question, HF_TOKEN)
            sql = sql.strip().split('\n')[0].strip()
            
            st.subheader("SQL Query:")
            st.code(sql, language="sql")
            
            try:
                cursor = conn.cursor()
                cursor.execute(sql)
                results = cursor.fetchall()
                
                if results:
                    st.success(f"Found {len(results)} results!")
                    cols = [d[0] for d in cursor.description]
                    st.table([dict(zip(cols, row)) for row in results])
                else:
                    st.info("No results found.")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Enter a question first.")

with st.expander("📋 Sample Data"):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students LIMIT 5")
    results = cursor.fetchall()
    cols = [d[0] for d in cursor.description]
    st.table([dict(zip(cols, row)) for row in results])
