import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
import json
from typing import Dict, Any

# Load environment variables
load_dotenv()

class EmailDraftingAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.model = "llama-3.3-70b-versatile"
    
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
    if 'agent' not in st.session_state:
        st.session_state.agent = EmailDraftingAgent()
    
    # Sidebar for API key configuration
    with st.sidebar:
        st.header("Configuration")
        groq_api_key = st.text_input(
            "Groq API Key",
            type="password",
            value=os.getenv('GROQ_API_KEY', ''),
            help="Enter your Groq API key"
        )
        
        if groq_api_key:
            os.environ['GROQ_API_KEY'] = groq_api_key
            st.session_state.agent = EmailDraftingAgent()
        
        st.markdown("---")
        st.markdown("### How to use:")
        st.markdown("1. Enter recipient details")
        st.markdown("2. Specify email purpose")
        st.markdown("3. Add key points")
        st.markdown("4. Choose tone")
        st.markdown("5. Generate email draft")
    
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
