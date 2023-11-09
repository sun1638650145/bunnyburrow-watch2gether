import argparse
import sys

from typing import List

from watch2gether.experimental_command_wrapper import (
    convert_command,
    help_command,
    version_command
)


class LocalizedArgumentParser(argparse.ArgumentParser):
    """本地化命令行参数解析器."""
    def error(self, message: str):
        """输出使用方法和错误消息.

        Args:
            message: str
                错误消息.
        """
        message = message.replace('unrecognized arguments', '未识别的参数')
        message = message.replace('the following arguments are required',
                                  '需要以下参数')

        self.print_usage()
        sys.stderr.write(f'错误: {message}\n')
        sys.exit(2)

    def format_help(self):
        """格式化帮助信息."""
        message = super().format_help()

        message = message.replace('usage', '使用方法')
        message = message.replace('positional arguments', '参数')
        message = message.replace('optional arguments', '帮助参数')
        message = message.replace('show this help message and exit',
                                  '显示帮助信息并退出.')

        return message

    def format_usage(self):
        """格式化使用方法."""
        message = super().format_usage()

        message = message.replace('usage', '使用方法')

        return message


def parse_args(args: List[str]) -> argparse.Namespace:
    """解析命令行参数.

    Args:
        args: list of str,
            命令行参数组成的字符串列表.

    Return:
        (解析后)参数组成的容器.
    """
    parser = LocalizedArgumentParser(usage='w2g-cli {convert, help, version}',
                                     add_help=False,
                                     exit_on_error=False)
    subparsers = parser.add_subparsers(dest='command')

    if len(args) < 2:  # 没有参数.
        help_command()
        sys.exit(2)
    else:
        args = args[1:]

        # 转换视频格式命令.
        convert_parser = subparsers.add_parser('convert',
                                               usage='w2g-cli convert mp4_filepath m3u8_directory',  # noqa: E501
                                               description='将视频从mp4格式转换成m3u8格式.')  # noqa: E501
        convert_parser.add_argument('mp4_filepath', help='mp4文件的路径.')
        convert_parser.add_argument('m3u8_directory', help='m3u8文件夹的路径.')

        # 帮助命令.
        subparsers.add_parser('help',
                              usage='w2g-cli help',
                              add_help=False,
                              description='获取帮助信息.')

        # 查看版本命令.
        subparsers.add_parser('version',
                              usage='w2g-cli version',
                              add_help=False,
                              description='查看命令行工具版本.')

        return parser.parse_args(args)


def run():
    """启动命令行工具."""
    try:
        args = parse_args(sys.argv)

        if args.command == 'convert':
            convert_command(args.mp4_filepath, args.m3u8_directory)
        elif args.command == 'help':
            help_command()
        elif args.command == 'version':
            version_command()
    except argparse.ArgumentError:
        help_command()
        sys.exit(2)
