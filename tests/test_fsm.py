import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from engine.fsm import StrokeFSM

fsm = StrokeFSM(confirm_frames=1)

print("===== FSM TEST START =====")

sequence = [
    "RECOVERY",
    "CATCH",
    "DRIVE",
    "FINISH",
    "RECOVERY",
]

expected = [
    "RECOVERY",
    "CATCH",
    "DRIVE",
    "FINISH",
    "RECOVERY",
]

for i, phase in enumerate(sequence):
    state = fsm.update(phase)

    print(f"Input : {phase}")
    print(f"State : {state}")

    assert state == expected[i]

print()

assert fsm.completed_stroke == True

print("Stroke Completed :", fsm.completed_stroke)
print("FSM TEST PASS")
