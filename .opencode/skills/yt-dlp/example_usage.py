#!/usr/bin/env python3
"""
yt-dlp技能使用示例
"""

import subprocess
import sys
from pathlib import Path

def run_example():
    """运行使用示例"""
    
    print("=" * 60)
    print("yt-dlp视频下载技能使用示例")
    print("=" * 60)
    
    # 示例1: 基本下载
    print("\n1. 基本下载示例:")
    print("   下载YouTube视频到下载目录")
    print("   python download_video.py https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    
    # 示例2: 指定质量
    print("\n2. 指定质量下载:")
    print("   下载1080p视频")
    print("   python download_video.py https://www.youtube.com/watch?v=dQw4w9WgXcQ -q 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'")
    
    # 示例3: 提取音频
    print("\n3. 提取音频:")
    print("   提取视频音频为MP3")
    print("   python download_video.py https://www.youtube.com/watch?v=dQw4w9WgXcQ -x --audio-format mp3")
    
    # 示例4: 下载字幕
    print("\n4. 下载带字幕的视频:")
    print("   下载视频和中文字幕")
    print("   python download_video.py https://www.youtube.com/watch?v=dQw4w9WgXcQ -s --sub-lang zh")
    
    # 示例5: 下载播放列表
    print("\n5. 下载播放列表:")
    print("   下载整个播放列表")
    print("   python download_video.py https://www.youtube.com/playlist?list=PLxxxx -p")
    
    # 示例6: 批量下载
    print("\n6. 批量下载:")
    print("   从文件批量下载")
    print("   echo 'https://www.youtube.com/watch?v=video1' > urls.txt")
    print("   echo 'https://www.youtube.com/watch?v=video2' >> urls.txt")
    print("   python download_video.py urls.txt -b")
    
    # 示例7: 获取视频信息
    print("\n7. 获取视频信息:")
    print("   仅获取视频信息不下载")
    print("   python download_video.py https://www.youtube.com/watch?v=dQw4w9WgXcQ -i")
    
    print("\n" + "=" * 60)
    print("常用平台URL格式:")
    print("-" * 60)
    print("YouTube:     https://www.youtube.com/watch?v=VIDEO_ID")
    print("Bilibili:    https://www.bilibili.com/video/BVxxxx")
    print("抖音:        https://www.douyin.com/video/VIDEO_ID")
    print("Twitter/X:   https://twitter.com/user/status/TWEET_ID")
    print("Instagram:   https://www.instagram.com/p/POST_ID")
    print("知乎:        https://www.zhihu.com/zvideo/VIDEO_ID")
    print("=" * 60)

def test_installation():
    """测试安装"""
    print("\n测试yt-dlp安装...")
    try:
        result = subprocess.run(
            ["yt-dlp", "--version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✓ yt-dlp已安装: {result.stdout.strip()}")
            return True
        else:
            print("✗ yt-dlp未正确安装")
            return False
    except FileNotFoundError:
        print("✗ yt-dlp未安装")
        return False

def check_download_dir():
    """检查下载目录"""
    download_dir = Path.home() / "Downloads"
    if download_dir.exists():
        print(f"✓ 下载目录: {download_dir}")
        return True
    else:
        print(f"✗ 下载目录不存在: {download_dir}")
        return False

if __name__ == "__main__":
    print("运行环境检查...")
    test_installation()
    check_download_dir()
    run_example()
    
    print("\n提示: 要使用此技能，请确保:")
    print("1. 已安装Python 3.7+")
    print("2. 已安装yt-dlp: pip install yt-dlp")
    print("3. 下载目录 (~/Downloads) 存在且有写入权限")
    print("\n开始使用: python download_video.py [视频URL]")