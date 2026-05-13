from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from models import db, OrdenAplicacion, OAProducto, OACuartel, Agricola, Cuartel, Producto
from calculadora import (calcular_fecha_desde, calcular_fecha_emision_retroactiva,
                         calcular_dosis_ha, calcular_dosis_maquinada,
                         calcular_litros_cuartel, calcular_maquinadas,
                         validar_incompatibilidades, validar_borneo_limon)
from datetime import date, datetime

oas_bp = Blueprint('oas', __name__)


@oas_bp.route('/')
def lista():
    agricola_id = request.args.get('agricola_id')
    estado = request.args.get('estado')
    q = OrdenAplicacion.query.order_by(OrdenAplicacion.fecha_inicio_aplicacion.desc())
    if agricola_id:
        q = q.filter_by(agricola_id=agricola_id)
    if estado:
        q = q.filter_by(estado=estado)
    oas = q.all()
    agricolas = Agricola.query.filter_by(activa=True).all()
    return render_template('oas/lista.html', oas=oas, agricolas=agricolas,
                           filtro_agricola=agricola_id, filtro_estado=estado)


@oas_bp.route('/nueva', methods=['GET', 'POST'])
def nueva():
    if request.method == 'POST':
        return _procesar_form_oa(None)
    agricolas = Agricola.query.filter_by(activa=True).all()
    return render_template('oas/form.html', oa=None, agricolas=agricolas)


@oas_bp.route('/<int:oa_id>/editar', methods=['GET', 'POST'])
def editar(oa_id):
    oa = OrdenAplicacion.query.get_or_404(oa_id)
    if oa.estado == 'confirmada':
        flash('No se puede editar una OA confirmada', 'error')
        return redirect(url_for('oas.detalle', oa_id=oa_id))
    if request.method == 'POST':
        return _procesar_form_oa(oa)
    agricolas = Agricola.query.filter_by(activa=True).all()
    return render_template('oas/form.html', oa=oa, agricolas=agricolas)


@oas_bp.route('/<int:oa_id>')
def detalle(oa_id):
    oa = OrdenAplicacion.query.get_or_404(oa_id)
    prods = [op.producto for op in oa.productos]
    alertas = validar_incompatibilidades(prods) + validar_borneo_limon(prods, oa.especie or '')
    return render_template('oas/detalle.html', oa=oa, alertas=alertas)


@oas_bp.route('/<int:oa_id>/confirmar', methods=['POST'])
def confirmar(oa_id):
    oa = OrdenAplicacion.query.get_or_404(oa_id)
    if oa.estado == 'confirmada':
        flash('Esta OA ya esta confirmada', 'error')
        return redirect(url_for('oas.detalle', oa_id=oa_id))

    prods = [op.producto for op in oa.productos]
    alertas_criticas = [a for a in
                        validar_incompatibilidades(prods) + validar_borneo_limon(prods, oa.especie or '')
                        if a['nivel'] == 'ROJO']

    if alertas_criticas and not request.form.get('forzar'):
        return render_template('oas/detalle.html', oa=oa, alertas=alertas_criticas, pedir_confirmacion=True)

    ha_totales = sum(float(oc.ha_efectivas) for oc in oa.cuarteles)
    litros_totales = sum(float(oc.litros or 0) for oc in oa.cuarteles)
    maquinadas_totales = sum(float(oc.maquinadas or 0) for oc in oa.cuarteles)

    oa.ha_totales = ha_totales
    oa.litros_totales = litros_totales
    oa.maquinadas_totales = maquinadas_totales
    oa.estado = 'confirmada'
    oa.confirmed_at = datetime.utcnow()
    db.session.commit()

    flash(f'OA {oa.num_oa} confirmada correctamente', 'success')
    return redirect(url_for('oas.detalle', oa_id=oa_id))


@oas_bp.route('/<int:oa_id>/anular', methods=['POST'])
def anular(oa_id):
    oa = OrdenAplicacion.query.get_or_404(oa_id)
    oa.estado = 'anulada'
    db.session.commit()
    flash(f'OA {oa.num_oa} anulada', 'error')
    return redirect(url_for('oas.lista'))


@oas_bp.route('/<int:oa_id>/pdf')
def generar_pdf(oa_id):
    oa = OrdenAplicacion.query.get_or_404(oa_id)
    try:
        from weasyprint import HTML
        html_str = render_template('pdf/oa_template.html', oa=oa)
        pdf = HTML(string=html_str).write_pdf()
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'inline; filename=OA-{oa.num_oa}.pdf'
        return response
    except ImportError:
        flash('WeasyPrint no esta instalado. Instala con: pip install weasyprint', 'error')
        return redirect(url_for('oas.detalle', oa_id=oa_id))


