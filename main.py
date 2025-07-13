
import subprocess
from datetime import datetime

STEPS = [
    ("Niche Discovery", "agents/niche_discovery.py"),
    ("Content Writer", "agents/content_writer.py"),
    ("Image Generator", "agents/image_creator.py"),
    ("Monetizer", "agents/monetizer.py"),
    ("Publisher", "agents/publisher.py"),
    ("SEO Tracker", "agents/tracker.py"),
    ("Content Refresher", "agents/content_updater.py"),
    ("Revenue Tracker", "agents/revenue_tracker.py")
]

LOG_FILE = "data/logs/run_log.txt"

def log(msg):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} {msg}\n")
    print(f"{timestamp} {msg}")

def run_step(name, path):
    log(f"▶ Starting: {name}")
    try:
        result = subprocess.run(["python", path], check=True)
        log(f"✅ Completed: {name}")
    except subprocess.CalledProcessError:
        log(f"❌ FAILED: {name}")

def main():
    log("🚀 === STARTING FULL AUTOMATION ===")
    for name, path in STEPS:
        run_step(name, path)
    log("✅ === ALL MODULES COMPLETED ===")

if __name__ == "__main__":
    main()
