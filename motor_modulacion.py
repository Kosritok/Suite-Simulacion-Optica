import numpy as np
import matplotlib
matplotlib.use('agg') # <--- SOLUCIÓN AL ERROR (Renderizado en memoria)
import matplotlib.pyplot as plt

class MotorModulacion:
    @staticmethod
    def configurar_subplots(titulo):
        fig, axs = plt.subplots(3, 1, figsize=(4.5, 4.5), facecolor='#2B2B2B', constrained_layout=True)
        
        fig.suptitle(titulo, color='#d4af37', fontsize=11, fontweight='bold')
        for i, ax in enumerate(axs):
            ax.set_facecolor('#212121')
            ax.tick_params(colors='white', labelsize=7)
            for spine in ax.spines.values():
                spine.set_edgecolor('#555555')
            ax.grid(color='#444444', linestyle=':', linewidth=0.5)
            
            if i < 2:
                ax.tick_params(labelbottom=False)
            else:
                ax.set_xlabel("Tiempo (s)", color='gray', fontsize=8)
                
        return fig, axs

    @staticmethod
    def plot_ask(Es: float, m: float, fc: float, fm: float):
        fig, axs = MotorModulacion.configurar_subplots("Modulación ASK (Amplitude Shift Keying)")
        
        t = np.linspace(0, 3/fm, 1500)
        
        mensaje = np.cos(2 * np.pi * fm * t)
        portadora = Es * np.cos(2 * np.pi * fc * t)
        modulada = Es * (1 + m * mensaje) * np.cos(2 * np.pi * fc * t)

        axs[0].plot(t, mensaje, color='#64b5f6', linewidth=2)
        axs[0].set_title("Señal de Mensaje (Analógica)", color='gray', fontsize=8)
        
        axs[1].plot(t, portadora, color='#66bb6a', linewidth=1)
        axs[1].set_title("Portadora Óptica", color='gray', fontsize=8)
        
        axs[2].plot(t, modulada, color='#d4af37', linewidth=1.5)
        axs[2].set_title("Señal Modulada ASK", color='gray', fontsize=8)
        
        return fig

    @staticmethod
    def plot_psk(Es: float, fc: float, bits_str: str):
        fig, axs = MotorModulacion.configurar_subplots("Modulación BPSK (Binary Phase Shift Keying)")
        
        bits = [int(b) for b in bits_str if b in '01']
        if not bits: 
            bits = [1, 0, 1, 1, 0]
            
        Tb = 1.0
        t = np.linspace(0, len(bits) * Tb, 1000 * len(bits))
        
        mensaje = np.zeros_like(t)
        modulada = np.zeros_like(t)
        portadora = Es * np.cos(2 * np.pi * fc * t)
        
        for i in range(len(bits)):
            idx = (t >= i * Tb) & (t < (i + 1) * Tb)
            mensaje[idx] = bits[i]
            
            b_t = 1 if bits[i] == 1 else -1
            modulada[idx] = b_t * Es * np.cos(2 * np.pi * fc * t[idx])
            
        axs[0].step(t, mensaje, color='#64b5f6', where='post', linewidth=2)
        axs[0].set_ylim(-0.2, 1.2)
        axs[0].set_title(f"Secuencia de Bits Original: {bits_str}", color='gray', fontsize=8)
        
        axs[1].plot(t, portadora, color='#66bb6a', linewidth=1)
        axs[1].set_title("Portadora Óptica", color='gray', fontsize=8)
        
        axs[2].plot(t, modulada, color='#d4af37', linewidth=1.5)
        axs[2].set_title("Señal Modulada BPSK (Inversiones de Fase de 180°)", color='gray', fontsize=8)
        
        return fig

    @staticmethod
    def plot_fsk(Es: float, delta_f: float, fc: float, fm: float):
        fig, axs = MotorModulacion.configurar_subplots("Modulación FSK (Frequency Shift Keying)")
        t = np.linspace(0, 3/fm, 1500)
        
        mensaje = np.cos(2 * np.pi * fm * t)
        portadora = Es * np.cos(2 * np.pi * fc * t)
        modulada = Es * np.cos(2 * np.pi * fc * t + (delta_f / fm) * np.sin(2 * np.pi * fm * t))

        axs[0].plot(t, mensaje, color='#64b5f6', linewidth=2)
        axs[0].set_title("Señal de Mensaje (Analógica)", color='gray', fontsize=8)
        
        axs[1].plot(t, portadora, color='#66bb6a', linewidth=1)
        axs[1].set_title("Portadora Óptica", color='gray', fontsize=8)
        
        axs[2].plot(t, modulada, color='#d4af37', linewidth=1.5)
        axs[2].set_title("Señal Modulada FSK", color='gray', fontsize=8)
        
        return fig

    @staticmethod
    def plot_dpsk(Es: float, fc: float, bits_str: str):
        fig, axs = MotorModulacion.configurar_subplots("Modulación DPSK (Differential Phase Shift Keying)")
        
        bits = [int(b) for b in bits_str if b in '01']
        if not bits: 
            bits = [1, 0, 1, 1, 0] 
            
        d_bits = [1] 
        for b in bits:
            d_bits.append(d_bits[-1] ^ b)
            
        Tb = 1.0 
        t = np.linspace(0, len(bits) * Tb, 1000 * len(bits))
        
        mensaje = np.zeros_like(t)
        modulada = np.zeros_like(t)
        portadora = Es * np.cos(2 * np.pi * fc * t)
        
        for i in range(len(bits)):
            idx = (t >= i * Tb) & (t < (i + 1) * Tb)
            mensaje[idx] = bits[i]
            
            fase = np.pi if d_bits[i+1] == 1 else 0
            modulada[idx] = Es * np.cos(2 * np.pi * fc * t[idx] + fase)
            
        axs[0].step(t, mensaje, color='#64b5f6', where='post', linewidth=2)
        axs[0].set_ylim(-0.2, 1.2)
        axs[0].set_title(f"Secuencia de Bits Original: {bits_str}", color='gray', fontsize=8)
        
        axs[1].plot(t, portadora, color='#66bb6a', linewidth=1)
        axs[1].set_title("Portadora Óptica", color='gray', fontsize=8)
        
        axs[2].plot(t, modulada, color='#d4af37', linewidth=1.5)
        axs[2].set_title("Señal Modulada DPSK (Saltos de Fase Diferenciales)", color='gray', fontsize=8)
        
        return fig