import os
import json
import requests
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
from bmw_scraper import BMWDataScraper
from car_configurator import CarConfigurator
import logging
from datetime import datetime
import re

# Load environment variables
load_dotenv()

def analyze_user_preferences(preferences_text: str) -> dict:
    """Analyze user preferences to identify key themes"""
    preferences_lower = preferences_text.lower()
    
    # Keywords for different preference categories
    budget_keywords = ['budget', 'affordable', 'cheap', 'economic', 'value', 'cost', 'price', 'money', 'save']
    performance_keywords = ['fast', 'speed', 'power', 'sport', 'performance', 'acceleration', 'handling', 'track', 'racing']
    luxury_keywords = ['luxury', 'comfort', 'premium', 'elegant', 'sophisticated', 'high-end', 'executive', 'plush']
    tech_keywords = ['technology', 'tech', 'gadgets', 'connectivity', 'infotainment', 'digital', 'smart', 'connected']
    family_keywords = ['family', 'kids', 'children', 'safety', 'practical', 'spacious', 'cargo', 'room', 'seats']
    eco_keywords = ['eco', 'environment', 'green', 'electric', 'hybrid', 'fuel', 'efficiency', 'mpg', 'sustainable']
    
    def count_keywords(keywords, text):
        return sum(1 for keyword in keywords if keyword in text)
    
    return {
        'budget_conscious': count_keywords(budget_keywords, preferences_lower) > 0,
        'performance_oriented': count_keywords(performance_keywords, preferences_lower) > 0,
        'luxury_oriented': count_keywords(luxury_keywords, preferences_lower) > 0,
        'tech_savvy': count_keywords(tech_keywords, preferences_lower) > 0,
        'family_oriented': count_keywords(family_keywords, preferences_lower) > 0,
        'eco_conscious': count_keywords(eco_keywords, preferences_lower) > 0
    }

def get_model_specific_recommendations(model_name: str, model_data: dict) -> str:
    """Get model-specific recommendations based on the car's characteristics"""
    recommendations = []
    
    category = model_data.get('category', '').lower()
    base_price = model_data.get('base_price', 0)
    
    # Model category-specific recommendations
    if 'suv' in category:
        recommendations.append("- Consider xDrive for enhanced traction and capability")
        recommendations.append("- Convenience Package adds practical SUV features")
        recommendations.append("- Larger wheels (19-20\") complement the SUV stance")
    elif 'sedan' in category:
        recommendations.append("- M Sport Package enhances the sedan's sporty character")
        recommendations.append("- Premium Package adds executive comfort features")
        recommendations.append("- Technology Package essential for business use")
    elif 'electric' in category:
        recommendations.append("- Fast charging capability is standard")
        recommendations.append("- No exhaust options available (electric vehicle)")
        recommendations.append("- Regenerative braking enhances efficiency")
    elif 'm performance' in category or model_name.startswith('M'):
        recommendations.append("- Competition Package recommended for track use")
        recommendations.append("- Carbon fiber options reduce weight")
        recommendations.append("- Performance tires are essential")
        recommendations.append("- Sport exhaust enhances the M experience")
    
    # Price-based recommendations
    if base_price > 80000:
        recommendations.append("- Executive Package justifies the premium positioning")
        recommendations.append("- Individual options available for personalization")
        recommendations.append("- Premium audio systems complement luxury positioning")
    elif base_price < 40000:
        recommendations.append("- Focus on essential packages for best value")
        recommendations.append("- Technology Package provides modern features")
        recommendations.append("- Avoid over-optioning to maintain value proposition")
    
    # Model-specific notes
    model_notes = {
        "X1": "Entry-level SAV benefits from Premium Package for completeness",
        "X3": "Sweet spot for M Sport Package - enhances handling without compromising comfort",
        "X5": "Executive Package transforms this into a luxury flagship",
        "3 Series": "M Sport Package is almost essential for the sporty character",
        "5 Series": "Executive Package elevates this to true luxury sedan status",
        "7 Series": "Individual options expected at this price point",
        "M3": "Competition Package and track-focused options recommended",
        "M5": "Full M package suite enhances the ultimate performance sedan",
        "i4": "Technology Package essential for electric vehicle experience",
        "iX": "Premium Package recommended for flagship electric positioning"
    }
    
    if model_name in model_notes:
        recommendations.append(f"- {model_notes[model_name]}")
    
    return '\n'.join(recommendations) if recommendations else "Standard configuration recommendations apply."

