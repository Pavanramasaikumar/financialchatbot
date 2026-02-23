import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Personal Finance Chatbot", page_icon="💰", layout="wide")

# Simple Google-style authentication
def google_style_auth():
    """Simple authentication with Google-style interface"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        # Login page with Google-style design
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 2rem;">
                <h1 style="color: #4285F4; margin-bottom: 0.5rem;">💰</h1>
                <h2 style="color: #202124; margin-bottom: 0.5rem;">Personal Finance Chatbot</h2>
                <p style="color: #5f6368; margin-bottom: 2rem;">Sign in to continue</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Login form
            with st.form("login_form"):
                email = st.text_input("📧 Email", placeholder="name@gmail.com")
                password = st.password_input("🔑 Password", placeholder="Enter your password")
                submit = st.form_submit_button("🔐 Sign in with Google", use_container_width=True)
                
                if submit:
                    # Simple validation - accept any Google email
                    if email and "@" in email and password:
                        st.session_state.authenticated = True
                        st.session_state.user_email = email
                        st.success("✅ Login successful! Redirecting...")
                        st.rerun()
                    else:
                        st.error("❌ Please enter a valid email and password")
            
            st.markdown("<hr style='margin: 2rem 0;'>", unsafe_allow_html=True)
            
            # Quick demo access
            if st.button("👤 Quick Demo Access (No Credentials Needed)", use_container_width=True):
                st.session_state.authenticated = True
                st.session_state.user_email = "demo.user@gmail.com"
                st.success("✅ Demo access granted! Redirecting...")
                st.rerun()
            
            # Info section
            with st.expander("ℹ️ About this app"):
                st.markdown("""
                **Personal Finance Chatbot** helps you with:
                - 💰 Budgeting advice
                - 📈 Investment guidance  
                - 💳 Credit management
                - 🎓 Student finance tips
                - 💼 Professional financial planning
                
                **Powered by:** Groq AI & Streamlit
                """)
        
        st.stop()
    else:
        # Show user info in sidebar
        with st.sidebar:
            st.divider()
            user_email = st.session_state.get("user_email", "User")
            st.markdown(f"**👤 Signed in as:**")
            st.info(user_email)
            
            if st.button("🚪 Sign out", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.user_email = None
                st.success("Signed out successfully!")
                st.rerun()

# Initialize and check authentication
google_style_auth()

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    text-align: center;
    color: #2E8B57;
    font-size: 2.5rem;
    margin-bottom: 1rem;
}
.demographic-badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 1rem;
    font-size: 0.8rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}
.student-badge {
    background-color: #E3F2FD;
    color: #1976D2;
}
.professional-badge {
    background-color: #E8F5E8;
    color: #388E3C;
}
.chat-message {
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.user-message {
    background-color: #F0F8FF;
    border-left: 4px solid #4682B4;
    color: #2C3E50;
}
.bot-message {
    background-color: #F5F5F5;
    border-left: 4px solid #32CD32;
    color: #2E8B57;
    font-weight: 500;
}
.response-text {
    color: #2C3E50 !important;
    line-height: 1.6;
    font-size: 1rem;
}
.bot-name {
    color: #2E8B57 !important;
    font-weight: bold;
}
.user-name {
    color: #1976D2 !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">💰 Personal Finance Chatbot</h1>', unsafe_allow_html=True)
st.markdown(f'<p style="text-align: center; color: #666;">Welcome, {st.session_state.get("user_email", "User")}!</p>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
Get personalized financial advice tailored to your life stage and goals!<br>
<small>Powered by Groq AI and Hugging Face</small>
</div>
""", unsafe_allow_html=True)

# Initialize API clients
@st.cache_resource
def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if api_key and len(api_key) > 10:
        try:
            return Groq(api_key=api_key)
        except Exception as e:
            st.error(f"Error initializing Groq client: {str(e)}")
            return None
    return None

def get_student_financial_advice(question, groq_client):
    """Generate student-specific financial advice"""
    student_context = """You are a friendly financial advisor specifically helping college students and young adults. 
    
    Your advice should be:
    - Simple and easy to understand
    - Focused on small amounts and practical tips
    - Encouraging about building good habits early
    - Realistic about limited income situations
    - Include specific examples with small dollar amounts ($5, $20, $100)
    
    Topics to emphasize:
    - Basic budgeting with apps like Mint or YNAB
    - Building emergency fund starting with $500-$1000
    - Student loan management and repayment options
    - Part-time work and side hustles
    - Credit building with student credit cards
    - Textbook savings and student discounts
    - Simple saving challenges (52-week challenge, etc.)
    - Free financial resources and tools
    
    Keep responses conversational, supportive, and actionable."""
    
    try:
        if groq_client:
            response = groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": student_context},
                    {"role": "user", "content": question}
                ],
                model="llama-3.1-8b-instant",
                temperature=0.7,
                max_tokens=400
            )
            return response.choices[0].message.content
        else:
            return get_fallback_student_advice(question)
    except Exception as e:
        st.error(f"Groq API Error: {str(e)}")
        return get_fallback_student_advice(question)

