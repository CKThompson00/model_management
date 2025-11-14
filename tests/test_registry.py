"""
Tests for the ModelRegistry class.
"""

import json
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

from model_management.model import Model, ModelStatus
from model_management.registry import ModelRegistry


class TestModelRegistry(unittest.TestCase):
    """Test cases for the ModelRegistry class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.registry = ModelRegistry()
        self.now = datetime.now()
        self.yesterday = self.now - timedelta(days=1)
        self.tomorrow = self.now + timedelta(days=1)
        self.next_week = self.now + timedelta(days=7)
    
    def test_add_model(self):
        """Test adding a model to the registry."""
        model = Model("GPT-4", "1.0")
        self.registry.add_model(model)
        self.assertEqual(len(self.registry), 1)
    
    def test_add_duplicate_model(self):
        """Test that adding a duplicate model raises an error."""
        model1 = Model("GPT-4", "1.0")
        model2 = Model("GPT-4", "1.0")
        self.registry.add_model(model1)
        with self.assertRaises(ValueError):
            self.registry.add_model(model2)
    
    def test_remove_model(self):
        """Test removing a model from the registry."""
        model = Model("GPT-4", "1.0")
        self.registry.add_model(model)
        result = self.registry.remove_model("GPT-4", "1.0")
        self.assertTrue(result)
        self.assertEqual(len(self.registry), 0)
    
    def test_remove_nonexistent_model(self):
        """Test removing a model that doesn't exist."""
        result = self.registry.remove_model("GPT-4", "1.0")
        self.assertFalse(result)
    
    def test_get_model(self):
        """Test getting a specific model."""
        model = Model("GPT-4", "1.0")
        self.registry.add_model(model)
        retrieved = self.registry.get_model("GPT-4", "1.0")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, "GPT-4")
        self.assertEqual(retrieved.version, "1.0")
    
    def test_get_nonexistent_model(self):
        """Test getting a model that doesn't exist."""
        result = self.registry.get_model("GPT-4", "1.0")
        self.assertIsNone(result)
    
    def test_get_all_models(self):
        """Test getting all models."""
        model1 = Model("GPT-4", "1.0")
        model2 = Model("GPT-3", "1.0")
        self.registry.add_model(model1)
        self.registry.add_model(model2)
        models = self.registry.get_all_models()
        self.assertEqual(len(models), 2)
    
    def test_get_active_models(self):
        """Test getting active models."""
        active_model = Model("GPT-4", "1.0")
        deprecated_model = Model(
            "GPT-3",
            "1.0",
            created_date=self.yesterday,
            deprecation_date=self.yesterday,
            retirement_date=self.next_week
        )
        self.registry.add_model(active_model)
        self.registry.add_model(deprecated_model)
        
        active_models = self.registry.get_active_models()
        self.assertEqual(len(active_models), 1)
        self.assertEqual(active_models[0].name, "GPT-4")
    
    def test_get_deprecated_models(self):
        """Test getting deprecated models."""
        active_model = Model("GPT-4", "1.0")
        deprecated_model = Model(
            "GPT-3",
            "1.0",
            created_date=self.yesterday,
            deprecation_date=self.yesterday,
            retirement_date=self.next_week
        )
        self.registry.add_model(active_model)
        self.registry.add_model(deprecated_model)
        
        deprecated_models = self.registry.get_deprecated_models()
        self.assertEqual(len(deprecated_models), 1)
        self.assertEqual(deprecated_models[0].name, "GPT-3")
    
    def test_get_retired_models(self):
        """Test getting retired models."""
        active_model = Model("GPT-4", "1.0")
        retired_model = Model(
            "GPT-2",
            "1.0",
            created_date=self.yesterday,
            deprecation_date=self.yesterday,
            retirement_date=self.yesterday
        )
        self.registry.add_model(active_model)
        self.registry.add_model(retired_model)
        
        retired_models = self.registry.get_retired_models()
        self.assertEqual(len(retired_models), 1)
        self.assertEqual(retired_models[0].name, "GPT-2")
    
    def test_get_models_by_name(self):
        """Test getting all versions of a model."""
        model1 = Model("GPT-4", "1.0")
        model2 = Model("GPT-4", "2.0")
        model3 = Model("GPT-3", "1.0")
        self.registry.add_model(model1)
        self.registry.add_model(model2)
        self.registry.add_model(model3)
        
        gpt4_models = self.registry.get_models_by_name("GPT-4")
        self.assertEqual(len(gpt4_models), 2)
    
    def test_save_and_load_file(self):
        """Test saving and loading registry to/from file."""
        model1 = Model("GPT-4", "1.0", created_date=self.now)
        model2 = Model(
            "GPT-3",
            "1.0",
            created_date=self.yesterday,
            deprecation_date=self.tomorrow
        )
        self.registry.add_model(model1)
        self.registry.add_model(model2)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            # Save to file
            self.registry.save_to_file(temp_file)
            
            # Load into new registry
            new_registry = ModelRegistry()
            new_registry.load_from_file(temp_file)
            
            # Verify
            self.assertEqual(len(new_registry), 2)
            model = new_registry.get_model("GPT-4", "1.0")
            self.assertIsNotNone(model)
            self.assertEqual(model.name, "GPT-4")
        finally:
            # Clean up
            Path(temp_file).unlink(missing_ok=True)
    
    def test_repr(self):
        """Test string representation."""
        model = Model("GPT-4", "1.0")
        self.registry.add_model(model)
        repr_str = repr(self.registry)
        self.assertIn("ModelRegistry", repr_str)
        self.assertIn("1", repr_str)


if __name__ == "__main__":
    unittest.main()
