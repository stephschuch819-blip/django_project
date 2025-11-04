#!/usr/bin/env python
"""
Setup script to create logs directory for security and application logging.
Run this script once before starting the application.
"""
import os
from pathlib import Path

# Get the base directory (where this script is located)
BASE_DIR = Path(__file__).resolve().parent

# Create logs directory
logs_dir = BASE_DIR / 'logs'
logs_dir.mkdir(exist_ok=True)

# Create .gitkeep to ensure directory is tracked but logs are ignored
gitkeep_file = logs_dir / '.gitkeep'
gitkeep_file.touch()

print(f"[OK] Created logs directory at: {logs_dir}")
print(f"[OK] Created .gitkeep file")
print("\nLogs will be written to:")
print(f"  - {logs_dir / 'security.log'} (security events)")
print(f"  - {logs_dir / 'application.log'} (application events)")
print("\nSetup complete!")
