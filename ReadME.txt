# 🎙️ Live Captions Transcript Logger + Cleaner (Windows)

A lightweight Python tool that captures **Windows Live Captions** in real-time, logs them into a text file, and provides a second script to automatically clean and deduplicate the transcript into readable notes.

This is especially useful for:
* **Online lectures**
* **Meetings / Zoom calls**
* **Accessibility transcription**
* **Study note generation**

---

## 🚀 Features

### ✅ Real-Time Caption Logging
* **Direct UI Integration:** Reads text directly from the Windows Live Captions window.
* **Live Updates:** Continuously saves new spoken words into a log file.
* **Smart Deduplication:** Prevents excessive repetition using history-based logic.

### ✅ Transcript Cleanup Script
* **Noise Removal:** Strips out duplicated expanding sentences.
* **UI Artifact Cleaning:** Removes system junk like `Ready to show live captions...`.
* **Readable Output:** Produces a concise, paragraph-based transcript.

### ✅ Tray App Support
* **Background Operation:** Runs quietly in the system tray.
* **Status Indicators:** Icon turns **red** when recording and **blue** when idle.
* **Start/Stop Control:** Toggle logging anytime without closing the app.

---

## 📂 Project Structure

| File | Description |
| :--- | :--- |
| `live_caption_logger.py` | The main tray application for real-time logging. |
| `clean_transcript.py` | Script to process raw logs into readable notes. |
| `captions_log.txt` | The raw output (auto-generated). |
| `captions_cleaned.txt` | The final polished transcript (auto-generated). |

---

## 🛠️ Requirements

You will need the following Python libraries:
```bash
pip install uiautomation pystray Pillow
