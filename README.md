# BMW Car Configurator

A Flask web application that recreates the BMW car configurator experience with real-time AI assistance using Google Gemini Flash 2.5.

## Features

- **Real BMW Data**: Scrapes actual BMW model data, options, and pricing
- **AI-Powered Suggestions**: Uses Google Gemini Flash 2.5 for intelligent configuration recommendations
- **Interactive Configuration**: Real-time price updates and validation
- **Responsive Design**: Works on desktop and mobile devices
- **Configuration Management**: Save and load different configurations
- **Validation System**: Checks for option conflicts and constraints

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- Chrome browser (for web scraping)

### 2. Installation

```bash
# Clone the repository
git clone <repository-url>
cd bmw-configurator

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

**Option A: Quick Setup (Recommended)**
```bash
python setup_env.py
```
This interactive script will guide you through setting up your environment variables.

**Option B: Manual Setup**
1. Create a `.env` file in the project root
2. Add your Google Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   FLASK_ENV=development
   FLASK_DEBUG=True
   SECRET_KEY=your-secret-key-here
   ```

**Getting a Gemini API Key:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key
5. Add it to your `.env` file

### 4. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
bmw-configurator/
├── app.py                 # Main Flask application
├── bmw_scraper.py        # BMW data scraping logic
├── car_configurator.py   # Configuration validation and pricing
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
├── static/
│   ├── css/
│   │   └── style.css     # Custom styles
│   ├── js/
│   │   └── main.js       # JavaScript functionality
│   └── images/           # Car images
└── templates/
    ├── base.html         # Base template
    ├── index.html        # Main page
    ├── configurator.html # Configuration page
    └── error.html        # Error page
```

## API Endpoints

- `GET /` - Main page with series selection
- `GET /api/series` - Get all BMW series
- `GET /api/models/<series>` - Get models for series
- `GET /api/options/<model>` - Get options for model
- `GET /configurator/<model>` - Configuration page
- `POST /api/gemini/suggest` - AI configuration suggestions
- `POST /api/validate-configuration` - Validate configuration
- `POST /api/calculate-price` - Calculate total price
- `POST /api/save-configuration` - Save configuration

## Usage

1. **Select Series**: Choose from SUVs, Sedans, Coupes, etc.
2. **Choose Model**: Pick your specific BMW model
3. **Configure Options**: Select engines, colors, packages, and features
4. **Get AI Help**: Ask the AI assistant for recommendations
5. **Validate**: Check for conflicts and get suggestions
6. **Save**: Store your configuration for later

## AI Integration

The application uses Google Gemini Flash 2.5 for:
- Intelligent option recommendations based on user preferences
- Configuration validation and suggestions
- Comparison between different configurations
- Budget optimization advice

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational purposes only. BMW and related trademarks are property of BMW AG.
