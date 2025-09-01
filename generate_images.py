"""
Generate placeholder images for BMW car configurator
Creates SVG-based placeholder images for different BMW models and series
"""

import os
from typing import Dict, List

def create_svg_car_image(model_name: str, car_type: str, color: str = "#1e3a5f", width: int = 400, height: int = 200) -> str:
    """Create an SVG representation of a car silhouette"""
    
    # Different car silhouettes based on type
    car_shapes = {
        "SUV": {
            "body": "M50,120 Q50,100 70,100 L330,100 Q350,100 350,120 L350,140 Q350,160 330,160 L320,160 Q320,180 300,180 Q280,180 280,160 L120,160 Q120,180 100,180 Q80,180 80,160 L70,160 Q50,160 50,140 Z",
            "wheel1": "cx='100' cy='160' r='15'",
            "wheel2": "cx='300' cy='160' r='15'",
            "windows": "M80,100 Q80,80 100,80 L150,80 Q170,80 170,100 M230,80 Q250,80 250,100 L300,100 Q320,80 320,100"
        },
        "Sedan": {
            "body": "M50,130 Q50,110 70,110 L330,110 Q350,110 350,130 L350,140 Q350,150 330,150 L320,150 Q320,170 300,170 Q280,170 280,150 L120,150 Q120,170 100,170 Q80,170 80,150 L70,150 Q50,150 50,140 Z",
            "wheel1": "cx='100' cy='150' r='12'",
            "wheel2": "cx='300' cy='150' r='12'",
            "windows": "M80,110 Q80,90 100,90 L140,90 Q160,90 160,110 M240,90 Q260,90 260,110 L300,110 Q320,90 320,110"
        },
        "Coupe": {
            "body": "M50,135 Q50,115 70,115 L330,115 Q350,115 350,135 L350,145 Q350,155 330,155 L320,155 Q320,175 300,175 Q280,175 280,155 L120,155 Q120,175 100,175 Q80,175 80,155 L70,155 Q50,155 50,145 Z",
            "wheel1": "cx='100' cy='155' r='12'",
            "wheel2": "cx='300' cy='155' r='12'",
            "windows": "M90,115 Q90,95 110,95 L290,95 Q310,95 310,115"
        },
        "Convertible": {
            "body": "M50,135 Q50,115 70,115 L330,115 Q350,115 350,135 L350,145 Q350,155 330,155 L320,155 Q320,175 300,175 Q280,175 280,155 L120,155 Q120,175 100,175 Q80,175 80,155 L70,155 Q50,155 50,145 Z",
            "wheel1": "cx='100' cy='155' r='12'",
            "wheel2": "cx='300' cy='155' r='12'",
            "windows": "M100,115 L300,115 Q310,105 300,105 L100,105 Q90,105 100,115"
        },
        "Electric": {
            "body": "M50,125 Q50,105 70,105 L330,105 Q350,105 350,125 L350,140 Q350,155 330,155 L320,155 Q320,175 300,175 Q280,175 280,155 L120,155 Q120,175 100,175 Q80,175 80,155 L70,155 Q50,155 50,140 Z",
            "wheel1": "cx='100' cy='155' r='14'",
            "wheel2": "cx='300' cy='155' r='14'",
            "windows": "M80,105 Q80,85 100,85 L150,85 Q170,85 170,105 M230,85 Q250,85 250,105 L300,105 Q320,85 320,105"
        },
        "M Performance": {
            "body": "M45,135 Q45,110 65,110 L335,110 Q355,110 355,135 L355,145 Q355,160 335,160 L325,160 Q325,180 305,180 Q285,180 285,160 L115,160 Q115,180 95,180 Q75,180 75,160 L65,160 Q45,160 45,145 Z",
            "wheel1": "cx='95' cy='160' r='16'",
            "wheel2": "cx='305' cy='160' r='16'",
            "windows": "M75,110 Q75,85 95,85 L145,85 Q165,85 165,110 M235,85 Q255,85 255,110 L305,110 Q325,85 325,110"
        }
    }
    
    shape = car_shapes.get(car_type, car_shapes["Sedan"])
    
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="carGradient" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:{color};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{darker_color(color)};stop-opacity:1" />
    </linearGradient>
    <linearGradient id="windowGradient" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#87CEEB;stop-opacity:0.8" />
      <stop offset="100%" style="stop-color:#4682B4;stop-opacity:0.8" />
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="{width}" height="{height}" fill="#f8f9fa"/>
  
  <!-- Ground line -->
  <line x1="0" y1="{height-20}" x2="{width}" y2="{height-20}" stroke="#ddd" stroke-width="2"/>
  
  <!-- Car body -->
  <path d="{shape['body']}" fill="url(#carGradient)" stroke="{darker_color(color)}" stroke-width="2"/>
  
  <!-- Windows -->
  <path d="{shape['windows']}" fill="url(#windowGradient)" stroke="#333" stroke-width="1"/>
  
  <!-- Wheels -->
  <circle {shape['wheel1']} fill="#2c3e50" stroke="#1a252f" stroke-width="2"/>
  <circle {shape['wheel2']} fill="#2c3e50" stroke="#1a252f" stroke-width="2"/>
  
  <!-- BMW kidney grille -->
  <ellipse cx="350" cy="127" rx="5" ry="8" fill="#333"/>
  <ellipse cx="350" cy="140" rx="5" ry="8" fill="#333"/>
  
  <!-- Headlights -->
  <ellipse cx="345" cy="120" rx="8" ry="4" fill="#fff" stroke="#ddd"/>
  <ellipse cx="345" cy="147" rx="8" ry="4" fill="#fff" stroke="#ddd"/>
  
  <!-- BMW logo area -->
  <circle cx="375" cy="133" r="12" fill="#0066cc" stroke="#fff" stroke-width="2"/>
  <text x="375" y="138" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-weight="bold" font-size="8">BMW</text>
  
  <!-- Model name -->
  <text x="{width//2}" y="{height-30}" text-anchor="middle" fill="#333" font-family="Arial, sans-serif" font-weight="bold" font-size="16">{model_name}</text>
  
  <!-- Car type -->
  <text x="{width//2}" y="{height-10}" text-anchor="middle" fill="#666" font-family="Arial, sans-serif" font-size="12">{car_type}</text>
