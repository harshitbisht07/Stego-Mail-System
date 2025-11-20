"""
Diagnostic script to identify VS Code/GUI issues
"""

import sys
print("Python version:", sys.version)
print("Platform:", sys.platform)

try:
    print("Testing tkinter import...")
    import tkinter as tk
    print("✅ Tkinter imported successfully")
    
    print("Testing tkinter window creation...")
    root = tk.Tk()
    root.title("Test Window")
    root.geometry("300x200")
    
    label = tk.Label(root, text="If you see this, tkinter is working!")
    label.pack(pady=50)
    
    print("✅ Tkinter window created successfully")
    print("Window should appear now...")
    
    # Show window for 3 seconds then close
    root.after(3000, root.destroy)
    root.mainloop()
    
    print("✅ Tkinter test completed successfully")
    
except Exception as e:
    print(f"❌ Error with tkinter: {e}")
    import traceback
    traceback.print_exc()

print("Diagnostic complete!")







