# Insta360 X4 to Instagram Reels/YouTube Shorts Converter

Convert Insta360 X4 .insv dual-fisheye videos into 9:16 vertical shorts for Instagram Reels and YouTube Shorts, with automatic splitting, lens selection, yaw control, and adjustable FOV.

## Features

- Proper fisheye-to-rectilinear reprojection using ffmpeg's `v360` filter
- Dual lens support (front and back camera streams from a single .insv file)
- Horizontal pan control (yaw) within each lens
- Adjustable field of view (zoom in/out)
- Automatic splitting of long videos into 2-minute segments
- Batch processing of multiple .insv files
- Three quality presets (high/medium/low)
- Fast-start enabled for web playback
- Preserves audio (192kbps AAC, 48kHz)

## Requirements

- Python 3.6+
- ffmpeg (with v360 filter support)

## Installation

### 1. Install ffmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

### 2. Download the script

```bash
git clone https://github.com/JimWas/JimWas-Insta360-INSV-to-Shorts.git
cd JimWas-Insta360-INSV-to-Shorts
```

## Usage

### Basic (convert all .insv files in current directory)

```bash
python JimWas-INSTA360-INSV-TO-SHORTS.PY
```

### Select lens

The Insta360 X4 stores both lenses as separate video streams in a single .insv file.

```bash
# Front lens (screen side) - default
python JimWas-INSTA360-INSV-TO-SHORTS.PY --lens front

# Back lens (opposite side)
python JimWas-INSTA360-INSV-TO-SHORTS.PY --lens back
```

### Pan the view (yaw)

Control which direction the camera faces within the fisheye. 0 = straight ahead, negative = left, positive = right.

```bash
# Pan left
python JimWas-INSTA360-INSV-TO-SHORTS.PY --yaw -40

# Pan right
python JimWas-INSTA360-INSV-TO-SHORTS.PY --yaw 40
```

Usable range is roughly -80 to 80 degrees per lens. Beyond that you'll see black (edge of fisheye).

### Adjust field of view

Lower FOV = zoomed in, higher FOV = wider angle.

```bash
# Zoomed in
python JimWas-INSTA360-INSV-TO-SHORTS.PY --fov 50

# Default
python JimWas-INSTA360-INSV-TO-SHORTS.PY --fov 80

# Wide angle
python JimWas-INSTA360-INSV-TO-SHORTS.PY --fov 110
```

### Other options

```bash
# Custom segment duration (60 seconds for YouTube Shorts)
python JimWas-INSTA360-INSV-TO-SHORTS.PY -d 60

# Medium quality for faster processing
python JimWas-INSTA360-INSV-TO-SHORTS.PY -q medium

# Specify output directory
python JimWas-INSTA360-INSV-TO-SHORTS.PY -o ./output

# Convert a specific file
python JimWas-INSTA360-INSV-TO-SHORTS.PY video.insv

# Combine options
python JimWas-INSTA360-INSV-TO-SHORTS.PY --lens back --yaw -20 --fov 90 -q medium -d 60
```

## Command-Line Reference

| Option | Default | Description |
|--------|---------|-------------|
| `input` | `.` | Input .insv file or directory |
| `-o, --output` | same as input | Output directory |
| `-d, --duration` | `120` | Max segment duration in seconds |
| `-q, --quality` | `high` | Quality preset: `high`, `medium`, `low` |
| `--lens` | `front` | Lens to use: `front` (screen side) or `back` |
| `--yaw` | `0` | Horizontal pan angle in degrees |
| `--fov` | `80` | Horizontal field of view (30-120) |

## How It Works

1. The script reads the .insv file which contains two fisheye video streams (front and back lens)
2. Selects the chosen lens stream using `-map`
3. Applies ffmpeg's `v360` filter to reproject from fisheye to rectilinear (flat) perspective
4. Outputs 1080x1920 portrait video with the specified yaw and FOV
5. Automatically splits videos longer than the segment duration

### Automatic splitting

- **10-minute video** -> 5 segments (2 min each)
- **5-minute video** -> 3 segments (2 min, 2 min, 1 min)
- **90-second video** -> 1 segment

Segments are named: `video_shorts_part1.mp4`, `video_shorts_part2.mp4`, etc.

## Quality Settings

| Quality | CRF | Preset | File Size | Speed |
|---------|-----|--------|-----------|-------|
| high | 18 | slow | Largest | Slowest |
| medium | 23 | medium | Medium | Medium |
| low | 28 | fast | Smallest | Fastest |

## Output Specifications

- **Resolution:** 1080x1920 (9:16)
- **Video Codec:** H.264
- **Audio Codec:** AAC, 192kbps, 48kHz
- **Container:** MP4 with fast-start

## Troubleshooting

**"ffmpeg is not installed"** - Install ffmpeg using the instructions above.

**Black areas in output** - Your yaw value is past the edge of the fisheye. Keep yaw between -80 and 80.

**Wrong camera angle** - Try `--lens back` to switch to the other lens, or adjust `--yaw`.

**Video looks too zoomed in/out** - Adjust `--fov`. Lower values zoom in, higher values zoom out.

**Audio/video out of sync** - Try `-q high` for better quality processing.

## Changelog

### v2.0.0
- Replaced simple crop method with proper `v360` fisheye-to-rectilinear reprojection
- Added dual lens support (`--lens front/back`) by reading both video streams from .insv file
- Added horizontal pan control (`--yaw`)
- Added adjustable field of view (`--fov`)
- Output now has correct flat perspective instead of distorted fisheye crop

### v1.0.0
- Initial release with basic crop-and-scale conversion
- Automatic video splitting into 2-minute segments
- Batch processing support
- Quality presets (high/medium/low)

## License

Free to use and modify as needed.
