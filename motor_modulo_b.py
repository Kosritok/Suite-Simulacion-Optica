#Las fórmulas de esta sección que incluyen todo el módulo de motor matemático fueron extraídas por
#Emilio y Germán
#La programación del módulo fue hecha por Óscar Rosas
import math

class MotorModuloB:

    # 1. FRECUENCIA NORMALIZADA (V)

    @staticmethod
    def frecuencia_normalizada_v(a: float, lam: float, an: float) -> float:
        """V = (2 * pi * a / lam) * AN"""
        return (2 * math.pi * a / lam) * an

#Fórmula expresada directamente

    @staticmethod
    def v_inverso_a(v: float, lam: float, an: float) -> float:
        """Despeja el radio del núcleo (a)."""
        return (v * lam) / (2 * math.pi * an)

#Fórmula expresada directamente

    @staticmethod
    def v_inverso_lam(v: float, a: float, an: float) -> float:
        """Despeja la longitud de onda (lam)."""
        return (2 * math.pi * a * an) / v

#Fórmula expresada directamente

    @staticmethod
    def v_inverso_an(v: float, a: float, lam: float) -> float:
        """Despeja la apertura numérica (AN)."""
        return (v * lam) / (2 * math.pi * a)
    
#Fórmula expresada directamente

    # 2. NÚMERO DE MODOS (M)

    @staticmethod
    def modos_step_index(v: float) -> float:
        """M ≈ V^2 / 2 para fibras de salto de índice."""
        return (v**2) / 2
    
#Fórmula expresada directamente

    @staticmethod
    def modos_graded_index(v: float) -> float:
        """M ≈ V^2 / 4 para fibras de índice gradual."""
        return (v**2) / 4

#Fórmula expresada directamente


    # 3. LONGITUD DE ONDA DE CORTE

    @staticmethod
    def longitud_corte(a: float, an: float) -> float:
        """lambda_c = (2 * pi * a * AN) / 2.4048"""
        return (2 * math.pi * a * an) / 2.4048
    
#Fórmula expresada directamente 

    @staticmethod
    def longitud_corte_inverso_a(lam_c: float, an: float) -> float:
        """Despeja el radio (a) desde la longitud de corte."""
        return (lam_c * 2.4048) / (2 * math.pi * an)

#Fórmula expresada directamente

    @staticmethod
    def longitud_corte_inverso_an(lam_c: float, a: float) -> float:
        """Despeja la Apertura Numérica (AN) desde la longitud de corte."""
        return (lam_c * 2.4048) / (2 * math.pi * a)
    
#Fórmula expresada directamente


    # 4. DIÁMETRO DE CAMPO MODAL (MFD)

    @staticmethod
    def mfd_marcuse(a: float, v: float) -> float:
        """Calcula el MFD (2 * omega_0) basado en la aproximación de Marcuse."""
        if v <= 0: 
            return 0.0
        # Fórmula: 2 * omega_0 ≈ 2a(0.65 + 1.619/V^1.5 + 2.879/V^6)
        return 2 * a * (0.65 + (1.619 / (v**1.5)) + (2.879 / (v**6)))
    
#Fórmula expresada directamente con un caso específico de excepción