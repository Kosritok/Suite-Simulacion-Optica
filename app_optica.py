import customtkinter as ctk
from tkinter import messagebox

# Importamos los dos motores matemáticos
from motor_optico import MotorCalculoOptico
from motor_modulo_a import MotorModuloA

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Suite de Simulación Electrónica y Óptica")
        self.geometry("1100x750") # Un poco más ancho para acomodar todo
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

        # --- BOTÓN TOGGLE: MÓDULO BASE ---
        self.menu_base_visible = True
        self.btn_toggle_base = ctk.CTkButton(self.sidebar_frame, text="▼ MÓDULO ÓPTICO BASE", anchor="w", font=ctk.CTkFont(weight="bold"), fg_color="transparent", hover_color="gray30", command=self.toggle_menu_base)
        self.btn_toggle_base.grid(row=2, column=0, padx=10, pady=(15, 5), sticky="ew")

        self.frame_sub_base = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.frame_sub_base.grid(row=3, column=0, sticky="ew", padx=15)
        
        ctk.CTkButton(self.frame_sub_base, text="📉 Atenuación", anchor="w", fg_color="transparent", hover_color="gray30", command=self.vista_calculo_atenuacion).pack(fill="x", pady=2)
        ctk.CTkButton(self.frame_sub_base, text="🎯 Eficiencia", anchor="w", fg_color="transparent", hover_color="gray30", command=self.vista_calculo_eficiencia).pack(fill="x", pady=2)
        ctk.CTkButton(self.frame_sub_base, text="⚡ Power Budget", anchor="w", fg_color="transparent", hover_color="gray30", command=self.vista_presupuesto_potencia).pack(fill="x", pady=2)

        # --- BOTÓN TOGGLE: MÓDULO A ---
        self.menu_moda_visible = False
        self.btn_toggle_moda = ctk.CTkButton(self.sidebar_frame, text="▶ MÓDULO A: DISPERSIÓN", anchor="w", font=ctk.CTkFont(weight="bold"), fg_color="transparent", hover_color="#6b5317", text_color="#d4af37", command=self.toggle_menu_moda)
        self.btn_toggle_moda.grid(row=4, column=0, padx=10, pady=(15, 5), sticky="ew")

        self.frame_sub_moda = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        # No lo ubicamos en el grid todavía porque inicia cerrado
        
        ctk.CTkButton(self.frame_sub_moda, text="📐 Óptica Geométrica", anchor="w", fg_color="transparent", hover_color="#6b5317", command=self.vista_moda_geometrica).pack(fill="x", pady=2)
        ctk.CTkButton(self.frame_sub_moda, text="🔢 Número V y Modos", anchor="w", fg_color="transparent", hover_color="#6b5317", command=self.vista_moda_parametros).pack(fill="x", pady=2)
        ctk.CTkButton(self.frame_sub_moda, text="⏱️ Dispersión y Retardos", anchor="w", fg_color="transparent", hover_color="#6b5317", command=self.vista_moda_dispersion).pack(fill="x", pady=2)

        # --- MÓDULO B (Futuro) ---
        ctk.CTkLabel(self.sidebar_frame, text="MÓDULOS FUTUROS", font=ctk.CTkFont(size=11, weight="bold"), text_color="gray").grid(row=8, column=0, padx=20, pady=(20, 5), sticky="w")
        ctk.CTkButton(self.sidebar_frame, text="🔒 Módulo B", anchor="w", state="disabled", fg_color="transparent").grid(row=9, column=0, padx=10, pady=(5, 20), sticky="ew")

        # --- ÁREA PRINCIPAL ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=20)
        self.mostrar_inicio()

    # ==========================================
    # LÓGICA DEL MENÚ ACORDEÓN
    # ==========================================
    def toggle_menu_base(self):
        if not self.menu_base_visible:
            # Abrir Base
            self.frame_sub_base.grid(row=3, column=0, sticky="ew", padx=15)
            self.btn_toggle_base.configure(text="▼ MÓDULO ÓPTICO BASE")
            self.menu_base_visible = True
            # Cerrar Mod A
            self.frame_sub_moda.grid_remove()
            self.btn_toggle_moda.configure(text="▶ MÓDULO A: DISPERSIÓN")
            self.menu_moda_visible = False

    def toggle_menu_moda(self):
        if not self.menu_moda_visible:
            # Abrir Mod A
            self.frame_sub_moda.grid(row=5, column=0, sticky="ew", padx=15)
            self.btn_toggle_moda.configure(text="▼ MÓDULO A: DISPERSIÓN")
            self.menu_moda_visible = True
            # Cerrar Base
            self.frame_sub_base.grid_remove()
            self.btn_toggle_base.configure(text="▶ MÓDULO ÓPTICO BASE")
            self.menu_base_visible = False

    def limpiar_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def mostrar_inicio(self):
        self.limpiar_main_frame()
        ctk.CTkLabel(self.main_frame, text="Bienvenido a ÓpticaSuite Pro", font=ctk.CTkFont(size=28, weight="bold")).pack(pady=(50, 10))
        ctk.CTkLabel(self.main_frame, text="Expande los módulos en la barra lateral para ver los cálculos disponibles.", text_color="gray", font=ctk.CTkFont(size=16)).pack(pady=10)

    # ==========================================
    # VISTAS DEL MÓDULO ÓPTICO BASE (Resumidas para ahorrar espacio)
    # ==========================================
    def vista_calculo_atenuacion(self):
        self.limpiar_main_frame()
        ctk.CTkLabel(self.main_frame, text="📉 Cálculo de Atenuación", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", pady=(0, 20))
        card = ctk.CTkFrame(self.main_frame, corner_radius=10); card.pack(fill="x", pady=10, ipady=10)
        ctk.CTkLabel(card, text="P_in (mW):").grid(row=0, column=0, padx=20, pady=10); ent_pin = ctk.CTkEntry(card); ent_pin.grid(row=0, column=1)
        ctk.CTkLabel(card, text="P_out (mW):").grid(row=1, column=0, padx=20, pady=10); ent_pout = ctk.CTkEntry(card); ent_pout.grid(row=1, column=1)
        ctk.CTkLabel(card, text="Distancia (km):").grid(row=2, column=0, padx=20, pady=10); ent_z = ctk.CTkEntry(card); ent_z.grid(row=2, column=1)
        res = ctk.CTkLabel(self.main_frame, text="Atenuación: -- dB/km", font=ctk.CTkFont(size=20, weight="bold")); res.pack(pady=20)
        ctk.CTkButton(self.main_frame, text="Calcular", command=lambda: self.ejecutar_base(MotorCalculoOptico.calcular_atenuacion_db_km, res, "Atenuación: {:.4f} dB/km", ent_pin, ent_pout, ent_z)).pack()

    def vista_calculo_eficiencia(self):
        self.limpiar_main_frame()
        ctk.CTkLabel(self.main_frame, text="🎯 Eficiencia de Acoplamiento", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", pady=(0, 20))
        card = ctk.CTkFrame(self.main_frame, corner_radius=10); card.pack(fill="x", pady=10, ipady=10)
        ctk.CTkLabel(card, text="Radio rs (µm):").grid(row=0, column=0, padx=20, pady=10); ent_rs = ctk.CTkEntry(card); ent_rs.grid(row=0, column=1)
        ctk.CTkLabel(card, text="Radio a (µm):").grid(row=1, column=0, padx=20, pady=10); ent_a = ctk.CTkEntry(card); ent_a.grid(row=1, column=1)
        ctk.CTkLabel(card, text="NA:").grid(row=2, column=0, padx=20, pady=10); ent_na = ctk.CTkEntry(card); ent_na.grid(row=2, column=1)
        res = ctk.CTkLabel(self.main_frame, text="Eficiencia (η): --", font=ctk.CTkFont(size=20, weight="bold")); res.pack(pady=20)
        ctk.CTkButton(self.main_frame, text="Calcular", command=lambda: self.ejecutar_base(MotorCalculoOptico.eficiencia_acoplamiento, res, "Eficiencia: {:.4f}", ent_rs, ent_a, ent_na)).pack()

    def vista_presupuesto_potencia(self):
        self.limpiar_main_frame()
        ctk.CTkLabel(self.main_frame, text="⚡ Presupuesto de Potencia", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", pady=(0, 10))
        card = ctk.CTkFrame(self.main_frame, corner_radius=10); card.pack(fill="x", pady=10)
        ctk.CTkLabel(card, text="P Tx (dBm):").grid(row=0, column=0, padx=10, pady=5); ent_tx = ctk.CTkEntry(card); ent_tx.grid(row=0, column=1)
        ctk.CTkLabel(card, text="P Rx (dBm):").grid(row=1, column=0, padx=10, pady=5); ent_rx = ctk.CTkEntry(card); ent_rx.grid(row=1, column=1)
        ctk.CTkLabel(card, text="Cable (dB):").grid(row=2, column=0, padx=10, pady=5); ent_cab = ctk.CTkEntry(card); ent_cab.grid(row=2, column=1)
        ctk.CTkLabel(card, text="Empalmes (dB):").grid(row=3, column=0, padx=10, pady=5); ent_emp = ctk.CTkEntry(card); ent_emp.grid(row=3, column=1)
        ctk.CTkLabel(card, text="Conectores (dB):").grid(row=4, column=0, padx=10, pady=5); ent_con = ctk.CTkEntry(card); ent_con.grid(row=4, column=1)
        res = ctk.CTkLabel(self.main_frame, text="Margen: -- dB", font=ctk.CTkFont(size=20, weight="bold")); res.pack(pady=15)
        ctk.CTkButton(self.main_frame, text="Calcular", command=lambda: self.ejecutar_base(MotorCalculoOptico.margen_potencia, res, "Margen: {:.2f} dB", ent_tx, ent_rx, ent_cab, ent_emp, ent_con)).pack()

    def ejecutar_base(self, func, lbl, formato, *entradas):
        try:
            valores = [float(e.get()) for e in entradas]
            res = func(*valores)
            lbl.configure(text=formato.format(res))
        except ValueError as e:
            messagebox.showerror("Error", "Ingresa números válidos.")

    # ==========================================
    # VISTAS DEL MÓDULO A (Con Scroll y TODAS las fórmulas)
    # ==========================================
    def crear_area_scroll(self, titulo):
        """Helper para limpiar y crear el área de scroll"""
        self.limpiar_main_frame()
        ctk.CTkLabel(self.main_frame, text=titulo, font=ctk.CTkFont(size=24, weight="bold"), text_color="#d4af37").pack(anchor="w", pady=(0, 10))
        scroll = ctk.CTkScrollableFrame(self.main_frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        return scroll

    # --- MÓDULO A: PANTALLA 1 ---
    def vista_moda_geometrica(self):
        scroll = self.crear_area_scroll("📐 Óptica Geométrica")

        # Tarjeta 1: Índice de Refracción
        c1 = ctk.CTkFrame(scroll, corner_radius=10); c1.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c1, text="Índice de Refracción (n = c/v)", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=3, pady=10)
        ctk.CTkLabel(c1, text="Velocidad v (m/s):").grid(row=1, column=0, padx=10); ent_v = ctk.CTkEntry(c1, placeholder_text="Ej. 2e8"); ent_v.grid(row=1, column=1)
        res_n = ctk.CTkLabel(c1, text="n = --", text_color="yellow"); res_n.grid(row=1, column=2, padx=20)
        ctk.CTkButton(c1, text="Calcular", fg_color="#8d6e1f", hover_color="#6b5317", width=100, command=lambda: self.ejecutar_mod_a(MotorModuloA.indice_refraccion, res_n, "n = {:.4f}", ent_v)).grid(row=1, column=3, padx=10)

        # Tarjeta 2: Ley de Snell
        c2 = ctk.CTkFrame(scroll, corner_radius=10); c2.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c2, text="Ley de Snell (Refracción)", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=3, pady=10)
        ctk.CTkLabel(c2, text="n1:").grid(row=1, column=0); ent_sn1 = ctk.CTkEntry(c2, width=70); ent_sn1.grid(row=1, column=1, padx=5)
        ctk.CTkLabel(c2, text="n2:").grid(row=1, column=2); ent_sn2 = ctk.CTkEntry(c2, width=70); ent_sn2.grid(row=1, column=3, padx=5)
        ctk.CTkLabel(c2, text="θ1 (°):").grid(row=1, column=4); ent_sth1 = ctk.CTkEntry(c2, width=70); ent_sth1.grid(row=1, column=5, padx=5)
        res_snell = ctk.CTkLabel(c2, text="θ2 = -- °", text_color="yellow"); res_snell.grid(row=2, column=0, columnspan=4, pady=10)
        ctk.CTkButton(c2, text="Calcular", fg_color="#8d6e1f", hover_color="#6b5317", width=100, command=lambda: self.ejecutar_mod_a(MotorModuloA.angulo_refraccion_snell, res_snell, "θ2 = {:.2f} °", ent_sn1, ent_sn2, ent_sth1)).grid(row=2, column=4, columnspan=2)

        # Tarjeta 3: Parámetros del Núcleo
        c3 = ctk.CTkFrame(scroll, corner_radius=10); c3.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c3, text="Parámetros del Núcleo y Revestimiento", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=3, pady=10)
        ctk.CTkLabel(c3, text="Índice n1:").grid(row=1, column=0); ent_pn1 = ctk.CTkEntry(c3); ent_pn1.grid(row=1, column=1, padx=10)
        ctk.CTkLabel(c3, text="Índice n2:").grid(row=2, column=0); ent_pn2 = ctk.CTkEntry(c3); ent_pn2.grid(row=2, column=1, padx=10, pady=5)
        res_param = ctk.CTkLabel(c3, text="Áng. Crítico: -- °\nNA: --\nΔ: --", text_color="yellow", justify="left"); res_param.grid(row=1, column=2, rowspan=2, padx=20)
        ctk.CTkButton(c3, text="Calcular", fg_color="#8d6e1f", hover_color="#6b5317", width=100, command=lambda: self.calc_parametros_nucleo(ent_pn1, ent_pn2, res_param)).grid(row=1, column=3, rowspan=2)

    def calc_parametros_nucleo(self, en1, en2, lbl):
        try:
            n1, n2 = float(en1.get()), float(en2.get())
            ac = MotorModuloA.angulo_critico(n1, n2)
            na = MotorModuloA.apertura_numerica(n1, n2)
            delta = MotorModuloA.diferencia_indice_relativa(n1, n2)
            lbl.configure(text=f"Áng. Crítico: {ac:.2f} °\nNA: {na:.4f}\nΔ: {delta:.4f} ({delta*100:.2f}%)")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # --- MÓDULO A: PANTALLA 2 ---
    def vista_moda_parametros(self):
        scroll = self.crear_area_scroll("🔢 Número V y Modos")

        # Tarjeta 1: Número V y Modos
        c1 = ctk.CTkFrame(scroll, corner_radius=10); c1.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c1, text="Frecuencia Normalizada (V) y Modos", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=3, pady=10)
        ctk.CTkLabel(c1, text="Radio a (µm):").grid(row=1, column=0, padx=10); ent_a = ctk.CTkEntry(c1, width=80); ent_a.grid(row=1, column=1, pady=5)
        ctk.CTkLabel(c1, text="Long. Onda λ (µm):").grid(row=2, column=0, padx=10); ent_lam = ctk.CTkEntry(c1, width=80); ent_lam.grid(row=2, column=1, pady=5)
        ctk.CTkLabel(c1, text="Apertura NA:").grid(row=3, column=0, padx=10); ent_na = ctk.CTkEntry(c1, width=80); ent_na.grid(row=3, column=1, pady=5)
        ctk.CTkLabel(c1, text="Perfil α (Opcional):").grid(row=4, column=0, padx=10); ent_alf = ctk.CTkEntry(c1, width=80, placeholder_text="Ej. 2.0"); ent_alf.grid(row=4, column=1, pady=5)
        res_v = ctk.CTkLabel(c1, text="V = --\nModos Escalonado = --\nModos Gradual = --", text_color="yellow", justify="left"); res_v.grid(row=1, column=2, rowspan=3, padx=20)
        ctk.CTkButton(c1, text="Calcular", fg_color="#8d6e1f", hover_color="#6b5317", width=100, command=lambda: self.calc_v_y_modos(ent_a, ent_lam, ent_na, ent_alf, res_v)).grid(row=4, column=2, padx=10)

        # Tarjeta 2: Radio Campo Modal
        c2 = ctk.CTkFrame(scroll, corner_radius=10); c2.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c2, text="Radio del Campo Modal (Spot Size w0)", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=3, pady=10)
        ctk.CTkLabel(c2, text="Radio a (µm):").grid(row=1, column=0, padx=10); ent_wa = ctk.CTkEntry(c2); ent_wa.grid(row=1, column=1)
        ctk.CTkLabel(c2, text="Número V:").grid(row=2, column=0, padx=10); ent_wv = ctk.CTkEntry(c2); ent_wv.grid(row=2, column=1, pady=5)
        res_w = ctk.CTkLabel(c2, text="w0 = -- µm", text_color="yellow"); res_w.grid(row=1, column=2, rowspan=2, padx=20)
        ctk.CTkButton(c2, text="Calcular", fg_color="#8d6e1f", hover_color="#6b5317", width=100, command=lambda: self.ejecutar_mod_a(MotorModuloA.radio_campo_modal, res_w, "w0 = {:.4f} µm", ent_wa, ent_wv)).grid(row=1, column=3, rowspan=2)

    def calc_v_y_modos(self, ea, el, ena, ealf, lbl):
        try:
            a, lam, na = float(ea.get()), float(el.get()), float(ena.get())
            v = MotorModuloA.frecuencia_normalizada_v(a, lam, na)
            m_esc = MotorModuloA.modos_guiados_escalonado(v)
            m_grad = "--"
            if ealf.get() != "":
                m_grad = MotorModuloA.modos_guiados_gradual(v, float(ealf.get()))
            lbl.configure(text=f"V = {v:.4f}\nModos Escalonado = {m_esc}\nModos Gradual = {m_grad}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # --- MÓDULO A: PANTALLA 3 ---
    def vista_moda_dispersion(self):
        scroll = self.crear_area_scroll("⏱️ Dispersión y Retardos")

        # Tarjeta 1: Retardo Modal
        c1 = ctk.CTkFrame(scroll, corner_radius=10); c1.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c1, text="Retardo Modal (Fibra Escalonada)", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=3, pady=10)
        ctk.CTkLabel(c1, text="Long. L (m):").grid(row=1, column=0, padx=5); ent_rl = ctk.CTkEntry(c1, width=70); ent_rl.grid(row=1, column=1)
        ctk.CTkLabel(c1, text="n1:").grid(row=1, column=2, padx=5); ent_rn1 = ctk.CTkEntry(c1, width=70); ent_rn1.grid(row=1, column=3)
        ctk.CTkLabel(c1, text="Δ:").grid(row=1, column=4, padx=5); ent_rdelta = ctk.CTkEntry(c1, width=70); ent_rdelta.grid(row=1, column=5)
        res_ret = ctk.CTkLabel(c1, text="ΔT = -- s", text_color="yellow"); res_ret.grid(row=2, column=0, columnspan=4, pady=10)
        ctk.CTkButton(c1, text="Calcular", fg_color="#8d6e1f", hover_color="#6b5317", width=100, command=lambda: self.ejecutar_mod_a(MotorModuloA.retardo_modal_escalonado, res_ret, "ΔT = {:.3e} s", ent_rl, ent_rn1, ent_rdelta)).grid(row=2, column=4, columnspan=2)

        # Tarjeta 2: Dispersión Cromática
        c2 = ctk.CTkFrame(scroll, corner_radius=10); c2.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c2, text="Ensanchamiento Total (Dispersión Cromática)", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=3, pady=10)
        ctk.CTkLabel(c2, text="D (ps/nm·km):").grid(row=1, column=0, padx=5); ent_ed = ctk.CTkEntry(c2, width=70); ent_ed.grid(row=1, column=1)
        ctk.CTkLabel(c2, text="L (km):").grid(row=1, column=2, padx=5); ent_el = ctk.CTkEntry(c2, width=70); ent_el.grid(row=1, column=3)
        ctk.CTkLabel(c2, text="σ_λ (nm):").grid(row=1, column=4, padx=5); ent_esig = ctk.CTkEntry(c2, width=70); ent_esig.grid(row=1, column=5)
        res_ens = ctk.CTkLabel(c2, text="σ = -- ps", text_color="yellow"); res_ens.grid(row=2, column=0, columnspan=4, pady=10)
        ctk.CTkButton(c2, text="Calcular", fg_color="#8d6e1f", hover_color="#6b5317", width=100, command=lambda: self.ejecutar_mod_a(MotorModuloA.ensanchamiento_total, res_ens, "σ = {:.2f} ps", ent_ed, ent_el, ent_esig)).grid(row=2, column=4, columnspan=2)

        # Tarjeta 3: PMD
        c3 = ctk.CTkFrame(scroll, corner_radius=10); c3.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c3, text="Dispersión por Modo de Polarización (PMD)", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=3, pady=10)
        ctk.CTkLabel(c3, text="D_PMD:").grid(row=1, column=0, padx=10); ent_dpmd = ctk.CTkEntry(c3); ent_dpmd.grid(row=1, column=1)
        ctk.CTkLabel(c3, text="L (km):").grid(row=2, column=0, padx=10); ent_pl = ctk.CTkEntry(c3); ent_pl.grid(row=2, column=1, pady=5)
        res_pmd = ctk.CTkLabel(c3, text="Δτ_PMD = --", text_color="yellow"); res_pmd.grid(row=1, column=2, rowspan=2, padx=20)
        ctk.CTkButton(c3, text="Calcular", fg_color="#8d6e1f", hover_color="#6b5317", width=100, command=lambda: self.ejecutar_mod_a(MotorModuloA.dispersion_polarizacion_pmd, res_pmd, "Δτ_PMD = {:.4f}", ent_dpmd, ent_pl)).grid(row=1, column=3, rowspan=2)

    def ejecutar_mod_a(self, func, lbl, formato, *entradas):
        try:
            valores = [float(e.get()) for e in entradas]
            res = func(*valores)
            lbl.configure(text=formato.format(res))
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", "Revisa que los campos no estén vacíos y contengan solo números.")

if __name__ == "__main__":
    app = App()
    app.mainloop()