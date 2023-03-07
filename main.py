import os
from chat_app import app, db

if __name__ == "__main__":
  app.run(host='0.0.0.0' ,debug=True, port=os.getenv("PORT", default=5000))