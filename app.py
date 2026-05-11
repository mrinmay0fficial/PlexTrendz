elif nav == "🔬 Content Strategy Lab":
        st.header("🔬 Niche Strategy & SEO Lab")
        st.caption(f"Advanced strategic breakdown for: {topic.upper()}")
        
        col1, col2 = st.columns([1.2, 1])
        
        with col1:
            st.subheader("🏷️ Semantic Dominance")
            fig_bar = px.bar(counts, x='Freq', y='Word', orientation='h', color='Freq', 
                            color_continuous_scale='Purples', template="plotly_dark")
            fig_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_bar, use_container_width=True)
            
        with col2:
            st.subheader("🎯 Content Game Plan")
            
            # 1. SEO KEYWORD STRATEGY
            st.success(f"**Primary Keyword:** Use **'{top_k}'** early in your title. It appears in {int((counts.iloc[0]['Freq']/len(df))*100)}% of top-ranking videos.")
            
            # 2. TITLE LENGTH OPTIMIZATION
            st.warning(f"**The 'Sweet Spot':** Aim for **{avg_l-5} to {avg_l+5} characters**. This is the mathematical average of current winners.")
            
            # 3. HOOK ANALYSIS (Calculated Logic)
            question_titles = df[df['Title'].str.contains('\?|How|Why|What', case=False)].shape[0]
            hook_type = "Inquisitive (Questions)" if question_titles > (len(df)*0.3) else "Declarative (Statement)"
            st.info(f"**Suggested Hook Style:** **{hook_type}**. The data shows this style dominates the 'Niche Vibe'.")
            
            # 4. COMPETITIVE DIFFICULTY (Calculated Logic)
            # If the average title length is very long, it usually means the niche is highly descriptive/technical.
            diff_score = "Hard" if avg_l > 70 else "Moderate"
            st.error(f"**Ranking Difficulty:** **{diff_score}**. High metadata precision is required to outrank current competitors.")

            # 5. BONUS CREATOR TIP
            with st.expander("💡 Pro Secret for this Niche"):
                st.write(f"""
                Based on the analysis of **{len(df)} videos**, the most successful creators in the **{topic}** space 
                are currently prioritizing **specific technical terms** over broad clickbait. 
                Double-down on the keyword **'{top_k.lower()}'** in your description and tags as well.
                """)
