from typing import Literal

from uvicorn import run

from watch2gether import __version__
from watch2gether import app
from watch2gether import convert_mp4_to_m3u8, streaming
from watch2gether import logger

Mode = Literal['error', 'info']


def convert_command(mp4_file: str,
                    m3u8_dir: str):
    """视频格式转换命令, 简化ffmpeg的使用,
    复杂功能请使用Python脚本模式.

    Example:
        ```shell
        w2g-cli convert ./flower.mp4 ./flower/
        ```

    Args:
        mp4_file: str,
            mp4文件的路径.
        m3u8_dir: str,
            m3u8文件夹的路径.
    """
    convert_mp4_to_m3u8(mp4_file, m3u8_dir)


def help_command(level: Mode):
    """帮助命令, 用于查看帮助信息.

    Example:
        ```shell
        w2g-cli help
        ```
    """
    _help_msg = f"""一起看电影命令行工具 {__version__}

Bunnyburrow Software Project(兔窝镇软件计划)
Copyright 2023 Steve R. Sun. All rights reserved.
--------------------------------------------------
usage:
  w2g-cli convert mp4_file m3u8_dir
    将视频从mp4格式转换成m3u8格式.
  w2g-cli help
    获取帮助信息.
  w2g-cli launch [--host] [--port] streaming_video
    启动流媒体服务和WebSocket服务.
    options:
      --host: 使用的主机地址, 默认为127.0.0.1.
      --port: 绑定的端口号, 默认为8000.
  w2g-cli version
    查看命令行工具版本.
"""

    if level == 'error':
        logger.error(_help_msg)
    else:
        logger.info(_help_msg)


def launch_command(video_dir: str,
                   host: str,
                   port: int):
    """启动服务命令, 用于启动流媒体服务和WebSocket服务.

    Example:
        ```shell
        w2g-cli launch ./flower/
        ```

    Args:
        video_dir: str,
            流媒体视频文件夹路径.
        host: str,
            使用的主机地址.
        port: int,
            绑定的端口号.
    """
    # 通过修改全局变量传递流媒体视频文件夹路径给流媒体服务.
    streaming.video_directory = video_dir

    run(app, host=host, port=port, log_level='error')


def version_command():
    """查看版本命令.

    Example:
        ```shell
        w2g-cli version
        ```
    """
    logger.info('一起看电影命令行工具 ' + __version__)