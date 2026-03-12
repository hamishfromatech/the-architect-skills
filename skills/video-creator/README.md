# Video Creator

Create and edit videos programmatically using MoviePy and FFmpeg.

## Overview

The Video Creator skill produces videos from images, text, and clips with support for audio mixing, transitions, and various export formats.

## Quick Start

### Trigger Phrases

Use these phrases to activate the skill:
- "create a video"
- "make a video"
- "generate a video"
- "edit video"
- "combine videos"
- "add text to video"
- "video from images"

## Capabilities

- Create videos from images, text, and clips
- Concatenate multiple video clips
- Add text overlays and titles
- Add audio tracks and background music
- Apply transitions and effects (fade in/out)
- Resize, crop, and trim videos
- Generate slideshows from images
- Export to MP4, GIF, and other formats

## Core Concepts

| Type | Description | Usage |
|------|-------------|-------|
| `VideoFileClip` | Load existing video | Edit, trim, combine |
| `ImageClip` | Static image as video | Slideshows, logos |
| `TextClip` | Text as video | Titles, captions |
| `ColorClip` | Solid color background | Backgrounds, padding |
| `AudioFileClip` | Load audio file | Background music, narration |

## Quick Example

### Create a Slideshow

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
text = TextClip("Hello!", fontsize=70, color='white')
text = text.set_duration(5).set_position('center')

result = CompositeVideoClip([video, text])
result.write_videofile("output.mp4", fps=24)
```

## Examples

See [examples/video_examples.md](examples/video_examples.md) for complete examples including:
- Slideshows with transitions
- Text overlays
- Picture-in-picture
- Audio mixing
- Title cards
- Speed effects

## Python Scripts

- `video_builder.py` - Build videos from structured specifications

## References

See [references/moviepy_guide.md](references/moviepy_guide.md) for the complete API reference.

## Dependencies

```bash
pip install moviepy
```

**Note:** MoviePy requires FFmpeg:
- **Windows**: Download from ffmpeg.org and add to PATH
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

## License

MIT License - Part of The Architect Skills project.