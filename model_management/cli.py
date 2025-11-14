#!/usr/bin/env python3
"""
Command-line interface for Model Management System.
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

from model_management import Model, ModelRegistry, ModelStatus


DEFAULT_REGISTRY_FILE = "model_registry.json"


def parse_date(date_string: str) -> datetime:
    """Parse a date string in ISO format."""
    try:
        return datetime.fromisoformat(date_string)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format: {date_string}. Use ISO format (YYYY-MM-DD)")


def load_registry(filepath: str) -> ModelRegistry:
    """Load registry from file, or create new if doesn't exist."""
    registry = ModelRegistry()
    if Path(filepath).exists():
        registry.load_from_file(filepath)
    return registry


def cmd_add(args):
    """Add a new model to the registry."""
    registry = load_registry(args.registry)
    
    try:
        model = Model(
            name=args.name,
            version=args.version,
            created_date=parse_date(args.created) if args.created else None,
            deprecation_date=parse_date(args.deprecation) if args.deprecation else None,
            retirement_date=parse_date(args.retirement) if args.retirement else None
        )
        registry.add_model(model)
        registry.save_to_file(args.registry)
        print(f"✓ Added model: {model}")
    except ValueError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_list(args):
    """List models in the registry."""
    registry = load_registry(args.registry)
    
    models = registry.get_all_models()
    
    if args.status:
        try:
            status = ModelStatus(args.status)
            models = registry.get_models_by_status(status)
        except ValueError:
            print(f"✗ Invalid status: {args.status}", file=sys.stderr)
            sys.exit(1)
    
    if args.name:
        models = [m for m in models if m.name == args.name]
    
    if not models:
        print("No models found.")
        return
    
    print(f"\nFound {len(models)} model(s):\n")
    for model in models:
        print(f"  {model.name} v{model.version}")
        print(f"    Status: {model.get_status().value}")
        print(f"    Created: {model.created_date.strftime('%Y-%m-%d')}")
        if model.deprecation_date:
            print(f"    Deprecation: {model.deprecation_date.strftime('%Y-%m-%d')}")
        if model.retirement_date:
            print(f"    Retirement: {model.retirement_date.strftime('%Y-%m-%d')}")
        print()


def cmd_status(args):
    """Check the status of a specific model."""
    registry = load_registry(args.registry)
    
    model = registry.get_model(args.name, args.version)
    if not model:
        print(f"✗ Model {args.name} v{args.version} not found", file=sys.stderr)
        sys.exit(1)
    
    reference_date = parse_date(args.date) if args.date else None
    status = model.get_status(reference_date)
    
    print(f"\nModel: {model.name} v{model.version}")
    print(f"Status: {status.value}")
    print(f"Created: {model.created_date.strftime('%Y-%m-%d')}")
    
    if model.deprecation_date:
        print(f"Deprecation: {model.deprecation_date.strftime('%Y-%m-%d')}")
    
    if model.retirement_date:
        print(f"Retirement: {model.retirement_date.strftime('%Y-%m-%d')}")


def cmd_remove(args):
    """Remove a model from the registry."""
    registry = load_registry(args.registry)
    
    if registry.remove_model(args.name, args.version):
        registry.save_to_file(args.registry)
        print(f"✓ Removed model: {args.name} v{args.version}")
    else:
        print(f"✗ Model {args.name} v{args.version} not found", file=sys.stderr)
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Model Management System for Azure AI Models",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--registry",
        default=DEFAULT_REGISTRY_FILE,
        help=f"Path to registry file (default: {DEFAULT_REGISTRY_FILE})"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new model")
    add_parser.add_argument("name", help="Model name")
    add_parser.add_argument("version", help="Model version")
    add_parser.add_argument("--created", help="Creation date (YYYY-MM-DD)")
    add_parser.add_argument("--deprecation", help="Deprecation date (YYYY-MM-DD)")
    add_parser.add_argument("--retirement", help="Retirement date (YYYY-MM-DD)")
    add_parser.set_defaults(func=cmd_add)
    
    # List command
    list_parser = subparsers.add_parser("list", help="List models")
    list_parser.add_argument("--status", choices=["active", "deprecated", "retired"], help="Filter by status")
    list_parser.add_argument("--name", help="Filter by model name")
    list_parser.set_defaults(func=cmd_list)
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Check model status")
    status_parser.add_argument("name", help="Model name")
    status_parser.add_argument("version", help="Model version")
    status_parser.add_argument("--date", help="Check status at specific date (YYYY-MM-DD)")
    status_parser.set_defaults(func=cmd_status)
    
    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a model")
    remove_parser.add_argument("name", help="Model name")
    remove_parser.add_argument("version", help="Model version")
    remove_parser.set_defaults(func=cmd_remove)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    main()
