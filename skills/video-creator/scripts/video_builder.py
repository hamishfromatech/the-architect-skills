"""
Video Builder - Create videos from structured data using MoviePy.

This module provides utilities for creating videos with clips,
images, text overlays, and audio.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union, Tuple
from pathlib import Path
from moviepy.editor import (
    VideoFileClip,
    ImageClip,
    TextClip,
    ColorClip,
    AudioFileClip,
    CompositeVideoClip,
    CompositeAudioClip,
    concatenate_videoclips,
    concatenate_audioclips
)


@dataclass
class ClipSpec:
    """Specification for a video clip."""
    type: str  # 'video', 'image', 'text', 'color'
    source: Optional[str] = None
    duration: Optional[float] = None
    start: float = 0
    end: Optional[float] = None
    position: Tuple[str, ...] = ('center', 'center')
    size: Optional[Tuple[int, int]] = None
    volume: float = 1.0
    text: Optional[str] = None
    fontsize: int = 70
    font: str = 'Arial'
    color: str = 'white'
    bg_color: Optional[Tuple[int, int, int]] = None


@dataclass
class AudioSpec:
    """Specification for an audio track."""
    source: str
    volume: float = 1.0
    start: float = 0
    loop: bool = False


@dataclass
class VideoConfig:
    """Configuration for video generation."""
    clips: List[ClipSpec]
    audio: List[AudioSpec] = field(default_factory=list)
    output_path: str = "output.mp4"
    fps: int = 24
    resolution: Tuple[int, int] = (1920, 1080)
    codec: str = "libx264"
    audio_codec: str = "aac"


class VideoBuilder:
    """Build videos from structured specifications."""

    def __init__(self, config: VideoConfig):
        """Initialize the video builder.

        Args:
            config: Video configuration with clip specs
        """
        self.config = config
        self.clips: List = []

    def build(self) -> None:
        """Build the complete video."""
        # Process each clip spec
        processed_clips = []
        for clip_spec in self.config.clips:
            clip = self._create_clip(clip_spec)
            if clip:
                processed_clips.append(clip)

        # Combine clips
        if len(processed_clips) == 1:
            final = processed_clips[0]
        else:
            # Use composite for overlapping, concatenate for sequential
            final = self._combine_clips(processed_clips)

        # Add audio
        if self.config.audio:
            audio = self._create_audio_track()
            final = final.set_audio(audio)

        # Ensure final clip has duration set
        if not hasattr(final, 'duration') or final.duration is None:
            # Calculate max duration from clips
            max_duration = max(
                (c.duration for c in processed_clips if hasattr(c, 'duration') and c.duration),
                default=5
            )
            final = final.set_duration(max_duration)

        self._final_clip = final

    def _create_clip(self, spec: ClipSpec):
        """Create a clip from a specification.

        Args:
            spec: Clip specification

        Returns:
            MoviePy clip object
        """
        clip = None

        if spec.type == 'video':
            clip = VideoFileClip(spec.source)
            if spec.start or spec.end:
                end = spec.end if spec.end else clip.duration
                clip = clip.subclip(spec.start, end)

        elif spec.type == 'image':
            clip = ImageClip(spec.source)
            if spec.duration:
                clip = clip.set_duration(spec.duration)

        elif spec.type == 'text':
            clip = TextClip(
                spec.text,
                fontsize=spec.fontsize,
                color=spec.color,
                font=spec.font
            )
            if spec.duration:
                clip = clip.set_duration(spec.duration)

        elif spec.type == 'color':
            color = spec.bg_color if spec.bg_color else (0, 0, 0)
            size = spec.size if spec.size else self.config.resolution
            clip = ColorClip(size=size, color=color)
            if spec.duration:
                clip = clip.set_duration(spec.duration)

        # Apply common settings
        if clip:
            if spec.size:
                clip = clip.resize(spec.size)
            if spec.position:
                clip = clip.set_position(spec.position)
            if spec.volume != 1.0:
                clip = clip.with_volume_scaled(spec.volume)

        return clip

    def _combine_clips(self, clips):
        """Combine multiple clips.

        Args:
            clips: List of MoviePy clips

        Returns:
            Combined clip
        """
        # Check if clips should be sequential or composite
        # For simplicity, use concatenate for sequential clips
        return concatenate_videoclips(clips, method="compose")

    def _create_audio_track(self):
        """Create composite audio track from specs.

        Returns:
            Composite audio clip
        """
        audio_clips = []

        for audio_spec in self.config.audio:
            clip = AudioFileClip(audio_spec.source)

            if audio_spec.volume != 1.0:
                clip = clip.with_volume_scaled(audio_spec.volume)

            if audio_spec.start > 0:
                clip = clip.set_start(audio_spec.start)

            # Loop if needed and shorter than video
            if audio_spec.loop:
                video_duration = max(
                    (c.duration for c in self.clips if hasattr(c, 'duration') and c.duration),
                    default=10
                )
                if clip.duration < video_duration:
                    clip = clip.loop(duration=video_duration)

            audio_clips.append(clip)

        if len(audio_clips) == 1:
            return audio_clips[0]

        return CompositeAudioClip(audio_clips)

    def save(self, filepath: Optional[str] = None) -> str:
        """Save the video to a file.

        Args:
            filepath: Output path (uses config if not provided)

        Returns:
            Path to saved video
        """
        output = filepath or self.config.output_path

        self._final_clip.write_videofile(
            output,
            fps=self.config.fps,
            codec=self.config.codec,
            audio_codec=self.config.audio_codec
        )

        return output

    def cleanup(self):
        """Clean up clip resources."""
        for clip in self.clips:
            if hasattr(clip, 'close'):
                clip.close()


def create_slideshow(
    images: List[str],
    output_path: str,
    duration_per_image: float = 3.0,
    fps: int = 24,
    resolution: Tuple[int, int] = (1920, 1080)
) -> str:
    """Create a slideshow from images.

    Args:
        images: List of image file paths
        output_path: Output video path
        duration_per_image: Seconds per image
        fps: Frames per second
        resolution: Output resolution

    Returns:
        Path to saved video
    """
    clips = [
        ImageClip(img)
        .set_duration(duration_per_image)
        .resize(resolution)
        for img in images
    ]

    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(output_path, fps=fps, codec="libx264")

    # Cleanup
    for clip in clips:
        clip.close()

    return output_path


def add_text_overlay(
    video_path: str,
    text: str,
    output_path: str,
    position: str = 'center',
    fontsize: int = 70,
    color: str = 'white',
    duration: Optional[float] = None
) -> str:
    """Add text overlay to a video.

    Args:
        video_path: Input video path
        text: Text to overlay
        output_path: Output video path
        position: Text position
        fontsize: Font size
        color: Text color
        duration: Overlay duration (full video if None)

    Returns:
        Path to saved video
    """
    video = VideoFileClip(video_path)

    text_clip = TextClip(
        text,
        fontsize=fontsize,
        color=color,
        font='Arial'
    )

    text_duration = duration if duration else video.duration
    text_clip = text_clip.set_duration(text_duration).set_position(position)

    result = CompositeVideoClip([video, text_clip])
    result.write_videofile(output_path, fps=24, codec="libx264")

    video.close()
    result.close()

    return output_path


def concatenate_videos(
    video_paths: List[str],
    output_path: str,
    fps: int = 24
) -> str:
    """Concatenate multiple videos.

    Args:
        video_paths: List of video file paths
        output_path: Output video path
        fps: Frames per second

    Returns:
        Path to saved video
    """
    clips = [VideoFileClip(p) for p in video_paths]
    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(output_path, fps=fps, codec="libx264")

    # Cleanup
    for clip in clips:
        clip.close()

    return output_path


def add_background_music(
    video_path: str,
    music_path: str,
    output_path: str,
    music_volume: float = 0.3
) -> str:
    """Add background music to a video.

    Args:
        video_path: Input video path
        music_path: Music file path
        output_path: Output video path
        music_volume: Music volume (0-1)

    Returns:
        Path to saved video
    """
    video = VideoFileClip(video_path)
    music = AudioFileClip(music_path).with_volume_scaled(music_volume)

    # Loop music if shorter than video
    if music.duration < video.duration:
        music = music.loop(duration=video.duration)

    video_with_music = video.set_audio(music)
    video_with_music.write_videofile(output_path, fps=24, codec="libx264")

    video.close()
    music.close()

    return output_path


if __name__ == "__main__":
    # Example: Create title card
    config = VideoConfig(
        clips=[
            ClipSpec(
                type='color',
                bg_color=(30, 30, 60),
                duration=5,
                size=(1920, 1080)
            ),
            ClipSpec(
                type='text',
                text='Welcome to My Video',
                fontsize=80,
                color='white',
                duration=5
            )
        ],
        output_path='title_card.mp4',
        fps=24
    )

    builder = VideoBuilder(config)
    builder.build()
    builder.save()
    print("Created title_card.mp4")