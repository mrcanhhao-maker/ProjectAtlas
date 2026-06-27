from pathlib import Path

print("ProjectAtlas Status")
print("===================")
print("Version:", Path("VERSION").read_text().strip() if Path("VERSION").exists() else "unknown")
print("atlas_core:", Path("atlas_core").exists())
print("legacy app:", Path("plugins/visionrow/app_alpha6.py").exists())
print("motion v2:", Path("atlas_core/motion_engine.py").exists())
