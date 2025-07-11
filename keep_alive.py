from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def keep_alive():
    def run():
        app.run(host='0.0.0.0', port=8080)
    Thread(target=run).start()
    print("✅ Server is running on port 8080")
    
