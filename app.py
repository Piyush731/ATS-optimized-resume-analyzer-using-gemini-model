from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from streamlit_extras import add_vertical_space as avs
import google.generativeai as genai
import os
import PyPDF2
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PIL import Image 

st.set_page_config(
    page_title="CareerCraft Pro",
    layout="wide",
    page_icon="🚀",
    initial_sidebar_state="collapsed"
)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

:root {
    --primary: #6366f1;
    --secondary: #4f46e5;
    --accent: #818cf8;
    --background: #f8fafc;
}

* {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

.header-gradient {
    background: linear-gradient(45deg, var(--primary), var(--secondary)) !important;
    color: white !important;
    padding: 2rem;
    border-radius: 15px;
    box-shadow: 0 10px 20px rgba(99, 102, 241, 0.2);
    transition: transform 0.3s ease;
}

.header-gradient:hover {
    transform: translateY(-5px);
}

.feature-card {
    background: white;
    padding: 2rem;
    border-radius: 15px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    margin: 1rem 0;
}

.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 15px rgba(0, 0, 0, 0.15);
}

.animated-border {
    position: relative;
    overflow: hidden;
    border-radius: 15px;
}

.animated-border::after {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, transparent, rgba(99, 102, 241, 0.2), transparent);
    animation: rotate 4s linear infinite;
}