def format_constraints_for_ai(constraints: dict) -> str:
    """Format constraints in a readable way for AI processing"""
    formatted = []
    
    # Engine/drivetrain constraints
    if 'engine_drivetrain' in constraints:
        formatted.append("Engine/Drivetrain Compatibility:")
        for engine, drivetrains in constraints['engine_drivetrain'].items():
            formatted.append(f"  - {engine}: {', '.join(drivetrains)}")
    
    # Package dependencies
    if 'package_dependencies' in constraints:
        formatted.append("\nPackage Dependencies:")
        for pkg, deps in constraints['package_dependencies'].items():
            formatted.append(f"  - {pkg} requires: {', '.join(deps)}")
    
    # Incompatible options
    if 'incompatible_options' in constraints:
        formatted.append("\nIncompatible Options:")
        for constraint in constraints['incompatible_options']:
            options = constraint.get('options', [])
            reason = constraint.get('reason', 'Conflict')
            formatted.append(f"  - Cannot combine: {', '.join(options)} ({reason})")
    
    return '\n'.join(formatted) if formatted else "No specific constraints to consider."

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'bmw-configurator-secret-key')
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini AI
gemini_api_key = os.environ.get('GEMINI_API_KEY')
if not gemini_api_key:
    logger.warning("GEMINI_API_KEY not found in environment variables. AI suggestions will not work.")
    logger.warning("Please add your Gemini API key to a .env file or environment variables.")
    gemini_model = None
else:
    try:
        genai.configure(api_key=gemini_api_key)
        gemini_model = genai.GenerativeModel('gemini-2.0-flash')
        logger.info("Google Gemini Flash 2.0 model initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Gemini model: {e}")
        gemini_model = None

# Initialize BMW data scraper and configurator
bmw_scraper = BMWDataScraper()
configurator = CarConfigurator()

@app.route('/')
def index():
    """Main page with BMW series selection"""
    try:
        series_data = bmw_scraper.get_all_series()
        return render_template('index.html', series=series_data)
    except Exception as e:
        logger.error(f"Error loading main page: {e}")
        return render_template('error.html', error="Failed to load BMW series data")

@app.route('/api/series')
def get_series():
    """API endpoint to get all BMW series"""
    try:
        series_data = bmw_scraper.get_all_series()
        return jsonify(series_data)
    except Exception as e:
        logger.error(f"Error fetching series data: {e}")
        return jsonify({'error': 'Failed to fetch series data'}), 500

@app.route('/api/models/<series>')
def get_models(series):
    """API endpoint to get models for a specific series"""
    try:
        models_data = bmw_scraper.get_models_for_series(series)
        return jsonify(models_data)
    except Exception as e:
        logger.error(f"Error fetching models for series {series}: {e}")
        return jsonify({'error': f'Failed to fetch models for series {series}'}), 500

@app.route('/api/options/<model>')
def get_options(model):
    """API endpoint to get all options for a specific model"""
    try:
        options_data = bmw_scraper.get_options_for_model(model)
        return jsonify(options_data)
    except Exception as e:
        logger.error(f"Error fetching options for model {model}: {e}")
        return jsonify({'error': f'Failed to fetch options for model {model}'}), 500

