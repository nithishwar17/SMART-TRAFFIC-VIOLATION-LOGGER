from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_bcrypt import Bcrypt
import qrcode, os

# ------------------------
# Flask App Configuration
# ------------------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey'  # Required for Flask-Login sessions

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# ------------------------
# Database Models
# ------------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


class Violation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_number = db.Column(db.String(20), nullable=False)
    violation_type = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    fine_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(10), default='Unpaid')
    qr_code_path = db.Column(db.String(200))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ------------------------
# QR Code Generator
# ------------------------
def generate_qr(violation_id):
    """Generate and save a QR code for the violation."""
    # Replace this with your PC’s local IP address for phone testing
    local_ip = "10.14.249.63"
    url = f"http://{local_ip}:5000/status/{violation_id}"

    qr = qrcode.make(url)
    qr_folder = os.path.join("static", "qr_codes")
    os.makedirs(qr_folder, exist_ok=True)

    filename = f"{violation_id}.png"
    file_path = os.path.join(qr_folder, filename)
    qr.save(file_path)

    return f"qr_codes/{filename}"

# ------------------------
# Authentication Routes
# ------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            return "Invalid credentials"
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ------------------------
# Main Routes
# ------------------------

# Redirect to login when app starts
@app.route('/')
def index():
    return redirect(url_for('login'))

# Officer: Add violation (protected)
@app.route('/add', methods=['POST'])
@login_required
def add_violation():
    vehicle_number = request.form['vehicle_number']
    violation_type = request.form['violation_type']
    location = request.form['location']
    date = request.form['date']
    fine_amount = float(request.form['fine_amount'])

    new_violation = Violation(
        vehicle_number=vehicle_number,
        violation_type=violation_type,
        location=location,
        date=datetime.strptime(date, "%Y-%m-%d"),
        fine_amount=fine_amount
    )

    db.session.add(new_violation)
    db.session.commit()

    qr_path = generate_qr(new_violation.id)
    new_violation.qr_code_path = qr_path
    db.session.commit()

    return redirect(url_for('view_violations'))

# Officer dashboard (protected)
@app.route('/dashboard')
@login_required
def home():
    return render_template('add_violation.html')

# Public: view all or search by vehicle
@app.route('/view')
def view_violations():
    search = request.args.get('search')
    if search:
        violations = Violation.query.filter(Violation.vehicle_number.contains(search)).all()
    else:
        violations = Violation.query.all()
    return render_template('view_violations.html', violations=violations)

# Officer: toggle payment status (protected)
@app.route('/update/<int:id>')
@login_required
def update_status(id):
    violation = Violation.query.get_or_404(id)
    violation.status = 'Paid' if violation.status == 'Unpaid' else 'Unpaid'
    db.session.commit()
    return redirect(url_for('view_violations'))

# Public: QR scan → status page
@app.route('/status/<int:id>')
def status_page(id):
    violation = Violation.query.get_or_404(id)
    return render_template('status.html', v=violation)

# ------------------------
# Run App
# ------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("✅ Flask app is running at http://127.0.0.1:5000/")
    app.run(host='0.0.0.0', port=5000, debug=True)
