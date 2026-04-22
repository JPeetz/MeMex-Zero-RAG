#!/usr/bin/env python3
# Copyright (c) 2026 Joerg Peetz. All rights reserved.
"""
Voice Capture for Memex

Records audio and transcribes to markdown using local Whisper.
Perfect for capturing thoughts, voice memos, and interview notes.

Usage:
    # Record and transcribe
    python scripts/ingest-voice.py
    
    # Transcribe existing audio file
    python scripts/ingest-voice.py path/to/audio.mp3
    
    # Specify output
    python scripts/ingest-voice.py --output raw/my-thoughts.md

Requires:
    pip install openai-whisper sounddevice soundfile numpy

For faster transcription:
    pip install faster-whisper  # Uses CTranslate2
"""

import argparse
import sys
import tempfile
from datetime import datetime
from pathlib import Path

try:
    import whisper
    HAS_WHISPER = True
except ImportError:
    HAS_WHISPER = False

try:
    from faster_whisper import WhisperModel
    HAS_FASTER_WHISPER = True
except ImportError:
    HAS_FASTER_WHISPER = False

try:
    import sounddevice as sd
    import soundfile as sf
    import numpy as np
    HAS_AUDIO = True
except ImportError:
    np = None  # type: ignore
    HAS_AUDIO = False


def record_audio(duration: int = None, sample_rate: int = 16000):
    """Record audio from default microphone. Returns numpy array."""
    """Record audio from default microphone."""
    print("🎙️  Recording... (Press Ctrl+C to stop)")
    
    if duration:
        # Fixed duration recording
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
        sd.wait()
    else:
        # Record until interrupted
        audio_chunks = []
        try:
            with sd.InputStream(samplerate=sample_rate, channels=1, dtype='float32') as stream:
                while True:
                    chunk, _ = stream.read(sample_rate)  # 1 second chunks
                    audio_chunks.append(chunk)
                    elapsed = len(audio_chunks)
                    print(f"\r   Recording: {elapsed}s", end="", flush=True)
        except KeyboardInterrupt:
            print(f"\n✅ Recorded {len(audio_chunks)} seconds")
        
        audio = np.concatenate(audio_chunks)
    
    return audio.flatten()


def transcribe_whisper(audio_path: Path, model_size: str = "base") -> dict:
    """Transcribe using OpenAI Whisper."""
    print(f"🔄 Loading Whisper ({model_size})...")
    model = whisper.load_model(model_size)
    
    print("📝 Transcribing...")
    result = model.transcribe(str(audio_path))
    
    return {
        "text": result["text"],
        "language": result.get("language", "en"),
        "segments": result.get("segments", [])
    }


def transcribe_faster_whisper(audio_path: Path, model_size: str = "base") -> dict:
    """Transcribe using faster-whisper (CTranslate2)."""
    print(f"🔄 Loading faster-whisper ({model_size})...")
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    
    print("📝 Transcribing...")
    segments, info = model.transcribe(str(audio_path))
    
    text_parts = []
    all_segments = []
    for segment in segments:
        text_parts.append(segment.text)
        all_segments.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text
        })
    
    return {
        "text": " ".join(text_parts),
        "language": info.language,
        "segments": all_segments
    }


