# Text-to-SQL App

A conversational database interface that translates natural language questions into SQL queries using Python, Ollama, LangChain, Streamlit, and SQLite.

## Features

- 🗣️ Ask questions in plain English
- 🔍 Automatic SQL query generation
- 📊 View query results in real-time
- 🔒 100% local execution (no cloud APIs)
- 💾 SQLite database with student grades

## Tech Stack

- **Python** - orchestration layer
- **Ollama** - locally-hosted language model runtime
- **LangChain** - AI-to-database connector framework
- **Streamlit** - web application interface
- **SQLite** - embedded database

## Prerequisites

### 1. Install Ollama

Download and install Ollama from [ollama.com](https://ollama.com)

### 2. Pull the Llama 3 Model

```bash
ollama pull llama3
```

### 3. Verify Ollama is Running

```bash
ollama list
```

You should see `llama3` in the list of models.

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create the Database

```bash
python create_database.py
```

This will create a `students.db` file with sample student grade data.

## Usage

### 1. Start the Streamlit App

```bash
streamlit run app.py
```

### 2. Open Your Browser

The app should automatically open at `http://localhost:8501`

### 3. Ask Questions!

Try these example questions:
- "Who got the highest score in Mathematics?"
- "Show all students with grade A"
- "What is the average score for each subject?"
- "List all grades for Alice Johnson"
- "Who are the top 3 students by average score?"

## How It Works

1. **User Input**: You type a question in natural language
2. **SQL Generation**: LangChain sends your question + database schema to Llama 3 via Ollama
3. **Query Execution**: The generated SQL query runs against the SQLite database
4. **Results Display**: Results are shown in the Streamlit interface

## Database Schema

```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    subject TEXT NOT NULL,
    score INTEGER NOT NULL,
    grade TEXT NOT NULL
)
```

## Troubleshooting

### "LLM initialization error"
- Make sure Ollama is running in the background
- Verify llama3 model is installed: `ollama list`
- Try running: `ollama serve`

### "Database connection error"
- Run `python create_database.py` to create the database
- Check that `students.db` file exists in the project directory

### Slow Response Times
- First query may take longer as the model loads
- Subsequent queries should be faster
- Consider using a smaller model like `llama3.2` if performance is an issue

## Privacy & Security

This application runs entirely on your local machine:
- ✅ No data sent to external APIs
- ✅ No cloud costs
- ✅ Full control over your data
- ✅ Works offline (after model download)

## Customization

### Using a Different Model

Edit `app.py` and change the model name:

```python
llm = ChatOllama(
    model="llama3.2",  # or mistral, codellama, etc.
    temperature=0
)
```

### Adding Your Own Database

Replace the database connection in `app.py`:

```python
db = SQLDatabase.from_uri("sqlite:///your_database.db")
```

## License

This project is based on the tutorial from [amanxai.com](https://amanxai.com/2026/02/08/build-your-first-text-to-sql-app/)

## Next Steps

- Add more complex queries
- Implement query history
- Add data visualization
- Support multiple tables with JOIN operations
- Add authentication for sensitive databases
