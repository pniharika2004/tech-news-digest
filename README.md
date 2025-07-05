# Daily Tech News Digest

This script fetches today’s top technology headlines, summarizes them into a 5-bullet digest using Google Gemini, and emails the result to a specified recipient.

## Features

- **Fetch** tech headlines from [NewsAPI](https://newsapi.org).
- **Summarize** headlines with Google Gemini (`gemini-2.0-flash` model).
- **Send** the digest via Gmail SMTP using an App Password.

## Prerequisites

1. **Python 3.8+**
2. A **NewsAPI** key (free signup at [https://newsapi.org](https://newsapi.org)).
3. A **Google Cloud** API key with Generative Language API enabled.
4. A **Gmail** account with 2-Step Verification enabled and an App Password generated.

## Setup

1. **Clone the repository** (or save `daily_digest.py` locally):

   ```bash
   git clone https://github.com/pniharika2004/tech-news-digest.git
   cd tech-news-digest
   ```

2. **Create and activate** a Python virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install requests
   ```

4. **Generate a Gmail App Password**:

   - Go to your Google Account settings: [https://myaccount.google.com/security](https://myaccount.google.com/security)
   - Under **"Signing in to Google"**, ensure **2-Step Verification** is turned **On**.
   - Click **App passwords**.
   - Under **Select app**, choose **Mail**.
   - Under **Select device**, choose **Other (Custom name)** and name it (e.g., "NewsDigestScript").
   - Click **Generate** and copy the 16-character password.

5. **Set environment variables**:

   ```bash
   export NEWS_API_KEY="<your_newsapi_key>"
   export GEMINI_API_KEY="<your_google_cloud_api_key>"
   export FROM_EMAIL="your.email@gmail.com"
   export FROM_EMAIL_PASS="<your_16_char_app_password>"
   export TO_EMAIL="recipient.email@example.com"
   ```

   > **Note:** Replace placeholders with your actual keys and emails.

## Usage

Run the script manually:

```bash
python daily_digest.py
```

You should see:

```
Digest sent!
```

and the recipient will receive a 5-bullet summary of today’s top tech news.

## Automation (Optional)

To run daily at 8 AM using `cron`:

```bash
crontab -e
```

Add the following line (adjust paths accordingly):

```cron
0 8 * * * cd /path/to/tech-news-digest && /path/to/.venv/bin/python daily_digest.py >> digest.log 2>&1
```

Save and exit. The script will now run every morning.

## Troubleshooting

- **HTTP 400/404** errors:

  - Verify your API keys and endpoints.
  - Ensure the Generative Language API is enabled in Google Cloud Console.

- **SMTP AuthenticationError**:

  - Confirm you’re using the generated App Password, not your Gmail login password.
  - Ensure 2-Step Verification is enabled on your Google account.

- **No headlines found**:

  - Check that your NewsAPI key is valid and has sufficient quota.

## License

MIT © Niharika
