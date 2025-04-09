import streamlit as st
from pdf_parser import parse_resume
from career_advisor import CareerAdvisor
from web_scraper import get_trends
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Electronics Career Guide", layout="wide")
advisor = CareerAdvisor()

# Sidebar Navigation
input_method = st.sidebar.radio("Navigation", ["📝 Resume Analysis", "❓ Career Questions"])

if input_method == "📝 Resume Analysis":
    st.header("🔧 Electronics Career Optimizer")
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=['pdf'])
    
    if uploaded_file:
        profile = parse_resume(uploaded_file)
        
        if 'error' in profile:
            st.error(f"Error: {profile['error']}")
        else:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Technical Skills Analysis
                if profile['technical_skills'][0] != "No technical skills found":
                    st.success("✅ Technical Skills Detected:")
                    st.write(", ".join(profile['technical_skills']))
                else:
                    st.warning("⚠️ No Technical Skills Found")
                    with st.expander("🔍 How to Improve"):
                        st.write("""
                        **Add these keywords to your resume:**
                        - Embedded Systems
                        - PCB Design
                        - MATLAB
                        - Circuit Analysis
                        - Any electronics tools you've used
                        """)
                        st.write("**Example:** 'Designed PCB layouts using Altium Designer'")
                
                # Transferable Skills
                if profile['transferable_skills'][0] != "No transferable skills found":
                    st.info("🌟 Transferable Skills:")
                    st.write(", ".join(profile['transferable_skills']))
                
                # AI Analysis
                with st.spinner("🤖 Generating career insights..."):
                    analysis = advisor.get_analysis(profile, is_resume=True)
                    st.subheader("📈 Career Recommendations")
                    st.write(analysis)
            
            with col2:
                st.subheader("📌 Quick Tips")
                st.write(get_trends())
                st.divider()
                if profile['missing_keywords']:
                    st.write("🔑 **Top Missing Keywords:**")
                    st.write(", ".join(profile['missing_keywords'][:5]))

elif input_method == "❓ Career Questions":
    st.header("💬 Electronics Career Q&A")
    question = st.text_area("Ask your career question:", height=150,
                          placeholder="What skills do I need for embedded systems roles?")
    
    if st.button("Get Expert Answer"):
        if question.strip():
            with st.spinner("🔍 Analyzing..."):
                response = advisor.get_analysis(question)
                st.subheader("📝 Expert Advice")
                st.write(response)
                
                st.divider()
                st.subheader("📌 Industry Context")
                st.info(get_trends())
        else:
            st.warning("Please enter a question")
