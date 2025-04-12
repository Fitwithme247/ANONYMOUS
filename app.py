from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask_mail import Mail, Message
import json
import os
import requests
from dotenv import load_dotenv

# Create the Flask app
app = Flask(__name__)
load_dotenv()
# Initialize Flask-Mail


BREVO_API_URL = 'https://api.brevo.com/v3/'
API_KEY = os.getenv('BREVO')
HEADERS = {
    'api-key': API_KEY,
    'Content-Type': 'application/json'
}


# Initialize Flask-Mail
mail = Mail(app)

# Home route - Show the review form
@app.route('/')
def index():
    return render_template('review_form.html')

# Route to handle form submission and send email
@app.route('/submit', methods=['POST'])
def submit_review():
    if request.method == 'POST':
        # Get data from the form
        customer_name = request.form['name']
        review_text = request.form['review']

        try:
            email_data = {
                    "sender": {"email": "okikidanielayo@gmail.com", "name": "Danilo"},
                    "to": [{"email": "clairclancy@gmail.com", "name": "clair"}],
                    "subject": customer_name,
                    "htmlContent": review_text
                }
            response = requests.post(f'{BREVO_API_URL}smtp/email', headers=HEADERS, data=json.dumps(email_data))
            print(response.text)

            if response.status_code == 201:
                return jsonify({"message": "Email sent successfully!", "status": response.status_code, "data": response.json()}), 200
            else:
                return jsonify({"message": "Failed to send email", "status": response.status_code, "error": response.
                son()}), response.status_code
        except Exception as e:
            return f"Error sending email: {e}"



        


# Thank you page after submission
@app.route('/thank_you')
def thank_you():
    return "Thank you for your review! It has been sent successfully."

if __name__ == '__main__':
    app.run(debug=True)