"""
Model class for representing AI models with lifecycle information.
"""

from datetime import datetime
from enum import Enum
from typing import Optional


class ModelStatus(Enum):
    """Enum representing the lifecycle status of a model."""
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    RETIRED = "retired"


class Model:
    """
    Represents an AI model with lifecycle management information.
    
    Attributes:
        name: The name of the model
        version: The version of the model
        created_date: When the model was created
        deprecation_date: Optional date when the model will be deprecated
        retirement_date: Optional date when the model will be retired
    """
    
    def __init__(
        self,
        name: str,
        version: str,
        created_date: Optional[datetime] = None,
        deprecation_date: Optional[datetime] = None,
        retirement_date: Optional[datetime] = None
    ):
        """
        Initialize a Model instance.
        
        Args:
            name: The name of the model
            version: The version of the model
            created_date: When the model was created (defaults to now)
            deprecation_date: Optional date when the model will be deprecated
            retirement_date: Optional date when the model will be retired
            
        Raises:
            ValueError: If dates are not in logical order
        """
        self.name = name
        self.version = version
        self.created_date = created_date or datetime.now()
        self.deprecation_date = deprecation_date
        self.retirement_date = retirement_date
        
        self._validate_dates()
    
    def _validate_dates(self):
        """Validate that dates are in logical order."""
        if self.deprecation_date and self.deprecation_date < self.created_date:
            raise ValueError("Deprecation date cannot be before creation date")
        
        if self.retirement_date and self.deprecation_date:
            if self.retirement_date < self.deprecation_date:
                raise ValueError("Retirement date cannot be before deprecation date")
        
        if self.retirement_date and not self.deprecation_date:
            if self.retirement_date < self.created_date:
                raise ValueError("Retirement date cannot be before creation date")
    
    def get_status(self, reference_date: Optional[datetime] = None) -> ModelStatus:
        """
        Get the current status of the model.
        
        Args:
            reference_date: The date to check status against (defaults to now)
            
        Returns:
            ModelStatus indicating whether the model is active, deprecated, or retired
        """
        ref_date = reference_date or datetime.now()
        
        if self.retirement_date and ref_date >= self.retirement_date:
            return ModelStatus.RETIRED
        
        if self.deprecation_date and ref_date >= self.deprecation_date:
            return ModelStatus.DEPRECATED
        
        return ModelStatus.ACTIVE
    
    def is_active(self, reference_date: Optional[datetime] = None) -> bool:
        """Check if the model is currently active."""
        return self.get_status(reference_date) == ModelStatus.ACTIVE
    
    def is_deprecated(self, reference_date: Optional[datetime] = None) -> bool:
        """Check if the model is currently deprecated."""
        return self.get_status(reference_date) == ModelStatus.DEPRECATED
    
    def is_retired(self, reference_date: Optional[datetime] = None) -> bool:
        """Check if the model is currently retired."""
        return self.get_status(reference_date) == ModelStatus.RETIRED
    
    def to_dict(self) -> dict:
        """Convert the model to a dictionary representation."""
        return {
            "name": self.name,
            "version": self.version,
            "created_date": self.created_date.isoformat(),
            "deprecation_date": self.deprecation_date.isoformat() if self.deprecation_date else None,
            "retirement_date": self.retirement_date.isoformat() if self.retirement_date else None,
            "status": self.get_status().value
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Model":
        """Create a Model instance from a dictionary."""
        return cls(
            name=data["name"],
            version=data["version"],
            created_date=datetime.fromisoformat(data["created_date"]),
            deprecation_date=datetime.fromisoformat(data["deprecation_date"]) if data.get("deprecation_date") else None,
            retirement_date=datetime.fromisoformat(data["retirement_date"]) if data.get("retirement_date") else None
        )
    
    def __repr__(self) -> str:
        """String representation of the model."""
        return f"Model(name='{self.name}', version='{self.version}', status='{self.get_status().value}')"
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"{self.name} v{self.version} [{self.get_status().value}]"
