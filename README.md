# Email Drafting Agent 📧

Transform bullet-point inputs into professional email drafts using AI-powered Llama 3.3 70B via Groq API.

## 🚀 Features

- **AI-Powered Email Generation**: Uses Llama 3.3 70B model for high-quality, professional emails
- **Bullet-Point to Email**: Convert simple bullet points into well-structured emails
- **Multiple Tones**: Choose from professional, friendly, formal, or casual tones
- **Clean Interface**: Simple, distraction-free web interface
- **Copy & Download**: Easy email copying and text file downloads
- **GenAI AgentOS Integration**: Fully compatible with GenAI AgentOS framework

## 📋 Prerequisites

- Python 3.8 or higher
- Groq API key (free from [Groq Console](https://console.groq.com/))

## 🛠️ Installation & Setup

### Step 1: Clone or Download
```bash
git clone <repository-url>
cd email-drafting-agent
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Up API Key
1. **Get your free Groq API key:**
   - Visit [Groq Console](https://console.groq.com/)
   - Sign up/login to get your API key
   - Your API key will start with `gsk_`

2. **Configure environment:**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit the .env file and add your API key
   GROQ_API_KEY=your_groq_api_key_here
   ```

### Step 4: Run the Application
```bash
streamlit run email_drafting_agent.py
```

Or use the launch script:
```bash
python launch.py
```

The app will open in your browser at `http://localhost:8501`

## 🎯 How to Use

1. **Fill in Email Details:**
   - **Recipient Name**: Person you're emailing (e.g., "John Snow")
   - **Recipient Role**: Their position (e.g., "Project Manager", "CEO")
   - **Purpose**: Main reason for the email (e.g., "Schedule a meeting")
   - **Key Details**: Bullet points of what to include
   - **Tone**: Choose the appropriate tone

2. **Generate Email**: Click "✨ Generate Email Draft"

3. **Copy & Use**: Copy the generated email to your email client

### Example Input
```
Recipient Name: Sarah Johnson
Recipient Role: Project Manager
Purpose: Schedule a project kickoff meeting
Key Details: 
• Need to discuss project timeline
• Review deliverables and milestones
• Assign team responsibilities
• Available next week Tuesday-Thursday
• Meeting duration: 2 hours
Tone: Professional
```

### Example Output
```
Subject: Project Kickoff Meeting Request

Dear Sarah Johnson,

I hope this email finds you well. I am reaching out to schedule a project kickoff meeting to ensure we start our collaboration on the right foot.

I would like to discuss the following key points during our meeting:
- Project timeline and key milestones
- Review of deliverables and expectations
- Assignment of team responsibilities

I am available next week from Tuesday through Thursday and would appreciate a 2-hour time slot that works best for your schedule. Please let me know your preferred date and time, and I will send out a calendar invitation accordingly.

Thank you for your time, and I look forward to our productive discussion.

Best regards,
[Your Name]
```

## 🔧 Technical Details

### Dependencies
- `streamlit` - Web interface
- `groq` - AI model API client
- `python-dotenv` - Environment variable management
- `typing` - Type hints support

### Model Configuration
- **Model**: Llama 3.3 70B Versatile
- **Max Tokens**: 1000
- **Temperature**: 0.7
- **Provider**: Groq API

## 🐛 Troubleshooting

### Common Issues

**❌ "GROQ_API_KEY environment variable is not set"**
- Make sure you've created a `.env` file
- Check that your API key is properly set in the `.env` file
- Ensure your API key starts with `gsk_`

**❌ "Invalid API key format"**
- Verify your API key from [Groq Console](https://console.groq.com/)
- Make sure there are no extra spaces or characters
- API keys should start with `gsk_`

**❌ "Error generating email"**
- Check your internet connection
- Verify your API key is valid and has credits
- Try generating the email again

### Getting Help
- Check the [Groq Documentation](https://console.groq.com/docs)
- Ensure all requirements are installed: `pip install -r requirements.txt`
- Try restarting the application

## 📁 Project Structure

```
email-drafting-agent/
├── email_drafting_agent.py    # Main application
├── agentos_integration.py     # GenAI AgentOS integration
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
├── .env                      # Your API key (create this)
├── launch.py                 # Launch script
├── README.md                 # This file
├── DEPLOYMENT.md             # Cloud deployment guide
└── .streamlit/
    └── config.toml           # Streamlit configuration
```


## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

**Email Drafting Agent** | Powered by Llama 3.3 70B via Groq API | Built with Streamlit