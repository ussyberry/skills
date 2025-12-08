import sys
try:
    with open("env_check.txt", "w") as f:
        f.write("Python is running\n")
        try:
            import reportlab
            f.write(f"Reportlab imported: {reportlab.__file__}\n")
        except ImportError:
            f.write("Reportlab MISSING\n")
        except Exception as e:
            f.write(f"Other error: {e}\n")
except Exception as e:
    pass # Can't log failure to write log
