import customtkinter as ctk
import math
from tkinter import messagebox

# ==========================================
# MOTOR MATEMÁTICO COMPLETO
# ==========================================
class MotorCalculoOptico:
    @staticmethod
    def calcular_atenuacion_db_km(p_in: float, p_out: float, z: float) -> float:
        if p_in <= 0 or p_out <= 0 or z <= 0:
            raise ValueError("Las potencias y la distancia deben ser > 0.")
        return (10 / z) * math.log10(p_in / p_out)

    @staticmethod
    def eficiencia_acoplamiento(rs: float, a: float, na: float) -> float:
        if rs <= 0 or a <= 0 or na <= 0:
            raise ValueError("Los radios y la apertura numérica deben ser > 0.")
        if rs <= a:
            return na ** 2
        else:
            return ((a / rs) ** 2) * (na ** 2)

    @staticmethod
    def margen_potencia(p_tx_dbm: float, sens_rx_dbm: float, atenuacion_cable_db: float, 
                        perdidas_empalmes_db: float, perdidas_conectores_db: float) -> float:
        perdida_permitida = p_tx_dbm - sens_rx_dbm
        perdidas_totales = atenuacion_cable_db + perdidas_empalmes_db + perdidas_conectores_db
        return perdida_permitida - perdidas_totales

