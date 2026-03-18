import math

class MotorCalculoOptico:
    """
    Motor matemático para cálculos de fibra óptica.
    Diseñado para recibir entradas (inputs) de una interfaz gráfica
    y retornar los resultados procesados.
    """

    # ==========================================
    # 1. ATENUACIÓN Y POTENCIA
    # ==========================================
    @staticmethod
    def calcular_atenuacion_db_km(p_in: float, p_out: float, z: float) -> float:
        """
        Calcula el coeficiente de atenuación (α) en dB/km.
        """
        if p_in <= 0 or p_out <= 0 or z <= 0:
            raise ValueError("Las potencias y la distancia deben ser > 0.")
        return (10 / z) * math.log10(p_in / p_out)

    # ==========================================
    # 2. EFICIENCIA DE ACOPLAMIENTO
    # ==========================================
    @staticmethod
    def eficiencia_acoplamiento(rs: float, a: float, na: float) -> float:
        """
        Calcula la eficiencia máxima de acoplamiento (η) de una fuente a una fibra.
        """
        if rs <= 0 or a <= 0 or na <= 0:
            raise ValueError("Los radios y la apertura numérica deben ser > 0.")
        
        if rs <= a:
            return na ** 2
        else:
            return ((a / rs) ** 2) * (na ** 2)

    # ==========================================
    # 3. PRESUPUESTO DE POTENCIA
    # ==========================================
    @staticmethod
    def margen_potencia(p_tx_dbm: float, sens_rx_dbm: float, atenuacion_cable_db: float, 
                        perdidas_empalmes_db: float, perdidas_conectores_db: float) -> float:
        """
        Calcula el margen de potencia operativo de un enlace completo.
        """
        perdida_permitida = p_tx_dbm - sens_rx_dbm
        perdidas_totales = atenuacion_cable_db + perdidas_empalmes_db + perdidas_conectores_db
        return perdida_permitida - perdidas_totales