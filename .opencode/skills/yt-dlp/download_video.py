#!/usr/bin/env python3
"""
yt-dlp视频下载脚本
自动将视频下载到用户的下载目录
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
import json
from typing import Optional, Dict, List

def get_download_dir() -> Path:
    """获取用户下载目录"""
    # 尝试获取用户下载目录
    if sys.platform == "darwin":  # macOS
        download_dir = Path.home() / "Downloads"
    elif sys.platform == "win32":  # Windows
        download_dir = Path.home() / "Downloads"
    else:  # Linux/Unix
        download_dir = Path.home() / "Downloads"
    
    # 如果下载目录不存在，创建它
    download_dir.mkdir(parents=True, exist_ok=True)
    return download_dir

def check_ytdlp_installed() -> bool:
    """检查yt-dlp是否已安装"""
    try:
        result = subprocess.run(
            ["yt-dlp", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def install_ytdlp() -> bool:
    """安装yt-dlp"""
    print("正在安装yt-dlp...")
    try:
        # 使用pip安装yt-dlp
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"],
            check=True,
            capture_output=True,
            text=True
        )
        print("yt-dlp安装成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"安装失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False

def get_video_info(url: str) -> Optional[Dict]:
    """获取视频信息"""
    try:
        result = subprocess.run(
            ["yt-dlp", "--dump-json", url],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            print(f"获取视频信息失败: {result.stderr}")
            return None
    except (subprocess.SubprocessError, json.JSONDecodeError) as e:
        print(f"获取视频信息时出错: {e}")
        return None

def download_video(
    url: str,
    output_template: Optional[str] = None,
    quality: str = "best",
    extract_audio: bool = False,
    audio_format: str = "mp3",
    download_subtitles: bool = False,
    subtitle_lang: str = "zh,en",
    playlist: bool = False,
    concurrent_downloads: int = 1
) -> bool:
    """下载视频"""
    
    # 获取下载目录
    download_dir = get_download_dir()
    
    # 设置输出模板
    if output_template is None:
        if playlist:
            output_template = f"{download_dir}/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s"
        else:
            output_template = f"{download_dir}/%(title)s.%(ext)s"
    
    # 构建命令
    cmd = ["yt-dlp"]
    
    # 添加输出选项
    cmd.extend(["-o", output_template])
    
    # 添加质量选项
    if quality != "best":
        cmd.extend(["-f", quality])
    
    # 添加音频提取选项
    if extract_audio:
        cmd.extend(["-x", "--audio-format", audio_format])
    
    # 添加字幕选项
    if download_subtitles:
        cmd.extend(["--write-subs"])
        if subtitle_lang:
            cmd.extend(["--sub-lang", subtitle_lang])
    
    # 添加播放列表选项
    if not playlist:
        cmd.append("--no-playlist")
    
    # 添加并发下载选项
    if concurrent_downloads > 1:
        cmd.extend(["-N", str(concurrent_downloads)])
    
    # 添加进度显示选项
    cmd.extend(["--progress", "--newline"])
    
    # 添加重试选项
    cmd.extend(["--retries", "3"])
    
    # 添加视频URL
    cmd.append(url)
    
    print(f"开始下载: {url}")
    print(f"保存到: {output_template}")
    print(f"命令: {' '.join(cmd)}")
    print("-" * 50)
    
    try:
        # 执行下载命令
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # 实时输出进度
        if process.stdout:
            for line in process.stdout:
                print(line.strip())
        
        process.wait()
        
        if process.returncode == 0:
            print("下载完成！")
            return True
        else:
            print(f"下载失败，退出码: {process.returncode}")
            return False
            
    except KeyboardInterrupt:
        print("\n下载被用户中断")
        return False
    except Exception as e:
        print(f"下载过程中出错: {e}")
        return False

def batch_download(urls_file: str, **kwargs) -> bool:
    """批量下载"""
    try:
        with open(urls_file, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        print(f"找到 {len(urls)} 个视频链接")
        
        success_count = 0
        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}] 处理: {url}")
            if download_video(url, **kwargs):
                success_count += 1
        
        print(f"\n批量下载完成！成功: {success_count}/{len(urls)}")
        return success_count > 0
        
    except FileNotFoundError:
        print(f"文件未找到: {urls_file}")
        return False
    except Exception as e:
        print(f"批量下载出错: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="yt-dlp视频下载工具")
    parser.add_argument("url", nargs="?", help="视频URL或包含URL列表的文件")
    parser.add_argument("-o", "--output", help="输出路径模板")
    parser.add_argument("-q", "--quality", default="best", help="视频质量 (默认: best)")
    parser.add_argument("-x", "--extract-audio", action="store_true", help="提取音频")
    parser.add_argument("--audio-format", default="mp3", help="音频格式 (默认: mp3)")
    parser.add_argument("-s", "--subtitles", action="store_true", help="下载字幕")
    parser.add_argument("--sub-lang", default="zh,en", help="字幕语言 (默认: zh,en)")
    parser.add_argument("-p", "--playlist", action="store_true", help="下载播放列表")
    parser.add_argument("-N", "--concurrent", type=int, default=1, help="同时下载数量 (默认: 1)")
    parser.add_argument("-b", "--batch", action="store_true", help="批量下载模式")
    parser.add_argument("-i", "--info", action="store_true", help="仅获取视频信息")
    
    args = parser.parse_args()
    
    # 检查yt-dlp是否安装
    if not check_ytdlp_installed():
        print("yt-dlp未安装，正在尝试安装...")
        if not install_ytdlp():
            print("请手动安装yt-dlp: pip install yt-dlp")
            sys.exit(1)
    
    # 如果指定了批量模式
    if args.batch and args.url:
        kwargs = {
            "output_template": args.output,
            "quality": args.quality,
            "extract_audio": args.extract_audio,
            "audio_format": args.audio_format,
            "download_subtitles": args.subtitles,
            "subtitle_lang": args.sub_lang,
            "playlist": args.playlist,
            "concurrent_downloads": args.concurrent
        }
        success = batch_download(args.url, **kwargs)
        sys.exit(0 if success else 1)
    
    # 如果仅获取信息
    if args.info and args.url:
        info = get_video_info(args.url)
        if info:
            print(json.dumps(info, indent=2, ensure_ascii=False))
        sys.exit(0 if info else 1)
    
    # 正常下载
    if args.url:
        success = download_video(
            url=args.url,
            output_template=args.output,
            quality=args.quality,
            extract_audio=args.extract_audio,
            audio_format=args.audio_format,
            download_subtitles=args.subtitles,
            subtitle_lang=args.sub_lang,
            playlist=args.playlist,
            concurrent_downloads=args.concurrent
        )
        sys.exit(0 if success else 1)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()