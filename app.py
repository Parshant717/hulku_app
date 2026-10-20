import streamlit as st
from google import genai
import os
import time
from dotenv import load_dotenv

# Environment variables load karein
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Nayi Google GenAI Client Configure karein
client = None
if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
    except Exception as e:
        st.error(f"Client initialization error: {e}")
else:
    st.error("⚠️ Security Alert: API Key nahi mili! Secrets check karein.")

# Page Configuration
st.set_page_config(page_title="Hulku - AI Creator Studio", page_icon="⚡", layout="centered")

# CSS file load karna for animations
try:
    with open("static/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

# Session State for Ad Tracking
if 'generation_count' not in st.session_state:
    st.session_state.generation_count = 0

# App Header
st.title("⚡ HULKU - Next-Gen AI Creator Studio")
st.markdown("### *Banao viral captions, memes aur stories ekdum fast aur secure tareeqe se!*")
st.divider()

# Sidebar: Language & Settings
with st.sidebar:
    st.header("⚡ Hulku AI Studio")
    st.success("🟢 Server Online & Secure")
    st.divider()
    
    # 🌐 3 Languages Selection Option
    selected_lang = st.selectbox(
        "🌐 Output Language Chunein:", 
        ["Desi Hinglish", "English", "Pure Hindi"]
    )
    
    st.divider()
    st.info("💡 **Hulku Tip:** Apni pasand ki language select karo aur ek click mein viral content pao!")

# Main Application Logic
user_topic = st.text_input("Aapko kis topic par content chahiye? (Jaise: Startup struggle, Chai lover, Motivation)")
content_type = st.selectbox("Category chunein:", ["Viral Instagram Caption", "Desi Hinglish Shayari", "Startup/Business Meme Idea"])

if st.button("🚀 Generate Content Now"):
    if user_topic.strip() == "":
        st.warning("Pehle koi topic toh likhiye bhai!")
    elif client is None:
        st.error("API client configure nahi hai. Secrets mein GEMINI_API_KEY check karein.")
    else:
        st.session_state.generation_count += 1
        
        with st.spinner(f"✨ Hulku AI {selected_lang} mein magic create kar raha hai..."):
            # Sponsored Ad Display
            st.markdown("""
                <div style='background: rgba(236, 72, 153, 0.1); border: 1px dashed #ec4899; padding: 12px; border-radius: 8px; text-align: center; margin-bottom: 15px;'>
                    <p style='color: #ec4899; font-size: 14px; margin: 0;'>📢 <b>Sponsored Ad:</b> Powered by Hulku Partner Network (Ad Loaded)</p>
                </div>
            """, unsafe_allow_html=True)
            
            prompt = f"Create a catchy, viral, and engaging {content_type} based on this topic: {user_topic}. Write the final output strictly in {selected_lang} language. Use emojis and relevant hashtags."
            
            # 🔁 Retry Logic for gemini-3.8-flash (Handles temporary 503 traffic spikes)
            max_retries = 3
            response_text = None
            last_error = None

            for attempt in range(max_retries):
                try:
                    response = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=prompt,
                    )
                    response_text = response.text
                    break  # Success! Loop se bahar
                except Exception as e:
                    last_error = e
                    if "503" in str(e) or "unavailable" in str(e).lower():
                        time.sleep(2)
                        continue
                    else:
                        break
            
            if response_text:
                st.subheader(f"🎉 Aapka Content ({selected_lang}) Tayar Hai:")
                st.success(response_text)
            else:
                st.error(f"Google server par abhi bohot heavy traffic hai. Kripya 10 seconds baad dobara click karein. Error details: {last_error}")

# Footer
st.markdown("<br><hr><center><p style='color: #94a3b8; font-size: 12px;'>Powered by Hulku Engine © 2026</p></center>", unsafe_allow_html=True)
