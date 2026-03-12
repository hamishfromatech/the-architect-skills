# MoviePy Reference Guide

## Installation

```bash
pip install moviepy
```

**Note**: MoviePy requires FFmpeg. Install it separately:
- **Windows**: Download from ffmpeg.org and add to PATH
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

## Core Classes

### VideoFileClip

Load and manipulate video files.

```python
from moviepy.editor import VideoFileClip

# Load video
clip = VideoFileClip("video.mp4")

# Properties
print(clip.duration)  # Length in seconds
print(clip.size)      # (width, height)
print(clip.fps)       # Frames per second

# Extract portion
subclip = clip.subclip(10, 30)  # Seconds 10-30

# Close when done
clip.close()
```

### ImageClip

Create video from static image.

```python
from moviepy.editor import ImageClip

# Create from image
clip = ImageClip("image.jpg")

# Must set duration
clip = clip.set_duration(5)  # 5 seconds

# Resize
clip = clip.resize((1920, 1080))
```

### TextClip

Create video from text.

```python
from moviepy.editor import TextClip

# Basic text
text = TextClip(
    "Hello World",
    fontsize=70,
    color='white',
    font='Arial'
).set_duration(5)

# Position
text = text.set_position('center')
text = text.set_position(('left', 'top'))
text = text.set_position((100, 200))  # Pixel coordinates
```

### ColorClip

Create solid color background.

```python
from moviepy.editor import ColorClip

# Create colored background
bg = ColorClip(
    size=(1920, 1080),
    color=(255, 0, 0),  # RGB
    duration=5
)
```

### AudioFileClip

Load audio files.

```python
from moviepy.editor import AudioFileClip

audio = AudioFileClip("music.mp3")

print(audio.duration)
print(audio.fps)
```

## Combining Clips

### concatenate_videoclips

Play clips sequentially.

```python
from moviepy.editor import VideoFileClip, concatenate_videoclips

clip1 = VideoFileClip("video1.mp4")
clip2 = VideoFileClip("video2.mp4")

# Sequential playback
final = concatenate_videoclips([clip1, clip2])

# Handle different sizes
final = concatenate_videoclips([clip1, clip2], method="compose")
```

### CompositeVideoClip

Overlay clips (play simultaneously).

```python
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

video = VideoFileClip("background.mp4")
text = TextClip("Overlay", fontsize=50).set_duration(5)

# Stack clips
result = CompositeVideoClip([video, text])
```

### CompositeAudioClip

Mix audio tracks.

```python
from moviepy.editor import AudioFileClip, CompositeAudioClip

music = AudioFileClip("music.mp3").with_volume_scaled(0.3)
voice = AudioFileClip("voice.mp3").with_volume_scaled(1.0)

# Start voice 2 seconds in
voice = voice.set_start(2)

mixed = CompositeAudioClip([music, voice])
```

## Clip Methods

### Positioning

```python
# Position presets
clip.set_position('center')
clip.set_position('left')
clip.set_position('right')
clip.set_position('top')
clip.set_position('bottom')

# Tuple positioning
clip.set_position(('center', 'top'))  # Horizontal, vertical
clip.set_position((100, 200))  # Pixel coordinates
```

### Timing

```python
# Set duration
clip.set_duration(10)

# Set start time (for composites)
clip.set_start(5)  # Start 5 seconds in

# Subclip
clip.subclip(10, 30)  # From second 10 to 30
clip.subclip(10)  # From second 10 to end
```

### Effects

```python
# Fade in/out
clip.fadein(1)  # 1 second fade in
clip.fadeout(1)  # 1 second fade out

# Speed
clip.with_speed_scaled(2.0)  # 2x faster
clip.with_speed_scaled(0.5)  # Half speed

# Volume
clip.with_volume_scaled(0.5)  # 50% volume

# Resize
clip.resize(0.5)  # Half size
clip.resize((1280, 720))  # Specific dimensions
```

## Export Options

### write_videofile

```python
clip.write_videofile(
    "output.mp4",
    fps=24,                    # Frames per second
    codec="libx264",          # Video codec
    audio_codec="aac",        # Audio codec
    bitrate="8000k",          # Video bitrate
    audio_bitrate="128k",     # Audio bitrate
    preset="medium",          # Encoding speed
    threads=4                 # CPU threads
)
```

### write_gif

```python
clip.write_gif(
    "output.gif",
    fps=15,
    program="ffmpeg"  # or "imageio"
)
```

### write_images_sequence

```python
# Export frames as images
clip.write_images_sequence("frame_%04d.png", fps=1)
```

## Common Codecs

| Format | Video Codec | Audio Codec |
|--------|-------------|-------------|
| MP4 | libx264 | aac |
| WebM | libvpx-vp9 | libvorbis |
| GIF | gif | - |
| AVI | mpeg4 | mp3 |

## Common Resolutions

| Name | Resolution |
|------|------------|
| 4K | 3840 x 2160 |
| 1080p | 1920 x 1080 |
| 720p | 1280 x 720 |
| 480p | 854 x 480 |
| 360p | 640 x 360 |

## Memory Management

MoviePy clips hold file handles. Always close clips when done:

```python
from moviepy.editor import VideoFileClip

# Bad - resource leak
def process():
    clip = VideoFileClip("video.mp4")
    clip.subclip(0, 10).write_videofile("out.mp4")

# Good - explicit cleanup
def process():
    clip = VideoFileClip("video.mp4")
    try:
        clip.subclip(0, 10).write_videofile("out.mp4")
    finally:
        clip.close()

# Or use context manager (MoviePy 2.0+)
with VideoFileClip("video.mp4") as clip:
    clip.subclip(0, 10).write_videofile("out.mp4")
```

## Troubleshooting

### ImageMagick Not Found

TextClip requires ImageMagick:

```bash
# macOS
brew install imagemagick

# Ubuntu
sudo apt install imagemagick

# Windows
# Download from imagemagick.org
```

### FFmpeg Not Found

Ensure FFmpeg is in your PATH:

```python
from moviepy.config import change_settings
change_settings({"FFMPEG_BINARY": "/path/to/ffmpeg"})
```

### Memory Issues

For large videos, process in chunks:

```python
# Process in segments
for start in range(0, int(clip.duration), 60):
    end = min(start + 60, clip.duration)
    segment = clip.subclip(start, end)
    # Process segment...
```

## Best Practices

1. **Set FPS explicitly**: Always specify `fps` when exporting
2. **Use method="compose"**: For concatenating different-sized clips
3. **Close clips**: Free resources after processing
4. **Use with clauses**: For automatic cleanup (Python 3.10+)
5. **Test with short clips**: Before processing long videos
6. **Monitor memory**: For large projects