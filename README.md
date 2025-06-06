# python2-magic

一个 Python 2 兼容的 magic 库包装器，使用 ctypes 直接调用 libmagic，无需安装 python-magic。

## 特性

- **Python 2 兼容**：专为 Python 2.7 设计，同时兼容 Python 3
- **无额外依赖**：只使用 Python 标准库，通过 ctypes 直接调用 libmagic
- **简单易用**：提供与 python-magic 兼容的 API
- **高性能**：直接调用 C 库，性能优异
- **自动库发现**：自动搜索系统中的 libmagic 库

## 安装

### 从 wheel 安装

```bash
pip install python2-magic-1.0.0-py2.py3-none-any.whl
```

### 从源码安装

```bash
python setup.py install
```

### 构建 wheel

```bash
python setup.py bdist_wheel
```

## 使用方法

### 基本用法

```python
import magic_wrapper

# 检测文件类型
file_type = magic_wrapper.magic_from_file('/path/to/file')
print("文件类型: %s" % file_type)

# 检测 MIME 类型
mime_type = magic_wrapper.magic_from_file('/path/to/file', mime=True)
print("MIME 类型: %s" % mime_type)

# 检测缓冲区内容
buffer_content = "#!/bin/bash\necho 'Hello World'"
buffer_type = magic_wrapper.magic_from_buffer(buffer_content)
print("缓冲区类型: %s" % buffer_type)
```

### 面向对象接口

```python
from magic_wrapper import Magic

# 创建 Magic 实例
m = Magic()
file_type = m.from_file('/path/to/file')

# 创建 MIME 类型检测实例
mime_magic = Magic(mime=True)
mime_type = mime_magic.from_file('/path/to/file')

# 创建 MIME 编码检测实例
encoding_magic = Magic(mime_encoding=True)
encoding = encoding_magic.from_file('/path/to/file')
```

## API 参考

### 便捷函数

#### `magic_from_file(filename, mime=False)`

从文件检测类型信息。

**参数：**
- `filename` (str): 文件路径
- `mime` (bool): 是否返回 MIME 类型，默认 False

**返回：**
- str: 文件类型信息

#### `magic_from_buffer(buffer_data, mime=False)`

从缓冲区数据检测类型信息。

**参数：**
- `buffer_data` (str/bytes): 缓冲区数据
- `mime` (bool): 是否返回 MIME 类型，默认 False

**返回：**
- str: 数据类型信息

### Magic 类

#### `Magic(mime=False, mime_encoding=False)`

创建 Magic 实例。

**参数：**
- `mime` (bool): 返回 MIME 类型，默认 False
- `mime_encoding` (bool): 返回 MIME 编码，默认 False

#### `Magic.from_file(filename)`

从文件检测类型。

#### `Magic.from_buffer(buffer_data)`

从缓冲区检测类型。

## 系统要求

- Python 2.7 或 Python 3.4+
- libmagic 库（通常随系统安装）
- Linux/Unix 系统

## 常见问题

### Q: 找不到 libmagic 库怎么办？

A: 库会自动搜索以下路径：
- `/usr/lib64/libmagic.so.1.0.0`
- `/usr/lib64/libmagic.so.1`
- `/usr/lib64/libmagic.so`
- `/usr/lib/libmagic.so.1`
- 其他标准路径

如果仍然找不到，请安装 `file` 包：

```bash
# CentOS/RHEL
yum install file

# Ubuntu/Debian  
apt-get install file

# 或安装开发包
yum install file-devel
apt-get install libmagic-dev
```

### Q: 与 python-magic 的区别？

A: 
- **python2-magic**: 使用 ctypes 直接调用 libmagic，Python 2 兼容
- **python-magic**: Python 3 库，需要额外安装

### Q: 性能如何？

A: 由于直接调用 C 库，性能与 python-magic 相当，甚至更好。

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 更新日志

### v1.0.0 (2024-XX-XX)
- 初始版本
- 支持 Python 2.7 和 Python 3
- 提供完整的 libmagic 包装
- 自动库发现功能 