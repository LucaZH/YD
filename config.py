import os

DEFAULT_SAVE_PATH = os.path.join(os.path.expanduser("~"), "Downloads", "YD")

QUALITY_FORMATS = {
    'best': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'medium': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best',
    '720p': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best',
    '1080p': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best',
    'audio': 'bestaudio[ext=m4a]/best'
}

YDL_OPTS_BASE = {
    'format': QUALITY_FORMATS['best'],
    'merge_output_format': 'mp4',
    'prefer_ffmpeg': True,
    'keepvideo': False,
    'postprocessors': [{
        'key': 'FFmpegVideoConvertor',
        'preferedformat': 'mp4',
    }]
}