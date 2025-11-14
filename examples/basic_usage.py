#!/usr/bin/env python3
"""
Example usage of the Model Management System.
"""

from datetime import datetime, timedelta
from model_management import Model, ModelRegistry, ModelStatus


def main():
    """Demonstrate model management system usage."""
    
    print("=== Model Management System Example ===\n")
    
    # Create some example models
    now = datetime.now()
    
    # Active model - no retirement planned yet
    gpt4 = Model(
        name="GPT-4",
        version="1.0",
        created_date=now - timedelta(days=30),
        deprecation_date=now + timedelta(days=335),  # Deprecate in ~1 year
        retirement_date=now + timedelta(days=700)    # Retire in ~2 years
    )
    
    # Deprecated model - still available but not recommended
    gpt3_5 = Model(
        name="GPT-3.5",
        version="2.0",
        created_date=now - timedelta(days=365),
        deprecation_date=now - timedelta(days=30),  # Deprecated 30 days ago
        retirement_date=now + timedelta(days=180)   # Retire in 6 months
    )
    
    # Retired model - no longer available
    gpt3 = Model(
        name="GPT-3",
        version="1.0",
        created_date=now - timedelta(days=730),
        deprecation_date=now - timedelta(days=365),
        retirement_date=now - timedelta(days=180)
    )
    
    # Create registry and add models
    print("Creating model registry...")
    registry = ModelRegistry()
    registry.add_model(gpt4)
    registry.add_model(gpt3_5)
    registry.add_model(gpt3)
    print(f"Registry created with {len(registry)} models\n")
    
    # Display all models
    print("All models:")
    for model in registry.get_all_models():
        print(f"  - {model}")
    print()
    
    # Query by status
    print("Active models:")
    for model in registry.get_active_models():
        print(f"  - {model.name} v{model.version}")
    print()
    
    print("Deprecated models:")
    for model in registry.get_deprecated_models():
        print(f"  - {model.name} v{model.version}")
        if model.retirement_date:
            days_until_retirement = (model.retirement_date - now).days
            print(f"    → Will be retired in {days_until_retirement} days")
    print()
    
    print("Retired models:")
    for model in registry.get_retired_models():
        print(f"  - {model.name} v{model.version}")
    print()
    
    # Save to file
    print("Saving registry to file...")
    registry.save_to_file("example_registry.json")
    print("✓ Saved to example_registry.json\n")
    
    # Load from file
    print("Loading registry from file...")
    new_registry = ModelRegistry()
    new_registry.load_from_file("example_registry.json")
    print(f"✓ Loaded {len(new_registry)} models\n")
    
    # Check specific model status
    print("Checking specific model status:")
    model = new_registry.get_model("GPT-4", "1.0")
    if model:
        print(f"  Model: {model.name} v{model.version}")
        print(f"  Status: {model.get_status().value}")
        print(f"  Created: {model.created_date.strftime('%Y-%m-%d')}")
        if model.deprecation_date:
            print(f"  Deprecation: {model.deprecation_date.strftime('%Y-%m-%d')}")
        if model.retirement_date:
            print(f"  Retirement: {model.retirement_date.strftime('%Y-%m-%d')}")
    
    print("\n=== Example Complete ===")


if __name__ == "__main__":
    main()
