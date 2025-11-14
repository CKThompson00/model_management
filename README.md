# Model Management System

A Python-based model management system for Azure AI Models that helps you track and manage model retirement and deprecation dates.

## Features

- **Model Lifecycle Tracking**: Track models through their entire lifecycle (Active → Deprecated → Retired)
- **Date Management**: Set and validate creation, deprecation, and retirement dates
- **Registry System**: Manage multiple models in a centralized registry
- **CLI Interface**: Easy-to-use command-line interface for common operations
- **Persistent Storage**: Save and load model registry to/from JSON files
- **Status Queries**: Query models by status, name, or date ranges

## Installation

```bash
pip install -e .
```

## Usage

### Command Line Interface

The package provides a `model-mgmt` command for managing models:

#### Add a Model

```bash
# Add a new model with deprecation and retirement dates
model-mgmt add GPT-4 1.0 --deprecation 2025-12-31 --retirement 2026-06-30

# Add with custom creation date
model-mgmt add GPT-3 2.0 --created 2023-01-01 --deprecation 2024-01-01 --retirement 2024-06-01
```

#### List Models

```bash
# List all models
model-mgmt list

# List only active models
model-mgmt list --status active

# List only deprecated models
model-mgmt list --status deprecated

# List only retired models
model-mgmt list --status retired

# Filter by model name
model-mgmt list --name GPT-4
```

#### Check Model Status

```bash
# Check current status of a model
model-mgmt status GPT-4 1.0

# Check status at a specific date
model-mgmt status GPT-4 1.0 --date 2026-01-01
```

#### Remove a Model

```bash
model-mgmt remove GPT-4 1.0
```

#### Custom Registry File

By default, models are stored in `model_registry.json`. You can specify a custom file:

```bash
model-mgmt --registry /path/to/custom.json add GPT-4 1.0
```

### Python API

You can also use the package programmatically:

```python
from datetime import datetime, timedelta
from model_management import Model, ModelRegistry, ModelStatus

# Create models
now = datetime.now()
model = Model(
    name="GPT-4",
    version="1.0",
    created_date=now,
    deprecation_date=now + timedelta(days=365),
    retirement_date=now + timedelta(days=730)
)

# Check model status
print(model.get_status())  # ModelStatus.ACTIVE
print(model.is_active())   # True

# Create and use a registry
registry = ModelRegistry()
registry.add_model(model)

# Query models
active_models = registry.get_active_models()
deprecated_models = registry.get_deprecated_models()
retired_models = registry.get_retired_models()

# Save to file
registry.save_to_file("models.json")

# Load from file
new_registry = ModelRegistry()
new_registry.load_from_file("models.json")
```

## Model Lifecycle

Models go through three lifecycle stages:

1. **Active**: Model is currently available and recommended for use
2. **Deprecated**: Model is still available but no longer recommended; users should migrate to newer versions
3. **Retired**: Model is no longer available and cannot be used

The status is automatically determined based on the current date and the model's deprecation and retirement dates.

## Date Validation

The system enforces logical date ordering:
- Deprecation date must be after creation date
- Retirement date must be after deprecation date
- All dates are optional except creation date (defaults to now)

## Data Format

Models are stored in JSON format:

```json
{
  "models": [
    {
      "name": "GPT-4",
      "version": "1.0",
      "created_date": "2023-01-01T00:00:00",
      "deprecation_date": "2024-12-31T00:00:00",
      "retirement_date": "2025-06-30T00:00:00",
      "status": "active"
    }
  ]
}
```

## Development

### Running Tests

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

All tests should pass before submitting changes.

## License

MIT License
