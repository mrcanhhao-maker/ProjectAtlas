import sys
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, ROOT)

from engine.fsm import StrokeFSM

fsm = StrokeFSM(confirm_frames=2)

while True:
    s = input("Phase (RECOVERY/CATCH/DRIVE/FINISH, q=quit): ").strip().upper()
    if s == "Q":
        break

    state = fsm.update(s)

    print(
        "Candidate:", s,
        "| FSM:", state,
        "| Changed:", fsm.state_changed,
        "| Stroke:", fsm.completed_stroke
    )
