from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models import Head, Category, Subcategory, Transaction, User

transaction_bp = Blueprint('transaction_bp', __name__)

# ---------- HEAD ROUTES ----------
@transaction_bp.route('/heads', methods=['GET', 'POST'])
@jwt_required()
def heads():
    user_uuid = get_jwt_identity()

    if request.method == 'GET':
        heads = Head.query.filter_by(user_uuid=user_uuid).order_by(Head.name).all()
        return jsonify([{'uuid': h.id, 'name': h.name} for h in heads])

    data = request.json
    name = data.get('name')

    if Head.query.filter_by(name=name, user_uuid=user_uuid).first():
        return jsonify({'error': 'Head already exists'}), 400

    head = Head(name=name, user_uuid=user_uuid)
    db.session.add(head)
    db.session.commit()
    return jsonify({'message': 'Head created', 'uuid': head.uuid}), 201

# ---------- CATEGORY ROUTES ----------
@transaction_bp.route('/heads/<int:head_uuid>/categories', methods=['GET', 'POST'])
@jwt_required()
def categories(head_uuid):
    user_uuid = get_jwt_identity()
    head = Head.query.filter_by(uudid=head_uuid, user_uuid=user_uuid).first()
    if not head:
        return jsonify({'error': 'Head not found'}), 404

    if request.method == 'GET':
        categories = Category.query.filter_by(head_uuid=head_uuid, user_uuid=user_uuid).all()
        return jsonify([{'id': c.id, 'name': c.name} for c in categories])

    data = request.json
    name = data.get('name')

    if Category.query.filter_by(head_uuid=head_uuid, name=name, user_uuid=user_uuid).first():
        return jsonify({'error': 'Category already exists'}), 400

    category = Category(name=name, head_uuid=head_uuid, user_uuid=user_uuid)
    db.session.add(category)
    db.session.commit()
    return jsonify({'message': 'Category created', 'id': category.id}), 201

# ---------- SUBCATEGORY ROUTES ----------
@transaction_bp.route('/categories/<int:category_uuid>/subcategories', methods=['GET', 'POST'])
@jwt_required()
def subcategories(category_uuid):
    user_uuid = get_jwt_identity()
    category = Category.query.filter_by(id=category_uuid, user_uuid=user_uuid).first()
    if not category:
        return jsonify({'error': 'Category not found'}), 404

    if request.method == 'GET':
        subcategories = Subcategory.query.filter_by(category_uuid=category_uuid, user_uuid=user_uuid).all()
        return jsonify([{'id': s.id, 'name': s.name} for s in subcategories])

    data = request.json
    name = data.get('name')

    if Subcategory.query.filter_by(category_uuid=category_uuid, name=name, user_uuid=user_uuid).first():
        return jsonify({'error': 'Subcategory already exists'}), 400

    subcategory = Subcategory(name=name, category_uuid=category_uuid, user_uuid=user_uuid)
    db.session.add(subcategory)
    db.session.commit()
    return jsonify({'message': 'Subcategory created', 'id': subcategory.id}), 201

