import customtkinter as ctk
from tkinter import messagebox
from motor_optico import MotorCalculoOptico
from motor_modulo_a import MotorModuloA

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Suite de Simulación Electrónica y Óptica")
        self.geometry("1350x850")  
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ==========================================
        # BARRA LATERAL (ACORDEÓN DINÁMICO)
        # ==========================================
        self.sidebar_frame = ctk.CTkFrame(self, width=330, corner_radius=0) 
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1) 

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="ÓpticaSuite Pro", font=ctk.CTkFont(size=26, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 20))

        self.btn_menu = ctk.CTkButton(self.sidebar_frame, text="🏠 Inicio", anchor="w", fg_color="transparent", text_color="gray90", hover_color="gray30", font=ctk.CTkFont(size=15), command=self.mostrar_inicio)
        self.btn_menu.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        # --- MOTOR DE ATENUACIÓN ---
        self.menu_base_visible = True
        self.btn_toggle_base = ctk.CTkButton(self.sidebar_frame, text="▼ Motor de Atenuación", anchor="w", font=ctk.CTkFont(size=15, weight="bold"), fg_color="transparent", hover_color="gray30", command=self.toggle_menu_base)
        self.btn_toggle_base.grid(row=2, column=0, padx=10, pady=(15, 5), sticky="ew")

        self.frame_sub_base = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.frame_sub_base.grid(row=3, column=0, sticky="ew", padx=15)
        
        btn_font = ctk.CTkFont(size=14)
        ctk.CTkButton(self.frame_sub_base, text="📉 Atenuación", anchor="w", font=btn_font, fg_color="transparent", hover_color="gray30", command=self.vista_calculo_atenuacion).pack(fill="x", pady=2)
        ctk.CTkButton(self.frame_sub_base, text="🎯 Eficiencia", anchor="w", font=btn_font, fg_color="transparent", hover_color="gray30", command=self.vista_calculo_eficiencia).pack(fill="x", pady=2)
        ctk.CTkButton(self.frame_sub_base, text="⚡ Power Budget", anchor="w", font=btn_font, fg_color="transparent", hover_color="gray30", command=self.vista_presupuesto_potencia).pack(fill="x", pady=2)
        ctk.CTkButton(self.frame_sub_base, text="✨ Rayleigh y Potencias", anchor="w", font=btn_font, fg_color="transparent", hover_color="gray30", command=self.vista_base_rayleigh).pack(fill="x", pady=2)
        ctk.CTkButton(self.frame_sub_base, text="🔄 Análisis Curvaturas", anchor="w", font=btn_font, fg_color="transparent", hover_color="gray30", command=self.vista_base_curvaturas).pack(fill="x", pady=2)
        ctk.CTkButton(self.frame_sub_base, text="📊 Modelos Estándar", anchor="w", font=btn_font, fg_color="transparent", hover_color="gray30", command=self.vista_base_modelos).pack(fill="x", pady=2)

        # --- MOTOR DE DISPERSIÓN ---
        self.menu_moda_visible = False
        self.btn_toggle_moda = ctk.CTkButton(self.sidebar_frame, text="▶ Motor de Dispersión", anchor="w", font=ctk.CTkFont(size=15, weight="bold"), fg_color="transparent", hover_color="#6b5317", text_color="#d4af37", command=self.toggle_menu_moda)
        self.btn_toggle_moda.grid(row=4, column=0, padx=10, pady=(15, 5), sticky="ew")

        self.frame_sub_moda = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        ctk.CTkButton(self.frame_sub_moda, text="📐 Óptica Geométrica", anchor="w", font=btn_font, fg_color="transparent", hover_color="#6b5317", command=self.vista_moda_geometrica).pack(fill="x", pady=2)
        ctk.CTkButton(self.frame_sub_moda, text="🔢 Número V y Modos", anchor="w", font=btn_font, fg_color="transparent", hover_color="#6b5317", command=self.vista_moda_parametros).pack(fill="x", pady=2)
        ctk.CTkButton(self.frame_sub_moda, text="⏱️ Dispersión y Retardos", anchor="w", font=btn_font, fg_color="transparent", hover_color="#6b5317", command=self.vista_moda_dispersion).pack(fill="x", pady=2)

        # --- MÓDULOS FUTUROS ---
        ctk.CTkLabel(self.sidebar_frame, text="MÓDULOS FUTUROS", font=ctk.CTkFont(size=13, weight="bold"), text_color="gray").grid(row=6, column=0, padx=20, pady=(20, 5), sticky="w")
        ctk.CTkButton(self.sidebar_frame, text="🔒 Módulo B", anchor="w", font=btn_font, state="disabled", fg_color="transparent").grid(row=7, column=0, padx=10, pady=(5, 20), sticky="ew")

        # --- ÁREA PRINCIPAL ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=20)
        self.mostrar_inicio()

    # ==========================================
    # FUNCIONES DE AYUDA Y UI DINÁMICA
    # ==========================================
    def abrir_ayuda(self, concepto, definicion):
        ventana_ayuda = ctk.CTkToplevel(self)
        ventana_ayuda.title(f"Ayuda: {concepto}")
        ventana_ayuda.geometry("500x280")
        ventana_ayuda.attributes("-topmost", True) 
        ctk.CTkLabel(ventana_ayuda, text=concepto, font=("Arial", 18, "bold")).pack(pady=(20, 10))
        ctk.CTkLabel(ventana_ayuda, text=definicion, font=("Arial", 14), wraplength=450, justify="left").pack(padx=20, pady=10)
        
        ctk.CTkLabel(ventana_ayuda, 
                     text="Para más información y derivación de fórmulas, consulte el libro:\nFiber Optic Communications por Gerd Keiser.", 
                     text_color="gray", 
                     wraplength=400, 
                     justify="center", 
                     font=("Arial", 12, "italic")).pack(side="bottom", pady=20)

    def crear_fila_input(self, parent, row, label_text, placeholder, unit_text, rango_text="", help_title="Info", help_desc="Detalle del parámetro."):
        lbl_font = ctk.CTkFont(size=14)
        ent_font = ctk.CTkFont(size=14)
        
        ctk.CTkLabel(parent, text=label_text, font=lbl_font).grid(row=row, column=0, padx=15, pady=10, sticky="e")
        ent = ctk.CTkEntry(parent, placeholder_text=placeholder, width=150, font=ent_font)
        ent.grid(row=row, column=1, padx=5, pady=10)
        
        rango_lbl = f"{unit_text}  {rango_text}" if rango_text else unit_text
        rango_font = ctk.CTkFont(size=13 if rango_text else 14)
        ctk.CTkLabel(parent, text=rango_lbl, text_color="#d4af37" if rango_text else "gray", width=250, anchor="w", font=rango_font).grid(row=row, column=2, padx=5, sticky="w")
        
        ctk.CTkButton(parent, text="?", width=32, height=32, font=lbl_font, command=lambda: self.abrir_ayuda(help_title, help_desc)).grid(row=row, column=3, padx=10)
        return ent

    def limpiar_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def mostrar_inicio(self):
        self.limpiar_main_frame()
        ctk.CTkLabel(self.main_frame, text="Bienvenido a ÓpticaSuite Pro", font=ctk.CTkFont(size=34, weight="bold")).pack(pady=(50, 10))
        ctk.CTkLabel(self.main_frame, text="Selecciona un módulo en la barra lateral para comenzar.", text_color="gray", font=ctk.CTkFont(size=18)).pack(pady=10)
        ctk.CTkLabel(self.main_frame, text="¡Deja un campo vacío para calcular su valor automáticamente!", text_color="#64b5f6", font=ctk.CTkFont(size=16)).pack(pady=5)

    def crear_area_scroll(self, titulo, color="white"):
        self.limpiar_main_frame()
        ctk.CTkLabel(self.main_frame, text=titulo, font=ctk.CTkFont(size=28, weight="bold"), text_color=color).pack(anchor="w", pady=(0, 10))
        scroll = ctk.CTkScrollableFrame(self.main_frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        return scroll

    def toggle_menu_base(self):
        if not self.menu_base_visible:
            self.frame_sub_base.grid(row=3, column=0, sticky="ew", padx=15)
            self.btn_toggle_base.configure(text="▼ Motor de Atenuación")
            self.menu_base_visible = True
            self.frame_sub_moda.grid_remove()
            self.btn_toggle_moda.configure(text="▶ Motor de Dispersión")
            self.menu_moda_visible = False

    def toggle_menu_moda(self):
        if not self.menu_moda_visible:
            self.frame_sub_moda.grid(row=5, column=0, sticky="ew", padx=15)
            self.btn_toggle_moda.configure(text="▼ Motor de Dispersión")
            self.menu_moda_visible = True
            self.frame_sub_base.grid_remove()
            self.btn_toggle_base.configure(text="▶ Motor de Atenuación")
            self.menu_base_visible = False

    def ejecutar_calculo_tradicional(self, func, lbl, formato, *entradas):
        try:
            valores = [float(e.get()) for e in entradas]
            res = func(*valores)
            lbl.configure(text=formato.format(res))
        except ValueError:
            messagebox.showerror("Error", "Revisa que todos los campos contengan números válidos.")

    # ==========================================
    # VISTAS DEL MOTOR DE ATENUACIÓN
    # ==========================================
    def vista_calculo_atenuacion(self):
        self.limpiar_main_frame()
        ctk.CTkLabel(self.main_frame, text="📉 Cálculo de Atenuación", font=ctk.CTkFont(size=28, weight="bold")).pack(anchor="w", pady=(0, 10))
        
        card = ctk.CTkFrame(self.main_frame, corner_radius=10); card.pack(fill="x", pady=10, ipady=10)
        ctk.CTkLabel(card, text="⮀ OMNIDIRECCIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        ctk.CTkLabel(card, text="Deja exactamente UN campo vacío para resolver la ecuación.", text_color="#64b5f6", font=ctk.CTkFont(size=13)).grid(row=1, column=0, columnspan=4, pady=(0, 10))

        ent_pin = self.crear_fila_input(card, 2, "Potencia (Pᵢₙ):", "Ej. 1.0", "[mW]", "[Típico: 0.1 a 10]")
        ent_pout = self.crear_fila_input(card, 3, "Potencia (Pₒᵤₜ):", "Ej. 0.5", "[mW]", "[Debe ser < Pᵢₙ]")
        ent_z = self.crear_fila_input(card, 4, "Distancia (z):", "Ej. 20.0", "[km]", "[Típico: 1 a 100]")
        ent_alpha = self.crear_fila_input(card, 5, "Atenuación (α):", "Ej. 0.25", "[dB/km]", "[Típico: 0.2 a 3.0]")

        def resolver_atenuacion():
            ents = {"pin": ent_pin, "pout": ent_pout, "z": ent_z, "alpha": ent_alpha}
            vacios = {k: v for k, v in ents.items() if v.get().strip() == ""}
            llenos = {k: float(v.get()) for k, v in ents.items() if v.get().strip() != ""}

            if len(vacios) != 1: return messagebox.showerror("Error", "Deja exactamente UN campo vacío.")
            inc = list(vacios.keys())[0]
            try:
                if inc == "alpha": res = MotorCalculoOptico.calcular_atenuacion_db_km(llenos["pin"], llenos["pout"], llenos["z"])
                elif inc == "pout": res = MotorCalculoOptico.calcular_potencia_salida(llenos["pin"], llenos["alpha"], llenos["z"])
                elif inc == "pin": res = MotorCalculoOptico.calcular_potencia_entrada(llenos["pout"], llenos["alpha"], llenos["z"])
                elif inc == "z": res = MotorCalculoOptico.calcular_distancia_atenuacion(llenos["pin"], llenos["pout"], llenos["alpha"])
                ents[inc].delete(0, 'end'); ents[inc].insert(0, f"{res:.4f}")
            except Exception as e: messagebox.showerror("Error", str(e))

        ctk.CTkButton(card, text="Resolver Variable", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=resolver_atenuacion).grid(row=6, column=0, columnspan=4, pady=15)

    def vista_presupuesto_potencia(self):
        self.limpiar_main_frame()
        ctk.CTkLabel(self.main_frame, text="⚡ Presupuesto de Potencia", font=ctk.CTkFont(size=28, weight="bold")).pack(anchor="w", pady=(0, 10))
        
        card = ctk.CTkFrame(self.main_frame, corner_radius=10); card.pack(fill="x", pady=10)
        ctk.CTkLabel(card, text="⮀ OMNIDIRECCIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        ctk.CTkLabel(card, text="Deja exactamente UN campo vacío para resolver la ecuación.", text_color="#64b5f6", font=ctk.CTkFont(size=13)).grid(row=1, column=0, columnspan=4, pady=(0, 10))

        ent_tx = self.crear_fila_input(card, 2, "Potencia Tx:", "Ej. 3.0", "[dBm]", "[Típico: -10 a 5]")
        ent_rx = self.crear_fila_input(card, 3, "Sensibilidad Rx:", "Ej. -32.0", "[dBm]", "[Típico: -40 a -20]")
        ent_cab = self.crear_fila_input(card, 4, "Pérdida Cable:", "Ej. 15.0", "[dB]", "[Típico: 0 a 30]")
        ent_emp = self.crear_fila_input(card, 5, "Empalmes:", "Ej. 1.0", "[dB]", "[Típico: 0.1 a 0.5 c/u]")
        ent_con = self.crear_fila_input(card, 6, "Conectores:", "Ej. 2.0", "[dB]", "[Típico: 0.5 a 2.0 c/u]")
        ent_mar = self.crear_fila_input(card, 7, "Margen Sistema:", "Ej. 5.0", "[dB]", "[Seguridad > 3]")

        def resolver_potencia():
            ents = {"tx": ent_tx, "rx": ent_rx, "cab": ent_cab, "emp": ent_emp, "con": ent_con, "mar": ent_mar}
            vacios = {k: v for k, v in ents.items() if v.get().strip() == ""}
            llenos = {k: float(v.get()) for k, v in ents.items() if v.get().strip() != ""}

            if len(vacios) != 1: return messagebox.showerror("Error", "Deja exactamente UN campo vacío.")
            inc = list(vacios.keys())[0]
            try:
                if inc == "mar": res = llenos["tx"] - llenos["rx"] - llenos["cab"] - llenos["emp"] - llenos["con"]
                elif inc == "tx": res = llenos["mar"] + llenos["rx"] + llenos["cab"] + llenos["emp"] + llenos["con"]
                elif inc == "rx": res = llenos["tx"] - llenos["mar"] - llenos["cab"] - llenos["emp"] - llenos["con"]
                elif inc == "cab": res = llenos["tx"] - llenos["rx"] - llenos["mar"] - llenos["emp"] - llenos["con"]
                elif inc == "emp": res = llenos["tx"] - llenos["rx"] - llenos["mar"] - llenos["cab"] - llenos["con"]
                elif inc == "con": res = llenos["tx"] - llenos["rx"] - llenos["mar"] - llenos["cab"] - llenos["emp"]
                ents[inc].delete(0, 'end'); ents[inc].insert(0, f"{res:.2f}")
            except Exception as e: messagebox.showerror("Error", str(e))

        ctk.CTkButton(card, text="Resolver Variable", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=resolver_potencia).grid(row=8, column=0, columnspan=4, pady=15)

    def vista_calculo_eficiencia(self):
        self.limpiar_main_frame()
        ctk.CTkLabel(self.main_frame, text="🎯 Eficiencia de Acoplamiento", font=ctk.CTkFont(size=28, weight="bold")).pack(anchor="w", pady=(0, 20))
        
        card = ctk.CTkFrame(self.main_frame, corner_radius=10); card.pack(fill="x", pady=10, ipady=10)
        ctk.CTkLabel(card, text="➔ TRADICIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        ctk.CTkLabel(card, text="Llena TODOS los campos para calcular el resultado final.", text_color="#9e9e9e", font=ctk.CTkFont(size=13)).grid(row=1, column=0, columnspan=4, pady=(0, 10))

        ent_rs = self.crear_fila_input(card, 2, "Radio Fuente (rs):", "Ej. 50.0", "[µm]", "[Típico: 10 a 100]")
        ent_a = self.crear_fila_input(card, 3, "Radio Núcleo (a):", "Ej. 25.0", "[µm]", "[Típico: 4 a 50]")
        ent_na = self.crear_fila_input(card, 4, "Apertura Numérica (NA):", "Ej. 0.22", "[Adim]", "[Típico: 0.1 a 0.3]")
        
        res = ctk.CTkLabel(card, text="Eficiencia (η): --", font=ctk.CTkFont(size=24, weight="bold")); res.grid(row=5, column=0, columnspan=4, pady=15)
        ctk.CTkButton(card, text="Calcular Eficiencia", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=lambda: self.ejecutar_calculo_tradicional(MotorCalculoOptico.eficiencia_acoplamiento, res, "Eficiencia: {:.4f}", ent_rs, ent_a, ent_na)).grid(row=6, column=0, columnspan=4, pady=10)

    def vista_base_rayleigh(self):
        scroll = self.crear_area_scroll("✨ Rayleigh y Predicción de Potencias")
        c1 = ctk.CTkFrame(scroll, corner_radius=10); c1.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c1, text="➔ TRADICIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        ctk.CTkLabel(c1, text="Llena TODOS los campos para calcular el resultado final.", text_color="#9e9e9e", font=ctk.CTkFont(size=13)).grid(row=1, column=0, columnspan=4, pady=(0, 10))

        ent_n = self.crear_fila_input(c1, 2, "Índice Núcleo (n):", "Ej. 1.46", "[Adim]", "[Típico: 1.44 a 1.48]")
        ent_bt = self.crear_fila_input(c1, 3, "Compresibilidad (βₜ):", "Ej. 7e-11", "[cm²/dina]", "[Típico: ~7e-11]")
        ent_tf = self.crear_fila_input(c1, 4, "Temp. Fusión (T_f):", "Ej. 1673", "[K]", "[Típico: 1400 a 1700]")
        ent_lnm = self.crear_fila_input(c1, 5, "Longitud Onda (λ):", "Ej. 850.0", "[nm]", "[Típico: 850, 1310, 1550]")
        
        res_r = ctk.CTkLabel(c1, text="α_Rayleigh = -- dB/km", font=ctk.CTkFont(size=18, weight="bold")); res_r.grid(row=6, column=0, columnspan=4, pady=5)
        ctk.CTkButton(c1, text="Calcular Rayleigh", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=lambda: self.ejecutar_calculo_tradicional(MotorCalculoOptico.atenuacion_rayleigh_eq37, res_r, "α_Rayleigh = {:.4f} dB/km", ent_n, ent_bt, ent_tf, ent_lnm)).grid(row=7, column=0, columnspan=4, pady=10)

    def vista_base_curvaturas(self):
        scroll = self.crear_area_scroll("🔄 Análisis Macro y Microcurvaturas")
        
        # Tarjeta 1: Macrocurvaturas
        c1 = ctk.CTkFrame(scroll, corner_radius=10); c1.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c1, text="Relación de Modos Efectivos (Macrocurvatura) ➔ TRADICIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        ctk.CTkLabel(c1, text="Llena TODOS los campos para calcular el resultado final.", text_color="#9e9e9e", font=ctk.CTkFont(size=13)).grid(row=1, column=0, columnspan=4, pady=(0, 10))

        ent_alf = self.crear_fila_input(c1, 2, "Perfil Índice (α):", "Ej. 2.0", "[Adim]", "[Gradual=2, Escalonado>1000]")
        ent_del = self.crear_fila_input(c1, 3, "Dif. Relativa (Δ):", "Ej. 0.01", "[Decimal]", "[Típico: 0.01 a 0.02]")
        ent_a = self.crear_fila_input(c1, 4, "Radio Núcleo (a):", "Ej. 25e-6", "[Metros]", "[Ej. 25e-6]")
        ent_R = self.crear_fila_input(c1, 5, "Radio Curvatura (R):", "Ej. 0.06", "[Metros]", "[Ej. 0.05 a 0.1]")
        ent_n2 = self.crear_fila_input(c1, 6, "Índice Revest. (n₂):", "Ej. 1.46", "[Adim]", "[Típico: 1.44 a 1.46]")
        ent_lmet = self.crear_fila_input(c1, 7, "Longitud Onda (λ):", "Ej. 1e-6", "[Metros]", "[Ej. 1.3e-6]")
        
        res_macro = ctk.CTkLabel(c1, text="Nₑᶠᶠ / N∞ = --", font=ctk.CTkFont(size=18, weight="bold")); res_macro.grid(row=8, column=0, columnspan=4, pady=5)
        ctk.CTkButton(c1, text="Calcular Macrocurvatura", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=lambda: self.ejecutar_calculo_tradicional(MotorCalculoOptico.modos_efectivos_curvatura, res_macro, "Modos Efectivos: {:.4f}", ent_alf, ent_del, ent_a, ent_R, ent_n2, ent_lmet)).grid(row=9, column=0, columnspan=4, pady=10)

        # Tarjeta 2: Microcurvaturas
        c2 = ctk.CTkFrame(scroll, corner_radius=10); c2.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c2, text="Factor Reducción (Microcurvatura) ➔ TRADICIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        ctk.CTkLabel(c2, text="Llena TODOS los campos para calcular el resultado final.", text_color="#9e9e9e", font=ctk.CTkFont(size=13)).grid(row=1, column=0, columnspan=4, pady=(0, 10))

        ent_ej = self.crear_fila_input(c2, 2, "Módulo Chaqueta (Eⱼ):", "Ej. 12.0", "[MPa]", "[Típico: 10 a 20]")
        ent_eg = self.crear_fila_input(c2, 3, "Módulo Vidrio (E_g):", "Ej. 65.0", "[GPa]", "[Típico: 60 a 75]")
        ent_ba = self.crear_fila_input(c2, 4, "Relación Radios (b/a):", "Ej. 2.5", "[Adim]", "[Típico: 2.0 a 3.0]")
        ent_del2 = self.crear_fila_input(c2, 5, "Diferencia Relativa (Δ):", "Ej. 0.01", "[Decimal]", "[Típico: 0.01 a 0.02]")
        
        res_micro = ctk.CTkLabel(c2, text="Factor de Reducción = --", font=ctk.CTkFont(size=18, weight="bold")); res_micro.grid(row=6, column=0, columnspan=4, pady=5)
        ctk.CTkButton(c2, text="Calcular Microcurvatura", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=lambda: self.ejecutar_calculo_tradicional(MotorCalculoOptico.factor_reduccion_keiser, res_micro, "Factor de Reducción: {:.4f}", ent_ej, ent_eg, ent_ba, ent_del2)).grid(row=7, column=0, columnspan=4, pady=10)

    def vista_base_modelos(self):
        scroll = self.crear_area_scroll("📊 Modelos y Dispersión Homologada")
        
        # Tarjeta 1: G.652
        c1 = ctk.CTkFrame(scroll, corner_radius=10); c1.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c1, text="Dispersión G.652 ➔ TRADICIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        ctk.CTkLabel(c1, text="Llena TODOS los campos para calcular el resultado final.", text_color="#9e9e9e", font=ctk.CTkFont(size=13)).grid(row=1, column=0, columnspan=4, pady=(0, 10))

        ent_l = self.crear_fila_input(c1, 2, "Longitud Onda (λ):", "Ej. 1550.0", "[nm]", "[Típico: 1200 a 1600]")
        ent_l0 = self.crear_fila_input(c1, 3, "Dispersión Cero (λ₀):", "Ej. 1310.0", "[nm]", "[Típico: 1300 a 1324]")
        ent_s0 = self.crear_fila_input(c1, 4, "Pendiente Cero (S₀):", "Ej. 0.092", "[ps/(nm²·km)]", "[Típico: 0.08 a 0.095]")
        
        res_g652 = ctk.CTkLabel(c1, text="D(λ) = -- ps/(nm·km)", font=ctk.CTkFont(size=18, weight="bold")); res_g652.grid(row=5, column=0, columnspan=4, pady=5)
        ctk.CTkButton(c1, text="Calcular Coeficiente D", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=lambda: self.ejecutar_calculo_tradicional(MotorCalculoOptico.calc_317_dispersion_g652, res_g652, "D(λ) = {:.4f} ps/(nm·km)", ent_l, ent_l0, ent_s0)).grid(row=6, column=0, columnspan=4, pady=10)

        # Tarjeta 2: Sellmeier
        c2 = ctk.CTkFrame(scroll, corner_radius=10); c2.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c2, text="Ecuación Sellmeier ➔ TRADICIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        ctk.CTkLabel(c2, text="Llena TODOS los campos para calcular el resultado final.", text_color="#9e9e9e", font=ctk.CTkFont(size=13)).grid(row=1, column=0, columnspan=4, pady=(0, 10))

        ent_lum = self.crear_fila_input(c2, 2, "Longitud Onda (λ):", "Ej. 1.3", "[µm]", "[Típico: 0.8 a 1.6]")
        ent_e0 = self.crear_fila_input(c2, 3, "Energía Reson. (E₀):", "Ej. 13.4", "[eV]", "[Típico: ~13.4]")
        ent_ed = self.crear_fila_input(c2, 4, "Energía Disp. (E_d):", "Ej. 14.7", "[eV]", "[Típico: ~14.7]")
        
        res_sell = ctk.CTkLabel(c2, text="n = --", font=ctk.CTkFont(size=18, weight="bold")); res_sell.grid(row=5, column=0, columnspan=4, pady=5)
        ctk.CTkButton(c2, text="Calcular Índice Sellmeier", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=lambda: self.ejecutar_calculo_tradicional(MotorCalculoOptico.indice_sellmeier, res_sell, "n = {:.4f}", ent_lum, ent_e0, ent_ed)).grid(row=6, column=0, columnspan=4, pady=10)

    # ==========================================
    # VISTAS DEL MOTOR DE DISPERSIÓN
    # ==========================================
    def vista_moda_geometrica(self):
        scroll = self.crear_area_scroll("📐 Óptica Geométrica", color="#d4af37")
        
        # Tarjeta 1: Índice y Velocidad
        c1 = ctk.CTkFrame(scroll, corner_radius=10); c1.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c1, text="Índice de Refracción (n = c/v) ⮀ OMNIDIRECCIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        ctk.CTkLabel(c1, text="Deja exactamente UN campo vacío para resolver la ecuación.", text_color="#64b5f6", font=ctk.CTkFont(size=13)).grid(row=1, column=0, columnspan=4, pady=(0, 10))
        
        ent_n = self.crear_fila_input(c1, 2, "Índice (n):", "Ej. 1.48", "[Adim]", "[Típico: 1.0 a 2.5]")
        ent_v = self.crear_fila_input(c1, 3, "Velocidad (v):", "Ej. 2e8", "[m/s]", "[< 3e8 m/s]")

        def resolver_n_v():
            ents = {"n": ent_n, "v": ent_v}
            vacios = {k: v for k, v in ents.items() if v.get().strip() == ""}
            llenos = {k: float(v.get()) for k, v in ents.items() if v.get().strip() != ""}
            if len(vacios) != 1: return messagebox.showerror("Error", "Deja exactamente UN campo vacío.")
            inc = list(vacios.keys())[0]
            try:
                if inc == "n": res = MotorModuloA.indice_refraccion(llenos["v"])
                elif inc == "v": res = MotorModuloA.velocidad_medio(llenos["n"])
                ents[inc].delete(0, 'end'); ents[inc].insert(0, f"{res:.2e}" if inc=="v" else f"{res:.4f}")
            except Exception as e: messagebox.showerror("Error", str(e))

        ctk.CTkButton(c1, text="Resolver Variables n/v", fg_color="#8d6e1f", hover_color="#6b5317", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=resolver_n_v).grid(row=4, column=0, columnspan=4, pady=10)

        # Tarjeta 2: Snell
        c2 = ctk.CTkFrame(scroll, corner_radius=10); c2.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c2, text="Ley de Snell (Refracción) ⮀ OMNIDIRECCIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        ctk.CTkLabel(c2, text="Deja exactamente UN campo vacío para resolver la ecuación.", text_color="#64b5f6", font=ctk.CTkFont(size=13)).grid(row=1, column=0, columnspan=4, pady=(0, 10))
        
        ent_sn1 = self.crear_fila_input(c2, 2, "Índice Origen (n₁):", "Ej. 1.48", "[Medio 1]", "[Típico: 1.44 a 1.48]")
        ent_sn2 = self.crear_fila_input(c2, 3, "Índice Destino (n₂):", "Ej. 1.46", "[Medio 2]", "[Típico: 1.0 a 1.48]")
        ent_th1 = self.crear_fila_input(c2, 4, "Áng. Incidencia (θ₁):", "Ej. 30.0", "[Grados °]", "[0 a 90 °]")
        ent_th2 = self.crear_fila_input(c2, 5, "Áng. Refracción (θ₂):", "Ej. 45.0", "[Grados °]", "[0 a 90 °]")

        def resolver_snell():
            ents = {"n1": ent_sn1, "n2": ent_sn2, "th1": ent_th1, "th2": ent_th2}
            vacios = {k: v for k, v in ents.items() if v.get().strip() == ""}
            llenos = {k: float(v.get()) for k, v in ents.items() if v.get().strip() != ""}
            if len(vacios) != 1: return messagebox.showerror("Error", "Deja exactamente UN campo vacío.")
            inc = list(vacios.keys())[0]
            try:
                if inc == "th2": res = MotorModuloA.angulo_refraccion_snell(llenos["n1"], llenos["n2"], llenos["th1"])
                elif inc == "th1": res = MotorModuloA.snell_inverso_theta1(llenos["n1"], llenos["n2"], llenos["th2"])
                elif inc == "n1": res = MotorModuloA.snell_inverso_n1(llenos["n2"], llenos["th1"], llenos["th2"])
                elif inc == "n2": res = MotorModuloA.snell_inverso_n2(llenos["n1"], llenos["th1"], llenos["th2"])
                ents[inc].delete(0, 'end'); ents[inc].insert(0, f"{res:.4f}")
            except Exception as e: messagebox.showerror("Error", str(e))

        ctk.CTkButton(c2, text="Resolver Snell", fg_color="#8d6e1f", hover_color="#6b5317", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=resolver_snell).grid(row=6, column=0, columnspan=4, pady=10)

        # Tarjeta 3: Parámetros del Núcleo (Tradicional)
        c3 = ctk.CTkFrame(scroll, corner_radius=10); c3.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c3, text="Parámetros del Núcleo ➔ TRADICIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        ctk.CTkLabel(c3, text="Llena TODOS los campos para calcular el resultado final.", text_color="#9e9e9e", font=ctk.CTkFont(size=13)).grid(row=1, column=0, columnspan=4, pady=(0, 10))
        
        ent_pn1 = self.crear_fila_input(c3, 2, "Índice Núcleo (n₁):", "Ej. 1.48", "[n₁ > n₂]", "[Típico: 1.44 a 1.48]")
        ent_pn2 = self.crear_fila_input(c3, 3, "Índice Revest. (n₂):", "Ej. 1.46", "[n₂ < n₁]", "[Típico: 1.44 a 1.46]")
        
        res_param = ctk.CTkLabel(c3, text="Áng. Crítico: -- ° | NA: -- | Δ: --", text_color="yellow", font=ctk.CTkFont(size=18, weight="bold")); res_param.grid(row=4, column=0, columnspan=4, pady=5)
        
        def calc_parametros_nucleo():
            try:
                n1, n2 = float(ent_pn1.get()), float(ent_pn2.get())
                ac = MotorModuloA.angulo_critico(n1, n2)
                na = MotorModuloA.apertura_numerica(n1, n2)
                delta = MotorModuloA.diferencia_indice_relativa(n1, n2)
                res_param.configure(text=f"Áng. Crítico: {ac:.2f} ° | NA: {na:.4f} | Δ: {delta*100:.2f}%")
            except Exception as e: messagebox.showerror("Error", str(e))
            
        ctk.CTkButton(c3, text="Calcular Parámetros", fg_color="#8d6e1f", hover_color="#6b5317", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=calc_parametros_nucleo).grid(row=5, column=0, columnspan=4, pady=10)

    def vista_moda_parametros(self):
        scroll = self.crear_area_scroll("🔢 Número V y Modos", color="#d4af37")
        
        c1 = ctk.CTkFrame(scroll, corner_radius=10); c1.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c1, text="Frecuencia Normalizada ⮀ OMNIDIRECCIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        ctk.CTkLabel(c1, text="Deja UN campo vacío (entre Radio, Longitud, NA o V) para despejar.", text_color="#64b5f6", font=ctk.CTkFont(size=13)).grid(row=1, column=0, columnspan=4, pady=(0, 10))

        ent_a = self.crear_fila_input(c1, 2, "Radio Núcleo (a):", "Ej. 25.0", "[µm]", "[Típico: 4 a 50]")
        ent_lam = self.crear_fila_input(c1, 3, "Longitud Onda (λ):", "Ej. 1.3", "[µm]", "[Típico: 0.85 a 1.55]")
        ent_na = self.crear_fila_input(c1, 4, "Apertura Num. (NA):", "Ej. 0.22", "[Adim]", "[Típico: 0.1 a 0.3]")
        ent_v = self.crear_fila_input(c1, 5, "Número V:", "Ej. 2.4", "[Adim]", "[Monomodo < 2.405]")
        ent_alf = self.crear_fila_input(c1, 6, "Perfil Índice (α):", "Ej. 2.0", "[Opcional]", "[Gradual=2]")
        
        res_modos = ctk.CTkLabel(c1, text="Modos Guiados: --", text_color="yellow", font=ctk.CTkFont(size=18, weight="bold")); res_modos.grid(row=7, column=0, columnspan=4, pady=5)
        
        def resolver_v():
            ents = {"a": ent_a, "lam": ent_lam, "na": ent_na, "v": ent_v}
            vacios = {k: v for k, v in ents.items() if v.get().strip() == ""}
            llenos = {k: float(v.get()) for k, v in ents.items() if v.get().strip() != ""}
            
            if len(vacios) != 1: return messagebox.showerror("Error", "Deja exactamente UN campo vacío en a, λ, NA o V.")
            inc = list(vacios.keys())[0]
            try:
                if inc == "v": res = MotorModuloA.frecuencia_normalizada_v(llenos["a"], llenos["lam"], llenos["na"])
                elif inc == "a": res = MotorModuloA.v_inverso_a(llenos["v"], llenos["lam"], llenos["na"])
                elif inc == "lam": res = MotorModuloA.v_inverso_lam(llenos["v"], llenos["a"], llenos["na"])
                elif inc == "na": res = MotorModuloA.v_inverso_na(llenos["v"], llenos["a"], llenos["lam"])
                
                ents[inc].delete(0, 'end'); ents[inc].insert(0, f"{res:.4f}")
                
                v_final = float(ent_v.get())
                m_esc = MotorModuloA.modos_guiados_escalonado(v_final)
                m_grad = MotorModuloA.modos_guiados_gradual(v_final, float(ent_alf.get())) if ent_alf.get() else "--"
                res_modos.configure(text=f"Modos Escalonados: {m_esc} | Graduales: {m_grad}")
            except Exception as e: messagebox.showerror("Error", str(e))
            
        ctk.CTkButton(c1, text="Resolver Ecuación V", fg_color="#8d6e1f", hover_color="#6b5317", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=resolver_v).grid(row=8, column=0, columnspan=4, pady=10)

    def vista_moda_dispersion(self):
        scroll = self.crear_area_scroll("⏱️ Dispersión y Retardos", color="#d4af37")

        # Tarjeta 1: Retardo Modal (Omni)
        c1 = ctk.CTkFrame(scroll, corner_radius=10); c1.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c1, text="Retardo Modal (Fibra Escalonada) ⮀ OMNIDIRECCIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        ctk.CTkLabel(c1, text="Deja exactamente UN campo vacío para resolver.", text_color="#64b5f6", font=ctk.CTkFont(size=13)).grid(row=1, column=0, columnspan=4, pady=(0, 5))
        ctk.CTkLabel(c1, text="⚠️ IMPORTANTE: Usa notación científica para el tiempo (Ej. 5e-9 para nanosegundos).", text_color="#ffcc00", font=ctk.CTkFont(size=13, slant="italic")).grid(row=2, column=0, columnspan=4, pady=(0, 10))

        ent_rl = self.crear_fila_input(c1, 3, "Longitud (L):", "Ej. 1000", "[m]", "[En metros]")
        ent_rn1 = self.crear_fila_input(c1, 4, "Índice Núcleo (n₁):", "Ej. 1.48", "[Adim]", "[Típico: 1.44 a 1.48]")
        ent_rdelta = self.crear_fila_input(c1, 5, "Dif. Relativa (Δ):", "Ej. 0.01", "[Decimal]", "[Típico: 0.01 a 0.02]")
        ent_rdt = self.crear_fila_input(c1, 6, "Retardo (ΔT):", "Ej. 5e-9", "[s]", "[Ej. 5e-9 s]")
        
        def resolver_retardo():
            ents = {"l": ent_rl, "n1": ent_rn1, "delta": ent_rdelta, "dt": ent_rdt}
            vacios = {k: v for k, v in ents.items() if v.get().strip() == ""}
            llenos = {k: float(v.get()) for k, v in ents.items() if v.get().strip() != ""}
            if len(vacios) != 1: return messagebox.showerror("Error", "Deja exactamente UN campo vacío en esta tarjeta.")
            inc = list(vacios.keys())[0]
            try:
                if inc == "dt": res = MotorModuloA.retardo_modal_escalonado(llenos["l"], llenos["n1"], llenos["delta"])
                elif inc == "l": res = MotorModuloA.retardo_inverso_l(llenos["dt"], llenos["n1"], llenos["delta"])
                elif inc == "n1": res = MotorModuloA.retardo_inverso_n1(llenos["dt"], llenos["l"], llenos["delta"])
                elif inc == "delta": res = MotorModuloA.retardo_inverso_delta(llenos["dt"], llenos["l"], llenos["n1"])
                ents[inc].delete(0, 'end'); ents[inc].insert(0, f"{res:.3e}" if inc=="dt" else f"{res:.4f}")
            except Exception as e: messagebox.showerror("Error", str(e))

        ctk.CTkButton(c1, text="Resolver Retardo", fg_color="#8d6e1f", hover_color="#6b5317", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=resolver_retardo).grid(row=7, column=0, columnspan=4, pady=10)

        # Tarjeta 2: Ensanchamiento Total (Tradicional)
        c2 = ctk.CTkFrame(scroll, corner_radius=10); c2.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c2, text="Ensanchamiento Total (Dispersión Cromática) ➔ TRADICIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        ctk.CTkLabel(c2, text="Llena TODOS los campos para calcular el resultado final.", text_color="#9e9e9e", font=ctk.CTkFont(size=13)).grid(row=1, column=0, columnspan=4, pady=(0, 10))

        ent_ed = self.crear_fila_input(c2, 2, "Coef. Dispersión (D):", "Ej. 17.0", "[ps/(nm·km)]", "[Típico: 15 a 18]")
        ent_el = self.crear_fila_input(c2, 3, "Longitud (L):", "Ej. 50.0", "[km]", "[Típico: 1 a 100]")
        ent_esig = self.crear_fila_input(c2, 4, "Ancho Espectral (σ_λ):", "Ej. 2.0", "[nm]", "[Típico: 0.1 a 5.0]")
        
        res_ens = ctk.CTkLabel(c2, text="σ = -- ps", text_color="yellow", font=ctk.CTkFont(size=18, weight="bold")); res_ens.grid(row=5, column=0, columnspan=4, pady=5)
        ctk.CTkButton(c2, text="Calcular Ensanchamiento", fg_color="#8d6e1f", hover_color="#6b5317", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=lambda: self.ejecutar_calculo_tradicional(MotorModuloA.ensanchamiento_total, res_ens, "σ = {:.2f} ps", ent_ed, ent_el, ent_esig)).grid(row=6, column=0, columnspan=4, pady=10)

        # Tarjeta 3: PMD (Tradicional)
        c3 = ctk.CTkFrame(scroll, corner_radius=10); c3.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c3, text="Dispersión por Modo de Polarización (PMD) ➔ TRADICIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        ctk.CTkLabel(c3, text="Llena TODOS los campos para calcular el resultado final.", text_color="#9e9e9e", font=ctk.CTkFont(size=13)).grid(row=1, column=0, columnspan=4, pady=(0, 10))

        ent_dpmd = self.crear_fila_input(c3, 2, "Coef. PMD (D_PMD):", "Ej. 0.5", "[ps/√km]", "[Típico: 0.1 a 0.5]")
        ent_pl = self.crear_fila_input(c3, 3, "Longitud (L):", "Ej. 100.0", "[km]", "[Típico: 1 a 100]")
        
        res_pmd = ctk.CTkLabel(c3, text="Δτ_PMD = -- ps", text_color="yellow", font=ctk.CTkFont(size=18, weight="bold")); res_pmd.grid(row=4, column=0, columnspan=4, pady=5)
        ctk.CTkButton(c3, text="Calcular PMD", fg_color="#8d6e1f", hover_color="#6b5317", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=lambda: self.ejecutar_calculo_tradicional(MotorModuloA.dispersion_polarizacion_pmd, res_pmd, "Δτ_PMD = {:.4f} ps", ent_dpmd, ent_pl)).grid(row=5, column=0, columnspan=4, pady=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()