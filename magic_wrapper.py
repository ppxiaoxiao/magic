#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python 2 compatible magic library wrapper
Direct ctypes calls to libmagic, no python-magic dependency required
"""

from __future__ import print_function
import ctypes
import os
import sys

# Python 2 compatibility: import ctypes.util separately
try:
    import ctypes.util
    _has_util = True
except ImportError:
    _has_util = False

class Magic(object):
    """
    Magic file type detection wrapper for Python 2
    """
    
    # libmagic constants
    MAGIC_NONE = 0
    MAGIC_DEBUG = 1
    MAGIC_SYMLINK = 2
    MAGIC_COMPRESS = 4
    MAGIC_DEVICES = 8
    MAGIC_MIME_TYPE = 16
    MAGIC_CONTINUE = 32
    MAGIC_CHECK = 64
    MAGIC_PRESERVE_ATIME = 128
    MAGIC_RAW = 256
    MAGIC_ERROR = 512
    MAGIC_MIME_ENCODING = 1024
    MAGIC_MIME = MAGIC_MIME_TYPE | MAGIC_MIME_ENCODING
    MAGIC_APPLE = 2048
    
    def __init__(self, mime=False, mime_encoding=False):
        """
        Initialize magic instance
        
        Args:
            mime (bool): Return MIME type instead of textual description
            mime_encoding (bool): Return MIME encoding
        """
        # Find libmagic library
        self.libmagic = None
        self.magic_cookie = None
        self._closed = False
        
        # Extended library path search list
        magic_lib_paths = []
        
        # Try ctypes.util first if available
        if _has_util:
            try:
                lib_path = ctypes.util.find_library('magic')
                if lib_path:
                    magic_lib_paths.append(lib_path)
            except:
                pass
        
        # Add common library paths
        magic_lib_paths.extend([
            '/usr/lib64/libmagic.so.1.0.0',  
            '/usr/lib64/libmagic.so.1',
            '/usr/lib64/libmagic.so',
            '/usr/lib/libmagic.so.1',
            '/usr/lib/x86_64-linux-gnu/libmagic.so.1',
            '/lib/libmagic.so.1',
            '/lib/x86_64-linux-gnu/libmagic.so.1',
            'libmagic.so.1',  
            'libmagic.so',
            'magic'
        ])
        
        for lib_path in magic_lib_paths:
            if lib_path:
                try:
                    self.libmagic = ctypes.cdll.LoadLibrary(lib_path)
                    break
                except OSError as e:
                    continue
        
        if not self.libmagic:
            raise ImportError("Unable to find libmagic library")
        
        # Setup function prototypes
        self._setup_prototypes()
        
        # Setup flags
        flags = self.MAGIC_NONE
        if mime and mime_encoding:
            flags |= self.MAGIC_MIME
        elif mime:
            flags |= self.MAGIC_MIME_TYPE
        elif mime_encoding:
            flags |= self.MAGIC_MIME_ENCODING
            
        # Initialize magic
        self.magic_cookie = self.libmagic.magic_open(flags)
        if not self.magic_cookie:
            raise Exception("Unable to initialize libmagic")
            
        # Load default database
        if self.libmagic.magic_load(self.magic_cookie, None) != 0:
            raise Exception("Unable to load magic database")
    
    def _setup_prototypes(self):
        """Setup libmagic function prototypes"""
        # magic_open
        self.libmagic.magic_open.restype = ctypes.c_void_p
        self.libmagic.magic_open.argtypes = [ctypes.c_int]
        
        # magic_load
        self.libmagic.magic_load.restype = ctypes.c_int
        self.libmagic.magic_load.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        
        # magic_file
        self.libmagic.magic_file.restype = ctypes.c_char_p
        self.libmagic.magic_file.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        
        # magic_buffer
        self.libmagic.magic_buffer.restype = ctypes.c_char_p
        self.libmagic.magic_buffer.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t]
        
        # magic_close
        self.libmagic.magic_close.restype = None
        self.libmagic.magic_close.argtypes = [ctypes.c_void_p]
        
        # magic_error
        self.libmagic.magic_error.restype = ctypes.c_char_p
        self.libmagic.magic_error.argtypes = [ctypes.c_void_p]
    
    def from_file(self, filename):
        """
        Get magic information from file
        
        Args:
            filename (str): Path to file
            
        Returns:
            str: Magic information
        """
        if self._closed:
            raise Exception("Magic instance has been closed")
            
        if not os.path.exists(filename):
            raise IOError("File not found: %s" % filename)
            
        result = self.libmagic.magic_file(self.magic_cookie, filename.encode('utf-8'))
        if result is None:
            error = self.libmagic.magic_error(self.magic_cookie)
            raise Exception("Magic error: %s" % error)
            
        return result.decode('utf-8')
    
    def from_buffer(self, buffer_data):
        """
        Get magic information from buffer
        
        Args:
            buffer_data (str/bytes): Buffer data
            
        Returns:
            str: Magic information
        """
        if self._closed:
            raise Exception("Magic instance has been closed")
            
        # Python 2 compatibility handling
        if hasattr(buffer_data, 'encode'):  
            buffer_data = buffer_data.encode('utf-8')
            
        result = self.libmagic.magic_buffer(
            self.magic_cookie, 
            ctypes.c_char_p(buffer_data), 
            len(buffer_data)
        )
        
        if result is None:
            error = self.libmagic.magic_error(self.magic_cookie)
            raise Exception("Magic error: %s" % error)
            
        return result.decode('utf-8')
    
    def close(self):
        """Explicitly close resources"""
        if not self._closed and self.magic_cookie:
            self.libmagic.magic_close(self.magic_cookie)
            self.magic_cookie = None
            self._closed = True
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
    
    def __del__(self):        
        """Destructor cleanup"""
        self.close()


# Global shared instances to avoid frequent create/destroy operations
_shared_magic = None
_shared_mime_magic = None

def _get_shared_magic(mime=False):
    """Get shared Magic instance"""
    global _shared_magic, _shared_mime_magic
    
    if mime:
        if _shared_mime_magic is None:
            _shared_mime_magic = Magic(mime=True)
        return _shared_mime_magic
    else:
        if _shared_magic is None:
            _shared_magic = Magic()
        return _shared_magic

# Convenience functions using shared instances to avoid frequent creation
def magic_from_file(filename, mime=False):
    """
    Get magic information from file (convenience function)
    
    Args:
        filename (str): Path to file
        mime (bool): Return MIME type
        
    Returns:
        str: Magic information
    """
    magic_instance = _get_shared_magic(mime=mime)
    return magic_instance.from_file(filename)


def magic_from_buffer(buffer_data, mime=False):
    """
    Get magic information from buffer (convenience function)
    
    Args:
        buffer_data (str/bytes): Buffer data
        mime (bool): Return MIME type
        
    Returns:
        str: Magic information
    """
    magic_instance = _get_shared_magic(mime=mime)
    return magic_instance.from_buffer(buffer_data)


def main():
    """Command line entry function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Python 2 compatible magic file type detector')
    parser.add_argument('files', nargs='+', help='Files to analyze')
    parser.add_argument('--mime', action='store_true', help='Output MIME type')
    parser.add_argument('--mime-encoding', action='store_true', help='Output MIME encoding')
    parser.add_argument('--version', action='version', version='python2-magic 1.0.0')
    
    args = parser.parse_args()
    
    try:
        magic = Magic(mime=args.mime, mime_encoding=args.mime_encoding)
        
        for filename in args.files:
            try:
                result = magic.from_file(filename)
                print("%s: %s" % (filename, result))
            except Exception as e:
                print("%s: ERROR - %s" % (filename, str(e)), file=sys.stderr)
                
    except Exception as e:
        print("ERROR: %s" % str(e), file=sys.stderr)
        sys.exit(1)


# Example usage
if __name__ == '__main__':
    # Check if there are command line arguments
    import sys
    if len(sys.argv) > 1:
        main()
    else:
        # Run test code
        try:
            print("Python version and ctypes info:")
            print("- Python: %s" % str(ctypes.pythonapi))
            print("- ctypes.util available: %s" % _has_util)
            
            # Detect file type
            file_type = magic_from_file('/etc/passwd')
            print("File type: %s" % file_type)
            
            # Detect MIME type
            mime_type = magic_from_file('/etc/passwd', mime=True)
            print("MIME type: %s" % mime_type)
            
            # Detect buffer content
            buffer_content = "#!/bin/bash\necho 'Hello World'"
            buffer_type = magic_from_buffer(buffer_content)
            print("Buffer type: %s" % buffer_type)
            
        except Exception as e:
            print("Error: %s" % str(e)) 