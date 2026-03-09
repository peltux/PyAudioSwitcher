# PyAudioSwitcher
用于音频设备快速切换

## 安装依赖

```bash
pip install -r requirements.txt
```

## 打包为 exe

### 安装打包工具

```bash
pip install pyinstaller
```

### 打包运行文件

```
pyinstaller --onefile switcher.py
```
运行文件在 dist 文件夹中。
