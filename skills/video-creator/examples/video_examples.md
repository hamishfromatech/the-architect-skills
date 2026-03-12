# Video Creator Examples

## Example 1: Basic Slideshow

```python
from moviepy.editor import ImageClip, concatenate_videoclips

images = ['photo1.jpg', 'photo2.jpg', 'photo3.jpg', 'photo4.jpg']
clips = [ImageClip(img).set_duration(3) for img in images]

slideshow = concatenate_videoclips(clips, method="compose")
slideshow.write_videofile("slideshow.mp4", fps=24)
```

## Example 2: Video from Images with Transitions

```python
from moviepy.editor import ImageClip, concatenate_videoclips

images = ['img1.jpg', 'img2.jpg', 'img3.jpg']

clips = []
for img in images:
    clip = ImageClip(img).set_duration(4)
    clip = clip.fadein(0.5).fadeout(0.5)  # Add transitions
    clips.append(clip)

slideshow = concatenate_videoclips(clips, method="compose")
slideshow.write_videofile("slideshow_transitions.mp4", fps=24)
```

## Example 3: Text Overlay on Video

```python
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

# Load video
video = VideoFileClip("input.mp4")

# Create text
text = TextClip(
    "Subscribe!",
    fontsize=50,
    color='yellow',
    font='Arial-Bold'
).set_duration(5).set_position('bottom')

# Overlay
result = CompositeVideoClip([video, text])
result.write_videofile("with_text.mp4", fps=24)
```

## Example 4: Picture-in-Picture

```python
from moviepy.editor import VideoFileClip, CompositeVideoClip

main_video = VideoFileClip("main.mp4")
overlay_video = VideoFileClip("overlay.mp4").resize(0.3)

# Position overlay in bottom-right corner
overlay_video = overlay_video.set_position(('right', 'bottom'))

result = CompositeVideoClip([main_video, overlay_video])
result.write_videofile("pip.mp4", fps=24)
```

## Example 5: Concatenate Multiple Videos

```python
from moviepy.editor import VideoFileClip, concatenate_videoclips

videos = ['part1.mp4', 'part2.mp4', 'part3.mp4']
clips = [VideoFileClip(v) for v in videos]

final = concatenate_videoclips(clips, method="compose")
final.write_videofile("combined.mp4", fps=24)
```

## Example 6: Trim and Cut Video

```python
from moviepy.editor import VideoFileClip

video = VideoFileClip("long_video.mp4")

# Extract 10-30 seconds
trimmed = video.subclip(10, 30)

trimmed.write_videofile("trimmed.mp4", fps=24)
```

## Example 7: Add Background Music

```python
from moviepy.editor import VideoFileClip, AudioFileClip

video = VideoFileClip("video.mp4")
music = AudioFileClip("background.mp3")

# Adjust music volume
music = music.with_volume_scaled(0.3)

# Loop music if shorter than video
if music.duration < video.duration:
    music = music.loop(duration=video.duration)

# Combine
final = video.set_audio(music)
final.write_videofile("with_music.mp4", fps=24, codec="libx264")
```

## Example 8: Title Card with Background

```python
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip

# Create colored background
bg = ColorClip(size=(1920, 1080), color=(50, 50, 100))
bg = bg.set_duration(4)

# Create title text
title = TextClip(
    "My Awesome Video",
    fontsize=80,
    color='white',
    font='Arial-Bold'
).set_duration(4).set_position('center')

# Subtitle
subtitle = TextClip(
    "Created with MoviePy",
    fontsize=40,
    color='lightgray',
    font='Arial'
).set_duration(4).set_position(('center', 600))

# Combine
title_card = CompositeVideoClip([bg, title, subtitle])
title_card.write_videofile("title_card.mp4", fps=24)
```

## Example 9: Add Intro and Outro

```python
from moviepy.editor import VideoFileClip, concatenate_videoclips

intro = VideoFileClip("intro.mp4")
main = VideoFileClip("main_content.mp4")
outro = VideoFileClip("outro.mp4")

final = concatenate_videoclips([intro, main, outro], method="compose")
final.write_videofile("complete.mp4", fps=24)
```

## Example 10: Speed Up / Slow Down

```python
from moviepy.editor import VideoFileClip

video = VideoFileClip("normal_speed.mp4")

# Speed up 2x
fast = video.with_speed_scaled(2.0)
fast.write_videofile("fast.mp4", fps=24)

# Slow down 0.5x
slow = video.with_speed_scaled(0.5)
slow.write_videofile("slow.mp4", fps=24)
```

## Example 11: Resize Video

```python
from moviepy.editor import VideoFileClip

video = VideoFileClip("1080p.mp4")

# Resize to 720p
smaller = video.resize(1280, 720)
smaller.write_videofile("720p.mp4", fps=24)

# Or scale by factor
half_size = video.resize(0.5)
half_size.write_videofile("540p.mp4", fps=24)
```

## Example 12: Mix Multiple Audio Tracks

```python
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip

video = VideoFileClip("video.mp4")

# Background music at 30% volume
music = AudioFileClip("music.mp3").with_volume_scaled(0.3)

# Voiceover at 100% volume
voice = AudioFileClip("narration.mp3").with_volume_scaled(1.0)

# Start music from beginning, voice 2 seconds in
music = music.set_start(0)
voice = voice.set_start(2)

# Combine audio
mixed_audio = CompositeAudioClip([music, voice])

# Apply to video
final = video.set_audio(mixed_audio)
final.write_videofile("mixed.mp4", fps=24)
```

## Example 13: Create GIF from Video

```python
from moviepy.editor import VideoFileClip

video = VideoFileClip("video.mp4")

# Extract 5 seconds and convert to GIF
gif = video.subclip(0, 5)
gif.write_gif("output.gif", fps=15)
```

## Example 14: Using VideoBuilder Class

```python
from video_builder import VideoBuilder, VideoConfig, ClipSpec

# Define video configuration
config = VideoConfig(
    clips=[
        # Title card
        ClipSpec(
            type='color',
            bg_color=(30, 30, 60),
            duration=3,
            size=(1920, 1080)
        ),
        ClipSpec(
            type='text',
            text='Introduction',
            fontsize=60,
            color='white',
            duration=3
        ),
        # Main content
        ClipSpec(
            type='video',
            source='content.mp4',
            start=0,
            end=30
        ),
        # Image slide
        ClipSpec(
            type='image',
            source='slide.jpg',
            duration=5
        )
    ],
    audio=[
        AudioSpec(
            source='background.mp3',
            volume=0.3,
            loop=True
        )
    ],
    output_path='final_video.mp4',
    fps=24
)

# Build video
builder = VideoBuilder(config)
builder.build()
builder.save()
```