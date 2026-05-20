"""
Genera OA_plantilla_v5.xlsx — Orden de Aplicación de Agroquímicos
San Pedro SpA · Mayo 2026

Hoja 1 "OA":     Cabecera, datos agrícola/aplicación, tabla productos (con fórmulas),
                  instrucciones, firma.
Hoja 2 "Desglose": Desglose de cantidades por cuartel (fórmulas automáticas desde Hoja 1).
"""

from openpyxl import Workbook
from openpyxl.styles import (Font, PatternFill, Alignment, Border, Side)
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
import os

# ── Paleta de colores ────────────────────────────────────────────
C_CG1_D  = "1B3347"   # Empresa (azul oscuro)
C_CG1_L  = "E5F0F6"
C_CG2_D  = "1A4D2E"   # Aplicación (verde oscuro)
C_CG2_L  = "EAF4EF"
C_CG3_D  = "3E2218"   # Control/seguridad (marrón oscuro)
C_CG3_L  = "F7EEEB"
C_GRAY_D = "424242"
C_GRAY_L = "E8E8E8"
C_GRAY_LL= "FAFAFA"
C_INPUT  = "FFFDE7"   # Celdas de entrada (amarillo suave)
C_CALC   = "EAF4EF"   # Celdas calculadas (verde suave)
C_ALERT  = "FFF5F5"   # Nota cosecha (rojo suave)
C_ALERT_T= "991B1B"
C_WHITE  = "FFFFFF"
C_TOX_IB = "E53E3E"   # Ripper Max Ib
C_TOX_U  = "38A169"   # Exirel U
C_TOX_NA = "888888"   # Defender NA

def fill(hex_color):
    return PatternFill("solid", fgColor=hex_color)

def font(bold=False, size=9, color="000000", italic=False):
    return Font(bold=bold, size=size, color=color, italic=italic, name="Arial")

def border_all(style="thin"):
    s = Side(border_style=style)
    return Border(left=s, right=s, top=s, bottom=s)

def border_bottom(color="000000", style="medium"):
    return Border(bottom=Side(border_style=style, color=color))

def align(horizontal="left", vertical="center", wrap=False):
    return Alignment(horizontal=horizontal, vertical=vertical, wrap_text=wrap)

def set_cell(ws, row, col, value="", bold=False, size=9, bg=None, fg="000000",
             h_align="left", v_align="center", wrap=False, italic=False,
             num_format=None, border=None):
    c = ws.cell(row=row, column=col, value=value)
    c.font = font(bold=bold, size=size, color=fg, italic=italic)
    if bg: c.fill = fill(bg)
    c.alignment = align(h_align, v_align, wrap)
    if num_format: c.number_format = num_format
    if border: c.border = border
    return c

def header_row(ws, row, text, bg_color, col_start=1, col_end=10, size=8):
    ws.merge_cells(start_row=row, start_column=col_start,
                   end_row=row, end_column=col_end)
    c = set_cell(ws, row, col_start, text, bold=True, size=size,
                 bg=bg_color, fg=C_WHITE, h_align="left", v_align="center")
    return c

def label_value(ws, row, label_col, val_col, label, value, bg_val=C_INPUT,
                size_val=9, bold_val=False, span_end=None):
    set_cell(ws, row, label_col, label, bold=True, size=8, fg="555555",
             bg=C_GRAY_LL, h_align="right")
    if span_end:
        ws.merge_cells(start_row=row, start_column=val_col,
                       end_row=row, end_column=span_end)
    set_cell(ws, row, val_col, value, bold=bold_val, size=size_val,
             bg=bg_val, h_align="left")

# ════════════════════════════════════════════════════════════════
wb = Workbook()
ws1 = wb.active
ws1.title = "OA"
ws2 = wb.create_sheet("Desglose")

# ── Anchos de columnas Hoja 1 ────────────────────────────────
col_widths_1 = [4, 22, 18, 13, 8, 8, 10, 10, 9, 9, 7]
for i, w in enumerate(col_widths_1, 1):
    ws1.column_dimensions[get_column_letter(i)].width = w

# ── Alturas de fila Hoja 1 (predefinidas) ───────────────────
row_heights = {1:18, 2:14, 3:4, 4:14, 5:14, 6:14, 7:4,
               8:14, 9:14, 10:14, 11:14, 12:4,
               13:28, 14:16, 15:16, 16:16, 17:4,
               18:11, 19:11, 20:11, 21:11, 22:4,
               23:20, 24:20, 25:20, 26:20, 27:4,
               28:14, 29:30, 30:4, 31:18, 32:18, 33:18}
