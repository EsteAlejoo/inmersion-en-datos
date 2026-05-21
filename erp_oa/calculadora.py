from datetime import timedelta


def calcular_fecha_desde(fecha_emision):
    """Fecha desde = emision + 2 dias, no domingo"""
    fd = fecha_emision + timedelta(days=2)
    if fd.weekday() == 6:  # domingo → lunes
        fd += timedelta(days=1)
    return fd


def calcular_fecha_emision_retroactiva(fecha_inicio_aplic):
    """Para OA retroactiva: emision = inicio - 2 dias, no domingo"""
    fe = fecha_inicio_aplic - timedelta(days=2)
    if fe.weekday() == 6:  # domingo → viernes
        fe -= timedelta(days=2)
    return fe


def calcular_dosis_ha(dosis_100L, mojamiento_Lha):
    """dosis/ha = dosis_100L * mojamiento / 100"""
    return round(float(dosis_100L) * float(mojamiento_Lha) / 100, 2)


def calcular_dosis_maquinada(dosis_100L, capacidad_estanque):
    """dosis/maquinada = dosis_100L * estanque / 100"""
    return round(float(dosis_100L) * float(capacidad_estanque) / 100, 2)


def calcular_litros_cuartel(ha_efectivas, mojamiento_Lha):
    """litros = ha * mojamiento"""
    return round(float(ha_efectivas) * float(mojamiento_Lha), 2)


def calcular_maquinadas(litros_cuartel, capacidad_estanque):
    """maquinadas = litros / estanque (decimal exacto — UNICAS por cuartel)"""
    return round(float(litros_cuartel) / float(capacidad_estanque), 2)


def calcular_necesidad_total(dosis_ha, ha_totales):
    """necesidad total = dosis/ha * ha totales"""
    return round(float(dosis_ha) * float(ha_totales), 2)


def validar_incompatibilidades(productos):
    """Detecta incompatibilidades usando ingrediente_activo y campo incompatibilidades."""
    alertas = []
    ias = [(p.ingrediente_activo or '').lower() for p in productos]
    formulaciones = [(p.formulacion or '').upper() for p in productos]

    # R001 (IA): aceites minerales/parafina + azufre → separar 30 días
    tiene_aceite = any('parafina' in ia or 'aceite mineral' in ia or 'aceite' in ia for ia in ias)
    tiene_azufre = any('azufre' in ia for ia in ias)
    if tiene_aceite and tiene_azufre:
        alertas.append({'nivel': 'ROJO', 'mensaje': 'Incompatibilidad Fatal: Aceite mineral y Azufre — separar 30 días'})

    # R002 (IA): cyantraniliprole (Exirel) + aceites/EC/OD
    tiene_cyantraniliprole = any('cyantraniliprole' in ia for ia in ias)
    if tiene_cyantraniliprole:
        if any(f in formulaciones for f in ('EC', 'OD')) or tiene_aceite:
            alertas.append({'nivel': 'ROJO', 'mensaje': 'Cyantraniliprole (Exirel) incompatible con aceites y formulaciones EC/OD'})

    # R004 genérico: cruza campo incompatibilidades de cada producto con IA de los demás
    for i, p in enumerate(productos):
        if not p.incompatibilidades:
            continue
        texto = p.incompatibilidades.lower()
        for j, q in enumerate(productos):
            if i == j:
                continue
            ia_q = (q.ingrediente_activo or '').lower()
            if ia_q and ia_q in texto:
                msg = (f'Incompatibilidad: {p.ingrediente_activo} '
                       f'incompatible con {q.ingrediente_activo}')
                alertas.append({'nivel': 'ROJO', 'mensaje': msg})

    # Deduplicar
    vistos, unicos = set(), []
    for a in alertas:
        if a['mensaje'] not in vistos:
            vistos.add(a['mensaje'])
            unicos.append(a)
    return unicos


def validar_borneo_limon(productos, especie):
    """R003 (IA): bifenazate en Limón = 70 días carencia"""
    alertas = []
    if 'LIMON' in especie.upper():
        if any('bifenazate' in (p.ingrediente_activo or '').lower() for p in productos):
            alertas.append({
                'nivel': 'ROJO',
                'mensaje': 'CRITICO: Bifenazate (Borneo) en Limón = 70 días carencia (vs 3 días otros cítricos)'
            })
    return alertas
