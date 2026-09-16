"""
Framework lifecycle hooks for JIT Context OS.
Executes inside Agent Zero framework runtime.
"""

import os
import sys

def install():
    """Called automatically by Agent Zero when plugin is installed."""
    print("[JIT Context OS] Running post-install setup...")
    plugin_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(plugin_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    return 0

def uninstall():
    """Called before plugin is deleted from usr/plugins/."""
    print("[JIT Context OS] Cleaning up runtime caches...")
    return 0
