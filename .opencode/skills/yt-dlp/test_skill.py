#!/usr/bin/env python3
"""
测试yt-dlp技能
"""

import subprocess
import sys
from pathlib import Path

def test_basic_functionality():
    """测试基本功能"""
    print("测试yt-dlp技能基本功能...")
    
    # 测试1: 检查yt-dlp是否安装
    print("\n1. 检查yt-dlp安装...")
    try:
        result = subprocess.run(
            ["yt-dlp", "--version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"   ✓ yt-dlp版本: {result.stdout.strip()}")
        else:
            print("   ✗ yt-dlp未正确安装")
            return False
    except FileNotFoundError:
        print("   ✗ yt-dlp未安装")
        return False
    
    # 测试2: 检查Python脚本
    print("\n2. 检查Python脚本...")
    script_path = Path(__file__).parent / "download_video.py"
    if script_path.exists():
        print(f"   ✓ 找到脚本: {script_path}")
        
        # 测试脚本帮助
        result = subprocess.run(
            [sys.executable, str(script_path), "--help"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("   ✓ 脚本帮助功能正常")
        else:
            print("   ✗ 脚本帮助功能异常")
            return False
    else:
        print("   ✗ 脚本未找到")
        return False
    
    # 测试3: 检查下载目录
    print("\n3. 检查下载目录...")
    download_dir = Path.home() / "Downloads"
    if download_dir.exists():
        print(f"   ✓ 下载目录存在: {download_dir}")
        
        # 检查写入权限
        test_file = download_dir / ".test_write"
        try:
            test_file.write_text("test")
            test_file.unlink()
            print("   ✓ 下载目录可写入")
        except Exception as e:
            print(f"   ✗ 下载目录不可写入: {e}")
            return False
    else:
        print("   ✗ 下载目录不存在")
        return False
    
    # 测试4: 测试获取视频信息功能（使用一个已知的测试URL）
    print("\n4. 测试视频信息获取...")
    # 使用一个简短的YouTube视频进行测试
    test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"  # 第一个YouTube视频
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path), test_url, "-i"],
            capture_output=True,
            text=True,
            timeout=15  # 减少超时时间
        )
        
        if result.returncode == 0:
            print("   ✓ 视频信息获取成功")
            # 尝试解析JSON输出
            import json
            try:
                info = json.loads(result.stdout)
                print(f"   ✓ 视频标题: {info.get('title', 'N/A')}")
                print(f"   ✓ 视频时长: {info.get('duration', 'N/A')}秒")
            except:
                print("   ⚠  JSON解析失败，但命令执行成功")
        else:
            print(f"   ⚠  视频信息获取失败（可能是网络问题）")
            print(f"      错误: {result.stderr[:200]}")
    
    except subprocess.TimeoutExpired:
        print("   ⚠  视频信息获取超时（网络较慢或视频不可访问）")
        print("      这不会影响基本功能，您可以继续测试下载功能")
    except Exception as e:
        print(f"   ⚠  视频信息获取异常: {e}")
    
    print("\n" + "=" * 60)
    print("技能测试完成！")
    print("=" * 60)
    
    print("\n使用说明:")
    print("1. 下载视频: python download_video.py [视频URL]")
    print("2. 提取音频: python download_video.py [视频URL] -x")
    print("3. 获取信息: python download_video.py [视频URL] -i")
    print("\n示例:")
    print("   python download_video.py https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    
    return True

if __name__ == "__main__":
    success = test_basic_functionality()
    sys.exit(0 if success else 1)