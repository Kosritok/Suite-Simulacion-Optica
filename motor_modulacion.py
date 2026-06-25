#Las fórmulas de esta sección que incluyen todo el módulo de motor de modulación fueron extraídas por
#ASK: Margarita y Patricia
#PSK: Germán
#FSK: Óscar Rosas
#DPSK: Emilio
#La programación del módulo fue hecha por Óscar Rosas ppara el caso de ASK y FSK
#La programación base de la sección de PSK fue hecha por Germán, en cuanto a refinarla y terminarla de integrar por Óscar Rosas
#La programación base de la sección de DPSK fue hecha por Emilio, en cuanto a refinarla y terminarla de integrar por Óscar Rosas


import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

class MotorModulacion:
    @staticmethod
    def configurar_subplots(titulo):
        fig, axs = plt.subplots(3, 1, figsize=(4.5, 4.5), facecolor='#2B2B2B', constrained_layout=True)
        #Definición de gráficos
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
    #Estilo de los gráficos

    @staticmethod
    def plot_ask_digital(A, f_m_ghz, bits_str):
        import numpy as np
        import matplotlib.pyplot as plt

        bits = [int(b) for b in bits_str if b in '01']
        if not bits: raise ValueError("Secuencia vacía")
        
        fc_vis = (500.0 / f_m_ghz) * 6.0
        fc_vis = max(min(fc_vis, 30.0), 1.0)
        
        t_bit = np.linspace(0, 1, 500)
        t_total, senial_modulada, senial_mensaje, senial_portadora = [], [], [], []
        
        for i, bit in enumerate(bits):
            t_actual = t_bit + i
            t_total.extend(t_actual)
            
            # Mensaje y Portadora pura
            senial_mensaje.extend(np.ones_like(t_bit) * bit)
            onda_portadora = A * np.cos(2 * np.pi * fc_vis * t_bit)
            senial_portadora.extend(onda_portadora)
            
            # Señal modulada BASK (OOK)
            if bit == 1:
                senial_modulada.extend(onda_portadora)
            else:
                senial_modulada.extend(np.zeros_like(t_bit))
                
        #Todas las lineas de código arriba de este comentario son la lógica de programación de ASK
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(6.5, 6), sharex=True, gridspec_kw={'height_ratios': [1, 1.2, 2]})
        
        ax1.plot(t_total, senial_mensaje, color="#64b5f6", linewidth=2)
        ax1.set_title("Señal de Mensaje m(t)", color='white', pad=5, fontsize=10)
        ax1.set_ylim(-0.2, 1.2)
        ax1.set_yticks([0, 1])
        for i, bit in enumerate(bits):
            ax1.text(i + 0.5, 1.3, str(bit), ha='center', va='bottom', color='white', fontweight='bold', fontsize=9)
            
        ax2.plot(t_total, senial_portadora, color="#ffd54f", linewidth=1.5)
        ax2.set_title("Portadora Óptica Pura c(t)", color='white', pad=5, fontsize=10)
        ax2.set_ylim(-A * 1.5, A * 1.5)
        
        ax3.plot(t_total, senial_modulada, color="#ab47bc", linewidth=1.5)
        ax3.set_title("Señal Modulada BASK (OOK)", color='white', pad=5, fontsize=10)
        ax3.set_xlabel("Tiempo (Bits)")
        ax3.set_ylabel("Amplitud [V/m]")
        ax3.set_ylim(-A * 1.5, A * 1.5)
        
        for ax in [ax1, ax2, ax3]:
            ax.set_facecolor('#212121')
            ax.tick_params(colors='white', labelsize=8)
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.grid(True, alpha=0.2)
            for i in range(len(bits) + 1):
                ax.axvline(x=i, color='gray', linestyle='--', alpha=0.5)

        fig.patch.set_alpha(0.0)
        plt.tight_layout()
        return fig
    #Las líneas de programación de arriba son para los plots de ASK

    @staticmethod
    def plot_psk_digital(A, f_m_ghz, bits_str):
        import numpy as np
        import matplotlib.pyplot as plt

        bits = [int(b) for b in bits_str if b in '01']
        if not bits: raise ValueError("Secuencia vacía")
        
        fc_vis = (500.0 / f_m_ghz) * 6.0
        fc_vis = max(min(fc_vis, 30.0), 1.0)
        
        t_bit = np.linspace(0, 1, 500)
        t_total, senial_modulada, senial_mensaje, senial_portadora = [], [], [], []
        
        for i, bit in enumerate(bits):
            t_actual = t_bit + i
            t_total.extend(t_actual)
            
            senial_mensaje.extend(np.ones_like(t_bit) * bit)
            
            # EL CAMBIO ESTÁ AQUÍ: Usamos t_actual en vez de t_bit
            onda_portadora = A * np.cos(2 * np.pi * fc_vis * t_actual)
            senial_portadora.extend(onda_portadora)
            
            # Señal modulada BPSK: Inversión de polaridad (NRZ) si el bit es 0
            if bit == 1:
                senial_modulada.extend(onda_portadora)
            else:
                senial_modulada.extend(-onda_portadora)
                
        #Todas las lineas de código arriba de este comentario son la lógica de programación de PSK
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(6.5, 6), sharex=True, gridspec_kw={'height_ratios': [1, 1.2, 2]})
        
        ax1.plot(t_total, senial_mensaje, color="#64b5f6", linewidth=2)
        ax1.set_title("Señal de Mensaje m(t)", color='white', pad=5, fontsize=10)
        ax1.set_ylim(-0.2, 1.2)
        ax1.set_yticks([0, 1])
        for i, bit in enumerate(bits):
            ax1.text(i + 0.5, 1.3, str(bit), ha='center', va='bottom', color='white', fontweight='bold', fontsize=9)
            
        ax2.plot(t_total, senial_portadora, color="#ffd54f", linewidth=1.5)
        ax2.set_title("Portadora Óptica Pura c(t)", color='white', pad=5, fontsize=10)
        ax2.set_ylim(-A * 1.5, A * 1.5)
        
        ax3.plot(t_total, senial_modulada, color="#ab47bc", linewidth=1.5)
        ax3.set_title("Señal Modulada BPSK", color='white', pad=5, fontsize=10)
        ax3.set_xlabel("Tiempo (Bits)")
        ax3.set_ylabel("Amplitud [V/m]")
        ax3.set_ylim(-A * 1.5, A * 1.5)
        
        for ax in [ax1, ax2, ax3]:
            ax.set_facecolor('#212121')
            ax.tick_params(colors='white', labelsize=8)
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.grid(True, alpha=0.2)
            for i in range(len(bits) + 1):
                ax.axvline(x=i, color='gray', linestyle='--', alpha=0.5)

        fig.patch.set_alpha(0.0)
        plt.tight_layout()
        return fig
    
    #Las líneas de programación de arriba son para los plots de PSK
    
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
    
    #Las líneas de programación de arriba son para los plots de FSK
    
    @staticmethod
    def plot_fsk_digital(A, f_m_ghz, bits_str):
        import numpy as np
        import matplotlib.pyplot as plt

        # Limpiar la cadena para asegurar que solo haya bits
        bits = [int(b) for b in bits_str if b in '01']
        if not bits:
            raise ValueError("Secuencia vacía")
        
        # LÓGICA DINÁMICA DE VISUALIZACIÓN
        # A mayor tasa de bits (f_m), la ventana de tiempo es más corta,
        # por lo que caben menos ciclos de la portadora por cada bit.
        # Tomamos 500 GHz como base para mostrar ~6 ciclos.
        fc_vis = (500.0 / f_m_ghz) * 6.0
        
        # Limitamos los ciclos entre 1 y 30 para que la gráfica de Matplotlib
        # no se vuelva una gráfica saturada negra si metes valores extremos.
        fc_vis = max(min(fc_vis, 30.0), 1.0)
        
        f1 = fc_vis * 1.5  # Frecuencia rápida para el bit '1' (+50%)
        f2 = fc_vis * 0.5  # Frecuencia lenta para el bit '0' (-50%)
        
        t_bit = np.linspace(0, 1, 500)
        t_total = []
        senial_modulada = []
        senial_mensaje = []
        senial_portadora = []
        
        for i, bit in enumerate(bits):
            t_actual = t_bit + i
            t_total.extend(t_actual)
            
            # 1. Mensaje m(t) (Onda cuadrada)
            senial_mensaje.extend(np.ones_like(t_bit) * bit)
            
            # 2. Portadora pura c(t) (Onda constante)
            senial_portadora.extend(A * np.cos(2 * np.pi * fc_vis * t_bit))
            
            # 3. Señal modulada BFSK s(t)
            if bit == 1:
                senial_modulada.extend(A * np.cos(2 * np.pi * f1 * t_bit))
            else:
                senial_modulada.extend(A * np.cos(2 * np.pi * f2 * t_bit))
                
        #Todas las lineas de código arriba de este comentario son la lógica de programación de FSK
        # Crear figura con 3 subplots apilados
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(6.5, 6), sharex=True, gridspec_kw={'height_ratios': [1, 1.2, 2]})
        
        # --- Subplot 1: Mensaje Digital m(t) ---
        ax1.plot(t_total, senial_mensaje, color="#64b5f6", linewidth=2)
        ax1.set_title("Señal de Mensaje m(t) (Datos)", color='white', pad=5, fontsize=10)
        ax1.set_ylim(-0.2, 1.2)
        ax1.set_yticks([0, 1])
        
        for i, bit in enumerate(bits):
            ax1.text(i + 0.5, 1.3, str(bit), ha='center', va='bottom', color='white', fontweight='bold', fontsize=9)
            
        # --- Subplot 2: Señal Portadora c(t) ---
        ax2.plot(t_total, senial_portadora, color="#ffd54f", linewidth=1.5)
        ax2.set_title("Portadora Óptica Pura c(t)", color='white', pad=5, fontsize=10)
        ax2.set_ylim(-A * 1.5, A * 1.5)
        
        # --- Subplot 3: Señal Modulada s(t) ---
        ax3.plot(t_total, senial_modulada, color="#ab47bc", linewidth=1.5)
        ax3.set_title("Señal Modulada BFSK s(t)", color='white', pad=5, fontsize=10)
        ax3.set_xlabel("Tiempo (Bits)")
        ax3.set_ylabel("Amplitud [V/m]")
        ax3.set_ylim(-A * 1.5, A * 1.5)
        
        # Estilos comunes para modo oscuro
        for ax in [ax1, ax2, ax3]:
            ax.set_facecolor('#212121')
            ax.tick_params(colors='white', labelsize=8)
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.grid(True, alpha=0.2)
            
            # Dibujar líneas separadoras de bits
            for i in range(len(bits) + 1):
                ax.axvline(x=i, color='gray', linestyle='--', alpha=0.5)

        fig.patch.set_alpha(0.0)
        plt.tight_layout()
        
        return fig
    
    #Las líneas de programación de arriba son para los plots de FSK

    @staticmethod
    def plot_dpsk_digital(A, f_m_ghz, bits_str):
        import numpy as np
        import matplotlib.pyplot as plt

        bits = [int(b) for b in bits_str if b in '01']
        if not bits: raise ValueError("Secuencia vacía")
        
        # Dinámica de escalado visual para la portadora
        fc_vis = (500.0 / f_m_ghz) * 6.0
        fc_vis = max(min(fc_vis, 30.0), 1.0)
        
        muestras_bit = 500
        num_bits = len(bits)
        t = np.linspace(0, num_bits, num_bits * muestras_bit, endpoint=False)
        
        # 1. Señal Original m(t)
        mensaje_original = np.repeat(bits, muestras_bit)
        
        # 2. Codificador Diferencial (Lógica XOR del archivo fuente)
        m_n = [0] # Bit de referencia inicial
        for bit in bits:
            nuevo_estado = bit ^ m_n[-1]
            m_n.append(nuevo_estado)
            
        # Repetimos los bits codificados (excluyendo el de referencia para encajar en el tiempo)
        datos_codificados = np.repeat(m_n[1:], muestras_bit)
        
        # 3. Señal Modulada DPSK
        fase = datos_codificados * np.pi
        senal_modulada = A * np.cos(2 * np.pi * fc_vis * t + fase)
        
        # 4. Detección en Receptor (Multiplicación por señal retrasada)
        # Usamos np.pad para evitar el comportamiento cíclico indeseado al inicio de la gráfica
        senal_retrasada = np.pad(senal_modulada, (muestras_bit, 0), mode='constant')[:len(senal_modulada)]
        producto_rx = senal_modulada * senal_retrasada
        
