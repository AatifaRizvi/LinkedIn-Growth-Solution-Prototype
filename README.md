# Wavess 1.0 – LinkedIn Growth Solution Prototype

**Wavess 1.0** is a prototype tool designed to analyze LinkedIn post performance, evaluate audience relevance, and provide actionable insights to optimize engagement. Built with Python and Streamlit, it visualizes key post metrics, sentiment, and audience ICP relevance.

## **Features**

- Extract and analyze post features: text, hashtags, sentiment
- Predict top-performing posts using engagement score
- Analyze audience roles and rank relevance to Ideal Customer Profile (ICP)
- Comment sentiment analysis for audience feedback
- Interactive dashboard with visualizations

**Data**
The project uses three datasets:

-> linkedin_post.csv – Post details including text, likes, comments, shares
-> comments_data.csv – Post comments for sentiment analysis
-> audience_data.csv – Audience roles, seniority, and relevance to ICP

Note: Replace with live LinkedIn data when integrating LinkedIn API.

**Technology Stack**

Python 3.10+
Streamlit for interactive dashboard
Pandas for data manipulation
TextBlob for sentiment analysis
Plotly for dynamic visualizations

**Key Insights**

Positive posts with relevant hashtags drive the highest engagement

Sustainability-focused audience showed the strongest ICP relevance

Comment sentiment provides early indicators of audience perception

**Future Enhancements**

Connect dashboard to LinkedIn API for real-time data
Automate daily or weekly analytics using Cron or Airflow
Integrate machine learning models for post performance prediction
Add a content recommendation engine for optimal hashtags and format
Real-time alerts for posts exceeding performance thresholdsLicense

**Try it locally:**
```bash
git clone https://github.com/AatifaRizvi
cd Wavess-1.0
pip install -r requirements.txt
streamlit run linkedin_analysis_app.py

MIT License © [2025] [Aatifa Rizvi]