def _procesar_form_oa(oa_existente):
    form = request.form

    agricola_id = int(form['agricola_id'])
    tipo_oa = form['tipo_oa']
    fecha_inicio = date.fromisoformat(form['fecha_inicio_aplicacion'])
    mojamiento = int(form['mojamiento_Lha'])
    estanque = int(form['capacidad_estanque'])

    if tipo_oa == 'Retroactiva':
        fecha_emision = calcular_fecha_emision_retroactiva(fecha_inicio)
    else:
        fecha_emision = date.today()
    fecha_desde = calcular_fecha_desde(fecha_emision)

    if not oa_existente:
        agricola = Agricola.query.get(agricola_id)
        prefijo = ''.join([p[0] for p in agricola.nombre.split()])[:2].upper()
        ultimo = (OrdenAplicacion.query
                  .filter_by(agricola_id=agricola_id)
                  .order_by(OrdenAplicacion.id.desc())
                  .first())
        siguiente = int(ultimo.num_oa.split('-')[-1]) + 1 if ultimo else 1
        num_oa = f'{prefijo}-{siguiente:03d}'
        oa = OrdenAplicacion(agricola_id=agricola_id, num_oa=num_oa)
    else:
        oa = oa_existente

    oa.tipo_oa = tipo_oa
    oa.tipo_aplicacion_codigo = form.get('tipo_aplicacion')
    oa.fecha_emision = fecha_emision
    oa.fecha_desde = fecha_desde
    oa.fecha_inicio_aplicacion = fecha_inicio
    oa.mojamiento_Lha = mojamiento
    oa.capacidad_estanque = estanque
    oa.especie = form.get('especie')
    oa.estado_fenologico = form.get('estado_fenologico')
    oa.tipo_maquina = form.get('tipo_maquina')
    oa.agronomo = form.get('agronomo')
    oa.mercado_destino = form.get('mercado_destino')
    oa.indicaciones = form.get('indicaciones')

    if not oa_existente:
        db.session.add(oa)
        db.session.flush()
    else:
        OAProducto.query.filter_by(oa_id=oa.id).delete()
        OACuartel.query.filter_by(oa_id=oa.id).delete()

    # Guardar productos
    productos_ids = request.form.getlist('producto_id[]')
    dosis_list = request.form.getlist('dosis_100L[]')
    unidades_list = request.form.getlist('unidad[]')
    objetivos_list = request.form.getlist('objetivo[]')

    for i, pid in enumerate(productos_ids):
        if not pid:
            continue
        dosis = float(dosis_list[i]) if i < len(dosis_list) and dosis_list[i] else 0
        unidad = unidades_list[i] if i < len(unidades_list) else 'cc'
        db.session.add(OAProducto(
            oa_id=oa.id,
            producto_id=int(pid),
            dosis_100L=dosis,
            unidad=unidad,
            objetivo=objetivos_list[i] if i < len(objetivos_list) else '',
            dosis_ha=calcular_dosis_ha(dosis, mojamiento),
            dosis_maquinada=calcular_dosis_maquinada(dosis, estanque),
            orden=i,
        ))

    # Guardar cuarteles
    cuartel_ids = request.form.getlist('cuartel_id[]')
    ha_ef_list = request.form.getlist('ha_efectivas[]')
    fechas_aplic = request.form.getlist('fecha_aplicacion[]')

    for i, cid in enumerate(cuartel_ids):
        if not cid:
            continue
        ha_ef = float(ha_ef_list[i]) if i < len(ha_ef_list) and ha_ef_list[i] else 0
        litros = calcular_litros_cuartel(ha_ef, mojamiento)
        maquinadas = calcular_maquinadas(litros, estanque)
        fecha_aplic = None
        if i < len(fechas_aplic) and fechas_aplic[i]:
            try:
                fecha_aplic = date.fromisoformat(fechas_aplic[i])
            except ValueError:
                pass
        db.session.add(OACuartel(
            oa_id=oa.id,
            cuartel_id=int(cid),
            ha_efectivas=ha_ef,
            litros=litros,
            maquinadas=maquinadas,
            fecha_aplicacion=fecha_aplic,
        ))

    db.session.commit()
    flash(f'OA {oa.num_oa} guardada correctamente', 'success')
    return redirect(url_for('oas.detalle', oa_id=oa.id))
