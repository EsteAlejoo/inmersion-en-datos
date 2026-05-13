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
    """Retorna lista de alertas de incompatibilidad entre productos"""
    alertas = []
    nombres = [p.nombre_comercial.upper() for p in productos]
    formulaciones = [p.formulacion.upper() if p.formulacion else '' for p in productos]

    # R001: Winspray + Azufre
    if any('WINSPRAY' in n for n in nombres) and any('AZUFRE' in n or 'THIOLUX' in n for n in nombres):
        alertas.append({'nivel': 'ROJO', 'mensaje': 'Incompatibilidad Fatal: Separar Winspray y Azufre 30 dias'})

    # R002: Exirel + Aceites/EC/OD
    if any('EXIREL' in n for n in nombres):
        if any(f in formulaciones for f in ['EC', 'OD']) or any('ACEITE' in n or 'WINSPRAY' in n for n in nombres):
            alertas.append({'nivel': 'ROJO', 'mensaje': 'Exirel incompatible con aceites y formulaciones EC/OD'})

    return alertas


def validar_borneo_limon(productos, especie):
    """R003: Borneo en Limon tiene carencia 70 dias"""
    alertas = []
    if 'LIMON' in especie.upper():
        if any('BORNEO' in p.nombre_comercial.upper() for p in productos):
            alertas.append({'nivel': 'ROJO', 'mensaje': 'CRITICO: Borneo en Limon = 70 dias carencia (vs 3 dias otros citricos)'})
    return alertas
