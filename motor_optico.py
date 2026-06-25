#Las fórmulas de esta sección que incluyen todo el módulo de motor de atenuación fueron extraídas por
#Issac Gómez y Óscar Rosas
#La programación de las mismas fue hecha entre los mismos dos integrantes
import math

class MotorCalculoOptico:
    @staticmethod
    def calcular_atenuacion_db_km(p_in: float, p_out: float, z: float) -> float:
        if p_in <= 0 or p_out <= 0 or z <= 0: raise ValueError("Las potencias y la distancia deben ser > 0.")
        return (10 / z) * math.log10(p_in / p_out)

#Fórmula expresada directamente

    @staticmethod
    def calcular_potencia_salida(p_in: float, alpha: float, z: float) -> float:
        return p_in * (10 ** (-(alpha * z) / 10))
    
#Fórmula expresada directamente

    @staticmethod
    def calcular_potencia_entrada(p_out: float, alpha: float, z: float) -> float:
        return p_out * (10 ** ((alpha * z) / 10))
    
#Fórmula expresada directamente

    @staticmethod
    def calcular_distancia_atenuacion(p_in: float, p_out: float, alpha: float) -> float:
        if alpha == 0: raise ValueError("La atenuación no puede ser cero al despejar distancia.")
        return (10 / alpha) * math.log10(p_in / p_out)
    
#Fórmula expresada directamente con una excepción directa ante el caso mencionado

    @staticmethod
    def eficiencia_acoplamiento(rs: float, a: float, na: float) -> float:
        if rs <= 0 or a <= 0 or na <= 0: raise ValueError("Los radios y NA deben ser > 0.")
        return na ** 2 if rs <= a else ((a / rs) ** 2) * (na ** 2)
    
#Condicionales expresados

    @staticmethod
    def atenuacion_rayleigh(alpha_0: float, lambda_0: float, lambd: float) -> float:
        if lambd <= 0: raise ValueError("La longitud de onda debe ser mayor a 0.")
        return alpha_0 * ((lambda_0 / lambd) ** 4)
    
#Fórmula expresada directamente con un caso específico de excepción

    @staticmethod
    def atenuacion_rayleigh_termodinamico(n: float, p_coef: float, beta_t: float, t_f: float, lambd_nm: float) -> float:
        numerador = 8 * (math.pi ** 3) * (n ** 8) * (p_coef ** 2) * beta_t * 1.38e-16 * t_f
        denominador = 3 * ((lambd_nm * 1e-7) ** 4)
        return (numerador / denominador) * 4.343 * 1e5

#Fórmula expresada directamente

    @staticmethod
    def atenuacion_rayleigh_eq37(n: float, beta_t: float, t_f: float, lambd_nm: float) -> float:
        lambd_cm = lambd_nm * 1e-7 
        termino_n = (n**2 - 1)**2
        numerador = 8 * (math.pi ** 3) * termino_n * beta_t * 1.38e-16 * t_f
        return (numerador / (3 * (lambd_cm ** 4))) * 4.343 * 1e5 
    
#Fórmula expresada directamente

    @staticmethod
    def atenuacion_por_modo(alpha_core: float, alpha_clad: float, p_clad_p: float) -> float:
        return alpha_core + (alpha_clad - alpha_core) * p_clad_p
    
#Fórmula expresada directamente
    
    @staticmethod
    def atenuacion_indice_graduado(alpha1: float, alpha2: float, ka2: float) -> float:
        return 0 if ka2 == 0 else alpha1 + (alpha2 - alpha1) / ka2
    
#Fórmula expresada directamente

    @staticmethod
    def modos_efectivos_curvatura(alpha: float, delta: float, a: float, R: float, n2: float, lambd: float) -> float:
        coef_perfil = 0.5 if alpha > 1000 else (alpha + 2) / (2 * alpha)
        k = (2 * math.pi) / lambd
        termino2 = (2 * a / R) + ((3 / (2 * n2 * k * R)) ** (2/3))
        return max(0.0, 1 - ((coef_perfil / delta) * termino2))
    
