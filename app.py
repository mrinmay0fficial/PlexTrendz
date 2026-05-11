import streamlit as st
import scrapetube
import pandas as pd
import plotly.express as px
from collections import Counter
import re

# --- 1. THEME & UI CONFIG ---
st.set_page_config(page_title="PlexTrendz Elite", page_icon="📈", layout="wide")

# Custom CSS for the "Modern SaaS" look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #050508; }
    .main { background: #050508; }
    div[data-testid="stMetricValue"] { font-size: 28px; font-weight: 800; color: #7c6af7; }
    .stButton>button {
        background-color: #7c6af7; color: white; border-radius: 8px;
        width: 100%; border: none; padding: 10px; font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA EXTRACTION ENGINE ---
def fetch_analytics(query, limit):
    try:
        videos = scrapetube.get_search(query, limit=limit)
        data = []
        text_blob = ""
        for i, v in enumerate(videos):
            title = v.get('title', {}).get('runs', [{}])[0].get('text', 'N/A')
            v_id = v.get('videoId')
            views = v.get('viewCountText', {}).get('simpleText', '0 views')
            text_blob += " " + title.lower()
            data.append({
                'Rank': i+1, 
                'Title': title, 
                'Views': views, 
                'Len': len(title), 
                'Link': f"https://youtube.com/watch?v={v_id}"
            })
        return pd.DataFrame(data), text_blob
    except:
        return pd.DataFrame(), ""

# --- 3. HEADER & SIDEBAR ---
st.title("📈 PlexTrendz Elite")
st.caption("Strategic Intelligence for Digital Content Architecture • Developed by Mrinmay Chakraborty")

with st.sidebar:
    st.markdown("### ⚙️ Search Settings")
    topic = st.text_input("Niche Keyword", "Data Science Career")
    count = st.select_slider("Analysis Depth", options=[20, 50, 100], value=50)
    st.divider()
    st.markdown("🚀 **System Status:** No-API Mode Active")

# --- 4. MAIN EXECUTION ---
if st.button("Generate Competitive Intelligence"):
    with st.spinner("Mining YouTube Metadata..."):
        df, raw_text = fetch_analytics(topic, count)
        
        if not df.empty:
            # Metrics Calculation
            avg_l = int(df['Len'].mean())
            words = re.findall(r'\w+', raw_text)
            # Filtering out common 'stop' words
            keywords = [w for w in words if len(w) > 4 and w not in ['video', 'youtube', '2025', '2026', 'about', 'latest']]
            top_k = Counter(keywords).most_common(1)[0][0] if keywords else "N/A"

            # KPI Row
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Target Length", f"{avg_l} Chars")
            m2.metric("Hot Keyword", top_k.upper())
            m3.metric("Sample Size", f"{len(df)} Videos")
            m4.metric("Sentiment", "Dynamic")

            st.markdown("---")

            # Visuals Row
            left, right = st.columns([1.2, 1])

            with left:
                st.markdown("#### 📊 Performance Distribution")
                fig_dist = px.area(df, x="Rank", y="Len", 
                                   title="Character Count Stability",
                                   color_discrete_sequence=['#7c6af7'], template="plotly_dark")
                fig_dist.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_dist, use_container_width=True)

            with right:
                st.markdown("#### 🏷️ Semantic Trends")
                top_10 = pd.DataFrame(Counter(keywords).most_common(8), columns=['Word', 'Count'])
                fig_words = px.bar(top_10, x='Count', y='Word', orientation='h',
                                   color='Count', color_continuous_scale='Purples', template="plotly_dark")
                fig_words.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_words, use_container_width=True)

            # Table Row
            st.markdown("#### 🔍 Competitor Intelligence Table")
            st.dataframe(df[['Rank', 'Title', 'Views', 'Len']], use_container_width=True, hide_index=True)
            
        else:
            st.error("Data retrieval failed. Please check the keyword and try again.")
