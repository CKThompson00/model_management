"""
Tests for the Model class.
"""

import unittest
from datetime import datetime, timedelta

from model_management.model import Model, ModelStatus


class TestModel(unittest.TestCase):
    """Test cases for the Model class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.now = datetime.now()
        self.yesterday = self.now - timedelta(days=1)
        self.tomorrow = self.now + timedelta(days=1)
        self.next_week = self.now + timedelta(days=7)
        self.next_month = self.now + timedelta(days=30)
    
    def test_create_basic_model(self):
        """Test creating a basic model without dates."""
        model = Model("GPT-4", "1.0")
        self.assertEqual(model.name, "GPT-4")
        self.assertEqual(model.version, "1.0")
        self.assertIsNotNone(model.created_date)
    
    def test_create_model_with_dates(self):
        """Test creating a model with all dates."""
        model = Model(
            "GPT-4",
            "1.0",
            created_date=self.yesterday,
            deprecation_date=self.next_week,
            retirement_date=self.next_month
        )
        self.assertEqual(model.created_date, self.yesterday)
        self.assertEqual(model.deprecation_date, self.next_week)
        self.assertEqual(model.retirement_date, self.next_month)
    
    def test_invalid_deprecation_date(self):
        """Test that deprecation date cannot be before creation date."""
        with self.assertRaises(ValueError):
            Model(
                "GPT-4",
                "1.0",
                created_date=self.now,
                deprecation_date=self.yesterday
            )
    
    def test_invalid_retirement_date(self):
        """Test that retirement date cannot be before deprecation date."""
        with self.assertRaises(ValueError):
            Model(
                "GPT-4",
                "1.0",
                created_date=self.yesterday,
                deprecation_date=self.next_week,
                retirement_date=self.tomorrow
            )
    
    def test_active_status(self):
        """Test that a model is active when no dates are passed."""
        model = Model("GPT-4", "1.0")
        self.assertEqual(model.get_status(), ModelStatus.ACTIVE)
        self.assertTrue(model.is_active())
        self.assertFalse(model.is_deprecated())
        self.assertFalse(model.is_retired())
    
    def test_deprecated_status(self):
        """Test that a model is deprecated when deprecation date has passed."""
        model = Model(
            "GPT-4",
            "1.0",
            created_date=self.yesterday,
            deprecation_date=self.yesterday,
            retirement_date=self.next_week
        )
        self.assertEqual(model.get_status(), ModelStatus.DEPRECATED)
        self.assertFalse(model.is_active())
        self.assertTrue(model.is_deprecated())
        self.assertFalse(model.is_retired())
    
    def test_retired_status(self):
        """Test that a model is retired when retirement date has passed."""
        model = Model(
            "GPT-4",
            "1.0",
            created_date=self.yesterday,
            deprecation_date=self.yesterday,
            retirement_date=self.yesterday
        )
        self.assertEqual(model.get_status(), ModelStatus.RETIRED)
        self.assertFalse(model.is_active())
        self.assertFalse(model.is_deprecated())
        self.assertTrue(model.is_retired())
    
    def test_status_with_reference_date(self):
        """Test checking status with a specific reference date."""
        model = Model(
            "GPT-4",
            "1.0",
            created_date=self.yesterday,
            deprecation_date=self.tomorrow,
            retirement_date=self.next_week
        )
        # Status now should be active
        self.assertEqual(model.get_status(self.now), ModelStatus.ACTIVE)
        # Status tomorrow should be deprecated
        self.assertEqual(model.get_status(self.tomorrow), ModelStatus.DEPRECATED)
        # Status next week should be retired
        self.assertEqual(model.get_status(self.next_week), ModelStatus.RETIRED)
    
    def test_to_dict(self):
        """Test converting model to dictionary."""
        model = Model(
            "GPT-4",
            "1.0",
            created_date=self.now,
            deprecation_date=self.tomorrow,
            retirement_date=self.next_week
        )
        data = model.to_dict()
        self.assertEqual(data["name"], "GPT-4")
        self.assertEqual(data["version"], "1.0")
        self.assertIn("created_date", data)
        self.assertIn("deprecation_date", data)
        self.assertIn("retirement_date", data)
        self.assertIn("status", data)
    
    def test_from_dict(self):
        """Test creating model from dictionary."""
        data = {
            "name": "GPT-4",
            "version": "1.0",
            "created_date": self.now.isoformat(),
            "deprecation_date": self.tomorrow.isoformat(),
            "retirement_date": self.next_week.isoformat()
        }
        model = Model.from_dict(data)
        self.assertEqual(model.name, "GPT-4")
        self.assertEqual(model.version, "1.0")
        self.assertAlmostEqual(
            model.created_date.timestamp(),
            self.now.timestamp(),
            delta=1
        )
    
    def test_repr(self):
        """Test string representation."""
        model = Model("GPT-4", "1.0")
        repr_str = repr(model)
        self.assertIn("GPT-4", repr_str)
        self.assertIn("1.0", repr_str)
    
    def test_str(self):
        """Test human-readable string."""
        model = Model("GPT-4", "1.0")
        str_repr = str(model)
        self.assertIn("GPT-4", str_repr)
        self.assertIn("1.0", str_repr)
        self.assertIn("active", str_repr)


if __name__ == "__main__":
    unittest.main()
