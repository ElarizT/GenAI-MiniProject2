import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
import json
from typing import Dict, Any

# Load environment variables
load_dotenv()

# Add API key validation
def validate_api_key(api_key: str) -> bool:
    """Validate if the API key format looks correct"""
    return api_key and api_key.startswith('gsk_') and len(api_key) > 20

class EmailDraftingAgent:
    def __init__(self, api_key=None):
        # Get API key from parameter or environment
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        
        # Initialize client only if API key is available
        if self.api_key:
            try:
                self.client = Groq(api_key=self.api_key)
                self.model = "llama-3.3-70b-versatile"
            except Exception as e:
                st.error(f"Error initializing Groq client: {str(e)}")
                self.client = None
        else:
            self.client = None
    
    def draft_email(self, recipient_name: str, recipient_role: str, purpose: str, 
                   key_details: str, tone: str = "professional") -> Dict[str, str]:
        """
        Draft an email based on bullet-point inputs
        
        Args:
            recipient_name: Name of the recipient
            recipient_role: Role/position of the recipient
            purpose: Purpose of the email
            key_details: Key details or points to include
            tone: Tone of the email (professional, friendly, formal)
        
        Returns:
            Dict containing subject, greeting, body, and closing
        """
        
        # Check if client is initialized
        if not self.client:
            st.error("Groq client not initialized. Please check your API key.")
            return None
        
        prompt = f"""
        You are an expert email drafting assistant. Create a professional email based on the following inputs:

        Recipient Name: {recipient_name}
        Recipient Role: {recipient_role}
        Purpose: {purpose}
        Key Details: {key_details}
        Tone: {tone}

        Please create a well-structured email with:
        1. A clear and relevant subject line
        2. An appropriate greeting
        3. A concise body that includes all key information in a natural flow
        4. A professional closing

        Return the response in JSON format with the following structure:
        {{
            "subject": "Email subject line",
            "greeting": "Dear [Name] or appropriate greeting",
            "body": "Main email content with proper paragraphs",
            "closing": "Professional closing with signature line"
        }}

        Make sure the email sounds natural, professional, and includes all the key details provided.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional email drafting assistant. Always respond with valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Parse the JSON response
            email_content = json.loads(response.choices[0].message.content)
            return email_content
            
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            raw_response = response.choices[0].message.content
            return {
                "subject": "Email Draft",
                "greeting": "Dear Recipient,",
                "body": raw_response,
                "closing": "Best regards,\nYour Name"
            }
        except Exception as e:
            st.error(f"Error generating email: {str(e)}")
            return None

def main():
    st.set_page_config(
        page_title="Email Drafting Agent",
        page_icon="📧",
        layout="wide"
    )
    
    st.title("📧 Email Drafting Agent")
    st.markdown("Transform bullet-point inputs into professional email drafts using AI")
    
    # Initialize the agent
    groq_api_key = os.getenv('GROQ_API_KEY', '')
    
    # Sidebar for API key configuration
    with st.sidebar:
        st.header("Configuration")
        groq_api_key = st.text_input(
            "Groq API Key",
            type="password",
            value=groq_api_key,
            help="Enter your Groq API key"
        )
        
        if not groq_api_key:
            st.info("💡 Get your free API key from [Groq Console](https://console.groq.com/)")
        
        st.markdown("---")
        st.markdown("### How to use:")
        st.markdown("1. Enter recipient details")
        st.markdown("2. Specify email purpose")
        st.markdown("3. Add key points")
        st.markdown("4. Choose tone")
        st.markdown("5. Generate email draft")
    
    # Initialize or update the agent with the API key
    if groq_api_key and validate_api_key(groq_api_key) and ('agent' not in st.session_state or st.session_state.get('current_api_key') != groq_api_key):
        try:
            st.session_state.agent = EmailDraftingAgent(api_key=groq_api_key)
            st.session_state.current_api_key = groq_api_key
            if st.session_state.agent.client:
                st.sidebar.success("✅ API key validated")
        except Exception as e:
            st.sidebar.error(f"❌ Error initializing agent: {str(e)}")
            st.session_state.agent = None
    elif groq_api_key and not validate_api_key(groq_api_key):
        st.sidebar.error("❌ Invalid API key format. Should start with 'gsk_'")
        st.session_state.agent = None
    elif not groq_api_key:
        st.session_state.agent = None
    
    # Main interface
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Email Details")
        
        # Input fields
        recipient_name = st.text_input(
            "Recipient Name",
            placeholder="e.g., John Smith",
            help="Name of the person you're emailing"
        )
        
        recipient_role = st.text_input(
            "Recipient Role/Position",
            placeholder="e.g., Project Manager, CEO, HR Director",
            help="Role or position of the recipient"
        )
        
        purpose = st.text_area(
            "Purpose of Email",
            placeholder="e.g., Schedule a meeting, Follow up on proposal, Request information",
            help="Main purpose or reason for the email"
        )
        
        key_details = st.text_area(
            "Key Details/Points",
            placeholder="• Meeting agenda items\n• Specific dates/times\n• Project deliverables\n• Questions to ask",
            help="Bullet points or key information to include",
            height=120
        )
        
        tone = st.selectbox(
            "Email Tone",
            ["professional", "friendly", "formal", "casual"],
            help="Choose the tone for your email"
        )
        
        # Generate button
        if st.button("✨ Generate Email Draft", type="primary"):
            if not groq_api_key:
                st.error("Please enter your Groq API key in the sidebar")
            elif not all([recipient_name, purpose, key_details]):
                st.error("Please fill in all required fields")
            elif not st.session_state.get('agent') or not st.session_state.agent.client:
                st.error("Agent not properly initialized. Please check your API key.")
            else:
                with st.spinner("Generating email draft..."):
                    email_draft = st.session_state.agent.draft_email(
                        recipient_name=recipient_name,
                        recipient_role=recipient_role,
                        purpose=purpose,
                        key_details=key_details,
                        tone=tone
                    )
                    
                    if email_draft:
                        st.session_state.email_draft = email_draft
                        st.success("Email draft generated successfully!")
    
    with col2:
        st.header("📧 Generated Email")
        
        if 'email_draft' in st.session_state:
            email = st.session_state.email_draft
            
            # Display the email
            st.subheader("Subject:")
            st.code(email.get('subject', ''), language=None)
            
            st.subheader("Email Content:")
            email_content = f"""{email.get('greeting', '')}

{email.get('body', '')}

{email.get('closing', '')}"""
            
            st.text_area(
                "Full Email Draft",
                value=email_content,
                height=400,
                help="Copy this email draft to your email client"
            )
            
            # Copy to clipboard button
            st.markdown("### Actions")
            if st.button("📋 Copy to Clipboard"):
                st.write("Email content copied! (Note: Manual copy required)")
                st.code(email_content, language=None)
            
            # Download as text file
            st.download_button(
                label="📥 Download as Text File",
                data=email_content,
                file_name="email_draft.txt",
                mime="text/plain"
            )
        else:
            st.info("Generate an email draft to see the result here")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "**Email Drafting Agent** | Powered by Llama 3.3 70B via Groq API | Built with Streamlit"
    )

if __name__ == "__main__":
    main()
