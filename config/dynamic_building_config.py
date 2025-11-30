"""
Dynamic Building Configuration Module
Loads and manages building templates and construction standards
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class RoomSpec:
    """Room specification with dynamic dimensions"""
    name: str
    area_percentage: float
    min_dimensions: Tuple[int, int]
    optimal_dimensions: Tuple[int, int]
    count: int = 1
    capacity: Optional[int] = None

@dataclass 
class BuildingSpec:
    """Complete building specification"""
    name: str
    category: str
    building_type: str
    total_area_range: Tuple[int, int]
    rooms: List[RoomSpec]
    features: List[str]
    construction_standard: str = "residential"
    region: str = "india"

class DynamicBuildingConfig:
    """Dynamic building configuration manager"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.building_templates = {}
        self.construction_standards = {}
        self.load_configurations()
    
    def load_configurations(self):
        """Load all configuration files"""
        try:
            # Load building templates
            templates_path = self.config_dir / "building_templates.json"
            if templates_path.exists():
                with open(templates_path, 'r') as f:
                    self.building_templates = json.load(f)
            
            # Load construction standards
            standards_path = self.config_dir / "construction_standards.json"
            if standards_path.exists():
                with open(standards_path, 'r') as f:
                    self.construction_standards = json.load(f)
                    
            logger.info("Dynamic building configurations loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load building configurations: {e}")
            self._load_fallback_config()
    
    def _load_fallback_config(self):
        """Load minimal fallback configuration"""
        self.building_templates = {
            "residential": {
                "2bhk": {
                    "total_area_range": [80, 120],
                    "rooms": {
                        "living_room": {"area_percentage": 25, "min_dimensions": [4000, 5000]},
                        "master_bedroom": {"area_percentage": 20, "min_dimensions": [3500, 4000]},
                        "second_bedroom": {"area_percentage": 15, "min_dimensions": [3000, 3500]},
                        "kitchen": {"area_percentage": 10, "min_dimensions": [2500, 3000]}
                    }
                }
            }
        }
        
        self.construction_standards = {
            "construction_standards": {
                "wall_thickness": {"residential": {"exterior": 250, "interior": 150}},
                "ceiling_height": {"residential": 3000}
            }
        }
    
    def parse_building_command(self, command: str) -> Optional[BuildingSpec]:
        """Parse user command and return appropriate building specification"""
        command_lower = command.lower()
        
        # Detect building category and type
        category, building_type = self._detect_building_type(command_lower)
        
        if not category or not building_type:
            return None
        
        # Get template
        template = self.building_templates.get(category, {}).get(building_type, {})
        if not template:
            return None
        
        # Extract user requirements
        area_requirements = self._extract_area_requirements(command_lower)
        custom_features = self._extract_custom_features(command_lower)
        region = self._extract_region(command_lower)
        
        # Build room specifications
        rooms = []
        for room_name, room_data in template.get("rooms", {}).items():
            room_spec = RoomSpec(
                name=room_name,
                area_percentage=room_data["area_percentage"],
                min_dimensions=tuple(room_data.get("min_dimensions", [3000, 3000])),
                optimal_dimensions=tuple(room_data.get("optimal_dimensions", [4000, 4000])),
                count=room_data.get("count", 1),
                capacity=room_data.get("capacity")
            )
            rooms.append(room_spec)
        
        # Create building specification
        building_spec = BuildingSpec(
            name=template.get("name", f"{category.title()} {building_type.title()}"),
            category=category,
            building_type=building_type,
            total_area_range=tuple(template.get("total_area_range", [100, 200])),
            rooms=rooms,
            features=template.get("features", []) + custom_features,
            construction_standard=category,
            region=region
        )
        
        return building_spec
    
    def _detect_building_type(self, command: str) -> Tuple[Optional[str], Optional[str]]:
        """Detect building category and type from command"""
        
        # Residential patterns
        if any(pattern in command for pattern in ['2bhk', '2 bhk', 'two bedroom']):
            return "residential", "2bhk"
        elif any(pattern in command for pattern in ['3bhk', '3 bhk', 'three bedroom']):
            return "residential", "3bhk"
        elif any(pattern in command for pattern in ['house', 'apartment', 'flat', 'home']):
            return "residential", "2bhk"  # Default residential
        
        # Educational patterns
        elif any(pattern in command for pattern in ['school', 'college', 'university', 'educational']):
            return "educational", "school"
        
        # Commercial patterns
        elif any(pattern in command for pattern in ['office', 'commercial', 'business']):
            return "commercial", "office"
        
        return None, None
    
    def _extract_area_requirements(self, command: str) -> Optional[int]:
        """Extract area requirements from command"""
        # Look for area mentions like "100 sqm", "1500 sq ft" etc.
        import re
        area_patterns = [
            r'(\d+)\s*(?:sq\.?\s*m|sqm|square\s*meter)',
            r'(\d+)\s*(?:sq\.?\s*ft|sqft|square\s*feet)',
        ]
        
        for pattern in area_patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        return None
    
    def _extract_custom_features(self, command: str) -> List[str]:
        """Extract custom features from command"""
        features = []
        
        feature_patterns = {
            'parking': ['parking', 'garage', 'car port'],
            'garden': ['garden', 'lawn', 'landscaping'],
            'pool': ['pool', 'swimming'],
            'balcony': ['balcony', 'terrace'],
            'basement': ['basement', 'cellar'],
            'attic': ['attic', 'loft'],
            'fireplace': ['fireplace', 'chimney']
        }
        
        for feature, patterns in feature_patterns.items():
            if any(pattern in command for pattern in patterns):
                features.append(feature)
        
        return features
    
    def _extract_region(self, command: str) -> str:
        """Extract regional building code requirements"""
        region_patterns = {
            'india': ['india', 'indian', 'mumbai', 'delhi', 'bangalore'],
            'usa': ['usa', 'america', 'us', 'new york', 'california'],
            'europe': ['europe', 'european', 'germany', 'france', 'uk']
        }
        
        for region, patterns in region_patterns.items():
            if any(pattern in command for pattern in patterns):
                return region
        
        return "india"  # Default
    
    def get_construction_standards(self, building_category: str, region: str = "india") -> Dict[str, Any]:
        """Get construction standards for building category and region"""
        standards = self.construction_standards.get("construction_standards", {})
        regional_codes = self.construction_standards.get("regional_codes", {}).get(region, {})
        
        # Merge standards with regional requirements
        result = {
            "wall_thickness": standards.get("wall_thickness", {}).get(building_category, {}),
            "ceiling_height": standards.get("ceiling_height", {}).get(building_category, 3000),
            "door_dimensions": standards.get("door_dimensions", {}),
            "window_dimensions": standards.get("window_dimensions", {}),
            "slab_thickness": standards.get("slab_thickness", {}).get(building_category, 150),
            "regional_requirements": regional_codes
        }
        
        return result
    
    def get_materials(self, material_type: str = "walls") -> Dict[str, Any]:
        """Get material specifications"""
        return self.construction_standards.get("materials", {}).get(material_type, {})
    
    def calculate_room_dimensions(self, room_spec: RoomSpec, total_area: int) -> Tuple[int, int, int]:
        """Calculate actual room dimensions based on total area"""
        room_area = (total_area * room_spec.area_percentage / 100) * 1000000  # Convert to mm²
        
        # Use optimal dimensions as target ratio
        target_width, target_length = room_spec.optimal_dimensions
        target_ratio = target_width / target_length
        
        # Calculate dimensions maintaining ratio
        length = int((room_area / target_ratio) ** 0.5)
        width = int(room_area / length)
        
        # Ensure minimum dimensions
        width = max(width, room_spec.min_dimensions[0])
        length = max(length, room_spec.min_dimensions[1])
        
        # Standard height based on building type (from construction standards)
        height = 3000  # Default, should be pulled from standards
        
        return width, length, height
    
    def get_intelligent_materials(self, building_spec: BuildingSpec, room_name: str) -> Dict[str, Any]:
        """Get intelligent material selection based on building type and room function"""
        
        materials = self.get_materials()
        
        # Material selection logic based on room function
        material_mapping = {
            "living_room": {
                "walls": "brick",
                "flooring": "ceramic",
                "color": (0.95, 0.92, 0.88)  # Warm white
            },
            "kitchen": {
                "walls": "concrete", 
                "flooring": "granite",
                "color": (0.9, 0.95, 0.9)  # Light green
            },
            "bathroom": {
                "walls": "concrete",
                "flooring": "ceramic",
                "color": (0.9, 0.9, 0.95)  # Light blue
            },
            "bedroom": {
                "walls": "brick",
                "flooring": "wood",
                "color": (0.95, 0.9, 0.85)  # Soft peach
            },
            "office": {
                "walls": "concrete",
                "flooring": "carpet",
                "color": (0.92, 0.92, 0.95)  # Professional gray
            },
            "classroom": {
                "walls": "brick",
                "flooring": "vinyl",
                "color": (0.95, 0.95, 0.9)  # Educational white
            }
        }
        
        # Get room-specific materials or default
        room_materials = material_mapping.get(room_name, {
            "walls": "brick",
            "flooring": "concrete", 
            "color": (0.9, 0.9, 0.9)
        })
        
        # Enhance with regional preferences
        if building_spec.region == "india":
            # Prefer locally available materials
            if room_materials["walls"] == "steel_frame":
                room_materials["walls"] = "brick"  # More common in India
        elif building_spec.region == "usa":
            # Modern materials preference
            if room_materials["walls"] == "brick" and building_spec.category == "commercial":
                room_materials["walls"] = "steel_frame"
        
        # Add material properties
        wall_material = materials.get("walls", {}).get(room_materials["walls"], {})
        
        return {
            "wall_material": room_materials["walls"],
            "wall_color": wall_material.get("color", room_materials["color"]),
            "flooring": room_materials["flooring"],
            "room_color": room_materials["color"],
            "thermal_properties": wall_material.get("thermal_conductivity", 1.0),
            "cost_factor": wall_material.get("cost_factor", 1.0)
        }

    def generate_dynamic_prompt(self, building_spec: BuildingSpec) -> str:
        
        standards = self.get_construction_standards(building_spec.category, building_spec.region)
        
        prompt = f"""Create a professional FreeCAD model for: {building_spec.name}

BUILDING SPECIFICATIONS:
- Category: {building_spec.category.title()}
- Type: {building_spec.building_type.upper()}
- Total Area: {building_spec.total_area_range[0]}-{building_spec.total_area_range[1]} sqm
- Region: {building_spec.region.title()}
- Construction Standard: {standards.get('regional_requirements', {}).get('building_code', 'Standard')}

CONSTRUCTION STANDARDS:
- Wall Thickness: Exterior {standards.get('wall_thickness', {}).get('exterior', 250)}mm, Interior {standards.get('wall_thickness', {}).get('interior', 150)}mm
- Ceiling Height: {standards.get('ceiling_height', 3000)}mm
- Door Size: {standards.get('door_dimensions', {}).get('standard', {}).get('width', 900)}mm x {standards.get('door_dimensions', {}).get('standard', {}).get('height', 2100)}mm
- Window Size: {standards.get('window_dimensions', {}).get('standard', {}).get('width', 1200)}mm x {standards.get('window_dimensions', {}).get('standard', {}).get('height', 1200)}mm

ROOMS REQUIRED:"""
        
        total_area = building_spec.total_area_range[1]  # Use max area for calculations
        
        for room in building_spec.rooms:
            width, length, height = self.calculate_room_dimensions(room, total_area)
            materials = self.get_intelligent_materials(building_spec, room.name)
            
            prompt += f"""
- {room.name.replace('_', ' ').title()}: {width}mm x {length}mm x {height}mm ({room.area_percentage}% of total area)
  * Material: {materials['wall_material'].title()} walls
  * Color: RGB{materials['wall_color']}
  * Flooring: {materials['flooring'].title()}"""
            
            if room.count > 1:
                prompt += f" (Quantity: {room.count})"
            if room.capacity:
                prompt += f" (Capacity: {room.capacity} persons)"

        if building_spec.features:
            prompt += f"\n\nSPECIAL FEATURES: {', '.join(building_spec.features)}"
        
        # Add regional compliance requirements
        regional_req = standards.get('regional_requirements', {})
        if regional_req.get('mandatory_features'):
            prompt += f"\nMANDATORY FEATURES ({building_spec.region.upper()}): {', '.join(regional_req['mandatory_features'])}"
        
        prompt += f"""

MATERIAL GUIDELINES:
- Use intelligent material selection based on room function
- Apply appropriate colors for each space type
- Consider thermal and structural properties
- Follow regional material availability and preferences

ARCHITECTURAL REQUIREMENTS:
- Create accurate structural model with proper proportions
- Include walls, doors, windows, and basic structural elements
- Ensure proper room connectivity and circulation
- Add foundation/slab and roof structure
- Use realistic joinery and construction details
- Follow accessibility standards where applicable

TECHNICAL REQUIREMENTS:
- Use FreeCAD Python API with proper imports (import FreeCAD, Part)
- Create new document with descriptive name
- All dimensions in millimeters
- Use proper geometric relationships and constraints
- Add meaningful labels and object organization
- Include professional color coding and materials
- End with doc.recompute() and ViewFit commands
- Ensure code executes without errors

QUALITY STANDARDS:
- Professional architectural accuracy
- Compliance with {building_spec.region.title()} building codes
- Realistic proportions and functional layout
- Clean, well-commented Python code
- Production-ready FreeCAD model

Generate comprehensive FreeCAD Python code that creates this architectural model with professional quality and accuracy."""

        return prompt

# Global instance
dynamic_config = DynamicBuildingConfig()