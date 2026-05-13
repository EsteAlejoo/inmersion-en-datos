from flask import Blueprint, render_template, request, jsonify
from models import db, Agricola, Cuartel, Producto, TipoAplicacion

maestros_bp = Blueprint('maestros', __name__)

MOJAMIENTOS = {
    'MOSQ': 4500, 'CHANCH': 5000, 'LAV': 9000,
    'FERT': 2000, 'HERB': 3200, 'INSEC': 4000,
}


@maestros_bp.route('/cuarteles')
def cuarteles():
    agricola_id = request.args.get('agricola_id')
    q = Cuartel.query
    if agricola_id:
        q = q.filter_by(agricola_id=agricola_id)
    agricolas = Agricola.query.filter_by(activa=True).all()
    return render_template('maestros/cuarteles.html',
                           cuarteles=q.order_by(Cuartel.agricola_id, Cuartel.nombre).all(),
                           agricolas=agricolas,
                           filtro_agricola=agricola_id)


@maestros_bp.route('/productos')
def productos():
    agricola_id = request.args.get('agricola_id')
    q = Producto.query.filter_by(activo=True)
    if agricola_id:
        q = q.filter_by(agricola_id=agricola_id)
    agricolas = Agricola.query.filter_by(activa=True).all()
    return render_template('maestros/productos.html',
                           productos=q.order_by(Producto.orden_mezcla, Producto.nombre_comercial).all(),
                           agricolas=agricolas,
                           filtro_agricola=agricola_id)


@maestros_bp.route('/api/cuarteles/<int:agricola_id>')
def api_cuarteles(agricola_id):
    cuarteles = Cuartel.query.filter_by(agricola_id=agricola_id, activo=True).order_by(Cuartel.nombre).all()
    return jsonify([{
        'id': c.id,
        'nombre': c.nombre,
        'especie': c.especie,
        'variedad': c.variedad or '',
        'ha_total': float(c.ha_total),
        'es_ensayo': c.es_ensayo,
    } for c in cuarteles])


@maestros_bp.route('/api/productos/<int:agricola_id>')
def api_productos(agricola_id):
    productos = (Producto.query
                 .filter_by(agricola_id=agricola_id, activo=True)
                 .order_by(Producto.orden_mezcla, Producto.nombre_comercial)
                 .all())
    return jsonify([{
        'id': p.id,
        'nombre': p.nombre_comercial,
        'ia': p.ingrediente_activo,
        'dosis_100L': float(p.dosis_100L),
        'unidad': p.unidad_dosis,
        'objetivo': p.objetivo or '',
    } for p in productos])


@maestros_bp.route('/api/mojamiento/<string:tipo_codigo>')
def api_mojamiento(tipo_codigo):
    return jsonify({'mojamiento': MOJAMIENTOS.get(tipo_codigo.upper(), 4000)})