for r, h in row_heights.items():
    ws1.row_dimensions[r].height = h

ws1.freeze_panes = "B14"

# ────────────────────────────────────────────────────────────────
# ENCABEZADO TÍTULO (filas 1-2)
# ────────────────────────────────────────────────────────────────
ws1.merge_cells("B1:H1")
set_cell(ws1, 1, 2, "ORDEN DE APLICACIÓN DE AGROQUÍMICOS",
         bold=True, size=12, fg=C_CG2_D, h_align="center", v_align="center")
ws1.merge_cells("I1:J1")
set_cell(ws1, 1, 9, "N. Orden:", bold=True, size=8, fg="555555",
         bg=C_GRAY_LL, h_align="right")
set_cell(ws1, 1, 11, "SP-042", bold=True, size=11, fg=C_CG2_D,
         bg=C_INPUT, h_align="center")

ws1.merge_cells("B2:H2")
set_cell(ws1, 2, 2, "San Pedro SpA · Emisión:", size=8, fg="888888", italic=True)
ws1.merge_cells("I2:J2")
set_cell(ws1, 2, 9, "Fecha Emisión:", bold=True, size=8, fg="555555",
         bg=C_GRAY_LL, h_align="right")
set_cell(ws1, 2, 11, "08-05-2026", size=9, bg=C_INPUT)

# ────────────────────────────────────────────────────────────────
# BLOQUE AGRÍCOLA (filas 4-6)  bg=cg1
# ────────────────────────────────────────────────────────────────
header_row(ws1, 4, "DATOS DE LA AGRÍCOLA", C_CG1_D, col_start=1, col_end=11)

label_value(ws1, 5, 1, 2, "Razón Social", "San Pedro SpA", span_end=4)
label_value(ws1, 5, 5, 6, "RUT", "76.123.456-7", span_end=7)
label_value(ws1, 5, 8, 9, "Predio", "Campo San Pablo", span_end=10)
label_value(ws1, 5, 11, 11, "CSG", "CSG-001")

label_value(ws1, 6, 1, 2, "Dirección", "Camino El Romero s/n", span_end=7)
label_value(ws1, 6, 8, 9, "Localidad", "La Serena, Elqui, Coquimbo", span_end=11)

# ────────────────────────────────────────────────────────────────
# BLOQUE APLICACIÓN (filas 8-11)  bg=cg2
# ────────────────────────────────────────────────────────────────
header_row(ws1, 8, "DATOS DE APLICACIÓN", C_CG2_D, col_start=1, col_end=11)

label_value(ws1, 9, 1, 2, "Fecha Inicio", "10-05-2026")
label_value(ws1, 9, 4, 5, "Especie", "Limón")
label_value(ws1, 9, 7, 8, "Variedad", "Fino 49", span_end=9)
label_value(ws1, 9, 10, 11, "E. Fenológico", "Frutos 40-60 mm")

label_value(ws1, 10, 1, 2, "Cuarteles", "15–16, 18–20  (5 cuarteles)", span_end=5)
label_value(ws1, 10, 6, 7, "Sup. Total (ha)", 23.11, bg_val=C_CALC, bold_val=True)
label_value(ws1, 10, 8, 9, "Mojamiento (L/ha)", 4500, bg_val=C_INPUT, bold_val=True)
ws1["J10"].number_format = "#,##0"
label_value(ws1, 10, 10, 11, "Cap. Estanque (L)", 2000, bg_val=C_INPUT, bold_val=True)

label_value(ws1, 11, 1, 2, "Mercado Destino", "Exportación — China/UE", span_end=4)
label_value(ws1, 11, 5, 6, "Forma Aplic.", "Pulverizadora", span_end=7)
label_value(ws1, 11, 8, 9, "Reingreso", "24 h · Emb./Lact.: 48 h", span_end=11)

# ── Notas de celdas clave ────────────────────────────────────
# Indicar cuales son input vs calculado
ws1["G10"].comment = None  # total ha

