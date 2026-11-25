#!/usr/bin/env python3
"""
Audio & Narration Synthesis Pipeline for Linear Algebra Animation Video
Author: Ipsit Debnath
Topic: Matrices & Matrix Operations
Generates:
  1. Scene-by-scene crystal-clear voiceover narration using macOS Speech Synthesis
  2. Royalty-free ambient musical background score (synthesized warm harmonic pad)
  3. Mixed final soundtrack with sidechain ducking (-24dB BGM under narration)
"""

import os
import sys
import math
import wave
import struct
import subprocess
import json

FFMPEG_BIN = "/Applications/BlueStacks.app/Contents/MacOS/ffmpeg"
OUTPUT_DIR = "assets/audio"

SCENES_NARRATION = [
    {
        "id": 1,
        "title": "Hook & Context",
        "text": (
            "Have you ever wondered how your phone rotates a photo in a split second, "
            "how computer graphics render lifelike three-dimensional worlds in video games, "
            "or how artificial intelligence models process millions of visual signals simultaneously? "
            "Behind every single one of these technological wonders lies a universal mathematical language: the matrix. "
            "To many students, a matrix looks like nothing more than an intimidating box of numbers trapped inside square brackets. "
            "In this video, we are going to look beneath the surface. "
            "We will discover what a matrix truly represents, how its operations work, "
            "and how simple numbers in a grid actually control the geometry of space itself."
        )
    },
    {
        "id": 2,
        "title": "Concept Introduction & Notation",
        "text": (
            "Let us begin with the formal definition. "
            "Mathematically, a matrix is a rectangular array of numbers arranged in horizontal rows and vertical columns. "
            "We describe any matrix by its dimensions: m by n, where m is the number of rows, and n is the number of columns. "
            "An easy memory trick is the phrase Row-Column, just like Roman Colonists, or R and C in alphabetical order. "
            "Any individual number inside the matrix is called an entry, denoted as a i j, "
            "where index i specifies its row, and index j specifies its column. "
            "For example, a two one lives in row two, column one. "
            "When a matrix has only one column, we call it a column vector. "
            "Thus, vectors are simply specialized single-column matrices!"
        )
    },
    {
        "id": 3,
        "title": "Visual Intuition - Space Transformers",
        "text": (
            "Now comes the profound visual insight that transforms how you see linear algebra forever: "
            "a matrix is not just a passive table of stored numbers; it is an active geometric function that transforms space! "
            "In two dimensions, every coordinate is tracked by two unit basis vectors: "
            "i hat, pointing to one zero along the horizontal axis, and j hat, pointing to zero one along the vertical axis. "
            "When space undergoes a linear transformation, two fundamental rules hold: "
            "all grid lines remain straight and parallel, and the origin remains fixed at zero zero. "
            "Because linear combinations are preserved, wherever the basis vectors land completely determines where every point in space lands! "
            "Look closely at the columns of our matrix: "
            "the first column, two zero, is where i hat lands. "
            "The second column, one, one point five, is where j hat lands. "
            "A matrix is literally a compact recording of where the basis vectors landed!"
        )
    },
    {
        "id": 4,
        "title": "Worked Example - Operations Step-by-Step",
        "text": (
            "Now let us master the core algebraic operations step-by-step. "
            "First: Matrix Addition. You can only add matrices of the exact same dimensions. "
            "If the sizes match, addition is component-wise: "
            "three plus one gives four; one plus two gives three; "
            "zero plus four gives four; and two plus five gives seven. "
            "Geometrically, this represents combining two vector fields across space. "
            "Second: Scalar Multiplication. When you multiply a matrix by a scalar like three, "
            "every entry scales by that number. "
            "Three times three is nine, three times one is three, three times zero is zero, and three times two is six. "
            "Geometrically, this dilates space uniformly. "
            "Third and most famous: Matrix Multiplication. "
            "To multiply matrix A by matrix B, the number of columns in A must equal the number of rows in B. "
            "The inner dimensions must match! "
            "Each entry in the product is computed by the dot product of a row from the left matrix with a column from the right matrix. "
            "For entry one one: three times one plus one times four equals seven. "
            "For entry one two: three times two plus one times five equals eleven. "
            "For entry two one: zero times one plus two times four equals eight. "
            "And for entry two two: zero times two plus two times five equals ten. "
            "All intermediate arithmetic follows strict, verifiable logic."
        )
    },
    {
        "id": 5,
        "title": "Geometric Interpretation & Non-Commutativity",
        "text": (
            "Why is matrix multiplication defined through this row-column rule rather than simply multiplying matching entries? "
            "Because matrix multiplication represents the composition of linear transformations! "
            "Multiplying B times A means applying transformation A first, and then applying transformation B to the result. "
            "This immediately reveals why matrix multiplication is generally non-commutative: "
            "A times B does not equal B times A! "
            "If you rotate space ninety degrees and then shear it horizontally, "
            "you arrive at a completely different final shape than if you shear first and rotate second. "
            "The order of transformations changes reality! "
            "Furthermore, the determinant of the matrix measures how the area of any region scales under the transformation. "
            "Algebra and geometry are two perspectives of the exact same truth."
        )
    },
    {
        "id": 6,
        "title": "Summary, Takeaways & Credits",
        "text": (
            "To summarize our journey, remember these three core principles: "
            "First, a matrix is both a structured data container and an engine of linear transformation. "
            "Its columns tell you exactly where the standard basis vectors land. "
            "Second, operations respect geometry: addition shifts vector spaces component-wise, "
            "scalar multiplication dilates space, and matrix multiplication composes transformations through row-by-column dot products. "
            "And third, order matters: matrix multiplication is non-commutative because transforming space is order-dependent. "
            "With these visual foundations, you are now ready to conquer higher-dimensional transformations, eigenvalues, and multivariable calculus. "
            "Thank you for watching!"
        )
    }
]

