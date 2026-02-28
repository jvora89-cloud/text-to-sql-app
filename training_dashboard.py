import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import json

st.set_page_config(
    page_title="AI Training Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI Model Training Dashboard")
st.markdown("Monitor training data collection, user feedback, and model performance")

# Database connection
def get_connection():
    return sqlite3.connect('training_data.db')

# Metrics Section
st.header("📈 Overall Statistics")

conn = get_connection()
cursor = conn.cursor()

# Get overall stats
cursor.execute('SELECT COUNT(*) FROM query_logs')
total_queries = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM query_logs WHERE execution_success = 1')
successful_queries = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM user_feedback WHERE feedback_type = "positive"')
positive_feedback = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM user_feedback WHERE feedback_type = "negative"')
negative_feedback = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM user_feedback WHERE feedback_type = "correction"')
corrections = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM verified_examples')
verified_examples = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(DISTINCT session_id) FROM query_logs')
unique_sessions = cursor.fetchone()[0]

# Display metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Queries", total_queries)
    st.metric("Unique Sessions", unique_sessions)

with col2:
    success_rate = (successful_queries / total_queries * 100) if total_queries > 0 else 0
    st.metric("Success Rate", f"{success_rate:.1f}%")
    st.metric("Successful Queries", successful_queries)

with col3:
    total_feedback = positive_feedback + negative_feedback
    satisfaction_rate = (positive_feedback / total_feedback * 100) if total_feedback > 0 else 0
    st.metric("User Satisfaction", f"{satisfaction_rate:.1f}%")
    st.metric("Total Feedback", total_feedback)

with col4:
    st.metric("Corrections Received", corrections)
    st.metric("Verified Examples", verified_examples)

# Training Readiness Assessment
st.header("🎓 Training Readiness")

readiness_score = 0
max_score = 100

col1, col2 = st.columns(2)

with col1:
    st.subheader("Data Quality Checklist")

    # Check 1: Minimum queries
    if total_queries >= 100:
        st.success("✅ Sufficient queries (100+)")
        readiness_score += 25
    elif total_queries >= 50:
        st.warning(f"⚠️ Limited queries ({total_queries}/100)")
        readiness_score += 10
    else:
        st.error(f"❌ Insufficient queries ({total_queries}/100)")

    # Check 2: Feedback coverage
    feedback_coverage = (total_feedback / total_queries * 100) if total_queries > 0 else 0
    if feedback_coverage >= 20:
        st.success(f"✅ Good feedback coverage ({feedback_coverage:.1f}%)")
        readiness_score += 25
    elif feedback_coverage >= 10:
        st.warning(f"⚠️ Low feedback coverage ({feedback_coverage:.1f}%)")
        readiness_score += 10
    else:
        st.error(f"❌ Very low feedback coverage ({feedback_coverage:.1f}%)")

    # Check 3: Success rate
    if success_rate >= 70:
        st.success(f"✅ High success rate ({success_rate:.1f}%)")
        readiness_score += 25
    elif success_rate >= 50:
        st.warning(f"⚠️ Moderate success rate ({success_rate:.1f}%)")
        readiness_score += 10
    else:
        st.error(f"❌ Low success rate ({success_rate:.1f}%)")

    # Check 4: Corrections
    if corrections >= 10:
        st.success(f"✅ Good correction count ({corrections})")
        readiness_score += 25
    elif corrections >= 5:
        st.warning(f"⚠️ Limited corrections ({corrections})")
        readiness_score += 10
    else:
        st.error(f"❌ Few corrections ({corrections})")

with col2:
    st.subheader("Training Readiness Score")
    st.progress(readiness_score / max_score)
    st.metric("Readiness", f"{readiness_score}/{max_score}")

    if readiness_score >= 75:
        st.success("🎉 Ready to start training!")
        st.info("Run: `python train_model.py --min-feedback 5`")
    elif readiness_score >= 50:
        st.warning("⚠️ More data recommended before training")
        st.info("Collect more user feedback to improve model quality")
    else:
        st.error("❌ Not ready for training yet")
        st.info("Continue using the app and collecting feedback")

# Recent Queries
st.header("🔍 Recent Queries")

cursor.execute('''
    SELECT
        ql.id,
        ql.user_query,
        ql.generated_sql,
        ql.execution_success,
        ql.timestamp,
        COALESCE(
            (SELECT GROUP_CONCAT(feedback_type)
             FROM user_feedback
             WHERE query_log_id = ql.id), 'No feedback'
        ) as feedback
    FROM query_logs ql
    ORDER BY ql.timestamp DESC
    LIMIT 50
''')

recent_queries = cursor.fetchall()

if recent_queries:
    df = pd.DataFrame(recent_queries, columns=['ID', 'Query', 'Generated SQL', 'Success', 'Timestamp', 'Feedback'])
    df['Success'] = df['Success'].map({1: '✅', 0: '❌'})

    st.dataframe(
        df,
        use_container_width=True,
        column_config={
            "Query": st.column_config.TextColumn("User Query", width="medium"),
            "Generated SQL": st.column_config.TextColumn("Generated SQL", width="large"),
            "Success": st.column_config.TextColumn("Status", width="small"),
            "Feedback": st.column_config.TextColumn("Feedback", width="small")
        }
    )
