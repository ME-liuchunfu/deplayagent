#!/bin/bash

# 检查是否安装了python3

python_command=python3.11

if ! command -v $python_command &> /dev/null
then
    echo "错误: python3 未安装，请先安装Python 3"
    exit 1
fi

# 检查是否安装了venv模块
#if ! $python_command -m venv --help &> /dev/null
#then
#    echo "错误: python3-venv 未安装，正在尝试安装..."
#    # 尝试安装venv模块（适用于Debian/Ubuntu系统）
#    if command -v apt-get &> /dev/null
#    then
#        sudo apt-get update
#        sudo apt-get install -y python3-venv
#    else
#        echo "请手动安装python3-venv或对应的Python虚拟环境包"
#        exit 1
#    fi
#fi

# 创建名为envs的虚拟环境
echo "正在创建名为'envs'的Python虚拟环境..."
$python_command -m venv envs

# 检查是否创建成功
if [ -d "envs" ]; then
    echo "虚拟环境创建成功！"
    echo "要激活虚拟环境，请运行: source envs/bin/activate"
else
    echo "虚拟环境创建失败"
    exit 1
fi

