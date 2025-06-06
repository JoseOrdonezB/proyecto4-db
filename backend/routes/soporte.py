from flask import Blueprint, request, jsonify
from extensions import db
from models.soporte import TicketSoporte, RespuestaSoporte

soporte_bp = Blueprint('soporte', __name__, url_prefix='/soporte')

# Listar todos los tickets de soporte
@soporte_bp.route('/tickets', methods=['GET'])
def listar_tickets():
    tickets = TicketSoporte.query.all()
    return jsonify([{
        'id': t.id,
        'usuario_id': t.usuario_id,
        'motivo': t.motivo,
        'estado': t.estado,
        'prioridad': t.prioridad
    } for t in tickets])

# Ver un ticket y sus respuestas
@soporte_bp.route('/tickets/<int:id>', methods=['GET'])
def obtener_ticket(id):
    ticket = TicketSoporte.query.get_or_404(id)
    respuestas = [{
        'id': r.id,
        'agente': r.agente,
        'fecha': r.fecha.isoformat(),
        'mensaje': r.mensaje
    } for r in ticket.respuestas]

    return jsonify({
        'id': ticket.id,
        'usuario_id': ticket.usuario_id,
        'motivo': ticket.motivo,
        'estado': ticket.estado,
        'prioridad': ticket.prioridad,
        'respuestas': respuestas
    })

# Crear un nuevo ticket
@soporte_bp.route('/tickets', methods=['POST'])
def crear_ticket():
    data = request.json
    ticket = TicketSoporte(
        usuario_id=data['usuario_id'],
        motivo=data['motivo'],
        estado=data['estado'],
        prioridad=data['prioridad']
    )
    db.session.add(ticket)
    db.session.commit()
    return jsonify({'mensaje': 'Ticket creado', 'id': ticket.id}), 201

# Agregar una respuesta a un ticket
@soporte_bp.route('/tickets/<int:ticket_id>/responder', methods=['POST'])
def responder_ticket(ticket_id):
    data = request.json
    respuesta = RespuestaSoporte(
        ticket_id=ticket_id,
        agente=data['agente'],
        fecha=data['fecha'],  # formato "YYYY-MM-DD"
        mensaje=data['mensaje']
    )
    db.session.add(respuesta)
    db.session.commit()
    return jsonify({'mensaje': 'Respuesta registrada', 'id': respuesta.id}), 201