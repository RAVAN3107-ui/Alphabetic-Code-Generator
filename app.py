import sys

try:
    from gui.main_window import main
except ImportError as e:
    print(f"Error: Could not import GUI module. Make sure PySide6 is installed.")
    print(f"Details: {e}")
    print("\nTo install dependencies, run:")
    print("  pip install -r requirements.txt")
    sys.exit(1)

if __name__ == "__main__":
    main()
