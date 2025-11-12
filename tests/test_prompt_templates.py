"""
Tests for prompt templates
"""

import pytest
from multimodal_camera.vision.prompt_templates import PromptTemplates

def test_template_initialization():
    """Test that templates initialize correctly"""
    templates = PromptTemplates()
    assert len(templates.list_templates()) > 0

def test_get_prompt():
    """Test getting a prompt by name"""
    templates = PromptTemplates()
    prompt = templates.get_prompt('general_description')
    assert isinstance(prompt, str)
    assert len(prompt) > 0

def test_suggest_template():
    """Test template suggestion based on objects"""
    templates = PromptTemplates()

    # Test food detection
    assert templates.suggest_template(['banana']) == 'food_nutrition'

    # Test product detection
    assert templates.suggest_template(['laptop']) == 'product_info'

    # Test plant detection
    assert templates.suggest_template(['potted plant']) == 'plant_care'

    # Test default
    assert templates.suggest_template(['person']) == 'general_description'

def test_template_info():
    """Test getting template information"""
    templates = PromptTemplates()
    info = templates.get_template_info('general_description')
    assert 'use_case' in info
    assert 'max_tokens' in info
