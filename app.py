import streamlit as st
from langchain_community.utilities import SQLDatabase
from langchain_ollama import ChatOllama
from langchain.chains import create_sql_query_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

# Page configuration
st.set_page_config(
    page_title="Text-to-SQL App",
    page_icon="🗃️",
    layout="wide"
)

st.title("🗃️ Text-to-SQL Query App")
st.markdown("Ask questions about student grades in natural language!")

# Initialize database connection
@st.cache_resource
def init_database():
    """Initialize SQLite database connection"""
    try:
        db = SQLDatabase.from_uri("sqlite:///students.db")
        return db
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None

# Initialize LLM
@st.cache_resource
def init_llm():
    """Initialize Ollama LLM"""
    try:
        llm = ChatOllama(
            model="llama3",
            temperature=0  # Zero temperature for precise SQL generation
        )
        return llm
    except Exception as e:
        st.error(f"LLM initialization error: {e}")
        st.info("Make sure Ollama is running and llama3 model is installed.")
        return None

# Create SQL query chain
@st.cache_resource
def create_chain(_db, _llm):
    """Create the LangChain SQL query generation chain"""

    # Custom prompt template
    template = """You are a SQL expert. Given an input question, create a syntactically correct SQLite query to run.

Database schema:
{schema}

Question: {question}

IMPORTANT: Return ONLY the SQL query without any explanations, markdown formatting, or additional text."""

    prompt = PromptTemplate(
        template=template,
        input_variables=["schema", "question"]
    )

    # Create chain
    chain = (
        prompt
        | _llm
        | StrOutputParser()
    )

    return chain

# Initialize components
db = init_database()
llm = init_llm()

if db and llm:
    chain = create_chain(db, llm)

    # Sidebar with database info
    with st.sidebar:
        st.header("📊 Database Info")
        st.markdown("**Table:** students")
        st.markdown("**Columns:**")
        st.code("""
- id (INTEGER)
- name (TEXT)
- subject (TEXT)
- score (INTEGER)
- grade (TEXT)
        """)

        st.markdown("---")
        st.markdown("**Example Questions:**")
        st.markdown("""
- Who got the highest score in Mathematics?
- Show all students with grade A
- What is the average score for each subject?
- List all grades for Alice Johnson
        """)

    # Main interface
    question = st.text_input(
        "Enter your question:",
        placeholder="e.g., Who are the top 3 students by average score?"
    )

    if st.button("Generate SQL & Execute", type="primary"):
        if question:
            with st.spinner("Generating SQL query..."):
                try:
                    # Generate SQL query
                    sql_query = chain.invoke({
                        "schema": db.get_table_info(),
                        "question": question
                    })

                    # Clean up the SQL query (remove any markdown or extra text)
                    sql_query = sql_query.strip()
                    if sql_query.startswith("```"):
                        sql_query = sql_query.split("```")[1]
                        if sql_query.startswith("sql"):
                            sql_query = sql_query[3:]
                    sql_query = sql_query.strip()

                    # Display generated SQL
                    st.subheader("Generated SQL Query:")
                    st.code(sql_query, language="sql")

                    # Execute query
                    with st.spinner("Executing query..."):
                        result = db.run(sql_query)

                        st.subheader("Query Results:")
                        if result:
                            st.success("Query executed successfully!")
                            st.text(result)
                        else:
                            st.info("Query executed but returned no results.")

                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.info("Try rephrasing your question or check if the database exists.")
        else:
            st.warning("Please enter a question first.")

    # Display sample data
    with st.expander("📋 View Sample Data"):
        try:
            sample_data = db.run("SELECT * FROM students LIMIT 10")
            st.text(sample_data)
        except Exception as e:
            st.error(f"Error loading sample data: {e}")

else:
    st.error("Failed to initialize the application. Please check:")
    st.markdown("""
    1. Ollama is installed and running
    2. Run `ollama pull llama3` to download the model
    3. The database file exists (run `python create_database.py`)
    """)
