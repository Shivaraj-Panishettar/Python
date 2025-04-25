def load_level(level_number):
    try:
        level_module = __import__(f"levels.level{level_number}", fromlist=["create"])
        return level_module.create()
    except ImportError:
        return None  # No more levels

