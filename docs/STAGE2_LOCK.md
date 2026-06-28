# ProjectAtlas Stage 2 Lock

Version: Alpha12.14
Stage: 2
Status: VIRTUAL_ROWER_LOCKED

## Goal

Stage 2 builds the Virtual Rower Engine.

The system converts camera rowing motion into virtual rowing machine metrics that can later be mapped to BLE FTMS data.

## Completed Components

- Virtual rower engine core
- Virtual watts estimator
- Pace /500m estimator
- Speed estimator
- Distance accumulator
- Camera drive_speed activation
- Camera drive_speed power estimator
- Virtual rower dashboard
- Session recorder
- Runtime session log ignore rules
- Stage 2 healthcheck gate
- Virtual rower test gate

## Production Files

engine/
    virtual_rower.py
    session_recorder.py

plugins/
    visionrow/
        alpha12/
            app_alpha12.py

scripts/
    stage2_healthcheck.py

tests/
    test_virtual_rower_engine.py

docs/
    STAGE1_LOCK.md
    STAGE1_COMPLETE.md
    STAGE2_LOCK.md

## Required Gate

Before moving toward BLE or FTMS, this command must pass:

python scripts/stage2_healthcheck.py

Expected result:

stage: stage2
status: PASS

## Stage 2 Boundary

Stage 2 does not include:

- BLE advertising
- BLE GATT server
- FTMS characteristic encoding
- MyWhoosh pairing
- Real Bluetooth connection
- External rowing hardware

These belong to the next stage.

## Confirmed Runtime

Alpha12 dashboard runs from MacBook camera and shows:

- Virtual Watts
- Pace /500m
- Speed
- Distance
- Moving state

Session logs are stored locally in sessions/ and ignored by Git.

## Next

Stage 3: BLE FTMS preparation.