else:
    st.info("No queries logged yet. Use the main app to generate queries.")

# Feedback Analysis
st.header("💭 Feedback Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Feedback Distribution")

    feedback_data = {
        'Positive': positive_feedback,
        'Negative': negative_feedback,
        'Corrections': corrections
    }

    if sum(feedback_data.values()) > 0:
        chart_data = pd.DataFrame(list(feedback_data.items()), columns=['Type', 'Count'])
        st.bar_chart(chart_data.set_index('Type'))
    else:
        st.info("No feedback collected yet")

with col2:
    st.subheader("Recent Corrections")

    cursor.execute('''
        SELECT
            ql.user_query,
            uf.corrected_sql,
            uf.feedback_comment,
            uf.timestamp
        FROM user_feedback uf
        JOIN query_logs ql ON uf.query_log_id = ql.id
        WHERE uf.feedback_type = 'correction'
        ORDER BY uf.timestamp DESC
        LIMIT 10
    ''')

    corrections_data = cursor.fetchall()

    if corrections_data:
        for i, (query, sql, comment, timestamp) in enumerate(corrections_data, 1):
            with st.expander(f"Correction #{i} - {timestamp}"):
                st.write(f"**Query:** {query}")
                st.code(sql, language='sql')
                if comment:
                    st.write(f"**Comment:** {comment}")
    else:
        st.info("No corrections submitted yet")

# Query Patterns
st.header("🔬 Query Pattern Analysis")

cursor.execute('''
    SELECT
        user_query,
        COUNT(*) as frequency,
        SUM(execution_success) as successes
    FROM query_logs
    GROUP BY user_query
    HAVING frequency > 1
    ORDER BY frequency DESC
    LIMIT 10
''')

patterns = cursor.fetchall()

if patterns:
    st.subheader("Most Common Queries")
    pattern_df = pd.DataFrame(patterns, columns=['Query', 'Frequency', 'Successes'])
    pattern_df['Success Rate'] = (pattern_df['Successes'] / pattern_df['Frequency'] * 100).round(1)

    st.dataframe(pattern_df, use_container_width=True)
else:
    st.info("Not enough data for pattern analysis yet")

# Model Performance Over Time
st.header("📅 Performance Trends")

cursor.execute('''
    SELECT
        DATE(timestamp) as date,
        COUNT(*) as queries,
        SUM(execution_success) as successes
    FROM query_logs
    WHERE timestamp >= datetime('now', '-30 days')
    GROUP BY DATE(timestamp)
    ORDER BY date
''')

trends = cursor.fetchall()

if trends:
    trend_df = pd.DataFrame(trends, columns=['Date', 'Queries', 'Successes'])
    trend_df['Success Rate'] = (trend_df['Successes'] / trend_df['Queries'] * 100).round(1)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Daily Query Volume")
        st.line_chart(trend_df.set_index('Date')['Queries'])

    with col2:
        st.subheader("Daily Success Rate")
        st.line_chart(trend_df.set_index('Date')['Success Rate'])
else:
    st.info("Not enough historical data for trends yet")

# Export Data
st.header("💾 Export Training Data")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📥 Export Training Data"):
        cursor.execute('''
            SELECT
                ql.user_query,
                ql.generated_sql,
                ql.execution_success
            FROM query_logs ql
            LEFT JOIN user_feedback uf ON ql.id = uf.query_log_id
            WHERE ql.execution_success = 1
            AND (uf.feedback_type = 'positive' OR uf.feedback_type = 'correction')
        ''')
        export_data = cursor.fetchall()

        if export_data:
            export_df = pd.DataFrame(export_data, columns=['Query', 'SQL', 'Success'])
            csv = export_df.to_csv(index=False)
            st.download_button(
                "Download CSV",
                csv,
                "training_data.csv",
                "text/csv"
            )
            st.success(f"Exported {len(export_data)} examples")
        else:
            st.warning("No training data to export yet")

with col2:
    if st.button("📊 Export Statistics"):
        stats = {
            'total_queries': total_queries,
            'successful_queries': successful_queries,
            'success_rate': success_rate,
            'positive_feedback': positive_feedback,
            'negative_feedback': negative_feedback,
            'corrections': corrections,
            'verified_examples': verified_examples,
            'unique_sessions': unique_sessions,
            'readiness_score': readiness_score
        }

        json_str = json.dumps(stats, indent=2)
        st.download_button(
            "Download JSON",
            json_str,
            "training_stats.json",
            "application/json"
        )

with col3:
    if st.button("🧹 Clear Old Data"):
        st.warning("⚠️ This will delete queries older than 90 days")
        if st.checkbox("I confirm deletion"):
            cursor.execute('''
                DELETE FROM query_logs
                WHERE timestamp < datetime('now', '-90 days')
            ''')
            conn.commit()
            deleted = cursor.rowcount
            st.success(f"Deleted {deleted} old queries")

conn.close()

# Footer
st.markdown("---")
st.caption("🤖 AI Training Dashboard | Text to SQL AI | Refresh page to update metrics")
