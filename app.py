from flask import Flask, render_template, request
import pickle
import os

app = Flask(__name__)

# Load model — resolve path relative to this file
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')
model = pickle.load(open(MODEL_PATH, 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        demand = float(request.form['demand'])
        competitor = float(request.form['competitor'])
        season = float(request.form['season'])

        # Validate ranges
        if demand not in [1, 2, 3]:
            return render_template('index.html', error="Demand must be 1 (Low), 2 (Medium), or 3 (High).")
        if competitor < 0:
            return render_template('index.html', error="Competitor price cannot be negative.")
        if season not in [0, 1]:
            return render_template('index.html', error="Please select a valid season.")

        prediction = model.predict([[demand, competitor, season]])
        result = round(float(prediction[0]), 2)

        return render_template('index.html', result=result)

    except ValueError:
        return render_template('index.html', error="Please enter valid numeric values in all fields.")
    except Exception as e:
        return render_template('index.html', error=f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)
