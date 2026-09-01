# RingFlow 🎵

An automated YouTube-to-Ringtone pipeline that generates high-fidelity ringtones for Android and iOS with loudness normalization and embedded thumbnail artwork.

## Features
- **Android Support (`.mp3`):** 320 kbps MP3 at 48 kHz with embedded video thumbnail album art.
- **iPhone Support (`.m4r`):** 256 kbps AAC in an Apple iPod container.
- **Loudness Normalization:** Built-in EBU R128 (`-16 LUFS`) filtering for clear playback on phone speakers.
- **Automatic FFmpeg Management:** Bundles static FFmpeg binaries seamlessly.

## Quick Start (From Source)
1. Clone the repository:
   ```bash
   git clone https://github.com/7abhijithm/RingFlow.git
   cd RingFlow