#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python magic library - main interface
Compatible with python-magic API

Resource Management Guide:
1. Convenience functions from_file/from_buffer use shared instances, no manual resource management needed
2. Magic class supports context manager, recommend using with statement
3. For long-term use, create Magic instance for reuse, remember to call close()

Usage Examples:
    # Convenience functions (recommended for simple scenarios)
    result = magic.from_file('file.txt')
    
    # Context manager (recommended for resource-controlled scenarios)
    with magic.Magic() as m:
        result = m.from_file('file.txt')
    
    # Manual management (remember to call close)
    m = magic.Magic()
    try:
        result = m.from_file('file.txt')
    finally:
        m.close()
"""

from magic_wrapper import Magic, magic_from_file, magic_from_buffer

# Provide standard python-magic compatible interface
def from_file(filename, mime=False):
    """
    Get magic information from file (uses shared instance, auto resource management)
    
    Args:
        filename (str): Path to file
        mime (bool): Return MIME type
        
    Returns:
        str: Magic information
    """
    return magic_from_file(filename, mime=mime)

def from_buffer(buffer_data, mime=False):
    """
    Get magic information from buffer (uses shared instance, auto resource management)
    
    Args:
        buffer_data (str/bytes): Buffer data
        mime (bool): Return MIME type
        
    Returns:
        str: Magic information
    """
    return magic_from_buffer(buffer_data, mime=mime)

# Export all functionality
__all__ = ['Magic', 'from_file', 'from_buffer', 'magic_from_file', 'magic_from_buffer'] 