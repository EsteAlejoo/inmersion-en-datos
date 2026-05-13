from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import db, Agricola, Cuartel, Producto, OrdenAplicacion, OAProducto, OACuartel
from calculadora import (calcular_fecha_emision_retroactiva, calcular_fecha_desde,
                         calcular_litros_cuartel, calcular_maquinadas,
                         calcular_dosis_ha, calcular_dosis_maquinada)
from collections import defaultdict
from datetime import datetime, date

importacion_bp = Blueprint('importacion', __name__)

DOSIS_OVERRIDE = {
    'DEFENDER POTASIO': 300,
    'DEFENDER K': 300,
    'NITRATO DE POTASIO': 3000,
    'RIPPER MAX 75 SG': 1000,
    'RIPPER MAX': 1000,
    'JABON POTASICO POPEYE ECOFRIENDLY AGRICULTURA': 500,
    'JABON POTASICO POPEYE': 500,
    'GIBER PLUS SP': 50,
}

CUARTELES_ALIAS = {
    '1 (N)': '1(N)', '2 (N)': '2(N)', '3 (N)': '3(N)',
    '4 (N)': '4(N)', '5 (N)': '5(N)', '6 (N)': '6(N)',
    '7 (N)': '7(N)', '8 (N)': '8(N)', '9 (N)': '9(N)',
    '10 (N)': '10(N)', '11 (N)': '11(N)', '12 (N)': '12(N)',
    '1': 'AMBIGUO_1',
    '10': 'AMBIGUO_10',
}

CUARTELES_EXPANSION = {
    'AMBIGUO_1': ['1A', '1B', '1C'],
    'AMBIGUO_10': ['10A', '10B'],
}


@importacion_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        archivo = request.files.get('archivo')
        agricola_id = request.form.get('agricola_id')
        fecha_desde_str = request.form.get('fecha_desde')
        fecha_hasta_str = request.form.get('fecha_hasta')

        if not archivo or not archivo.filename:
            flash('Debes subir un archivo Excel', 'error')
            return redirect(url_for('importacion.index'))

        try:
            fecha_desde = datetime.strptime(fecha_desde_str, '%Y-%m-%d').date()
            fecha_hasta = datetime.strptime(fecha_hasta_str, '%Y-%m-%d').date()
            oas_propuestas = procesar_registro(archivo, int(agricola_id), fecha_desde, fecha_hasta)
            return render_template('importacion/revisar.html',
                                   oas=oas_propuestas,
                                   agricola_id=int(agricola_id),
                                   agricola=Agricola.query.get(int(agricola_id)))
        except Exception as e:
            flash(f'Error al procesar archivo: {str(e)}', 'error')

    agricolas = Agricola.query.filter_by(activa=True).all()
    return render_template('importacion/index.html', agricolas=agricolas)


@importacion_bp.route('/confirmar', methods=['POST'])
def confirmar_importacion():
    import json
    agricola_id = int(request.form['agricola_id'])
    oas_json = request.form.get('oas_json', '[]')
    oas_data = json.loads(oas_json)

    agricola = Agricola.query.get_or_404(agricola_id)
    prefijo = ''.join([p[0] for p in agricola.nombre.split()])[:2].upper()

    creadas = 0
    for oa_info in oas_data:
        if not oa_info.get('seleccionada', True):
            continue

        fi = date.fromisoformat(oa_info['fecha_inicio'])
        fe = calcular_fecha_emision_retroactiva(fi)
        fd = calcular_fecha_desde(fe)
        mojamiento = int(oa_info['mojamiento'])
        estanque = int(oa_info.get('estanque', 2000))

        ultimo = (OrdenAplicacion.query
                  .filter_by(agricola_id=agricola_id)
                  .order_by(OrdenAplicacion.id.desc())
                  .first())
        siguiente = int(ultimo.num_oa.split('-')[-1]) + 1 if ultimo else 1
        num_oa = f'{prefijo}-{siguiente:03d}'

        oa = OrdenAplicacion(
            agricola_id=agricola_id,
            num_oa=num_oa,
            tipo_oa='Retroactiva',
            fecha_emision=fe,
            fecha_desde=fd,
            fecha_inicio_aplicacion=fi,
            mojamiento_Lha=mojamiento,
            capacidad_estanque=estanque,
        )
        db.session.add(oa)
        db.session.flush()

        for prod_nombre, dosis in oa_info['productos'].items():
            p = (Producto.query
                 .filter_by(agricola_id=agricola_id)
                 .filter(Producto.nombre_comercial.ilike(f'%{prod_nombre[:15]}%'))
                 .first())
            if p:
                db.session.add(OAProducto(
                    oa_id=oa.id,
                    producto_id=p.id,
                    dosis_100L=dosis,
                    unidad=p.unidad_dosis,
                    dosis_ha=calcular_dosis_ha(dosis, mojamiento),
                    dosis_maquinada=calcular_dosis_maquinada(dosis, estanque),
                ))

        for cuartel_nombre in oa_info['cuarteles']:
            c = Cuartel.query.filter_by(agricola_id=agricola_id, nombre=cuartel_nombre).first()
            if c:
                litros = calcular_litros_cuartel(float(c.ha_total), mojamiento)
                maquinadas = calcular_maquinadas(litros, estanque)
                db.session.add(OACuartel(
                    oa_id=oa.id,
                    cuartel_id=c.id,
                    ha_efectivas=float(c.ha_total),
                    litros=litros,
                    maquinadas=maquinadas,
                    fecha_aplicacion=fi,
                ))
        creadas += 1

    db.session.commit()
    flash(f'{creadas} OA(s) importadas correctamente', 'success')
    return redirect(url_for('oas.lista'))


