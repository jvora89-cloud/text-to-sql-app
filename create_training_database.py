import sqlite3
from datetime import datetime

def create_training_database():
    """Create database for AI training data collection"""
    conn = sqlite3.connect('training_data.db')
    cursor = conn.cursor()

    # Table 1: Query logs - stores every user query and generated SQL
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS query_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_query TEXT NOT NULL,
            generated_sql TEXT NOT NULL,
            execution_success INTEGER DEFAULT 0,
            execution_result TEXT,
            error_message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            session_id TEXT,
            model_used TEXT
        )
    ''')

    # Table 2: User feedback - thumbs up/down and corrections
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_log_id INTEGER NOT NULL,
            feedback_type TEXT NOT NULL,  -- 'positive', 'negative', 'correction'
            corrected_sql TEXT,
            feedback_comment TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (query_log_id) REFERENCES query_logs(id)
        )
    ''')

    # Table 3: Training metrics - track model performance over time
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS training_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_version TEXT NOT NULL,
            accuracy_score REAL,
            avg_execution_success REAL,
            total_queries INTEGER,
            positive_feedback INTEGER,
            negative_feedback INTEGER,
            training_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            notes TEXT
        )
    ''')

    # Table 4: Verified training examples - curated high-quality examples
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS verified_examples (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_log_id INTEGER,
            natural_language TEXT NOT NULL,
            correct_sql TEXT NOT NULL,
            database_schema TEXT,
            difficulty_level TEXT,  -- 'easy', 'medium', 'hard'
            verified_by TEXT,
            verified_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            used_in_training INTEGER DEFAULT 0,
            FOREIGN KEY (query_log_id) REFERENCES query_logs(id)
        )
    ''')

    # Table 5: Model versions - track deployed models
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS model_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version_name TEXT NOT NULL UNIQUE,
            model_type TEXT NOT NULL,  -- 'mistral', 'flan-t5', 'custom'
            base_model TEXT,
            fine_tuned INTEGER DEFAULT 0,
            training_data_size INTEGER,
            deployment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 0,
            performance_notes TEXT
        )
    ''')

    # Create indexes for performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_query_timestamp ON query_logs(timestamp)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_feedback_query ON user_feedback(query_log_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_execution_success ON query_logs(execution_success)')

    # Insert initial model version
    cursor.execute('''
        INSERT OR IGNORE INTO model_versions
        (version_name, model_type, base_model, is_active, performance_notes)
        VALUES ('baseline-v1.0', 'mistral', 'mistralai/Mistral-7B-Instruct-v0.2', 1,
                'Initial model using Hugging Face Inference API')
    ''')

    conn.commit()
    conn.close()
    print("✅ Training database created successfully!")
    print("📊 Tables created:")
    print("   - query_logs: Stores all user queries and generated SQL")
    print("   - user_feedback: Stores user ratings and corrections")
    print("   - training_metrics: Tracks model performance over time")
    print("   - verified_examples: Curated training examples")
    print("   - model_versions: Deployed model tracking")

if __name__ == "__main__":
    create_training_database()
