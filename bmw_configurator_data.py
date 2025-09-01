"""
BMW Configurator Data with Real Constraints
Based on actual BMW USA configurator data and constraints
"""

import json
from typing import Dict, List, Any

class BMWConfiguratorData:
    """Comprehensive BMW configurator data with real constraints"""
    
    def __init__(self):
        self.models_data = self._load_models_data()
        self.constraints = self._load_constraints()
        self.pricing = self._load_pricing()
        self.packages = self._load_packages()
        
    def _load_models_data(self) -> Dict[str, Any]:
        """Load comprehensive model data with specifications"""
        return {
            "X1": {
                "name": "X1 xDrive28i",
                "category": "SUV",
                "base_price": 37500,
                "body_style": "Sports Activity Vehicle",
                "drivetrain": "xDrive (AWD)",
                "fuel_economy": {"city": 22, "highway": 30, "combined": 25},
                "dimensions": {
                    "length": 185.0, "width": 73.0, "height": 66.0,
                    "wheelbase": 112.0, "cargo": 27.1
                },
                "performance": {
                    "acceleration": "6.6 seconds (0-60 mph)",
                    "top_speed": "130 mph",
                    "power": "228 hp",
                    "torque": "258 lb-ft"
                },
                "available_engines": ["B48_2_0T"],
                "available_drivetrains": ["xDrive"],
                "trim_levels": ["xDrive28i", "M35i"]
            },
            "X3": {
                "name": "X3 xDrive30i",
                "category": "SUV", 
                "base_price": 45000,
                "body_style": "Sports Activity Vehicle",
                "drivetrain": "xDrive (AWD)",
                "fuel_economy": {"city": 23, "highway": 29, "combined": 26},
                "dimensions": {
                    "length": 185.9, "width": 74.4, "height": 66.0,
                    "wheelbase": 112.8, "cargo": 28.7
                },
                "performance": {
                    "acceleration": "6.0 seconds (0-60 mph)",
                    "top_speed": "130 mph", 
                    "power": "248 hp",
                    "torque": "258 lb-ft"
                },
                "available_engines": ["B48_2_0T", "B58_3_0T"],
                "available_drivetrains": ["xDrive"],
                "trim_levels": ["xDrive30i", "M40i", "M"]
            },
            "X5": {
                "name": "X5 xDrive40i",
                "category": "SUV",
                "base_price": 62000,
                "body_style": "Sports Activity Vehicle",
                "drivetrain": "xDrive (AWD)",
                "fuel_economy": {"city": 20, "highway": 26, "combined": 23},
                "dimensions": {
                    "length": 194.3, "width": 78.9, "height": 69.4,
                    "wheelbase": 117.1, "cargo": 33.9
                },
                "performance": {
                    "acceleration": "5.5 seconds (0-60 mph)",
                    "top_speed": "130 mph",
                    "power": "335 hp", 
                    "torque": "330 lb-ft"
                },
                "available_engines": ["B58_3_0T", "N63_4_4T_V8", "S63_4_4T_V8"],
                "available_drivetrains": ["xDrive"],
                "trim_levels": ["xDrive40i", "xDrive50e", "M50i", "M60i", "M"]
            },
            "3 Series": {
                "name": "330i xDrive Sedan",
                "category": "Sedan",
                "base_price": 35000,
                "body_style": "Sedan",
                "drivetrain": "RWD/xDrive",
                "fuel_economy": {"city": 26, "highway": 36, "combined": 30},
                "dimensions": {
                    "length": 185.7, "width": 71.9, "height": 56.8,
                    "wheelbase": 112.2, "cargo": 17.0
                },
                "performance": {
                    "acceleration": "5.6 seconds (0-60 mph)",
                    "top_speed": "130 mph",
                    "power": "255 hp",
                    "torque": "295 lb-ft"
                },
                "available_engines": ["B48_2_0T", "B58_3_0T"],
                "available_drivetrains": ["RWD", "xDrive"],
                "trim_levels": ["330i", "330i xDrive", "M340i", "M340i xDrive", "M3"]
            },
            "5 Series": {
                "name": "530i xDrive Sedan",
                "category": "Sedan",
                "base_price": 55000,
                "body_style": "Sedan",
                "drivetrain": "RWD/xDrive",
                "fuel_economy": {"city": 25, "highway": 33, "combined": 28},
                "dimensions": {
                    "length": 195.0, "width": 73.0, "height": 58.0,
                    "wheelbase": 117.1, "cargo": 18.7
                },
                "performance": {
                    "acceleration": "6.0 seconds (0-60 mph)",
                    "top_speed": "130 mph",
                    "power": "248 hp",
                    "torque": "258 lb-ft"
                },
                "available_engines": ["B48_2_0T", "B58_3_0T", "N63_4_4T_V8"],
                "available_drivetrains": ["RWD", "xDrive"],
                "trim_levels": ["530i", "530i xDrive", "540i", "540i xDrive", "M550i xDrive", "M5"]
            },
            "7 Series": {
                "name": "740i xDrive Sedan", 
                "category": "Sedan",
                "base_price": 88000,
                "body_style": "Sedan",
                "drivetrain": "xDrive (AWD)",
                "fuel_economy": {"city": 21, "highway": 29, "combined": 24},
                "dimensions": {
                    "length": 206.6, "width": 75.0, "height": 59.1,
                    "wheelbase": 126.4, "cargo": 18.2
                },
                "performance": {
                    "acceleration": "5.3 seconds (0-60 mph)",
                    "top_speed": "130 mph",
                    "power": "335 hp",
                    "torque": "330 lb-ft"
                },
                "available_engines": ["B58_3_0T", "N63_4_4T_V8"],
                "available_drivetrains": ["xDrive"],
                "trim_levels": ["740i xDrive", "750i xDrive", "M760i xDrive"]
            },
            "M3": {
                "name": "M3 Competition",
                "category": "M Performance", 
                "base_price": 72000,
                "body_style": "Sedan",
                "drivetrain": "RWD/xDrive",
                "fuel_economy": {"city": 16, "highway": 23, "combined": 19},
                "dimensions": {
                    "length": 185.7, "width": 71.9, "height": 56.8,
                    "wheelbase": 112.2, "cargo": 17.0
                },
                "performance": {
                    "acceleration": "3.8 seconds (0-60 mph)",
                    "top_speed": "180 mph",
                    "power": "473 hp",
                    "torque": "406 lb-ft"
                },
                "available_engines": ["S58_3_0T"],
                "available_drivetrains": ["RWD", "xDrive"],
                "trim_levels": ["Competition", "Competition xDrive"]
            },
            "M5": {
                "name": "M5 Competition",
                "category": "M Performance",
                "base_price": 105000,
                "body_style": "Sedan",
                "drivetrain": "xDrive (AWD)",
                "fuel_economy": {"city": 15, "highway": 21, "combined": 17},
                "dimensions": {
                    "length": 195.0, "width": 73.0, "height": 58.0,
                    "wheelbase": 117.1, "cargo": 18.7
                },
                "performance": {
                    "acceleration": "3.1 seconds (0-60 mph)",
                    "top_speed": "190 mph",
                    "power": "617 hp",
                    "torque": "553 lb-ft"
                },
                "available_engines": ["S63_4_4T_V8"],
                "available_drivetrains": ["xDrive"],
                "trim_levels": ["Competition xDrive"]
            },
            "i4": {
                "name": "i4 eDrive40",
                "category": "Electric",
                "base_price": 52000,
                "body_style": "Gran Coupe",
                "drivetrain": "RWD/AWD Electric",
                "fuel_economy": {"city": 129, "highway": 108, "combined": 119}, # MPGe
                "dimensions": {
                    "length": 185.7, "width": 71.9, "height": 56.8,
                    "wheelbase": 112.2, "cargo": 17.0
                },
                "performance": {
                    "acceleration": "5.7 seconds (0-60 mph)",
                    "top_speed": "118 mph",
                    "power": "335 hp",
                    "torque": "317 lb-ft"
                },
                "available_engines": ["Electric_Single_Motor", "Electric_Dual_Motor"],
                "available_drivetrains": ["RWD", "AWD"],
                "trim_levels": ["eDrive40", "M50"],
                "battery_range": {"eDrive40": 270, "M50": 227} # miles
            },
            "iX": {
                "name": "iX xDrive50",
                "category": "Electric SUV",
                "base_price": 85000,
                "body_style": "Sports Activity Vehicle",
                "drivetrain": "AWD Electric",
                "fuel_economy": {"city": 105, "highway": 96, "combined": 100}, # MPGe
                "dimensions": {
                    "length": 195.0, "width": 77.4, "height": 68.7,
                    "wheelbase": 118.1, "cargo": 35.5
                },
                "performance": {
                    "acceleration": "4.6 seconds (0-60 mph)",
                    "top_speed": "124 mph",
                    "power": "516 hp",
                    "torque": "564 lb-ft"
                },
                "available_engines": ["Electric_Dual_Motor"],
                "available_drivetrains": ["AWD"],
                "trim_levels": ["xDrive50", "M70"],
                "battery_range": {"xDrive50": 324, "M70": 280} # miles
            }
        }
    
    def _load_constraints(self) -> Dict[str, Any]:
        """Load realistic BMW option constraints"""
        return {
            "engine_drivetrain_constraints": {
                # Only certain engines work with certain drivetrains
                "B48_2_0T": ["RWD", "xDrive"],  # 2.0L turbo 4-cyl
                "B58_3_0T": ["RWD", "xDrive"],  # 3.0L turbo 6-cyl
                "N63_4_4T_V8": ["xDrive"],      # 4.4L twin-turbo V8
                "S63_4_4T_V8": ["xDrive"],      # M 4.4L twin-turbo V8
                "S58_3_0T": ["RWD", "xDrive"],  # M 3.0L twin-turbo 6-cyl
                "Electric_Single_Motor": ["RWD"],
                "Electric_Dual_Motor": ["AWD"]
            },
            
            "package_dependencies": {
                # Packages that require other packages
                "Executive_Package": ["Premium_Package"],
                "M_Performance_Package": ["M_Sport_Package"],
                "Driver_Assistance_Professional": ["Driver_Assistance_Package"],
                "Individual_Interior": ["Premium_Package"],
                "Bang_Olufsen_Audio": ["Premium_Package"]
            },
            
            "incompatible_options": [
                # Options that cannot be selected together
                {"options": ["Sunroof", "Carbon_Fiber_Roof"], "reason": "Physical conflict"},
                {"options": ["19_Inch_Wheels", "Run_Flat_Tires"], "reason": "Not available with this wheel size"},
                {"options": ["M_Sport_Package", "Comfort_Package"], "reason": "Different suspension types"},
                {"options": ["Individual_Paint", "M_Paint"], "reason": "Different paint categories"},
                {"options": ["Ventilated_Seats", "Base_Interior"], "reason": "Requires premium interior"},
                {"options": ["HUD", "Base_Interior"], "reason": "Requires technology package"},
                {"options": ["Adaptive_LED", "Base_Lighting"], "reason": "Lighting upgrade conflict"},
                {"options": ["Sport_Exhaust", "Electric_Motor"], "reason": "Electric vehicles don't have exhaust"}
            ],
            
            "required_combinations": [
                # When selecting A, must also select B
                {"base": "M_Sport_Package", "requires": ["Sport_Suspension"], "reason": "M Sport requires sport suspension"},
                {"base": "Competition_Package", "requires": ["M_Sport_Package"], "reason": "Competition builds on M Sport"},
                {"base": "Carbon_Fiber_Interior", "requires": ["Individual_Interior"], "reason": "Carbon fiber requires Individual interior"},
                {"base": "Track_Package", "requires": ["Performance_Tires", "M_Sport_Brakes"], "reason": "Track package requires performance components"},
                {"base": "Cold_Weather_Package", "requires": ["Heated_Seats"], "reason": "Cold weather includes heated seats"},
                {"base": "Premium_Audio", "requires": ["Premium_Package"], "reason": "Audio upgrade requires premium package"}
            ],
            
            "model_specific_constraints": {
                "M3": {
                    "required_options": ["M_Sport_Package", "Performance_Tires"],
                    "excluded_options": ["Comfort_Package", "Run_Flat_Tires"],
                    "mandatory_packages": ["M_Competition_Package"]
                },
                "M5": {
                    "required_options": ["M_Sport_Package", "Performance_Tires", "Sport_Exhaust"],
                    "excluded_options": ["Comfort_Package", "Eco_Pro_Mode"],
                    "mandatory_packages": ["M_Competition_Package", "Executive_Package"]
                },
                "i4": {
                    "excluded_options": ["Sport_Exhaust", "Oil_Change_Service"],
                    "required_options": ["Electric_Charging_Package"],
                    "special_features": ["Charging_Cable", "BMW_Wallbox"]
                },
                "iX": {
                    "excluded_options": ["Sport_Exhaust", "Engine_Options"],
                    "required_options": ["Electric_Charging_Package"],
                    "special_features": ["Fast_Charging", "BMW_Wallbox", "Charging_Cable"]
                }
            },
            
            "regional_constraints": {
                # US market specific constraints
                "required_safety": ["Backup_Camera", "Tire_Pressure_Monitor"],
                "emissions_compliance": ["Catalytic_Converter", "OBD_II"],
                "lighting_requirements": ["Daytime_Running_Lights"]
            },
            
            "seasonal_availability": {
                # Some options only available certain times of year
                "Winter_Tires": {"available_months": [10, 11, 12, 1, 2, 3]},
                "Summer_Tires": {"available_months": [4, 5, 6, 7, 8, 9]},
                "Convertible_Top": {"production_months": [3, 4, 5, 6, 7, 8, 9, 10]}
            }
        }
    
    def _load_pricing(self) -> Dict[str, Any]:
        """Load comprehensive pricing data with real BMW pricing structure"""
        return {
            "engines": {
                "B48_2_0T": {"price": 0, "name": "2.0L TwinPower Turbo 4-Cylinder"},
                "B58_3_0T": {"price": 5000, "name": "3.0L TwinPower Turbo 6-Cylinder"},
                "N63_4_4T_V8": {"price": 12000, "name": "4.4L TwinTurbo V8"},
                "S63_4_4T_V8": {"price": 25000, "name": "M 4.4L TwinTurbo V8"},
                "S58_3_0T": {"price": 15000, "name": "M 3.0L TwinTurbo 6-Cylinder"},
                "Electric_Single_Motor": {"price": 0, "name": "Electric Motor"},
                "Electric_Dual_Motor": {"price": 8000, "name": "Dual Electric Motors"}
            },
            
            "drivetrains": {
                "RWD": {"price": 0, "name": "Rear-Wheel Drive"},
                "xDrive": {"price": 2000, "name": "Intelligent All-Wheel Drive"},
                "AWD": {"price": 2000, "name": "All-Wheel Drive (Electric)"}
            },
            
            "exterior_colors": {
                "Alpine_White": {"price": 0, "metallic": False},
                "Jet_Black": {"price": 550, "metallic": True},
                "Mineral_Grey": {"price": 550, "metallic": True},
                "Storm_Bay": {"price": 550, "metallic": True},
                "Phytonic_Blue": {"price": 550, "metallic": True},
                "Mineral_White": {"price": 550, "metallic": True},
                "Barcelona_Blue": {"price": 550, "metallic": True},
                "Sunset_Orange": {"price": 995, "metallic": True},
                "Individual_Paint": {"price": 5000, "metallic": True, "special": True}
            },
            
            "wheel_options": {
                "17_Inch_Style_512": {"price": 0, "size": 17, "style": "Standard"},
                "18_Inch_Style_848M": {"price": 800, "size": 18, "style": "M Sport"},
                "19_Inch_Style_849M": {"price": 1800, "size": 19, "style": "M Performance"},
                "20_Inch_Style_850M": {"price": 3200, "size": 20, "style": "M Performance"},
                "21_Inch_Individual": {"price": 4500, "size": 21, "style": "Individual"}
            },
            
            "interior_options": {
                "Sensatec_Black": {"price": 0, "material": "Synthetic Leather"},
                "Dakota_Black": {"price": 1450, "material": "Leather"},
                "Dakota_Cognac": {"price": 1450, "material": "Leather"},
                "Vernasca_Black": {"price": 1950, "material": "Premium Leather"},
                "Vernasca_Cognac": {"price": 1950, "material": "Premium Leather"},
                "Merino_Individual": {"price": 4500, "material": "Individual Leather"},
                "Full_Merino": {"price": 6000, "material": "Full Merino Leather"}
            },
            
            "packages": {
                "Premium_Package": {
                    "price": 3200,
                    "includes": ["Comfort_Access", "SiriusXM", "Auto_Dimming_Mirrors", "Universal_Garage_Opener"]
                },
                "Technology_Package": {
                    "price": 2200,
                    "includes": ["BMW_Live_Cockpit_Pro", "Navigation", "BMW_Assistant", "Wireless_CarPlay"]
                },
                "M_Sport_Package": {
                    "price": 3000,
                    "includes": ["M_Aerodynamics", "Sport_Suspension", "M_Steering_Wheel", "Sport_Seats"]
                },
                "Executive_Package": {
                    "price": 4800,
                    "includes": ["Comfort_Seats", "Four_Zone_Climate", "Soft_Close_Doors", "Ambient_Lighting"]
                },
                "Driver_Assistance_Package": {
                    "price": 1700,
                    "includes": ["Blind_Spot_Detection", "Lane_Departure_Warning", "Cross_Traffic_Alert"]
                },
                "Driver_Assistance_Professional": {
                    "price": 1900,
                    "includes": ["Active_Driving_Assistant", "Traffic_Jam_Assistant", "Steering_Assistant"]
                },
                "Cold_Weather_Package": {
                    "price": 1000,
                    "includes": ["Heated_Seats", "Heated_Steering_Wheel", "Heated_Mirrors"]
                },
                "Convenience_Package": {
                    "price": 1500,
                    "includes": ["Power_Tailgate", "Three_Zone_Climate", "Auto_High_Beams"]
                }
            },
            
            "individual_options": {
                "Sunroof": {"price": 1200},
                "Head_Up_Display": {"price": 1100},
                "Harman_Kardon_Audio": {"price": 875},
                "Bowers_Wilkins_Audio": {"price": 3200},
                "Adaptive_LED_Headlights": {"price": 1300},
                "Laser_Headlights": {"price": 1800},
                "Park_Distance_Control": {"price": 500},
                "Surround_View_Camera": {"price": 900},
                "Wireless_Charging": {"price": 500},
                "Remote_Start": {"price": 300},
                "Apple_CarPlay": {"price": 300},
                "Android_Auto": {"price": 300},
                "Gesture_Control": {"price": 600},
                "Massaging_Seats": {"price": 1200},
                "Ventilated_Seats": {"price": 800},
                "Carbon_Fiber_Trim": {"price": 1500},
                "Sport_Exhaust": {"price": 800},
                "M_Performance_Exhaust": {"price": 2200}
            }
        }
    
    def _load_packages(self) -> Dict[str, Any]:
        """Load detailed package information with dependencies"""
        return {
            "Premium_Package": {
                "name": "Premium Package",
                "price": 3200,
                "description": "Enhanced comfort and convenience features",
                "features": [
                    "Comfort Access Keyless Entry",
                    "SiriusXM Radio with 1-year subscription", 
                    "Auto-dimming interior and exterior mirrors",
                    "Universal garage-door opener",
                    "Power front seats with memory",
                    "Lumbar support"
                ],
                "models_available": ["X1", "X3", "X5", "3 Series", "5 Series", "7 Series"],
                "conflicts_with": [],
                "requires": []
            },
            
            "Technology_Package": {
                "name": "Technology Package", 
                "price": 2200,
                "description": "Advanced infotainment and navigation features",
                "features": [
                    "BMW Live Cockpit Professional",
                    "BMW Navigation System",
                    "BMW Intelligent Personal Assistant",
                    "Wireless Apple CarPlay",
                    "WiFi Hotspot Preparation",
                    "Remote Services"
                ],
                "models_available": ["X1", "X3", "X5", "3 Series", "5 Series"],
                "conflicts_with": [],
                "requires": []
            },
            
            "M_Sport_Package": {
                "name": "M Sport Package",
                "price": 3000,
                "description": "Enhanced sporty appearance and handling",
                "features": [
                    "M Aerodynamics Package",
                    "M Sport Suspension",
                    "M Sport Steering Wheel",
                    "Sport Seats",
                    "Anthracite Headliner",
                    "Shadow Line Exterior Trim"
                ],
                "models_available": ["X1", "X3", "X5", "3 Series", "5 Series"],
                "conflicts_with": ["Comfort_Package"],
                "requires": ["Sport_Suspension"]
            },
            
            "Executive_Package": {
                "name": "Executive Package",
                "price": 4800,
                "description": "Premium luxury and comfort features",
                "features": [
                    "Comfort seats with massage function",
                    "Four-zone automatic climate control",
                    "Soft-close automatic doors",
                    "Ambient lighting",
                    "Power rear window sunshade",
                    "Rear seat adjustability"
                ],
                "models_available": ["5 Series", "7 Series"],
                "conflicts_with": [],
                "requires": ["Premium_Package"]
            },
            
            "Driver_Assistance_Package": {
                "name": "Driving Assistance Package",
                "price": 1700,
                "description": "Enhanced safety and driver assistance features",
                "features": [
                    "Active Blind Spot Detection",
                    "Lane Departure Warning",
                    "Rear Cross-Traffic Alert",
                    "Park Distance Control",
                    "Speed Limit Information"
                ],
                "models_available": ["X1", "X3", "X5", "3 Series", "5 Series", "7 Series"],
                "conflicts_with": [],
                "requires": []
            },
            
            "Driver_Assistance_Professional": {
                "name": "Driving Assistance Professional Package", 
                "price": 1900,
                "description": "Advanced semi-autonomous driving features",
                "features": [
                    "Active Driving Assistant Pro",
                    "Traffic Jam Assistant", 
                    "Extended Traffic Jam Assistant",
                    "Steering and Lane Control Assistant",
                    "Active Lane Keeping Assistant"
                ],
                "models_available": ["X3", "X5", "3 Series", "5 Series", "7 Series"],
                "conflicts_with": [],
                "requires": ["Driver_Assistance_Package"]
            },
            
            "Cold_Weather_Package": {
                "name": "Cold Weather Package",
                "price": 1000, 
                "description": "Features for winter driving comfort",
                "features": [
                    "Heated front seats",
                    "Heated steering wheel",
                    "Heated exterior mirrors",
                    "Headlight washers"
                ],
                "models_available": ["X1", "X3", "X5", "3 Series", "5 Series"],
                "conflicts_with": [],
                "requires": []
            }
        }
    
    def get_model_data(self, model_name: str) -> Dict[str, Any]:
        """Get comprehensive data for a specific model"""
        return self.models_data.get(model_name, {})
    
    def get_available_options(self, model_name: str) -> Dict[str, Any]:
        """Get all available options for a model with pricing and constraints"""
        model_data = self.get_model_data(model_name)
        if not model_data:
            return {}
            
        available_options = {
            "engines": {},
            "drivetrains": {},
            "exterior_colors": self.pricing["exterior_colors"],
            "wheels": self.pricing["wheel_options"],
            "interior": self.pricing["interior_options"],
            "packages": {},
            "individual_options": self.pricing["individual_options"],
            "constraints": self.get_model_constraints(model_name)
        }
        
        # Filter engines available for this model
        for engine in model_data.get("available_engines", []):
            if engine in self.pricing["engines"]:
                available_options["engines"][engine] = self.pricing["engines"][engine]
        
        # Filter drivetrains available for this model
        for drivetrain in model_data.get("available_drivetrains", []):
            if drivetrain in self.pricing["drivetrains"]:
                available_options["drivetrains"][drivetrain] = self.pricing["drivetrains"][drivetrain]
        
        # Filter packages available for this model
        for package_name, package_data in self.packages.items():
            if model_name in package_data.get("models_available", []):
                available_options["packages"][package_name] = package_data
        
        return available_options
    
    def get_model_constraints(self, model_name: str) -> Dict[str, Any]:
        """Get all constraints that apply to a specific model"""
        base_constraints = {
            "engine_drivetrain": self.constraints["engine_drivetrain_constraints"],
            "package_dependencies": self.constraints["package_dependencies"],
            "incompatible_options": self.constraints["incompatible_options"],
            "required_combinations": self.constraints["required_combinations"],
            "regional_constraints": self.constraints["regional_constraints"]
        }
        
        # Add model-specific constraints
        if model_name in self.constraints["model_specific_constraints"]:
            base_constraints["model_specific"] = self.constraints["model_specific_constraints"][model_name]
        
        return base_constraints
    
    def validate_configuration(self, model_name: str, configuration: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a configuration against all constraints"""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "suggestions": []
        }
        
        constraints = self.get_model_constraints(model_name)
        
        # Validate engine/drivetrain compatibility
        selected_engine = configuration.get("engine")
        selected_drivetrain = configuration.get("drivetrain")
        
        if selected_engine and selected_drivetrain:
            compatible_drivetrains = constraints["engine_drivetrain"].get(selected_engine, [])
            if selected_drivetrain not in compatible_drivetrains:
                validation_result["valid"] = False
                validation_result["errors"].append({
                    "type": "engine_drivetrain_incompatible",
                    "message": f"Engine {selected_engine} is not compatible with {selected_drivetrain}",
                    "available_drivetrains": compatible_drivetrains
                })
        
        # Validate package dependencies
        selected_packages = [k for k, v in configuration.items() if k.endswith("_Package") and v]
        for package in selected_packages:
            if package in constraints["package_dependencies"]:
                required_packages = constraints["package_dependencies"][package]
                missing_packages = [req for req in required_packages if not configuration.get(req)]
                if missing_packages:
                    validation_result["valid"] = False
                    validation_result["errors"].append({
                        "type": "missing_required_packages",
                        "message": f"Package {package} requires: {', '.join(missing_packages)}",
                        "missing_packages": missing_packages
                    })
        
        # Check incompatible options
        selected_options = [k for k, v in configuration.items() if v]
        for constraint in constraints["incompatible_options"]:
            conflicting_options = [opt for opt in constraint["options"] if opt in selected_options]
            if len(conflicting_options) > 1:
                validation_result["valid"] = False
                validation_result["errors"].append({
                    "type": "incompatible_options",
                    "message": f"Cannot select {' and '.join(conflicting_options)}: {constraint['reason']}",
                    "conflicting_options": conflicting_options
                })
        
        # Check required combinations
        for requirement in constraints["required_combinations"]:
            if configuration.get(requirement["base"]):
                missing_required = [req for req in requirement["requires"] if not configuration.get(req)]
                if missing_required:
                    validation_result["valid"] = False
                    validation_result["errors"].append({
                        "type": "missing_required_options",
                        "message": f"{requirement['base']} requires: {', '.join(missing_required)}",
                        "missing_options": missing_required,
                        "reason": requirement["reason"]
                    })
        
        # Model-specific validations
        if "model_specific" in constraints:
            model_constraints = constraints["model_specific"]
            
            # Check required options for this model
            if "required_options" in model_constraints:
                missing_required = [opt for opt in model_constraints["required_options"] 
                                  if not configuration.get(opt)]
                if missing_required:
                    validation_result["valid"] = False
                    validation_result["errors"].append({
                        "type": "model_required_options",
                        "message": f"{model_name} requires: {', '.join(missing_required)}",
                        "missing_options": missing_required
                    })
            
            # Check excluded options for this model
            if "excluded_options" in model_constraints:
                conflicting_options = [opt for opt in model_constraints["excluded_options"]
                                     if configuration.get(opt)]
                if conflicting_options:
                    validation_result["valid"] = False
                    validation_result["errors"].append({
                        "type": "model_excluded_options", 
                        "message": f"{model_name} cannot have: {', '.join(conflicting_options)}",
                        "conflicting_options": conflicting_options
                    })
        
        # Add suggestions for popular combinations
        self._add_configuration_suggestions(model_name, configuration, validation_result)
        
        return validation_result
    
    def _add_configuration_suggestions(self, model_name: str, configuration: Dict[str, Any], result: Dict[str, Any]):
        """Add helpful suggestions for configuration optimization"""
        
        # Suggest popular package combinations
        if configuration.get("Premium_Package") and not configuration.get("Technology_Package"):
            result["suggestions"].append({
                "type": "package_combo",
                "message": "Many customers add Technology Package with Premium Package for enhanced connectivity",
                "benefit": "Complete luxury and technology experience"
            })
        
        # Suggest M Sport for performance models
        if model_name in ["3 Series", "5 Series"] and not configuration.get("M_Sport_Package"):
            result["suggestions"].append({
                "type": "performance_enhancement",
                "message": "Consider M Sport Package for enhanced driving dynamics and appearance",
                "benefit": "Sportier driving experience and resale value"
            })
        
        # Suggest winter package in certain regions
        result["suggestions"].append({
            "type": "seasonal",
            "message": "Cold Weather Package recommended for northern climates",
            "benefit": "Enhanced comfort during winter months"
        })
        
        # Suggest driver assistance for family vehicles
        if model_name in ["X1", "X3", "X5"] and not configuration.get("Driver_Assistance_Package"):
            result["suggestions"].append({
                "type": "safety",
                "message": "Driver Assistance Package adds important safety features for family vehicles",
                "benefit": "Enhanced safety and peace of mind"
            })
    
    def calculate_total_price(self, model_name: str, configuration: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comprehensive pricing breakdown"""
        model_data = self.get_model_data(model_name)
        base_price = model_data.get("base_price", 50000)
        
        breakdown = {
            "base_price": base_price,
            "engine_upgrade": 0,
            "drivetrain_upgrade": 0,
            "exterior_options": 0,
            "interior_options": 0,
            "packages": 0,
            "individual_options": 0,
            "subtotal": base_price,
            "package_discount": 0,
            "destination_fee": 995,
            "total_msrp": 0,
            "estimated_taxes": 0,
            "estimated_total": 0,
            "itemized_breakdown": []
        }
        
        # Calculate engine upgrade cost
        selected_engine = configuration.get("engine")
        if selected_engine and selected_engine in self.pricing["engines"]:
            engine_cost = self.pricing["engines"][selected_engine]["price"]
            breakdown["engine_upgrade"] = engine_cost
            if engine_cost > 0:
                breakdown["itemized_breakdown"].append({
                    "item": self.pricing["engines"][selected_engine]["name"],
                    "price": engine_cost,
                    "category": "Engine"
                })
        
        # Calculate drivetrain upgrade cost
        selected_drivetrain = configuration.get("drivetrain")
        if selected_drivetrain and selected_drivetrain in self.pricing["drivetrains"]:
            drivetrain_cost = self.pricing["drivetrains"][selected_drivetrain]["price"]
            breakdown["drivetrain_upgrade"] = drivetrain_cost
            if drivetrain_cost > 0:
                breakdown["itemized_breakdown"].append({
                    "item": self.pricing["drivetrains"][selected_drivetrain]["name"],
                    "price": drivetrain_cost,
                    "category": "Drivetrain"
                })
        
        # Calculate exterior options
        selected_color = configuration.get("exterior_color")
        if selected_color and selected_color in self.pricing["exterior_colors"]:
            color_cost = self.pricing["exterior_colors"][selected_color]["price"]
            breakdown["exterior_options"] += color_cost
            if color_cost > 0:
                breakdown["itemized_breakdown"].append({
                    "item": f"{selected_color.replace('_', ' ')} Paint",
                    "price": color_cost,
                    "category": "Exterior"
                })
        
        selected_wheels = configuration.get("wheels")
        if selected_wheels and selected_wheels in self.pricing["wheel_options"]:
            wheel_cost = self.pricing["wheel_options"][selected_wheels]["price"]
            breakdown["exterior_options"] += wheel_cost
            if wheel_cost > 0:
                breakdown["itemized_breakdown"].append({
                    "item": selected_wheels.replace("_", " "),
                    "price": wheel_cost,
                    "category": "Exterior"
                })
        
        # Calculate interior options
        selected_interior = configuration.get("interior")
        if selected_interior and selected_interior in self.pricing["interior_options"]:
            interior_cost = self.pricing["interior_options"][selected_interior]["price"]
            breakdown["interior_options"] = interior_cost
            if interior_cost > 0:
                breakdown["itemized_breakdown"].append({
                    "item": selected_interior.replace("_", " "),
                    "price": interior_cost,
                    "category": "Interior"
                })
        
        # Calculate packages
        selected_packages = [k for k, v in configuration.items() if k.endswith("_Package") and v]
        for package in selected_packages:
            if package in self.pricing["packages"]:
                package_cost = self.pricing["packages"][package]["price"]
                breakdown["packages"] += package_cost
                breakdown["itemized_breakdown"].append({
                    "item": package.replace("_", " "),
                    "price": package_cost,
                    "category": "Package"
                })
        
        # Calculate individual options
        for option, selected in configuration.items():
            if selected and option in self.pricing["individual_options"]:
                option_cost = self.pricing["individual_options"][option]["price"]
                breakdown["individual_options"] += option_cost
                breakdown["itemized_breakdown"].append({
                    "item": option.replace("_", " "),
                    "price": option_cost,
                    "category": "Option"
                })
        
        # Calculate package discounts
        package_discount = self._calculate_package_discounts(selected_packages)
        breakdown["package_discount"] = package_discount
        
        # Calculate totals
        breakdown["subtotal"] = (base_price + breakdown["engine_upgrade"] + 
                               breakdown["drivetrain_upgrade"] + breakdown["exterior_options"] +
                               breakdown["interior_options"] + breakdown["packages"] + 
                               breakdown["individual_options"] - package_discount)
        
        breakdown["total_msrp"] = breakdown["subtotal"] + breakdown["destination_fee"]
        breakdown["estimated_taxes"] = breakdown["total_msrp"] * 0.08  # 8% estimated tax
        breakdown["estimated_total"] = breakdown["total_msrp"] + breakdown["estimated_taxes"]
        
        return breakdown
    
    def _calculate_package_discounts(self, selected_packages: List[str]) -> float:
        """Calculate discounts for package combinations"""
        discount = 0
        
        # Popular package combinations
        if "Premium_Package" in selected_packages and "Technology_Package" in selected_packages:
            discount += 500  # $500 discount for popular combo
        
        if "M_Sport_Package" in selected_packages and len([p for p in selected_packages if "M_" in p]) >= 2:
            discount += 300  # Additional M package discount
        
        if len(selected_packages) >= 3:
            discount += 200  # Multi-package discount
            
        return discount

# Create global instance
bmw_data = BMWConfiguratorData()
