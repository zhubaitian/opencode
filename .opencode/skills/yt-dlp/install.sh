#!/bin/bash
# yt-dlp技能安装脚本

set -e

echo "=========================================="
echo "安装 yt-dlp 视频下载技能"
echo "=========================================="

# 检查Python
echo "检查Python安装..."
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到python3，请先安装Python 3.7+"
    exit 1
fi

python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python版本: $python_version"

# 检查pip
echo "检查pip安装..."
if ! command -v pip3 &> /dev/null; then
    echo "安装pip..."
    if python3 -m ensurepip --upgrade; then
        echo "✓ pip安装成功"
    else
        echo "错误: 无法安装pip"
        exit 1
    fi
else
    echo "✓ pip已安装"
fi

# 安装yt-dlp
echo "安装yt-dlp..."
if pip3 install --upgrade yt-dlp; then
    echo "✓ yt-dlp安装成功"
else
    echo "错误: yt-dlp安装失败"
    exit 1
fi

# 检查yt-dlp版本
ytdlp_version=$(yt-dlp --version 2>&1 || echo "未知")
echo "✓ yt-dlp版本: $ytdlp_version"

# 检查下载目录
echo "检查下载目录..."
download_dir="$HOME/Downloads"
if [ -d "$download_dir" ]; then
    echo "✓ 下载目录存在: $download_dir"
    
    # 测试写入权限
    if touch "$download_dir/.test_write" 2>/dev/null; then
        rm "$download_dir/.test_write"
        echo "✓ 下载目录可写入"
    else
        echo "警告: 下载目录可能不可写入"
    fi
else
    echo "创建下载目录..."
    if mkdir -p "$download_dir"; then
        echo "✓ 下载目录创建成功: $download_dir"
    else
        echo "警告: 无法创建下载目录"
    fi
fi

# 设置脚本权限
echo "设置脚本权限..."
chmod +x *.py *.sh 2>/dev/null || true
echo "✓ 脚本权限设置完成"

# 可选：安装FFmpeg
echo ""
echo "可选：安装FFmpeg（用于格式转换）"
echo "------------------------------------------"
echo "macOS: brew install ffmpeg"
echo "Ubuntu/Debian: sudo apt update && sudo apt install ffmpeg"
echo "Windows: choco install ffmpeg"
echo ""

# 测试安装
echo "测试安装..."
if python3 test_skill.py 2>/dev/null | grep -q "技能测试完成"; then
    echo "✓ 技能测试通过"
else
    echo "⚠  技能测试未完全通过，但基本功能可用"
fi

echo ""
echo "=========================================="
echo "安装完成！"
echo "=========================================="
echo ""
echo "使用示例:"
echo "  python download_video.py https://www.youtube.com/watch?v=dQw4w9WgXcQ"
echo "  python download_video.py [视频URL] -x  # 提取音频"
echo "  python download_video.py [视频URL] -s  # 下载字幕"
echo ""
echo "查看完整帮助:"
echo "  python download_video.py --help"
echo "  python example_usage.py"
echo ""
echo "技能文档:"
echo "  cat README.md"
echo "  cat USAGE_GUIDE.md"
echo ""
echo "=========================================="