import pickle
import os

# --- 1. CRITICAL: Triggers arbitrary command execution (e.g., shell commands) ---
class CriticalMalicious:
    def __reduce__(self):
        # This will trigger a "CRITICAL" alert in ModelScan
        return (os.system, ("echo 'CRITICAL DETECTED'",))

# --- 2. HIGH: Triggers dangerous global usage (e.g., networking/browser) ---
class HighRisk:
    def __reduce__(self):
        import webbrowser
        # Using built-ins that interact with the network or OS often flag as HIGH
        return (webbrowser.open, ("http://malicious-site.com",))

# Save the files
with open("test_critical.pkl", "wb") as f:
    pickle.dump(CriticalMalicious(), f)

with open("test_high.pkl", "wb") as f:
    pickle.dump(HighRisk(), f)

print("Files created: test_critical.pkl, test_high.pkl")
