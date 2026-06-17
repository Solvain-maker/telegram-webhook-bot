web: uvicorn app:app --host 0.0.0.0 --port $PORT
# integrations script lives in the main repo folder (odysseus-dev/odysseus-dev)
# reference it via relative path so Railway can run the worker correctly
worker: python ../odysseus-dev/integrations/telegram_bot.py
