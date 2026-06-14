Deploy a Telegram webhook bot to Render

1. Create a GitHub repo and push the `telegram-webhook-bot` folder.
2. On Render: New -> Web Service -> connect the repo.
   - Runtime: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
3. Add environment variables in Render:
   - `BOT_TOKEN` = your Telegram bot token
   - Optional: `ODYSSEUS_API_URL` = http://your-odysseus-host
   - Optional: `ODYSSEUS_API_TOKEN` = your ody_... token
4. Deploy and note the service URL (https://<your-service>.onrender.com)
5. Set Telegram webhook:
   ```bash
   curl -F "url=https://<your-service>.onrender.com/webhook" https://api.telegram.org/bot<NEW_TOKEN>/setWebhook
   ```

Security: keep tokens secret and use HTTPS. If you want me to prepare a GitHub repo or create the Render service instructions exactly, tell me which GitHub repo name you want.