@keyframes rotate {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.cta-button {
    background: linear-gradient(45deg, var(--primary), var(--secondary)) !important;
    color: white !important;
    border: none !important;
    padding: 0.8rem 2rem !important;
    border-radius: 8px !important;
    transition: transform 0.3s ease !important;
}

.cta-button:hover {
    transform: scale(1.05) !important;
    box-shadow: 0 5px 15px rgba(99, 102, 241, 0.3) !important;
}

.result-card {
    background: white;
    padding: 2rem;
    border-radius: 15px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    animation: slideUp 0.5s ease;
}

@keyframes slideUp {
    from { transform: translateY(20px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

.faq-item {
    background: var(--glass);
    padding: 2rem;
    border-radius: 20px;
    margin: 1.5rem 0;
    cursor: pointer;
    transition: all 0.4s ease;
    position: relative;
    overflow: hidden;
    border-left: 5px solid transparent;
}

.faq-item:hover {
    transform: translateX(15px);
    border-left-color: var(--primary);
    box-shadow: 0 10px 25px rgba(99, 102, 241, 0.1);
}

.faq-item::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(45deg, transparent, rgba(99, 102, 241, 0.05), transparent);
    z-index: -1;
}

/* Contact Form Styling */
.contact-form {
    background: var(--glass);
    backdrop-filter: blur(10px);
    padding: 3rem;
    border-radius: 25px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.05);
    position: relative;
    overflow: hidden;
}

.contact-form::after {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, transparent, rgba(99, 102, 241, 0.1), transparent);
    animation: rotate 20s linear infinite;
    z-index: -1;
}

</style>
""", unsafe_allow_html=True)


EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')  
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.0-flash")


def get_gemini_response(input_text):
    response = model.generate_content(input_text)
    return response.text

def input_pdf_text(uploaded_file):
    reader=PyPDF2.PdfReader(uploaded_file)
    text=''
    for page_num in range(len(reader.pages)):
        page=reader.pages[page_num]
        text+= str(page.extract_text()) 
    return text    
input_prompt="""
 As a expierienced ATS (Applicant Tracking System), proficient in the technical domain encompassing Software Engineering, Data Science,
 Data Analysis, Big Data Engineering, Web Developer, Mobile App Developer, Dev Ops Engineer, Machine Learning Engineer, Cybersecurity 
 Analyst, Cloud Solutions Architect, Database Administrator, Network Engineer, AI Engineer, Systems Analyst, Full Stack Developer, UI/UX 
 Designer, IT Project Manager, and additional specialized areas, your objective is to meticulously assess  resumes against provided job 
 description. In a fiercely competitive job market, your expertise is crucial in  offering not notch guidance for resume enhancement.  
 Assign precise matching percentages based on the JD(Job Description) and meticulously identify any missing keywords with utmost accuracy.
 resume:{text}
 description:{jd} 

 I want the response in the following structure:
 the first line indicates the percentage match with the job description(JD).
 The second line presents a list of missing keywords.
 The third section provides a profile summary.

 Mention the title for all the three sections.
 While generating the response put some space to seprate all the three section.
 """ 

avs.add_vertical_space(4) 

col1, col2 = st.columns([3,2]) 
with col1: 
    st.markdown("""
    <div class="header-gradient">
        <h1 style="margin: 0;">CareerCraft</h1>
        <h3 style="margin: 0; font-weight: 400;">Navigate the Job Market with Confidence!</h3>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""<p style='text-align: justify; font-size: 1.1rem; line-height: 1.6;'>
    Introducing CareerCraft, an ATS-Optimized Resume Analyzer - your ultimate solution for optimizing 
    job applications and accelerating career growth. Our innovative platform leverages advanced ATS 
    technology to provide job seekers with valuable insights into their resume compatibility with 
    job descriptions.
    </p>""", unsafe_allow_html=True)

with col2: 
         st.image('https://cdn.dribbble.com/userupload/12500996/file/original-b458fe398a6d7f4e9999ce66ec856ff9.gif', use_column_width=True) 

avs.add_vertical_space(6) 
col1, col2 = st.columns([2,3]) 
with col2: 
    st.markdown("""
    <div class="feature-card">
        <h3><i class="fas fa-rocket"></i> Wide Range of Offerings</h3>
        <div class="features-grid" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">
            <div><i class="fas fa-check-circle"></i> ATS Resume Analysis</div>
            <div><i class="fas fa-check-circle"></i> Resume Optimization</div>
            <div><i class="fas fa-check-circle"></i> Skill Enhancement</div>
            <div><i class="fas fa-check-circle"></i> Career Guidance</div>
            <div><i class="fas fa-check-circle"></i> Profile Summaries</div>
            <div><i class="fas fa-check-circle"></i> Application Tracking</div>
        </div>
    </div>
    """, unsafe_allow_html=True) 

with col1: 
    img1 = Image.open("images/icon1.jpg")
    st.image(img1, use_column_width=True)


avs.add_vertical_space(5) 

col1, col2 =st.columns([3,2]) 
with col1:
    with st.form("analysis_form"):
        st.markdown("""
        <div class="animated-border">
            <div style="padding: 2rem; background: white; border-radius: 15px;">
                <h2 style="text-align: center; margin-bottom: 2rem;"><i class="fas fa-paper-plane"></i> Embark on Your Career Adventure</h2>
        """, unsafe_allow_html=True)
        
        jd = st.text_area("Paste Job Description", height=150)
        uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
        submit = st.form_submit_button("Analyze Resume", use_container_width=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)

# Results Handling
if submit:
    if uploaded_file and jd:
        with st.spinner("Analyzing your resume..."):
            try:
                text = input_pdf_text(uploaded_file)
                final_prompt = input_prompt.format(text=text, jd=jd)
                response = get_gemini_response(final_prompt)
                
                st.markdown(f"""
                <div class="result-card">
                    <h3><i class="fas fa-chart-line"></i> Analysis Results</h3>
                    <div style="margin-top: 1.5rem; white-space: pre-wrap">{response}</div>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
    else:
        st.warning("Please upload a resume and provide a job description")

with col2: 
    img2 = Image.open("images/icon2.jpg")
    st.image(img2, use_column_width=True) 
avs.add_vertical_space(10)

#faq 
st.markdown("""
    <div class="feature-card">
        <h2><i class="fas fa-question-circle"></i> Expert Insights</h2>
        <div class="faq-item">
            <h4>🤖 How does our AI analysis work?</h4>
            <p>Our system employs multi-layer neural networks trained on 50M+ successful resumes...</p>
        </div>
        <div class="faq-item">
            <h4>🎯 Industry-Specific Optimization</h4>
            <p>Custom algorithms for 15+ industries including Tech, Healthcare, and Finance...</p>
        </div>
        <div class="faq-item">
            <h4>📊 Competitive Benchmarking</h4>
            <p>Compare your profile against top performers in your target roles...</p>
        </div>
        <div class="faq-item">
            <h4>🛠️ Continuous Improvement</h4>
            <p>Real-time updates based on changing market trends and ATS algorithms...</p>
        </div>
    </div>
    """, unsafe_allow_html=True) 


avs.add_vertical_space(5) 



# contact us by smtp
with st.container():
    st.markdown("""
    <div class="contact-form">
        <h2 style="color: var(--primary); margin-bottom: 2rem;">
            <i class="fas fa-comments"></i> Connect With Career Experts
        </h2>
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 2rem;">
            <div>
                <h4>📬 Contact Form</h4>
    """, unsafe_allow_html=True)
    
    # Contact Form Elements
    contact_email = st.text_input("Your Professional Email", key="contact_email", 
                                placeholder="name@professional.com")
    message = st.text_area("Your Message", key="contact_message", 
                         height=150,
                         placeholder="Share your questions or feedback...")
    
    if st.button("Send Message", key="contact_submit", type="primary"):
        if contact_email and message:
            try:
                msg = MIMEMultipart()
                msg['From'] = EMAIL_ADDRESS
                msg['To'] = 'piyushkashyap3247@gmail.com'
                msg['Subject'] = "New Contact Message - CareerCraft Pro"
                
                body = f"""
                From: {contact_email}
                Message:
                {message}
                """
                msg.attach(MIMEText(body, 'plain'))
                
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    server.send_message(msg)
                
                st.success("🎉 Message sent successfully! We'll respond within 24 hours.")
            except Exception as e:
                st.error(f"❌ Error sending message: {str(e)}")
        else:
            st.warning("⚠️ Please provide both your email and message")
    
    st.markdown("""
            </div>
            <div>
                <h4>📞 Direct Support</h4>
                <p style="margin: 1rem 0;"><i class="fas fa-clock"></i> 24/7 Career Support Team</p>
                <p style="margin: 1rem 0;"><i class="fas fa-envelope"></i> Email: support@careercraft.com</p>
                <p style="margin: 1rem 0;"><i class="fas fa-phone"></i> Phone: +91 7310703247</p>
                <div style="margin-top: 2rem;">
                    <h4>🔗 Follow Us</h4>
                    <div style="display: flex; gap: 1.5rem; font-size: 1.8rem; margin-top: 1rem;">
                        <a href="#" style="color: var(--primary);"><i class="fab fa-linkedin"></i></a>
                        <a href="#" style="color: var(--primary);"><i class="fab fa-twitter"></i></a>
                        <a href="#" style="color: var(--primary);"><i class="fab fa-github"></i></a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)



st.markdown("""---""", unsafe_allow_html=True)
avs.add_vertical_space(5)
st.markdown("""
<div style="text-align: center; padding: 3rem; background: var(--glass); border-radius: 25px;">
    <div style="display: flex; justify-content: center; gap: 2rem; margin-bottom: 1.5rem;">
        <a href="#" style="color: var(--text);">Privacy Policy</a>
        <a href="#" style="color: var(--text);">Terms of Service</a>
        <a href="#" style="color: var(--text);">Careers</a>
    </div>
    <p style="color: var(--text);">© 2024 CareerCraft Pro. All rights reserved.<br>
    Empowering 1M+ professionals worldwide</p>
</div>
""", unsafe_allow_html=True)