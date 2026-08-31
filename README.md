# RingFlow 🎵

An automated YouTube-to-Ringtone tool that extracts, normalizes, tags, and exports high-fidelity ringtones for both Android and iPhone devices.

---

## ⚡ Option 1: Quick Start (No Python Required)

If you just want to create ringtones without installing Python:

1. Go to the [Releases](https://github.com/7abhijithm/RingFlow/releases) page.
2. Download the latest `RingFlow-v1.0.0-Windows.zip`.
3. Extract the `.zip` archive to any folder.
4. Double-click **`RingFlow.exe`**.
5. Paste any YouTube link and press **Enter**.

---

## 🛠️ Option 2: Run From Source (Developers)

### Prerequisites
* **Python 3.10+** installed on your system.
* **Git** installed.

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/7abhijithm/RingFlow.git
   cd RingFlow
   python -m venv env
   env\Scripts\activate
   pip install -r requirements.txt
   python main.py
