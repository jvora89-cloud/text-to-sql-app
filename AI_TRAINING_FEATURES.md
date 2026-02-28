# 🤖 AI Training System - Complete Guide

## Overview

Your Text-to-SQL app now includes a **comprehensive AI training system** that collects user queries and feedback to continuously improve the AI models. This transforms your app from a simple query tool into a self-improving AI system.

---

## ✅ What Was Added

### 1. Training Data Collection Database
**File:** `create_training_database.py`

Created a SQLite database with 5 tables:
- **query_logs**: Stores every user query and generated SQL
- **user_feedback**: Stores thumbs up/down ratings and corrections
- **training_metrics**: Tracks model performance over time
- **verified_examples**: Curated high-quality training examples
- **model_versions**: Tracks deployed AI models

**Run once to set up:**
```bash
python3 create_training_database.py
```

### 2. Feedback Collection UI
**File:** `app.py` (updated)

Added to the main Streamlit app:
- 👍 Thumbs Up / 👎 Thumbs Down buttons after every query
- ✏️ SQL correction submission form
- 💬 Optional feedback comments
- 📊 Live training statistics in sidebar

### 3. Automatic Query Logging
**File:** `app.py` (updated)

Every query is automatically logged with:
- User's natural language question
- Generated SQL query
- Execution success/failure status
- Error messages (if failed)
- Timestamp and session ID
- Model version used

### 4. Model Fine-Tuning Pipeline
**File:** `train_model.py`

Complete pipeline for training custom models:
- Exports high-quality examples from database
- Filters based on positive feedback
- Generates training scripts for PEFT/LoRA
- Supports Mistral and FLAN-T5 models
- Creates requirements.txt for training

**Usage:**
```bash
python3 train_model.py --model mistral --min-feedback 5 --output models/fine-tuned-v1
```

### 5. Training Dashboard
**File:** `training_dashboard.py`

Comprehensive analytics dashboard showing:
- 📈 Overall statistics (total queries, success rate, feedback)
- 🎓 Training readiness assessment
- 🔍 Recent queries with feedback
- 💭 Feedback analysis and corrections
- 🔬 Query pattern analysis
- 📅 Performance trends over time
- 💾 Data export capabilities

**Run the dashboard:**
```bash
streamlit run training_dashboard.py
```

### 6. Updated Privacy Policy
**Files:** `docs/privacy-policy.html`, `privacy-policy.html`

**CRITICAL CHANGES:**
- ⚠️ Now discloses data collection for AI training
- ⚠️ States that queries are stored indefinitely
- ✅ Explains opt-out and data deletion rights
- ✅ Details what data is/isn't collected
- ✅ GDPR/CCPA compliant

### 7. Updated AI Consent Modal
**File:** `ios-app/www/index.html`

**iOS app now shows:**
- Clear "AI-Powered App with Training" badge
- Explicit disclosure of data collection for training
- List of what is/isn't collected
- Consent checkboxes for data storage
- Link to privacy policy and opt-out instructions

### 8. Updated Privacy Manifest
**File:** `ios-app/ios/App/App/PrivacyInfo.xcprivacy`

Apple privacy manifest now declares:
- Data collection for analytics
- Data collection for product personalization
- Usage data collection
- Purposes: App Functionality, Analytics, Product Personalization

---

## 🚀 How It Works

### User Flow:

1. **User asks a question** → Query logged to training database
2. **AI generates SQL** → SQL saved with query
3. **SQL executes** → Success/failure logged
4. **User provides feedback** → Thumbs up/down or correction saved
5. **Data accumulates** → Training dashboard tracks metrics
6. **Threshold reached** → Model fine-tuning pipeline triggers
7. **New model trained** → Deployed to improve accuracy
8. **Cycle repeats** → Continuous improvement

### Data Lifecycle:

```
User Query
    ↓
Query Logged (training_data.db)
    ↓
Feedback Collected (positive/negative/correction)
    ↓
Training Data Exported (training_data.jsonl)
    ↓
Model Fine-Tuned (PEFT/LoRA)
    ↓
New Model Deployed
    ↓
Better SQL Generation
```

---

## 📊 Training Dashboard Features

### Run Dashboard:
```bash
cd "/Users/jayvora/Downloads/SQL APP"
streamlit run training_dashboard.py
```

### Dashboard Sections:

#### 1. Overall Statistics
- Total queries processed
- Unique user sessions
- Success rate percentage
- User satisfaction (feedback ratio)
- Corrections received
- Verified examples

#### 2. Training Readiness Assessment
Automatically calculates if you have enough data to train:
- ✅ Minimum 100 queries
- ✅ 20%+ feedback coverage
- ✅ 70%+ success rate
- ✅ 10+ corrections

**Readiness Score:** 0-100
- **75+**: Ready to train
- **50-74**: More data recommended
- **<50**: Not ready yet

#### 3. Recent Queries View
- Last 50 queries in table format
- Success/failure status
- Feedback received
- Timestamps

