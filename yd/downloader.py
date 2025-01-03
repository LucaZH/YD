import yt_dlp
from .config import YDL_OPTS_BASE, QUALITY_FORMATS
import os

class YouTubeDownloader:
    def __init__(self, output_path):
        self.output_path = output_path
        
    def _get_ydl_opts(self, quality, format_id=None, progress_hook=None):
        opts = YDL_OPTS_BASE.copy()
        opts['outtmpl'] = os.path.join(self.output_path, '%(title)s.%(ext)s')
        
        if format_id:
            opts['format'] = format_id
        else:
            opts['format'] = QUALITY_FORMATS.get(quality, QUALITY_FORMATS['best'])
            
        if progress_hook:
            opts['progress_hooks'] = [progress_hook]
            
        return opts
    
    def download(self, url, quality='best', format_id=None, progress_hook=None):
        opts = self._get_ydl_opts(quality, format_id, progress_hook)
        
        with yt_dlp.YoutubeDL(opts) as ydl:
            try:
                ydl.download([url])
            except Exception as e:
                raise Exception(f"Download failed: {str(e)}")
    
    def get_video_info(self, url):
        with yt_dlp.YoutubeDL() as ydl:
            try:
                return yd.extract_info(url, download=False)
            except Exception as e:
                raise Exception(f"Failed to get video info: {str(e)}")