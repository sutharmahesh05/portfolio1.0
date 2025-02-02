from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables
with app.app_context():
    db.create_all()

# Sample project data
projects = [
    {
        'title': 'E-commerce Platform',
        'description': 'A full-stack e-commerce solution built with Django and React.',
        'image': 'https://via.placeholder.com/300x200.png?text=E-commerce+Platform',
        'url': 'https://github.com/yourusername/ecommerce-platform'
    },
    {
        'title': 'Weather App',
        'description': 'A responsive weather application using OpenWeatherMap API and Vue.js.',
        'image': 'https://via.placeholder.com/300x200.png?text=Weather+App',
        'url': 'https://github.com/yourusername/weather-app'
    },
    {
        'title': 'Task Manager',
        'description': 'A Flask-based task management system with user authentication.',
        'image': 'https://via.placeholder.com/300x200.png?text=Task+Manager',
        'url': 'https://github.com/yourusername/task-manager'
    },
    {
        'title': 'Portfolio Website',
        'description': 'This very portfolio, built with Flask and Tailwind CSS.',
        'image': 'https://via.placeholder.com/300x200.png?text=Portfolio+Website',
        'url': 'https://github.com/yourusername/portfolio-website'
    }
]

@app.route('/')
def index():
    return render_template('index.html', projects=projects)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        new_contact = Contact(name=name, email=email, message=message)
        db.session.add(new_contact)
        db.session.commit()
        return redirect(url_for('thank_you'))
    return render_template('contact.html')

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/admin/contacts')
def admin_contacts():
    contacts = Contact.query.order_by(Contact.date.desc()).all()
    return render_template('admin_contacts.html', contacts=contacts)

if __name__ == '__main__':
    app.run(debug=True)

