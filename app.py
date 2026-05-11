import streamlit as st
import scrapetube
import pandas as pd
import plotly.express as px

# UI Setup with your signature styling
st.set_page_config(page_title="PlexTrendz", page_icon="🎬", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0a0a0f; color: #f0eeff; }
    .stMetric { background-color: #1e1e28; padding: 15px; border-radius: 10px; border: 1px solid rgba(124,106,247,0.2); }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 PlexTrendz")
st.subheader("Data-Driven YouTube Analysis (No API Required)")

# Sidebar Settings
with st.sidebar:
    st.header("Search Settings")
    target_topic = st.text_input("Niche/Keyword", "Gaming Cinematics")
    limit = st.slider("Videos to Analyze", 10, 100, 30)
    sort_by = st.selectbox("Sort Strategy", ["relevance", "view_count", "upload_date", "rating"])

def fetch_data(query, video_limit, sort):
    videos = scrapetube.get_search(query, limit=video_limit, sort_by=sort)
    data = []
    for video in videos:
        # Extract title and ID
        title_data = video.get('title', {}).get('runs', [{}])[0].get('text', 'Unknown Title')
        v_id = video.get('videoId')
        
        # Views handling (Scrapetube returns text like "1.2M views")
        view_text = video.get('viewCountText', {}).get('simpleText', '0 views')
        
        data.append({
            'Title': title_data,
            'Views': view_text,
            'Title Length': len(title_data),
            'Link': f"https://youtube.com/watch?v={v_id}"
        })
    return pd.DataFrame(data)

if st.button("Start PlexTrendz Analysis"):
    with st.spinner("Analyzing YouTube trends..."):
        df = fetch_data(target_topic, limit, sort_by)
        
        if not df.empty:
            # Metrics
            avg_len = int(df['Title Length'].mean())
            st.metric("Avg. Optimal Title Length", f"{avg_len} Chars")
            
            # Scatter Plot: Title Length vs Ranking
            df['Rank'] = range(1, len(df) + 1)
            fig = px.scatter(df, x="Title Length", y="Rank", hover_name="Title", 
                             template="plotly_dark", title="Title Length vs Search Rank",
                             color_discrete_sequence=['#38d9a9'])
            fig.update_yaxes(autorange="reversed") # Rank 1 at top
            st.plotly_chart(fig, use_container_width=True)
            
            # Data Table
            st.subheader("Top Results Detailed View")
            st.dataframe(df[['Title', 'Views', 'Title Length', 'Link']], use_container_width=True)
        else:
            st.error("No data found for this keyword.")
