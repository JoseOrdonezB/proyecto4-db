from flask import Blueprint, request, jsonify
from extensions import db
from models.pago import Pago, MetodoPago

pagos_bp = Blueprint('pagos', __name__, url_prefix='/pagos')

# Listar todos los pagos
@pagos_bp.route('/', methods=['GET'])
def listar_pagos():
    pagos = Pago.query.all()
    return jsonify([{
        'id': p.id,
        'pedido_id': p.pedido_id,
        'metodo_pago_id': p.metodo_pago_id,
        'estado': p.estado,
        'fecha': p.fecha.isoformat()
    } for p in pagos])

# Obtener un pago por ID
@pagos_bp.route('/<int:id>', methods=['GET'])
def obtener_pago(id):
    pago = Pago.query.get_or_404(id)
    return jsonify({
        'id': pago.id,
        'pedido_id': pago.pedido_id,
        'metodo_pago_id': pago.metodo_pago_id,
        'estado': pago.estado,
        'fecha': pago.fecha.isoformat()
    })

# Crear un nuevo pago
@pagos_bp.route('/', methods=['POST'])
def crear_pago():
    data = request.json
    nuevo_pago = Pago(
        pedido_id=data['pedido_id'],
        metodo_pago_id=data['metodo_pago_id'],
        estado=data['estado'],
        fecha=data['fecha']  # Debe venir en formato 'YYYY-MM-DD'
    )
    db.session.add(nuevo_pago)
    db.session.commit()
    return jsonify({'mensaje': 'Pago registrado', 'id': nuevo_pago.id}), 201

# Listar métodos de pago
@pagos_bp.route('/metodos', methods=['GET'])
def listar_metodos_pago():
    metodos = MetodoPago.query.all()
    return jsonify([{
        'id': m.id,
        'tipo': m.tipo
    } for m in metodos])