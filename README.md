# Kitty Gift Choice

A cute pink Hello Kitty gift selection page with a result page for viewing the chosen gift.

## Run locally

```bash
cd /Users/cuize/kitty-gift-site
python3 server.py
```

Then open:

- http://localhost:8000/
- http://localhost:8000/result.html

The app uses the `PORT` environment variable when deployed, while defaulting to 8000 locally.

## Deploy to Render

1. Push this folder to GitHub.
2. Go to https://dashboard.render.com
3. Click "New" -> "Web Service"
4. Connect your GitHub repo.
5. Set the start command to `python server.py`.
6. Render will provide a public URL automatically.

The app keeps the selected gift in memory and exposes:

- POST /save-gift
- GET /gift-result

This is enough for a simple public demo.
