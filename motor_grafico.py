import numpy as np
import matplotlib
matplotlib.use('agg')  # <--- SOLUCIÓN AL ERROR (Renderizado en memoria)
import matplotlib.pyplot as plt

class MotorGrafico:
    @staticmethod
    def configurar_grafica(titulo, xlabel, ylabel):
        fig, ax = plt.subplots(figsize=(4.5, 2.5), facecolor='#2B2B2B')
        fig.subplots_adjust(left=0.15, right=0.95, top=0.85, bottom=0.25)
        ax.set_facecolor('#212121')
        ax.tick_params(colors='white', labelsize=8)
        ax.set_title(titulo, color='#d4af37', fontsize=11, fontweight='bold')
        ax.set_xlabel(xlabel, color='gray', fontsize=9)
        ax.set_ylabel(ylabel, color='gray', fontsize=9)
        for spine in ax.spines.values():
            spine.set_edgecolor('#555555')
        ax.grid(color='#444444', linestyle=':', linewidth=0.5)
        return fig, ax

    @staticmethod
    def plot_atenuacion(pin, alpha, z_max):
        fig, ax = MotorGrafico.configurar_grafica("Decaimiento de Potencia", "Distancia (km)", "Potencia (mW/µW)")
        distancias = np.linspace(0, max(z_max, 1.0), 100)
        potencias = pin * (10 ** (-(alpha * distancias) / 10))
        ax.plot(distancias, potencias, color='#66bb6a', linewidth=2)
        ax.fill_between(distancias, potencias, color='#66bb6a', alpha=0.1)
        return fig

    @staticmethod
    def plot_presupuesto(tx, rx, cable, empalmes, conectores):
        fig, ax = MotorGrafico.configurar_grafica("Caída del Presupuesto", "Componentes del Enlace", "Potencia (dBm)")
        etiquetas = ['Tx', 'Cable', 'Empalmes', 'Conect', 'Rx Ideal']
        valores = [tx, tx - cable, tx - cable - empalmes, tx - cable - empalmes - conectores, rx]
        ax.step(range(len(etiquetas)), valores, where='mid', color='#64b5f6', linewidth=2, marker='o')
        ax.set_xticks(range(len(etiquetas)))
        ax.set_xticklabels(etiquetas, rotation=15, ha='right', fontsize=7)
        ax.axhline(y=rx, color='#ff5555', linestyle='--', linewidth=1.5, label='Límite Rx')
        ax.legend(facecolor='#2B2B2B', edgecolor='none', labelcolor='white', fontsize=7)
        return fig

    @staticmethod
    def plot_rayleigh(lam_op):
        fig, ax = MotorGrafico.configurar_grafica("Dispersión Rayleigh", "Longitud de onda (nm)", "Atenuación (dB/km)")
        lams = np.linspace(800, 1600, 100)
        atenuaciones = 1.0 / (lams / 1000)**4
        ax.plot(lams, atenuaciones, color='#ab47bc', linewidth=2)
        ax.axvline(x=lam_op, color='#d4af37', linestyle='--', linewidth=1.5, label=f'Operación: {lam_op} nm')
        ax.legend(facecolor='#2B2B2B', edgecolor='none', labelcolor='white', fontsize=7)
        return fig

    @staticmethod
    def plot_g652(lam_0, s0):
        fig, ax = MotorGrafico.configurar_grafica("Dispersión Cromática G.652", "Longitud de onda (nm)", "D (ps/nm·km)")
        lams = np.linspace(1200, 1600, 100)
        dispersiones = (s0 / 4) * (lams - (lam_0**4 / lams**3))
        ax.plot(lams, dispersiones, color='#64b5f6', linewidth=2)
        ax.axhline(y=0, color='gray', linestyle='--')
        ax.axvline(x=lam_0, color='#d4af37', linestyle=':', label=f'Disp. Cero ({lam_0} nm)')
        ax.legend(facecolor='#2B2B2B', edgecolor='none', labelcolor='white', fontsize=7)
        return fig

    @staticmethod
    def plot_ensanchamiento(sigma_total):
        fig, ax = MotorGrafico.configurar_grafica("Ensanchamiento de Pulso", "Tiempo (ps)", "Amplitud Relativa")
        t = np.linspace(-3*sigma_total, 3*sigma_total, 200)
        if sigma_total == 0: sigma_total = 1e-9 
        pulso_in = np.exp(- (t**2) / (2 * (sigma_total/3)**2))
        pulso_out = np.exp(- (t**2) / (2 * sigma_total**2))
        ax.plot(t, pulso_in, color='#64b5f6', linestyle='--', label='Entrada')
        ax.plot(t, pulso_out, color='#ff5555', linewidth=2, label='Salida')
        ax.fill_between(t, pulso_out, color='#ff5555', alpha=0.1)
        ax.legend(facecolor='#2B2B2B', edgecolor='none', labelcolor='white', fontsize=7)
        return fig

    @staticmethod
    def plot_snell(n1, n2, theta1, theta2):
        fig, ax = MotorGrafico.configurar_grafica("Refracción de Snell", "Frontera (x)", "Normal (y)")
        ax.axhline(y=0, color='#d4af37', linewidth=2)
        ax.axvline(x=0, color='gray', linestyle='--')
        rad1 = np.radians(theta1)
        x1, y1 = -np.sin(rad1), np.cos(rad1)
        ax.plot([x1, 0], [y1, 0], color='#ff5555', linewidth=2, label='Incidente')
        
        rad2 = np.radians(theta2)
        if n1 > n2 and theta1 >= np.degrees(np.arcsin(n2/n1)):
            x2, y2 = np.sin(rad1), np.cos(rad1)
            ax.plot([0, x2], [0, y2], color='#ff5555', linewidth=2, linestyle=':', label='RTI')
        else:
            x2, y2 = np.sin(rad2), -np.cos(rad2)
            ax.plot([0, x2], [0, y2], color='#64b5f6', linewidth=2, label='Refractado')
            
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect('equal')
        ax.legend(facecolor='#2B2B2B', edgecolor='none', labelcolor='white', fontsize=7)
        return fig

    @staticmethod
    def plot_numero_v(a, lam_um, na):
        fig, ax = MotorGrafico.configurar_grafica("Análisis de Modos (Frecuencia V)", "Longitud de onda (µm)", "Número V")
        lambdas = np.linspace(max(0.1, lam_um - 0.5), lam_um + 0.5, 100)
        vs = (2 * np.pi * a / lambdas) * na
        ax.plot(lambdas, vs, color='#64b5f6', linewidth=2)
        
        v_op = (2 * np.pi * a / lam_um) * na
        ax.plot(lam_um, v_op, marker='o', markersize=6, color='white')
        ax.axvline(x=lam_um, color='gray', linestyle=':')
        
        ax.axhline(y=2.4048, color='#ff5555', linestyle='--', label='Corte Monomodo (2.4048)')
        ax.legend(facecolor='#2B2B2B', edgecolor='none', labelcolor='white', fontsize=7)
        return fig

    @staticmethod
    def plot_corte(lam_c_um, a, an):
        fig, ax = MotorGrafico.configurar_grafica("Condición de Corte Monomodo", "Longitud de Onda (µm)", "Número V")
        lambdas = np.linspace(max(0.1, lam_c_um - 1.0), lam_c_um + 1.0, 100)
        vs = (2 * np.pi * a * an) / lambdas
        
        ax.plot(lambdas, vs, color='#64b5f6', linewidth=2)
        ax.axhline(y=2.4048, color='#d4af37', linestyle='--', linewidth=1.5, label='V = 2.4048')
        ax.axvline(x=lam_c_um, color='#ff5555', linestyle=':', label=f'λ Corte: {lam_c_um*1000:.1f} nm')
        
        ax.fill_between(lambdas, 0, np.max(vs), where=(lambdas >= lam_c_um), color='#66bb6a', alpha=0.1, label='Monomodo')
        ax.fill_between(lambdas, 0, np.max(vs), where=(lambdas < lam_c_um), color='#ff5555', alpha=0.1, label='Multimodo')
        
        ax.set_ylim(0, np.max(vs))
        ax.legend(facecolor='#2B2B2B', edgecolor='none', labelcolor='white', fontsize=7)
        return fig

    @staticmethod
    def plot_mfd(a_um, mfd):
        fig, ax = MotorGrafico.configurar_grafica("Distribución del Campo Modal", "Radio transversal (µm)", "Intensidad I(r)")
        w0 = mfd / 2.0
        r = np.linspace(-3*a_um, 3*a_um, 200)
        
        intensidad = np.exp(-2 * (r**2) / (w0**2))
        ax.plot(r, intensidad, color='#66bb6a', linewidth=2, label='Intensidad Óptica')
        
        ax.axvline(x=a_um, color='gray', linestyle='--')
        ax.axvline(x=-a_um, color='gray', linestyle='--')
        ax.fill_between(r, 0, intensidad, where=(abs(r) <= a_um), color='#64b5f6', alpha=0.3, label='Núcleo (2a)')
        ax.fill_between(r, 0, intensidad, where=(abs(r) > a_um), color='#ff5555', alpha=0.3, label='Revestimiento')
        
        ax.axvline(x=w0, color='#d4af37', linestyle=':')
        ax.axvline(x=-w0, color='#d4af37', linestyle=':', label='MFD (2ω₀)')
        
        ax.legend(facecolor='#2B2B2B', edgecolor='none', labelcolor='white', fontsize=7)
        return fig