#Todas las lineas de código arriba de este comentario son la lógica de programación de DPSK

        # --- Generación de Gráficas (4 Paneles) ---
        fig, axs = plt.subplots(4, 1, figsize=(6.5, 7.5), sharex=True, gridspec_kw={'height_ratios': [1, 1, 2, 1.5]})
        
        # Panel 1: Mensaje Original
        axs[0].plot(t, mensaje_original, color="#64b5f6", linewidth=2)
        axs[0].set_title("Mensaje Original m(t)", color='white', pad=5, fontsize=10)
        axs[0].set_ylim(-0.2, 1.2)
        axs[0].set_yticks([0, 1])
        for i, bit in enumerate(bits):
            axs[0].text(i + 0.5, 1.3, str(bit), ha='center', va='bottom', color='white', fontweight='bold', fontsize=9)
            
        # Panel 2: Mensaje Codificado (Diferencial)
        axs[1].plot(t, datos_codificados, color="#ffd54f", linewidth=2)
        axs[1].set_title("Mensaje Codificado Diferencialmente d(t)", color='white', pad=5, fontsize=10)
        axs[1].set_ylim(-0.2, 1.2)
        axs[1].set_yticks([0, 1])
        
        # Panel 3: Señal Modulada
        axs[2].plot(t, senal_modulada, color="#ab47bc", linewidth=1.5)
        axs[2].set_title("Señal Modulada DPSK", color='white', pad=5, fontsize=10)
        axs[2].set_ylim(-A * 1.5, A * 1.5)
        
        # Panel 4: Producto en Receptor
        axs[3].plot(t, producto_rx, color="#ff7043", alpha=0.8, linewidth=1.5)
        axs[3].set_title("Detección en Receptor (Producto)", color='white', pad=5, fontsize=10)
        axs[3].set_xlabel("Tiempo (Bits)")
        axs[3].set_ylabel("Amplitud Relativa")
        # El límite vertical se adapta dinámicamente al producto de amplitudes
        axs[3].set_ylim(-(A**2) * 1.5, (A**2) * 1.5)
        
        # Estilos comunes de modo oscuro
        for ax in axs:
            ax.set_facecolor('#212121')
            ax.tick_params(colors='white', labelsize=8)
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.grid(True, alpha=0.2)
            # Dibujar separadores de bits
            for i in range(len(bits) + 1):
                ax.axvline(x=i, color='gray', linestyle='--', alpha=0.5)

        fig.patch.set_alpha(0.0)
        plt.tight_layout()
        return fig
    
    #Las líneas de programación de arriba son para los plots de DPSK