# JimWas-Insta360-INSV-to-Shorts
Convert Insta360 X4 .insv dual-fisheye videos into 9:16 vertical shorts for Instagram Reels and YouTube Shorts, with automatic splitting, lens selection, and quality control.

# Insta360 to Instagram Reels/YouTube Shorts Converter

A Python script that automatically converts Insta360 .insv videos into 9:16 vertical format perfect for Instagram Reels and YouTube Shorts. **Automatically splits long videos into multiple 2-minute segments.**

## Features

- ✅ Converts .insv files to 9:16 (1080x1920) vertical format
- ✅ **Automatically splits long videos into multiple 2-minute segments**
- ✅ Smart naming for multi-part videos (part1, part2, etc.)
- ✅ Batch processing support for multiple files
- ✅ Multiple quality presets (high/medium/low)
- ✅ Fast-start enabled for web playback
- ✅ Preserves audio quality (192kbps AAC)
- ✅ Shows progress and file information

## How It Works

The script automatically detects video length and creates multiple segments:

- **10-minute video** → Creates 5 separate 2-minute videos
- **5-minute video** → Creates 3 videos (2min, 2min, 1min)
- **90-second video** → Creates 1 video (90 seconds)

Each segment is named sequentially: `video_shorts_part1.mp4`, `video_shorts_part2.mp4`, etc.

## Requirements

- Python 3.6+
- ffmpeg (must be installed separately)

## Installation

### 1. Install ffmpeg

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
- Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- Add to PATH

### 2. Install the script

Simply download `insta360_to_shorts.py` and make it executable:

```bash
chmod +x insta360_to_shorts.py
```

## Two Processing Modes

### Simple Mode (Default - Recommended)

By default, the script uses a simple crop method that works with most Insta360 formats:

```bash
python insta360_to_shorts.py
```

This mode just crops and scales your video to 9:16 format without any special 360° processing.

### 360° Mode (Advanced)

If your video is in equirectangular 360° format and you want to control the viewing angle, use the `--use-360` flag:

```bash
python insta360_to_shorts.py --use-360 --yaw 180
```

**Important:** Only use `--use-360` if:
- Your video appears distorted in simple mode
- You have an equirectangular 360° video
- You need precise camera angle control

## Camera Angle Control (360° Mode Only)

These options only work when you add the `--use-360` flag:

Since .insv files are 360° videos, you can control which direction the output video faces:

### Horizontal Rotation (Yaw)

```bash
# Front camera
python insta360_to_shorts.py --use-360 --yaw 0

# Back camera
python insta360_to_shorts.py --use-360 --yaw 180

# Right side
python insta360_to_shorts.py --use-360 --yaw 90

# Left side  
python insta360_to_shorts.py --use-360 --yaw 270
```

### Vertical Tilt (Pitch)

```bash
# Look up 30 degrees
python insta360_to_shorts.py --use-360 --pitch 30

# Look down 20 degrees
python insta360_to_shorts.py --use-360 --pitch -20

# Straight ahead (default)
python insta360_to_shorts.py --use-360 --pitch 0
```

### Field of View (FOV)

```bash
# Wider view (more fisheye)
python insta360_to_shorts.py --use-360 --fov 110

# Narrower view (more zoomed)
python insta360_to_shorts.py --use-360 --fov 70

# Default
python insta360_to_shorts.py --use-360 --fov 90
```

### Combined Example

Back camera, looking slightly down, wider FOV:
```bash
python insta360_to_shorts.py --use-360 --yaw 180 --pitch -10 --fov 100
```

### Visual Guide

```
        Pitch +90° (up)
              ↑
              |
Yaw 270° ←----+---→ Yaw 90°
(left)        |        (right)
              |
              ↓
        Pitch -90° (down)

Yaw 0° = Front camera (default)
Yaw 180° = Back camera
```

## Usage

### Simplest Usage (Recommended)

Just run the script in the folder with your .insv files - it will automatically process all of them:

```bash
cd /path/to/your/insv/files
python insta360_to_shorts.py
```

That's it! All .insv files will be converted with output files saved in the same folder.

### Other Options

**Specify output directory:**
```bash
python insta360_to_shorts.py -o ./output_folder
```

**Custom segment duration (e.g., 60 seconds for YouTube Shorts):**
```bash
python insta360_to_shorts.py -d 60
```

**Convert specific directory:**
```bash
python insta360_to_shorts.py /path/to/videos
```

**Convert single file:**
```bash
python insta360_to_shorts.py video.insv
```

**Lower quality for faster processing:**
```bash
python insta360_to_shorts.py -q medium
```

## Command-Line Options

```
positional arguments:
  input                 Input .insv file or directory (default: current directory)

optional arguments:
  -h, --help            Show help message
  -o, --output OUTPUT   Output directory (default: same as input)
  -d, --duration DURATION
                        Maximum video duration per segment in seconds (default: 120)
  -q, --quality {high,medium,low}
                        Output quality (default: high)

360° mode (advanced):
  --use-360            Enable 360° video mode for equirectangular videos
  --yaw YAW            [360 only] Horizontal rotation: 0=front, 90=right, 180=back, 270=left
  --pitch PITCH        [360 only] Vertical tilt: positive=up, negative=down
  --fov FOV            [360 only] Field of view in degrees, 60-120
```