def procesar_registro(archivo, agricola_id, fecha_desde, fecha_hasta):
    import pandas as pd

    df = pd.read_excel(archivo)
    df.columns = [str(c).strip() for c in df.columns]

    col_fecha = df.columns[0]
    col_cuartel = df.columns[2]
    col_producto = df.columns[4]
    col_dosis = df.columns[7]
    col_moj = df.columns[8]

    df[col_fecha] = pd.to_datetime(df[col_fecha], errors='coerce')
    df = df.dropna(subset=[col_fecha])
    df = df[(df[col_fecha].dt.date >= fecha_desde) & (df[col_fecha].dt.date <= fecha_hasta)]

    df[col_cuartel] = df[col_cuartel].astype(str).str.strip()
    df[col_cuartel] = df[col_cuartel].map(lambda x: CUARTELES_ALIAS.get(x, x))

    def get_dosis(row):
        prod_key = str(row[col_producto]).strip().upper()
        try:
            dosis_raw = float(row[col_dosis]) if pd.notna(row[col_dosis]) else 0
        except (ValueError, TypeError):
            dosis_raw = 0
        return DOSIS_OVERRIDE.get(prod_key, dosis_raw if dosis_raw else 0)

    df['dosis_norm'] = df.apply(get_dosis, axis=1)
    df['moj_norm'] = df[col_moj].apply(
        lambda x: int(float(x)) if pd.notna(x) and str(x) not in ['#N/A', ''] else 4000
    )

    mezclas = defaultdict(dict)
    for _, row in df.iterrows():
        key = (row[col_fecha].strftime('%Y-%m-%d'), str(row[col_cuartel]), row['moj_norm'])
        mezclas[key][str(row[col_producto]).strip()] = row['dosis_norm']

    grupos = defaultdict(lambda: {'fechas': set(), 'cuarteles': set(), 'productos': {}, 'mojamiento': 0})
    for (fecha_str, cuartel, moj), prods in sorted(mezclas.items()):
        key = (frozenset((p, d) for p, d in prods.items()), moj)
        grupos[key]['fechas'].add(fecha_str)
        grupos[key]['cuarteles'].add(cuartel)
        grupos[key]['productos'] = prods
        grupos[key]['mojamiento'] = moj

    # Expandir cuarteles ambiguos
    for key, info in grupos.items():
        expandidos = set()
        for c in info['cuarteles']:
            if c in CUARTELES_EXPANSION:
                expandidos.update(CUARTELES_EXPANSION[c])
            else:
                expandidos.add(c)
        info['cuarteles'] = expandidos

    oas = []
    for key, info in sorted(grupos.items(), key=lambda x: min(x[1]['fechas'])):
        alertas = [c for c in info['cuarteles'] if c.startswith('AMBIGUO')]
        alertas += [p for p, d in info['productos'].items() if d == 0]
        oas.append({
            'fecha_inicio': min(info['fechas']),
            'fecha_fin': max(info['fechas']),
            'n_dias': len(info['fechas']),
            'mojamiento': info['mojamiento'],
            'productos': info['productos'],
            'cuarteles': sorted(info['cuarteles']),
            'alertas': alertas,
            'estado': 'alerta' if alertas else 'ok',
        })

    return oas
