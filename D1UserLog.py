import re
from datetime import datetime
from collections import defaultdict

def parse_log_line(line):
    """
    Parse a single log line of the form:
      [YYYY-MM-DD HH:MM:SS] [LEVEL] Message text
    Returns a dict with timestamp, level, and message, or None if no match.
    """
    pattern = r"\[(.*?)\] \[(.*?)\] (.*)"
    match = re.match(pattern, line)
    if not match:
        return None
    raw_ts, level, message = match.groups()
    ts = datetime.strptime(raw_ts, "%Y-%m-%d %H:%M:%S")
    return {"timestamp": ts, "level": level, "message": message.strip()}

def detect_consecutive_failures(log_path, threshold=3):
    """
    Scan the given log file and print an alert for any user
    who reaches `threshold` consecutive login failures in a single day.
    """
    # user → date → list of login messages (in chronological order)
    user_daily_logs = defaultdict(lambda: defaultdict(list))

    # Step 1: Read and bucket login events
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            data = parse_log_line(line)
            if not data:
                continue
            ts = data["timestamp"]
            msg = data["message"]
            date = ts.date()

            if "Login failed for user:" in msg:
                user = msg.split(":")[-1].strip()
                user_daily_logs[user][date].append("FAIL")
            elif "Login successful for user:" in msg:
                user = msg.split(":")[-1].strip()
                user_daily_logs[user][date].append("SUCCESS")
            # ignore any other messages

    # Step 2: Analyze each user's daily sequences
    for user, days in user_daily_logs.items():
        for day, results in days.items():
            streak = 0
            for result in results:
                if result == "SUCCESS":
                    streak = 0
                elif result == "FAIL":
                    streak += 1
                    if streak >= threshold:
                        print(f"[ALERT] {user} had {streak} consecutive failures on {day}")
                        break
                # ignore other kinds of entries
    print(user_daily_logs)

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python detect_failures.py <log_file> [threshold]")
        sys.exit(1)

    log_file = sys.argv[1]
    try:
        thresh = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    except ValueError:
        print("Threshold must be an integer")
        sys.exit(1)

    detect_consecutive_failures(log_file, threshold=thresh)
