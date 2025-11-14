"""
ModelRegistry for managing a collection of models.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from .model import Model, ModelStatus


class ModelRegistry:
    """
    A registry for managing multiple AI models.
    
    Provides functionality to:
    - Add and remove models
    - Query models by status
    - Load and save registry to file
    - Find models by name/version
    """
    
    def __init__(self):
        """Initialize an empty model registry."""
        self._models: List[Model] = []
    
    def add_model(self, model: Model) -> None:
        """
        Add a model to the registry.
        
        Args:
            model: The Model instance to add
            
        Raises:
            ValueError: If a model with the same name and version already exists
        """
        if self.get_model(model.name, model.version):
            raise ValueError(f"Model {model.name} v{model.version} already exists in registry")
        self._models.append(model)
    
    def remove_model(self, name: str, version: str) -> bool:
        """
        Remove a model from the registry.
        
        Args:
            name: The name of the model
            version: The version of the model
            
        Returns:
            True if the model was removed, False if not found
        """
        model = self.get_model(name, version)
        if model:
            self._models.remove(model)
            return True
        return False
    
    def get_model(self, name: str, version: str) -> Optional[Model]:
        """
        Get a specific model by name and version.
        
        Args:
            name: The name of the model
            version: The version of the model
            
        Returns:
            The Model instance if found, None otherwise
        """
        for model in self._models:
            if model.name == name and model.version == version:
                return model
        return None
    
    def get_all_models(self) -> List[Model]:
        """Get all models in the registry."""
        return self._models.copy()
    
    def get_models_by_status(
        self,
        status: ModelStatus,
        reference_date: Optional[datetime] = None
    ) -> List[Model]:
        """
        Get all models with a specific status.
        
        Args:
            status: The status to filter by
            reference_date: The date to check status against (defaults to now)
            
        Returns:
            List of models with the specified status
        """
        return [
            model for model in self._models
            if model.get_status(reference_date) == status
        ]
    
    def get_active_models(self, reference_date: Optional[datetime] = None) -> List[Model]:
        """Get all active models."""
        return self.get_models_by_status(ModelStatus.ACTIVE, reference_date)
    
    def get_deprecated_models(self, reference_date: Optional[datetime] = None) -> List[Model]:
        """Get all deprecated models."""
        return self.get_models_by_status(ModelStatus.DEPRECATED, reference_date)
    
    def get_retired_models(self, reference_date: Optional[datetime] = None) -> List[Model]:
        """Get all retired models."""
        return self.get_models_by_status(ModelStatus.RETIRED, reference_date)
    
    def get_models_by_name(self, name: str) -> List[Model]:
        """
        Get all versions of a model by name.
        
        Args:
            name: The name of the model
            
        Returns:
            List of all models with the specified name
        """
        return [model for model in self._models if model.name == name]
    
    def save_to_file(self, filepath: str) -> None:
        """
        Save the registry to a JSON file.
        
        Args:
            filepath: Path to the file to save to
        """
        data = {
            "models": [model.to_dict() for model in self._models]
        }
        
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_from_file(self, filepath: str) -> None:
        """
        Load the registry from a JSON file.
        
        Args:
            filepath: Path to the file to load from
            
        Raises:
            FileNotFoundError: If the file doesn't exist
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self._models = [Model.from_dict(model_data) for model_data in data.get("models", [])]
    
    def __len__(self) -> int:
        """Return the number of models in the registry."""
        return len(self._models)
    
    def __repr__(self) -> str:
        """String representation of the registry."""
        return f"ModelRegistry(models={len(self._models)})"
