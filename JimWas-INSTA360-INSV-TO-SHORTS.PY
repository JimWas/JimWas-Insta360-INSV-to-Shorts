#!/usr/bin/env python3
"""
Insta360 to Instagram Reels/YouTube Shorts Converter
Converts .insv files to 9:16 vertical videos with 2-minute duration
"""

import subprocess
import sys
import os
from pathlib import Path
import argparse


def check_ffmpeg():
    """Check if ffmpeg is installed"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_video_info(input_file):
    """Get video duration and other metadata"""
    try:
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            str(input_file)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        duration = float(result.stdout.strip())
        return duration
    except Exception as e:
        print(f"Error getting video info: {e}")
        return None


def convert_insv_to_shorts(input_file, output_dir=None, max_duration=120, 
                           quality='high', lens='front'):
    """
    Convert Insta360 .insv file to 9:16 vertical video(s)
    Automatically splits long videos into multiple segments
    
    Args:
        input_file: Path to .insv input file
        output_dir: Output directory (default: same as input)
        max_duration: Maximum video duration per segment in seconds (default: 120)
        quality: Video quality - 'high', 'medium', 'low' (default: 'high')
        lens: Which lens to use - 'front' or 'back' (default: 'front')
    
    Returns:
        Number of segments created (0 if failed)
    """
    input_path = Path(input_file)
    
    if not input_path.exists():
        print(f"Error: Input file '{input_file}' not found")
        return 0
    
    # Set output directory
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = input_path.parent
    
    # Get video duration
    duration = get_video_info(input_file)
    if duration is None:
        print("Warning: Could not determine video duration, creating single segment...")
        duration = max_duration
    
    # Calculate number of segments needed
    num_segments = int(duration / max_duration) + (1 if duration % max_duration > 0 else 0)
    
    # Quality settings
    quality_settings = {
        'high': {'crf': '18', 'preset': 'slow'},
        'medium': {'crf': '23', 'preset': 'medium'},
        'low': {'crf': '28', 'preset': 'fast'}
    }
    
    settings = quality_settings.get(quality, quality_settings['high'])
    
    print(f"\nProcessing: {input_path.name}")
    print(f"Total duration: {duration:.1f}s")
    print(f"Segments to create: {num_segments} ({max_duration}s each)")
    print(f"Quality: {quality} (CRF {settings['crf']})")
    print(f"Lens: {lens}")
    
    successful_segments = 0
    
    # Process each segment
    for segment in range(num_segments):
        start_time = segment * max_duration
        segment_duration = min(max_duration, duration - start_time)
        
        # Create output filename with segment number if multiple segments
        if num_segments > 1:
            output_file = output_path / f"{input_path.stem}_shorts_part{segment + 1}.mp4"
        else:
            output_file = output_path / f"{input_path.stem}_shorts.mp4"
        
        print(f"\n--- Segment {segment + 1}/{num_segments} ---")
        print(f"Start time: {start_time}s")
        print(f"Duration: {segment_duration:.1f}s")
        print(f"Output: {output_file.name}")
        
        # Build video filter for Insta360 X4 dual-fisheye format
        # The X4 has two fisheye lenses side by side in the frame
        # Front lens is on the left side, back lens is on the right side
        # We'll crop to one lens and rotate to portrait orientation
        
        if lens == 'front':
            # Crop left half (front lens)
            # X4 resolution is typically 3840x1920 or 7680x3840 (dual fisheye side-by-side)
            # Each half is square (1920x1920 or 3840x3840), scale and crop to 9:16 portrait
            video_filter = (
                "crop=iw/2:ih:0:0,"  # Crop left half (front lens)
                "scale=1080:1920:force_original_aspect_ratio=increase,"
                "crop=1080:1920"
            )
        else:  # back lens
            # Crop right half (back lens)
            video_filter = (
                "crop=iw/2:ih:iw/2:0,"  # Crop right half (back lens)
                "scale=1080:1920:force_original_aspect_ratio=increase,"
                "crop=1080:1920"
            )
        
        cmd = [
            'ffmpeg',
            '-ss', str(start_time),  # Start time
            '-i', str(input_file),
            '-t', str(segment_duration),  # Segment duration
            '-vf', video_filter,
            '-c:v', 'libx264',
            '-crf', settings['crf'],
            '-preset', settings['preset'],
            '-c:a', 'aac',
            '-b:a', '192k',
            '-ar', '48000',
            '-movflags', '+faststart',  # Enable fast start for web playback
            '-y',  # Overwrite output file
            str(output_file)
        ]
        
        try:
            print("Converting...")
            subprocess.run(cmd, check=True, capture_output=True)
            
            # Get output file size
            size_mb = output_file.stat().st_size / (1024 * 1024)
            print(f"✓ Success! Size: {size_mb:.2f} MB")
            successful_segments += 1
            
        except subprocess.CalledProcessError as e:
            print(f"✗ Error during conversion: {e}")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Completed: {successful_segments}/{num_segments} segments")
    print(f"{'='*60}")
    
    return successful_segments


def batch_convert(input_dir, output_dir=None, max_duration=120, quality='high', lens='front'):
    """Convert all .insv files in a directory"""
    input_path = Path(input_dir)
    
    if not input_path.exists() or not input_path.is_dir():
        print(f"Error: '{input_dir}' is not a valid directory")
        return
    
    insv_files = list(input_path.glob('*.insv')) + list(input_path.glob('*.INSV'))
    
    if not insv_files:
        print(f"No .insv files found in '{input_dir}'")
        return
    
    print(f"\nFound {len(insv_files)} .insv file(s)")
    
    total_segments = 0
    successful_files = 0
    failed_files = 0
    
    for idx, file in enumerate(insv_files, 1):
        print(f"\n{'='*60}")
        print(f"Processing file {idx}/{len(insv_files)}")
        print(f"{'='*60}")
        
        segments = convert_insv_to_shorts(file, output_dir, max_duration, quality, lens)
        if segments > 0:
            successful_files += 1
            total_segments += segments
        else:
            failed_files += 1
    
    print(f"\n{'='*60}")
    print(f"Batch conversion complete!")
    print(f"Files processed: {successful_files}/{len(insv_files)}")
    print(f"Total segments created: {total_segments}")
    print(f"Failed: {failed_files}")
    print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(
        description='Convert Insta360 X4 .insv videos to 9:16 Instagram Reels/YouTube Shorts format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert all .insv files using front lens (default)
  python insta360_to_shorts.py
  
  # Use back lens
  python insta360_to_shorts.py --lens back
  
  # 60-second segments with back lens
  python insta360_to_shorts.py --lens back -d 60
  
  # Medium quality for faster processing
  python insta360_to_shorts.py --lens front -q medium

The Insta360 X4 has two lenses:
- Front lens: The side with the screen (facing you when shooting)
- Back lens: The opposite side (facing away from you)
        """
    )
    
    parser.add_argument('input', nargs='?', default='.', 
                        help='Input .insv file or directory (default: current directory)')
    parser.add_argument('-o', '--output', help='Output directory (default: same as input)')
    parser.add_argument('-d', '--duration', type=int, default=120, 
                        help='Maximum video duration per segment in seconds (default: 120)')
    parser.add_argument('-q', '--quality', choices=['high', 'medium', 'low'], 
                        default='high', help='Output quality (default: high)')
    parser.add_argument('--lens', choices=['front', 'back'], default='front',
                        help='Which lens to use: front (screen side) or back (default: front)')
    
    args = parser.parse_args()
    
    # Check if ffmpeg is installed
    if not check_ffmpeg():
        print("Error: ffmpeg is not installed or not in PATH")
        print("\nTo install ffmpeg:")
        print("  Ubuntu/Debian: sudo apt-get install ffmpeg")
        print("  macOS: brew install ffmpeg")
        print("  Windows: Download from https://ffmpeg.org/download.html")
        sys.exit(1)
    
    input_path = Path(args.input)
    
    # Determine if input is a directory or file
    if input_path.is_dir():
        # Batch process all .insv files in the directory
        batch_convert(args.input, args.output, args.duration, args.quality, args.lens)
    elif input_path.is_file() and input_path.suffix.lower() == '.insv':
        # Process single file
        convert_insv_to_shorts(args.input, args.output, args.duration, args.quality, args.lens)
    else:
        print(f"Error: '{args.input}' is not a valid .insv file or directory")
        sys.exit(1)


if __name__ == '__main__':
    main()