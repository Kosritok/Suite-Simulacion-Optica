import numpy as np
import matplotlib
matplotlib.use('TkAgg')
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
        ax.plot(distancias, potencias, color='#64b5f6', linewidth=2)
        ax.fill_between(distancias, potencias, color='#64b5f6', alpha=0.1)
        return fig

    @staticmethod
    def plot_presupuesto(tx, rx, cab, emp, con):
        fig, ax = MotorGrafico.configurar_grafica("Diagrama de Presupuesto", "Etapas del Enlace", "Potencia (dBm)")
        etapas = ["Tx", "Conect.", "Cable", "Empalmes", "Rx"]
        valores = [tx, tx - con, tx - con - cab, tx - con - cab - emp, tx - con - cab - emp]
        ax.step(range(len(etapas)), valores, where='post', color='#64b5f6', marker='o', linewidth=2)
        ax.axhline(y=rx, color='#ff5555', linestyle='--', label=f"Sensibilidad: {rx} dBm")
        ax.set_xticks(range(len(etapas)))
        ax.set_xticklabels(etapas, rotation=20, fontsize=7)
        ax.legend(facecolor='#2B2B2B', edgecolor='none', labelcolor='white', fontsize=7)
        return fig

    @staticmethod
    def plot_rayleigh(lambd_act):
        fig, ax = MotorGrafico.configurar_grafica("Esparcimiento Rayleigh", "Longitud de Onda (nm)", "Pérdida Relativa")
        lambdas = np.linspace(800, 1600, 100)
        atenuaciones = 1 / (lambdas ** 4)
        atenuaciones = atenuaciones / max(atenuaciones) # Normalizar curva
        ax.plot(lambdas, atenuaciones, color='#64b5f6', linewidth=2)
        ax.axvline(x=lambd_act, color='#d4af37', linestyle='--', label=f"λ act: {lambd_act:.0f}nm")
        ax.legend(facecolor='#2B2B2B', edgecolor='none', labelcolor='white', fontsize=7)
        return fig

    @staticmethod
    def plot_numero_v(a_um, lam_um, na):
        fig, ax = MotorGrafico.configurar_grafica("Región de Modos (V)", "Longitud de Onda (µm)", "Valor V")
        lambdas = np.linspace(max(0.1, lam_um - 0.5), lam_um + 0.5, 100)
        vs = (2 * np.pi * a_um / lambdas) * na
        ax.plot(lambdas, vs, color='#64b5f6', linewidth=2)
        ax.axhline(y=2.405, color='#ff5555', linestyle=':', label="Límite Monomodo")
        v_act = (2 * np.pi * a_um / lam_um) * na
        ax.plot(lam_um, v_act, 'go', markersize=6)
        ax.legend(facecolor='#2B2B2B', edgecolor='none', labelcolor='white', fontsize=7)
        return fig

    @staticmethod
    def plot_snell(n1, n2, th1, th2):
        fig, ax = MotorGrafico.configurar_grafica("Ley de Snell", "Frontera", "Medio")
        ax.axhline(0, color='gray', linewidth=2)
        ax.axvline(0, color='#555555', linestyle='--')
        
        x_inc = [-np.sin(np.radians(th1)), 0]
        y_inc = [np.cos(np.radians(th1)), 0]
        ax.plot(x_inc, y_inc, color='#d4af37', linewidth=2, label='Incidente')
        
        x_ref = [0, np.sin(np.radians(th2))]
        y_ref = [0, -np.cos(np.radians(th2))]
        ax.plot(x_ref, y_ref, color='#64b5f6', linewidth=2, label='Refractado')
        
        ax.set_xlim(-1, 1); ax.set_ylim(-1, 1)
        ax.text(-0.8, 0.5, f"n1 = {n1:.2f}", color="white")
        ax.text(0.2, -0.5, f"n2 = {n2:.2f}", color="white")
        ax.axis('off')
        return fig

    @staticmethod
    def plot_ensanchamiento(sigma_val):
        fig, ax = MotorGrafico.configurar_grafica("Ensanchamiento Temporal", "Tiempo (ps/ns)", "Amplitud")
        x = np.linspace(-10, 10, 200)
        y_in = np.exp(-(x**2)/0.5)
        ancho = max(1.0, float(sigma_val) / 5) 
        y_out = (1/ancho) * np.exp(-(x**2)/(2 * ancho**2))
        ax.plot(x, y_in, color='#d4af37', linestyle='--', label='Pulso Entrada')
        ax.plot(x, y_out, color='#64b5f6', linewidth=2, label='Pulso Salida')
        ax.legend(facecolor='#2B2B2B', edgecolor='none', labelcolor='white', fontsize=7)
        return fig

    @staticmethod
    def plot_g652(l0, s0):
        fig, ax = MotorGrafico.configurar_grafica("Curva Dispersión G.652", "Longitud de Onda (nm)", "D(λ) ps/(nm·km)")
        lambdas = np.linspace(1200, 1600, 100)
        d_vals = (s0 / 4) * (lambdas - (l0**4 / lambdas**3))
        ax.plot(lambdas, d_vals, color='#64b5f6', linewidth=2)
        ax.axhline(0, color='gray', linestyle='-')
        ax.axvline(l0, color='#ff5555', linestyle=':', label=f"λ₀ = {l0}nm")
        ax.legend(facecolor='#2B2B2B', edgecolor='none', labelcolor='white', fontsize=7)
        return fig