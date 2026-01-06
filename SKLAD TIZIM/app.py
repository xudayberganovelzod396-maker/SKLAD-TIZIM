from sqlalchemy import or_
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sklad.db'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # 7 kun sessiya
app.config['SESSION_COOKIE_SECURE'] = False  # True bo‘lsa, faqat HTTPSda ishlaydi
app.config['SESSION_COOKIE_HTTPONLY'] = True
db = SQLAlchemy(app)

# ====================== MODELS ======================
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default='viewer')  # (legacy, not used)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Batch(db.Model):
    __tablename__ = 'batches'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(200), nullable=False)
    batch_code = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)
    quantity_sht = db.Column(db.Integer, nullable=True)
    quantity_kg = db.Column(db.Float, nullable=True)
    comment = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='ACTIVE')  # 'ACTIVE' or 'REMOVED'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    removed_at = db.Column(db.DateTime)
    removed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='batches_removed')

# ====================== DECORATORS ======================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ====================== QATORLAR MATRITSA STATUS API ======================
@app.route('/api/rows_matrix_status')
@login_required
def rows_matrix_status():
    sectors = ['A', 'B', 'C']
    rows = 9
    cells = 4
    matrix = {}
    for sector in sectors:
        matrix[sector] = []
        for row in range(1, rows+1):
            row_cells = []
            for cell in range(1, cells+1):
                loc = f"{sector}-{row}-{cell}"
                batch = Batch.query.filter_by(location=loc).filter(
                    ((Batch.quantity_sht != None) & (Batch.quantity_sht > 0)) |
                    ((Batch.quantity_kg != None) & (Batch.quantity_kg > 0))
                ).first()
                row_cells.append('busy' if batch else 'free')
            matrix[sector].append(row_cells)
    return jsonify(matrix)
from sqlalchemy import or_
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from datetime import datetime
from functools import wraps


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sklad.db'
# Sessiya muddati va cookie sozlamalari
from datetime import timedelta
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # 7 kun sessiya
app.config['SESSION_COOKIE_SECURE'] = False  # True bo‘lsa, faqat HTTPSda ishlaydi
app.config['SESSION_COOKIE_HTTPONLY'] = True
db = SQLAlchemy(app)

# ====================== MODELS ======================
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default='viewer')  # (legacy, not used)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Batch(db.Model):
    __tablename__ = 'batches'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(200), nullable=False)
    batch_code = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)
    quantity_sht = db.Column(db.Integer, nullable=True)
    quantity_kg = db.Column(db.Float, nullable=True)
    comment = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='ACTIVE')  # 'ACTIVE' or 'REMOVED'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    removed_at = db.Column(db.DateTime)
    removed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='batches_removed')

# ====================== DECORATORS ======================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function



from sqlalchemy import or_

    # ...existing code...

# ====================== BATCH SEARCH API ======================
@app.route('/api/batches/search', methods=['GET'])
@login_required
def search_batches():
    query = request.args.get('q', '').strip()
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 7))
    if not query:
        return jsonify({'results': [], 'total': 0})
    q = f"%{query.lower()}%"
    batches_query = Batch.query.filter(
        or_(
            Batch.product_name.ilike(q),
            Batch.batch_code.ilike(q),
            Batch.location.ilike(q)
        )
    ).order_by(Batch.created_at.desc())
    total = batches_query.count()
    batches = batches_query.offset((page-1)*page_size).limit(page_size).all()
    results = []
    for b in batches:
        results.append({
            'id': b.id,
            'product_name': b.product_name,
            'batch_code': b.batch_code,
            'quantity': b.quantity,
            'quantity_sht': b.quantity_sht,
            'quantity_kg': b.quantity_kg,
            'comment': b.comment,
            'location': b.location,
            'status': b.status,
            'created_at': b.created_at.strftime('%Y-%m-%d %H:%M'),
            'removed_at': b.removed_at.strftime('%Y-%m-%d %H:%M') if b.removed_at else None,
            'removed_by': b.removed_by
        })
    return jsonify({'results': results, 'total': total})
# ====================== BATCH OPERATIONS ======================

