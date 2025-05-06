from flask import Flask, render_template
from cleanerCont import get_cleaners  # Import the controller function

app = Flask(__name__)

@app.route("/")
def home():
    cleaners = get_cleaners()  # Call the controller to fetch data
    return render_template("cleanerPg.html", cleaners=cleaners)

if __name__ == "__main__":
    app.run(debug=True)