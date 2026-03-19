import math

class MotorModuloA:
    """
    Motor matemático para el Módulo A (Óptica Geométrica y Dispersión).
    Contiene las fórmulas de los Capítulos 2 y 3.
    """
    
    # Velocidad de la luz en el vacío (m/s)
    C = 3e8 

    # ==========================================
    # 1. ESTRUCTURAS DE LA FIBRA Y ÓPTICA GEOMÉTRICA
    # ==========================================

    @staticmethod
    def indice_refraccion(v: float) -> float:
        """Calcula el índice de refracción (n)."""
        if v <= 0:
            raise ValueError("La velocidad en el medio debe ser > 0.")
        return MotorModuloA.C / v

    @staticmethod
    def angulo_refraccion_snell(n1: float, n2: float, theta1_grados: float) -> float:
        """
        Calcula el ángulo de refracción (theta2) usando la Ley de Snell.
        Retorna el ángulo en grados.
        """
        theta1_rad = math.radians(theta1_grados)
        seno_theta2 = (n1 / n2) * math.sin(theta1_rad)
        if seno_theta2 > 1.0 or seno_theta2 < -1.0:
            raise ValueError("Reflexión interna total (no hay refracción).")
        return math.degrees(math.asin(seno_theta2))

    @staticmethod
    def angulo_critico(n1: float, n2: float) -> float:
        """Calcula el ángulo crítico para la reflexión interna total en grados."""
        if n1 <= n2:
            raise ValueError("n1 debe ser mayor que n2 para que exista un ángulo crítico.")
        return math.degrees(math.asin(n2 / n1))

    @staticmethod
    def diferencia_indice_relativa(n1: float, n2: float) -> float:
        """Calcula la diferencia de índice relativa (Delta)."""
        return (n1 - n2) / n1

    @staticmethod
    def apertura_numerica(n1: float, n2: float) -> float:
        """Calcula la Apertura Numérica (NA) exacta."""
        if n1 < n2:
            raise ValueError("n1 debe ser mayor o igual a n2.")
        return math.sqrt((n1 ** 2) - (n2 ** 2))

    # ==========================================
    # 2. MODOS DE PROPAGACIÓN Y PARÁMETROS DE DISEÑO
    # ==========================================

    @staticmethod
    def frecuencia_normalizada_v(a: float, lam: float, na: float) -> float:
        """Calcula la Frecuencia Normalizada (Número V)."""
        if lam <= 0:
            raise ValueError("La longitud de onda debe ser > 0.")
        return (2 * math.pi * a / lam) * na

    @staticmethod
    def modos_guiados_escalonado(v: float) -> int:
        """Calcula el número aproximado de modos en fibra de índice escalonado."""
        return math.floor((v ** 2) / 2)

    @staticmethod
    def modos_guiados_gradual(v: float, alpha: float) -> int:
        """Calcula el número aproximado de modos en fibra de índice gradual."""
        return math.floor((alpha / (alpha + 2)) * ((v ** 2) / 2))

    @staticmethod
    def radio_campo_modal(a: float, v: float) -> float:
        """
        Calcula el Radio del campo modal (Spot Size w0) para fibras monomodo.
        Válido típicamente para V entre 1.2 y 2.4.
        """
        if v <= 0:
            raise ValueError("El número V debe ser > 0.")
        factor = 0.65 + (1.619 * (v ** -1.5)) + (2.879 * (v ** -6))
        return a * factor

    # ==========================================
    # 3. DISPERSIÓN DE LA SEÑAL Y RETARDOS
    # ==========================================

    @staticmethod
    def retardo_modal_escalonado(l_metros: float, n1: float, delta: float) -> float:
        """Calcula el Retardo Modal para una fibra de índice escalonado en segundos."""
        return (l_metros * n1 * delta) / MotorModuloA.C

    @staticmethod
    def ensanchamiento_total(d_lambda: float, l_km: float, sigma_lambda: float) -> float:
        """
        Calcula el ensanchamiento total del pulso (Dispersión Cromática) en ps.
        D_lambda: Dispersión en ps/(nm*km)
        """
        return abs(d_lambda * l_km * sigma_lambda)

    @staticmethod
    def dispersion_polarizacion_pmd(d_pmd: float, l_km: float) -> float:
        """
        Calcula la Dispersión por Modo de Polarización (PMD).
        D_pmd: Coeficiente típico en ps/sqrt(km)
        """
        if l_km < 0:
            raise ValueError("La longitud no puede ser negativa.")
        return d_pmd * math.sqrt(l_km)