# Qatorlar holati (demo, realda DBdan olinadi)
@app.route('/api/rows_status', methods=['GET', 'POST'])
@login_required
def rows_status():
    # Demo uchun, realda DBdan olinadi yoki sessiondan
    if request.method == 'GET':
        rows = [
            {'id': 1, 'status': 'free'},
            {'id': 2, 'status': 'busy'},
            {'id': 3, 'status': 'free'},
            {'id': 4, 'status': 'busy'},
            {'id': 5, 'status': 'free'},
            {'id': 6, 'status': 'free'},
            {'id': 7, 'status': 'free'},
            {'id': 8, 'status': 'free'},
            {'id': 9, 'status': 'free'}
        ]
        return jsonify(rows)
    elif request.method == 'POST':
        data = request.get_json()
        # Demo: statusni o'zgartirishni qaytaradi
        return jsonify({'success': True, 'row_id': data.get('id'), 'new_status': data.get('status')})

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/api/batches', methods=['GET'])
@login_required
def get_batches():
    """Get all batches (all statuses, but 0/0 partiyalar ko'rinmaydi)"""
    batches = Batch.query.order_by(Batch.created_at.desc()).all()
    filtered = [
        b for b in batches
        if not ((b.quantity_sht == 0 or b.quantity_sht is None) and (b.quantity_kg == 0 or b.quantity_kg is None))
    ]
    return jsonify([
        {
            'id': b.id,
            'product_name': b.product_name,
            'batch_code': b.batch_code,
            'quantity': b.quantity,
            'quantity_sht': b.quantity_sht,
            'quantity_kg': b.quantity_kg,
            'comment': b.comment,
            'location': b.location,
            'status': b.status,
            'created_at': b.created_at.strftime('%Y-%m-%d %H:%M'),
            'removed_at': b.removed_at.strftime('%Y-%m-%d %H:%M') if b.removed_at else None,
            'removed_by': b.removed_by
        }
        for b in filtered
    ])

@app.route('/api/batches', methods=['POST'])
@login_required
def create_batch():
    """Add new batch (admin only, unique batch_code+location+ACTIVE)"""
    data = request.get_json()
    # quantity maydoni frontenddan kelmasa, uni avtomatik hisoblash
    quantity = data.get('quantity')
    if quantity is None:
        # quantity_sht yoki quantity_kg dan biri bo'yicha hisoblash
        quantity = data.get('quantity_sht') or data.get('quantity_kg') or 0
    batch = Batch(
        product_name=data.get('product_name'),
        batch_code=data.get('batch_code'),
        quantity=quantity,
        quantity_sht=data.get('quantity_sht'),
        quantity_kg=data.get('quantity_kg'),
        comment=data.get('comment'),
        location=data.get('location'),
        status='ACTIVE'
    )
    db.session.add(batch)
    db.session.commit()
    return jsonify({'success': True, 'batch_id': batch.id}), 201

@app.route('/api/batches/<int:batch_id>/remove', methods=['PUT'])
@login_required
def remove_batch(batch_id):
    """Remove batch by sliding (admin only)"""
    batch = Batch.query.get(batch_id)
    if not batch:
        return jsonify({'error': 'Partiya topilmadi'}), 404

    data = request.get_json(silent=True) or {}
    qty_sht = data.get('quantity_sht', None)
    qty_kg = data.get('quantity_kg', None)
    # Agar ikkala qiymat ham yo'q bo'lsa, xato
    if qty_sht is None and qty_kg is None:
        return jsonify({'error': 'Miqdor kiritilmadi'}), 400
    # Sht uchun tekshiruv va kamaytirish
    if qty_sht is not None:
        try:
            qty_sht = int(qty_sht)
        except Exception:
            return jsonify({'error': 'Noto‘g‘ri dona miqdor'}), 400
        if qty_sht < 0 or (batch.quantity_sht is not None and qty_sht > batch.quantity_sht):
            return jsonify({'error': f'Dona miqdor 0 dan {batch.quantity_sht} gacha bo‘lishi kerak'}), 400
    # Kg uchun tekshiruv va kamaytirish
    if qty_kg is not None:
        try:
            qty_kg = float(qty_kg)
        except Exception:
            return jsonify({'error': 'Noto‘g‘ri kg miqdor'}), 400
        if qty_kg < 0 or (batch.quantity_kg is not None and qty_kg > batch.quantity_kg):
            return jsonify({'error': f'Kg miqdor 0 dan {batch.quantity_kg} gacha bo‘lishi kerak'}), 400
    # Hammasini chiqarishmi yoki qismanmi?
    all_sht = (batch.quantity_sht is not None and qty_sht == batch.quantity_sht) if qty_sht is not None else True
    all_kg = (batch.quantity_kg is not None and qty_kg == batch.quantity_kg) if qty_kg is not None else True
    if all_sht and all_kg:
        batch.status = 'REMOVED'
        batch.removed_at = datetime.utcnow()
        batch.removed_by = session['user_id']
        batch.quantity_sht = 0
        batch.quantity_kg = 0
    else:
        if qty_sht is not None and batch.quantity_sht is not None:
            batch.quantity_sht -= qty_sht
        if qty_kg is not None and batch.quantity_kg is not None:
            batch.quantity_kg -= qty_kg
    db.session.commit()
    return jsonify({'success': True})

