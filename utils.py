import os
import yt_dlp

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_available_formats(url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            formats = []
            for f in info['formats']:
                format_dict = {
                    'format_id': f['format_id'],
                    'ext': f.get('ext', 'N/A'),
                    'resolution': f.get('resolution', 'N/A'),
                    'filesize_approx': f.get('filesize_approx', 0) // (1024 * 1024) 
                }
                formats.append(format_dict)
            return formats
        except Exception as e:
            raise Exception(f"Failed to get formats: {str(e)}")

def clean_temp_files(directory):
    temp_patterns = ['*.f[0-9]*.mp4', '*.f[0-9]*.m4a', '*.part', '*.temp']
    for pattern in temp_patterns:
        for file in glob.glob(os.path.join(directory, pattern)):
            try:
                os.remove(file)
            except OSError:
                pass