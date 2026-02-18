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

A conversational database interface that translates natural language questions into SQL queries using Hugging Face Inference API, LangChain, and Streamlit.

## Features

- 🗣️ Ask questions in plain English
- 🔍 Automatic SQL query generation using Mistral-7B-Instruct
- 📊 View query results in real-time
- ⚡ Fast inference using Hugging Face's serverless API
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

- **Hugging Face Inference API + Mistral-7B** - LLM for SQL generation
- **LangChain** - AI-to-database connector framework
- **Streamlit** - Web application interface
- **SQLite** - Embedded database

## Setup

This Space uses Hugging Face's Inference API with Meta-Llama-3-8B-Instruct model. When running on Hugging Face Spaces, authentication is handled automatically - no additional setup needed!

### Local Development

For local development:
1. Get a Hugging Face token from https://huggingface.co/settings/tokens
2. Create a `.env` file with: `HF_TOKEN=your_token_here`
3. Run: `streamlit run app.py`