@app.route('/configurator/<model>')
def configurator_page(model):
    """Car configurator page for specific model"""
    try:
        logger.info(f"Loading configurator for model: {model}")
        
        model_data = bmw_scraper.get_model_details(model)
        options_data = bmw_scraper.get_options_for_model(model)
        
        # Debug logging
        logger.info(f"Model data keys: {model_data.keys() if model_data else 'None'}")
        logger.info(f"Options data keys: {options_data.keys() if options_data else 'None'}")
        
        # Ensure we have valid data structures
        if not model_data:
            logger.warning(f"No model data found for {model}")
            model_data = {"name": model, "base_price": 50000}
        
        if not options_data:
            logger.warning(f"No options data found for {model}")
            options_data = {
                "engines": [],
                "drivetrains": [],
                "exterior": {"colors": [], "wheels": []},
                "interior": {"upholstery": []},
                "packages": {"all_packages": []},
                "individual_options": []
            }
        
        return render_template('configurator.html', 
                             model=model_data, 
                             options=options_data)
    except Exception as e:
        logger.error(f"Error loading configurator for model {model}: {e}")
        logger.error(f"Exception details: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return render_template('error.html', error=f"Failed to load configurator for {model}")

@app.route('/api/gemini/suggest', methods=['POST'])
def gemini_suggest():
    """Use Gemini AI to suggest car configuration based on user preferences"""
    try:
        # Check if Gemini model is available
        if gemini_model is None:
            return jsonify({
                'error': 'AI suggestion service unavailable. Please configure GEMINI_API_KEY in environment variables.',
                'setup_instructions': {
                    'step1': 'Get API key from https://makersuite.google.com/app/apikey',
                    'step2': 'Create .env file with GEMINI_API_KEY=your_key_here',
                    'step3': 'Restart the application'
                }
            }), 503
        data = request.get_json()
        user_preferences = data.get('preferences', '')
        model_name = data.get('model', '')
        current_config = data.get('current_config', {})
        
        # Get comprehensive model data
        model_data = bmw_scraper.get_model_details(model_name)
        available_options = bmw_scraper.get_options_for_model(model_name)
        constraints = available_options.get('constraints', {})
        
        # Analyze user preferences for key themes
        preference_analysis = analyze_user_preferences(user_preferences)
        
        # Get model-specific recommendations
        model_recommendations = get_model_specific_recommendations(model_name, model_data)
        
        # Create comprehensive prompt for Gemini
        prompt = f"""
        You are a BMW expert consultant helping a customer configure their {model_name}. 

        MODEL DETAILS:
        - Base Price: ${model_data.get('base_price', 'N/A'):,}
        - Category: {model_data.get('category', 'N/A')}
        - Body Style: {model_data.get('body_style', 'N/A')}
        - Performance: {model_data.get('performance', {})}
        - Fuel Economy: {model_data.get('fuel_economy', {})}

        CUSTOMER PREFERENCES: "{user_preferences}"

        PREFERENCE ANALYSIS:
        - Budget Focus: {preference_analysis['budget_conscious']}
        - Performance Focus: {preference_analysis['performance_oriented']}
        - Luxury Focus: {preference_analysis['luxury_oriented']}
        - Technology Focus: {preference_analysis['tech_savvy']}
        - Family Focus: {preference_analysis['family_oriented']}
        - Eco Focus: {preference_analysis['eco_conscious']}

        AVAILABLE OPTIONS:
        Engines: {[f"{eng['code']}: {eng['name']} (+${eng['price']})" for eng in available_options.get('engines', [])]}
        Drivetrains: {[f"{dt['code']}: {dt['name']} (+${dt['price']})" for dt in available_options.get('drivetrains', [])]}
        Exterior Colors: {[f"{color['code']}: {color['name']} (+${color['price']})" for color in available_options.get('exterior', {}).get('colors', [])]}
        Interior Options: {[f"{interior['code']}: {interior['name']} (+${interior['price']})" for interior in available_options.get('interior', {}).get('upholstery', [])]}
        Packages: {[f"{pkg['code']}: {pkg['name']} - ${pkg['price']}" for pkg in available_options.get('packages', {}).get('all_packages', [])]}
        Individual Options: {[f"{opt['code']}: {opt['name']} - ${opt['price']}" for opt in available_options.get('individual_options', [])]}

        CURRENT SELECTION: {current_config}

        CONSTRAINTS TO CONSIDER:
        {format_constraints_for_ai(constraints)}

        MODEL-SPECIFIC RECOMMENDATIONS:
        {model_recommendations}

        Please provide a detailed configuration recommendation in the following JSON format:
        {{
            "recommended_config": {{
                "engine": "engine_code_from_available_options",
                "drivetrain": "drivetrain_code_from_available_options", 
                "exterior_color": "color_code_from_available_options",
                "interior": "interior_code_from_available_options",
                "packages": ["package_code1", "package_code2"],
                "individual_options": ["option_code1", "option_code2"]
            }},
            "reasoning": {{
                "engine": "Why this engine matches their needs",
                "drivetrain": "Why this drivetrain is recommended",
                "color": "Color recommendation reasoning",
                "packages": "Package recommendations and why",
                "overall": "Overall configuration summary"
            }},
            "price_estimate": {{
                "base_price": {model_data.get('base_price', 50000)},
                "estimated_options": 0,
                "estimated_total": 0
            }},
            "alternatives": {{
                "budget_option": "Suggestion for lower budget",
                "performance_option": "Suggestion for performance focus",
                "luxury_option": "Suggestion for luxury focus"
            }},
            "warnings": [
                "Any important considerations or trade-offs"
            ]
        }}

        Focus on:
        1. Use EXACT CODES from the available options above (e.g., "B58_3_0T" for engine, "xDrive" for drivetrain)
        2. Match customer preferences with appropriate options
        3. Avoid conflicting options based on constraints
        4. Provide value-conscious recommendations
        5. Explain the reasoning behind each choice
        6. Offer alternatives for different priorities
        
        IMPORTANT: Use only the option codes listed above. Do not make up codes.
        """
        
        response = gemini_model.generate_content(prompt)
        
        # Try to parse the JSON response
        try:
            suggestion_data = json.loads(response.text.strip().replace('```json', '').replace('```', ''))
        except json.JSONDecodeError:
            # Fallback to text response if JSON parsing fails
            suggestion_data = {
                "recommendation": response.text,
                "type": "text_response"
            }
        
        return jsonify({
            'suggestion': suggestion_data,
            'model': model_name,
            'preferences': user_preferences,
            'preference_analysis': preference_analysis,
            'model_data': model_data
        })
        
    except Exception as e:
        logger.error(f"Error with Gemini suggestion: {e}")
        return jsonify({'error': 'Failed to generate AI suggestion'}), 500

@app.route('/api/validate-configuration', methods=['POST'])
def validate_configuration():
    """Validate car configuration for conflicts and constraints"""
    try:
        data = request.get_json()
        configuration = data.get('configuration', {})
        model = data.get('model', '')
        
        validation_result = configurator.validate_configuration(model, configuration)
        
        return jsonify(validation_result)
        
    except Exception as e:
        logger.error(f"Error validating configuration: {e}")
        return jsonify({'error': 'Failed to validate configuration'}), 500

@app.route('/api/calculate-price', methods=['POST'])
def calculate_price():
    """Calculate total price for the configuration"""
    try:
        data = request.get_json()
        configuration = data.get('configuration', {})
        model = data.get('model', '')
        
        price_breakdown = configurator.calculate_price(model, configuration)
        
        return jsonify(price_breakdown)
        
    except Exception as e:
        logger.error(f"Error calculating price: {e}")
        return jsonify({'error': 'Failed to calculate price'}), 500

@app.route('/api/gemini/compare', methods=['POST'])
def gemini_compare():
    """Use Gemini AI to compare different configurations"""
    try:
        data = request.get_json()
        config1 = data.get('config1', {})
        config2 = data.get('config2', {})
        model = data.get('model', '')
        
        prompt = f"""
        Compare these two BMW {model} configurations and provide insights:
        
        Configuration 1: {json.dumps(config1, indent=2)}
        Configuration 2: {json.dumps(config2, indent=2)}
        
        Provide a detailed comparison including:
        1. Performance differences
        2. Value for money
        3. Luxury and comfort features
        4. Technology differences
        5. Overall recommendation
        
        Format your response in a clear, structured way.
        """
        
        response = gemini_model.generate_content(prompt)
        
        return jsonify({
            'comparison': response.text,
            'config1': config1,
            'config2': config2
        })
        
    except Exception as e:
        logger.error(f"Error with Gemini comparison: {e}")
        return jsonify({'error': 'Failed to generate AI comparison'}), 500

@app.route('/saved-configurations')
def saved_configurations():
    """Page to view saved configurations"""
    saved_configs = session.get('saved_configurations', [])
    return render_template('saved_configurations.html', configurations=saved_configs)

@app.route('/api/save-configuration', methods=['POST'])
def save_configuration():
    """Save a car configuration"""
    try:
        data = request.get_json()
        configuration = data.get('configuration', {})
        name = data.get('name', 'Untitled Configuration')
        
        if 'saved_configurations' not in session:
            session['saved_configurations'] = []
        
        config_data = {
            'name': name,
            'configuration': configuration,
            'timestamp': str(datetime.now()),
            'model': configuration.get('model', 'Unknown')
        }
        
        session['saved_configurations'].append(config_data)
        session.modified = True
        
        return jsonify({'success': True, 'message': 'Configuration saved successfully'})
        
    except Exception as e:
        logger.error(f"Error saving configuration: {e}")
        return jsonify({'error': 'Failed to save configuration'}), 500

@app.route('/api/delete-configuration', methods=['POST'])
def delete_configuration():
    """Delete a saved configuration"""
    try:
        data = request.get_json()
        index = data.get('index')
        
        if 'saved_configurations' in session and index is not None:
            saved_configs = session['saved_configurations']
            if 0 <= index < len(saved_configs):
                deleted_config = saved_configs.pop(index)
                session.modified = True
                return jsonify({'success': True, 'message': f'Configuration "{deleted_config["name"]}" deleted successfully'})
            else:
                return jsonify({'error': 'Invalid configuration index'}), 400
        else:
            return jsonify({'error': 'No configurations found or invalid index'}), 400
        
    except Exception as e:
        logger.error(f"Error deleting configuration: {e}")
        return jsonify({'error': 'Failed to delete configuration'}), 500

@app.route('/api/load-configuration/<int:index>')
def load_configuration(index):
    """Load a specific configuration"""
    try:
        saved_configs = session.get('saved_configurations', [])
        if 0 <= index < len(saved_configs):
            return jsonify({
                'success': True,
                'configuration': saved_configs[index]
            })
        else:
            return jsonify({'error': 'Configuration not found'}), 404
        
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        return jsonify({'error': 'Failed to load configuration'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
