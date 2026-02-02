# OpenCode中使用yt-dlp技能指南

## 技能概述

yt-dlp技能允许您在OpenCode中直接下载视频。当用户提供视频链接时，您可以自动将视频下载到用户的下载目录。

## 技能位置

```
.opencode/skills/yt-dlp/
├── SKILL.md              # 技能定义
├── download_video.py     # 主Python脚本
├── ytdlp_skill.sh        # Bash包装脚本
├── example_usage.py      # 使用示例
├── test_skill.py         # 测试脚本
├── README.md             # 用户文档
└── USAGE_GUIDE.md        # 本指南
```

## 在OpenCode对话中使用

### 基本使用模式

当用户请求下载视频时：

1. **检查依赖**：确保yt-dlp已安装
2. **解析参数**：从用户消息中提取视频URL和选项
3. **执行下载**：调用下载脚本
4. **提供反馈**：向用户报告进度和结果

### 示例对话

**用户**: 请帮我下载这个YouTube视频：https://www.youtube.com/watch?v=dQw4w9WgXcQ

**助手**:
```
我将帮您下载这个YouTube视频。首先检查yt-dlp是否已安装...

✓ yt-dlp已安装 (版本: 2026.01.31)
开始下载: https://www.youtube.com/watch?v=dQw4w9WgXcQ
保存到: ~/Downloads/视频标题.mp4

下载进度: [████████████████████] 100%
下载完成！视频已保存到您的下载目录。
```

### 处理不同请求

#### 1. 简单下载请求
```python
# 用户: "下载 https://example.com/video"
# 响应: 使用默认设置下载
python .opencode/skills/yt-dlp/download_video.py "https://example.com/video"
```

#### 2. 音频提取请求
```python
# 用户: "把视频转成MP3"
# 响应: 提取音频
python .opencode/skills/yt-dlp/download_video.py "URL" -x --audio-format mp3
```

#### 3. 高质量下载请求
```python
# 用户: "下载1080p版本"
# 响应: 指定质量
python .opencode/skills/yt-dlp/download_video.py "URL" -q "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
```

#### 4. 带字幕下载
```python
# 用户: "下载带中文字幕的视频"
# 响应: 下载字幕
python .opencode/skills/yt-dlp/download_video.py "URL" -s --sub-lang zh
```

## 实现代码示例

### 检查yt-dlp是否安装
```python
import subprocess

def check_ytdlp_installed():
    try:
        result = subprocess.run(
            ["yt-dlp", "--version"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False
```

### 下载视频函数
```python
def download_video_for_user(url, options=None):
    """为用户下载视频"""
    
    # 检查yt-dlp
    if not check_ytdlp_installed():
        return "需要先安装yt-dlp。请运行: pip install yt-dlp"
    
    # 构建命令
    cmd = ["python", ".opencode/skills/yt-dlp/download_video.py", url]
    
    # 添加选项
    if options:
        if options.get("audio_only"):
            cmd.extend(["-x", "--audio-format", options.get("audio_format", "mp3")])
        if options.get("quality"):
            cmd.extend(["-q", options["quality"]])
        if options.get("subtitles"):
            cmd.extend(["-s", "--sub-lang", options.get("sub_lang", "zh,en")])
    
    # 执行下载
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            return f"下载成功！\n{result.stdout}"
        else:
            return f"下载失败：\n{result.stderr}"
            
    except Exception as e:
        return f"下载过程中出错：{e}"
```

## 错误处理

### 常见错误及处理

1. **yt-dlp未安装**
   ```
   响应: "需要先安装yt-dlp。正在尝试自动安装..."
   操作: pip install yt-dlp
   ```

2. **网络错误**
   ```
   响应: "网络连接失败，请检查网络后重试"
   操作: 建议用户检查网络或使用代理
   ```

3. **视频不可访问**
   ```
   响应: "无法访问该视频，可能是私密视频或链接无效"
   操作: 请用户提供有效的公开视频链接
   ```

4. **磁盘空间不足**
   ```
   响应: "磁盘空间不足，请清理下载目录后重试"
   操作: 提示用户清理 ~/Downloads 目录
   ```

## 最佳实践

### 1. 用户确认
在开始下载前，确认用户意图：
```
"我将下载这个视频到您的下载目录(~/Downloads)，确认吗？"
```

### 2. 进度反馈
提供实时进度反馈：
```
"开始下载... (0%)"
"下载中... (50%)"
"下载完成！(100%)"
```

### 3. 结果通知
下载完成后提供明确信息：
```
"下载完成！视频已保存到: ~/Downloads/视频标题.mp4"
"文件大小: 125 MB"
"下载时间: 2分30秒"
```

### 4. 安全提醒
添加适当的法律提醒：
```
"注意：请仅下载您有权访问的内容，并遵守相关平台的使用条款。"
```

## 技能集成示例

### 在OpenCode响应中使用
```python
# 解析用户消息
user_message = "请下载 https://www.youtube.com/watch?v=example"

if "下载" in user_message and "http" in user_message:
    # 提取URL
    import re
    url_match = re.search(r'https?://[^\s]+', user_message)
    if url_match:
        url = url_match.group(0)
        
        # 检查选项
        options = {}
        if "音频" in user_message or "mp3" in user_message:
            options["audio_only"] = True
        if "字幕" in user_message:
            options["subtitles"] = True
        
        # 执行下载
        result = download_video_for_user(url, options)
        print(result)
```

## 测试技能

### 快速测试
```bash
# 测试技能安装
python .opencode/skills/yt-dlp/test_skill.py

# 测试帮助功能
python .opencode/skills/yt-dlp/download_video.py --help

# 测试信息获取（不下载）
python .opencode/skills/yt-dlp/download_video.py "https://youtu.be/jNQXAC9IVRw" -i
```

### 完整测试流程
1. 安装yt-dlp: `pip install yt-dlp`
2. 运行测试: `python test_skill.py`
3. 测试下载: 使用一个简短的测试视频

## 更新和维护

### 更新yt-dlp
```bash
pip install --upgrade yt-dlp
```

### 更新技能
定期检查GitHub仓库更新：
```bash
cd .opencode/skills/yt-dlp
git pull origin main  # 如果有Git仓库
```

### 问题反馈
如果遇到问题：
1. 检查yt-dlp版本: `yt-dlp --version`
2. 查看错误信息
3. 更新到最新版本
4. 检查网络连接

## 法律和道德指南

使用本技能时，请确保：

1. **合法使用**: 仅下载公开可访问的内容
2. **尊重版权**: 不下载受版权保护的内容用于商业用途
3. **遵守条款**: 遵守各视频平台的服务条款
4. **个人使用**: 仅用于个人学习和研究目的

**免责声明**: 用户应对自己的下载行为负责。本技能开发者不对用户的下载行为承担任何法律责任。