</svg>'''
    
    return svg_content

def darker_color(hex_color: str) -> str:
    """Make a hex color darker"""
    # Remove # if present
    hex_color = hex_color.lstrip('#')
    
    # Convert to RGB
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    # Make darker (reduce by 30%)
    r = max(0, int(r * 0.7))
    g = max(0, int(g * 0.7))
    b = max(0, int(b * 0.7))
    
    return f"#{r:02x}{g:02x}{b:02x}"

def create_series_hero_image(series_name: str, width: int = 600, height: int = 300) -> str:
    """Create a hero image for a BMW series"""
    
    colors = {
        "SUVs": "#2c5aa0",
        "Sedans": "#1e3a5f", 
        "Coupes": "#8b0000",
        "Convertibles": "#ff6b35",
        "Electric": "#00a86b",
        "M Models": "#e74c3c"
    }
    
    color = colors.get(series_name, "#1e3a5f")
    
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{color};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{darker_color(color)};stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="{width}" height="{height}" fill="url(#bgGradient)"/>
  
  <!-- Grid pattern for modern look -->
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
  </pattern>
  <rect width="{width}" height="{height}" fill="url(#grid)"/>
  
  <!-- BMW logo -->
  <circle cx="50" cy="50" r="25" fill="#fff" stroke="none"/>
  <circle cx="50" cy="50" r="20" fill="#0066cc"/>
  <text x="50" y="57" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-weight="bold" font-size="12">BMW</text>
  
  <!-- Series title -->
  <text x="50" y="{height-80}" fill="white" font-family="Arial, sans-serif" font-weight="bold" font-size="28">{series_name}</text>
  <text x="50" y="{height-50}" fill="rgba(255,255,255,0.9)" font-family="Arial, sans-serif" font-size="16">The Ultimate Driving Machine</text>
  
  <!-- Decorative elements -->
  <polygon points="{width-100},50 {width-50},25 {width-50},75" fill="rgba(255,255,255,0.2)"/>
  <polygon points="{width-150},100 {width-100},75 {width-100},125" fill="rgba(255,255,255,0.1)"/>
</svg>'''
    
    return svg_content

