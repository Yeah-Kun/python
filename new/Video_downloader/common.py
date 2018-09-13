"""
	create by Ian in 2018-5-29 14:40:04
	视频下载的核心组件
"""
import argparse



def script_main(download, download_playlist, **kwargs):
	parser = argparse.ArgumentParser(
	        prog='mom-get',
	        usage='mom-get [OPTION]... URL...',
	        description='妈妈下载器，专注于给爸爸妈妈下载各种资源',
	        add_help=False,
	    )
	parser.add_argument(
	        '-V', '--version', action='store_true',
	        help='输出版本信息'
	    )
	parser.add_argument(
	        '-h', '--help', action='store_true',
	        help='输出帮助提示信息'
	    )
	