# ────────────────────────────────────────────────────────────────
# TABLA PRODUCTOS (fila 13 header, 14-23 datos, 24 total)
# ────────────────────────────────────────────────────────────────
# Referencias a valores clave en la hoja
REF_MOJ  = "J10"   # Mojamiento L/ha
REF_EST  = "K10"   # Cap. Estanque L
REF_HA   = "G10"   # Superficie total ha
N_PROD   = 10      # Filas de producto

# Encabezados tabla
PROD_HEADERS = [
    ("Nombre comercial",   22, "left"),
    ("Ingrediente activo", 18, "center"),
    ("Objetivo",           13, "center"),
    ("Dosis/100L\n(cc ó g)", 8, "center"),
    ("Dosis/Ha\n(L ó kg)",   8, "center"),
    ("Nec.\nMaquinada\n(L ó kg)", 10, "center"),
    ("Nec.\nTotal\n(L ó kg)",     10, "center"),
    ("Carencia\nEtiq.\n(días)",    9, "center"),
    ("Carencia\nASOEX\n(días)",    9, "center"),
    ("Usos/\nTemp.",               7, "center"),
]

header_row(ws1, 12, "PRODUCTOS — MEZCLA DE APLICACIÓN", C_CG2_D, col_start=1, col_end=10)

t_thick = Side(border_style="medium")
t_thin  = Side(border_style="thin")

for idx, (hdr, _w, ha) in enumerate(PROD_HEADERS, 1):
    c = ws1.cell(row=13, column=idx, value=hdr)
    c.font     = Font(bold=True, size=7, name="Arial", color="111111")
    c.fill     = fill(C_GRAY_L)
    c.alignment = Alignment(horizontal=ha, vertical="center", wrap_text=True)
    c.border   = Border(left=t_thin, right=t_thin,
                        top=t_thick, bottom=t_thick)

ws1.row_dimensions[13].height = 32

# Filas de producto (14 a 23)
sample_products = [
    ("Defender Potasio",    "Fosfito de potasio",      "Nutricion / Resistencia",   300, C_TOX_NA),
    ("Ripper Max 75 SG",    "Abamectina 75 g/kg",      "Acaros / Mosquita blanca", 1000, C_TOX_IB),
    ("Exirel 200 SC",       "Cyantraniliprole 200 g/L","Trips / Lepidópteros",       50, C_TOX_U),
] + [("","","",None, C_WHITE)] * 7

sample_carencia = [
    (0, "—", "—"),
    (14, 30, "1 de 3"),
    (7,  14, "1 de 2"),
] + [("—","—","—")] * 7

for i, (prod, car) in enumerate(zip(sample_products, sample_carencia)):
    row = 14 + i
    nombre, ia, obj, dosis, tox_color = prod
    c_etiq, c_asoex, usos = car
    bg_row = C_GRAY_LL if i % 2 == 0 else C_WHITE

    def pc(col, val, bg=bg_row, bold=False, ha="left", nf=None):
        c = set_cell(ws1, row, col, val, bold=bold, size=8, bg=bg,
                     h_align=ha, v_align="center")
        c.border = Border(left=t_thin, right=t_thin,
                          top=t_thin, bottom=t_thin)
        if nf: c.number_format = nf
        return c

    pc(1, nombre, bold=bool(nombre))
    pc(2, ia, ha="center")
    pc(3, obj, ha="center")

    # Dosis/100L input
    dc = ws1.cell(row=row, column=4, value=dosis)
    dc.font = Font(bold=bool(dosis), size=8, name="Arial", color="1A3080")
    dc.fill = fill(C_INPUT if dosis else bg_row)
    dc.alignment = align("center")
    dc.border = Border(left=t_thin, right=t_thin, top=t_thin, bottom=t_thin)
    if dosis: dc.number_format = "#,##0"

    # Dosis/ha = dosis_100L * moj / 100 / 1000  → L o kg
    col_d = get_column_letter(4)
    moj_ref = REF_MOJ  # J10
    est_ref = REF_EST  # K10
    ha_ref  = REF_HA   # G10

    if dosis:
        f_ha   = f"=IFERROR({col_d}{row}*{moj_ref}/100/1000,\"—\")"
        f_maq  = f"=IFERROR({col_d}{row}*{est_ref}/100/1000,\"—\")"
        f_tot  = f"=IFERROR({col_d}{row}*{moj_ref}*{ha_ref}/100/1000,\"—\")"
    else:
        f_ha = f_maq = f_tot = ""

    for col_idx, fval in [(5, f_ha), (6, f_maq), (7, f_tot)]:
        c2 = ws1.cell(row=row, column=col_idx, value=fval)
        c2.font = Font(size=8, name="Arial", color="1A3080" if fval else "888888")
        c2.fill = fill(C_CALC if fval else bg_row)
        c2.alignment = align("center")
        c2.border = Border(left=t_thin, right=t_thin, top=t_thin, bottom=t_thin)
        if fval: c2.number_format = "#,##0.00"

    # Carencia cols
    for col_idx, val in [(8, c_etiq), (9, c_asoex)]:
        cv = ws1.cell(row=row, column=col_idx, value=val)
        cv.font = Font(size=8, name="Arial", bold=isinstance(val, int) and val > 0)
        cv.fill = fill(bg_row)
        cv.alignment = align("center")
        cv.border = Border(left=t_thin, right=t_thin, top=t_thin, bottom=t_thin)

    # Color borde inferior según tox (col A)
    ws1.cell(row=row, column=1).border = Border(
        left=t_thin, right=t_thin, top=t_thin,
        bottom=Side(border_style="medium", color=tox_color.replace("#",""))
    )

    # Usos/Temp
    pc(10, usos, ha="center")

