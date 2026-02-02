#!/bin/bash
# yt-dlp技能包装脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/download_video.py"

# 检查Python脚本是否存在
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "错误: 找不到Python脚本 $PYTHON_SCRIPT"
    exit 1
fi

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到python3，请先安装Python 3.7+"
    exit 1
fi

# 检查yt-dlp是否安装
if ! command -v yt-dlp &> /dev/null; then
    echo "警告: yt-dlp未安装，尝试自动安装..."
    if python3 -m pip install --upgrade yt-dlp; then
        echo "yt-dlp安装成功！"
    else
        echo "安装失败，请手动安装: pip install yt-dlp"
        exit 1
    fi
fi

# 运行Python脚本
python3 "$PYTHON_SCRIPT" "$@"