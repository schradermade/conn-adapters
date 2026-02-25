# conn-adapters

Source-specific connector adapters.

## Structure
- `adapters/interface.py`: required adapter interface for runtime integration
- `adapters/gdrive/`: Google Drive adapter models and config

## Adapter Responsibilities
- fetch source objects (full + incremental)
- normalize source objects to base document contract
- emit tombstones
- commit checkpoints

## Current Status
- `gdrive` contains model/config scaffolding
- fetch/emit implementations are pending