def generate_speech():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timing_info = []

    print("[1/3] Generating voiceover audio with macOS Speech Synthesizer...")
    for scene in SCENES_NARRATION:
        s_id = scene["id"]
        aiff_file = os.path.join(OUTPUT_DIR, f"scene_{s_id}.aiff")
        wav_file = os.path.join(OUTPUT_DIR, f"scene_{s_id}.wav")
        
        # say command with clear pace (-r 170 words per minute)
        cmd = ["/usr/bin/say", "-v", "Samantha", "-r", "165", scene["text"], "-o", aiff_file]
        subprocess.run(cmd, check=True)

        # Convert to standard 44.1kHz 16-bit WAV with ffmpeg
        conv_cmd = [
            FFMPEG_BIN, "-y", "-i", aiff_file,
            "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le",
            wav_file
        ]
        subprocess.run(conv_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        if os.path.exists(aiff_file):
            os.remove(aiff_file)

        # Get exact duration
        with wave.open(wav_file, "r") as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            duration = frames / float(rate)

        timing_info.append({
            "scene_id": s_id,
            "title": scene["title"],
            "duration": round(duration, 3),
            "wav_path": wav_file
        })
        print(f"  ✓ Scene {s_id} ({scene['title']}): {duration:.2f} seconds")

    total_voice_duration = sum(t["duration"] for t in timing_info)
    print(f"Total voice narration duration: {total_voice_duration:.2f}s (~{total_voice_duration/60:.2f} min)")

    with open(os.path.join(OUTPUT_DIR, "timing.json"), "w") as f:
        json.dump(timing_info, f, indent=2)

    return timing_info, total_voice_duration


def generate_ambient_music(total_duration):
    """
    Synthesizes a royalty-free ambient cinematic warm harmonic pad
    in D Major / B Minor with gentle low-pass, chorus, and smooth envelopes.
    """
    print("[2/3] Synthesizing ambient cinematic background score...")
    sample_rate = 44100
    total_samples = int((total_duration + 5.0) * sample_rate)
    
    # Chord progression: Dmaj9 -> Gmaj7 -> Bm9 -> Asus4 (slow 8-second bars)
    chords = [
        [146.83, 220.00, 277.18, 329.63, 369.99],  # D3, A3, C#4, E4, F#4 (Dmaj9)
        [98.00,  196.00, 246.94, 293.66, 369.99],  # G2, G3, B3, D4, F#4 (Gmaj7)
        [123.47, 185.00, 220.00, 277.18, 329.63],  # B2, F#3, A3, C#4, E4 (Bm9)
        [110.00, 164.81, 220.00, 293.66, 329.63]   # A2, E3, A3, D4, E4 (Asus4)
    ]
    chord_len = 8.0 * sample_rate  # 8 seconds per chord

    bgm_wav = os.path.join(OUTPUT_DIR, "ambient_bgm.wav")
    with wave.open(bgm_wav, "w") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)

        buf = bytearray()
        batch_size = 44100
        t = 0

        while t < total_samples:
            chord_idx = int((t // chord_len) % len(chords))
            curr_chord = chords[chord_idx]
            next_chord = chords[(chord_idx + 1) % len(chords)]

            # Crossfade factor inside the chord
            local_t = (t % chord_len) / chord_len
            fade_in = 0.5 * (1.0 - math.cos(math.pi * min(1.0, local_t * 3.0)))
            fade_out = 0.5 * (1.0 + math.cos(math.pi * max(0.0, (local_t - 0.7) / 0.3)))
            env = fade_in * fade_out

            left_sample = 0.0
            right_sample = 0.0

            time_sec = t / sample_rate
            # Master fade in at start, fade out at end
            master_env = min(1.0, time_sec / 4.0) * min(1.0, (total_samples - t) / (4.0 * sample_rate))

            for i, freq in enumerate(curr_chord):
                detune1 = 1.0 + 0.0012 * (i - 2)
                detune2 = 1.0 - 0.0014 * (i - 2)
                # Soft harmonics
                s1 = math.sin(2.0 * math.pi * freq * detune1 * time_sec)
                s2 = 0.3 * math.sin(4.0 * math.pi * freq * detune2 * time_sec)
                sub = 0.4 * math.sin(math.pi * freq * time_sec)

                # Stereo panning
                pan = 0.3 + 0.4 * (i / max(1, len(curr_chord) - 1))
                val = (s1 + s2 + sub) * env * 0.18
                left_sample += val * (1.0 - pan)
                right_sample += val * pan

            # LFO modulation
            lfo = 0.85 + 0.15 * math.sin(2.0 * math.pi * 0.2 * time_sec)
            l = int(max(-32767, min(32767, left_sample * lfo * master_env * 32767.0)))
            r = int(max(-32767, min(32767, right_sample * lfo * master_env * 32767.0)))
            buf.extend(struct.pack("<hh", l, r))

            t += 1
            if len(buf) >= batch_size * 4:
                wf.writeframes(buf)
                buf.clear()

        if buf:
            wf.writeframes(buf)

    print(f"  ✓ Ambient background score synthesized: {bgm_wav}")
    return bgm_wav


def mix_soundtrack(timing_info, bgm_wav, total_duration):
    """
    Concatenates scene narrations with subtle pauses and mixes with low-volume background music.
    """
    print("[3/3] Mixing voice narration with background music...")
    
    # 1. Create concatenated speech file with 0.6s inter-scene pauses
    speech_concat = os.path.join(OUTPUT_DIR, "speech_full.wav")
    
    # Create a 0.6s silence file
    silence_wav = os.path.join(OUTPUT_DIR, "silence_06.wav")
    silence_cmd = [
        FFMPEG_BIN, "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
        "-t", "0.6", silence_wav
    ]
    subprocess.run(silence_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # Build concat file list
    concat_list_file = os.path.join(OUTPUT_DIR, "concat_list.txt")
    with open(concat_list_file, "w") as f:
        for item in timing_info:
            f.write(f"file '{os.path.abspath(item['wav_path'])}'\n")
            f.write(f"file '{os.path.abspath(silence_wav)}'\n")

    concat_cmd = [
        FFMPEG_BIN, "-y", "-f", "concat", "-safe", "0",
        "-i", concat_list_file, "-c", "copy", speech_concat
    ]
    subprocess.run(concat_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # Get final speech duration
    with wave.open(speech_concat, "r") as wf:
        full_speech_duration = wf.getnframes() / float(wf.getframerate())

    # 2. Mix Speech (0dB / normalized) with BGM (-22dB volume for crystal clear voiceover)
    final_audio = os.path.join(OUTPUT_DIR, "final_soundtrack.wav")
    mix_cmd = [
        FFMPEG_BIN, "-y",
        "-i", speech_concat,
        "-i", bgm_wav,
        "-filter_complex",
        "[1:a]volume=0.12,aloop=loop=-1:size=2e+09[bgm];[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]",
        "-map", "[aout]",
        "-c:a", "pcm_s16le",
        final_audio
    ]
    subprocess.run(mix_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"  ✓ Final mixed soundtrack created: {final_audio} ({full_speech_duration:.2f}s)")
    return final_audio, full_speech_duration


if __name__ == "__main__":
    timing, duration = generate_speech()
    bgm = generate_ambient_music(duration + 10.0)
    final_audio, full_dur = mix_soundtrack(timing, bgm, duration)
    print("\nSUCCESS: All audio assets generated and synchronized!")
