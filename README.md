# 🚀 Resume Chatbot - AI-Powered Career Assistant

An intelligent chatbot that knows all about my professional background, skills, experience, and career details. Built with Streamlit and powered by OpenAI's GPT models.

## ✨ Features

- 🤖 **AI-Powered Conversations** - Intelligent responses about resume, skills, and experience
- 💬 **Interactive Chat Interface** - Clean, modern chat UI with Streamlit
- 📊 **Question Tracking** - Monitor usage with session management
- 🔄 **Session Management** - Persistent chat history and question limits
- 📱 **Responsive Design** - Works great on desktop and mobile
- 🚀 **Easy Deployment** - One-click deployment to Streamlit Cloud

## 🚀 Quick Deploy to Streamlit Cloud

1. **Fork this repository** to your GitHub account

2. **Go to [Streamlit Cloud](https://streamlit.io/cloud)** and sign up/login

3. **Create a new app:**
   - Click "New app"
   - Connect your GitHub repository
   - Set the main file path to: `streamlit_app.py`
   - Click "Deploy!"

4. **Set up secrets:**
   - In your Streamlit Cloud dashboard, go to "Settings" → "Secrets"
   - Add your environment variables:
   ```
   OPENAI_API_KEY = "your_actual_openai_api_key"
   PUSHOVER_TOKEN = "your_pushover_token"  # optional
   PUSHOVER_USER = "your_pushover_user_key"  # optional
   ```

5. **Your app will be live!** 🎉

## 🛠️ Local Development

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd Resume_chatbot-main
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up secrets:**
   
   **Option A: Local development (recommended)**
   Create `.streamlit/secrets.toml`:
   ```toml
   OPENAI_API_KEY = "your_openai_api_key_here"
   PUSHOVER_TOKEN = "your_pushover_token_here"  # optional
   PUSHOVER_USER = "your_pushover_user_key_here"  # optional
   ```
   
   **Option B: Environment variables**
   Create a `.env` file in the root directory:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   PUSHOVER_TOKEN=your_pushover_token_here  # optional
   PUSHOVER_USER=your_pushover_user_key_here  # optional
   ```

5. **Run the app:**
   ```bash
   streamlit run streamlit_app.py
   ```

6. **Open your browser** and go to `http://localhost:8501`

## 📁 Project Structure

```
Resume_chatbot-main/
├── streamlit_app.py          # Main Streamlit application
├── database.py              # Database operations and caching
├── embeddings.py            # Embedding utilities
├── search.py                # Search functionality
├── me/                      # Resume data and embeddings
│   ├── embeddings.json      # Pre-computed embeddings
│   ├── summary2.txt         # Background summary
│   ├── github_profile.txt   # GitHub profile data
│   └── MKM_Master_Resume.pdf # Resume PDF (not in repo)
├── requirements.txt         # Python dependencies
├── .streamlit/              # Streamlit configuration
│   └── config.toml
├── packages.txt             # System dependencies
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY` (required): Your OpenAI API key
- `PUSHOVER_TOKEN` (optional): For push notifications
- `PUSHOVER_USER` (optional): Pushover user key

### Customization

- **Question Limit**: Modify `MAX_QUESTIONS` in `streamlit_app.py`
- **Admin Access**: Change `ADMIN_SESSION_ID` for unlimited access
- **Model**: Update the OpenAI model in the `chat()` function
- **Styling**: Customize the Streamlit theme and layout

## 🤖 How It Works

1. **Document Processing**: Resume and profile data are processed into embeddings
2. **Context Retrieval**: User queries are matched against relevant content
3. **AI Response**: OpenAI GPT generates contextual responses
4. **Caching**: Responses are cached for faster future access
5. **Session Management**: Tracks user sessions and question limits

## 🎯 Use Cases

- **Portfolio Integration**: Embed in your personal website
- **Career Networking**: Share with potential employers
- **Interview Preparation**: Practice common questions
- **Professional Branding**: Showcase AI skills and experience

## 🛡️ Security & Privacy

- **No Data Storage**: Chat history is session-based only
- **API Key Protection**: Secrets are securely managed
- **Rate Limiting**: Built-in question limits prevent abuse
- **Input Validation**: All user inputs are sanitized

## 🚀 Deployment Options

### Streamlit Cloud (Recommended)
- Free tier available
- Automatic deployments from GitHub
- Built-in secret management
- Global CDN

### Other Options
- **Heroku**: Use the `Procfile` and `runtime.txt`
- **Railway**: Direct GitHub integration
- **Vercel**: Python runtime support
- **AWS/GCP**: Container deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - feel free to use this project for your own resume chatbot!

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [OpenAI GPT](https://openai.com/)
- Icons from [Emoji](https://emojipedia.org/)

---

**Ready to deploy?** Follow the [Quick Deploy](#-quick-deploy-to-streamlit-cloud) guide above! 🚀