def format_segments(segments: list) -> str:
    """Format segments with timestamps."""
    lines = []
    for seg in segments:
        start = seg.get("start", 0)
        minutes = int(start // 60)
        seconds = int(start % 60)
        timestamp = f"[{minutes:02d}:{seconds:02d}]"
        lines.append(f"{timestamp} {seg.get('text', '').strip()}")
    return "\n".join(lines)


def generate_markdown(transcription: dict, audio_file: Path = None, title: str = None) -> str:
    """Generate markdown from transcription."""
    
    now = datetime.now()
    
    if not title:
        title = f"Voice Note - {now.strftime('%Y-%m-%d %H:%M')}"
    
    frontmatter = [
        "---",
        f'title: "{title}"',
        f"type: source",
        f"source_type: voice",
        f"recorded: {now.strftime('%Y-%m-%d %H:%M')}",
        f"language: {transcription.get('language', 'en')}",
    ]
    
    if audio_file:
        frontmatter.append(f"audio_file: {audio_file.name}")
    
    frontmatter.append("status: raw")
    frontmatter.append("---")
    
    content = [
        "\n".join(frontmatter),
        "",
        f"# {title}",
        "",
        "## Transcription",
        "",
        transcription["text"].strip(),
        "",
    ]
    
    # Add timestamped segments if available
    if transcription.get("segments"):
        content.extend([
            "## Timestamped Segments",
            "",
            "```",
            format_segments(transcription["segments"]),
            "```",
            "",
        ])
    
    content.extend([
        "---",
        "",
        f"*Transcribed with Whisper on {now.strftime('%Y-%m-%d %H:%M')}*",
    ])
    
    return "\n".join(content)


def main():
    parser = argparse.ArgumentParser(description="Voice capture and transcription for Memex")
    parser.add_argument("audio", type=Path, nargs="?", help="Path to audio file (optional, records if omitted)")
    parser.add_argument("--output", "-o", type=Path, help="Output markdown file")
    parser.add_argument("--title", "-t", type=str, help="Title for the note")
    parser.add_argument("--duration", "-d", type=int, help="Recording duration in seconds (records indefinitely if omitted)")
    parser.add_argument("--model", "-m", type=str, default="base", choices=["tiny", "base", "small", "medium", "large"], help="Whisper model size")
    parser.add_argument("--keep-audio", action="store_true", help="Keep the audio file")
    args = parser.parse_args()
    
    # Check dependencies
    if not HAS_WHISPER and not HAS_FASTER_WHISPER:
        print("❌ Whisper not installed. Run: pip install openai-whisper")
        print("   Or for faster transcription: pip install faster-whisper")
        sys.exit(1)
    
    # Determine audio source
    if args.audio:
        if not args.audio.exists():
            print(f"❌ File not found: {args.audio}")
            sys.exit(1)
        audio_path = args.audio
        temp_audio = None
    else:
        if not HAS_AUDIO:
            print("❌ Audio recording not available. Install: pip install sounddevice soundfile numpy")
            sys.exit(1)
        
        # Record audio
        audio = record_audio(duration=args.duration)
        
        # Save to temp file
        temp_audio = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        sf.write(temp_audio.name, audio, 16000)
        audio_path = Path(temp_audio.name)
        print(f"💾 Saved recording to: {audio_path}")
    
    # Transcribe
    try:
        if HAS_FASTER_WHISPER:
            transcription = transcribe_faster_whisper(audio_path, args.model)
        else:
            transcription = transcribe_whisper(audio_path, args.model)
    except Exception as e:
        print(f"❌ Transcription failed: {e}")
        sys.exit(1)
    
    print(f"✅ Transcribed {len(transcription['text'])} characters")
    
    # Generate markdown
    markdown = generate_markdown(transcription, audio_path if args.audio else None, args.title)
    
    # Determine output path
    if args.output:
        output_file = args.output
    else:
        output_dir = Path("raw")
        output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_file = output_dir / f"voice-{timestamp}.md"
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(markdown, encoding="utf-8")
    
    print(f"📝 Saved to: {output_file}")
    
    # Cleanup temp audio
    if temp_audio and not args.keep_audio:
        Path(temp_audio.name).unlink()
    elif temp_audio and args.keep_audio:
        # Move to raw/
        audio_dest = Path("raw") / f"voice-{datetime.now().strftime('%Y%m%d-%H%M%S')}.wav"
        Path(temp_audio.name).rename(audio_dest)
        print(f"🎵 Audio saved to: {audio_dest}")
    
    print("")
    print("Next steps:")
    print(f"  1. Review {output_file}")
    print(f"  2. Ask your LLM: 'Ingest {output_file} following SCHEMA.md'")


if __name__ == "__main__":
    main()