#### 4. Feedback Analysis
- Bar chart of feedback distribution
- Recent corrections with comments
- SQL improvement suggestions

#### 5. Query Pattern Analysis
- Most common queries
- Success rates per query type
- Identifies problematic patterns

#### 6. Performance Trends
- Daily query volume chart
- Daily success rate trends
- 30-day historical data

#### 7. Data Export
- Export training data as CSV
- Export statistics as JSON
- Clean old data (90+ days)

---

## 🎓 Model Training Process

### Step 1: Collect Data (Current Stage)

Use the app normally and encourage users to provide feedback:
- Ask diverse questions
- Click thumbs up/down
- Submit corrections when SQL is wrong

**Goal:** 100+ queries with 20%+ feedback

### Step 2: Assess Readiness

Check training dashboard:
```bash
streamlit run training_dashboard.py
```

Look for readiness score ≥ 75

### Step 3: Export Training Data

```bash
python3 train_model.py --min-feedback 5 --export-only
```

This creates:
- `training_data.jsonl` - Queries with positive feedback
- `verified_examples.jsonl` - Manually verified examples

### Step 4: Generate Training Script

```bash
python3 train_model.py --model mistral --output models/fine-tuned-v1
```

This creates:
- `fine_tune_mistral.py` - Ready-to-run training script
- `requirements_training.txt` - Training dependencies

### Step 5: Install Training Requirements

```bash
pip install -r requirements_training.txt
```

**Note:** Requires PyTorch with CUDA for GPU training

### Step 6: Run Training (Requires GPU)

```bash
python3 fine_tune_mistral.py
```

**Estimated time:**
- GPU (RTX 3090): 2-4 hours
- GPU (A100): 1-2 hours
- CPU: Not recommended (days/weeks)

**Requirements:**
- 16GB+ GPU memory (for 8-bit training)
- 32GB+ RAM
- 50GB+ disk space

### Step 7: Deploy Fine-Tuned Model

Update `app.py` to load your custom model:

```python
# Change from:
llm = HuggingFaceEndpoint(repo_id="mistralai/Mistral-7B-Instruct-v0.2", ...)

# To:
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained("models/fine-tuned-v1")
tokenizer = AutoTokenizer.from_pretrained("models/fine-tuned-v1")
```

### Step 8: Monitor Performance

- Track new queries in training dashboard
- Compare success rates before/after
- Collect more feedback
- Repeat training cycle

---

## 🔒 Privacy & Compliance

### What Changed:

#### ❌ Old Privacy Policy:
- "Queries are not stored"
- "Not used for training AI"

#### ✅ New Privacy Policy:
- "Queries are stored for AI training"
- "Data retained indefinitely"
- "Used to improve AI models"

### Compliance Updates:

1. **iOS Consent Modal:**
   - Now says "AI-Powered App with Training"
   - Lists data collection clearly
   - Requires explicit consent

2. **Privacy Manifest (PrivacyInfo.xcprivacy):**
   - Declares analytics data collection
   - Declares product personalization
   - States purposes clearly

3. **App Store Connect:**
   - Update app description to mention AI training
   - In "App Privacy" section, declare:
     - ✅ Collects "Other Usage Data"
     - ✅ Purpose: Analytics, Product Personalization
     - ✅ Linked to user: NO
     - ✅ Used for tracking: NO

### User Rights:

Users can now:
- **Opt-Out:** Email privacy@texttosql.app with Session ID
- **Request Deletion:** 30-day deletion of their queries
- **Access Data:** Request JSON export of their queries
- **Withdraw Consent:** Stop using the app

---

## 📝 App Store Submission Updates

### Before Submitting:

1. **Test Feedback System:**
   - Submit queries
   - Click thumbs up/down
   - Submit a correction
   - Verify data appears in training dashboard

2. **Update App Store Description:**

Add to description:
```
🤖 CONTINUOUS LEARNING:
This app improves over time using AI training. Your queries and feedback
help train better models. All data is anonymous and you can opt-out anytime.
```

3. **App Review Notes:**

Add to "App Review Information":
```
AI TRAINING DISCLOSURE:
This app collects user queries and feedback to train AI models. This is
clearly disclosed in the consent modal and privacy policy. Users can
opt-out via privacy@texttosql.app.

Training data is anonymous (no personal info) and used solely to improve
SQL generation accuracy.
```

4. **App Privacy Section:**

In App Store Connect → App Privacy:
- ❓ Do you collect data? → **YES**
- Select: **Other Usage Data**
  - Linked to user? → **NO**
  - Used for tracking? → **NO**
  - Purposes: **Analytics, Product Personalization**

---

## 🎯 Best Practices

### For Better Training Data:

1. **Encourage Feedback:**
   - Add incentives for feedback (e.g., "Help improve AI!")
   - Show impact ("Your feedback trained 10 better queries today")

2. **Quality Over Quantity:**
   - Verify corrections manually
   - Mark high-quality examples in `verified_examples` table

