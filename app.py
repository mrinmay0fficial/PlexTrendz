import streamlit as st
import scrapetube
import pandas as pd
import plotly.express as px
from collections import Counter
import re

# UI Setup
st.set_page_config(page_title="PlexTrendz Pro", page_icon="🎬", layout="wide")

# Custom CSS for that "Premium" feel
st.markdown("""
    <style>
    .main { background-color: #0a0a0f; }
    .stMetric { border: 1px solid #7c6af7; border-radius: 10px; padding: 10px; background: #1e1e28; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 PlexTrendz Pro")
st.caption("Advanced YouTube Metadata & Keyword Intelligence System")

# Sidebar
with st.sidebar:
    st.header("Control Panel")
    target_topic = st.text_input("Niche/Keyword", "Data Science Roadmap")
    limit = st.slider("Deep Scan Limit", 20, 100, 50)
    sort_by = st.selectbox("Algorithm Strategy", ["relevance", "view_count", "upload_date"])
    st.divider()
    st.info("Tip: Higher scan limits provide better keyword trends but take longer.")

def fetch_data(query, video_limit, sort):
    videos = scrapetube.get_search(query, limit=video_limit, sort_by=sort)
    data = []
    all_titles_text = ""
    
    for i, video in enumerate(videos):
        title = video.get('title', {}).get('runs', [{}])[0].get('text', 'Unknown')
        v_id = video.get('videoId')
        view_text = video.get('viewCountText', {}).get('simpleText', '0 views')
        
        all_titles_text += " " + title.lower()
        
        data.append({
            'Rank': i + 1,
            'Title': title,
            'Views': view_text,
            'Title Length': len(title),
            'Link': f"https://youtube.com/watch?v={v_id}"
        })
    return pd.DataFrame(data), all_titles_text

if st.button("Execute Deep Scan"):
    with st.spinner("Mining YouTube Metadata..."):
        df, raw_text = fetch_data(target_topic, limit, sort_by)
        
        if not df.empty:
            # --- ROW 1: Metrics ---
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Optimal Title Length", f"{int(df['Title Length'].mean())} chars")
            with c2:
                # Basic Keyword Extractor
                words = re.findall(r'\w+', raw_text)
                common_words = [w for w in words if len(w) > 3 and w not in ['youtube', 'video', '2025', '2026']]
                top_word = Counter(common_words).most_common(1)[0][0]
                st.metric("Hot Keyword", f"'{top_word}'")
            with c3:
                st.metric("Competition Strength", "High" if limit > 40 else "Medium")

            # --- ROW 2: Charts ---
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.subheader("Title Length vs. Search Rank")
                fig1 = px.scatter(df, x="Title Length", y="Rank", hover_name="Title", 
                                 template="plotly_dark", color="Title Length",
                                 color_continuous_scale="RdYlGn_r")
                fig1.update_yaxes(autorange="reversed")
                st.plotly_chart(fig1, use_container_width=True)
                
            with col_b:
                st.subheader("Keyword Frequency (Top 10)")
                word_counts = Counter(common_words).most_common(10)
                word_df = pd.DataFrame(word_counts, columns=['Keyword', 'Frequency'])
                fig2 = px.bar(word_df, x="Frequency", y="Keyword", orientation='h',
                              template="plotly_dark", color="Frequency")
                st.plotly_chart(fig2, use_container_width=True)

            # --- ROW 3: Table ---
            st.divider()
            st.subheader("Raw Competitive Intelligence")
            st.dataframe(df, use_container_width=True)
            
        else:
            st.error("No results found.")
