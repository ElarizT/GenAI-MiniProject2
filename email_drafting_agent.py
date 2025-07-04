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
        Create a professional email based on these inputs:

        Recipient Name: {recipient_name}
        Recipient Role: {recipient_role}
        Purpose: {purpose}
        Key Details: {key_details}
        Tone: {tone}

        Requirements:
        1. Create a clear, relevant subject line
        2. Use appropriate greeting for the recipient
        3. Write a concise body that naturally incorporates all key details
        4. End with a professional closing

        CRITICAL: You must respond with ONLY a valid JSON object. No markdown formatting, no code blocks, no additional text. Just the JSON object.
        
        Format exactly like this:
        {{
            "subject": "Your subject line here",
            "greeting": "Dear {recipient_name}," if name provided, otherwise "Dear Sir/Madam,",
            "body": "Complete email body with all key details naturally integrated",
            "closing": "Professional closing with signature placeholder"
        }}
        
        Do not include any text before or after the JSON. Do not wrap in markdown code blocks.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional email drafting assistant. Always respond with valid JSON format only, no markdown formatting or additional text."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Get the raw response
            raw_response = response.choices[0].message.content.strip()
            
            # Clean up the response - remove any markdown code blocks
            cleaned_response = raw_response
            if '```json' in cleaned_response:
                cleaned_response = cleaned_response.split('```json')[1].split('```')[0].strip()
            elif '```' in cleaned_response:
                # Handle cases where there's just ``` without json
                parts = cleaned_response.split('```')
                if len(parts) >= 3:
                    cleaned_response = parts[1].strip()
                elif len(parts) == 2:
                    cleaned_response = parts[1].strip()
            
            # Remove any leading/trailing whitespace and newlines
            cleaned_response = cleaned_response.strip()
            
            # Parse the JSON response
            email_content = json.loads(cleaned_response)
            
            # Clean each field to ensure no JSON artifacts remain
            cleaned_email = {}
            for field in ['subject', 'greeting', 'body', 'closing']:
                if field in email_content:
                    value = str(email_content[field]).strip()
                    # Remove any remaining JSON artifacts
                    value = value.replace('```json', '').replace('```', '').strip()
                    # Remove quotes if the entire string is quoted
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    cleaned_email[field] = value
            
            # Validate that we have the required fields
            required_fields = ['subject', 'greeting', 'body', 'closing']
            if all(field in cleaned_email and cleaned_email[field] for field in required_fields):
                return cleaned_email
            else:
                # If fields are missing, create a fallback structure
                return {
                    "subject": cleaned_email.get('subject', 'Email Draft'),
                    "greeting": cleaned_email.get('greeting', f"Dear {recipient_name},"),
                    "body": cleaned_email.get('body', cleaned_response),
                    "closing": cleaned_email.get('closing', "Best regards,\n[Your Name]")
                }
            
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails - try to extract content manually
            raw_response = response.choices[0].message.content
            
            # Try to extract JSON from within the response
            import re
            json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
            if json_match:
                try:
                    email_content = json.loads(json_match.group())
                    # Clean the extracted content
                    cleaned_email = {}
                    for field in ['subject', 'greeting', 'body', 'closing']:
                        if field in email_content:
                            value = str(email_content[field]).strip()
                            value = value.replace('```json', '').replace('```', '').strip()
                            if value.startswith('"') and value.endswith('"'):
                                value = value[1:-1]
                            cleaned_email[field] = value
                    return cleaned_email
                except:
                    pass
            
            # Final fallback - create structured response from raw text
            clean_text = raw_response.replace('```json', '').replace('```', '').strip()
            return {
                "subject": f"Re: {purpose}",
                "greeting": f"Dear {recipient_name},",
                "body": clean_text,
                "closing": "Best regards,\n[Your Name]"
            }
        except Exception as e:
            st.error(f"Error generating email: {str(e)}")
            return None

def main():
    st.set_page_config(
        page_title="Email Drafting Agent",
        page_icon="📧",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    st.title("📧 Email Drafting Agent")
    st.markdown("Transform bullet-point inputs into professional email drafts using AI")
    
    # Initialize the agent with environment variable API key
    groq_api_key = os.getenv('GROQ_API_KEY', '')
    
    # Check if API key is available and valid
    if not groq_api_key:
        st.error("❌ GROQ_API_KEY environment variable is not set. Please set your API key in the .env file.")
        st.info("💡 Get your free API key from [Groq Console](https://console.groq.com/) and add it to your .env file")
        st.stop()
    
    if not validate_api_key(groq_api_key):
        st.error("❌ Invalid API key format. Should start with 'gsk_'")
        st.stop()
    
    # Initialize the agent
    if 'agent' not in st.session_state:
        try:
            st.session_state.agent = EmailDraftingAgent(api_key=groq_api_key)
            if not st.session_state.agent.client:
                st.error("❌ Failed to initialize Groq client. Please check your API key.")
                st.stop()
        except Exception as e:
            st.error(f"❌ Error initializing agent: {str(e)}")
            st.stop()
    
    # Main interface - full width
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
            if not all([recipient_name, purpose, key_details]):
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
            
            # Validate and clean email content
            subject = str(email.get('subject', 'Email Draft')).strip()
            greeting = str(email.get('greeting', 'Dear Recipient,')).strip()
            body = str(email.get('body', '')).strip()
            closing = str(email.get('closing', 'Best regards,\n[Your Name]')).strip()
            
            # Additional cleaning to ensure no JSON artifacts remain
            def clean_field(field_content):
                """Clean any remaining JSON or markdown artifacts from a field"""
                content = str(field_content).strip()
                # Remove markdown code blocks
                content = content.replace('```json', '').replace('```', '').strip()
                # Remove quotes if the entire string is quoted
                if content.startswith('"') and content.endswith('"'):
                    content = content[1:-1]
                return content
            
            subject = clean_field(subject)
            greeting = clean_field(greeting)
            body = clean_field(body)
            closing = clean_field(closing)
            
            # Validate that none of the fields look like JSON or contain artifacts
            def is_json_like(content):
                """Check if content looks like JSON or contains JSON artifacts"""
                content = str(content).strip()
                return (content.startswith('{') and content.endswith('}')) or \
                       content.startswith('```') or \
                       '"subject"' in content or \
                       '"greeting"' in content or \
                       '"body"' in content or \
                       '"closing"' in content
            
            # Check if any field contains JSON artifacts
            if any(is_json_like(field) for field in [subject, greeting, body, closing]):
                st.error("Email formatting error detected. Please try generating again.")
                del st.session_state.email_draft
                return
            
            # Display the email
            st.subheader("Subject:")
            st.code(subject, language=None)
            
            st.subheader("Email Content:")
            email_content = f"""{greeting}

{body}

{closing}"""
            
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
