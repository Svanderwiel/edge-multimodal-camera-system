#!/usr/bin/env python3
"""
Prompt Templates for Multimodal AI Camera Assistant
Pre-defined prompts for different scenarios and use cases
"""

from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class PromptTemplates:
    """Collection of optimized prompts for different vision scenarios"""

    def __init__(self):
        """Initialize prompt templates"""
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict[str, Dict[str, str]]:
        """Load all prompt templates"""
        return {
            'general_description': {
                'prompt': "Describe what you see in this image in 2-3 sentences. Focus on the main objects and their context.",
                'use_case': 'General object detection and description',
                'max_tokens': 150
            },

            'food_nutrition': {
                'prompt': "This appears to be food. Identify the food items and provide: 1) What it is, 2) Estimated calories per serving, 3) Key nutritional benefits or concerns. Keep response under 100 words.",
                'use_case': 'Food identification and nutrition analysis',
                'max_tokens': 100
            },

            'product_info': {
                'prompt': "Identify this product and provide: 1) Product name and brand, 2) Estimated retail price range, 3) Key features or uses. Keep response concise and factual.",
                'use_case': 'Product identification and information',
                'max_tokens': 120
            },

            'plant_care': {
                'prompt': "This appears to be a plant. Identify the plant species and provide: 1) Common name and scientific name, 2) Basic care instructions (watering, light, soil), 3) Common issues to watch for. Keep response practical and helpful.",
                'use_case': 'Plant identification and care instructions',
                'max_tokens': 150
            },

            'book_info': {
                'prompt': "This appears to be a book. Identify: 1) Title and author, 2) Genre or category, 3) Brief synopsis or main topic. If you can't read the text clearly, describe what you can see.",
                'use_case': 'Book identification and information',
                'max_tokens': 120
            },

            'visual_qa': {
                'prompt': "Answer this question about the image: {question}. Provide a clear, concise answer based on what you can see.",
                'use_case': 'Visual question answering',
                'max_tokens': 100,
                'requires_question': True
            },

            'scene_analysis': {
                'prompt': "Analyze this scene and list everything you can see. Format as a numbered list with brief descriptions. Focus on objects, people, and notable details.",
                'use_case': 'Comprehensive scene analysis',
                'max_tokens': 200
            },

            'kitchen_assistant': {
                'prompt': "You are a kitchen assistant. Identify all food items visible in this image. For each item, note: 1) What it is, 2) Approximate quantity, 3) Any expiration concerns or freshness notes. Format as a simple list.",
                'use_case': 'Kitchen inventory and food management',
                'max_tokens': 180
            },

            'safety_check': {
                'prompt': "Look at this image for any potential safety concerns, hazards, or issues. Identify: 1) Any obvious safety problems, 2) Recommendations for improvement, 3) Overall safety assessment. Be practical and helpful.",
                'use_case': 'Safety assessment and hazard identification',
                'max_tokens': 150
            },

            'accessibility': {
                'prompt': "Analyze this image from an accessibility perspective. Identify: 1) Any accessibility barriers, 2) How someone with visual, mobility, or other impairments might experience this space, 3) Suggestions for improvement.",
                'use_case': 'Accessibility assessment',
                'max_tokens': 180
            }
        }

    def get_prompt(self, template_name: str, **kwargs) -> str:
        """
        Get a prompt template by name
        Args:
            template_name: Name of the template
            **kwargs: Additional parameters (e.g., question for visual_qa)
        Returns:
            Formatted prompt string
        """
        if template_name not in self.templates:
            logger.warning(f"Template '{template_name}' not found, using general_description")
            template_name = 'general_description'

        template = self.templates[template_name]
        prompt = template['prompt']

        # Handle templates that require additional parameters
        if template_name == 'visual_qa' and 'question' in kwargs:
            prompt = prompt.format(question=kwargs['question'])
        elif template_name == 'visual_qa' and 'question' not in kwargs:
            logger.warning("visual_qa template requires 'question' parameter")
            prompt = "What do you see in this image? Describe the main objects and their context."

        return prompt

    def get_template_info(self, template_name: str) -> Dict[str, str]:
        """Get information about a template"""
        if template_name not in self.templates:
            return {}

        template = self.templates[template_name]
        return {
            'use_case': template['use_case'],
            'max_tokens': template.get('max_tokens', 150),
            'requires_question': template.get('requires_question', False)
        }

    def list_templates(self) -> List[str]:
        """Get list of available template names"""
        return list(self.templates.keys())

    def get_templates_by_use_case(self, use_case_keywords: List[str]) -> List[str]:
        """
        Find templates matching use case keywords
        Args:
            use_case_keywords: List of keywords to search for
        Returns:
            List of template names that match
        """
        matching_templates = []

        for template_name, template in self.templates.items():
            use_case = template['use_case'].lower()
            if any(keyword.lower() in use_case for keyword in use_case_keywords):
                matching_templates.append(template_name)

        return matching_templates

    def suggest_template(self, detected_objects: List[str]) -> str:
        """
        Suggest the best template based on detected objects
        Args:
            detected_objects: List of detected object class names
        Returns:
            Suggested template name
        """
        # Convert to lowercase for matching
        objects_lower = [obj.lower() for obj in detected_objects]

        # Food-related objects
        food_keywords = ['banana', 'apple', 'orange', 'broccoli', 'carrot', 'pizza',
                        'sandwich', 'cake', 'donut', 'hot dog', 'hamburger', 'bread']
        if any(keyword in objects_lower for keyword in food_keywords):
            return 'food_nutrition'

        # Product-related objects
        product_keywords = ['bottle', 'cup', 'book', 'laptop', 'cell phone', 'tv',
                           'remote', 'keyboard', 'mouse']
        if any(keyword in objects_lower for keyword in product_keywords):
            return 'product_info'

        # Plant-related objects
        plant_keywords = ['potted plant', 'vase', 'flower']
        if any(keyword in objects_lower for keyword in plant_keywords):
            return 'plant_care'

        # Book-related objects
        book_keywords = ['book']
        if any(keyword in objects_lower for keyword in book_keywords):
            return 'book_info'

        # Default to general description
        return 'general_description'
