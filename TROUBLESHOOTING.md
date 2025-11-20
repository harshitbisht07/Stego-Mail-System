# Gmail Connection Troubleshooting Guide

## Quick Fix Checklist

### ✅ Step 1: Enable 2-Step Verification
1. Go to [myaccount.google.com](https://myaccount.google.com)
2. Click **Security** → **2-Step Verification**
3. Follow the setup process if not already enabled

### ✅ Step 2: Generate App Password
1. In Google Account settings, go to **Security** → **App passwords**
2. Select **Mail** as the app
3. Copy the 16-character password (format: xxxx xxxx xxxx xxxx)
4. **Important**: Use this App Password, NOT your regular Gmail password

### ✅ Step 3: Test Your Setup
Run the connection test:
```bash
python test_gmail_connection.py
```

## Common Issues & Solutions

### Issue 1: "Authentication Failed"
**Cause**: Using regular password instead of App Password
**Solution**: Generate and use App Password

### Issue 2: "Invalid Email Format"
**Cause**: Missing @gmail.com or typos
**Solution**: Use full email: `yourname@gmail.com`

### Issue 3: "Connection Refused"
**Cause**: Network/firewall issues
**Solution**: Check internet connection and firewall settings

### Issue 4: "App Password Not Available"
**Cause**: 2-Step Verification not enabled
**Solution**: Enable 2-Step Verification first

## Testing Steps

1. **Verify Email Format**:
   ```
   ✅ Correct: harshvardhanbisht90@gmail.com
   ❌ Wrong: harshvardhanbisht90
   ```

2. **Verify App Password**:
   ```
   ✅ Correct: 16 characters (e.g., abcd efgh ijkl mnop)
   ❌ Wrong: Your regular Gmail password
   ```

3. **Test Connection**:
   ```bash
   python test_gmail_connection.py
   ```

## Still Having Issues?

If the connection test still fails, try these additional steps:

1. **Check Gmail Settings**:
   - Ensure "Less secure app access" is not blocking the connection
   - Verify IMAP is enabled (not required but good to check)

2. **Network Issues**:
   - Try from a different network
   - Check if your firewall is blocking port 587

3. **Alternative SMTP Settings**:
   - Server: smtp.gmail.com
   - Port: 587
   - Security: STARTTLS

## Success Indicators

When everything is working correctly, you should see:
```
✅ SUCCESS: Connection established!
🎉 Your credentials are working correctly.
```

Then you can use the main application with confidence!