#Fórmula expresada directamente

    @staticmethod
    def factor_reduccion_microcurvaturas(ej_mpa: float, eg_gpa: float, b_a_ratio: float, delta: float) -> float:
        return 1 / (1 + ((ej_mpa / (eg_gpa * 1000)) * (b_a_ratio ** 4)))
    
#Fórmula expresada directamente

    @staticmethod
    def factor_reduccion_keiser(ej_mpa: float, eg_gpa: float, b_a_ratio: float, delta: float) -> float:
        termino = 0.5 * ((eg_gpa * 1000) / ej_mpa) * (b_a_ratio**4) * (delta**3) * 13600
        return 1 / (1 + termino)
    
#Fórmula expresada directamente

    @staticmethod
    def numero_v(a_core_um: float, n1: float, delta: float, lambda_um: float) -> float:
        n2 = math.sqrt(n1**2 - (2 * delta * n1**2))
        return (2 * math.pi * (a_core_um * 1e-6) / (lambda_um * 1e-6)) * math.sqrt(n1**2 - n2**2)
    
#Fórmula expresada directamente

    @staticmethod
    def indice_sellmeier(lambda_um: float, e0_ev: float = 13.4, ed_ev: float = 14.7) -> float:
        e_ev = (4.135667696e-15 * 299792458) / (lambda_um * 1e-6)
        return math.sqrt(1 + ((e0_ev * ed_ev) / (e0_ev**2 - e_ev**2)))
    
#Fórmula expresada directamente

    @staticmethod
    def calc_311_a_retardo(L_km: float, n1: float, delta: float) -> float:
        return (L_km * 1000 * n1 * delta) / 2.99792458e8 * 1e9
    
#Fórmula expresada directamente

    @staticmethod
    def calc_311_b_rms(L_km: float, n1: float, delta: float) -> float:
        return (((L_km * 1000 * n1 * delta) / 2.99792458e8) / math.sqrt(12)) * 1e9
    
#Fórmula expresada directamente

    @staticmethod
    def calc_311_c_bl(L_km: float, n1: float, delta: float) -> float:
        dT = (L_km * 1000 * n1 * delta) / 2.99792458e8
        return (0.2 / dT) * L_km / 1e6
    
#Fórmula expresada directamente

    @staticmethod
    def calc_313_a_material_led(sigma_lambda: float, D_mat: float) -> float:
        return (sigma_lambda * D_mat) / 1000
    
#Fórmula expresada directamente

    @staticmethod
    def calc_313_b_material_laser(sigma_lambda: float, D_mat: float) -> float:
        return sigma_lambda * D_mat
    
#Fórmula expresada directamente

    @staticmethod
    def dispersion_intermodal_graded(L_km: float, n1: float, delta: float) -> float:
        return ((L_km * 1000 * n1 * (delta ** 2)) / (20 * math.sqrt(3) * 2.99792458e8)) * 1e12
    
#Fórmula expresada directamente

    @staticmethod
    def calc_314_b_normalizado(v: float) -> float:
        return 0 if v < 1 else (1.142 - (0.996 / v))**2
    
#Fórmula expresada directamente

    @staticmethod
    def calc_316_dispersio_aprox(n1: float, delta_porcentaje: float) -> float:
        return (n1 * (delta_porcentaje / 100)) / 2.99792458e8 * 1e12 / 1000 
    
#Fórmula expresada directamente

    @staticmethod
    def calc_316_dispersio_exacta(n1: float, delta_porcentaje: float, a_um: float, lambd_nm: float) -> float:
        delta = delta_porcentaje / 100
        n2 = n1 * (1 - delta)
        v = (2 * math.pi * (a_um * 1e-6) / (lambd_nm * 1e-9)) * math.sqrt(n1**2 - n2**2)
        return (((n1 - n2) / 2.99792458e8) * (1 - (math.pi / v))) * 1e12 / 1000 
    
#Fórmula expresada directamente

    @staticmethod
    def calc_317_dispersion_g652(lambd: float, lambd0: float, s0: float) -> float:
        return (s0 / 4) * (lambd - (lambd0**4 / lambd**3))
    
#Fórmula expresada directamente