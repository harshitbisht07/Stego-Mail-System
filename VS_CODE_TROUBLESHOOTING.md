# VS Code Troubleshooting Guide

## 🚨 "No Response in VS Code" - Solutions

### **Issue**: Application doesn't respond or GUI doesn't appear

### **Quick Solutions**

#### 1. **Use the Simplified Version**
```bash
python simple_app.py
```
This version has minimal dependencies and should work reliably in VS Code.

#### 2. **Run from Terminal Instead of VS Code**
- Open Command Prompt or PowerShell
- Navigate to your project folder
- Run: `python simple_app.py`

#### 3. **Check Python Installation**
```bash
python --version
python -c "import tkinter; print('Tkinter OK')"
```

### **Common VS Code Issues & Solutions**

#### **Issue 1: GUI Not Appearing**
**Cause**: VS Code terminal might not support GUI properly
**Solution**: 
- Use external terminal (Command Prompt/PowerShell)
- Or use the simplified app: `python simple_app.py`

#### **Issue 2: Import Errors**
**Cause**: Missing dependencies
**Solution**:
```bash
pip install Pillow numpy
```

#### **Issue 3: Application Hangs**
**Cause**: Complex imports or GUI blocking
**Solution**: Use the simplified version with minimal dependencies

### **Recommended Workflow**

1. **For Testing**: Use `simple_app.py`
   ```bash
   python simple_app.py
   ```

2. **For Full Features**: Use external terminal
   ```bash
   python main_enhanced.py
   ```

3. **For Development**: Use VS Code for editing, terminal for running

### **Available Applications**

| Application | Purpose | Dependencies | VS Code Compatible |
|-------------|---------|--------------|-------------------|
| `simple_app.py` | Basic steganography | Pillow, numpy | ✅ Yes |
| `main_enhanced.py` | Full features | All dependencies | ⚠️ Use external terminal |
| `main.py` | Original version | All dependencies | ⚠️ Use external terminal |

### **Quick Test Commands**

```bash
# Test basic functionality
python simple_app.py

# Test enhanced system (use external terminal)
python main_enhanced.py

# Test steganography only
python test_steganography.py
```

### **If Nothing Works**

1. **Check Python Installation**:
   ```bash
   python --version
   ```

2. **Install Basic Dependencies**:
   ```bash
   pip install Pillow numpy
   ```

3. **Use Simple App**:
   ```bash
   python simple_app.py
   ```

4. **Run from External Terminal** (not VS Code terminal)

### **Success Indicators**

✅ **Working**: GUI window appears with interface
✅ **Working**: You can browse and select images
✅ **Working**: You can encode/decode messages
✅ **Working**: Status messages appear

❌ **Not Working**: No window appears
❌ **Not Working**: Application hangs
❌ **Not Working**: Import errors

### **Next Steps**

If the simple app works:
1. You can use it for basic steganography
2. For email features, use external terminal with `main_enhanced.py`
3. The core functionality is working!

The simplified app provides all the essential steganography features without the complexity that might cause VS Code issues.







