from flask import Flask, render_template
from servicesCont import get_services  # Import the controller function
import webbrowser  # Add this import
import threading   # To delay browser opening until server starts

app = Flask(__name__)

def open_browser():
    # Wait 1 second to ensure server starts
    import time
    time.sleep(1)
    webbrowser.open_new("http://127.0.0.1:5000")


@app.route("/")
def home():
    services = get_services()  # Call the controller to fetch data
    return render_template("ServicesPg.html", services=services)

if __name__ == "__main__":
     # Start browser in a new thread
    threading.Thread(target=open_browser).start()
    app.run(debug=True)