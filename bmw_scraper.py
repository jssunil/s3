import requests
from bs4 import BeautifulSoup
import json
import time
import logging
from bmw_configurator_data import bmw_data

logger = logging.getLogger(__name__)

class BMWDataScraper:
    def __init__(self):
        self.base_url = "https://www.bmwusa.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_all_series(self):
        """Get all BMW series data"""
        try:
            # BMW series data (based on the website structure)
            series_data = {
                "SUVs": {
                    "models": ["X1", "X2", "X3", "X4", "X5", "X6", "X7", "iX", "XM"],
                    "description": "BMW Sports Activity Vehicles",
                    "image": "/static/images/bmw-suvs.jpg"
                },
                "Sedans": {
                    "models": ["2 Series Gran Coupe", "3 Series", "4 Series Gran Coupe", "5 Series", "7 Series", "8 Series Gran Coupe", "i4", "i5", "i7"],
                    "description": "BMW Sedans & Gran Coupes",
                    "image": "/static/images/bmw-sedans.jpg"
                },
                "Coupes": {
                    "models": ["2 Series", "4 Series", "8 Series", "M2", "M4"],
                    "description": "BMW Coupes",
                    "image": "/static/images/bmw-coupes.jpg"
                },
                "Convertibles": {
                    "models": ["4 Series", "8 Series", "Z4", "M4", "M8"],
                    "description": "BMW Convertibles",
                    "image": "/static/images/bmw-convertibles.jpg"
                },
                "Electric": {
                    "models": ["iX", "i4", "i5", "i7"],
                    "description": "All-Electric BMW i Models",
                    "image": "/static/images/bmw-electric.jpg"
                },
                "M Models": {
                    "models": ["M2", "M3", "M4", "M5", "M8", "X4 M", "X5 M", "X6 M", "XM"],
                    "description": "BMW M Performance Models",
                    "image": "/static/images/bmw-m-models.jpg"
                }
            }
            
            return series_data
            
        except Exception as e:
            logger.error(f"Error fetching series data: {e}")
            return {}

    def get_models_for_series(self, series):
        """Get models for a specific series"""
        series_data = self.get_all_series()
        return series_data.get(series, {})

    def get_model_details(self, model):
        """Get detailed information for a specific model"""
        try:
            # Get model data from comprehensive dataset
            model_data = bmw_data.get_model_data(model)
            if not model_data:
                # Fallback to legacy method
                return self._get_legacy_model_details(model)
            
            model_details = {
                "name": model_data["name"],
                "base_price": model_data["base_price"],
                "category": model_data["category"],
                "body_style": model_data["body_style"],
                "drivetrain": model_data["drivetrain"],
                "fuel_economy": model_data["fuel_economy"],
                "performance": model_data["performance"],
                "dimensions": model_data["dimensions"],
                "images": self._get_model_images(model),
                "description": self._get_model_description(model),
                "available_engines": model_data.get("available_engines", []),
                "available_drivetrains": model_data.get("available_drivetrains", []),
                "trim_levels": model_data.get("trim_levels", [])
            }
            
            # Add electric-specific data if applicable
            if "battery_range" in model_data:
                model_details["battery_range"] = model_data["battery_range"]
            
            return model_details
            
        except Exception as e:
            logger.error(f"Error fetching model details for {model}: {e}")
            return {}

    def get_options_for_model(self, model):
        """Get all available options for a specific model"""
        try:
            # Get comprehensive options data with constraints
            options_data = bmw_data.get_available_options(model)
            if not options_data:
                # Fallback to legacy method
                return self._get_legacy_options(model)
            
            # Transform data for frontend compatibility
            formatted_options = {
                "engines": [
                    {
                        "name": engine_data["name"],
                        "power": "255 hp",  # Would be dynamic in real implementation
                        "torque": "295 lb-ft",
                        "price": engine_data["price"],
                        "fuel_type": "Gasoline" if "Electric" not in engine else "Electric",
                        "code": engine_code
                    }
                    for engine_code, engine_data in options_data.get("engines", {}).items()
                ],
                "drivetrains": [
                    {
                        "name": drivetrain_data["name"],
                        "price": drivetrain_data["price"],
                        "code": drivetrain_code
                    }
                    for drivetrain_code, drivetrain_data in options_data.get("drivetrains", {}).items()
                ],
                "exterior": {
                    "colors": [
                        {
                            "name": color_name.replace("_", " "),
                            "code": color_name,
                            "price": color_data["price"],
                            "metallic": color_data.get("metallic", False)
                        }
                        for color_name, color_data in options_data.get("exterior_colors", {}).items()
                    ],
                    "wheels": [
                        {
                            "name": wheel_name.replace("_", " "),
                            "price": wheel_data["price"],
                            "description": f"{wheel_data['size']}\" {wheel_data['style']}",
                            "code": wheel_name
                        }
                        for wheel_name, wheel_data in options_data.get("wheels", {}).items()
                    ]
                },
                "interior": {
                    "upholstery": [
                        {
                            "name": interior_name.replace("_", " "),
                            "price": interior_data["price"],
                            "color": "Black",  # Would be dynamic
                            "material": interior_data.get("material", "Unknown"),
                            "code": interior_name
                        }
                        for interior_name, interior_data in options_data.get("interior", {}).items()
                    ]
                },
                "packages": {
                    "all_packages": [
                        {
                            "name": package_data["name"],
                            "price": package_data["price"],
                            "features": package_data["features"],
                            "description": package_data.get("description", ""),
                            "code": package_name,
                            "conflicts_with": package_data.get("conflicts_with", []),
                            "requires": package_data.get("requires", [])
                        }
                        for package_name, package_data in options_data.get("packages", {}).items()
                    ]
                },
                "individual_options": [
                    {
                        "name": option_name.replace("_", " "),
                        "price": option_data["price"],
                        "category": "individual",
                        "code": option_name
                    }
                    for option_name, option_data in options_data.get("individual_options", {}).items()
                ],
                "constraints": options_data.get("constraints", {})
            }
            
            return formatted_options
            
        except Exception as e:
            logger.error(f"Error fetching options for {model}: {e}")
            return {}

    def _get_base_price(self, model):
        """Get base price for model"""
        # Sample pricing data
        base_prices = {
            "X1": 37500,
            "X3": 45000,
            "X5": 62000,
            "3 Series": 35000,
            "5 Series": 55000,
            "7 Series": 88000,
            "M3": 72000,
            "M5": 105000,
            "i4": 52000,
            "iX": 85000
        }
        return base_prices.get(model, 50000)

    def _get_engine_options(self, model):
        """Get engine options for model"""
        return [
            {
                "name": "2.0L TwinPower Turbo 4-Cylinder",
                "power": "255 hp",
                "torque": "295 lb-ft",
                "price": 0,
                "fuel_type": "Gasoline"
            },
            {
                "name": "3.0L TwinPower Turbo 6-Cylinder",
                "power": "382 hp",
                "torque": "365 lb-ft",
                "price": 5000,
                "fuel_type": "Gasoline"
            }
        ]

    def _get_exterior_colors(self, model):
        """Get exterior color options"""
        return [
            {"name": "Alpine White", "code": "300", "price": 0, "metallic": False},
            {"name": "Jet Black", "code": "668", "price": 550, "metallic": True},
            {"name": "Mineral Grey", "code": "C1M", "price": 550, "metallic": True},
            {"name": "Storm Bay", "code": "C2S", "price": 550, "metallic": True},
            {"name": "Phytonic Blue", "code": "C3S", "price": 550, "metallic": True},
            {"name": "Mineral White", "code": "283", "price": 550, "metallic": True}
        ]

    def _get_wheel_options(self, model):
        """Get wheel options"""
        return [
            {"name": "18\" Style 848M", "price": 0, "description": "Bicolor Jet Black"},
            {"name": "19\" Style 849M", "price": 1200, "description": "Bicolor Orbit Grey"},
            {"name": "20\" Style 850M", "price": 2400, "description": "Jet Black"}
        ]

    def _get_technology_packages(self, model):
        """Get technology package options"""
        return [
            {
                "name": "Premium Package",
                "price": 3200,
                "features": [
                    "SiriusXM Radio",
                    "Comfort Access Keyless Entry",
                    "Universal Garage-Door Opener",
                    "Auto-Dimming Mirrors"
                ]
            },
            {
                "name": "Technology Package",
                "price": 2200,
                "features": [
                    "BMW Live Cockpit Professional",
                    "Navigation System",
                    "BMW Intelligent Personal Assistant",
                    "Wireless Apple CarPlay"
                ]
            }
        ]

    def _get_comfort_packages(self, model):
        """Get comfort package options"""
        return [
            {
                "name": "Convenience Package",
                "price": 1500,
                "features": [
                    "Power Tailgate",
                    "3-Zone Automatic Climate Control",
                    "Heated Front Seats"
                ]
            }
        ]

    def _get_performance_packages(self, model):
        """Get performance package options"""
        return [
            {
                "name": "M Sport Package",
                "price": 3000,
                "features": [
                    "M Aerodynamics Package",
                    "M Sport Suspension",
                    "M Sport Steering Wheel",
                    "Sport Seats"
                ]
            }
        ]

    def _get_driver_assistance_packages(self, model):
        """Get driver assistance packages"""
        return [
            {
                "name": "Driving Assistance Package",
                "price": 1700,
                "features": [
                    "Active Blind Spot Detection",
                    "Lane Departure Warning",
                    "Rear Cross-Traffic Alert"
                ]
            },
            {
                "name": "Driving Assistance Professional Package",
                "price": 1900,
                "features": [
                    "Active Driving Assistant Pro",
                    "Traffic Jam Assistant",
                    "Extended Traffic Jam Assistant"
                ]
            }
        ]

    def _get_individual_options(self, model):
        """Get individual options"""
        return [
            {"name": "Sunroof", "price": 1200, "category": "comfort"},
            {"name": "Heated Steering Wheel", "price": 190, "category": "comfort"},
            {"name": "Wireless Charging", "price": 500, "category": "technology"},
            {"name": "Harman Kardon Surround Sound", "price": 875, "category": "entertainment"},
            {"name": "Head-Up Display", "price": 1100, "category": "technology"}
        ]

    def _get_upholstery_options(self, model):
        """Get upholstery options"""
        return [
            {"name": "Sensatec Synthetic Leather", "price": 0, "color": "Black"},
            {"name": "Dakota Leather", "price": 1450, "color": "Black"},
            {"name": "Dakota Leather", "price": 1450, "color": "Cognac"},
            {"name": "Vernasca Leather", "price": 1950, "color": "Black"}
        ]

    def _get_interior_trim(self, model):
        """Get interior trim options"""
        return [
            {"name": "Anthracite Wood", "price": 0},
            {"name": "Aluminum Hexagon", "price": 300},
            {"name": "Oak Grain", "price": 500}
        ]

    def _get_interior_colors(self, model):
        """Get interior color options"""
        return [
            {"name": "Black", "price": 0},
            {"name": "Oyster", "price": 0},
            {"name": "Cognac", "price": 0}
        ]

    def _get_exterior_trim(self, model):
        """Get exterior trim options"""
        return [
            {"name": "Standard", "price": 0},
            {"name": "Chrome", "price": 400},
            {"name": "High-gloss Shadow Line", "price": 600}
        ]

    def _get_fuel_economy(self, model):
        """Get fuel economy data"""
        return {
            "city": "22 mpg",
            "highway": "30 mpg",
            "combined": "25 mpg"
        }

    def _get_performance_specs(self, model):
        """Get performance specifications"""
        return {
            "acceleration": "5.6 seconds (0-60 mph)",
            "top_speed": "130 mph",
            "power": "255 hp",
            "torque": "295 lb-ft"
        }

    def _get_dimensions(self, model):
        """Get vehicle dimensions"""
        return {
            "length": "185.0 in",
            "width": "73.0 in",
            "height": "66.0 in",
            "wheelbase": "112.0 in",
            "cargo_capacity": "27.1 cu ft"
        }

    def _get_model_images(self, model):
        """Get model images"""
        return [
            f"/static/images/{model.lower().replace(' ', '-')}-front.jpg",
            f"/static/images/{model.lower().replace(' ', '-')}-side.jpg",
            f"/static/images/{model.lower().replace(' ', '-')}-rear.jpg",
            f"/static/images/{model.lower().replace(' ', '-')}-interior.jpg"
        ]

    def _get_model_description(self, model):
        """Get model description"""
        descriptions = {
            "X1": "The first-ever BMW X1 Sports Activity Vehicle combines the elevated seating position and versatility of a SAV with signature BMW driving dynamics.",
            "X3": "The BMW X3 Sports Activity Vehicle balances impressive capability with signature BMW performance and luxury.",
            "3 Series": "The BMW 3 Series represents the perfect balance of performance, luxury, and innovation in the sports sedan segment."
        }
        return descriptions.get(model, f"The BMW {model} delivers exceptional performance and luxury in its class.")

    def _get_legacy_model_details(self, model):
        """Legacy fallback method for model details"""
        return {
            "name": model,
            "base_price": self._get_base_price(model),
            "engine_options": self._get_engine_options(model),
            "fuel_economy": self._get_fuel_economy(model),
            "performance": self._get_performance_specs(model),
            "dimensions": self._get_dimensions(model),
            "images": self._get_model_images(model),
            "description": self._get_model_description(model)
        }

    def _get_legacy_options(self, model):
        """Legacy fallback method for options"""
        return {
            "exterior": {
                "colors": self._get_exterior_colors(model),
                "wheels": self._get_wheel_options(model),
                "trim": self._get_exterior_trim(model)
            },
            "interior": {
                "upholstery": self._get_upholstery_options(model),
                "trim": self._get_interior_trim(model),
                "colors": self._get_interior_colors(model)
            },
            "packages": {
                "technology": self._get_technology_packages(model),
                "comfort": self._get_comfort_packages(model),
                "performance": self._get_performance_packages(model),
                "driver_assistance": self._get_driver_assistance_packages(model)
            },
            "individual_options": self._get_individual_options(model)
        }