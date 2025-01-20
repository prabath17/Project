from flask import Flask, render_template, request
import requests

app = Flask(__name__,template_folder="templates")


API_KEY = "036eb568fbe9cc62a08862ab0af4207a"

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    error = None

    if request.method == "POST":
        location = request.form.get("location")
        if location:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
            try:
                response = requests.get(url)
                response.raise_for_status()
                weather_data = response.json()
            except requests.exceptions.RequestException:
                error = "Could not retrieve weather data. Please try again."

    return render_template("index.html", weather_data=weather_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)

