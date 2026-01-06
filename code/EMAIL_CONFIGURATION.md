# Email Configuration Guide

This guide explains how to configure email functionality for the Doubt Summarizer export feature.

## Overview

The system now supports sending doubt summary reports via email using FastAPI-Mail. This requires SMTP configuration.

## Prerequisites

✅ `fastapi-mail==1.5.8` - Already added to `requirements.txt` and installed

## Configuration Steps

### 1. Set Environment Variables

Create or update your `.env` file in the `backend/` directory with SMTP credentials:

```bash
# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAILS_FROM_EMAIL=your-email@gmail.com
EMAILS_FROM_NAME=AURA - Academic Assistant
SMTP_TLS=True
SMTP_SSL=False
```

### 2. Gmail Configuration (Recommended for Testing)

If using Gmail, follow these steps:

1. **Enable 2-Factor Authentication**
   - Go to your Google Account settings
   - Security → 2-Step Verification → Turn On

2. **Generate App Password**
   - Go to Google Account → Security → 2-Step Verification
   - Scroll to "App passwords" at the bottom
   - Select "Mail" and your device
   - Copy the 16-character password (e.g., `abcd efgh ijkl mnop`)
   - Use this as your `SMTP_PASSWORD` (without spaces)

3. **Update .env file**
   ```bash
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=abcdefghijklmnop  # Your app password
   ```

### 3. Other Email Providers

#### Outlook/Hotmail
```bash
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_TLS=True
```

#### Yahoo Mail
```bash
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_TLS=True
```

#### SendGrid (Production)
```bash
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=your-sendgrid-api-key
```

#### AWS SES (Production)
```bash
SMTP_HOST=email-smtp.us-east-1.amazonaws.com
SMTP_PORT=587
SMTP_USER=your-aws-smtp-username
SMTP_PASSWORD=your-aws-smtp-password
```

## Testing the Configuration

### 1. Start Backend Server
```bash
cd backend
uvicorn main:app --reload
```

### 2. Test Email Endpoint

Use the Swagger UI at `http://localhost:8000/docs` or send a POST request:

```bash
curl -X POST "http://localhost:8000/api/ta/doubts/export/email" \
  -H "Content-Type: application/json" \
  -d '{
    "course_code": "CS101",
    "period": "weekly",
    "source": null,
    "recipient_email": "recipient@example.com"
  }'
```

### 3. Expected Response

**Success:**
```json
{
  "message": "Report successfully sent to recipient@example.com",
  "recipient": "recipient@example.com",
  "course_code": "CS101",
  "period": "weekly",
  "stats": {
    "total_messages": 45,
    "unique_uploads": 12,
    "topic_clusters": 5,
    "learning_gaps": 3,
    "recurring_issues": 2
  }
}
```

**Error (Not Configured):**
```json
{
  "detail": "Email service not configured. Please set SMTP_USER and SMTP_PASSWORD environment variables."
}
```

## Implementation Details

### Backend Changes

1. **`requirements.txt`** - Added `fastapi-mail==1.4.1`

2. **`app/core/config.py`** - Extended email settings:
   - `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`
   - `EMAILS_FROM_EMAIL`, `EMAILS_FROM_NAME`
   - `SMTP_TLS`, `SMTP_SSL`

3. **`app/api/doubt_summarizer_router.py`** - Integrated FastAPI-Mail:
   - Email configuration with `ConnectionConfig`
   - HTML email body with styled summary statistics
   - PDF attachment generation and sending
   - Error handling for unconfigured SMTP

### Email Format

The system sends professional HTML emails with:
- Course information and period
- Summary statistics table
- PDF attachment with detailed analysis
- AURA branding

### Security Considerations

⚠️ **Important:**
- Never commit `.env` file to version control
- Use app-specific passwords, not account passwords
- For production, use dedicated email service (SendGrid, AWS SES)
- Rotate credentials regularly
- Use environment variables in deployment platforms

## Frontend Integration

The frontend (`ExportOptions.vue`) already includes:
- Email modal with input validation
- Email format validation (regex + Pydantic)
- Success/error message display
- Loading states during send

## Troubleshooting

### "Email service not configured"
- Verify `SMTP_USER` and `SMTP_PASSWORD` are set in `.env`
- Restart backend server after updating `.env`

### "Authentication failed"
- For Gmail, ensure you're using an App Password, not account password
- Check 2FA is enabled on your account
- Verify credentials are correct (no extra spaces)

### "Connection timeout"
- Check firewall/antivirus settings
- Verify SMTP port is not blocked
- Try alternative ports (465 for SSL, 587 for TLS)

### "SSL/TLS error"
- For Gmail, use `SMTP_TLS=True` and `SMTP_SSL=False`
- For port 465, use `SMTP_SSL=True` and `SMTP_TLS=False`

## Production Deployment

For production environments:

1. **Use Professional Email Service**
   - SendGrid (12,000 free emails/month)
   - AWS SES (pay-as-you-go)
   - Mailgun
   - Postmark

2. **Set Environment Variables**
   - Use platform-specific secrets management
   - Heroku: `heroku config:set SMTP_USER=...`
   - AWS: Use Parameter Store or Secrets Manager
   - Docker: Use secrets or environment files

3. **Monitor Email Delivery**
   - Track bounce rates
   - Monitor spam complaints
   - Implement retry logic for failures

## Example `.env` File (Complete)

```bash
# Application
APP_NAME=AURA
DEBUG=True
API_PREFIX=/api

# Database
DATABASE_URL=sqlite:///./app.db

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=aura.system@gmail.com
SMTP_PASSWORD=abcdefghijklmnop
EMAILS_FROM_EMAIL=aura.system@gmail.com
EMAILS_FROM_NAME=AURA - Academic Assistant
SMTP_TLS=True
SMTP_SSL=False

# AI/LLM
GOOGLE_API_KEY=your-gemini-api-key
```

## File Location Changes

✅ **Router Moved:**
- From: `backend/app/routers/doubt_summarizer_router.py`
- To: `backend/app/api/doubt_summarizer_router.py`
- Updated import in `main.py`

This consolidates all API endpoints in the `api/` folder for better organization.

## Support

For issues or questions:
1. Check error messages in backend logs
2. Verify `.env` configuration
3. Test SMTP credentials with a simple email client
4. Review FastAPI-Mail documentation: https://sabuhish.github.io/fastapi-mail/
