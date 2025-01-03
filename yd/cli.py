import click
from rich.console import Console
from rich.progress import Progress
from .config import DEFAULT_SAVE_PATH
from .downloader import YouTubeDownloader
from .utils import get_available_formats, create_directory, display_formats_table

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
@click.option('--interactive', '-i', is_flag=True, help='Interactive format selection')
def download(url, quality, output, list_formats, format_id, interactive):
    create_directory(output)
    downloader = YouTubeDownloader(output)
    
    try:
        formats = get_available_formats(url)
        
        if list_formats or interactive:
            display_formats_table(formats)
            
            if interactive:
                format_ids = [f['format_id'] for f in formats]
                while True:
                    format_id = click.prompt('Enter the Format ID you want to download', type=str)
                    if format_id in format_ids:
                        break
                    console.print("[red]Invalid Format ID. Please choose from the table above.[/red]")
        
        if not format_id and not interactive:
            console.print(f"[cyan]Using quality preset: {quality}[/cyan]")
            
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