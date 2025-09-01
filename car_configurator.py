import json
import logging
from typing import Dict, List, Any
from bmw_configurator_data import bmw_data

logger = logging.getLogger(__name__)

class CarConfigurator:
    def __init__(self):
        self.constraints = self._load_constraints()
        self.pricing = self._load_pricing()

    def _load_constraints(self):
        """Load configuration constraints"""
        return {
            "incompatible_options": [
                # Engine and package constraints
                {"options": ["base_engine", "m_sport_package"], "rule": "M Sport requires upgraded engine"},
                {"options": ["electric_motor", "gasoline_engine"], "rule": "Cannot combine electric and gasoline"},
                
                # Color and trim constraints
                {"options": ["light_interior", "dark_wheels"], "rule": "Color combination not recommended"},
                
                # Package constraints
                {"options": ["basic_tech", "premium_tech"], "rule": "Cannot select multiple tech packages"}
            ],
            "required_combinations": [
                {"base": "premium_package", "requires": ["comfort_access"], "rule": "Premium package requires comfort access"},
                {"base": "m_sport_package", "requires": ["sport_suspension"], "rule": "M Sport requires sport suspension"}
            ]
        }

    def _load_pricing(self):
        """Load pricing information"""
        return {
            "base_prices": {
                "X1": 37500,
                "X3": 45000,
                "X5": 62000,
                "3 Series": 35000,
                "5 Series": 55000,
                "7 Series": 88000
            },
            "option_prices": {
                "premium_package": 3200,
                "technology_package": 2200,
                "m_sport_package": 3000,
                "sunroof": 1200,
                "premium_audio": 875
            }
        }

    def validate_configuration(self, model: str, configuration: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a car configuration for conflicts and constraints"""
        try:
            # Use comprehensive validation from bmw_data
            return bmw_data.validate_configuration(model, configuration)

        except Exception as e:
            logger.error(f"Error validating configuration: {e}")
            return {
                "valid": False,
                "errors": [{"type": "validation_error", "message": "Configuration validation failed"}],
                "warnings": [],
                "suggestions": []
            }

    def _add_warnings_and_suggestions(self, configuration: Dict[str, Any], result: Dict[str, Any]):
        """Add warnings and suggestions to validation result"""
        # Check for common optimizations
        if configuration.get("premium_package") and not configuration.get("technology_package"):
            result["suggestions"].append({
                "type": "package_combo",
                "message": "Consider adding Technology Package for enhanced connectivity features",
                "savings": "Save $500 when combined with Premium Package"
            })

        # Check for color combinations
        if configuration.get("exterior_color") == "white" and configuration.get("interior_color") == "black":
            result["suggestions"].append({
                "type": "styling",
                "message": "Classic white exterior with black interior is a popular choice",
                "benefit": "High resale value combination"
            })

    def calculate_price(self, model: str, configuration: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate total price for the configuration"""
        try:
            # Use comprehensive pricing from bmw_data
            return bmw_data.calculate_total_price(model, configuration)

        except Exception as e:
            logger.error(f"Error calculating price: {e}")
            return {"error": "Price calculation failed"}

    def _calculate_package_discounts(self, configuration: Dict[str, Any]) -> float:
        """Calculate discounts for package combinations"""
        discount = 0
        
        # Premium + Technology package combo discount
        if configuration.get("premium_package") and configuration.get("technology_package"):
            discount += 500
        
        # M Sport package with performance options
        if configuration.get("m_sport_package") and configuration.get("performance_tires"):
            discount += 300
            
        return discount

    def get_recommendations(self, model: str, user_preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Get configuration recommendations based on user preferences"""
        try:
            recommendations = {
                "suggested_packages": [],
                "suggested_options": [],
                "color_combinations": [],
                "budget_optimizations": []
            }

            # Budget-based recommendations
            budget = user_preferences.get("budget", 50000)
            if budget > 60000:
                recommendations["suggested_packages"].extend([
                    "premium_package",
                    "technology_package",
                    "driver_assistance_professional"
                ])
            elif budget > 45000:
                recommendations["suggested_packages"].extend([
                    "technology_package",
                    "driver_assistance"
                ])

            # Usage-based recommendations
            usage = user_preferences.get("primary_use", "daily_driving")
            if usage == "performance":
                recommendations["suggested_packages"].append("m_sport_package")
                recommendations["suggested_options"].extend([
                    "sport_suspension",
                    "performance_tires"
                ])
            elif usage == "family":
                recommendations["suggested_options"].extend([
                    "sunroof",
                    "three_zone_climate",
                    "rear_entertainment"
                ])

            return recommendations

        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return {"error": "Failed to generate recommendations"}
