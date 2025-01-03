import os
import glob
import yt_dlp
from rich.table import Table
from rich.console import Console

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def format_filesize(size_in_bytes):
    if size_in_bytes is None:
        return "N/A"
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.1f} {unit}"
        size_in_bytes /= 1024
    return f"{size_in_bytes:.1f} TB"

def get_format_quality(format_dict):
    if format_dict.get('height'):
        return f"{format_dict['height']}p"
    elif format_dict.get('abr'):
        return f"{format_dict['abr']}kbps"
    return "N/A"

def safe_get(dictionary, key, default=0):
    value = dictionary.get(key)
    return default if value is None else value

def get_available_formats(url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            formats = []
            
            best_audio = next((f for f in info['formats'] 
                             if f.get('acodec') != 'none' and f.get('vcodec') == 'none'), None)
            
            for f in info['formats']:
                if f.get('vcodec') == 'none':
                    continue
                video_size = f.get('filesize') or f.get('filesize_approx') or 0
                audio_size = best_audio.get('filesize') or best_audio.get('filesize_approx') or 0 if best_audio else 0
                total_size = video_size + audio_size if f.get('acodec') == 'none' else video_size
                
                quality = get_format_quality(f)
                format_dict = {
                    'format_id': f['format_id'],
                    'ext': f.get('ext', 'N/A'),
                    'resolution': quality,
                    'filesize': format_filesize(total_size),
                    'fps': safe_get(f, 'fps', 'N/A'),
                    'tbr': safe_get(f, 'tbr', 0),
                    'has_audio': f.get('acodec') != 'none',
                    'format_note': f.get('format_note', '')
                }
                formats.append(format_dict)
            
            formats.sort(key=lambda x: (
                int(x['resolution'].replace('p', '')) if x['resolution'] != 'N/A' else 0,
                x['fps'] if x['fps'] != 'N/A' else 0
            ), reverse=True)
            
            return formats
            
        except Exception as e:
            raise Exception(f"Failed to get formats: {str(e)}")

def display_formats_table(formats):
    table = Table(title="Available Video Formats (All Include Audio)", 
                 show_header=True, header_style="bold magenta")
    
    table.add_column("Format ID", style="dim")
    table.add_column("Extension")
    table.add_column("Resolution")
    table.add_column("FPS")
    table.add_column("Estimated Size")
    table.add_column("Notes")
    
    for fmt in formats:
        table.add_row(
            fmt['format_id'],
            fmt['ext'],
            fmt['resolution'],
            str(fmt['fps']) if fmt['fps'] != 'N/A' else '-',
            fmt['filesize'],
            f"{fmt['format_note']}"
        )
    
    console = Console()
    console.print("\n[bold]All formats will be downloaded with audio![/bold]")
    console.print(table)
    console.print("\n[italic]Note: File sizes are estimates and include both video and audio[/italic]")