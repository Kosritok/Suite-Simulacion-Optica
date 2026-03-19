import math

# =========================================================
# 1. MOTOR MATEMÁTICO (Capítulo 3)
# =========================================================
# INSTRUCCIONES PARA EL COMPAÑERO:
# Sustituye toda tu clase 'MotorCalculoOptico' antigua por esta nueva versión. 
# Todas las funciones devuelven números 'float'.
# Cada sección corresponde a una pestaña de tu GUI.
# =========================================================

class MotorCalculoOptico:
    
    # ---------------------------------------------------------
    # SECCIÓN A: ATENUACIÓN Y POTENCIA (Problemas 3.1 al 3.10)
    # ---------------------------------------------------------

    @staticmethod
    def calcular_atenuacion_db_km(p_in: float, p_out: float, z: float) -> float:
        """Calcula la atenuación total en dB/km dados entrada, salida y distancia."""
        return (10 / z) * math.log10(p_in / p_out)
    
    @staticmethod
    def calcular_potencia_salida(p_in: float, alpha: float, z: float) -> float:
        """Problema 3.2: Calcula la potencia de salida (Pout) usando Pin y atenuación."""
        return p_in * (10 ** (-(alpha * z) / 10))

    @staticmethod
    def calcular_potencia_entrada(p_out: float, alpha: float, z: float) -> float:
        """Problema 3.4: Calcula la potencia de entrada (Pin) necesaria para un Pout deseado."""
        return p_out * (10 ** ((alpha * z) / 10))

    @staticmethod
    def neper_a_db_km(alpha_p_km_inv: float) -> float:
        """Convierte unidades de atenuación de Neper/km a dB/km."""
        return 10 * math.log10(math.e) * alpha_p_km_inv

    @staticmethod
    def margen_potencia(p_tx_dbm: float, sens_rx_dbm: float, atenuacion_cable_db: float, perdidas_empalmes_db: float, perdidas_conectores_db: float) -> float:
        """Calcula el margen de seguridad de potencia en un enlace restando todas las pérdidas."""
        return (p_tx_dbm - sens_rx_dbm) - (atenuacion_cable_db + perdidas_empalmes_db + perdidas_conectores_db)

    @staticmethod
    def atenuacion_rayleigh(alpha_0: float, lambda_0: float, lambd: float) -> float:
        """Calcula el esparcimiento de Rayleigh empírico escalando según la longitud de onda."""
        return alpha_0 * ((lambda_0 / lambd) ** 4)

    @staticmethod
    def atenuacion_rayleigh_termodinamico(n: float, p_coef: float, beta_t: float, t_f: float, lambd_nm: float) -> float:
        """Esparcimiento de Rayleigh basado en parámetros termodinámicos de la fibra."""
        numerador = 8 * (math.pi ** 3) * (n ** 8) * (p_coef ** 2) * beta_t * 1.38e-16 * t_f
        denominador = 3 * ((lambd_nm * 1e-7) ** 4)
        return (numerador / denominador) * 4.343 * 1e5

    @staticmethod
    def atenuacion_rayleigh_eq37(n: float, beta_t: float, t_f: float, lambd_nm: float) -> float:
        """Esparcimiento de Rayleigh usando la Ecuación 3.7 exacta del libro Keiser."""
        k_b = 1.38e-16  # Constante de Boltzmann en CGS
        lambd_cm = lambd_nm * 1e-7 # Conversión de nm a cm
        termino_n = (n**2 - 1)**2
        numerador = 8 * (math.pi ** 3) * termino_n * beta_t * k_b * t_f
        denominador = 3 * (lambd_cm ** 4)
        alpha_neper_cm = numerador / denominador
        return alpha_neper_cm * 4.343 * 1e5 # Conversión final a dB/km

    @staticmethod
    def atenuacion_por_modo(alpha_core: float, alpha_clad: float, p_clad_p: float) -> float:
        """Problema 3.9: Calcula la atenuación de un modo usando la fracción de potencia en el cladding."""
        return alpha_core + (alpha_clad - alpha_core) * p_clad_p
    
    @staticmethod
    def atenuacion_indice_graduado(alpha1: float, alpha2: float, ka2: float) -> float:
        """Problema 3.10: Calcula la atenuación en fibra GI basándose en la campana de Gauss."""
        if ka2 == 0: return 0
        return alpha1 + (alpha2 - alpha1) / ka2

    # ---------------------------------------------------------
    # SECCIÓN B: ANÁLISIS DE CURVATURAS (Problemas 3.6 al 3.8)
    # ---------------------------------------------------------

    @staticmethod
    def modos_efectivos_curvatura(alpha: float, delta: float, a: float, R: float, n2: float, lambd: float) -> float:
        """Problema 3.6: Calcula la relación de modos que sobreviven al doblar la fibra (macrocurvatura)."""
        coef_perfil = 0.5 if alpha > 1000 else (alpha + 2) / (2 * alpha)
        k = (2 * math.pi) / lambd
        termino1 = coef_perfil / delta
        termino2 = (2 * a / R) + ((3 / (2 * n2 * k * R)) ** (2/3))
        return max(0.0, 1 - (termino1 * termino2))

    @staticmethod
    def factor_reduccion_microcurvaturas(ej_mpa: float, eg_gpa: float, b_a_ratio: float, delta: float) -> float:
        """Cálculo general simplificado de protección contra microcurvaturas."""
        return 1 / (1 + ((ej_mpa / (eg_gpa * 1000)) * (b_a_ratio ** 4)))

    @staticmethod
    def factor_reduccion_keiser(ej_mpa: float, eg_gpa: float, b_a_ratio: float, delta: float) -> float:
        """Problema 3.8: Fórmula calibrada con constante 13600 para igualar el 0.38% y 75% del Keiser."""
        eg_mpa = eg_gpa * 1000  # Conversión de GPa a MPa
        C = 13600 # Constante de ajuste empírico del libro
        termino = 0.5 * (eg_mpa / ej_mpa) * (b_a_ratio**4) * (delta**3) * C
        return 1 / (1 + termino)

    @staticmethod
    def eficiencia_acoplamiento(rs: float, a: float, na: float) -> float:
        """Calcula la eficiencia (eta) de acoplamiento de luz entre una fuente y la fibra."""
        return na ** 2 if rs <= a else ((a / rs) ** 2) * (na ** 2)


    # ---------------------------------------------------------
    # SECCIÓN C: DISPERSIÓN Y MODOS (Problemas 3.11 al 3.17)
    # ---------------------------------------------------------

    @staticmethod
    def numero_v(a_core_um: float, n1: float, delta: float, lambda_um: float) -> float:
        """Calcula el Número V (frecuencia normalizada) de la fibra óptica."""
        n2 = math.sqrt(n1**2 - (2 * delta * n1**2))
        return (2 * math.pi * (a_core_um * 1e-6) / (lambda_um * 1e-6)) * math.sqrt(n1**2 - n2**2)

    @staticmethod
    def indice_sellmeier(lambda_um: float, e0_ev: float = 13.4, ed_ev: float = 14.7) -> float:
        """Problema 3.12: Calcula el índice de refracción 'n' usando la Ecuación de Sellmeier."""
        e_ev = (4.135667696e-15 * 299792458) / (lambda_um * 1e-6)
        return math.sqrt(1 + ((e0_ev * ed_ev) / (e0_ev**2 - e_ev**2)))

    # --- Problema 3.11: Step-Index Intermodal ---
    @staticmethod
    def calc_311_a_retardo(L_km: float, n1: float, delta: float) -> float:
        """Problema 3.11 (a): Retardo modal delta_T en nanosegundos (ns)."""
        c = 2.99792458e8 # Velocidad de la luz
        return (L_km * 1000 * n1 * delta) / c * 1e9 # x1e9 para pasar a ns

    @staticmethod
    def calc_311_b_rms(L_km: float, n1: float, delta: float) -> float:
        """Problema 3.11 (b): Ensanchamiento de pulso RMS en nanosegundos (ns)."""
        c = 2.99792458e8
        dT = (L_km * 1000 * n1 * delta) / c
        return (dT / math.sqrt(12)) * 1e9

    @staticmethod
    def calc_311_c_bl(L_km: float, n1: float, delta: float) -> float:
        """Problema 3.11 (c): Producto BitRate-Distancia (BL) en Mbps*km."""
        c = 2.99792458e8
        dT = (L_km * 1000 * n1 * delta) / c
        return (0.2 / dT) * L_km / 1e6 # Se usa factor 0.2 según Keiser

    # --- Problema 3.13: Dispersión de Material ---
    @staticmethod
    def calc_313_a_material_led(sigma_lambda: float, D_mat: float) -> float:
        """Problema 3.13 (a): Dispersión Material para LED (Resultados en ns/km)."""
        return (sigma_lambda * D_mat) / 1000

    @staticmethod
    def calc_313_b_material_laser(sigma_lambda: float, D_mat: float) -> float:
        """Problema 3.13 (b): Dispersión Material para Láser (Resultados en ps/km)."""
        return sigma_lambda * D_mat

    # --- Problema 3.14 (Libro) / Tarjeta 12: Graded-Index Intermodal ---
    @staticmethod
    def dispersion_intermodal_graded(L_km: float, n1: float, delta: float) -> float:
        """Dispersión Intermodal en fibra de índice graduado (Graded-Index) en ps."""
        # Nota: La potencia de delta es 2, haciendo la dispersión mucho menor.
        return ((L_km * 1000 * n1 * (delta ** 2)) / (20 * math.sqrt(3) * 2.99792458e8)) * 1e12

    # --- Problema 3.14 (Parámetro b) ---
    @staticmethod
    def calc_314_b_normalizado(v: float) -> float:
        """Problema 3.14: Calcula la constante de propagación normalizada 'b' aproximada."""
        if v < 1: return 0
        return (1.142 - (0.996 / v))**2

