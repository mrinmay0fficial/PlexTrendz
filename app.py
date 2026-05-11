import streamlit as st
import scrapetube
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import re

# --- 1. THEME & UI CONFIG ---
st.set_page_config(page_title="PlexTrendz Elite", page_icon="📈", layout="wide")

# Injecting Custom CSS for a clean, professional aesthetic
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #050508;
    }
    .main { background: #050508; }
    div[data-testid="stMetricValue"] { font-size: 28px; font-weight: 800; color: #7c6af7; }
    .stButton>button {
        background-color: #7c6af7; color: white; border-radius: 8px;
        width: 100%; border: none; padding: 10px; font-weight: 600;
    }
    .card {
        background: #111119; border: 1px solid #1e1e2d;
        padding: 20px; border-radius: 12px; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIC ---
def fetch_analytics(query, limit):
    videos = scrapetube.get_search(query, limit=limit)
    data = []
    text_blob = ""
    for i, v in enumerate(videos):
        title = v.get('title', {}).get('runs', [{}])[0].get('text', 'N/A')
        v_id = v.get('videoId')
        views = v.get('viewCountText', {}).get('simpleText', '0 views')
        text_blob += " " + title.lower()
        data.append({'Rank': i+1, 'Title': title, 'Views': views, 'Len': len(title), 'Link': f"https://youtube.com/watch?v={v_id}"})
    return pd.DataFrame(data), text_blob

# --- 3. HEADER ---
st.title("📈 PlexTrendz Elite")
st.caption("Strategic Intelligence for Digital Content Architecture")

with st.sidebar:
    st.markdown("### ⚙️ Analysis Settings")
    topic = st.text_input("Search Niche", "Data Science Career")
    count = st.select_slider("Depth of Scan", options=[20, 50, 100], value=50)
    st.divider()
    st.markdown("🚀 *PlexTrendz uses No-API scraping for unlimited niche exploration.*")

# --- 4. EXECUTION ---
if st.button("Generate Competitive Intelligence"):
    with st.spinner("Processing metadata..."):
        df, raw_text = fetch_analytics(topic, count)
        
        if not df.empty:
            # --- METRICS ROW ---
            m1, m2, m3, m4 = st.columns(4)
            avg_l = int(df['Len'].mean())
            
            # Simple keyword extraction
            words = re.findall(r'\w+', raw_text)
            keywords = [w for w in words if len(w) > 4 and w not in ['video', 'youtube', '2025', '2026', 'about']]
            top_k = Counter(keywords).most_common(1)[0][0]

            m1.metric("Target Length", f"{avg_l} Chars")
            m2.metric("Niche Keyword", top_k.upper())
            m3.metric("Sample Size", f"{len(df)} Videos")
            m4.metric("Market Status", "Saturated" if count > 40 else "Growing")

            st.markdown("---")

            # --- STEP 1: Drawing the Performance Graph ---
st.markdown("#### 📊 Title Performance Trend")

# This creates a smooth "Area" graph
# x="Rank" (1st place, 2nd place, etc.)
# y="Len" (How long the title is)
fig_performance = px.area(df, x="Rank", y="Len", 
                         title="How Title Length Changes with Rank",
                         template="plotly_dark", 
                         color_discrete_sequence=['#7c6af7']) # Your brand purple

# This line makes the background transparent so it looks "Elite"
fig_performance.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')

# Show the graph
st.plotly_chart(fig_performance, use_container_width=True)


# --- STEP 2: Drawing the Keyword Graph ---
st.markdown("#### 🏷️ Trending Keywords")

# This takes the top words we found and makes a Bar Chart
# orientation='h' makes it horizontal (easier to read)
fig_keywords = px.bar(word_df, x='Count', y='Word', orientation='h',
                      color='Count', color_continuous_scale='Purples', 
                      template="plotly_dark")

fig_keywords.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')

# Show the graph
st.plotly_chart(fig_keywords, use_container_width=True)

            # --- DATA TABLE ---
            st.markdown("#### 🔍 Competitor Breakdown")
            st.dataframe(df[['Rank', 'Title', 'Views', 'Len']], use_container_width=True, hide_index=True)
            
        else:
            st.error("Connection failed. Check your niche keyword and try again.")