def get_professional_financial_advice(question, groq_client):
    """Generate professional-specific financial advice"""
    professional_context = """You are a sophisticated financial advisor working with established professionals and career-focused individuals.
    
    Your advice should be:
    - Detailed and comprehensive
    - Include specific financial products and strategies
    - Use professional financial terminology appropriately
    - Focus on wealth building and optimization
    - Provide multiple options and considerations
    - Include tax implications and benefits
    
    Topics to emphasize:
    - 401(k) optimization and employer matching
    - IRA vs Roth IRA strategies
    - Investment portfolio diversification
    - Tax-loss harvesting and tax-efficient investing
    - Real estate investment considerations
    - Estate planning basics
    - Insurance optimization (term life, disability, umbrella)
    - Advanced budgeting and cash flow management
    - Side business and additional income streams
    - Retirement planning and FIRE strategies
    
    Provide actionable advice with specific numbers, percentages, and timeframes where appropriate."""
    
    try:
        if groq_client:
            response = groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": professional_context},
                    {"role": "user", "content": question}
                ],
                model="llama-3.1-8b-instant",
                temperature=0.6,
                max_tokens=600
            )
            return response.choices[0].message.content
        else:
            return get_fallback_professional_advice(question)
    except Exception as e:
        st.error(f"Groq API Error: {str(e)}")
        return get_fallback_professional_advice(question)

def get_fallback_student_advice(question):
    """Fallback advice for students when APIs are unavailable"""
    advice_map = {
        "budget": "🎯 **Start Simple!** Try the 50/30/20 rule: 50% needs (food, rent), 30% wants (entertainment), 20% savings. Use apps like Mint or even a simple notebook. Start with tracking expenses for one week to see where your money goes!",
        "save": "💰 **Begin Small!** Start with a $500 emergency fund - even $5/week adds up! Try the 'pay yourself first' method: set aside money for savings before spending on anything else. Look for student discounts everywhere and consider a high-yield savings account.",
        "invest": "📈 **Time is Your Advantage!** Start small with apps like Acorns or Stash that round up purchases. Consider a Roth IRA - you can contribute up to $6,500/year. Index funds are great for beginners. Even $25/month can grow significantly over time!",
        "credit": "💳 **Build Responsibly!** Get a student credit card, but use it responsibly! Pay it off in full each month. Keep utilization under 30%. Consider becoming an authorized user on a parent's card with good history.",
        "loan": "🎓 **Know Your Loans!** Understand your student loans! Know if they're federal or private, interest rates, and repayment options. Consider income-driven repayment plans after graduation. Pay interest while in school if possible.",
        "job": "💼 **Every Dollar Counts!** Look for campus jobs, tutoring opportunities, or freelance work. Even 10 hours/week can provide $400-800/month. Consider work-study programs that align with your studies."
    }
    
    question_lower = question.lower()
    for key, advice in advice_map.items():
        if key in question_lower:
            return advice
    
    return "💡 **Great Question!** As a student, focus on building good financial habits early. Start with a simple budget, build an emergency fund ($500-$1000), and learn about investing basics. Every small step counts toward your financial future!"

def get_fallback_professional_advice(question):
    """Fallback advice for professionals when APIs are unavailable"""
    advice_map = {
        "invest": "📊 **Portfolio Strategy:** Consider a diversified portfolio with 80-90% in low-cost index funds (VTI, VTIAX) and 10-20% in bonds (BND). Maximize your 401(k) employer match first, then Roth IRA ($6,500 annually), then back to 401(k). Dollar-cost averaging reduces timing risk.",
        "tax": "💼 **Tax Optimization:** Max out 401(k) ($22,500 + $7,500 catch-up if 50+), HSA if available ($3,850 individual), consider tax-loss harvesting in taxable accounts. Hold index funds in taxable accounts, bonds in tax-advantaged accounts.",
        "retire": "🏖️ **Retirement Planning:** Follow the 4% rule for retirement planning. Aim to save 10-15% of income. Calculate your FI number (25x annual expenses). Consider both traditional and Roth accounts for tax diversification. Review asset allocation annually.",
        "budget": "📋 **Advanced Budgeting:** Use zero-based budgeting or 50/30/20 rule scaled up. Track net worth monthly. Automate investments and bill payments. Maintain 3-6 months emergency fund in high-yield savings. Consider liability umbrella insurance.",
        "real estate": "🏠 **Real Estate Strategy:** Real estate can be 20-30% of portfolio. Consider REITs for easy diversification. For rental properties, follow 1% rule (monthly rent ≥ 1% of purchase price). Factor in maintenance, vacancy, and management costs.",
        "401k": "🏦 **401(k) Optimization:** Contribute enough to get full employer match, then max Roth IRA, then return to 401(k). Choose low-cost index funds. Consider Roth 401(k) if in lower tax bracket now. Rebalance annually."
    }
    
    question_lower = question.lower()
    for key, advice in advice_map.items():
        if key in question_lower:
            return advice
    
    return "💼 **Professional Strategy:** Focus on maximizing tax-advantaged accounts, building a diversified investment portfolio, and optimizing your overall financial strategy. Consider consulting with a fee-only financial advisor for complex situations."

