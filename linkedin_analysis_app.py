import streamlit as st
import pandas as pd
from textblob import TextBlob
import plotly.express as px
from streamlit_lottie import st_lottie
import requests
import re
import uuid

# PAGE CONFIG
st.set_page_config(
    page_title="Wavess 1.0 - LinkedIn Growth Solution",
    layout="wide",
)

# HELPER
def load_lottie(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None

wave_animation = load_lottie("https://assets7.lottiefiles.com/packages/lf20_4kx2q32n.json")

# HEADER SECTION 
col1, col2 = st.columns([0.75, 0.25])
with col1:
    st.markdown("""
        <div style="
            background: linear-gradient(90deg, #007BFF, #00C9A7);
            padding: 20px; border-radius: 15px; color: white;">
            <h1 style="margin:0;"> Wavess 1.0: LinkedIn Growth Solution</h1>
            <p style="margin-top:5px;">Analyze post performance, audience relevance & engagement sentiment</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    try:
        if wave_animation:
            st_lottie(wave_animation, height=120, key="wave_animation_header")
    except:
        pass

st.write("")

# LOAD DATA
try:
    posts = pd.read_csv("data/linkedin_post.csv")
    audience = pd.read_csv("data/audience_data.csv")
    comments = pd.read_csv("data/comments_data.csv")
except FileNotFoundError:
    st.error("Data files missing. Please ensure `data/` folder contains all CSV files.")
    st.stop()

# POST OVERVIEW
st.header("Post Overview")
col1, col2 = st.columns(2)

with col1:
    st.dataframe(posts[['post_id', 'likes', 'comments', 'shares']], use_container_width=True)

with col2:
    st.subheader(" Post Content")
    post_text = posts.loc[0, 'post_text'] if len(posts) > 0 else ""
    st.write(post_text)

# POST SENTIMENT
blob = TextBlob(post_text)
post_sentiment = blob.sentiment.polarity
post_sentiment_label = (
    "Positive 😊" if post_sentiment > 0
    else "Negative 😞" if post_sentiment < 0
    else "Neutral 😐"
)

st.markdown(f"""
<div style="
    background: linear-gradient(90deg, #00C9A7, #007BFF);
    padding: 15px; border-radius: 12px; margin-top:20px; color:white;
    display:flex; justify-content:space-around; text-align:center;">
    <div><h4>Post Sentiment</h4><h2>{post_sentiment_label}</h2><p>{round(post_sentiment, 2)}</p></div>
    <div><h4>❤️ Likes</h4><h2>{int(posts.loc[0, 'likes'])}</h2></div>
    <div><h4>💬 Comments</h4><h2>{int(posts.loc[0, 'comments'])}</h2></div>
    <div><h4>🔁 Shares</h4><h2>{int(posts.loc[0, 'shares'])}</h2></div>
</div>
""", unsafe_allow_html=True)

# HASHTAG & KEYWORD INSIGHTS
st.subheader(" Hashtag & Keyword Insights")
hashtags = re.findall(r"#\w+", post_text)
keywords = [w.lower() for w in re.findall(r"\b\w+\b", post_text) if len(w) > 4]

col1, col2 = st.columns(2)
with col1:
    st.markdown("###  Hashtags Found")
    if hashtags:
        st.write(", ".join(hashtags))
    else:
        st.info("No hashtags found in this post.")

with col2:
    st.markdown("### Common Keywords")
    if keywords:
        keyword_counts = pd.Series(keywords).value_counts().head(5)
        st.dataframe(keyword_counts.rename_axis("Keyword").reset_index(name="Frequency"))
    else:
        st.warning("No significant keywords detected.")

# ENGAGEMENT VISUALIZATION
st.subheader("Engagement Metrics")
engagement_data = posts.loc[0, ['likes', 'comments', 'shares']]
engagement_df = pd.DataFrame({
    'Metric': ['Likes', 'Comments', 'Shares'],
    'Count': engagement_data.values
})

fig_engagement = px.bar(
    engagement_df, x='Metric', y='Count', color='Metric',
    color_discrete_sequence=px.colors.sequential.Aggrnyl,
    title="Engagement Distribution", text='Count'
)
fig_engagement.update_traces(textposition='outside')
fig_engagement.update_layout(showlegend=False, template="plotly_dark")
st.plotly_chart(fig_engagement, use_container_width=True)

# COMMENT SENTIMENT ANALYSIS
st.header("💬 Comment Sentiment Analysis")
comments["sentiment"] = comments["comment_text"].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
avg_comment_sentiment = comments["sentiment"].mean()

col1, col2 = st.columns(2)
with col1:
    st.metric("Avg Comment Sentiment", round(avg_comment_sentiment, 2))
    st.dataframe(comments[['comment_text', 'sentiment']], use_container_width=True)
with col2:
    fig_comments = px.histogram(
        comments, x="sentiment", nbins=10,
        title="Sentiment Distribution of Comments",
        color_discrete_sequence=['#00C9A7']
    )
    fig_comments.update_layout(
        xaxis_title="Sentiment Polarity",
        yaxis_title="Frequency",
        template="plotly_dark"
    )
    st.plotly_chart(fig_comments, use_container_width=True)

# AUDIENCE ICP RELEVANCE
st.header("Audience ICP Relevance")

def map_role_to_field(role):
    role = str(role).lower()
    if "marketing" in role:
        return "Marketing"
    elif "policy" in role or "climate" in role:
        return "Policy"
    elif "esg" in role or "sustainability" in role:
        return "Sustainability"
    elif "research" in role:
        return "Research"
    elif "founder" in role or "tech" in role:
        return "Technology"
    else:
        return "Other"

audience['field'] = audience['role'].apply(map_role_to_field)
avg_relevance = audience["relevance_to_icp"].mean()
field_engagement = (
    audience.groupby("field")["relevance_to_icp"]
    .mean().reset_index().sort_values("relevance_to_icp", ascending=False)
)
top_field = field_engagement.iloc[0]["field"] if len(field_engagement) > 0 else "Unknown"

col1, col2 = st.columns(2)
with col1:
    st.metric("Avg ICP Relevance", f"{round(avg_relevance * 100, 2)}%")
    st.dataframe(audience[["name", "role", "field", "relevance_to_icp"]], use_container_width=True)
with col2:
    fig_audience = px.bar(
        field_engagement, x="relevance_to_icp", y="field",
        orientation='h', color="relevance_to_icp",
        color_continuous_scale='Tealgrn',
        title="Average Relevance by Field"
    )
    fig_audience.update_layout(template="plotly_dark")
    st.plotly_chart(fig_audience, use_container_width=True)

st.success(f" Top audience field: **{top_field}** — showing strongest interest from professionals here.")

# BEST PERFORMING POST 
st.header(" Predicting Best-Performing Post")
posts["engagement_score"] = posts["likes"]*0.5 + posts["comments"]*0.3 + posts["shares"]*0.2
best_post = posts.loc[posts["engagement_score"].idxmax()]

st.success(f"Best performing post is **Post ID {best_post['post_id']}** with score {round(best_post['engagement_score'],2)}")

fig_score = px.bar(
    posts, x='post_id', y='engagement_score', color='engagement_score',
    color_continuous_scale='Viridis', title="Post Engagement Scores"
)
fig_score.update_layout(template="plotly_dark")
st.plotly_chart(fig_score, use_container_width=True)

st.caption("This section is for demo view only — can be extended to compare multiple posts.")

# SUMMARY
st.header(" Final Summary")
st.markdown(f"""
- **Post Sentiment:** {post_sentiment_label}  
- **Avg Comment Sentiment:** {round(avg_comment_sentiment,2)}  
- **Avg ICP Relevance:** {round(avg_relevance*100,2)}%  
- **Top Audience Field:** {top_field}  
- **Best Performing Post ID:** {best_post['post_id']}  
""")

# FUTURE SCOPE
st.header(" Automation & Future Scope")
st.markdown("""
- Connect dashboard to **LinkedIn API** to fetch live posts, comments & metrics.
- Automate data refresh using **Airflow** or **Streamlit Schedule**.
- Use **ML models** to predict engagement based on sentiment, hashtags & audience.
- Add **real-time notifications** for posts exceeding engagement benchmarks.
- Integrate a **post recommender system** for optimal hashtags & content.
""")

st.success("Analysis Complete — Wavess 1.0 Prototype!")
