import importlib

mods = [
    ("tensorflow", lambda m: getattr(m, "__version__", "unknown")),
    ("transformers", lambda m: getattr(m, "__version__", "unknown")),
    ("datasets", lambda m: getattr(m, "__version__", "unknown")),
    ("sklearn", lambda m: getattr(m, "__version__", "unknown")),
    ("numpy", lambda m: getattr(m, "__version__", "unknown")),
    ("pandas", lambda m: getattr(m, "__version__", "unknown")),
    ("huggingface_hub", lambda m: getattr(m, "__version__", "unknown")),
    ("kaggle", lambda m: getattr(m, "__version__", "installed")),
]

for name, getter in mods:
    try:
        mod = importlib.import_module(name)
        print(f"{name}: {getter(mod)}")
    except Exception as e:
        print(f"{name}: ImportError -> {e.__class__.__name__}: {e}")
