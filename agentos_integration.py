"""
GenAI AgentOS Integration for Email Drafting Agent
This module provides integration with the GenAI AgentOS framework
"""

import json
import sys
import os
from typing import Dict, Any, Optional
from email_drafting_agent import EmailDraftingAgent

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class EmailDraftingAgentOS:
    """
    Email Drafting Agent for GenAI AgentOS
    Transforms bullet-point inputs into professional email drafts
    """
    
    def __init__(self):
        self.name = "Email Drafting Agent"
        self.description = "Transform bullet-point inputs into professional email drafts using AI"
        self.version = "1.0.0"
        self.author = "AI Assistant"
        self.tags = ["email", "writing", "productivity", "communication"]
        self.email_agent = EmailDraftingAgent()
        self.id = "email-drafting-agent-v1"
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the email drafting agent
        
        Args:
            input_data: Dictionary containing:
                - recipient_name: str (required)
                - recipient_role: str (optional)
                - purpose: str (required)
                - key_details: str (required)
                - tone: str (optional, defaults to "professional")
        
        Returns:
            Dictionary containing the generated email draft
        """
        try:
            # Extract parameters from input
            recipient_name = input_data.get('recipient_name', '')
            recipient_role = input_data.get('recipient_role', '')
            purpose = input_data.get('purpose', '')
            key_details = input_data.get('key_details', '')
            tone = input_data.get('tone', 'professional')
            
            # Validate required fields
            if not recipient_name or not purpose or not key_details:
                return {
                    "success": False,
                    "error": "Missing required fields: recipient_name, purpose, and key_details are required"
                }
            
            # Generate email draft
            email_draft = self.email_agent.draft_email(
                recipient_name=recipient_name,
                recipient_role=recipient_role,
                purpose=purpose,
                key_details=key_details,
                tone=tone
            )
            
            if email_draft:
                return {
                    "success": True,
                    "email_draft": email_draft,
                    "full_email": self._format_full_email(email_draft),
                    "agent_info": {
                        "name": self.name,
                        "version": self.version,
                        "id": self.id
                    }
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to generate email draft"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"An error occurred: {str(e)}"
            }
    
    def _format_full_email(self, email_draft: Dict[str, str]) -> str:
        """Format the email draft into a complete email string"""
        return f"""Subject: {email_draft.get('subject', '')}

{email_draft.get('greeting', '')}

{email_draft.get('body', '')}

{email_draft.get('closing', '')}"""
    
    def get_input_schema(self) -> Dict[str, Any]:
        """Return the input schema for the agent"""
        return {
            "type": "object",
            "properties": {
                "recipient_name": {
                    "type": "string",
                    "description": "Name of the email recipient",
                    "required": True
                },
                "recipient_role": {
                    "type": "string",
                    "description": "Role or position of the recipient (optional)",
                    "required": False
                },
                "purpose": {
                    "type": "string",
                    "description": "Purpose or reason for the email",
                    "required": True
                },
                "key_details": {
                    "type": "string",
                    "description": "Key details or bullet points to include in the email",
                    "required": True
                },
                "tone": {
                    "type": "string",
                    "description": "Tone of the email (professional, friendly, formal, casual)",
                    "enum": ["professional", "friendly", "formal", "casual"],
                    "default": "professional",
                    "required": False
                }
            },
            "required": ["recipient_name", "purpose", "key_details"]
        }
    
    def get_output_schema(self) -> Dict[str, Any]:
        """Return the output schema for the agent"""
        return {
            "type": "object",
            "properties": {
                "success": {
                    "type": "boolean",
                    "description": "Whether the email generation was successful"
                },
                "email_draft": {
                    "type": "object",
                    "description": "Generated email components",
                    "properties": {
                        "subject": {"type": "string"},
                        "greeting": {"type": "string"},
                        "body": {"type": "string"},
                        "closing": {"type": "string"}
                    }
                },
                "full_email": {
                    "type": "string",
                    "description": "Complete formatted email"
                },
                "agent_info": {
                    "type": "object",
                    "description": "Agent information",
                    "properties": {
                        "name": {"type": "string"},
                        "version": {"type": "string"},
                        "id": {"type": "string"}
                    }
                },
                "error": {
                    "type": "string",
                    "description": "Error message if generation failed"
                }
            }
        }
    
    def get_agent_metadata(self) -> Dict[str, Any]:
        """Return agent metadata for registration"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "author": self.author,
            "tags": self.tags,
            "input_schema": self.get_input_schema(),
            "output_schema": self.get_output_schema(),
            "capabilities": [
                "Email drafting from bullet points",
                "Multiple tone options",
                "Professional email formatting",
                "Subject line generation",
                "Greeting and closing generation"
            ]
        }

# Create a global instance for easy access
email_agent = EmailDraftingAgentOS()

def register_email_agent():
    """Register the Email Drafting Agent with GenAI AgentOS"""
    agent = EmailDraftingAgentOS()
    
    # Generate registration info
    registration_info = agent.get_agent_metadata()
    
    # Save registration info to file for GenAI AgentOS
    with open('agent_registration.json', 'w') as f:
        json.dump(registration_info, f, indent=2)
    
    print("Email Drafting Agent registration info saved to agent_registration.json")
    return agent

def test_agent_integration():
    """Test the agent integration with sample data"""
    agent = EmailDraftingAgentOS()
    
    # Test input
    test_input = {
        "recipient_name": "John Doe",
        "recipient_role": "Project Manager",
        "purpose": "Schedule a meeting",
        "key_details": "• Discuss project timeline\n• Review deliverables\n• Next week availability",
        "tone": "professional"
    }
    
    print("Testing Email Drafting Agent...")
    print(f"Input: {test_input}")
    
    result = agent.execute(test_input)
    print(f"Output: {json.dumps(result, indent=2)}")
    
    return result

if __name__ == "__main__":
    # Register the agent when run directly
    agent = register_email_agent()
    print(f"Email Drafting Agent registered successfully!")
    print(f"Agent ID: {agent.id}")
    print(f"Agent Name: {agent.name}")
    print(f"Agent Description: {agent.description}")
    
    # Test the agent
    print("\n" + "="*50)
    print("Testing Agent Integration...")
    test_agent_integration()
