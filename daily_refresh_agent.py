import schedule
import time
import subprocess
import os
from datetime import datetime

# Configuration
TRACKER_PATH = r"C:\Users\rajki\OneDrive\Desktop\investment\commodity_tracker.py"
REFRESH_TIME = "08:00"  # 8 AM daily

def run_tracker():
    """Launch the Streamlit tracker"""
    print(f"\n{'='*50}")
    print(f"🚀 Starting tracker at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")
    
    try:
        # Check if file exists
        if not os.path.exists(TRACKER_PATH):
            print(f"❌ Error: File not found at {TRACKER_PATH}")
            return
        
        # Launch Streamlit
        subprocess.Popen(['streamlit', 'run', TRACKER_PATH])
        print("✅ Tracker launched successfully!")
        print(f"📊 Access it at: http://localhost:8501")
        
    except Exception as e:
        print(f"❌ Error launching tracker: {e}")

def main():
    print("🤖 Daily Refresh Agent Started!")
    print(f"⏰ Scheduled to run daily at {REFRESH_TIME}")
    print(f"📁 Tracking file: {TRACKER_PATH}")
    print("\nPress Ctrl+C to stop the agent\n")
    
    # Schedule the job
    schedule.every().day.at(REFRESH_TIME).do(run_tracker)
    
    # Optional: Run once immediately on startup
    print("▶️  Running tracker now (startup)...")
    run_tracker()
    
    # Keep the agent running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Agent stopped by user")
    except Exception as e:
        print(f"\n❌ Agent error: {e}")