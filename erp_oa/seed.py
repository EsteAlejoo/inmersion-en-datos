"""
Carga datos iniciales para San Pablo (San Pedro SpA).
Uso: flask --app app seed-db
"""
import click
from flask import current_app
from flask.cli import with_appcontext


CUARTELES_SP = [
    # Limon
    {'nombre': '1A',  'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 1.50},
    {'nombre': '1B',  'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 2.25},
    {'nombre': '1C',  'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 1.25},
    {'nombre': '2',   'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 2.60},
    {'nombre': '3',   'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 0.84},
    {'nombre': '4',   'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 0.84},
    {'nombre': '5',   'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 5.80},
    {'nombre': '6',   'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 0.53},
    {'nombre': '7',   'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 1.93},
    {'nombre': '8',   'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 1.03},
    {'nombre': '9',   'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 0.92},
    {'nombre': '10A', 'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 2.12},
    {'nombre': '10B', 'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 1.47},
    {'nombre': '11',  'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 2.28},
    {'nombre': '12',  'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 0.78},
    {'nombre': '13',  'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 2.25},
    {'nombre': '14',  'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 2.78},
    {'nombre': '15',  'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 3.79},
    {'nombre': '16',  'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 4.31},
    {'nombre': '17',  'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 1.49},
    {'nombre': '18',  'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 4.73},
    {'nombre': '19',  'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 5.14},
    {'nombre': '20',  'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 5.14},
    {'nombre': '21',  'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 4.36},
    {'nombre': '21B', 'especie': 'Limon', 'variedad': 'Lemon Pink', 'ha_total': 0.50, 'es_ensayo': True},
    {'nombre': '22',  'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 2.83},
    {'nombre': '23',  'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 2.61},
    {'nombre': '24',  'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 3.85},
    {'nombre': '25',  'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 5.87},
    {'nombre': '26',  'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 1.73},
    {'nombre': '27',  'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 3.96},
    {'nombre': '28',  'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 3.13},
    {'nombre': '29A', 'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 2.22},
    {'nombre': '29B', 'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 0.96},
    {'nombre': '29C', 'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 0.42},
    {'nombre': '30',  'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 2.23},
    {'nombre': '31',  'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 2.67},
    {'nombre': '32',  'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 1.72},
    {'nombre': '33',  'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 2.57},
    {'nombre': '34',  'especie': 'Limon', 'variedad': 'Fino 49', 'ha_total': 3.10},
    # Naranja
    {'nombre': '1(N)',  'especie': 'Naranja', 'variedad': 'Olinda Valencia', 'ha_total': 0.59},
    {'nombre': '2(N)',  'especie': 'Naranja', 'variedad': 'Olinda Valencia', 'ha_total': 2.30},
    {'nombre': '3(N)',  'especie': 'Naranja', 'variedad': 'Olinda Valencia', 'ha_total': 3.27},
    {'nombre': '4(N)',  'especie': 'Naranja', 'variedad': 'Olinda Valencia', 'ha_total': 4.49},
    {'nombre': '5(N)',  'especie': 'Naranja', 'variedad': 'Olinda Valencia', 'ha_total': 4.36},
    {'nombre': '6(N)',  'especie': 'Naranja', 'variedad': 'Barnfield',       'ha_total': 0.93},
    {'nombre': '7(N)',  'especie': 'Naranja', 'variedad': 'Barnfield',       'ha_total': 3.14},
    {'nombre': '8(N)',  'especie': 'Naranja', 'variedad': 'Barnfield',       'ha_total': 1.43},
    {'nombre': '9(N)',  'especie': 'Naranja', 'variedad': 'Rodhe',           'ha_total': 1.87},
    {'nombre': '10(N)', 'especie': 'Naranja', 'variedad': 'Rodhe',           'ha_total': 2.67},
    {'nombre': '11(N)', 'especie': 'Naranja', 'variedad': 'Lane Late',       'ha_total': 2.10},
    {'nombre': '12(N)', 'especie': 'Naranja', 'variedad': 'Lane Late',       'ha_total': 1.82},
]

PRODUCTOS_SP = [
    {
        'nombre_comercial': 'Defender Potasio',
        'ingrediente_activo': 'Fosfito de potasio',
        'concentracion': '390 g/L',
        'formulacion': 'SL',
        'dosis_100L': 300, 'unidad_dosis': 'cc',
        'objetivo': 'Nutricion / Resistencia sistemica',
        'carencia_limon': 0, 'carencia_naranja': 0,
        'banda_sag': 'VERDE', 'orden_mezcla': 1,
    },
    {
        'nombre_comercial': 'Nitrato de Potasio',
        'ingrediente_activo': 'Nitrato de potasio',
        'concentracion': '99%',
        'formulacion': 'SG',
        'dosis_100L': 3000, 'unidad_dosis': 'g',
        'objetivo': 'Fertilizacion foliar',
        'carencia_limon': 0, 'carencia_naranja': 0,
        'banda_sag': 'VERDE', 'orden_mezcla': 2,
    },
    {
        'nombre_comercial': 'Jabon Potasico Popeye',
        'ingrediente_activo': 'Acidos grasos de potasio',
        'concentracion': '700 g/L',
        'formulacion': 'SL',
        'dosis_100L': 500, 'unidad_dosis': 'cc',
        'objetivo': 'Control mosquita blanca / chanchito blanco',
        'carencia_limon': 0, 'carencia_naranja': 0,
        'banda_sag': 'VERDE', 'orden_mezcla': 3,
    },
    {
        'nombre_comercial': 'Giber Plus SP',
        'ingrediente_activo': 'Acido giberelico',
        'concentracion': '10%',
        'formulacion': 'SP',
        'dosis_100L': 50, 'unidad_dosis': 'cc',
        'objetivo': 'Regulador de crecimiento',
        'carencia_limon': 0, 'carencia_naranja': 0,
        'banda_sag': 'VERDE', 'orden_mezcla': 4,
    },
    {
        'nombre_comercial': 'Konan 240 SC',
        'ingrediente_activo': 'Chlorantraniliprole 200 g/L + Lambda-cihalotrina 50 g/L',
        'concentracion': '240 g/L',
        'formulacion': 'SC',
        'dosis_100L': 50, 'unidad_dosis': 'cc',
        'objetivo': 'Control insectos (trips, lepidopteros)',
        'carencia_limon': 14, 'carencia_naranja': 14, 'carencia_asoex': 21,
        'banda_sag': 'CUIDADO',
        'epp': 'Overol, guantes, mascarilla',
        'orden_mezcla': 5,
    },
    {
        'nombre_comercial': 'Ripper Max 75 SG',
        'ingrediente_activo': 'Abamectina 75 g/kg',
        'concentracion': '75 g/kg',
        'formulacion': 'SG',
        'dosis_100L': 1000, 'unidad_dosis': 'g',
        'objetivo': 'Control acaros y mosquita blanca',
        'carencia_limon': 14, 'carencia_naranja': 14, 'carencia_asoex': 30,
        'banda_sag': 'NOCIVO',
        'epp': 'Overol, guantes, mascarilla, lentes',
        'orden_mezcla': 6,
    },
    {
        'nombre_comercial': 'Winspray',
        'ingrediente_activo': 'Aceite mineral parafinico',
        'concentracion': '850 g/L',
        'formulacion': 'EC',
        'dosis_100L': 1500, 'unidad_dosis': 'cc',
        'objetivo': 'Surfactante / Control mosquita blanca',
        'carencia_limon': 3, 'carencia_naranja': 3,
        'banda_sag': 'VERDE',
        'incompatibilidades': 'No mezclar con Azufre - separar minimo 30 dias. No mezclar con Exirel.',
        'orden_mezcla': 7,
    },
    {
        'nombre_comercial': 'Exirel 200 SC',
        'ingrediente_activo': 'Cyantraniliprole 200 g/L',
        'concentracion': '200 g/L',
        'formulacion': 'SC',
        'dosis_100L': 50, 'unidad_dosis': 'cc',
        'objetivo': 'Control trips y lepidopteros',
        'carencia_limon': 7, 'carencia_naranja': 7, 'carencia_asoex': 14,
        'banda_sag': 'CUIDADO',
        'incompatibilidades': 'No mezclar con formulaciones EC/OD ni aceites minerales (Winspray).',
        'epp': 'Overol, guantes, mascarilla, lentes',
        'orden_mezcla': 8,
    },
    {
        'nombre_comercial': 'Azufre Thiolux Jet',
        'ingrediente_activo': 'Azufre 800 g/kg',
        'concentracion': '800 g/kg',
        'formulacion': 'WG',
        'dosis_100L': 300, 'unidad_dosis': 'g',
        'objetivo': 'Control oidio y acaros',
        'carencia_limon': 3, 'carencia_naranja': 3,
        'banda_sag': 'VERDE',
        'incompatibilidades': 'No mezclar con Winspray (aceites) - separar 30 dias.',
        'orden_mezcla': 9,
    },
    {
        'nombre_comercial': 'Borneo 500 SC',
        'ingrediente_activo': 'Etoxazole 500 g/L',
        'concentracion': '500 g/L',
        'formulacion': 'SC',
        'dosis_100L': 20, 'unidad_dosis': 'cc',
        'objetivo': 'Control acaros (acaricida ovicida)',
        'carencia_limon': 70, 'carencia_naranja': 3, 'carencia_asoex': 70,
        'banda_sag': 'CUIDADO',
        'epp': 'Overol, guantes, mascarilla, lentes',
        'orden_mezcla': 10,
    },
]

TIPOS_APLICACION = [
    {'codigo': 'MOSQ',  'etiqueta': 'Control mosquita blanca',      'mojamiento_sugerido': 4500, 'orden': 1},
    {'codigo': 'CHANCH','etiqueta': 'Control chanchito blanco',     'mojamiento_sugerido': 5000, 'orden': 2},
    {'codigo': 'LAV',   'etiqueta': 'Lavado con detergente',        'mojamiento_sugerido': 9000, 'orden': 3},
    {'codigo': 'FERT',  'etiqueta': 'Fertilizante foliar',          'mojamiento_sugerido': 2000, 'orden': 4},
    {'codigo': 'HERB',  'etiqueta': 'Herbicida',                    'mojamiento_sugerido': 3200, 'orden': 5},
    {'codigo': 'INSEC', 'etiqueta': 'Insecticida / Acaricida general','mojamiento_sugerido': 4000, 'orden': 6},
]


def seed_database():
    from models import db, Agricola, Cuartel, Producto, TipoAplicacion

    # Tipos de aplicacion
    for t in TIPOS_APLICACION:
        if not TipoAplicacion.query.filter_by(codigo=t['codigo']).first():
            db.session.add(TipoAplicacion(**t))

    # Agricola San Pablo
    sp = Agricola.query.filter_by(nombre='San Pablo').first()
    if not sp:
        sp = Agricola(
            nombre='San Pablo',
            productor='San Pedro SpA',
            predio='Campo San Pablo',
            localidad='El Romero, La Serena',
            mercados_destino='["China","UE","USA","Argentina"]',
        )
        db.session.add(sp)
        db.session.flush()

    # Cuarteles San Pablo
    for c in CUARTELES_SP:
        if not Cuartel.query.filter_by(agricola_id=sp.id, nombre=c['nombre']).first():
            db.session.add(Cuartel(
                agricola_id=sp.id,
                nombre=c['nombre'],
                especie=c['especie'],
                variedad=c.get('variedad'),
                ha_total=c['ha_total'],
                es_ensayo=c.get('es_ensayo', False),
            ))

    # Productos San Pablo
    for p in PRODUCTOS_SP:
        if not Producto.query.filter_by(agricola_id=sp.id, nombre_comercial=p['nombre_comercial']).first():
            db.session.add(Producto(agricola_id=sp.id, **p))

    # Agricolas adicionales sin datos
    for nombre in ['Ketcal', 'Pan de Azucar']:
        if not Agricola.query.filter_by(nombre=nombre).first():
            db.session.add(Agricola(nombre=nombre, productor='San Pedro SpA'))

    db.session.commit()
    print(f"Seed completado: {len(CUARTELES_SP)} cuarteles, {len(PRODUCTOS_SP)} productos en San Pablo.")


def init_app(app):
    @app.cli.command('seed-db')
    @with_appcontext
    def seed_cmd():
        """Carga datos iniciales de San Pablo."""
        seed_database()
