#!/usr/bin/env python3
import os
import smtplib
import requests
from email.mime.text import MIMEText
from datetime import date

# ─── CONFIG ────────────────────────────────────────────────────────────────────
NEWS_API_KEY   = os.getenv("NEWS_API_KEY")     
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  
FROM_EMAIL     = os.getenv("FROM_EMAIL")       
FROM_PASS      = os.getenv("FROM_EMAIL_PASS") 
TO_EMAIL       = os.getenv("TO_EMAIL")         
# ────────────────────────────────────────────────────────────────────────────────

def fetch_headlines():
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "category": "technology",
        "pageSize": 10,
        "apiKey": NEWS_API_KEY,
        "language": "en",
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return [a["title"] for a in resp.json().get("articles", [])]

def summarize_with_gemini(headlines):
    prompt = (
        "Summarize these tech headlines into 5 concise bullet points:\n\n"
        + "\n".join(f"- {h}" for h in headlines)
    )

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }
    body = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    resp = requests.post(url, json=body, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    cand = data["candidates"][0]

    # Extract from content.parts
    content = cand.get("content", {})
    parts = content.get("parts", [])
    text = "".join(p.get("text", "") for p in parts)

    return text.strip()

def send_email(subject: str, body: str):
    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"]    = FROM_EMAIL
    msg["To"]      = TO_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(FROM_EMAIL, FROM_PASS)
        smtp.send_message(msg)

def main():
    headlines = fetch_headlines()
    if not headlines:
        print("No headlines found.")
        return

    # Get raw lines from the model
    raw_summary = summarize_with_gemini(headlines).splitlines()
    today       = date.today().strftime("%B %d, %Y")
    subject     = f"Tech News Digest — {today}"

    body_lines = [
        "Hi there,",
        "",
        f"Here are today’s top tech headlines ({today}):",
        ""
    ]
    for line in raw_summary:
        # remove any leading stars or markdown bold markers:
        clean = line.lstrip(" *").replace("**", "").strip()
        if clean:
            body_lines.append(f"• {clean}")

    body_lines += [
        "",
        "Have a great day!",
        "— Niharika"
    ]
    body = "\n".join(body_lines)

    send_email(subject, body)
    print("Digest sent!")



if __name__ == "__main__":
    main()