def generate_all_images():
    """Generate all placeholder images for the BMW configurator"""
    
    # Model images by series
    models_by_series = {
        "SUVs": ["X1", "X2", "X3", "X4", "X5", "X6", "X7", "iX", "XM"],
        "Sedans": ["2 Series Gran Coupe", "3 Series", "4 Series Gran Coupe", "5 Series", "7 Series", "8 Series Gran Coupe", "i4", "i5", "i7"],
        "Coupes": ["2 Series", "4 Series", "8 Series", "M2", "M4"],
        "Convertibles": ["4 Series", "8 Series", "Z4", "M4", "M8"],
        "Electric": ["iX", "i4", "i5", "i7"],
        "M Models": ["M2", "M3", "M4", "M5", "M8", "X4 M", "X5 M", "X6 M", "XM"]
    }
    
    # Colors for different model types
    model_colors = {
        "X": "#2c5aa0",  # SUVs
        "3": "#1e3a5f",  # Sedans
        "5": "#1e3a5f",  # Sedans
        "7": "#2c3e50",  # Luxury sedans
        "i": "#00a86b",  # Electric
        "M": "#e74c3c",  # M Performance
        "Z": "#ff6b35"   # Roadsters
    }
    
    # Create series hero images
    for series_name in models_by_series.keys():
        hero_svg = create_series_hero_image(series_name)
        filename = f"static/images/bmw-{series_name.lower().replace(' ', '-')}.jpg"
        
        # Save as SVG (we'll rename to .jpg for compatibility)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(hero_svg)
        print(f"Created {filename}")
    
    # Create individual model images
    for series_name, models in models_by_series.items():
        for model in models:
            # Determine car type
            if "X" in model and model != "XM":
                car_type = "SUV"
            elif any(x in model for x in ["Gran Coupe", "Series"]) and "Coupe" not in model:
                car_type = "Sedan"
            elif "Convertible" in series_name or model in ["Z4"]:
                car_type = "Convertible"
            elif model.startswith("i") or "Electric" in series_name:
                car_type = "Electric"
            elif model.startswith("M") or "M " in model:
                car_type = "M Performance"
            else:
                car_type = "Coupe"
            
            # Choose color based on model
            color = "#1e3a5f"  # Default BMW blue
            for prefix, model_color in model_colors.items():
                if model.startswith(prefix):
                    color = model_color
                    break
            
            # Create different view angles
            views = ["front", "side", "rear", "interior"]
            for view in views:
                model_svg = create_svg_car_image(model, car_type, color)
                filename = f"static/images/{model.lower().replace(' ', '-')}-{view}.jpg"
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(model_svg)
                print(f"Created {filename}")
    
    # Create hero background image
    hero_bg_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="1200" height="600" viewBox="0 0 1200 600" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="heroGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0f4c75;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#1e3a5f;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#2c5aa0;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <rect width="1200" height="600" fill="url(#heroGradient)"/>
  
  <!-- Abstract car silhouettes in background -->
  <g opacity="0.1">
    <path d="M200,300 Q200,250 250,250 L400,250 Q450,250 450,300 L450,350 Q450,400 400,400 L250,400 Q200,400 200,350 Z" fill="white"/>
    <path d="M600,200 Q600,150 650,150 L800,150 Q850,150 850,200 L850,250 Q850,300 800,300 L650,300 Q600,300 600,250 Z" fill="white"/>
    <path d="M300,450 Q300,400 350,400 L500,400 Q550,400 550,450 L550,500 Q550,550 500,550 L350,550 Q300,550 300,500 Z" fill="white"/>
  </g>
  
  <!-- BMW logo pattern -->
  <g opacity="0.2">
    <circle cx="100" cy="100" r="30" fill="white"/>
    <circle cx="1100" cy="500" r="25" fill="white"/>
    <circle cx="900" cy="150" r="20" fill="white"/>
  </g>
</svg>'''
    
    with open("static/images/bmw-hero-bg.jpg", 'w', encoding='utf-8') as f:
        f.write(hero_bg_svg)
    print("Created static/images/bmw-hero-bg.jpg")
    
    print(f"\nGenerated images for {sum(len(models) for models in models_by_series.values())} models")
    print("Note: Images are saved as SVG content in .jpg files for web compatibility")

if __name__ == "__main__":
    generate_all_images()