# Fila total (fila 24)
ws1.row_dimensions[24].height = 14
header_row(ws1, 24, "* Celdas amarillas = entrada manual   · Celdas verdes = cálculo automático   · Dosis/ha = Dosis/100L × Mojamiento ÷ 100 ÷ 1000",
           C_GRAY_D, col_start=1, col_end=10, size=7)

# ────────────────────────────────────────────────────────────────
# NOTA COSECHA (filas 26-28)
# ────────────────────────────────────────────────────────────────
ws1.merge_cells("A26:J26")
nc = ws1["A26"]
nc.value = ("⚠  Fecha posible Cosecha = Fecha aplicación (día 0) + días carencia + 1."
            "  Ej: aplicado 10-05 (día 0) + 30 días ASOEX + 1 = cosecha no antes del 11-06-2026."
            "  — Carencia mayor este OA: Ripper Max ASOEX 30 días.")
nc.font = Font(bold=False, size=7.5, name="Arial", color=C_ALERT_T)
nc.fill = fill("FFF5F5")
nc.alignment = Alignment(wrap_text=True, vertical="center")
ws1.row_dimensions[26].height = 20

# ────────────────────────────────────────────────────────────────
# INSTRUCCIONES / SEGURIDAD (filas 28-30)
# ────────────────────────────────────────────────────────────────
header_row(ws1, 28, "INSTRUCCIONES DE SEGURIDAD", C_CG3_D, col_start=1, col_end=10)
instrs = [
    "• Verifique que SAG, apicultores, y poblaciones cercanas estén notificados.",
    "• Use siempre su equipo de protección personal (EPP) y lea la etiqueta del producto.",
    "• No debe haber terceros durante la aplicación.",
]
for i, txt in enumerate(instrs):
    ws1.merge_cells(start_row=29+i, start_column=1, end_row=29+i, end_column=10)
    c = ws1.cell(row=29+i, column=1, value=txt)
    c.font = Font(size=8, name="Arial")
    c.fill = fill(C_CG3_L)
    c.alignment = Alignment(vertical="center", wrap_text=False)
    ws1.row_dimensions[29+i].height = 13

# ────────────────────────────────────────────────────────────────
# FIRMAS (fila 33)
# ────────────────────────────────────────────────────────────────
header_row(ws1, 32, "", C_WHITE, col_start=1, col_end=10)  # spacer
ws1.row_dimensions[32].height = 6
for col_s, col_e, label in [(1,3,"Responsable Técnico"), (4,7,"Emisor"), (8,10,"Recibe")]:
    ws1.merge_cells(start_row=33, start_column=col_s, end_row=33, end_column=col_e)
    c = ws1.cell(row=33, column=col_s, value=label)
    c.font = Font(bold=True, size=8, name="Arial", color="333333")
    c.fill = fill(C_GRAY_LL)
    c.alignment = Alignment(horizontal="center", vertical="bottom")
    c.border = Border(bottom=Side(border_style="medium"))
    ws1.row_dimensions[33].height = 28

