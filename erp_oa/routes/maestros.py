import csv
import os

from flask import Blueprint, render_template, request, jsonify
from models import db, Agricola, Cuartel, Producto, TipoAplicacion

_DATOS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'datos')


def _leer_csv(nombre_archivo):
    ruta = os.path.join(_DATOS_DIR, nombre_archivo)
    if not os.path.exists(ruta):
        return []
    with open(ruta, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

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
    cuarteles = Cuartel.query.filter_by(agricola_id=agricola_id, activo=True).order_by(Cuartel.especie, Cuartel.nombre).all()
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
        'incompat': p.incompatibilidades or '',
        'dosis_100L': float(p.dosis_100L),
        'unidad': p.unidad_dosis,
        'objetivo': p.objetivo or '',
    } for p in productos])


@maestros_bp.route('/api/maquinaria')
def api_maquinaria():
    filas = _leer_csv('maquinaria.csv')
    return jsonify([{
        'nombre': r['nombre'],
        'capacidad_L': int(r['capacidad_L']) if r.get('capacidad_L') else None,
        'tipo': r.get('tipo', ''),
    } for r in filas])


@maestros_bp.route('/api/mojamiento/<string:tipo_codigo>')
def api_mojamiento(tipo_codigo):
    return jsonify({'mojamiento': MOJAMIENTOS.get(tipo_codigo.upper(), 4000)})
