# yt-dlp 视频下载技能

基于yt-dlp开源项目的视频下载技能，支持从1000+视频平台下载视频到您的下载目录。

## 快速开始

### 1. 安装依赖

```bash
# 安装Python 3.7+ (如果尚未安装)
python3 --version

# 安装yt-dlp
pip install yt-dlp

# 安装FFmpeg (可选，用于格式转换)
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg
```

### 2. 使用技能

#### 基本下载
```bash
# 使用Python脚本
python download_video.py https://www.youtube.com/watch?v=dQw4w9WgXcQ

# 使用包装脚本
./ytdlp_skill.sh https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

#### 下载音频
```bash
python download_video.py https://www.youtube.com/watch?v=dQw4w9WgXcQ -x --audio-format mp3
```

#### 下载带字幕的视频
```bash
python download_video.py https://www.youtube.com/watch?v=dQw4w9WgXcQ -s --sub-lang zh
```

#### 下载播放列表
```bash
python download_video.py https://www.youtube.com/playlist?list=PLxxxx -p
```

## 在OpenCode中使用

当用户提供视频链接要求下载时，您可以：

1. 检查yt-dlp是否安装
2. 使用适当的参数调用下载脚本
3. 将视频下载到用户的下载目录

### 示例响应
```
我将帮您下载这个视频。首先检查yt-dlp是否已安装...

✓ yt-dlp已安装
开始下载: https://www.youtube.com/watch?v=dQw4w9WgXcQ
保存到: ~/Downloads/视频标题.mp4
下载进度: [████████████████████] 100%
下载完成！视频已保存到您的下载目录。
```

## 支持的平台

- YouTube
- Bilibili (哔哩哔哩)
- 抖音/TikTok
- Twitter/X
- Instagram
- Facebook
- 知乎
- 微博
- 以及1000+其他视频平台

## 高级功能

### 批量下载
创建`urls.txt`文件：
```
https://www.youtube.com/watch?v=video1
https://www.youtube.com/watch?v=video2
https://www.bilibili.com/video/BVxxxx
```

然后运行：
```bash
python download_video.py urls.txt -b
```

### 自定义输出路径
```bash
python download_video.py URL -o "~/Videos/%(title)s.%(ext)s"
```

### 指定视频质量
```bash
# 1080p或更低
python download_video.py URL -q "bestvideo[height<=1080]+bestaudio/best[height<=1080]"

# 仅720p
python download_video.py URL -q "best[height=720]"
```

## 故障排除

### 常见问题

1. **"yt-dlp未找到"错误**
   ```bash
   pip install yt-dlp
   ```

2. **网络错误**
   - 检查网络连接
   - 使用代理：`--proxy http://proxy:port`

3. **权限错误**
   ```bash
   chmod +x download_video.py ytdlp_skill.sh
   ```

4. **磁盘空间不足**
   - 清理下载目录
   - 指定其他输出路径

### 更新yt-dlp
```bash
pip install --upgrade yt-dlp
```

## 法律声明

本技能仅用于个人学习和研究目的。用户应遵守相关平台的服务条款和当地法律法规。不得用于侵犯版权的行为。

## 文件说明

- `SKILL.md` - 技能定义文件
- `download_video.py` - 主Python脚本
- `ytdlp_skill.sh` - Bash包装脚本
- `example_usage.py` - 使用示例
- `README.md` - 本文档