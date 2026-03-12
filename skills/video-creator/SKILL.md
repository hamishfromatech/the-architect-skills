---
name: Video Creator
description: This skill should be used when the user asks to "create a video", "make a video", "generate a video", "edit video", "combine videos", "add text to video", "video from images", or mentions moviepy, ffmpeg, video editing, video creation, or video processing.
version: 1.0.0
---

# Video Creator

Create and edit videos programmatically using MoviePy and FFmpeg.

## Capabilities

- Create videos from images, text, and clips
- Concatenate multiple video clips
- Add text overlays and titles
- Add audio tracks and background music
- Apply transitions and effects
- Resize, crop, and trim videos
- Generate slideshows from images
- Export to various formats (MP4, GIF, etc.)

## Process

1. **Load/Create Clips**: Use `VideoFileClip()`, `ImageClip()`, `TextClip()`, or `ColorClip()`
2. **Edit Clips**: Apply cuts, resizes, effects
3. **Combine**: Use `concatenate_videoclips()` or `CompositeVideoClip()`
4. **Add Audio**: Overlay audio with `set_audio()` or `CompositeAudioClip()`
5. **Export**: Render with `write_videofile()`

## Core Concepts

### Clip Types

| Type | Description | Usage |
|------|-------------|-------|
| `VideoFileClip` | Load existing video | Edit, trim, combine |
| `ImageClip` | Static image as video | Slideshows, logos |
| `TextClip` | Text as video | Titles, captions |
| `ColorClip` | Solid color background | Backgrounds, padding |
| `AudioFileClip` | Load audio file | Background music, narration |

### Key Methods

| Method | Purpose |
|--------|---------|
| `subclip(start, end)` | Extract portion of clip |
| `resize(scale)` | Scale video dimensions |
| `with_effects()` | Apply visual effects |
| `set_audio(audio)` | Add audio track |
| `set_duration(sec)` | Set clip duration |

## Common Operations

### Create Video from Images

```python
from moviepy.editor import ImageClip, concatenate_videoclips

images = ['img1.jpg', 'img2.jpg', 'img3.jpg']
clips = [ImageClip(img).set_duration(3) for img in images]

final = concatenate_videoclips(clips)
final.write_videofile("slideshow.mp4", fps=24)
```

### Add Text Overlay

```python
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

video = VideoFileClip("input.mp4")

text = TextClip(
    "Hello World!",
    fontsize=70,
    color='white',
    font='Arial'
).set_duration(5).set_position('center')

result = CompositeVideoClip([video, text])
result.write_videofile("output.mp4")
```

### Concatenate Videos

```python
from moviepy.editor import VideoFileClip, concatenate_videoclips

clip1 = VideoFileClip("video1.mp4")
clip2 = VideoFileClip("video2.mp4")
clip3 = VideoFileClip("video3.mp4")

final = concatenate_videoclips([clip1, clip2, clip3])
final.write_videofile("combined.mp4")
```

### Add Background Music

```python
from moviepy.editor import VideoFileClip, AudioFileClip

video = VideoFileClip("video.mp4")
audio = AudioFileClip("music.mp3")

# Loop audio if shorter than video
if audio.duration < video.duration:
    audio = audio.loop(duration=video.duration)

video_with_audio = video.set_audio(audio)
video_with_audio.write_videofile("video_with_music.mp4")
```

### Create Title Card

```python
from moviepy.editor import TextClip, ColorClip, CompositeVideoClip

# Background
bg = ColorClip(size=(1920, 1080), color=(30, 30, 60))
bg = bg.set_duration(5)

# Title text
title = TextClip(
    "My Video Title",
    fontsize=80,
    color='white',
    font='Arial-Bold'
).set_duration(5).set_position('center')

# Combine
title_card = CompositeVideoClip([bg, title])
title_card.write_videofile("title.mp4", fps=24)
```

## Guidelines

- Always set `fps` when exporting (typically 24 or 30)
- Use `codec="libx264"` for MP4 videos
- Close clips with `clip.close()` to free resources
- Set duration for ImageClip and ColorClip (they have no natural duration)
- Use `method="compose"` in concatenate for different-sized clips

## Audio Handling

### Volume Control

```python
# Reduce volume to 50%
video = video.with_volume_scaled(0.5)

# Or for audio clips
audio = audio.with_volume_scaled(0.3)
```

### Mixing Multiple Audio Tracks

```python
from moviepy.editor import CompositeAudioClip

music = AudioFileClip("music.mp3").with_volume_scaled(0.3)
narration = AudioFileClip("voice.mp3").with_volume_scaled(1.0)

# Start narration 2 seconds in
narration = narration.set_start(2)

mixed = CompositeAudioClip([music, narration])
video = video.set_audio(mixed)
```

## Effects and Transitions

### Fade In/Out

```python
from moviepy.editor import VideoFileClip

clip = VideoFileClip("video.mp4")

# Add 1-second fade in and fade out
clip = clip.fadein(1).fadeout(1)
```

### Crossfade Between Clips

```python
from moviepy.editor import VideoFileClip, concatenate_videoclips

clip1 = VideoFileClip("video1.mp4").fadeout(0.5)
clip2 = VideoFileClip("video2.mp4").fadein(0.5)

final = concatenate_videoclips([clip1, clip2], method="compose")
```

### Speed Effects

```python
# Speed up 2x
fast = clip.with_speed_scaled(2.0)

# Slow down 0.5x
slow = clip.with_speed_scaled(0.5)
```

## Python Scripts

The `scripts/` directory contains:
- `video_builder.py` - Build videos from structured data
- `slideshow_maker.py` - Create slideshows from images
- `title_generator.py` - Generate title cards and overlays
- `audio_mixer.py` - Mix and manage audio tracks

## Usage Examples

See `examples/` directory for:
- Slideshow creation
- Video concatenation
- Text overlay examples
- Audio mixing examples

## References

See `references/` directory for:
- MoviePy API reference
- FFmpeg codec options
- Common video resolutions