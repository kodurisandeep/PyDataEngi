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

def extract_email_and_domain(message):
    """
    Extract email and domain from a log message.
    Returns (email, domain) or (None, None) if not found.
    """
    match = re.search(r"[\w\.-]+@([\w\.-]+)", message)
    if match:
        full_email = match.group(0)
        domain = match.group(1)
        return full_email, domain
    return None, None

def detect_consecutive_failures(log_path, threshold=3):
    """
    Scan the given log file and print an alert for any user
    who reaches `threshold` consecutive login failures in a single day.
    """
    user_daily_logs = defaultdict(lambda: defaultdict(list))  # email → date → events
    domain_counter = defaultdict(int)

    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            data = parse_log_line(line)
            if not data:
                continue
            ts = data["timestamp"]
            msg = data["message"]
            date = ts.date()

            email, domain = extract_email_and_domain(msg)
            if not email:
                continue  # Skip non-login lines

            if "Login failed for user:" in msg:
                user_daily_logs[email][date].append("FAIL")
                domain_counter[domain] += 1
            elif "Login successful for user:" in msg:
                user_daily_logs[email][date].append("SUCCESS")

    for user_email, daily_attempts in user_daily_logs.items():
        for day, sequence in daily_attempts.items():
            streak = 0
            for result in sequence:
                if result == "SUCCESS":
                    streak = 0
                elif result == "FAIL":
                    streak += 1
                    if streak >= threshold:
                        print(f"[ALERT] {user_email} had {streak} consecutive failures on {day}")
                        break

    print("\n📊 Login failure counts by domain:")
    for domain, count in domain_counter.items():
        print(f"  {domain}: {count} failed attempts")

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