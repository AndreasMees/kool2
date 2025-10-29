from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hinnangud.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a model for Hinnang
class Hinnang(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aine = db.Column(db.String(100), nullable=False)
    nimi = db.Column(db.String(100), nullable=False)
    hinne = db.Column(db.Integer, nullable=False)
    kommentaar = db.Column(db.Text, nullable=True)

# Create the database and tables if they don't exist
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        aine = request.form.get('aine')
        nimi = request.form.get('nimi')
        hinne = request.form.get('hinne')
        kommentaar = request.form.get('kommentaar')

        if aine and nimi and hinne:
            uus_hinnang = Hinnang(
                aine=aine,
                nimi=nimi,
                hinne=int(hinne),
                kommentaar=kommentaar or ''
            )
            db.session.add(uus_hinnang)
            db.session.commit()
        return redirect(url_for('index'))

    hinnangud = Hinnang.query.all()
    return render_template('index.html', hinnangud=hinnangud)

@app.route('/kustuta/<int:hinnang_id>', methods=['POST'])
def kustuta_hinnang(hinnang_id):
    hinnang = Hinnang.query.get_or_404(hinnang_id)
    db.session.delete(hinnang)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
