# Smart Parking – Updated Version

## Changes
- Modern responsive styling shared across the Django templates.
- New floating AI chat panel on the home page.
- Django `/api/chatbot/` POST endpoint, CSRF-aware frontend, and server-side Gemini API access.
- Model defaults to `gemini-3.8-flash` (as listed by the API key in the debugging session). Override using `GEMINI_MODEL` if your account supports a different model.
- Improved server-side logging without exposing errors to visitors.

## Run locally (Windows PowerShell)
1. Open a terminal in the folder containing `manage.py`.
2. `python -m pip install -r requirements.txt`
3. Set a **new** Gemini key in that terminal: `$env:GEMINI_API_KEY="YOUR_NEW_KEY"`
4. `python manage.py migrate`
5. `python manage.py runserver 8001`
6. Open `http://127.0.0.1:8001/` and test the chatbot.

If the chat fails, inspect the Django terminal logs for the actual Gemini error. Model availability and quotas depend on your API account. The ZIP's existing database is included; do not publish real customer data. For deployment, set `GEMINI_API_KEY` and a new `DJANGO_SECRET_KEY` as server environment variables. Never put either secret in HTML or GitHub.

**Important:** This is an updated copy of the uploaded July archive, not a merge with later local edits. Test authentication, dashboards, and deployment before replacing your working project.
