# YD

Youtube Video Downloader

### Description

YD is a command-line tool for downloading YouTube videos in various formats and qualities. It provides an interactive way to choose the video format and quality, and it also supports listing available formats and displaying video information.

## Usage

### Command: `download`

Download a YouTube video in the desired format and quality.

```bash
yd download <url> [options]
```

#### Arguments:

- `url`: The YouTube URL of the video you want to download.

#### Options:

- `--quality`, `-q`: The quality preset to download. Available choices: `best`, `medium`, `720p`, `1080p`, `audio` (default: `best`).
- `--output`, `-o`: The output directory where the video will be saved (default: `DEFAULT_SAVE_PATH`).
- `--list-formats`, `-l`: List the available formats for the video.
- `--format-id`, `-f`: Specify a specific format ID to download.
- `--interactive`, `-i`: Choose an interactive way to select the format.

#### Example:

```bash
yd download https://youtube.com/watch?v=gset79KMmt0 --quality 1080p
```

By default the file is saved into the `Downloads` Folder

### Command: `info`

Get information about a YouTube video.

```bash
yd info <url>
```

#### Arguments:

- `url`: The YouTube URL of the video you want information about.

#### Example:

```bash
yd info https://youtube.com/watch?v=gset79KMmt0
```

### Command: `version`

Display the version of the YouTube Downloader.

```bash
yd version
```

#### Example:

```bash
yd version
```

### Todo

- [ ] Add installation guide
- [ ] Add more download options (e.g., subtitles)
- [ ] Add an option for users to choose their preferred download format (currently, it is automatically selected by default by yt_dlp)