## Examples

## Examples

### Example 1: Simple Mode (Recommended)
```bash
cd ~/Videos/Insta360
python insta360_to_shorts.py
```
Converts all .insv files using simple crop mode - works for most Insta360 videos

### Example 2: 60-Second Segments
```bash
python insta360_to_shorts.py -d 60 -q medium
```
All videos split into 60-second segments with medium quality

### Example 3: 360° Mode - Back Camera
```bash
python insta360_to_shorts.py --use-360 --yaw 180
```
Use this if you have equirectangular 360° video and want back camera view

### Example 4: 360° Mode - Custom Angle
```bash
python insta360_to_shorts.py --use-360 --yaw 90 --pitch -15 --fov 100
```
Right side camera, looking slightly down, wider FOV (360° mode only)

### Example 5: Specific Folder
```bash
python insta360_to_shorts.py ~/Videos/Insta360 -o ~/Videos/Shorts
```
Process videos from one folder, save to another

## Output Specifications

- **Resolution:** 1080x1920 (9:16 aspect ratio)
- **Video Codec:** H.264
- **Audio Codec:** AAC, 192kbps, 48kHz
- **Max Duration:** 120 seconds (configurable)
- **Format:** MP4 with fast-start enabled

## Quality Settings Details

| Quality | CRF | Preset | File Size | Processing Speed |
|---------|-----|--------|-----------|------------------|
| High    | 18  | slow   | Largest   | Slowest          |
| Medium  | 23  | medium | Medium    | Medium           |
| Low     | 28  | fast   | Smallest  | Fastest          |

## Troubleshooting

### "ffmpeg is not installed"
Install ffmpeg using the instructions in the Installation section above.

### "Input file not found"
Make sure the .insv file path is correct and the file exists.

### Video looks distorted/warped/triangular
The default simple mode should work for most Insta360 videos. If you see distortion:
1. First, try running without any flags: `python insta360_to_shorts.py`
2. If still distorted, your video might be equirectangular 360°. Try: `python insta360_to_shorts.py --use-360`

### Wrong camera angle / Not showing what I want
**In simple mode (default):** You get whatever angle the video was saved with. No angle control.

**In 360° mode:** Use angle controls:
- Back camera: `--use-360 --yaw 180`
- Right side: `--use-360 --yaw 90`
- Left side: `--use-360 --yaw 270`
- Adjust up/down: `--use-360 --pitch 20` (or negative)

### Which mode should I use?
- **Default (simple mode):** Works for 90% of Insta360 videos. Start here.
- **360° mode (`--use-360`):** Only if you have equirectangular format or need angle control.

### Video looks too fisheye or zoomed in (360° mode only)
Adjust FOV: `--use-360 --fov 70` (zoomed in) or `--fov 110` (wider)

### Audio/Video out of sync
Try using `-q high` for better quality processing, or check that your source file isn't corrupted.

## Quick Reference

### Simple Mode (Default)
```bash
python insta360_to_shorts.py                    # Convert all videos, simple crop
python insta360_to_shorts.py -d 60              # 60-second segments
python insta360_to_shorts.py -q medium          # Medium quality, faster
```

### 360° Mode Camera Angles (Advanced)

| What you want | Command |
|---------------|---------|
| Front camera | `python insta360_to_shorts.py --use-360 --yaw 0` |
| Back camera | `python insta360_to_shorts.py --use-360 --yaw 180` |
| Right side | `python insta360_to_shorts.py --use-360 --yaw 90` |
| Left side | `python insta360_to_shorts.py --use-360 --yaw 270` |
| Front, looking up | `python insta360_to_shorts.py --use-360 --pitch 20` |
| Back, looking down | `python insta360_to_shorts.py --use-360 --yaw 180 --pitch -20` |

## Notes

- **Long videos are automatically split** into multiple segments of the specified duration
- Each segment is named with `_part1`, `_part2`, etc. (single segments have no part number)
- The script automatically crops/scales to fit 9:16 format
- If your video is shorter than the max duration, only one file is created
- Fast-start is enabled, making videos start playing faster when uploaded
- Splitting happens at exact time intervals (no smart scene detection)

## Platform-Specific Tips

### Instagram Reels
- Maximum file size: 4GB
- Recommended duration: 15-90 seconds
- Use `high` or `medium` quality

### YouTube Shorts
- Maximum duration: 60 seconds
- Recommended: Use `-d 60` to ensure compliance
- Use `high` quality for best results

## Advanced Usage

If you need to customize the conversion further, you can modify the `convert_insv_to_shorts()` function in the script to adjust:
- Video filters
- Bitrate settings
- Audio settings
- Cropping/scaling behavior

## License

Free to use and modify as needed.

## Support

For issues related to:
- **Script functionality:** Check that ffmpeg is installed and working
- **Video quality:** Try different quality settings
- **Insta360 formats:** Ensure your .insv files are compatible