# ====================== SEARCH ======================
@app.route('/api/search', methods=['GET'])
@login_required
def search():
    """Search batches by code, product name, or location"""
    query = request.args.get('q', '').lower()
    
    if not query:
        return jsonify([])
    
    results = Batch.query.filter(
        Batch.status == 'ACTIVE',
        db.or_(
            Batch.batch_code.ilike(f'%{query}%'),
            Batch.product_name.ilike(f'%{query}%'),
            Batch.location.ilike(f'%{query}%')
        )
    ).all()
    
    return jsonify([{
        'id': b.id,
        'product_name': b.product_name,
        'batch_code': b.batch_code,
        'quantity': b.quantity,
        'quantity_sht': b.quantity_sht,
        'quantity_kg': b.quantity_kg,
        'location': b.location,
        'created_at': b.created_at.strftime('%Y-%m-%d %H:%M')
    } for b in results])

@app.route('/api/user', methods=['GET'])
@login_required
def get_user():
    """Get current user info"""
    user = User.query.get(session['user_id'])
    return jsonify({
        'id': user.id,
        'username': user.username,
        'created_at': user.created_at.strftime('%Y-%m-%d %H:%M')
    })

@app.route('/api/user/password', methods=['POST'])
@login_required
def change_password():
    """Change user password"""
    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    user = User.query.get(session['user_id'])
    
    # Verify current password
    if not check_password_hash(user.password, current_password):
        return jsonify({'error': 'Joriy parol noto\'g\'ri'}), 401
    
    # Validate new password
    if len(new_password) < 5:
        return jsonify({'error': 'Parol kamida 5 ta belgi bo\'lishi kerak'}), 400
    
    # Update password
    user.password = generate_password_hash(new_password)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Parol muvaffaqiyatli o\'zgartirildi!'})

@app.route('/api/user/activity', methods=['GET'])
@login_required
def get_user_activity():
    """Get user activity stats"""
    user_id = session['user_id']
    total_batches = Batch.query.filter_by(status='ACTIVE').count()
    removed_batches = Batch.query.filter_by(status='REMOVED', removed_by=user_id).count()
    
    return jsonify({
        'total_batches': total_batches,
        'removed_batches': removed_batches,
        'last_active': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    })

# ====================== ERROR HANDLERS ======================
from flask import flash

# ====================== AUTH ======================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session.permanent = True
            return jsonify({'success': True, 'message': 'Kirish muvaffaqiyatli!'}), 200
        else:
            return jsonify({'error': 'Login yoki parol noto‘g‘ri'}), 401
    # GET so'rovi uchun login sahifasini ko'rsatish
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Server error'}), 500

# ====================== INIT DB ======================
def init_db():
    with app.app_context():
        db.create_all()
        # Create default users if not exist
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                password=generate_password_hash('admin123')
            )
            db.session.add(admin)
        if not User.query.filter_by(username='user').first():
            user = User(
                username='user',
                password=generate_password_hash('user123')
            )
            db.session.add(user)
        
        db.session.commit()




# ====================== 404 ERROR HANDLER ======================
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='127.0.0.1', port=5000)
