from extensions import db
from sqlalchemy.orm import relationship

class TicketSoporte(db.Model):
    __tablename__ = 'tickets_soporte'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    motivo = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    prioridad = db.Column(db.String(50), nullable=False)

    # Relación con respuestas
    respuestas = relationship('RespuestaSoporte', backref='ticket', lazy=True)

    def __repr__(self):
        return f'<TicketSoporte {self.id} - Estado: {self.estado}>'

class RespuestaSoporte(db.Model):
    __tablename__ = 'respuestas_soporte'

    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets_soporte.id'), nullable=False)
    agente = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    mensaje = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<RespuestaSoporte {self.id} - Ticket {self.ticket_id}>'