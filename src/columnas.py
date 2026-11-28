"""Clasificación de las 126 columnas de concentradohogar (ENIGH 2024) para evitar leakage.

Etiqueta: gasto catastrófico = salud / (ing_cor - ali_dentro) > 0.30
Regla del equipo: el ingreso NO se usa como predictor.

Fuente de las definiciones: Catálogo ENIGH 2024, tabla CONCENTRADOHOGAR (pág. 215 en adelante).
"""

# 1) Identificadores y diseño muestral: no son predictores.
#    (entidad se puede derivar de folioviv[:2] si se quiere como variable categórica)
ID_DISENO = ["folioviv", "foliohog", "ubica_geo", "upm", "est_dis", "factor"]

# 2) Constantes: sin varianza (smg vale 22403.70 en todos los registros).
CONSTANTES = ["smg"]

# 3) Insumos directos de la etiqueta: PROHIBIDAS como predictores.
#    - Numerador: salud y sus tres componentes.
#    - Denominador: ing_cor (y todos sus componentes) y ali_dentro (y sus componentes).
INSUMOS_ETIQUETA = [
    # numerador
    "salud", "ambul_serv", "aten_hosp", "medic_prod",
    # ing_cor = ingtrab + rentas + transfer + estim_alqu + otros_ing
    "ing_cor", "ingtrab", "trabajo", "sueldos", "horas_extr", "comisiones",
    "aguinaldo", "indemtrab", "otra_rem", "remu_espec", "negocio", "noagrop",
    "industria", "comercio", "servicios", "agrope", "agricolas", "pecuarios",
    "reproducc", "pesca", "otros_trab", "rentas", "utilidad", "arrenda",
    "transfer", "jubilacion", "becas", "donativos", "remesas", "bene_gob",
    "transf_hog", "trans_inst", "estim_alqu", "otros_ing",
    # ali_dentro = cereales + carnes + ... + otros_alim + bebidas
    "ali_dentro", "cereales", "carnes", "pescado", "leche", "huevo", "aceites",
    "tuberculo", "verduras", "frutas", "azucar", "cafe", "especias",
    "otros_alim", "bebidas",
]

# 4) Contienen insumos por construcción (parte-todo): PROHIBIDAS.
#    gasto_mon incluye salud; alimentos incluye ali_dentro.
CONTIENEN_INSUMOS = ["gasto_mon", "alimentos"]

# 5) Gasto y flujos financieros: no son insumo directo de la etiqueta, pero son
#    proxies de la capacidad económica del hogar (equivalen a "ingreso por otra vía")
#    y no serían observables al focalizar. RECOMENDADO excluir (decisión del equipo).
PROXIES_ECONOMICOS = [
    "ali_fuera", "tabaco", "vesti_calz", "vestido", "calzado", "vivienda",
    "alquiler", "pred_cons", "agua", "energia", "limpieza", "cuidados",
    "utensilios", "enseres", "transporte", "publico", "foraneo", "adqui_vehi",
    "mantenim", "refaccion", "combus", "comunica", "educa_espa", "educacion",
    "esparci", "paq_turist", "personales", "cuida_pers", "acces_pers",
    "otros_gas", "transf_gas",
    "percep_tot", "retiro_inv", "prestamos", "otras_perc", "ero_nm_viv",
    "ero_nm_hog", "erogac_tot", "cuota_viv", "mater_serv", "material",
    "servicio", "deposito", "prest_terc", "pago_tarje", "deudas", "balance",
    "otras_erog",
]

# 6) Candidatas a predictores: características del hogar y su jefatura.
CANDIDATAS = [
    "tam_loc", "est_socio", "clase_hog", "sexo_jefe", "edad_jefe", "educa_jefe",
    "tot_integ", "hombres", "mujeres", "mayores", "menores", "p12_64", "p65mas",
    "ocupados", "percep_ing", "perc_ocupa",
]

PROHIBIDAS = INSUMOS_ETIQUETA + CONTIENEN_INSUMOS


def verificar_cobertura(columnas):
    """Comprueba que cada columna del DataFrame esté en exactamente un grupo."""
    grupos = [ID_DISENO, CONSTANTES, INSUMOS_ETIQUETA, CONTIENEN_INSUMOS,
              PROXIES_ECONOMICOS, CANDIDATAS]
    asignadas = [c for g in grupos for c in g]
    repetidas = {c for c in asignadas if asignadas.count(c) > 1}
    sin_grupo = set(columnas) - set(asignadas)
    inexistentes = set(asignadas) - set(columnas)
    assert not repetidas, f"En más de un grupo: {repetidas}"
    assert not sin_grupo, f"Sin clasificar: {sin_grupo}"
    assert not inexistentes, f"No existen en la base: {inexistentes}"