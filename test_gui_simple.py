# test_gui_simple.py
"""
Simple test for the Shadow AI GUI to verify it works
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Test if basic GUI components work
def test_gui_components():
    """Test basic GUI functionality"""
    
    root = tk.Tk()
    root.title("Shadow AI GUI Test")
    root.geometry("800x600")
    root.configure(bg='#1a1a1a')
    
    # Test modern styling
    style = ttk.Style()
    style.theme_use('clam')
    
    # Create test frame
    main_frame = ttk.Frame(root)
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Test title
    title_label = tk.Label(main_frame, text="🧠 Shadow AI GUI Test", 
                          font=('Segoe UI', 24, 'bold'),
                          bg='#1a1a1a', fg='#ffffff')
    title_label.pack(pady=20)
    
    # Test status indicator
    status_frame = tk.Frame(main_frame, bg='#1a1a1a')
    status_frame.pack(pady=10)
    
    status_canvas = tk.Canvas(status_frame, width=16, height=16, 
                             bg='#1a1a1a', highlightthickness=0)
    status_canvas.pack(side='left', padx=(0, 10))
    status_canvas.create_oval(2, 2, 14, 14, fill='#4ade80', outline="")
    
    status_label = tk.Label(status_frame, text="GUI Test Running", 
                           bg='#1a1a1a', fg='#ffffff')
    status_label.pack(side='left')
    
    # Test input field
    input_label = tk.Label(main_frame, text="Test Input Field:", 
                          bg='#1a1a1a', fg='#b0b0b0')
    input_label.pack(anchor='w', pady=(20, 5))
    
    input_field = tk.Text(main_frame, height=3, font=('Segoe UI', 11),
                         bg='#404040', fg='#ffffff', 
                         insertbackground='#00d4aa', relief='flat',
                         wrap='word', padx=15, pady=10)
    input_field.pack(fill='x', pady=(0, 10))
    input_field.insert('1.0', "Type a test command here...")
    
    # Test buttons
    button_frame = tk.Frame(main_frame, bg='#1a1a1a')
    button_frame.pack(fill='x', pady=10)
    
    test_btn = tk.Button(button_frame, text="✨ Test Button", 
                        font=('Segoe UI', 11, 'bold'),
                        bg='#00d4aa', fg='white', relief='flat',
                        padx=30, pady=12,
                        command=lambda: print("✅ Button clicked!"))
    test_btn.pack(side='left', padx=(0, 10))
    
    close_btn = tk.Button(button_frame, text="❌ Close Test", 
                         font=('Segoe UI', 11),
                         bg='#f87171', fg='white', relief='flat',
                         padx=20, pady=12,
                         command=root.destroy)
    close_btn.pack(side='left')
    
    # Test log area
    log_label = tk.Label(main_frame, text="📝 Test Log:", 
                        bg='#1a1a1a', fg='#ffffff',
                        font=('Segoe UI', 14, 'bold'))
    log_label.pack(anchor='w', pady=(20, 10))
    
    log_text = tk.Text(main_frame, height=8, font=('Consolas', 10),
                      bg='#404040', fg='#ffffff', relief='flat', wrap='word')
    log_text.pack(fill='both', expand=True)
    
    # Add test messages
    import datetime
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    test_messages = [
        f"[{timestamp}] 🚀 GUI components initialized successfully",
        f"[{timestamp}] ✅ Tkinter is working properly", 
        f"[{timestamp}] 🎨 Dark theme applied",
        f"[{timestamp}] 🎯 All widgets created successfully",
        f"[{timestamp}] 💡 Click buttons to test functionality",
        f"[{timestamp}] 🧠 Ready for Shadow AI integration!"
    ]
    
    for msg in test_messages:
        log_text.insert(tk.END, msg + "\n")
    
    log_text.config(state='disabled')
    
    print("🎨 Shadow AI GUI Test Window Opened")
    print("✅ Basic components are working")
    print("🔄 Close the test window when ready")
    
    root.mainloop()

if __name__ == "__main__":
    print("🧠 Shadow AI GUI Component Test")
    print("=" * 40)
    print("Testing basic GUI functionality...")
    print()
    
    try:
        test_gui_components()
        print("✅ GUI test completed successfully!")
    except Exception as e:
        print(f"❌ GUI test failed: {e}")
        print("Please check your Python and tkinter installation")