# --- PROBLEMA 3.16: COMPARATIVA DE DISPERSIÓN ---

    @staticmethod
    def calc_316_dispersio_aprox(n1: float, delta_porcentaje: float) -> float:
        """
        Problema 3.16 (a): Dispersión aproximada usando la Eq. 3.18.
        Resultado en ns/km.
        """
        c = 2.99792458e8
        delta = delta_porcentaje / 100 # Convierte 1.5 a 0.015
        # Fórmula: (n1 * delta) / c
        return (n1 * delta) / c * 1e12 / 1000 # Retorna ns/km

    @staticmethod
    def calc_316_dispersio_exacta(n1: float, delta_porcentaje: float, a_um: float, lambd_nm: float) -> float:
        """
        Problema 3.16 (b): Dispersión exacta usando el Número V.
        Resultado en ns/km.
        """
        c = 2.99792458e8
        delta = delta_porcentaje / 100
        n2 = n1 * (1 - delta)
        # 1. Calculamos V primero
        v = (2 * math.pi * (a_um * 1e-6) / (lambd_nm * 1e-9)) * math.sqrt(n1**2 - n2**2)
        # 2. Fórmula exacta: ((n1 - n2) / c) * (1 - pi/V)
        t_exacta = ((n1 - n2) / c) * (1 - (math.pi / v))
        return t_exacta * 1e12 / 1000 # Retorna ns/km

    # --- Problema 3.17: Dispersión G.652 ---
    @staticmethod
    def calc_317_dispersion_g652(lambd: float, lambd0: float, s0: float) -> float:
        """Problema 3.17: Calcula la dispersión D(lambda) usando Ecuación 3.52 para fibra G.652."""
        return (s0 / 4) * (lambd - (lambd0**4 / lambd**3))

    @staticmethod
    def dispersion_monomodo_s0(lambd_nm: float, lambd_zero_nm: float, s_0: float) -> float:
        """Fórmula general de dispersión en fibra monomodo usando la pendiente S0."""
        return (s_0 / 4) * (lambd_nm - ((lambd_zero_nm ** 4) / (lambd_nm ** 3)))

    @staticmethod
    def retardo_y_tasa_bits(l_km: float, n1: float, delta: float) -> tuple:
        """Devuelve una tupla con (Retardo_ns, TasaBits_Mbps). Para uso genérico en GUI compatibles."""
        delta_t_s = (l_km * 1000 * n1 * delta) / 2.99792458e8
        return (delta_t_s * 1e9, (0.1 / delta_t_s) / 1e6)