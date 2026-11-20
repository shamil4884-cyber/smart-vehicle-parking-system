# Smart Parking System — Setup (Windows)

1. Open the `smart-vehicle-parking-system-main` folder in VS Code (the folder containing `manage.py`).
2. In its terminal run `python -m pip install -r requirements.txt`.
3. Set the Gemini key **in the terminal only**, never in HTML, Python files or a public GitHub repository.
   - PowerShell: `$env:GEMINI_API_KEY="YOUR_NEW_KEY"`
   - Command Prompt: `set GEMINI_API_KEY=YOUR_NEW_KEY`
4. Optional: set a model available to your Gemini account, e.g. PowerShell `$env:GEMINI_MODEL="gemini-3.8-flash"`. Check available models if that one is unavailable.
5. Run `python manage.py migrate` and `python manage.py runserver 8001`.
6. Open `http://127.0.0.1:8001/` and use the **Chat with AI** button in the bottom-right.

Keep the server running while testing. If using another port, open that port instead.

The chatbot sends requests to Django at `/api/chatbot/`; it is not a standalone static/Vercel HTML feature. Hosting the frontend on Vercel alone will not run this Django API. A Python-capable host is required for the backend.

If the AI says unavailable, check the Django terminal for the exact error and confirm the key/model are valid. Do not share your key in screenshots or messages.