# ==========================================
# INTERFAZ GRÁFICA
# ==========================================
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Suite de Simulación Electrónica y Óptica")
        self.geometry("850x600") # Un poco más grande para que todo quepa holgado
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.contenedor = ctk.CTkFrame(self)
        self.contenedor.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.mostrar_menu_principal()

    def limpiar_contenedor(self):
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    def mostrar_menu_principal(self):
        self.limpiar_contenedor()
        
        titulo = ctk.CTkLabel(self.contenedor, text="Módulos de Simulación", font=("Arial", 24, "bold"))
        titulo.pack(pady=30)
        
        btn_mod1 = ctk.CTkButton(self.contenedor, text="1. Motor de Cálculo Óptico", width=300, height=50, command=self.mostrar_menu_optico)
        btn_mod1.pack(pady=10)
        
        btn_mod2 = ctk.CTkButton(self.contenedor, text="2. Módulo Externo A (Pendiente)", width=300, height=50, state="disabled")
        btn_mod2.pack(pady=10)
        
        btn_mod3 = ctk.CTkButton(self.contenedor, text="3. Módulo Externo B (Pendiente)", width=300, height=50, state="disabled")
        btn_mod3.pack(pady=10)

    def mostrar_menu_optico(self):
        self.limpiar_contenedor()
        
        btn_volver = ctk.CTkButton(self.contenedor, text="← Volver al Menú", width=150, fg_color="gray", hover_color="darkgray", command=self.mostrar_menu_principal)
        btn_volver.pack(anchor="nw", pady=10, padx=10)
        
        titulo = ctk.CTkLabel(self.contenedor, text="Motor de Cálculo Óptico", font=("Arial", 22, "bold"))
        titulo.pack(pady=10)
        
        btn_atenuacion = ctk.CTkButton(self.contenedor, text="Calcular Atenuación (dB/km)", width=250, command=self.vista_calculo_atenuacion)
        btn_atenuacion.pack(pady=10)
        
        btn_eficiencia = ctk.CTkButton(self.contenedor, text="Calcular Eficiencia de Acoplamiento", width=250, command=self.vista_calculo_eficiencia) 
        btn_eficiencia.pack(pady=10)
        
        btn_presupuesto = ctk.CTkButton(self.contenedor, text="Presupuesto de Potencia", width=250, command=self.vista_presupuesto_potencia)
        btn_presupuesto.pack(pady=10)

    def abrir_ayuda(self, concepto, definicion):
        ventana_ayuda = ctk.CTkToplevel(self)
        ventana_ayuda.title(f"Ayuda: {concepto}")
        ventana_ayuda.geometry("400x250")
        ventana_ayuda.attributes("-topmost", True) 
        
        ctk.CTkLabel(ventana_ayuda, text=concepto, font=("Arial", 16, "bold")).pack(pady=(20, 10))
        ctk.CTkLabel(ventana_ayuda, text=definicion, wraplength=350, justify="left").pack(padx=20, pady=10)
        ctk.CTkLabel(ventana_ayuda, text="Para más información y derivación de fórmulas, consulte el libro:\nFiber Optic Communications por Gerd Keiser.", text_color="gray", wraplength=350, justify="center", font=("Arial", 11, "italic")).pack(side="bottom", pady=20)

    # === VISTA 1: ATENUACIÓN ===
    def vista_calculo_atenuacion(self):
        self.limpiar_contenedor()
        btn_volver = ctk.CTkButton(self.contenedor, text="← Volver a Módulo Óptico", width=180, fg_color="gray", hover_color="darkgray", command=self.mostrar_menu_optico)
        btn_volver.pack(anchor="nw", pady=10, padx=10)
        
        ctk.CTkLabel(self.contenedor, text="Cálculo de Atenuación (dB/km)", font=("Arial", 20, "bold")).pack(pady=10)
        
        frame_inputs = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        frame_inputs.pack(pady=20)

        ctk.CTkLabel(frame_inputs, text="Potencia Inicial (P_in):").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        ent_pin = ctk.CTkEntry(frame_inputs, placeholder_text="Ej. 1.0")
        ent_pin.grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkLabel(frame_inputs, text="[Rango típico: 0.1 - 10 mW]", text_color="gray").grid(row=0, column=2, padx=10, pady=10)
        ctk.CTkButton(frame_inputs, text="?", width=30, command=lambda: self.abrir_ayuda("Potencia Inicial (P_in)", "Potencia luminosa de entrada (mW o uW).")).grid(row=0, column=3, padx=5)

        ctk.CTkLabel(frame_inputs, text="Potencia Final (P_out):").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        ent_pout = ctk.CTkEntry(frame_inputs, placeholder_text="Ej. 0.5")
        ent_pout.grid(row=1, column=1, padx=10, pady=10)
        ctk.CTkLabel(frame_inputs, text="[Debe ser < P_in]", text_color="gray").grid(row=1, column=2, padx=10, pady=10)
        ctk.CTkButton(frame_inputs, text="?", width=30, command=lambda: self.abrir_ayuda("Potencia Final (P_out)", "Potencia óptica medida al final de la fibra.")).grid(row=1, column=3, padx=5)

        ctk.CTkLabel(frame_inputs, text="Distancia (z) en km:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        ent_z = ctk.CTkEntry(frame_inputs, placeholder_text="Ej. 20.0")
        ent_z.grid(row=2, column=1, padx=10, pady=10)
        ctk.CTkLabel(frame_inputs, text="[Rango típico: 1 - 100 km]", text_color="gray").grid(row=2, column=2, padx=10, pady=10)
        ctk.CTkButton(frame_inputs, text="?", width=30, command=lambda: self.abrir_ayuda("Distancia (z)", "Longitud de la fibra óptica en km.")).grid(row=2, column=3, padx=5)

        lbl_resultado = ctk.CTkLabel(self.contenedor, text="Resultado: -- dB/km", font=("Arial", 16, "bold"))
        btn_calcular = ctk.CTkButton(self.contenedor, text="Calcular", width=150, command=lambda: self.ejecutar_atenuacion(ent_pin, ent_pout, ent_z, lbl_resultado))
        btn_calcular.pack(pady=20)
        lbl_resultado.pack()

    def ejecutar_atenuacion(self, ent_pin, ent_pout, ent_z, lbl_resultado):
        try:
            res = MotorCalculoOptico.calcular_atenuacion_db_km(float(ent_pin.get()), float(ent_pout.get()), float(ent_z.get()))
            lbl_resultado.configure(text=f"Resultado: {res:.4f} dB/km", text_color="white")
        except ValueError:
            messagebox.showerror("Error", "Ingresa valores numéricos válidos > 0.")

    # === VISTA 2: EFICIENCIA ===
    def vista_calculo_eficiencia(self):
        self.limpiar_contenedor()
        btn_volver = ctk.CTkButton(self.contenedor, text="← Volver a Módulo Óptico", width=180, fg_color="gray", hover_color="darkgray", command=self.mostrar_menu_optico)
        btn_volver.pack(anchor="nw", pady=10, padx=10)
        
        ctk.CTkLabel(self.contenedor, text="Eficiencia de Acoplamiento (η)", font=("Arial", 20, "bold")).pack(pady=10)
        
        frame_inputs = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        frame_inputs.pack(pady=20)

        ctk.CTkLabel(frame_inputs, text="Radio de la Fuente (rs):").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        ent_rs = ctk.CTkEntry(frame_inputs, placeholder_text="Ej. 50.0")
        ent_rs.grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkLabel(frame_inputs, text="[µm]", text_color="gray").grid(row=0, column=2, padx=10, pady=10)
        ctk.CTkButton(frame_inputs, text="?", width=30, command=lambda: self.abrir_ayuda("Radio de la Fuente (rs)", "Radio del área emisora (LED/Láser) en µm.")).grid(row=0, column=3, padx=5)

        ctk.CTkLabel(frame_inputs, text="Radio del Núcleo (a):").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        ent_a = ctk.CTkEntry(frame_inputs, placeholder_text="Ej. 25.0")
        ent_a.grid(row=1, column=1, padx=10, pady=10)
        ctk.CTkLabel(frame_inputs, text="[µm]", text_color="gray").grid(row=1, column=2, padx=10, pady=10)
        ctk.CTkButton(frame_inputs, text="?", width=30, command=lambda: self.abrir_ayuda("Radio del Núcleo (a)", "Radio del núcleo de la fibra en µm.")).grid(row=1, column=3, padx=5)

        ctk.CTkLabel(frame_inputs, text="Apertura Numérica (NA):").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        ent_na = ctk.CTkEntry(frame_inputs, placeholder_text="Ej. 0.22")
        ent_na.grid(row=2, column=1, padx=10, pady=10)
        ctk.CTkLabel(frame_inputs, text="[Adimensional]", text_color="gray").grid(row=2, column=2, padx=10, pady=10)
        ctk.CTkButton(frame_inputs, text="?", width=30, command=lambda: self.abrir_ayuda("Apertura Numérica (NA)", "Capacidad de la fibra para captar luz.")).grid(row=2, column=3, padx=5)

        lbl_resultado = ctk.CTkLabel(self.contenedor, text="Resultado: -- %", font=("Arial", 16, "bold"))
        btn_calcular = ctk.CTkButton(self.contenedor, text="Calcular", width=150, command=lambda: self.ejecutar_eficiencia(ent_rs, ent_a, ent_na, lbl_resultado))
        btn_calcular.pack(pady=20)
        lbl_resultado.pack()

    def ejecutar_eficiencia(self, ent_rs, ent_a, ent_na, lbl_resultado):
        try:
            res = MotorCalculoOptico.eficiencia_acoplamiento(float(ent_rs.get()), float(ent_a.get()), float(ent_na.get()))
            lbl_resultado.configure(text=f"Resultado: {res * 100:.2f} %  (η = {res:.4f})", text_color="white")
        except ValueError:
            messagebox.showerror("Error", "Ingresa valores numéricos válidos > 0.")

    # === VISTA 3: PRESUPUESTO DE POTENCIA ===
    def vista_presupuesto_potencia(self):
        self.limpiar_contenedor()
        btn_volver = ctk.CTkButton(self.contenedor, text="← Volver a Módulo Óptico", width=180, fg_color="gray", hover_color="darkgray", command=self.mostrar_menu_optico)
        btn_volver.pack(anchor="nw", pady=10, padx=10)
        
        ctk.CTkLabel(self.contenedor, text="Presupuesto de Potencia (Power Budget)", font=("Arial", 20, "bold")).pack(pady=10)
        
        frame_inputs = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        frame_inputs.pack(pady=10)

        ctk.CTkLabel(frame_inputs, text="Potencia Tx (P_tx):").grid(row=0, column=0, padx=10, pady=8, sticky="e")
        ent_ptx = ctk.CTkEntry(frame_inputs, placeholder_text="Ej. 3.0")
        ent_ptx.grid(row=0, column=1, padx=10, pady=8)
        ctk.CTkLabel(frame_inputs, text="[dBm]", text_color="gray").grid(row=0, column=2, padx=10, pady=8)
        ctk.CTkButton(frame_inputs, text="?", width=30, command=lambda: self.abrir_ayuda("Potencia Tx", "Potencia de salida en dBm.")).grid(row=0, column=3, padx=5)

        ctk.CTkLabel(frame_inputs, text="Sensibilidad Rx (P_rx):").grid(row=1, column=0, padx=10, pady=8, sticky="e")
        ent_prx = ctk.CTkEntry(frame_inputs, placeholder_text="Ej. -32.0")
        ent_prx.grid(row=1, column=1, padx=10, pady=8)
        ctk.CTkLabel(frame_inputs, text="[dBm]", text_color="gray").grid(row=1, column=2, padx=10, pady=8)
        ctk.CTkButton(frame_inputs, text="?", width=30, command=lambda: self.abrir_ayuda("Sensibilidad Rx", "Nivel mínimo requerido por el detector.")).grid(row=1, column=3, padx=5)

        ctk.CTkLabel(frame_inputs, text="Pérdida Cable:").grid(row=2, column=0, padx=10, pady=8, sticky="e")
        ent_cable = ctk.CTkEntry(frame_inputs, placeholder_text="Ej. 15.0")
        ent_cable.grid(row=2, column=1, padx=10, pady=8)
        ctk.CTkLabel(frame_inputs, text="[dB]", text_color="gray").grid(row=2, column=2, padx=10, pady=8)
        ctk.CTkButton(frame_inputs, text="?", width=30, command=lambda: self.abrir_ayuda("Pérdida del Cable", "Atenuación total de la fibra.")).grid(row=2, column=3, padx=5)

        ctk.CTkLabel(frame_inputs, text="Pérdidas Empalmes:").grid(row=3, column=0, padx=10, pady=8, sticky="e")
        ent_empalmes = ctk.CTkEntry(frame_inputs, placeholder_text="Ej. 1.0")
        ent_empalmes.grid(row=3, column=1, padx=10, pady=8)
        ctk.CTkLabel(frame_inputs, text="[dB]", text_color="gray").grid(row=3, column=2, padx=10, pady=8)
        ctk.CTkButton(frame_inputs, text="?", width=30, command=lambda: self.abrir_ayuda("Pérdidas Empalmes", "Atenuación por empalmes.")).grid(row=3, column=3, padx=5)

        ctk.CTkLabel(frame_inputs, text="Pérdidas Conectores:").grid(row=4, column=0, padx=10, pady=8, sticky="e")
        ent_conectores = ctk.CTkEntry(frame_inputs, placeholder_text="Ej. 2.0")
        ent_conectores.grid(row=4, column=1, padx=10, pady=8)
        ctk.CTkLabel(frame_inputs, text="[dB]", text_color="gray").grid(row=4, column=2, padx=10, pady=8)
        ctk.CTkButton(frame_inputs, text="?", width=30, command=lambda: self.abrir_ayuda("Pérdidas Conectores", "Atenuación por conectores mecánicos.")).grid(row=4, column=3, padx=5)

        lbl_resultado = ctk.CTkLabel(self.contenedor, text="Margen: -- dB", font=("Arial", 16, "bold"))
        btn_calcular = ctk.CTkButton(self.contenedor, text="Calcular Margen", width=150, command=lambda: self.ejecutar_presupuesto(ent_ptx, ent_prx, ent_cable, ent_empalmes, ent_conectores, lbl_resultado))
        btn_calcular.pack(pady=15)
        lbl_resultado.pack()

    def ejecutar_presupuesto(self, ent_ptx, ent_prx, ent_cable, ent_empalmes, ent_conectores, lbl_resultado):
        try:
            margen = MotorCalculoOptico.margen_potencia(float(ent_ptx.get()), float(ent_prx.get()), float(ent_cable.get()), float(ent_empalmes.get()), float(ent_conectores.get()))
            if margen >= 0:
                lbl_resultado.configure(text=f"Margen del Sistema: {margen:.2f} dB  (Sistema Viable)", text_color="green")
            else:
                lbl_resultado.configure(text=f"Margen del Sistema: {margen:.2f} dB  (Sistema NO Viable)", text_color="red")
        except ValueError:
            messagebox.showerror("Error", "Ingresa valores numéricos (usa 0 si no hay pérdidas de empalmes o conectores).")

if __name__ == "__main__":
    app = App()
    app.mainloop()