3. **Diverse Queries:**
   - Test edge cases
   - Try complex queries
   - Test different table combinations

4. **Regular Training Cycles:**
   - Train every 500-1000 new queries
   - Compare model versions
   - A/B test old vs new models

### For Privacy Compliance:

1. **Honor Opt-Outs:**
   - Create process to exclude Session IDs from training
   - Respond to deletion requests within 30 days

2. **Data Minimization:**
   - Don't collect IP addresses
   - Don't store device identifiers
   - Keep data anonymous

3. **Transparency:**
   - Keep privacy policy updated
   - Make opt-out easy
   - Respond to user inquiries

---

## 🛠️ Deployment

### Update Hugging Face Space:

```bash
cd "/Users/jayvora/Downloads/SQL APP"

# Copy training files to HF Space branch
git checkout hf-space
git merge main  # Merge AI training features

# Add new files
git add create_training_database.py
git add train_model.py
git add training_dashboard.py
git add training_data.db

# Update requirements
echo "pandas>=2.0.0" >> requirements.txt

# Commit
git commit -m "Add AI training system with feedback collection"

# Push to Hugging Face
git push origin hf-space
```

### Initialize Training Database on HF Space:

Add to `Dockerfile`:
```dockerfile
RUN python3 create_training_database.py
```

Or run once after deployment:
```bash
# SSH into HF Space or use Space Secrets to run:
python3 create_training_database.py
```

### Access Training Dashboard:

If deploying as multi-page app on HF Spaces:
```
https://jayyvora-text-to-sql-app.hf.space/?page=training_dashboard
```

Or run locally:
```bash
streamlit run training_dashboard.py --server.port 8502
```

---

## 📈 Success Metrics

Track these KPIs:

### Data Collection:
- ✅ 100+ queries/week
- ✅ 20%+ feedback rate
- ✅ 10+ corrections/week

### Model Performance:
- ✅ 70%+ SQL success rate
- ✅ 60%+ user satisfaction
- ✅ Improving trends over time

### Training Cycles:
- ✅ First model: After 100 queries
- ✅ Second model: After 500 queries
- ✅ Monthly retraining thereafter

---

## 🚨 Important Warnings

### ⚠️ App Store Rejection Risks:

1. **Privacy Disclosure:** Must be crystal clear about data collection
2. **Consent Required:** Users must explicitly consent to training
3. **Opt-Out Required:** Must provide easy way to opt-out
4. **Data Deletion:** Must honor deletion requests

### ⚠️ Technical Risks:

1. **Database Size:** `training_data.db` will grow indefinitely
   - Solution: Implement data archiving after 90 days

2. **Performance:** Large databases may slow queries
   - Solution: Index optimization, periodic cleanup

3. **Storage Costs:** HF Spaces has storage limits
   - Solution: Export old data to external storage

### ⚠️ Legal Risks:

1. **GDPR Compliance:** Must honor EU data rights
2. **CCPA Compliance:** Must honor California data rights
3. **Children's Privacy:** Don't market to children

---

## 📚 Files Reference

### Core Files:
- `create_training_database.py` - Database setup
- `app.py` - Main app with feedback UI
- `train_model.py` - Training pipeline
- `training_dashboard.py` - Analytics dashboard

### Documentation:
- `AI_TRAINING_FEATURES.md` - This file
- `APP_STORE_COMPLIANCE.md` - App Store guidelines

### Privacy:
- `docs/privacy-policy.html` - Updated privacy policy
- `ios-app/www/index.html` - Updated consent modal
- `ios-app/ios/App/App/PrivacyInfo.xcprivacy` - Privacy manifest

### Database:
- `training_data.db` - SQLite training database
- `training_data.jsonl` - Exported training examples
- `verified_examples.jsonl` - Curated examples

---

## 🎉 What's Next?

1. **Deploy to HF Space** - Push AI training features
2. **Enable GitHub Pages** - For updated privacy policy
3. **Test Everything** - Query → Feedback → Dashboard → Export
4. **Collect Initial Data** - Get 100+ queries with feedback
5. **Train First Model** - When readiness score ≥ 75
6. **Submit to App Store** - With updated privacy disclosures
7. **Monitor & Iterate** - Continuous improvement cycle

---

## 💡 Tips for Success

1. **Start Small:** Collect 100 queries before first training
2. **Quality Feedback:** Manually verify a few corrections
3. **Regular Monitoring:** Check dashboard weekly
4. **Iterate Fast:** Train new models every 2-4 weeks
5. **Measure Impact:** Compare model versions with A/B testing
6. **Stay Compliant:** Keep privacy policy updated
7. **Engage Users:** Show how feedback improves the app

---

**Your app is now a self-improving AI system!** 🚀

Every query makes it smarter. Every piece of feedback trains better models.
This is the future of AI applications - continuously learning from real users.

**Ready to deploy?** Let's push these changes to production!
