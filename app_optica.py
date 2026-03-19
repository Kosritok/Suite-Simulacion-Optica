import customtkinter as ctk
from tkinter import messagebox
from motor_optico import MotorCalculoOptico
from motor_modulo_a import MotorModuloA

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Suite de Simulación Electrónica y Óptica")
        self.geometry("1100x750")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ==========================================
        # BARRA LATERAL (ACORDEÓN DINÁMICO)
        # ==========================================
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1) 

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="ÓpticaSuite Pro", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 20))

        self.btn_menu = ctk.CTkButton(self.sidebar_frame, text="🏠 Inicio", anchor="w", fg_color="transparent", text_color="gray90", hover_color="gray30", command=self.mostrar_inicio)
        self.btn_menu.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        # --- MÓDULO BASE ---
        self.menu_base_visible = True
        self.btn_toggle_base = ctk.CTkButton(self.sidebar_frame, text="▼ MÓDULO ÓPTICO BASE", anchor="w", font=ctk.CTkFont(weight="bold"), fg_color="transparent", hover_color="gray30", command=self.toggle_menu_base)
        self.btn_toggle_base.grid(row=2, column=0, padx=10, pady=(15, 5), sticky="ew")

        self.frame_sub_base = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.frame_sub_base.grid(row=3, column=0, sticky="ew", padx=15)
        
        ctk.CTkButton(self.frame_sub_base, text="📉 Atenuación", anchor="w", fg_color="transparent", hover_color="gray30", command=self.vista_calculo_atenuacion).pack(fill="x", pady=2)
        ctk.CTkButton(self.frame_sub_base, text="🎯 Eficiencia", anchor="w", fg_color="transparent", hover_color="gray30", command=self.vista_calculo_eficiencia).pack(fill="x", pady=2)
        ctk.CTkButton(self.frame_sub_base, text="⚡ Power Budget", anchor="w", fg_color="transparent", hover_color="gray30", command=self.vista_presupuesto_potencia).pack(fill="x", pady=2)

        # --- MÓDULO A ---
        self.menu_moda_visible = False
        self.btn_toggle_moda = ctk.CTkButton(self.sidebar_frame, text="▶ MÓDULO A: DISPERSIÓN", anchor="w", font=ctk.CTkFont(weight="bold"), fg_color="transparent", hover_color="#6b5317", text_color="#d4af37", command=self.toggle_menu_moda)
        self.btn_toggle_moda.grid(row=4, column=0, padx=10, pady=(15, 5), sticky="ew")

        self.frame_sub_moda = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        ctk.CTkButton(self.frame_sub_moda, text="📐 Óptica Geométrica", anchor="w", fg_color="transparent", hover_color="#6b5317", command=self.vista_moda_geometrica).pack(fill="x", pady=2)
        ctk.CTkButton(self.frame_sub_moda, text="🔢 Número V y Modos", anchor="w", fg_color="transparent", hover_color="#6b5317", command=self.vista_moda_parametros).pack(fill="x", pady=2)
        ctk.CTkButton(self.frame_sub_moda, text="⏱️ Dispersión y Retardos", anchor="w", fg_color="transparent", hover_color="#6b5317", command=self.vista_moda_dispersion).pack(fill="x", pady=2)

        # --- MÓDULO B ---
        ctk.CTkLabel(self.sidebar_frame, text="MÓDULOS FUTUROS", font=ctk.CTkFont(size=11, weight="bold"), text_color="gray").grid(row=8, column=0, padx=20, pady=(20, 5), sticky="w")
        ctk.CTkButton(self.sidebar_frame, text="🔒 Módulo B", anchor="w", state="disabled", fg_color="transparent").grid(row=9, column=0, padx=10, pady=(5, 20), sticky="ew")

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
        ventana_ayuda.geometry("450x250")
        ventana_ayuda.attributes("-topmost", True) 
        ctk.CTkLabel(ventana_ayuda, text=concepto, font=("Arial", 16, "bold")).pack(pady=(20, 10))
        ctk.CTkLabel(ventana_ayuda, text=definicion, wraplength=400, justify="left").pack(padx=20, pady=10)
        
        # Referencia bibliográfica restaurada
        ctk.CTkLabel(ventana_ayuda, 
                     text="Para más información y derivación de fórmulas, consulte el libro:\nFiber Optic Communications por Gerd Keiser.", 
                     text_color="gray", 
                     wraplength=350, 
                     justify="center", 
                     font=("Arial", 11, "italic")).pack(side="bottom", pady=20)

    def crear_fila_input(self, parent, row, label_text, placeholder, unit_text, help_title, help_desc):
        """Dibuja de forma automática una fila con Label, Input, Rango gris y botón de Ayuda."""
        ctk.CTkLabel(parent, text=label_text).grid(row=row, column=0, padx=15, pady=8, sticky="e")
        ent = ctk.CTkEntry(parent, placeholder_text=placeholder, width=130)
        ent.grid(row=row, column=1, padx=5, pady=8)
        ctk.CTkLabel(parent, text=unit_text, text_color="gray", width=140, anchor="w").grid(row=row, column=2, padx=5, sticky="w")
        ctk.CTkButton(parent, text="?", width=28, height=28, command=lambda: self.abrir_ayuda(help_title, help_desc)).grid(row=row, column=3, padx=10)
        return ent

    def limpiar_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def mostrar_inicio(self):
        self.limpiar_main_frame()
        ctk.CTkLabel(self.main_frame, text="Bienvenido a ÓpticaSuite Pro", font=ctk.CTkFont(size=28, weight="bold")).pack(pady=(50, 10))
        ctk.CTkLabel(self.main_frame, text="Expande los módulos en la barra lateral para ver los cálculos disponibles.", text_color="gray", font=ctk.CTkFont(size=16)).pack(pady=10)

    def toggle_menu_base(self):
        if not self.menu_base_visible:
            self.frame_sub_base.grid(row=3, column=0, sticky="ew", padx=15)
            self.btn_toggle_base.configure(text="▼ MÓDULO ÓPTICO BASE")
            self.menu_base_visible = True
            self.frame_sub_moda.grid_remove()
            self.btn_toggle_moda.configure(text="▶ MÓDULO A: DISPERSIÓN")
            self.menu_moda_visible = False

    def toggle_menu_moda(self):
        if not self.menu_moda_visible:
            self.frame_sub_moda.grid(row=5, column=0, sticky="ew", padx=15)
            self.btn_toggle_moda.configure(text="▼ MÓDULO A: DISPERSIÓN")
            self.menu_moda_visible = True
            self.frame_sub_base.grid_remove()
            self.btn_toggle_base.configure(text="▶ MÓDULO ÓPTICO BASE")
            self.menu_base_visible = False

    def ejecutar_calculo(self, func, lbl, formato, *entradas):
        try:
            valores = [float(e.get()) for e in entradas]
            res = func(*valores)
            lbl.configure(text=formato.format(res))
        except ValueError:
            messagebox.showerror("Error", "Revisa que todos los campos contengan números válidos.")

    # ==========================================
    # VISTAS DEL MÓDULO ÓPTICO BASE
    # ==========================================
    def vista_calculo_atenuacion(self):
        self.limpiar_main_frame()
        ctk.CTkLabel(self.main_frame, text="📉 Cálculo de Atenuación", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", pady=(0, 20))
        card = ctk.CTkFrame(self.main_frame, corner_radius=10); card.pack(fill="x", pady=10, ipady=10)
        
        ent_pin = self.crear_fila_input(card, 0, "Potencia In (P_in):", "Ej. 1.0", "[Rango: 0.1 - 10 mW]", "Potencia Inicial", "Potencia luminosa de entrada a la fibra.")
        ent_pout = self.crear_fila_input(card, 1, "Potencia Out (P_out):", "Ej. 0.5", "[Debe ser < P_in]", "Potencia Final", "Potencia óptica medida en la salida.")
        ent_z = self.crear_fila_input(card, 2, "Distancia (z):", "Ej. 20.0", "[Rango: 1 - 100 km]", "Distancia", "Longitud física del enlace de fibra óptica.")
        
        res = ctk.CTkLabel(self.main_frame, text="Atenuación: -- dB/km", font=ctk.CTkFont(size=20, weight="bold")); res.pack(pady=20)
        ctk.CTkButton(self.main_frame, text="Calcular", command=lambda: self.ejecutar_calculo(MotorCalculoOptico.calcular_atenuacion_db_km, res, "Atenuación: {:.4f} dB/km", ent_pin, ent_pout, ent_z)).pack()

    def vista_calculo_eficiencia(self):
        self.limpiar_main_frame()
        ctk.CTkLabel(self.main_frame, text="🎯 Eficiencia de Acoplamiento", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", pady=(0, 20))
        card = ctk.CTkFrame(self.main_frame, corner_radius=10); card.pack(fill="x", pady=10, ipady=10)

        ent_rs = self.crear_fila_input(card, 0, "Radio Fuente (rs):", "Ej. 50.0", "[µm]", "Radio de la Fuente", "Radio del área emisora de luz (LED o Láser).")
        ent_a = self.crear_fila_input(card, 1, "Radio Núcleo (a):", "Ej. 25.0", "[µm]", "Radio del Núcleo", "Radio del núcleo de la fibra óptica.")
        ent_na = self.crear_fila_input(card, 2, "Apertura Numérica (NA):", "Ej. 0.22", "[Adimensional]", "Apertura Numérica", "Capacidad de captación de luz de la fibra.")

        res = ctk.CTkLabel(self.main_frame, text="Eficiencia (η): --", font=ctk.CTkFont(size=20, weight="bold")); res.pack(pady=20)
        ctk.CTkButton(self.main_frame, text="Calcular", command=lambda: self.ejecutar_calculo(MotorCalculoOptico.eficiencia_acoplamiento, res, "Eficiencia: {:.4f}", ent_rs, ent_a, ent_na)).pack()

    def vista_presupuesto_potencia(self):
        self.limpiar_main_frame()
        ctk.CTkLabel(self.main_frame, text="⚡ Presupuesto de Potencia", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", pady=(0, 10))
        card = ctk.CTkFrame(self.main_frame, corner_radius=10); card.pack(fill="x", pady=10)

        ent_tx = self.crear_fila_input(card, 0, "Potencia Tx:", "Ej. 3.0", "[dBm]", "Potencia de Transmisión", "Potencia inyectada al sistema.")
        ent_rx = self.crear_fila_input(card, 1, "Sensibilidad Rx:", "Ej. -32.0", "[dBm]", "Sensibilidad de Recepción", "Potencia mínima detectada por el receptor.")
        ent_cab = self.crear_fila_input(card, 2, "Pérdida Cable:", "Ej. 15.0", "[dB]", "Pérdida por Cable", "Atenuación total en el tramo de fibra.")
        ent_emp = self.crear_fila_input(card, 3, "Empalmes:", "Ej. 1.0", "[dB]", "Pérdidas por Empalmes", "Suma de atenuaciones por uniones fijas.")
        ent_con = self.crear_fila_input(card, 4, "Conectores:", "Ej. 2.0", "[dB]", "Pérdidas por Conectores", "Atenuación en las conexiones mecánicas extraíbles.")

        res = ctk.CTkLabel(self.main_frame, text="Margen: -- dB", font=ctk.CTkFont(size=20, weight="bold")); res.pack(pady=15)
        ctk.CTkButton(self.main_frame, text="Calcular", command=lambda: self.ejecutar_calculo(MotorCalculoOptico.margen_potencia, res, "Margen: {:.2f} dB", ent_tx, ent_rx, ent_cab, ent_emp, ent_con)).pack()

    # ==========================================
    # VISTAS DEL MÓDULO A (Con Scroll y Diseño Restaurado)
    # ==========================================
    def crear_area_scroll(self, titulo):
        self.limpiar_main_frame()
        ctk.CTkLabel(self.main_frame, text=titulo, font=ctk.CTkFont(size=24, weight="bold"), text_color="#d4af37").pack(anchor="w", pady=(0, 10))
        scroll = ctk.CTkScrollableFrame(self.main_frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        return scroll

    def vista_moda_geometrica(self):
        scroll = self.crear_area_scroll("📐 Óptica Geométrica")

        # Tarjeta 1: Índice
        c1 = ctk.CTkFrame(scroll, corner_radius=10); c1.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c1, text="Índice de Refracción (n = c/v)", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=4, pady=10)
        ent_v = self.crear_fila_input(c1, 1, "Velocidad (v):", "Ej. 2e8", "[m/s]", "Velocidad en el medio", "Velocidad a la que viaja la luz en este material.")
        res_n = ctk.CTkLabel(c1, text="n = --", text_color="yellow"); res_n.grid(row=2, column=0, columnspan=4, pady=5)
        ctk.CTkButton(c1, text="Calcular", fg_color="#8d6e1f", hover_color="#6b5317", width=150, command=lambda: self.ejecutar_calculo(MotorModuloA.indice_refraccion, res_n, "n = {:.4f}", ent_v)).grid(row=3, column=0, columnspan=4, pady=10)

        # Tarjeta 2: Snell
        c2 = ctk.CTkFrame(scroll, corner_radius=10); c2.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c2, text="Ley de Snell (Refracción)", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=4, pady=10)
        ent_sn1 = self.crear_fila_input(c2, 1, "Índice Origen (n1):", "Ej. 1.48", "[Típico: 1.4 - 1.5]", "Índice n1", "Índice de refracción del medio 1 (ej. Núcleo).")
        ent_sn2 = self.crear_fila_input(c2, 2, "Índice Destino (n2):", "Ej. 1.46", "[Típico: 1.4 - 1.5]", "Índice n2", "Índice de refracción del medio 2 (ej. Revestimiento).")
        ent_th1 = self.crear_fila_input(c2, 3, "Ángulo de Incidencia (θ1):", "Ej. 30.0", "[Grados °]", "Ángulo de Incidencia", "Ángulo en grados con el que la luz golpea la interfaz.")
        res_snell = ctk.CTkLabel(c2, text="θ2 = -- °", text_color="yellow"); res_snell.grid(row=4, column=0, columnspan=4, pady=5)
        ctk.CTkButton(c2, text="Calcular Snell", fg_color="#8d6e1f", hover_color="#6b5317", width=150, command=lambda: self.ejecutar_calculo(MotorModuloA.angulo_refraccion_snell, res_snell, "θ2 = {:.2f} °", ent_sn1, ent_sn2, ent_th1)).grid(row=5, column=0, columnspan=4, pady=10)

        # Tarjeta 3: Parámetros del Núcleo
        c3 = ctk.CTkFrame(scroll, corner_radius=10); c3.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c3, text="Parámetros del Núcleo y Revestimiento", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=4, pady=10)
        ent_pn1 = self.crear_fila_input(c3, 1, "Índice Núcleo (n1):", "Ej. 1.48", "[Debe ser > n2]", "Índice del Núcleo", "Para que la luz se guíe, n1 > n2.")
        ent_pn2 = self.crear_fila_input(c3, 2, "Índice Revestimiento (n2):", "Ej. 1.46", "[Debe ser < n1]", "Índice del Revestimiento", "Índice del material exterior.")
        res_param = ctk.CTkLabel(c3, text="Áng. Crítico: -- ° | NA: -- | Δ: --", text_color="yellow"); res_param.grid(row=3, column=0, columnspan=4, pady=5)
        ctk.CTkButton(c3, text="Calcular Parámetros", fg_color="#8d6e1f", hover_color="#6b5317", width=150, command=lambda: self.calc_parametros_nucleo(ent_pn1, ent_pn2, res_param)).grid(row=4, column=0, columnspan=4, pady=10)

    def calc_parametros_nucleo(self, en1, en2, lbl):
        try:
            n1, n2 = float(en1.get()), float(en2.get())
            ac = MotorModuloA.angulo_critico(n1, n2)
            na = MotorModuloA.apertura_numerica(n1, n2)
            delta = MotorModuloA.diferencia_indice_relativa(n1, n2)
            lbl.configure(text=f"Áng. Crítico: {ac:.2f} ° | NA: {na:.4f} | Δ: {delta*100:.2f}%")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def vista_moda_parametros(self):
        scroll = self.crear_area_scroll("🔢 Número V y Modos")

        # Tarjeta 1: Número V
        c1 = ctk.CTkFrame(scroll, corner_radius=10); c1.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c1, text="Frecuencia Normalizada (V) y Modos", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=4, pady=10)
        ent_a = self.crear_fila_input(c1, 1, "Radio Núcleo (a):", "Ej. 25.0", "[µm]", "Radio de Núcleo", "Mitad del diámetro interior de la fibra.")
        ent_lam = self.crear_fila_input(c1, 2, "Longitud Onda (λ):", "Ej. 1.3", "[µm]", "Longitud de Onda", "Longitud de onda de operación (ej. 0.85, 1.3, 1.55 µm).")
        ent_na = self.crear_fila_input(c1, 3, "Apertura Numérica (NA):", "Ej. 0.22", "[Adimensional]", "Apertura Numérica", "Capacidad de recolección de luz calculada previamente.")
        ent_alf = self.crear_fila_input(c1, 4, "Perfil de Índice (α):", "Ej. 2.0", "[Opcional - para Gradual]", "Perfil de Índice", "Forma del perfil para fibras de índice gradual (ej. 2.0 para parabólico).")
        
        res_v = ctk.CTkLabel(c1, text="V = -- | Modos: --", text_color="yellow"); res_v.grid(row=5, column=0, columnspan=4, pady=5)
        ctk.CTkButton(c1, text="Calcular V", fg_color="#8d6e1f", hover_color="#6b5317", width=150, command=lambda: self.calc_v_y_modos(ent_a, ent_lam, ent_na, ent_alf, res_v)).grid(row=6, column=0, columnspan=4, pady=10)

        # Tarjeta 2: Radio Modal
        c2 = ctk.CTkFrame(scroll, corner_radius=10); c2.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c2, text="Radio del Campo Modal (Spot Size w0)", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=4, pady=10)
        ent_wa = self.crear_fila_input(c2, 1, "Radio Núcleo (a):", "Ej. 4.0", "[µm]", "Radio de Núcleo", "Radio usado típicamente en fibras monomodo.")
        ent_wv = self.crear_fila_input(c2, 2, "Número V:", "Ej. 2.0", "[Adimensional]", "Número V", "Debe ser > 0.")
        
        res_w = ctk.CTkLabel(c2, text="w0 = -- µm", text_color="yellow"); res_w.grid(row=3, column=0, columnspan=4, pady=5)
        ctk.CTkButton(c2, text="Calcular Spot Size", fg_color="#8d6e1f", hover_color="#6b5317", width=150, command=lambda: self.ejecutar_calculo(MotorModuloA.radio_campo_modal, res_w, "w0 = {:.4f} µm", ent_wa, ent_wv)).grid(row=4, column=0, columnspan=4, pady=10)

    def calc_v_y_modos(self, ea, el, ena, ealf, lbl):
        try:
            a, lam, na = float(ea.get()), float(el.get()), float(ena.get())
            v = MotorModuloA.frecuencia_normalizada_v(a, lam, na)
            m_esc = MotorModuloA.modos_guiados_escalonado(v)
            m_grad = "--"
            if ealf.get() != "":
                m_grad = MotorModuloA.modos_guiados_gradual(v, float(ealf.get()))
            lbl.configure(text=f"V = {v:.4f} | Modos Escalonados: {m_esc} | Modos Graduales: {m_grad}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def vista_moda_dispersion(self):
        scroll = self.crear_area_scroll("⏱️ Dispersión y Retardos")

        # Tarjeta 1: Retardo
        c1 = ctk.CTkFrame(scroll, corner_radius=10); c1.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c1, text="Retardo Modal (Fibra Escalonada)", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=4, pady=10)
        ent_rl = self.crear_fila_input(c1, 1, "Longitud (L):", "Ej. 1000", "[Metros]", "Longitud", "Longitud física de la fibra en metros.")
        ent_rn1 = self.crear_fila_input(c1, 2, "Índice Núcleo (n1):", "Ej. 1.48", "[Adimensional]", "Índice n1", "Índice de refracción del núcleo.")
        ent_rdelta = self.crear_fila_input(c1, 3, "Diferencia Relativa (Δ):", "Ej. 0.01", "[Decimal (No %)]", "Diferencia Relativa", "Calculada como (n1-n2)/n1.")
        
        res_ret = ctk.CTkLabel(c1, text="ΔT = -- s", text_color="yellow"); res_ret.grid(row=4, column=0, columnspan=4, pady=5)
        ctk.CTkButton(c1, text="Calcular Retardo", fg_color="#8d6e1f", hover_color="#6b5317", width=150, command=lambda: self.ejecutar_calculo(MotorModuloA.retardo_modal_escalonado, res_ret, "ΔT = {:.3e} s", ent_rl, ent_rn1, ent_rdelta)).grid(row=5, column=0, columnspan=4, pady=10)

        # Tarjeta 2: Dispersión Cromática
        c2 = ctk.CTkFrame(scroll, corner_radius=10); c2.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c2, text="Ensanchamiento Total (Dispersión Cromática)", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=4, pady=10)
        ent_ed = self.crear_fila_input(c2, 1, "Dispersión (D):", "Ej. 17.0", "[ps/(nm·km)]", "Coeficiente D", "Ensanchamiento por unidad de longitud y espectro.")
        ent_el = self.crear_fila_input(c2, 2, "Longitud (L):", "Ej. 50.0", "[km]", "Longitud", "Longitud en kilómetros.")
        ent_esig = self.crear_fila_input(c2, 3, "Ancho Espectral (σ_λ):", "Ej. 2.0", "[nm]", "Ancho Espectral", "Ancho espectral de la fuente de luz en nanómetros.")
        
        res_ens = ctk.CTkLabel(c2, text="σ = -- ps", text_color="yellow"); res_ens.grid(row=4, column=0, columnspan=4, pady=5)
        ctk.CTkButton(c2, text="Calcular Ensanchamiento", fg_color="#8d6e1f", hover_color="#6b5317", width=150, command=lambda: self.ejecutar_calculo(MotorModuloA.ensanchamiento_total, res_ens, "σ = {:.2f} ps", ent_ed, ent_el, ent_esig)).grid(row=5, column=0, columnspan=4, pady=10)

        # Tarjeta 3: PMD
        c3 = ctk.CTkFrame(scroll, corner_radius=10); c3.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c3, text="Dispersión por Modo de Polarización (PMD)", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=4, pady=10)
        ent_dpmd = self.crear_fila_input(c3, 1, "Coeficiente D_PMD:", "Ej. 0.5", "[ps/sqrt(km)]", "Coeficiente PMD", "Coeficiente típico de la fibra para PMD.")
        ent_pl = self.crear_fila_input(c3, 2, "Longitud (L):", "Ej. 100.0", "[km]", "Longitud", "Longitud de la fibra en km.")
        
        res_pmd = ctk.CTkLabel(c3, text="Δτ_PMD = -- ps", text_color="yellow"); res_pmd.grid(row=3, column=0, columnspan=4, pady=5)
        ctk.CTkButton(c3, text="Calcular PMD", fg_color="#8d6e1f", hover_color="#6b5317", width=150, command=lambda: self.ejecutar_calculo(MotorModuloA.dispersion_polarizacion_pmd, res_pmd, "Δτ_PMD = {:.4f} ps", ent_dpmd, ent_pl)).grid(row=4, column=0, columnspan=4, pady=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()