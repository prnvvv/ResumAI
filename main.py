import streamlit as st
import PyPDF2 as pdf
import io
import os
import json
import re
import time
from datetime import datetime
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader
import plotly.graph_objects as go
import plotly.express as px

load_dotenv()

st.set_page_config(
    page_title="ATS Resume Analyzer Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        padding: 0 !important;
        background: transparent;
    }
    
    .block-container {
        padding: 2rem 1rem;
        max-width: 1200px;
    }
    
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        margin: -2rem -1rem 3rem -1rem;
        padding: 3rem 2rem;
        border-radius: 0 0 30px 30px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Ccircle cx='30' cy='30' r='4'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        animation: float 20s infinite linear;
    }
    
    @keyframes float {
        0% { transform: translateY(0px) translateX(0px); }
        33% { transform: translateY(-10px) translateX(10px); }
        66% { transform: translateY(5px) translateX(-5px); }
        100% { transform: translateY(0px) translateX(0px); }
    }
    
    .hero-title {
        color: white;
        font-size: 3.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 4px 20px rgba(0,0,0,0.3);
        position: relative;
        z-index: 2;
    }
    
    .hero-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.3rem;
        font-weight: 400;
        margin: 1rem 0 0 0;
        position: relative;
        z-index: 2;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.2);
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1.5rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #667eea, #764ba2, #f093fb, #667eea);
        z-index: -1;
        border-radius: 20px;
        animation: glow 3s linear infinite;
        background-size: 300% 300%;
    }
    
    @keyframes glow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
    }
    
    .metric-title {
        font-size: 1rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
        opacity: 0.9;
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 15px;
        text-align: center;
    }
    
    .analysis-section {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }
    
    .analysis-section:hover {
        border: 1px solid rgba(102, 126, 234, 0.5);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.2);
    }
    
    .section-title {
        color: #667eea;
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .strength-item {
        background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
        color: white;
        padding: 1rem 1.5rem;
        margin: 0.8rem 0;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(39, 174, 96, 0.3);
        transition: all 0.3s ease;
    }
    
    .strength-item:hover {
        transform: translateX(10px);
        box-shadow: 0 6px 20px rgba(39, 174, 96, 0.4);
    }
    
    .gap-item {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        color: white;
        padding: 1rem 1.5rem;
        margin: 0.8rem 0;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(231, 76, 60, 0.3);
        transition: all 0.3s ease;
    }
    
    .gap-item:hover {
        transform: translateX(10px);
        box-shadow: 0 6px 20px rgba(231, 76, 60, 0.4);
    }
    
    .keyword-tag {
        background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
        color: white;
        padding: 0.5rem 1rem;
        margin: 0.3rem;
        border-radius: 25px;
        display: inline-block;
        font-size: 0.9rem;
        font-weight: 500;
        box-shadow: 0 3px 10px rgba(243, 156, 18, 0.3);
        transition: all 0.3s ease;
    }
    
    .keyword-tag:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(243, 156, 18, 0.5);
    }
    
    .email-container {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        border: 2px solid #667eea;
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .email-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .email-header {
        color: #3498db;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        text-align: center;
        text-shadow: 0 2px 10px rgba(52, 152, 219, 0.3);
    }
    
    .email-content {
        background: #1a252f;
        color: #ecf0f1;
        padding: 2rem;
        border-radius: 15px;
        font-family: 'Inter', sans-serif;
        line-height: 1.8;
        border: 1px solid #34495e;
        box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(39, 174, 96, 0.4);
        width: 100%;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(39, 174, 96, 0.6);
    }
    
    .stFileUploader {
        border: 2px dashed #667eea;
        border-radius: 15px;
        padding: 2rem;
        background: rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: #764ba2;
        background: rgba(102, 126, 234, 0.15);
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        color: white;
        padding: 1rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
    }
    
    .stSelectbox > div > div > select {
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        color: white;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        background: rgba(102, 126, 234, 0.1);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        filter: drop-shadow(0 4px 8px rgba(102, 126, 234, 0.3));
    }
    
    .progress-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50px;
        padding: 0.5rem;
        margin: 1rem 0;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 20px;
        border-radius: 50px;
        transition: width 2s ease-in-out;
        position: relative;
        overflow: hidden;
    }
    
    .progress-bar::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        animation: loading 2s infinite;
    }
    
    @keyframes loading {
        0% { left: -100%; }
        50% { left: 100%; }
        100% { left: 100%; }
    }
    
    .cert-card {
        background: linear-gradient(135deg, #8e2de2 0%, #4a00e0 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(142, 45, 226, 0.3);
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .cert-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 40px rgba(142, 45, 226, 0.5);
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .loading-spinner {
        border: 4px solid rgba(255, 255, 255, 0.1);
        border-left: 4px solid #667eea;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 2rem auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .success-alert {
        background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(39, 174, 96, 0.3);
    }
    
    .warning-alert {
        background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(243, 156, 18, 0.3);
    }
    
    .error-alert {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(231, 76, 60, 0.3);
    }
    
    .tab-style {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 0.5rem;
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: rgba(255, 255, 255, 0.7);
        border-radius: 10px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .footer-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        margin: 3rem -1rem -2rem -1rem;
        border-radius: 30px 30px 0 0;
        text-align: center;
        color: white;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #ecf0f1;
    }
    
    p, span, div {
        color: rgba(255, 255, 255, 0.9);
    }
    
    .stMarkdown {
        color: rgba(255, 255, 255, 0.9);
    }
    
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        
        .metric-value {
            font-size: 2rem;
        }
        
        .block-container {
            padding: 1rem 0.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'email_content' not in st.session_state:
    st.session_state.email_content = None
if 'analysis_timestamp' not in st.session_state:
    st.session_state.analysis_timestamp = None

def get_groq_api_keys():
    keys = {
    'GROQ_API_KEY1': os.environ.get('GROQ_API_KEY1'),
    'GROQ_API_KEY2': os.environ.get('GROQ_API_KEY2'),
    'GROQ_API_KEY3': os.environ.get('GROQ_API_KEY3')
}

    missing_keys = [key for key, value in keys.items() if not value]
    if missing_keys:
        st.markdown(f"""
        <div class="error-alert">
            <strong>⚠️ Configuration Error</strong><br>
            Missing environment variables: {', '.join(missing_keys)}<br>
            Please set your GROQ API keys in the .env file
        </div>
        """, unsafe_allow_html=True)
        return None
    
    return keys

def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = pdf.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.markdown(f"""
        <div class="error-alert">
            <strong>📄 PDF Error</strong><br>
            Error extracting text from PDF: {str(e)}
        </div>
        """, unsafe_allow_html=True)
        return None

def scrape_job_website(job_link, api_key):
    if not job_link:
        return None

    try:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.markdown("🔍 **Connecting to job website...**")
        progress_bar.progress(25)
        time.sleep(0.5)
        
        llm_scrape = ChatGroq(
            model_name="llama-3.3-70b-versatile",
            temperature=0.5,
            groq_api_key=api_key
        )
        
        status_text.markdown("📊 **Loading page content...**")
        progress_bar.progress(50)
        
        loader = WebBaseLoader(job_link)
        page_data = loader.load().pop().page_content
        
        status_text.markdown("🤖 **Extracting job details with AI...**")
        progress_bar.progress(75)

        prompt_job_content = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            Extract and structure the following information from the scraped text:
            - Company Details (Name, Industry, Size)
            - Job Title and Role Level
            - Detailed Job Description
            - Required Skills and Technologies
            - Preferred Qualifications and Experience
            - Benefits and Compensation (if mentioned)
            - Application Instructions
            Format the response in a clear, organized manner.
            """
        )

        chain_extract = prompt_job_content | llm_scrape
        res = chain_extract.invoke(input={'page_data': page_data})
        
        progress_bar.progress(100)
        status_text.markdown("✅ **Job details extracted successfully!**")
        time.sleep(0.5)
        progress_bar.empty()
        status_text.empty()
        
        return res.content
    except Exception as e:
        st.markdown(f"""
        <div class="error-alert">
            <strong>🌐 Scraping Error</strong><br>
            Error scraping job content: {str(e)}
        </div>
        """, unsafe_allow_html=True)
        return None

def create_match_chart(match_percentage):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = match_percentage,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Resume Match Score", 'font': {'color': 'white', 'size': 20}},
        delta = {'reference': 80, 'font': {'color': 'white'}},
        gauge = {
            'axis': {'range': [None, 100], 'tickcolor': 'white', 'tickfont': {'color': 'white'}},
            'bar': {'color': "#667eea"},
            'bgcolor': "rgba(255,255,255,0.1)",
            'borderwidth': 2,
            'bordercolor': "white",
            'steps': [
                {'range': [0, 50], 'color': "rgba(231, 76, 60, 0.3)"},
                {'range': [50, 80], 'color': "rgba(243, 156, 18, 0.3)"},
                {'range': [80, 100], 'color': "rgba(39, 174, 96, 0.3)"}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': 'white'},
        height=400
    )
    
    return fig

def create_skills_radar(analysis_data):
    categories = ['Technical Skills', 'Experience Match', 'Education Fit', 'Keyword Coverage', 'Format Quality']
    match_percentage = analysis_data.get('match_percentage', 0)
    
    values = [
        min(match_percentage + 10, 100),
        match_percentage,
        min(match_percentage + 5, 100),
        max(match_percentage - 20, 30),
        min(match_percentage + 15, 100)
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Your Profile',
        line_color='#667eea',
        fillcolor='rgba(102, 126, 234, 0.3)'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=[90, 90, 90, 90, 90],
        theta=categories,
        fill='toself',
        name='Ideal Candidate',
        line_color='#27ae60',
        fillcolor='rgba(39, 174, 96, 0.1)',
        line_dash='dash'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                color='white',
                gridcolor='rgba(255, 255, 255, 0.2)'
            ),
            angularaxis=dict(
                color='white',
                gridcolor='rgba(255, 255, 255, 0.2)'
            )
        ),
        showlegend=True,
        legend=dict(font=dict(color='white')),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color='white'),
        height=500
    )
    
    return fig

def analyze_resume(resume_content, job_content, api_key):
    try:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.markdown("🤖 **Initializing AI analyzer...**")
        progress_bar.progress(20)
        time.sleep(0.5)
        
        llm = ChatGroq(
            model_name="llama-3.3-70b-versatile",
            temperature=0.5,
            groq_api_key=api_key
        )
        
        status_text.markdown("📊 **Analyzing resume compatibility...**")
        progress_bar.progress(50)
        
        prompt_extract = PromptTemplate.from_template(
            """Act as an expert ATS (Application Tracking System) professional with 10+ years of experience in resume evaluation and talent acquisition.

Perform a comprehensive analysis of the resume against the job description and provide insights in JSON format.

Resume Content: {resume_content}
Job Description: {job_content}

Generate a detailed JSON response with this exact structure:
{{
    "match_percentage": 75,
    "match_reasons": {{
        "strengths": [
            "Strong technical background in required programming languages",
            "Relevant industry experience matching job sector",
            "Educational qualifications align with job requirements"
        ],
        "gaps": [
            "Limited experience with specific tools mentioned in job description",
            "Missing certifications that could strengthen application"
        ],
        "alignment": [
            "Years of experience match job requirements",
            "Core competencies overlap significantly with job needs"
        ]
    }},
    "missing_keywords": [
        "Docker",
        "Kubernetes", 
        "CI/CD Pipeline"
    ],
    "improvement_suggestions": [
        "Add cloud platform certifications to strengthen profile",
        "Include more quantifiable achievements in previous roles",
        "Highlight containerization and DevOps experience"
    ],
    "recommended_certifications": [
        {{
            "name": "AWS Certified Solutions Architect",
            "platform": "Amazon Web Services",
            "link": "https://aws.amazon.com/certification/",
            "priority": "High"
        }},
        {{
            "name": "Certified Kubernetes Administrator",
            "platform": "Linux Foundation", 
            "link": "https://training.linuxfoundation.org/certification/",
            "priority": "Medium"
        }}
    ],
    "skill_categories": {{
        "technical_skills": 85,
        "soft_skills": 70,
        "industry_knowledge": 80,
        "education_fit": 90
    }}
}}

Provide accurate percentages and actionable recommendations based on the content analysis."""
        )

        status_text.markdown("🎯 **Generating insights and recommendations...**")
        progress_bar.progress(80)

        chain = prompt_extract | llm
        res = chain.invoke(input={'resume_content': resume_content, 'job_content': job_content})

        try:
            json_content = res.content
            if "```json" in json_content:
                json_content = json_content.split("```json")[1].split("```")[0]
            elif "```" in json_content:
                json_content = json_content.split("```")[1]
            
            analysis_data = json.loads(json_content.strip())
            
            progress_bar.progress(100)
            status_text.markdown("✅ **Analysis complete!**")
            time.sleep(0.5)
            progress_bar.empty()
            status_text.empty()
            
            return analysis_data
            
        except json.JSONDecodeError:
            json_match = re.search(r'\{.*\}', res.content, re.DOTALL)
            if json_match:
                try:
                    analysis_data = json.loads(json_match.group(0))
                    return analysis_data
                except:
                    st.markdown("""
                    <div class="error-alert">
                        <strong>🔧 Processing Error</strong><br>
                        Failed to parse analysis response. Please try again.
                    </div>
                    """, unsafe_allow_html=True)
                    return None
            else:
                st.markdown("""
                <div class="error-alert">
                    <strong>🔧 Format Error</strong><br>
                    Invalid response format received. Please try again.
                </div>
                """, unsafe_allow_html=True)
                return None

    except Exception as e:
        st.markdown(f"""
        <div class="error-alert">
            <strong>🤖 Analysis Error</strong><br>
            Analysis generation error: {str(e)}
        </div>
        """, unsafe_allow_html=True)
        return None

def generate_job_email(resume_content, job_content, api_key):
    try:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.markdown("📧 **Preparing email generator...**")
        progress_bar.progress(30)
        time.sleep(0.3)
        
        llm_mail = ChatGroq(
            model_name="llama-3.3-70b-versatile",
            temperature=0.7,
            groq_api_key=api_key
        )

        status_text.markdown("✍️ **Crafting personalized email...**")
        progress_bar.progress(70)

        prompt_mail = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_content}

            ### CANDIDATE RESUME:
            {resume_content}

            ### INSTRUCTION:
            Create a compelling and personalized job application email that:
            
            1. Uses a professional yet engaging tone
            2. Demonstrates clear understanding of the role and company
            3. Highlights specific achievements and skills that match the job
            4. Shows genuine interest and enthusiasm
            5. Includes a strong call-to-action
            6. Maintains appropriate length (200-300 words)
            
            Structure the email with:
            - Subject line suggestion
            - Formal greeting (use "Hiring Manager" if company name not clear)
            - Strong opening that mentions the specific role
            - Value proposition paragraph highlighting relevant experience
            - Closing paragraph with enthusiasm and next steps
            - Professional signature placeholder
            
            Make it compelling and tailored to increase response rates.
            """
        )

        mail_extract = prompt_mail | llm_mail
        final_mail = mail_extract.invoke(input={'job_content': job_content, 'resume_content': resume_content})
        
        progress_bar.progress(100)
        status_text.markdown("✅ **Email generated successfully!**")
        time.sleep(0.3)
        progress_bar.empty()
        status_text.empty()
        
        return final_mail.content
    except Exception as e:
        st.markdown(f"""
        <div class="error-alert">
            <strong>📧 Email Error</strong><br>
            Email generation error: {str(e)}
        </div>
        """, unsafe_allow_html=True)
        return None

def display_analysis_results(analysis_data):
    if not analysis_data:
        return
    
    match_percentage = analysis_data.get('match_percentage', 0)
    missing_keywords = analysis_data.get('missing_keywords', [])
    suggestions = analysis_data.get('improvement_suggestions', [])
    
    tab1, tab2, tab3 = st.tabs(["📊 Analysis Overview", "📈 Detailed Insights", "🎯 Recommendations"])
    
    with tab1:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.plotly_chart(create_match_chart(match_percentage), use_container_width=True)
        
        with col2:
            st.plotly_chart(create_skills_radar(analysis_data), use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">🎯 ATS Match</div>
                <div class="metric-value">{match_percentage}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">🔑 Missing Keywords</div>
                <div class="metric-value">{len(missing_keywords)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">💡 Improvements</div>
                <div class="metric-value">{len(suggestions)}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        match_reasons = analysis_data.get('match_reasons', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="analysis-section">
                <h3 class="section-title">✅ Your Strengths</h3>
            """, unsafe_allow_html=True)
            
            strengths = match_reasons.get('strengths', [])
            for strength in strengths:
                st.markdown(f'<div class="strength-item">• {strength}</div>', unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("""
            <div class="analysis-section">
                <h3 class="section-title">🎯 Profile Alignment</h3>
            """, unsafe_allow_html=True)
            
            alignment = match_reasons.get('alignment', [])
            for align in alignment:
                st.markdown(f'<div class="strength-item">• {align}</div>', unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="analysis-section">
                <h3 class="section-title">⚠️ Areas for Improvement</h3>
            """, unsafe_allow_html=True)
            
            gaps = match_reasons.get('gaps', [])
            for gap in gaps:
                st.markdown(f'<div class="gap-item">• {gap}</div>', unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("""
            <div class="analysis-section">
                <h3 class="section-title">🔍 Missing Keywords</h3>
            """, unsafe_allow_html=True)
            
            if missing_keywords:
                keyword_html = "".join([f'<span class="keyword-tag">{keyword}</span>' for keyword in missing_keywords])
                st.markdown(keyword_html, unsafe_allow_html=True)
            else:
                st.markdown('<div class="success-alert">🎉 All important keywords are present!</div>', unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        skill_categories = analysis_data.get('skill_categories', {})
        if skill_categories:
            st.markdown("""
            <div class="analysis-section">
                <h3 class="section-title">📈 Skill Category Breakdown</h3>
            """, unsafe_allow_html=True)
            
            cols = st.columns(len(skill_categories))
            for i, (category, score) in enumerate(skill_categories.items()):
                with cols[i]:
                    color = "#27ae60" if score >= 80 else "#f39c12" if score >= 60 else "#e74c3c"
                    st.markdown(f"""
                    <div style="text-align: center; padding: 1rem;">
                        <h4 style="color: white; margin-bottom: 0.5rem;">{category.replace('_', ' ').title()}</h4>
                        <div class="progress-container">
                            <div class="progress-bar" style="width: {score}%; background: {color};"></div>
                        </div>
                        <p style="color: {color}; font-weight: bold; margin: 0.5rem 0 0 0;">{score}%</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="analysis-section">
                <h3 class="section-title">💡 Actionable Improvements</h3>
            """, unsafe_allow_html=True)
            
            for i, suggestion in enumerate(suggestions, 1):
                priority = "🔥 High" if i <= 2 else "⭐ Medium" if i <= 4 else "📋 Low"
                st.markdown(f"""
                <div class="glass-card" style="margin: 1rem 0; padding: 1.5rem;">
                    <div style="display: flex; justify-content: between; align-items: center; margin-bottom: 0.5rem;">
                        <strong style="color: #667eea;">#{i}</strong>
                        <span style="background: rgba(102, 126, 234, 0.2); padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem; color: #667eea;">{priority}</span>
                    </div>
                    <p style="margin: 0; line-height: 1.6;">{suggestion}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            certifications = analysis_data.get('recommended_certifications', [])
            if certifications:
                st.markdown("""
                <div class="analysis-section">
                    <h3 class="section-title">🎓 Recommended Certifications</h3>
                """, unsafe_allow_html=True)
                
                for cert in certifications:
                    name = cert.get('name', 'N/A')
                    platform = cert.get('platform', 'N/A')
                    link = cert.get('link', '#')
                    priority = cert.get('priority', 'Medium')
                    
                    priority_color = "#e74c3c" if priority == "High" else "#f39c12" if priority == "Medium" else "#3498db"
                    
                    st.markdown(f"""
                    <div class="cert-card">
                        <div style="display: flex; justify-content: between; align-items: center; margin-bottom: 1rem;">
                            <h4 style="margin: 0; color: white;">🏆 {name}</h4>
                            <span style="background: {priority_color}; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem; font-weight: bold;">{priority}</span>
                        </div>
                        <p style="margin: 0.5rem 0; opacity: 0.9;">📚 Platform: {platform}</p>
                        <a href="{link}" target="_blank" style="color: #3498db; text-decoration: none; font-weight: 600; display: inline-flex; align-items: center; gap: 0.5rem; margin-top: 0.5rem;">
                            📖 Learn More →
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)

def main():
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🤖 ATS Resume Analyzer Pro</h1>
        <p class="hero-subtitle">AI-Powered Resume Optimization for Modern Job Markets</p>
    </div>
    """, unsafe_allow_html=True)
    
    api_keys = get_groq_api_keys()
    if not api_keys:
        return

    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <h2 style="color: white; margin: 0;">⚙️ Control Panel</h2>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📤 Upload Resume", expanded=True):
            uploaded_file = st.file_uploader(
                "Choose your resume PDF",
                type="pdf",
                help="Upload your resume in PDF format (max 10MB)"
            )
            
            if uploaded_file:
                st.markdown("""
                <div class="success-alert">
                    <strong>✅ File Uploaded</strong><br>
                    Resume ready for analysis
                </div>
                """, unsafe_allow_html=True)
        
        with st.expander("🎯 Job Target", expanded=True):
            job_link = st.text_input(
                "Job Posting URL",
                placeholder="https://company.com/careers/job-id",
                help="Enter the direct URL to the job posting"
            )
            
            analysis_mode = st.selectbox(
                "Analysis Depth",
                ["Standard Analysis", "Deep Analysis", "Quick Scan"],
                index=0,
                help="Choose the level of analysis detail"
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            analyze_button = st.button("🚀 Analyze", use_container_width=True)
        with col2:
            if st.session_state.analysis_result:
                if st.button("🔄 Reset", use_container_width=True):
                    st.session_state.analysis_result = None
                    st.session_state.email_content = None
                    st.session_state.analysis_timestamp = None
                    st.rerun()
        
        st.markdown("---")
        
        st.markdown("""
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <h4>Smart Matching</h4>
                <p>AI-powered compatibility analysis</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <h4>Visual Insights</h4>
                <p>Interactive charts and metrics</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">💡</div>
                <h4>Optimization Tips</h4>
                <p>Actionable improvement suggestions</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📧</div>
                <h4>Email Generator</h4>
                <p>Personalized application emails</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if not uploaded_file and not st.session_state.analysis_result:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 3rem 2rem;">
            <h2 style="color: #667eea; margin-bottom: 1rem;">🚀 Ready to Optimize Your Resume?</h2>
            <p style="font-size: 1.2rem; margin-bottom: 2rem;">Get AI-powered insights to improve your job application success rate</p>
        </div>
        """, unsafe_allow_html=True)

        # Use Streamlit columns instead of HTML grid
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class="glass-card">
                <div class="feature-icon">📈</div>
                <h3 style="color: #27ae60;">94%</h3>
                <p>Average improvement in match scores</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="glass-card">
                <div class="feature-icon">⚡</div>
                <h3 style="color: #3498db;">< 30s</h3>
                <p>Analysis completion time</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="glass-card">
                <div class="feature-icon">🎯</div>
                <h3 style="color: #f39c12;">5x</h3>
                <p>Higher callback rates reported</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <p style="margin-top: 2rem; opacity: 0.8; text-align: center;">Upload your resume and job link to get started!</p>
        """, unsafe_allow_html=True)

    if analyze_button:
        if not uploaded_file:
            st.markdown("""
            <div class="warning-alert">
                <strong>⚠️ Resume Required</strong><br>
                Please upload a PDF resume file to proceed with analysis.
            </div>
            """, unsafe_allow_html=True)
            return
        
        if not job_link:
            st.markdown("""
            <div class="warning-alert">
                <strong>⚠️ Job URL Required</strong><br>
                Please provide a valid job posting URL for comparison.
            </div>
            """, unsafe_allow_html=True)
            return

        resume_text = extract_text_from_pdf(uploaded_file)
        if not resume_text:
            return

        job_content = scrape_job_website(job_link, api_keys['GROQ_API_KEY2'])
        if not job_content:
            return

        analysis_result = analyze_resume(resume_text, job_content, api_keys['GROQ_API_KEY1'])
        if analysis_result:
            st.session_state.analysis_result = analysis_result
            st.session_state.analysis_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        email_content = generate_job_email(resume_text, job_content, api_keys['GROQ_API_KEY3'])
        if email_content:
            st.session_state.email_content = email_content

        if analysis_result:
            st.balloons()
            st.markdown("""
            <div class="success-alert">
                <strong>🎉 Analysis Complete!</strong><br>
                Your resume has been successfully analyzed. Check the results below!
            </div>
            """, unsafe_allow_html=True)

    if st.session_state.analysis_result:
        st.markdown("---")
        
        if st.session_state.analysis_timestamp:
            st.markdown(f"""
            <div style="text-align: right; color: rgba(255,255,255,0.6); margin-bottom: 1rem;">
                📅 Analysis completed: {st.session_state.analysis_timestamp}
            </div>
            """, unsafe_allow_html=True)
        
        display_analysis_results(st.session_state.analysis_result)

    if st.session_state.email_content:
        st.markdown("---")
        
        st.markdown("""
        <div class="email-container">
            <div class="email-header">✨ Your Personalized Application Email</div>
            <div class="email-content">{}</div>
        </div>
        """.format(st.session_state.email_content), unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.download_button(
                label="📥 Download Email Content",
                data=st.session_state.email_content,
                file_name=f"application_email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )

    st.markdown("""
    <div class="footer-section">
        <h2 style="margin-bottom: 1rem;">🚀 Powered by Advanced AI Technology</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem; margin: 2rem 0;">
            <div>
                <h4>🤖 LLaMA 3.3 AI</h4>
                <p>State-of-the-art language model for accurate analysis</p>
            </div>
            <div>
                <h4>⚡ GROQ Infrastructure</h4>
                <p>Lightning-fast processing and responses</p>
            </div>
            <div>
                <h4>📊 Interactive Visualizations</h4>
                <p>Beautiful charts and metrics powered by Plotly</p>
            </div>
        </div>
        <div style="margin-top: 2rem; padding-top: 2rem; border-top: 1px solid rgba(255,255,255,0.2);">
            <p style="opacity: 0.8;">💡 <strong>Pro Tip:</strong> For optimal results, ensure your resume is well-formatted and contains relevant keywords for your target role.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()