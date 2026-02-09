import time
import threading
import pystray
from pystray import MenuItem as item
from PIL import Image
import uiautomation as auto
import os
import re

# --- Configuration ---
LOG_FILE = "captions_log.txt"
running = False
# Keeps a rolling memory of words to check against repeats
logged_history = []
MAX_HISTORY = 200  # Words to remember for deduplication

def clean_text(text):
    """Removes special icons and extra whitespace."""
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return " ".join(text.split())

def get_all_textcontrols(ctrl):
    """Recursively collect all TextControls inside a UI tree."""
    results = []
    try:
        children = ctrl.GetChildren()
    except:
        return results
    for child in children:
        if child.ControlTypeName == "TextControl":
            if child.Name.strip():
                results.append(child)
        results.extend(get_all_textcontrols(child))
    return results

def get_new_content_only(window_text):
    """
    Checks the last 30 words logged to see if the window is repeating itself.
    Returns only the suffix that hasn't been saved yet.
    """
    global logged_history
    current_words = clean_text(window_text).split()
    
    if not current_words:
        return ""

    if not logged_history:
        logged_history = current_words
        return " ".join(current_words)

    # 1. REPETITION CHECK:
    # We join our recent history into a string and check if the current
    # window content is already completely inside it.
    history_str = " ".join(logged_history[-50:])
    current_win_str = " ".join(current_words)
    
    if current_win_str in history_str:
        return ""

    # 2. OVERLAP STITCHING:
    # We look for the point where the window content continues our history.
    match_index = -1
    # Check for a match using between 1 to 15 words as an anchor.
    for i in range(min(len(logged_history), 15), 0, -1):
        anchor = logged_history[-i:]
        for j in range(len(current_words) - len(anchor) + 1):
            if current_words[j:j+len(anchor)] == anchor:
                match_index = j + len(anchor)
                break
        if match_index != -1:
            break

    # 3. EXTRACT NEW WORDS
    if match_index != -1:
        new_words = current_words[match_index:]
        if new_words:
            logged_history.extend(new_words)
            logged_history = logged_history[-MAX_HISTORY:]
            return " ".join(new_words)
        return ""

    # 4. FALLBACK: If window cleared/jumped, reset history
    logged_history = current_words
    return " ".join(current_words)

def log_loop():
    global running
    print("🚀 Logger Active. History-based deduplication enabled.")
    
    while running:
        try:
            root = auto.GetRootControl()
            caption_ctrl = None
            
            for child in root.GetChildren():
                if "Captions" in child.Name or child.ClassName == "LiveCaptionsWindow":
                    caption_ctrl = child
                    break
            
            if caption_ctrl:
                text_controls = get_all_textcontrols(caption_ctrl)
                if text_controls:
                    raw_text = " ".join([c.Name for c in text_controls])
                    new_chunk = get_new_content_only(raw_text)

                    if new_chunk.strip():
                        with open(LOG_FILE, "a", encoding="utf-8") as f:
                            # Write new unique content on its own line
                            f.write(new_chunk.strip() + "\n")
                            f.flush()
                        print(f"Logged: {new_chunk}")
            
        except Exception:
            pass
        
        # 1.2s delay is better for Indian English accents (longer syllables)
        time.sleep(1.2)

# --- Tray System ---

def toggle_logging(icon, item):
    global running, logged_history
    running = not running
    if running:
        logged_history = [] # Reset history on fresh start
        threading.Thread(target=log_loop, daemon=True).start()
    icon.icon = Image.new('RGB', (64, 64), "red" if running else "blue")

def run_tray():
    menu = pystray.Menu(
        item(lambda text: "Stop" if running else "Start", toggle_logging),
        item("Open Log", lambda: os.startfile(LOG_FILE) if os.path.exists(LOG_FILE) else None),
        item("Exit", lambda icon: icon.stop())
    )
    icon = pystray.Icon("CapLog", Image.new('RGB', (64, 64), "blue"), "Caption Logger", menu)
    icon.run()

if __name__ == "__main__":
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, 'w').close()
    run_tray()