# Sidebar configuration
with st.sidebar:
    st.header("👤 Your Profile")
    demographic = st.selectbox(
        "I am a...", 
        ["Student", "Professional"],
        help="This helps customize advice to your situation"
    )
    
    # API Status
    groq_client = get_groq_client()
    if groq_client:
        st.success("🚀 Groq AI Connected")
    else:
        st.warning("⚠️ Using Fallback Responses")
    
    # Show demographic-specific badge and tips
    if demographic == "Student":
        st.markdown('<span class="demographic-badge student-badge">🎓 Student Mode</span>', unsafe_allow_html=True)
        st.markdown("""
        ### 📚 Student Quick Tips
        - **Emergency Fund**: Start with $500-$1000
        - **Credit Building**: Student credit card, pay in full
        - **Budgeting**: Try 50/30/20 rule
        - **Investing**: Start with $25/month in index funds
        - **Income**: Look for campus jobs, internships
        - **Discounts**: Student pricing on everything!
        """)
        
    else:  # Professional
        st.markdown('<span class="demographic-badge professional-badge">💼 Professional Mode</span>', unsafe_allow_html=True)
        st.markdown("""
        ### 💼 Professional Strategies
        - **401(k)**: Max employer match, then Roth IRA
        - **Portfolio**: 80-90% stocks, 10-20% bonds
        - **Emergency**: 3-6 months expenses
        - **Tax Optimization**: HSA, tax-loss harvesting
        - **Insurance**: Term life, disability, umbrella
        - **Estate Planning**: Will, beneficiaries updated
        """)

# Main chat interface
col1, col2 = st.columns([3, 1])

with col1:
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    # User input
    user_input = st.text_input(
        f"Ask me anything about finances as a {demographic.lower()}:",
        placeholder="e.g., How should I start investing with $100/month?",
        key="user_input"
    )

    # Process user input
    if user_input and user_input.strip():
        groq_client = get_groq_client()
        
        with st.spinner(f"Getting personalized advice for {demographic.lower()}s..."):
            if demographic == "Student":
                response = get_student_financial_advice(user_input, groq_client)
            else:
                response = get_professional_financial_advice(user_input, groq_client)
            
            # Add to chat history
            st.session_state['chat_history'].append({
                'question': user_input,
                'answer': response,
                'demographic': demographic
            })

    # Display chat history
    if st.session_state['chat_history']:
        st.subheader("💬 Chat History")
        
        for i, chat in enumerate(reversed(st.session_state['chat_history'])):
            # User message
            st.markdown(f"""
            <div class="chat-message user-message">
                <span class="user-name">You ({chat['demographic']}):</span> {chat['question']}
            </div>
            """, unsafe_allow_html=True)
            
            # Bot response
            st.markdown(f"""
            <div class="chat-message bot-message">
                <span class="bot-name">💰 Finance Bot:</span><br>
                <span class="response-text">{chat['answer']}</span>
            </div>
            """, unsafe_allow_html=True)
            
            if i < len(st.session_state['chat_history']) - 1:
                st.divider()

with col2:
    # Quick action buttons
    st.subheader("🚀 Quick Questions")
    
    if demographic == "Student":
        questions = [
            "How to budget $200/month?",
            "Best student credit card?",
            "Should I get a part-time job?",
            "How to save for textbooks?",
            "Building credit tips?"
        ]
    else:
        questions = [
            "401(k) vs Roth IRA strategy?",
            "Best investment allocation?",
            "Tax optimization tips?",
            "Emergency fund amount?",
            "Real estate investing?"
        ]
    
    for question in questions:
        if st.button(question, key=f"quick_{question}", use_container_width=True):
            # Add the question directly to chat history with response
            groq_client = get_groq_client()
            with st.spinner(f"Getting advice..."):
                if demographic == "Student":
                    response = get_student_financial_advice(question, groq_client)
                else:
                    response = get_professional_financial_advice(question, groq_client)
                
                # Add to chat history
                st.session_state['chat_history'].append({
                    'question': question,
                    'answer': response,
                    'demographic': demographic
                })
                st.rerun()

# Clear chat button
if st.session_state['chat_history']:
    if st.button("🗑️ Clear Chat History", type="secondary"):
        st.session_state['chat_history'] = []
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8rem;">
💡 This chatbot provides educational information only. Always consult with qualified financial professionals for important decisions.<br>
<strong>Status:</strong> Groq API Connected ✅ | Fallback Responses Available ✅
</div>
""", unsafe_allow_html=True)
