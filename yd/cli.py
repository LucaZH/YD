import click
import os
from rich.console import Console
from rich.progress import Progress
from rich.table import Table
from .config import DEFAULT_SAVE_PATH
from .downloader import YouTubeDownloader
from .utils import get_available_formats, create_directory

console = Console()

@click.group()
def cli():
    pass

@cli.command()
@click.argument('url')
@click.option('--quality', '-q', type=click.Choice(['best', 'medium', '720p', '1080p', 'audio']), default='best')
@click.option('--output', '-o', default=DEFAULT_SAVE_PATH, help='Output directory')
@click.option('--list-formats', '-l', is_flag=True, help='List available formats')
@click.option('--format-id', '-f', help='Specific format ID to download')
def download(url, quality, output, list_formats, format_id):
    create_directory(output)
    downloader = YouTubeDownloader(output)
    
    if list_formats:
        formats = get_available_formats(url)
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Format ID", style="dim")
        table.add_column("Extension")
        table.add_column("Resolution")
        table.add_column("File Size (MB)")
        
        for fmt in formats:
            table.add_row(
                fmt['format_id'],
                fmt['ext'],
                fmt['resolution'],
                str(fmt['filesize'])
            )
        
        console.print("\n[bold]Available formats:[/bold]")
        console.print(table)
        return

    try:
        with Progress() as progress:
            task = progress.add_task("[cyan]Downloading...", total=100)
            def progress_hook(d):
                if d['status'] == 'downloading':
                    p = d.get('_percent_str', '0%').replace('%', '')
                    try:
                        progress.update(task, completed=float(p))
                    except ValueError:
                        pass
            
            downloader.download(url, quality, format_id, progress_hook)
            
        console.print("[green]Download completed successfully![/green]")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

@cli.command()
@click.argument('url')
def info(url):
    downloader = YouTubeDownloader(DEFAULT_SAVE_PATH)
    info = downloader.get_video_info(url)
    
    console.print("\n[bold cyan]Video Information:[/bold cyan]")
    console.print(f"Title: {info['title']}")
    console.print(f"Duration: {info['duration']} seconds")
    console.print(f"View Count: {info['view_count']}")
    console.print(f"Upload Date: {info['upload_date']}")
    console.print(f"Channel: {info['uploader']}")

@cli.command()
def version():
    console.print("[bold]YD - YouTube Downloader v1.0.0[/bold]")

if __name__ == '__main__':
    cli()