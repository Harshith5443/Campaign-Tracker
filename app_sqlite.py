from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import time

# Initialize Flask app and SQLAlchemy
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///campaigns.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY') or 'supersecretkey123'

db = SQLAlchemy(app)
CORS(app, supports_credentials=True)

# -------------------- Database Models --------------------

class User(db.Model):
    """User model for login."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {'id': self.id, 'username': self.username}


class Campaign(db.Model):
    """Campaign model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    client = db.Column(db.String(255), nullable=False)
    startDate = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Active')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'client': self.client,
            'startDate': self.startDate,
            'status': self.status
        }


# -------------------- Initialize Database --------------------

def init_db():
    """Create tables and default user if they don't exist."""
    with app.app_context():
        db.create_all()
        # Check if default user exists
        default_user = User.query.filter_by(username='admin').first()
        if not default_user:
            admin = User(username='admin', password='1234')
            db.session.add(admin)
            db.session.commit()
            print("✓ Default user 'admin' created.")
        print("✓ Database initialized.")


# -------------------- User Management --------------------

@app.route('/api/login', methods=['POST'])
def login():
    """Login endpoint."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        session['username'] = username
        return jsonify({'message': 'Login successful', 'username': username})
    return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/api/logout', methods=['POST'])
def logout():
    """Logout endpoint."""
    session.pop('username', None)
    return jsonify({'message': 'Logged out'})


@app.route('/api/check-login', methods=['GET'])
def check_login():
    """Check if user is logged in."""
    return jsonify({'logged_in': 'username' in session, 'user': session.get('username')})


# -------------------- Campaign Endpoints --------------------

@app.route('/')
def index():
    """Serve frontend HTML."""
    return send_from_directory('.', 'gin.html')


@app.route('/api/campaigns', methods=['GET'])
def get_campaigns():
    """Get all campaigns, with optional filters."""
    status = request.args.get('status', 'All')
    search = request.args.get('search', '').lower()
    
    query = Campaign.query
    
    if status != 'All':
        query = query.filter_by(status=status)
    
    campaigns = query.all()
    
    # Apply search filter on retrieved campaigns
    if search:
        campaigns = [
            c for c in campaigns 
            if search in c.name.lower() or search in c.client.lower()
        ]
    
    return jsonify([c.to_dict() for c in campaigns])


@app.route('/api/campaigns', methods=['POST'])
def add_campaign():
    """Add a new campaign."""
    if 'username' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.get_json()
    if not all(k in data for k in ['name', 'client', 'startDate', 'status']):
        return jsonify({'message': 'All fields required'}), 400

    new_campaign = Campaign(
        name=data['name'],
        client=data['client'],
        startDate=data['startDate'],
        status=data['status']
    )
    db.session.add(new_campaign)
    db.session.commit()
    
    return jsonify(new_campaign.to_dict()), 201


@app.route('/api/campaigns/<int:id>', methods=['PUT'])
def update_campaign(id):
    """Update a campaign."""
    if 'username' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.get_json()
    campaign = Campaign.query.get(id)
    
    if not campaign:
        return jsonify({'message': 'Campaign not found'}), 404
    
    campaign.name = data.get('name', campaign.name)
    campaign.client = data.get('client', campaign.client)
    campaign.startDate = data.get('startDate', campaign.startDate)
    campaign.status = data.get('status', campaign.status)
    
    db.session.commit()
    return jsonify(campaign.to_dict())


@app.route('/api/campaigns/<int:id>', methods=['DELETE'])
def delete_campaign(id):
    """Delete a campaign."""
    if 'username' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    campaign = Campaign.query.get(id)
    if not campaign:
        return jsonify({'message': 'Campaign not found'}), 404
    
    db.session.delete(campaign)
    db.session.commit()
    
    return jsonify({'message': 'Deleted successfully'})


@app.route('/api/summary', methods=['GET'])
def summary():
    """Return dashboard summary."""
    total = Campaign.query.count()
    active = Campaign.query.filter_by(status='Active').count()
    paused = Campaign.query.filter_by(status='Paused').count()
    completed = Campaign.query.filter_by(status='Completed').count()
    
    summary_data = {
        'total': total,
        'active': active,
        'paused': paused,
        'completed': completed
    }
    return jsonify(summary_data)


# -------------------- Main --------------------

if __name__ == '__main__':
    init_db()  # Create tables and default user
    app.run(debug=True, port=5000)
