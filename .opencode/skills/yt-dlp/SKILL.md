---
name: yt-dlp
description: "YouTube视频下载工具。使用yt-dlp从YouTube、Bilibili等视频平台下载视频到用户的下载目录。支持多种视频格式和质量选择，自动处理视频信息提取和下载。"
compatibility: "OpenCode with Python 3.x and yt-dlp installed"
---

# yt-dlp 视频下载技能

基于yt-dlp开源项目的视频下载工具，支持从YouTube、Bilibili、抖音等1000+视频平台下载视频。

## 功能特性

- 自动下载视频到用户下载目录（~/Downloads）
- 支持多种视频格式和质量选择
- 自动提取视频标题、描述、作者等信息
- 支持播放列表下载
- 支持字幕下载
- 支持音频提取
- 断点续传功能

## 安装要求

### 1. 安装Python 3.7+
```bash
python3 --version || python --version
```

### 2. 安装yt-dlp
```bash
pip install yt-dlp
```

### 3. 安装FFmpeg（可选，用于格式转换）
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# Windows (使用chocolatey)
choco install ffmpeg
```

## 使用示例

### 基本下载（最高质量）
```bash
yt-dlp -o "~/Downloads/%(title)s.%(ext)s" "视频URL"
```

### 指定质量
```bash
yt-dlp -f "bestvideo[height<=1080]+bestaudio/best[height<=1080]" -o "~/Downloads/%(title)s.%(ext)s" "视频URL"
```

### 下载音频
```bash
yt-dlp -x --audio-format mp3 -o "~/Downloads/%(title)s.%(ext)s" "视频URL"
```

### 下载播放列表
```bash
yt-dlp -o "~/Downloads/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s" "播放列表URL"
```

## 常用命令参数

| 参数 | 说明 |
|------|------|
| `-o PATH` | 指定输出路径模板 |
| `-f FORMAT` | 指定视频格式/质量 |
| `-x` | 提取音频 |
| `--audio-format FORMAT` | 指定音频格式 |
| `--write-subs` | 下载字幕 |
| `--sub-lang LANG` | 指定字幕语言 |
| `--playlist-start NUMBER` | 播放列表起始位置 |
| `--playlist-end NUMBER` | 播放列表结束位置 |
| `--no-playlist` | 只下载单个视频 |
| `-N NUMBER` | 同时下载数量 |

## 输出路径模板变量

| 变量 | 说明 |
|------|------|
| `%(title)s` | 视频标题 |
| `%(id)s` | 视频ID |
| `%(ext)s` | 文件扩展名 |
| `%(uploader)s` | 上传者名称 |
| `%(upload_date)s` | 上传日期 |
| `%(playlist)s` | 播放列表名称 |
| `%(playlist_index)s` | 播放列表索引 |

## 错误处理

1. **网络错误**: 自动重试3次
2. **格式错误**: 尝试备用格式
3. **权限错误**: 检查下载目录权限
4. **磁盘空间不足**: 提示用户清理空间

## 安全注意事项

- 仅下载公开可访问的视频
- 遵守平台的使用条款
- 不下载受版权保护的内容
- 不用于商业用途

## 扩展功能

### 批量下载
创建下载列表文件 `urls.txt`:
```bash
yt-dlp -a urls.txt -o "~/Downloads/%(title)s.%(ext)s"
```

### 自定义配置
创建配置文件 `~/.config/yt-dlp/config`:
```yaml
-o: ~/Downloads/%(title)s.%(ext)s
--no-mtime
--write-thumbnail
--convert-thumbnails png
```

### 进度显示
```bash
yt-dlp --progress --newline "视频URL"
```

## 故障排除

### 常见问题
1. **yt-dlp未找到**: 确保已正确安装 `pip install yt-dlp`
2. **FFmpeg错误**: 安装FFmpeg或使用 `--no-post-overwrites`
3. **权限错误**: 检查下载目录写入权限
4. **网络错误**: 检查网络连接，使用代理 `--proxy URL`

### 更新yt-dlp
```bash
pip install --upgrade yt-dlp
```

## 平台支持

- YouTube
- Bilibili
- 抖音/TikTok
- Twitter/X
- Instagram
- Facebook
- 知乎
- 微博
- 以及1000+其他平台

## 法律声明

本技能仅用于个人学习和研究目的。用户应遵守相关平台的服务条款和当地法律法规。不得用于侵犯版权的行为。