# ════════════════════════════════════════════════════════════════
# HOJA 2 — DESGLOSE POR CUARTEL
# ════════════════════════════════════════════════════════════════
col_widths_2 = [3, 9, 8, 11, 10, 10, 14, 14, 14, 14]
for i, w in enumerate(col_widths_2, 1):
    ws2.column_dimensions[get_column_letter(i)].width = w

# Cabecera hoja 2
header_row(ws2, 1, "DESGLOSE POR CUARTEL — Cantidades de producto por carga", C_CG2_D, col_start=1, col_end=10)
ws2.row_dimensions[1].height = 16
ws2.merge_cells("A2:D2")
ws2["A2"] = "=OA!K1"
ws2["A2"].font = Font(bold=True, size=9, name="Arial", color=C_CG2_D)
ws2.merge_cells("E2:G2")
ws2["E2"] = "Mojamiento (L/ha):"
ws2["E2"].font = Font(bold=True, size=8, name="Arial", color="555555")
ws2["E2"].alignment = Alignment(horizontal="right", vertical="center")
ws2["H2"] = "=OA!J10"
ws2["H2"].number_format = "#,##0"
ws2["H2"].font = Font(bold=True, size=9, name="Arial")
ws2["I2"] = "Cap. estanque (L):"
ws2["I2"].font = Font(bold=True, size=8, name="Arial", color="555555")
ws2["I2"].alignment = Alignment(horizontal="right", vertical="center")
ws2["J2"] = "=OA!K10"
ws2["J2"].number_format = "#,##0"
ws2["J2"].font = Font(bold=True, size=9, name="Arial")

# Encabezados tabla desglose (fila 4)
ws2.row_dimensions[4].height = 36
desg_headers = [
    ("", 3),
    ("Cuartel", 9),
    ("Sup. (ha)", 8),
    ("Vol. solución\n(L)", 11),
    ("Maq. completas\n×J2 L", 10),
    ("L adicionales", 10),
    ("Defender Potasio\n(L)\nNA ·· FERT", 14),
    ("Ripper Max 75 SG\n(kg)\nIb ·· ACAR", 14),
    ("Exirel 200 SC\n(L)\nU ·· INSC", 14),
    ("Prod.4\n(L ó kg)", 14),
]
tox_colors = [None, None, None, None, None, None,
              C_TOX_NA, C_TOX_IB, C_TOX_U, "AAAAAA"]

for idx, ((hdr, _w), tox_col) in enumerate(zip(desg_headers, tox_colors), 1):
    c = ws2.cell(row=4, column=idx, value=hdr)
    c.font  = Font(bold=True, size=7, name="Arial", color="111111")
    c.fill  = fill(C_GRAY_L)
    c.alignment = Alignment(horizontal="center", vertical="bottom", wrap_text=True)
    bot_side = Side(border_style="thick", color=tox_col) if tox_col else Side(border_style="medium")
    c.border = Border(left=t_thin, right=t_thin, top=t_thick, bottom=bot_side)

# Datos cuarteles (filas 5-9 para los 5 cuarteles del ejemplo)
cuarteles = [("15", 3.79), ("16", 4.31), ("18", 4.73), ("19", 5.14), ("20", 5.14)]
dosis_100L = [300, 1000, 50]  # cc o g por 100L de los 3 productos

# Columnas de productos en desglose: G, H, I (cols 7, 8, 9)
# Fórmula vol. sol. = ha * moj  →  B* * J2
# Maq. completas = INT(vol / J2)
# L adicionales = vol - maq_completas * J2
# Producto = vol * dosis100L / 100 / 1000

