from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    product = request.form['product']
    rating = request.form['rating']
    comment = request.form['comment']

    feedback = {
        'name': name,
        'product': product,
        'rating': rating,
        'comment': comment
    }

    feedback_file = r'C:\Users\praba\OneDrive\Documents\workspace\NOTHING\IP\feedback.json'

    if os.path.exists(feedback_file):
        with open(feedback_file, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []  # Handle empty or invalid JSON file
    else:
        data = []

    data.append(feedback)

    with open(feedback_file, 'w') as f:
        json.dump(data, f, indent=4)

    return f"Thank you, {name}! Your feedback has been recorded."

if __name__ == '__main__':
    app.run(debug=True)
