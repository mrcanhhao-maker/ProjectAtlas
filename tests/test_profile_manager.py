import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from engine.profile_manager import ProfileManager

pm = ProfileManager()

profile = pm.load()

print("===== PROFILE =====")

for phase in profile:
    print(phase, profile[phase])

print()
print("PROFILE TEST PASS")
