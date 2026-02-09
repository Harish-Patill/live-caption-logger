# Live Caption Logger

**Live Caption Logger** is a lightweight Python tool that captures text directly from **Windows Live Captions** in real time and saves it into a text file.It works completely offline and is especially useful for logging spoken content during lectures, meetings, or video sessions.

---

## How to Use
###TRANSCRIBE
1. Turn on Windows Live Captions  
   - Settings → Accessibility → Live Captions → ON  

2. Run the logger script from the project folder by running the following command in the terminal:
    ```bash
    python live_caption_logger.py

3. A tray icon will appear in the system tray.
    - Right-click the tray icon and select:
   -- Start Logging (begins capturing captions)
   - When finished, right-click the same tray icon and select:
   --Stop Logging (stops capturing)
   - You can view the saved transcript anytime by selecting:
   -- Open Log File
4. The raw transcript is saved in:
    ```bash
   captions_log.txt
###CLEANUP
1. Run the terminal
   ```bash
   python cleaner.py
2. The cleaned and deduplicated transcript will be generated in :
   ```bash
   cleaned_transcript.txt

   
   
   

