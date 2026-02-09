import re

INPUT_FILE = "captions_log.txt"
OUTPUT_FILE = "captions_cleaned.txt"

IGNORE_PHRASES = [
    "Ready to show live captions",
    "English (India)"
]

def normalize(text):
    """Normalize text for matching."""
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    return " ".join(text.lower().split())

def clean_transcript():
    print("🧹 Cleaning transcript (global superset removal)...")

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        raw_lines = [line.strip() for line in f if line.strip()]

    # Remove junk UI lines
    raw_lines = [
        line for line in raw_lines
        if not any(x in line for x in IGNORE_PHRASES)
    ]

    # Normalize all lines
    norm_lines = [normalize(l) for l in raw_lines]

    keep = [True] * len(raw_lines)

    # -------------------------------
    # GLOBAL SUPerset Removal
    # If line i is contained inside ANY later line j → drop i
    # -------------------------------
    for i in range(len(raw_lines)):
        for j in range(i + 1, len(raw_lines)):
            if norm_lines[i] and norm_lines[i] in norm_lines[j]:
                keep[i] = False
                break

    # Build final cleaned output
    cleaned = [raw_lines[i] for i in range(len(raw_lines)) if keep[i]]

    # Save
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for line in cleaned:
            f.write(line + "\n")

    print("✅ Clean transcript saved to:", OUTPUT_FILE)
    print("📌 Lines reduced:", len(raw_lines), "→", len(cleaned))


if __name__ == "__main__":
    clean_transcript()
