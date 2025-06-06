# magic

A Python 2 compatible magic library wrapper that uses ctypes to directly call libmagic, without requiring python-magic installation.

## Features

- **Python 2 Compatible**: Designed for Python 2.7, also compatible with Python 3
- **No Extra Dependencies**: Only uses Python standard library, directly calls libmagic via ctypes
- **Easy to Use**: Provides python-magic compatible API
- **High Performance**: Direct C library calls, excellent performance
- **Auto Library Discovery**: Automatically searches for libmagic library in system
- **Resource Management**: Smart resource management with shared instances and context managers

## Installation

### Install from wheel

```bash
pip install magic-1.0.0-py2.py3-none-any.whl
```

### Install from source

```bash
python setup.py install
```

### Build wheel

```bash
python setup.py bdist_wheel
```

## Usage

### Simple Usage (Recommended)

```python
import magic

# Detect file type
file_type = magic.from_file('/path/to/file')
print("File type: %s" % file_type)

# Detect MIME type
mime_type = magic.from_file('/path/to/file', mime=True)
print("MIME type: %s" % mime_type)

# Detect buffer content
buffer_content = "#!/bin/bash\necho 'Hello World'"
buffer_type = magic.from_buffer(buffer_content)
print("Buffer type: %s" % buffer_type)
```

### Context Manager (Resource Controlled)

```python
import magic

# Recommended for batch processing
with magic.Magic() as m:
    for filename in file_list:
        result = m.from_file(filename)
        print("%s: %s" % (filename, result))
# Resources automatically cleaned up
```

### Object-Oriented Interface

```python
import magic

# Create Magic instance
m = magic.Magic()
try:
    file_type = m.from_file('/path/to/file')
    print("File type: %s" % file_type)
finally:
    m.close()  # Remember to close

# MIME type detection instance
mime_magic = magic.Magic(mime=True)
try:
    mime_type = mime_magic.from_file('/path/to/file')
    print("MIME type: %s" % mime_type)
finally:
    mime_magic.close()

# MIME encoding detection instance
encoding_magic = magic.Magic(mime_encoding=True)
try:
    encoding = encoding_magic.from_file('/path/to/file')
    print("Encoding: %s" % encoding)
finally:
    encoding_magic.close()
```

### Legacy magic_wrapper Interface

```python
import magic_wrapper

# Direct module functions (uses shared instances)
file_type = magic_wrapper.magic_from_file('/path/to/file')
mime_type = magic_wrapper.magic_from_file('/path/to/file', mime=True)
buffer_type = magic_wrapper.magic_from_buffer(buffer_content)
```

## Command Line Tool

After installation, you can use the `py2-magic` command:

```bash
# Detect single file
py2-magic file.txt

# Detect multiple files
py2-magic file1.txt file2.jpg file3.pdf

# Get MIME type
py2-magic --mime file.txt

# Get MIME encoding
py2-magic --mime-encoding file.txt

# Show version
py2-magic --version

# Show help
py2-magic --help
```

## API Reference

### Convenience Functions

#### `magic.from_file(filename, mime=False)`

Detect type information from file (uses shared instance).

**Parameters:**
- `filename` (str): File path
- `mime` (bool): Return MIME type, default False

**Returns:**
- str: File type information

#### `magic.from_buffer(buffer_data, mime=False)`

Detect type information from buffer data (uses shared instance).

**Parameters:**
- `buffer_data` (str/bytes): Buffer data
- `mime` (bool): Return MIME type, default False

**Returns:**
- str: Data type information

### Magic Class

#### `Magic(mime=False, mime_encoding=False)`

Create Magic instance.

**Parameters:**
- `mime` (bool): Return MIME type, default False
- `mime_encoding` (bool): Return MIME encoding, default False

#### `Magic.from_file(filename)`

Detect type from file.

#### `Magic.from_buffer(buffer_data)`

Detect type from buffer.

#### `Magic.close()`

Explicitly close resources.

#### Context Manager Support

```python
with Magic() as m:
    # Use m here
    pass
# Automatically closed
```

## Resource Management

This library provides intelligent resource management:

1. **Shared Instances**: `magic.from_file()` and `magic.from_buffer()` use global shared instances
2. **Context Manager**: `Magic` class supports `with` statement for automatic cleanup
3. **Explicit Control**: Call `close()` method for manual resource management
4. **No Memory Leaks**: Proper cleanup prevents resource leaks

## System Requirements

- Python 2.7 or Python 3.4+
- libmagic library (usually installed with system)
- Linux/Unix systems

## FAQ

### Q: What if libmagic library is not found?

A: The library automatically searches these paths:
- `/usr/lib64/libmagic.so.1.0.0`
- `/usr/lib64/libmagic.so.1`
- `/usr/lib64/libmagic.so`
- `/usr/lib/libmagic.so.1`
- Other standard paths

If still not found, install the `file` package:

```bash
# CentOS/RHEL
yum install file

# Ubuntu/Debian  
apt-get install file

# Or install development packages
yum install file-devel
apt-get install libmagic-dev
```

### Q: Difference from python-magic?

A: 
- **magic**: Uses ctypes to directly call libmagic, Python 2 compatible
- **python-magic**: Python 3 library, requires separate installation

### Q: Performance?

A: Due to direct C library calls, performance is comparable to python-magic, sometimes even better.

## License

MIT License

## Contributing

Issues and Pull Requests are welcome!

## Changelog

### v1.0.0 (2024-XX-XX)
- Initial release
- Support for Python 2.7 and Python 3
- Complete libmagic wrapper
- Auto library discovery
- Resource management with shared instances
- Context manager support
- Command line tool 
