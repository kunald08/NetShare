"""
Utils package for NetShare
Contains utility modules for file management, settings, and common functions
"""

__version__ = "2.0.0"
__author__ = "kunald08"

from .file_manager import FileManager
from .settings_manager import SettingsManager
from .app_utils import AppUtils, ProgressTracker, EventManager

__all__ = ['FileManager', 'SettingsManager',
           'AppUtils', 'ProgressTracker', 'EventManager']
