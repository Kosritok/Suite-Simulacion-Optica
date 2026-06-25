#Las fórmulas de esta sección que incluyen todo el módulo de motor de dispersión fueron extraídas por
#Patricia y Margarita
#La programación del módulo fue hecha por Óscar Rosas
import math

class MotorModuloA:
    C = 3e8 

    # --- GEOMÉTRICA Y SNELL ---
    @staticmethod
    def indice_refraccion(v: float) -> float:
        if v <= 0: raise ValueError("La velocidad en el medio debe ser > 0.")
        return MotorModuloA.C / v

#Fórmula expresada directamente con una excepción directa ante el caso mencionado

    @staticmethod
    def velocidad_medio(n: float) -> float:
        if n <= 0: raise ValueError("El índice debe ser > 0.")
        return MotorModuloA.C / n

#Fórmula expresada directamente con una excepción directa ante el caso mencionado

    @staticmethod
    def angulo_refraccion_snell(n1: float, n2: float, theta1_grados: float) -> float:
        theta1_rad = math.radians(theta1_grados)
        seno_theta2 = (n1 / n2) * math.sin(theta1_rad)
        if abs(seno_theta2) > 1.0: raise ValueError("Reflexión interna total.")
        return math.degrees(math.asin(seno_theta2))

#Fórmula expresada directamente con una excepción directa ante el caso mencionado

    @staticmethod
    def snell_inverso_n1(n2: float, theta1: float, theta2: float) -> float:
        t1, t2 = math.radians(theta1), math.radians(theta2)
        if math.sin(t1) == 0: raise ValueError("El ángulo de incidencia no puede ser 0.")
        return n2 * math.sin(t2) / math.sin(t1)

#Fórmula expresada directamente con una excepción directa ante el caso mencionado

    @staticmethod
    def snell_inverso_n2(n1: float, theta1: float, theta2: float) -> float:
        t1, t2 = math.radians(theta1), math.radians(theta2)
        if math.sin(t2) == 0: raise ValueError("El ángulo de refracción no puede ser 0.")
        return n1 * math.sin(t1) / math.sin(t2)

#Fórmula expresada directamente con una excepción directa ante el caso mencionado

    @staticmethod
    def snell_inverso_theta1(n1: float, n2: float, theta2: float) -> float:
        val = (n2 / n1) * math.sin(math.radians(theta2))
        if abs(val) > 1.0: raise ValueError("Sin solución real.")
        return math.degrees(math.asin(val))

#Fórmula expresada directamente con una excepción directa ante el caso mencionado

    @staticmethod
    def angulo_critico(n1: float, n2: float) -> float:
        if n1 <= n2: raise ValueError("n1 debe ser > n2.")
        return math.degrees(math.asin(n2 / n1))

#Fórmula expresada directamente con una excepción directa ante el caso mencionado

    @staticmethod
    def diferencia_indice_relativa(n1: float, n2: float) -> float:
        return (n1 - n2) / n1

#Fórmula expresada directamente

    @staticmethod
    def apertura_numerica(n1: float, n2: float) -> float:
        if n1 < n2: raise ValueError("n1 debe ser >= n2.")
        return math.sqrt((n1 ** 2) - (n2 ** 2))

#Fórmula expresada directamente con una excepción directa ante el caso mencionado

    # --- NÚMERO V Y MODOS (Nuevas Inversas) ---
    @staticmethod
    def frecuencia_normalizada_v(a: float, lam: float, na: float) -> float:
        if lam <= 0: raise ValueError("La longitud de onda debe ser > 0.")
        return (2 * math.pi * a / lam) * na

#Fórmula expresada directamente con una excepción directa ante el caso mencionado

    @staticmethod
    def v_inverso_a(v: float, lam: float, na: float) -> float:
        if na <= 0: raise ValueError("NA debe ser > 0.")
        return (v * lam) / (2 * math.pi * na)

#Fórmula expresada directamente con una excepción directa ante el caso mencionado

    @staticmethod
    def v_inverso_lam(v: float, a: float, na: float) -> float:
        if v <= 0: raise ValueError("V debe ser > 0.")
        return (2 * math.pi * a * na) / v

#Fórmula expresada directamente con una excepción directa ante el caso mencionado

    @staticmethod
    def v_inverso_na(v: float, a: float, lam: float) -> float:
        if a <= 0: raise ValueError("El radio 'a' debe ser > 0.")
        return (v * lam) / (2 * math.pi * a)

#Fórmula expresada directamente con una excepción directa ante el caso mencionado

    @staticmethod
    def modos_guiados_escalonado(v: float) -> int:
        return math.floor((v ** 2) / 2)

#Fórmula expresada directamente 

    @staticmethod
    def modos_guiados_gradual(v: float, alpha: float) -> int:
        return math.floor((alpha / (alpha + 2)) * ((v ** 2) / 2))

#Fórmula expresada directamente

    @staticmethod
    def radio_campo_modal(a: float, v: float) -> float:
        if v <= 0: raise ValueError("El número V debe ser > 0.")
        return a * (0.65 + (1.619 * (v ** -1.5)) + (2.879 * (v ** -6)))
    
#Fórmula expresada directamente con una excepción directa ante el caso mencionado

    # --- DISPERSIÓN Y RETARDOS (Nuevas Inversas) ---
    @staticmethod
    def retardo_modal_escalonado(l_metros: float, n1: float, delta: float) -> float:
        return (l_metros * n1 * delta) / MotorModuloA.C

#Fórmula expresada directamente

    @staticmethod
    def retardo_inverso_l(dt: float, n1: float, delta: float) -> float:
        if n1 <= 0 or delta <= 0: raise ValueError("n1 y delta deben ser > 0.")
        return (dt * MotorModuloA.C) / (n1 * delta)

#Fórmula expresada directamente con una excepción directa ante el caso mencionado

    @staticmethod
    def retardo_inverso_n1(dt: float, l_metros: float, delta: float) -> float:
        if l_metros <= 0 or delta <= 0: raise ValueError("L y delta deben ser > 0.")
        return (dt * MotorModuloA.C) / (l_metros * delta)

#Fórmula expresada directamente con una excepción directa ante el caso mencionado

    @staticmethod
    def retardo_inverso_delta(dt: float, l_metros: float, n1: float) -> float:
        if l_metros <= 0 or n1 <= 0: raise ValueError("L y n1 deben ser > 0.")
        return (dt * MotorModuloA.C) / (l_metros * n1)

#Fórmula expresada directamente con una excepción directa ante el caso mencionado

    @staticmethod
    def ensanchamiento_total(d_lambda: float, l_km: float, sigma_lambda: float) -> float:
        return abs(d_lambda * l_km * sigma_lambda)

#Fórmula expresada directamente

    @staticmethod
    def ensanchamiento_inverso_l(sigma_total: float, d_lambda: float, sigma_lambda: float) -> float:
        if d_lambda == 0 or sigma_lambda == 0: raise ValueError("D y ancho espectral deben ser != 0.")
        return abs(sigma_total / (d_lambda * sigma_lambda))

#Fórmula expresada directamente con una excepción directa ante el caso mencionado

    @staticmethod
    def dispersion_polarizacion_pmd(d_pmd: float, l_km: float) -> float:
        if l_km < 0: raise ValueError("La longitud no puede ser negativa.")
        return d_pmd * math.sqrt(l_km)
    
    #Fórmula expresada directamente con una excepción directa ante el caso mencionado