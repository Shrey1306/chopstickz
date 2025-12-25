# Chopsticks: AI-Powered Video Editing Platform

An AI-powered video editing platform designed to simplify content creation for streamers and content creators.

## Project Structure

```
chopstickz/
├── webui/                          # Main Reflex web application
│   ├── __init__.py
│   ├── webui.py                    # Application entry point
│   ├── state.py                    # Application state management
│   ├── styles.py                   # Styling constants
│   └── components/                 # UI components
│       ├── __init__.py
│       ├── chat.py                 # Chat interface
│       ├── loading.py              # Loading indicator
│       ├── modal.py                # Modal dialogs
│       ├── navbar.py               # Navigation bar
│       ├── sidebar.py              # Sidebar drawer
│       └── video.py                # Video display and upload
├── tools/                          # Standalone tools
│   ├── __init__.py
│   └── video_editor.py             # PyQt5 video editor with LLM guidance
├── demo/                           # Demo applications
│   ├── __init__.py
│   └── showcase.py                 # Streamlit showcase app
├── assets/                         # Static assets
│   ├── custom_video_controls.js    # Video player controls
│   ├── favicon.ico
│   └── *.png, *.mp4                # Media files
├── rxconfig.py                     # Reflex configuration
├── requirements.txt                # Python dependencies
└── README.md
```

## Features

- **LLM-Powered Chat Interface**: Natural language commands for video editing
- **Video Upload and Display**: Upload streams and view them with custom controls
- **Multi-API Support**: OpenAI and Baidu API integration
- **Engagement Analysis**: Analyzes viewer engagement using:
  - Voice transcription (Whisper)
  - Chat sentiment analysis (RoBERTa)
  - Facial expression recognition (DeepFace)
  - Key moment identification (T5)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Shrey1306/chopstickz.git
   cd chopstickz
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   export OPENAI_API_KEY="your-api-key"
   # Or for Baidu:
   export BAIDU_API_KEY="your-api-key"
   export BAIDU_SECRET_KEY="your-secret-key"
   ```

## Running the Application

### Main Web Application (Reflex)
```bash
reflex run
```
The app will be available at `http://localhost:3000`

### Demo Showcase (Streamlit)
```bash
streamlit run demo/showcase.py
```

### Video Editor Tool (PyQt5)
```bash
python tools/video_editor.py
```

## Development

### Project Conventions
- Components in `webui/components/` are single-responsibility
- State management centralized in `webui/state.py`
- Styles defined in `webui/styles.py`

## License

MIT License