# ---------- TRANSACTION ROUTES ----------
@transaction_bp.route('/transactions', methods=['POST'])
@jwt_required()
def create_transaction():
    user_uuid = get_jwt_identity()
    data = request.json
    type = data.get('type')
    amount = data.get('amount')

    user = User.query.get(user_uuid)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if type not in ['income', 'expense']:
        return jsonify({'error': 'Invalid transaction type'}), 400

    if type == 'expense':
        required = ['head_uuid', 'category_uuid', 'subcategory_uuid', 'title']
        missing = [field for field in required if not data.get(field)]
        if missing:
            return jsonify({'error': f'Missing fields: {", ".join(missing)}'}), 400

        # Explicitly verify ownership
        head = Head.query.filter_by(id=data['head_uuid'], user_uuid=user_uuid).first()
        category = Category.query.filter_by(id=data['category_uuid'], user_uuid=user_uuid).first()
        subcategory = Subcategory.query.filter_by(id=data['subcategory_uuid'], user_uuid=user_uuid).first()

        if not all([head, category, subcategory]):
            return jsonify({'error': 'Invalid head/category/subcategory provided'}), 400

    elif type == 'income':
        if not data.get('source'):
            return jsonify({'error': 'Source required for income'}), 400

    transaction = Transaction(
        user_uuid=user_uuid,
        type=type,
        amount=amount,
        description=data.get('description'),
        head_uuid=data.get('head_uuid') if type == 'expense' else None,
        category_uuid=data.get('category_uuid') if type == 'expense' else None,
        subcategory_uuid=data.get('subcategory_uuid') if type == 'expense' else None,
        title=data.get('title') if type == 'expense' else None,
        source=data.get('source') if type == 'income' else None
    )
    db.session.add(transaction)
    db.session.commit()

    return jsonify({'message': 'Transaction created', 'id': transaction.id}), 201

@transaction_bp.route('/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    user_uuid = get_jwt_identity()
    
    transactions = Transaction.query.filter_by(user_uuid=user_uuid).order_by(Transaction.timestamp.desc()).all()

    result = []
    for txn in transactions:
        txn_data = {
            'id': txn.id,
            'type': txn.type,
            'amount': txn.amount,
            'description': txn.description,
            'timestamp': txn.timestamp.isoformat(),
        }
        if txn.type == 'expense':
            txn_data.update({
                'head': txn.head.name if txn.head else None,
                'category': txn.category.name if txn.category else None,
                'subcategory': txn.subcategory.name if txn.subcategory else None,
                'title': txn.title,
            })
        elif txn.type == 'income':
            txn_data.update({
                'source': txn.source
            })

        result.append(txn_data)

    return jsonify(result), 200

@transaction_bp.route('/transactions/<int:txn_id>', methods=['PUT'])
@jwt_required()
def update_transaction(txn_id):
    user_uuid = get_jwt_identity()
    transaction = Transaction.query.filter_by(id=txn_id, user_uuid=user_uuid).first()

    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404

    data = request.json

    # Update basic fields
    transaction.amount = data.get('amount', transaction.amount)
    transaction.description = data.get('description', transaction.description)
    transaction.timestamp = data.get('timestamp', transaction.timestamp)

    if transaction.type == 'income':
        transaction.source = data.get('source', transaction.source)

    elif transaction.type == 'expense':
        transaction.title = data.get('title', transaction.title)
        
        # Update related fields if provided
        head_uuid = data.get('head_uuid')
        category_uuid = data.get('category_uuid')
        subcategory_uuid = data.get('subcategory_uuid')

        # Validate ownership and existence
        if head_uuid:
            head = Head.query.filter_by(id=head_uuid, user_uuid=user_uuid).first()
            if not head:
                return jsonify({'error': 'Invalid head provided'}), 400
            transaction.head_uuid = head_uuid

        if category_uuid:
            category = Category.query.filter_by(id=category_uuid, user_uuid=user_uuid).first()
            if not category:
                return jsonify({'error': 'Invalid category provided'}), 400
            transaction.category_uuid = category_uuid

        if subcategory_uuid:
            subcategory = Subcategory.query.filter_by(id=subcategory_uuid, user_uuid=user_uuid).first()
            if not subcategory:
                return jsonify({'error': 'Invalid subcategory provided'}), 400
            transaction.subcategory_uuid = subcategory_uuid

    db.session.commit()

    return jsonify({"message": "Transaction updated"}), 200


@transaction_bp.route('/transactions/<int:txn_id>', methods=['DELETE'])
@jwt_required()
def delete_transaction(txn_id):
    user_uuid = get_jwt_identity()
    transaction = Transaction.query.filter_by(id=txn_id, user_uuid=user_uuid).first()

    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404

    db.session.delete(transaction)
    db.session.commit()

    return jsonify({"message": "Transaction deleted"}), 200
