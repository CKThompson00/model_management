"""
Model Management System for Azure AI Models

This package provides tools for managing model lifecycle including:
- Model registration
- Deprecation tracking
- Retirement management
"""

from .model import Model, ModelStatus
from .registry import ModelRegistry

__version__ = "0.1.0"
__all__ = ["Model", "ModelStatus", "ModelRegistry"]
