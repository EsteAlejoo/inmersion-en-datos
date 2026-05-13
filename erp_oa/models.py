from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Agricola(db.Model):
    __tablename__ = 'agricolas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    productor = db.Column(db.String(100))
    predio = db.Column(db.String(100))
    localidad = db.Column(db.String(100))
    mercados_destino = db.Column(db.Text)  # JSON string
    activa = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    cuarteles = db.relationship('Cuartel', backref='agricola', lazy=True)
    productos = db.relationship('Producto', backref='agricola', lazy=True)


class Cuartel(db.Model):
    __tablename__ = 'cuarteles'
    id = db.Column(db.Integer, primary_key=True)
    agricola_id = db.Column(db.Integer, db.ForeignKey('agricolas.id'), nullable=False)
    nombre = db.Column(db.String(20), nullable=False)
    especie = db.Column(db.String(20), nullable=False)
    variedad = db.Column(db.String(50))
    ha_total = db.Column(db.Numeric(6, 2), nullable=False)
    marco = db.Column(db.String(10))
    entre_hilera = db.Column(db.Numeric(4, 2))
    sobre_hilera = db.Column(db.Numeric(4, 2))
    anno_plantacion = db.Column(db.Integer)
    n_plantas = db.Column(db.Integer)
    es_ensayo = db.Column(db.Boolean, default=False)
    observaciones = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)
    __table_args__ = (db.UniqueConstraint('agricola_id', 'nombre'),)


class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    agricola_id = db.Column(db.Integer, db.ForeignKey('agricolas.id'), nullable=False)
    nombre_comercial = db.Column(db.String(100), nullable=False)
    ingrediente_activo = db.Column(db.String(100), nullable=False)
    concentracion = db.Column(db.String(50))
    formulacion = db.Column(db.String(10))
    dosis_100L = db.Column(db.Numeric(10, 2), nullable=False)
    unidad_dosis = db.Column(db.String(5), nullable=False)  # 'cc' o 'g'
    objetivo = db.Column(db.String(150))
    carencia_limon = db.Column(db.Integer)
    carencia_naranja = db.Column(db.Integer)
    carencia_mandarina = db.Column(db.Integer)
    carencia_asoex = db.Column(db.Integer)
    banda_sag = db.Column(db.String(20))
    registro_sag = db.Column(db.String(20))
    epp = db.Column(db.Text)
    ocasiones_temporada = db.Column(db.Integer)
    incompatibilidades = db.Column(db.Text)
    orden_mezcla = db.Column(db.Integer, default=99)
    observaciones = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)
    __table_args__ = (db.UniqueConstraint('agricola_id', 'nombre_comercial'),)


class TipoAplicacion(db.Model):
    __tablename__ = 'tipos_aplicacion'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    etiqueta = db.Column(db.String(100), nullable=False)
    mojamiento_sugerido = db.Column(db.Integer, nullable=False)
    orden = db.Column(db.Integer, default=0)
    activo = db.Column(db.Boolean, default=True)


class OrdenAplicacion(db.Model):
    __tablename__ = 'ordenes_aplicacion'
    id = db.Column(db.Integer, primary_key=True)
    agricola_id = db.Column(db.Integer, db.ForeignKey('agricolas.id'), nullable=False)
    num_oa = db.Column(db.String(20), unique=True, nullable=False)
    tipo_oa = db.Column(db.String(20), nullable=False)  # 'Proactiva', 'Retroactiva'
    tipo_aplicacion_codigo = db.Column(db.String(20))   # 'MOSQ', 'CHANCH', etc.
    especie = db.Column(db.String(30))
    estado_fenologico = db.Column(db.String(50))
    fecha_emision = db.Column(db.Date, nullable=False)
    fecha_desde = db.Column(db.Date, nullable=False)
    fecha_inicio_aplicacion = db.Column(db.Date, nullable=False)
    mojamiento_Lha = db.Column(db.Integer, nullable=False)
    capacidad_estanque = db.Column(db.Integer, nullable=False)
    ha_totales = db.Column(db.Numeric(8, 2))
    litros_totales = db.Column(db.Numeric(10, 2))
    maquinadas_totales = db.Column(db.Numeric(8, 2))
    tipo_maquina = db.Column(db.String(50))
    agronomo = db.Column(db.String(100))
    mercado_destino = db.Column(db.String(100))
    reingreso_hrs = db.Column(db.Integer, default=24)
    indicaciones = db.Column(db.Text)
    estado = db.Column(db.String(20), default='borrador')  # 'borrador', 'confirmada', 'anulada'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed_at = db.Column(db.DateTime)
    agricola = db.relationship('Agricola', backref='ordenes')
    productos = db.relationship('OAProducto', backref='oa', lazy=True, cascade='all, delete-orphan')
    cuarteles = db.relationship('OACuartel', backref='oa', lazy=True, cascade='all, delete-orphan')


class OAProducto(db.Model):
    __tablename__ = 'oa_productos'
    id = db.Column(db.Integer, primary_key=True)
    oa_id = db.Column(db.Integer, db.ForeignKey('ordenes_aplicacion.id', ondelete='CASCADE'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    dosis_100L = db.Column(db.Numeric(10, 2), nullable=False)
    unidad = db.Column(db.String(5), nullable=False)
    dosis_ha = db.Column(db.Numeric(10, 2))
    dosis_maquinada = db.Column(db.Numeric(10, 2))
    objetivo = db.Column(db.String(150))
    orden = db.Column(db.Integer, default=0)
    producto = db.relationship('Producto', backref='oa_productos')
    __table_args__ = (db.UniqueConstraint('oa_id', 'producto_id'),)


class OACuartel(db.Model):
    __tablename__ = 'oa_cuarteles'
    id = db.Column(db.Integer, primary_key=True)
    oa_id = db.Column(db.Integer, db.ForeignKey('ordenes_aplicacion.id', ondelete='CASCADE'), nullable=False)
    cuartel_id = db.Column(db.Integer, db.ForeignKey('cuarteles.id'), nullable=False)
    ha_efectivas = db.Column(db.Numeric(6, 2), nullable=False)
    fecha_aplicacion = db.Column(db.Date)
    litros = db.Column(db.Numeric(10, 2))
    maquinadas = db.Column(db.Numeric(8, 2))
    cuartel = db.relationship('Cuartel', backref='oa_cuarteles')
    __table_args__ = (db.UniqueConstraint('oa_id', 'cuartel_id'),)