for i, (cname, ha_val) in enumerate(cuarteles):
    row = 5 + i
    bg_row = C_GRAY_LL if i % 2 == 0 else C_WHITE
    ws2.row_dimensions[row].height = 14

    ws2.cell(row=row, column=1)  # spacer
    cn = ws2.cell(row=row, column=2, value=cname)
    cn.font = Font(bold=True, size=8, name="Arial")
    cn.fill = fill(C_CG2_L)
    cn.border = border_all()
    cn.alignment = align("center")

    ha_c = ws2.cell(row=row, column=3, value=ha_val)
    ha_c.font = Font(size=8, name="Arial")
    ha_c.fill = fill(C_INPUT)
    ha_c.border = border_all()
    ha_c.alignment = align("center")
    ha_c.number_format = "#,##0.00"

    # Vol. solución = C{row} * OA.J10
    vol_col = get_column_letter(3)
    vc = ws2.cell(row=row, column=4, value=f"={vol_col}{row}*OA!$J$10")
    vc.font = Font(size=8, name="Arial", color="1A3080")
    vc.fill = fill(C_CALC)
    vc.border = border_all()
    vc.alignment = align("center")
    vc.number_format = "#,##0"

    # Maq. completas = INT(D{row}/OA!K10)
    mc = ws2.cell(row=row, column=5, value=f"=INT(D{row}/OA!$K$10)")
    mc.font = Font(size=8, name="Arial", color="1A3080")
    mc.fill = fill(C_CALC)
    mc.border = border_all()
    mc.alignment = align("center")
    mc.number_format = "#,##0"

    # L adicionales = D{row} - E{row}*OA!K10
    la = ws2.cell(row=row, column=6, value=f"=D{row}-E{row}*OA!$K$10")
    la.font = Font(size=8, name="Arial", color="1A3080")
    la.fill = fill(C_CALC)
    la.border = border_all()
    la.alignment = align("center")
    la.number_format = "#,##0"

    # Producto cols (G, H, I = cols 7, 8, 9)
    # Cantidad = Vol_solución * dosis_100L / 100 / 1000
    oa_dosis_cells = ["OA!$D$14", "OA!$D$15", "OA!$D$16"]  # dosis/100L en OA hoja
    for j, (d_cell) in enumerate(oa_dosis_cells):
        col_idx = 7 + j
        formula = f"=IFERROR(D{row}*{d_cell}/100/1000,\"—\")"
        pc2 = ws2.cell(row=row, column=col_idx, value=formula)
        pc2.font = Font(size=8, name="Arial", color="1A3080")
        pc2.fill = fill(C_CALC)
        pc2.border = border_all()
        pc2.alignment = align("center")
        pc2.number_format = "#,##0.00"

    # Col 10: placeholder producto 4
    p4 = ws2.cell(row=row, column=10, value="")
    p4.fill = fill(C_INPUT)
    p4.border = border_all()

# Fila TOTAL (fila 10)
tot_row = 5 + len(cuarteles)
ws2.row_dimensions[tot_row].height = 14
for col_idx in range(2, 11):
    c = ws2.cell(row=tot_row, column=col_idx)
    if col_idx == 2:
        c.value = "TOTAL"
        c.font = Font(bold=True, size=8, name="Arial")
        c.fill = fill(C_GRAY_L)
    elif col_idx >= 3:
        col_l = get_column_letter(col_idx)
        c.value = f"=SUM({col_l}5:{col_l}{tot_row-1})"
        c.font = Font(bold=True, size=8, name="Arial", color="1A3080")
        c.fill = fill(C_GRAY_L)
        if col_idx in [4, 5, 6]: c.number_format = "#,##0"
        else: c.number_format = "#,##0.00"
    c.border = Border(left=t_thin, right=t_thin,
                      top=t_thick, bottom=t_thick)
    c.alignment = align("center")

# Nota al pie hoja 2
ws2.merge_cells(f"A{tot_row+2}:J{tot_row+2}")
n = ws2.cell(row=tot_row+2, column=1,
             value="* Maq. completa = capacidad estanque OA!K10 L  ·  "
                   "Cantidades referenciales según calibración vigente.  ·  "
                   "FERT=Fertilizante  ACAR=Acaricida  INSC=Insecticida")
n.font = Font(size=7, italic=True, color="666666", name="Arial")
n.alignment = Alignment(wrap_text=True, vertical="center")
ws2.row_dimensions[tot_row+2].height = 12

ws2.merge_cells(f"A{tot_row+3}:J{tot_row+3}")
n2 = ws2.cell(row=tot_row+3, column=1,
              value="* Columna 'Categ. OMS': borde inferior grueso color según categoría — "
                    "Ia=#7b0000  Ib=#e53e3e  II=#d69e2e  III=#3182ce  U=#38a169  NA=#888888")
n2.font = Font(size=7, italic=True, color="666666", name="Arial")
n2.alignment = Alignment(wrap_text=True, vertical="center")
ws2.row_dimensions[tot_row+3].height = 12

# ── Guardar ─────────────────────────────────────────────────────
out_path = os.path.join(os.path.dirname(__file__), "OA_plantilla_v5.xlsx")
wb.save(out_path)
print(f"✓  Generado: {out_path}")
