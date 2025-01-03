import click
from rich.console import Console
from rich.progress import Progress, TextColumn, BarColumn, SpinnerColumn, TimeElapsedColumn
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

        current_file = None
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=50),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%", justify="right"),
            TimeElapsedColumn(),
            expand=False,
            console=console,
            refresh_per_second=300
        ) as progress:
            info_task = progress.add_task("[yellow]Getting video info...", total=None)
            download_task = progress.add_task("[cyan]Downloading...", total=100, visible=False)
            merge_task = progress.add_task("[magenta]Merging formats...", total=None, visible=False)
            cleanup_task = progress.add_task("[red]Cleaning up...", total=None, visible=False)

            def progress_hook(d):
                nonlocal current_file
                
                if d['status'] == 'downloading':
                    
                    progress.update(info_task, visible=False)
                    progress.update(download_task, visible=True)
                    progress.update(merge_task, visible=False)
                    progress.update(cleanup_task, visible=False)

                    if 'filename' in d and current_file != d['filename']:
                        current_file = d['filename']
                        filename = current_file.split('\\')[-1]
                        progress.update(download_task, description=f"[cyan]{filename}")

                    try:
                        percentage = float(d.get('_percent_str', '0%').replace('%', ''))
                        progress.update(download_task, completed=percentage)
                    except ValueError:
                        pass

                elif d['status'] == 'extracting':
                    progress.update(info_task, visible=True)
                    progress.update(download_task, visible=False)
                    progress.update(merge_task, visible=False)
                    progress.update(cleanup_task, visible=False)

                elif d['status'] == 'merging':
                    progress.update(info_task, visible=False)
                    progress.update(download_task, visible=False)
                    progress.update(merge_task, visible=True)
                    progress.update(cleanup_task, visible=False)
                    
                elif d['status'] == 'deleting':
                    progress.update(info_task, visible=False)
                    progress.update(download_task, visible=False)
                    progress.update(merge_task, visible=False)
                    progress.update(cleanup_task, visible=True)
                    if 'filename' in d:
                        filename = d['filename'].split('\\')[-1]
                        progress.update(cleanup_task, description=f"[red]Removing {filename}")

            downloader.download(url, quality, format_id, progress_hook)
            
        console.print("[green]Download completed successfully![/green]")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

@cli.command()
@click.argument('url')
def info(url):
    try:
        downloader = YouTubeDownloader(DEFAULT_SAVE_PATH)
        info = downloader.get_video_info(url)
        
        console.print("\n[bold cyan]Video Information:[/bold cyan]")
        console.print(f"Title: {info['title']}")
        console.print(f"Duration: {info['duration']} seconds")
        console.print(f"View Count: {info['view_count']}")
        console.print(f"Upload Date: {info['upload_date']}")
        console.print(f"Channel: {info['uploader']}")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

@cli.command()
def version():
    console.print("[bold]YD - YouTube Downloader v1.0.0[/bold]")

if __name__ == '__main__':
    cli()