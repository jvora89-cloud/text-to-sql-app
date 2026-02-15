---
title: Text-to-SQL App
emoji: 🗃️
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
---

# Text-to-SQL App 🗃️

A conversational database interface that translates natural language questions into SQL queries using Ollama, LangChain, and Streamlit.

## Features

- 🗣️ Ask questions in plain English
- 🔍 Automatic SQL query generation using Llama 3
- 📊 View query results in real-time
- 🔒 100% local execution (no external APIs)
- 💾 SQLite database with student grades

## How to Use

1. Type your question in natural language (e.g., "Who got the highest score in Mathematics?")
2. Click "Generate SQL & Execute"
3. View the generated SQL query and results

## Example Questions

- "Who got the highest score in Mathematics?"
- "Show all students with grade A"
- "What is the average score for each subject?"
- "List all grades for Alice Johnson"
- "Who are the top 3 students by average score?"

## Tech Stack

- **Ollama + Llama 3** - Local LLM for SQL generation
- **LangChain** - AI-to-database connector framework
- **Streamlit** - Web application interface
- **SQLite** - Embedded database

## Note

This Space uses Ollama with Llama 3 model running inside Docker. First startup may take a few minutes while the model downloads.
