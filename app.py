import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

# 🔥 EPIC CUSTOM UI SETUP
st.set_page_config(page_title="WhatsApp Analyzer Pro", layout="wide", page_icon="📱")
plt.style.use('dark_background')

# CUSTOM CSS
st.markdown("""
<style>
    .main {background: linear-gradient(135deg, #0C0E1A 0%, #1A1D2E 100%);}
    .stApp {background: linear-gradient(135deg, #0C0E1A 0%, #1A1D2E 100%);}
    .sidebar .sidebar-content {background: linear-gradient(135deg, #16213E 0%, #0F3460 100%);}
    .metric-card {background: linear-gradient(45deg, #FF6B6B, #4ECDC4); 
                  padding: 1.5rem; border-radius: 20px; margin: 0.5rem 0; box-shadow: 0 10px 30px rgba(0,0,0,0.3);}
    h1 {color: #00D4AA; font-size: 3rem; font-weight: 800;}
    .stButton > button {background: linear-gradient(45deg, #667eea 0%, #764ba2 100%); 
                        color: white; border-radius: 25px; border: none; padding: 0.8rem 2rem; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("# 📱 **WhatsApp Chat Analyzer Pro**")
st.markdown("*Advanced Analytics • Beautiful Visuals • Deep Insights* ✨")

# SIDEBAR
with st.sidebar:
    st.markdown("### 📤 **Upload Chat**")
    uploaded_file = st.file_uploader("Choose WhatsApp TXT", type="txt")
    
    if uploaded_file:
        st.success("✅ File uploaded!")
        st.markdown("### 👤 **Select User**")

# MAIN CONTENT
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8", errors='ignore')
    
    try:
        df = preprocessor.preprocess(data)

        # Safe user list
        user_list = df['user'].unique().tolist()
        if 'group_notification' in user_list:
            user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0,"Overall")

        selected_user = st.sidebar.selectbox("🎯 Analyze", user_list)

        if st.sidebar.button("🚀 **GENERATE INSIGHTS**", use_container_width=True):

            # 🌟 STATS CARDS
            stats = helper.fetch_stats(selected_user, df)
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>💬 Messages</h3>
                    <h1 style='color:white'>{stats[0]:,}</h1>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>📝 Words</h3>
                    <h1 style='color:white'>{stats[1]:,}</h1>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🖼️ Media</h3>
                    <h1 style='color:white'>{stats[2]}</h1>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🔗 Links</h3>
                    <h1 style='color:white'>{stats[3]}</h1>
                </div>
                """, unsafe_allow_html=True)

            # TIMELINE CHARTS
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📅 Monthly Timeline")
                timeline = helper.monthly_timeline(selected_user, df)
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.plot(timeline['time'], timeline['message'], color='#00D4AA', linewidth=3)
                plt.xticks(rotation=45)
                st.pyplot(fig)

            with col2:
                st.subheader("🗓️ Daily Timeline")
                daily_timeline = helper.daily_timeline(selected_user, df)
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='#FF6B6B', linewidth=3)
                plt.xticks(rotation=45)
                st.pyplot(fig)

            # ACTIVITY CHARTS
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("🔥 Busiest Day")
                busy_day = helper.week_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_day.index, busy_day.values, color='purple')
                plt.xticks(rotation=45)
                st.pyplot(fig)

            with col2:
                st.subheader("📅 Busiest Month")
                busy_month = helper.month_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values, color='orange')
                plt.xticks(rotation=45)
                st.pyplot(fig)

            # HEATMAP
            st.subheader("⏰ Weekly Activity Heatmap")
            user_heatmap = helper.activity_heatmap(selected_user, df)
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.heatmap(user_heatmap, annot=True, fmt='d', cmap='YlOrRd')
            st.pyplot(fig)

            # BUSY USERS
            if selected_user == 'Overall':
                st.subheader("🏆 Most Active Users")
                x, new_df = helper.most_busy_users(df)
                col1, col2 = st.columns(2)
                with col1:
                    fig, ax = plt.subplots()
                    ax.bar(x.index, x.values, color='red')
                    plt.xticks(rotation=45)
                    st.pyplot(fig)
                with col2:
                    st.dataframe(new_df)

            # WORDCLOUD
            st.subheader("🌈 Word Cloud")
            df_wc = helper.create_wordcloud(selected_user, df)
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.imshow(df_wc)
            ax.axis('off')
            st.pyplot(fig)

            # MOST COMMON WORDS
            st.subheader("🔝 Most Common Words")
            most_common_df = helper.most_common_words(selected_user, df)
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.barh(most_common_df[0], most_common_df[1])
            st.pyplot(fig)

            # EMOJI ANALYSIS
            st.subheader("🎭 Emoji Analysis")
            emoji_df = helper.emoji_helper(selected_user, df)
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(emoji_df.head(10))
            with col2:
                fig, ax = plt.subplots()
                ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.1f")
                st.pyplot(fig)

            # DOWNLOAD
            csv = df.to_csv(index=False)
            st.download_button("💾 Download Analysis", csv, "chat_analysis.csv", "text/csv")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("💡 Upload a proper WhatsApp chat export (.txt)")

else:
    st.info("👆 **Upload a WhatsApp chat file to get started!**")
    st.markdown("""
    ### 📋 **How to export:**
    1. Open WhatsApp → Group Chat
    2. Tap group name → **Export Chat**
    3. Select **Without Media** → Save TXT file
    4. Upload here! 🚀
    """)
