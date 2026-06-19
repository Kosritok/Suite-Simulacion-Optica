import customtkinter as ctk
from tkinter import messagebox
import math

# Intento de importar winsound (nativo en Windows) para feedback auditivo
try:
    import winsound
except ImportError:
    winsound = None

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from motor_optico import MotorCalculoOptico
from motor_modulo_a import MotorModuloA
from motor_modulo_b import MotorModuloB
from motor_grafico import MotorGrafico
from motor_modulacion import MotorModulacion  # <--- IMPORTACIÓN DEL NUEVO MOTOR

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Suite de Simulación Electrónica y Óptica")
        self.geometry("1450x900")
        self.resizable(False, False)
        
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
        ctk.CTkButton(self.frame_sub_base, text="⚡ Presupuesto de Potencia", anchor="w", font=btn_font, fg_color="transparent", hover_color="gray30", command=self.vista_presupuesto_potencia).pack(fill="x", pady=2)
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

        # --- MOTOR MATEMÁTICO ---
        self.menu_modb_visible = False
        self.btn_toggle_modb = ctk.CTkButton(self.sidebar_frame, text="▶ Motor Matemático", anchor="w", font=ctk.CTkFont(size=15, weight="bold"), fg_color="transparent", hover_color="#1a5a40", text_color="#66bb6a", command=self.toggle_menu_modb)
        self.btn_toggle_modb.grid(row=6, column=0, padx=10, pady=(15, 5), sticky="ew")

        self.frame_sub_modb = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        ctk.CTkButton(self.frame_sub_modb, text="🔢 Frecuencia y Modos", anchor="w", font=btn_font, fg_color="transparent", hover_color="#1a5a40", command=self.vista_modb_frecuencia).pack(fill="x", pady=2)
        ctk.CTkButton(self.frame_sub_modb, text="✂️ Longitud de Corte", anchor="w", font=btn_font, fg_color="transparent", hover_color="#1a5a40", command=self.vista_modb_corte).pack(fill="x", pady=2)
        ctk.CTkButton(self.frame_sub_modb, text="⭕ Campo Modal (MFD)", anchor="w", font=btn_font, fg_color="transparent", hover_color="#1a5a40", command=self.vista_modb_mfd).pack(fill="x", pady=2)

        # --- MOTOR DE MODULACIÓN ---
        self.menu_modc_visible = False
        self.btn_toggle_modc = ctk.CTkButton(self.sidebar_frame, text="▶ Motor de Modulación", anchor="w", font=ctk.CTkFont(size=15, weight="bold"), fg_color="transparent", hover_color="#4a148c", text_color="#ab47bc", command=self.toggle_menu_modc)
        self.btn_toggle_modc.grid(row=8, column=0, padx=10, pady=(15, 5), sticky="ew")

        self.frame_sub_modc = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        ctk.CTkButton(self.frame_sub_modc, text="📈 Modulación ASK", anchor="w", font=btn_font, fg_color="transparent", hover_color="#4a148c", command=self.vista_modulacion_ask).pack(fill="x", pady=2)
        ctk.CTkButton(self.frame_sub_modc, text="📉 Modulación PSK", anchor="w", font=btn_font, fg_color="transparent", hover_color="#4a148c", command=self.vista_modulacion_psk).pack(fill="x", pady=2)
        ctk.CTkButton(self.frame_sub_modc, text="📊 Modulación FSK", anchor="w", font=btn_font, fg_color="transparent", hover_color="#4a148c", command=self.vista_modulacion_fsk).pack(fill="x", pady=2)
        ctk.CTkButton(self.frame_sub_modc, text="🔢 Modulación DPSK", anchor="w", font=btn_font, fg_color="transparent", hover_color="#4a148c", command=self.vista_modulacion_dpsk).pack(fill="x", pady=2)

        # --- ÁREA PRINCIPAL ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=20)
        self.mostrar_inicio()

    # ==========================================
    # FUNCIONES DE AYUDA Y HERRAMIENTAS VISUALES
    # ==========================================
    def abrir_ayuda(self, concepto, definicion):
        ventana_ayuda = ctk.CTkToplevel(self)
        ventana_ayuda.title(f"Ayuda: {concepto}")
        ventana_ayuda.geometry("500x280")
        ventana_ayuda.attributes("-topmost", True) 
        ctk.CTkLabel(ventana_ayuda, text=concepto, font=("Arial", 18, "bold")).pack(pady=(20, 10))
        ctk.CTkLabel(ventana_ayuda, text=definicion, font=("Arial", 14), wraplength=450, justify="left").pack(padx=20, pady=10)
        
        ctk.CTkLabel(ventana_ayuda, 
                     text="Para más información y derivación de fórmulas, consulte el marco teórico.", 
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

    def crear_tarjeta_dividida(self, padre):
        card = ctk.CTkFrame(padre, corner_radius=10)
        card.pack(fill="x", pady=(10, 5), ipady=5)
        
        panel_izquierdo = ctk.CTkFrame(card, fg_color="transparent")
        panel_izquierdo.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        panel_derecho = ctk.CTkFrame(card, fg_color="#212121", width=450) # Ligeramente más ancho para las 3 gráficas
        panel_derecho.pack(side="right", fill="both", padx=10, pady=10)
        panel_derecho.pack_propagate(False) 
        
        ctk.CTkLabel(panel_derecho, text="[ La gráfica adaptativa aparecerá aquí ]", text_color="gray").pack(expand=True)
        return card, panel_izquierdo, panel_derecho

    def crear_panel_formula(self, padre, formula_str, descripcion_variables):
        frame_form = ctk.CTkFrame(padre, fg_color="#2b2b2b", corner_radius=8)
        frame_form.pack(fill="x", padx=10, pady=(0, 20))
        
        ctk.CTkLabel(frame_form, text=formula_str, font=ctk.CTkFont(family="Cambria Math", size=22, weight="bold"), text_color="#d4af37").pack(pady=(10, 5))
        ctk.CTkLabel(frame_form, text=descripcion_variables, font=ctk.CTkFont(size=13), text_color="gray70").pack(pady=(0, 10))

    def reproducir_exito(self):
        if winsound:
            winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC)

    def mostrar_grafica(self, frame_destino, figura_matplotlib):
        for widget in frame_destino.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(figura_matplotlib, master=frame_destino)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
        plt.close(figura_matplotlib)

    def limpiar_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def mostrar_inicio(self):
        self.limpiar_main_frame()
        ctk.CTkLabel(self.main_frame, text="Bienvenido a ÓpticaSuite Pro", font=ctk.CTkFont(size=34, weight="bold")).pack(pady=(50, 10))
        ctk.CTkLabel(self.main_frame, text="Selecciona un módulo en la barra lateral para comenzar.", text_color="gray", font=ctk.CTkFont(size=18)).pack(pady=10)
        ctk.CTkLabel(self.main_frame, text="¡Deja un campo vacío en las tarjetas OMNI para calcular su valor automáticamente!", text_color="#64b5f6", font=ctk.CTkFont(size=16)).pack(pady=5)

    def crear_area_scroll(self, titulo, color="white"):
        self.limpiar_main_frame()
        ctk.CTkLabel(self.main_frame, text=titulo, font=ctk.CTkFont(size=28, weight="bold"), text_color=color).pack(anchor="w", pady=(0, 10))
        scroll = ctk.CTkScrollableFrame(self.main_frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        return scroll

    # === ACORDEÓN LOGIC ===
    def _cerrar_todos_menos(self, acordeon_mantener):
        # Base
        if acordeon_mantener != "base" and self.menu_base_visible:
            self.frame_sub_base.grid_remove()
            self.btn_toggle_base.configure(text="▶ Motor de Atenuación")
            self.menu_base_visible = False
        # Moda
        if acordeon_mantener != "moda" and self.menu_moda_visible:
            self.frame_sub_moda.grid_remove()
            self.btn_toggle_moda.configure(text="▶ Motor de Dispersión")
            self.menu_moda_visible = False
        # Modb
        if acordeon_mantener != "modb" and self.menu_modb_visible:
            self.frame_sub_modb.grid_remove()
            self.btn_toggle_modb.configure(text="▶ Motor Matemático")
            self.menu_modb_visible = False
        # Modc (Modulación)
        if acordeon_mantener != "modc" and self.menu_modc_visible:
            self.frame_sub_modc.grid_remove()
            self.btn_toggle_modc.configure(text="▶ Motor de Modulación")
            self.menu_modc_visible = False

    def toggle_menu_base(self):
        if not self.menu_base_visible:
            self.frame_sub_base.grid(row=3, column=0, sticky="ew", padx=15)
            self.btn_toggle_base.configure(text="▼ Motor de Atenuación")
            self.menu_base_visible = True
            self._cerrar_todos_menos("base")

    def toggle_menu_moda(self):
        if not self.menu_moda_visible:
            self.frame_sub_moda.grid(row=5, column=0, sticky="ew", padx=15)
            self.btn_toggle_moda.configure(text="▼ Motor de Dispersión")
            self.menu_moda_visible = True
            self._cerrar_todos_menos("moda")

    def toggle_menu_modb(self):
        if not self.menu_modb_visible:
            self.frame_sub_modb.grid(row=7, column=0, sticky="ew", padx=15)
            self.btn_toggle_modb.configure(text="▼ Motor Matemático")
            self.menu_modb_visible = True
            self._cerrar_todos_menos("modb")

    def toggle_menu_modc(self):
        if not self.menu_modc_visible:
            self.frame_sub_modc.grid(row=9, column=0, sticky="ew", padx=15)
            self.btn_toggle_modc.configure(text="▼ Motor de Modulación")
            self.menu_modc_visible = True
            self._cerrar_todos_menos("modc")

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
        scroll = self.crear_area_scroll("📉 Cálculo de Atenuación")
        card, p_izq, p_der = self.crear_tarjeta_dividida(scroll)
        
        ctk.CTkLabel(p_izq, text="⮀ OMNIDIRECCIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        ctk.CTkLabel(p_izq, text="Deja exactamente UN campo vacío para resolver la ecuación.", text_color="#64b5f6", font=ctk.CTkFont(size=13)).grid(row=1, column=0, columnspan=4, pady=(0, 10))

        ent_pin = self.crear_fila_input(p_izq, 2, "Potencia (Pᵢₙ):", "Ej. 1.0", "[mW]", "[Típico: 0.1 a 10]", "Potencia de Entrada (P_in)", "Nivel de potencia óptica inyectada por la fuente transmisora al inicio del enlace de fibra.")
        ent_pout = self.crear_fila_input(p_izq, 3, "Potencia (Pₒᵤₜ):", "Ej. 0.5", "[mW]", "[Debe ser < Pᵢₙ]", "Potencia de Salida (P_out)", "Nivel de potencia óptica medida al final del tramo atenuado.")
        ent_z = self.crear_fila_input(p_izq, 4, "Distancia (z):", "Ej. 20.0", "[km]", "[Típico: 1 a 100]", "Distancia del Enlace (z)", "Longitud física total del cable de fibra óptica a través del cual viaja la señal luminosa.")
        ent_alpha = self.crear_fila_input(p_izq, 5, "Atenuación (α):", "Ej. 0.25", "[dB/km]", "[Típico: 0.2 a 3.0]", "Coeficiente de Atenuación (α)", "Pérdida de potencia intrínseca del material, medida por cada kilómetro recorrido.")

        def resolver_atenuacion():
            ents = {"pin": ent_pin, "pout": ent_pout, "z": ent_z, "alpha": ent_alpha}
            for ent in ents.values(): ent.configure(text_color="white")
            vacios = {k: v for k, v in ents.items() if v.get().strip() == ""}
            
            try:
                llenos = {k: float(v.get()) for k, v in ents.items() if v.get().strip() != ""}
                if len(vacios) != 1: return messagebox.showerror("Error", "Deja exactamente UN campo vacío.")
                inc = list(vacios.keys())[0]
            
                if inc == "alpha": res = MotorCalculoOptico.calcular_atenuacion_db_km(llenos["pin"], llenos["pout"], llenos["z"])
                elif inc == "pout": res = MotorCalculoOptico.calcular_potencia_salida(llenos["pin"], llenos["alpha"], llenos["z"])
                elif inc == "pin": res = MotorCalculoOptico.calcular_potencia_entrada(llenos["pout"], llenos["alpha"], llenos["z"])
                elif inc == "z": res = MotorCalculoOptico.calcular_distancia_atenuacion(llenos["pin"], llenos["pout"], llenos["alpha"])
                
                ents[inc].delete(0, 'end')
                ents[inc].insert(0, f"{res:.4f}")
                ents[inc].configure(text_color="#66bb6a")
                self.reproducir_exito()
                
                fig = MotorGrafico.plot_atenuacion(float(ent_pin.get()), float(ent_alpha.get()), float(ent_z.get()))
                self.mostrar_grafica(p_der, fig)
            except ValueError:
                messagebox.showerror("Error", "Revisa que todos los campos contengan números válidos.")
            except Exception as e: 
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(p_izq, text="Resolver y Graficar", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=resolver_atenuacion).grid(row=6, column=0, columnspan=4, pady=15)
        self.crear_panel_formula(scroll, "P_out = P_in · 10^(-α · z / 10)", "P_out = Potencia Final | P_in = Potencia Inicial | α = Coef. Atenuación | z = Distancia")

    def vista_presupuesto_potencia(self):
        scroll = self.crear_area_scroll("⚡ Presupuesto de Potencia")
        card, p_izq, p_der = self.crear_tarjeta_dividida(scroll)
        
        ctk.CTkLabel(p_izq, text="⮀ OMNIDIRECCIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        ctk.CTkLabel(p_izq, text="Deja exactamente UN campo vacío para resolver.", text_color="#64b5f6", font=ctk.CTkFont(size=13)).grid(row=1, column=0, columnspan=4, pady=(0, 10))

        ent_tx = self.crear_fila_input(p_izq, 2, "Potencia Tx:", "Ej. 3.0", "[dBm]", "[Típico: -10 a 5]", "Potencia de Transmisión (Tx)", "Potencia media acoplada a la fibra óptica por el emisor electrónico (Láser o LED).")
        ent_rx = self.crear_fila_input(p_izq, 3, "Sensibilidad Rx:", "Ej. -32.0", "[dBm]", "[Típico: -40 a -20]", "Sensibilidad de Recepción (Rx)", "Potencia mínima requerida por el fotodetector receptor para interpretar los datos sin errores perceptibles.")
        ent_cab = self.crear_fila_input(p_izq, 4, "Pérdida Cable:", "Ej. 15.0", "[dB]", "[Típico: 0 a 30]", "Pérdida Total del Cable", "Suma completa de la atenuación distribuida a lo largo de toda la longitud física de la fibra.")
        ent_emp = self.crear_fila_input(p_izq, 5, "Empalmes:", "Ej. 1.0", "[dB]", "[Típico: 0.1 a 0.5 c/u]", "Pérdidas por Empalmes", "Suma de las caídas de potencia ocasionadas por uniones permanentes en la fibra (fusión térmica).")
        ent_con = self.crear_fila_input(p_izq, 6, "Conectores:", "Ej. 2.0", "[dB]", "[Típico: 0.5 a 2.0 c/u]", "Pérdidas por Conectores", "Suma de atenuaciones generadas en todas las uniones mecánicas acopladas y desacoplables del sistema.")
        ent_mar = self.crear_fila_input(p_izq, 7, "Margen Sistema:", "Ej. 5.0", "[dB]", "[Seguridad > 3]", "Margen de Seguridad Operativo", "Reserva estática de potencia guardada explícitamente para compensar el envejecimiento futuro de los componentes.")

        def resolver_potencia():
            ents = {"tx": ent_tx, "rx": ent_rx, "cab": ent_cab, "emp": ent_emp, "con": ent_con, "mar": ent_mar}
            for ent in ents.values(): ent.configure(text_color="white")
            vacios = {k: v for k, v in ents.items() if v.get().strip() == ""}
            
            try:
                llenos = {k: float(v.get()) for k, v in ents.items() if v.get().strip() != ""}
                if len(vacios) != 1: return messagebox.showerror("Error", "Deja exactamente UN campo vacío.")
                inc = list(vacios.keys())[0]
            
                if inc == "mar": res = llenos["tx"] - llenos["rx"] - llenos["cab"] - llenos["emp"] - llenos["con"]
                elif inc == "tx": res = llenos["mar"] + llenos["rx"] + llenos["cab"] + llenos["emp"] + llenos["con"]
                elif inc == "rx": res = llenos["tx"] - llenos["mar"] - llenos["cab"] - llenos["emp"] - llenos["con"]
                elif inc == "cab": res = llenos["tx"] - llenos["rx"] - llenos["mar"] - llenos["emp"] - llenos["con"]
                elif inc == "emp": res = llenos["tx"] - llenos["rx"] - llenos["mar"] - llenos["cab"] - llenos["con"]
                elif inc == "con": res = llenos["tx"] - llenos["rx"] - llenos["mar"] - llenos["cab"] - llenos["emp"]
                
                ents[inc].delete(0, 'end'); ents[inc].insert(0, f"{res:.2f}")
                ents[inc].configure(text_color="#66bb6a")
                self.reproducir_exito()
                
                fig = MotorGrafico.plot_presupuesto(float(ent_tx.get()), float(ent_rx.get()), float(ent_cab.get()), float(ent_emp.get()), float(ent_con.get()))
                self.mostrar_grafica(p_der, fig)
            except ValueError:
                messagebox.showerror("Error", "Revisa que todos los campos contengan números válidos.")
            except Exception as e: messagebox.showerror("Error", str(e))

        ctk.CTkButton(p_izq, text="Resolver y Graficar", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=resolver_potencia).grid(row=8, column=0, columnspan=4, pady=15)
        self.crear_panel_formula(scroll, "P_Rx = P_Tx - P_Cable - P_Empalmes - P_Conectores - Margen", "Toda la ecuación se realiza en dominio logarítmico (dB / dBm)")

    def vista_calculo_eficiencia(self):
        scroll = self.crear_area_scroll("🎯 Eficiencia de Acoplamiento")
        
        card = ctk.CTkFrame(scroll, corner_radius=10); card.pack(fill="x", pady=10, ipady=10)
        ctk.CTkLabel(card, text="➔ TRADICIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        ctk.CTkLabel(card, text="Llena TODOS los campos.", text_color="#9e9e9e", font=ctk.CTkFont(size=13)).grid(row=1, column=0, columnspan=4, pady=(0, 10))

        ent_rs = self.crear_fila_input(card, 2, "Radio Fuente (rs):", "Ej. 50.0", "[µm]", "[Típico: 10 a 100]", "Radio de Emisión de la Fuente", "Radio físico que abarca el área activa emisora de luz geométrica de la fuente (Láser o LED).")
        ent_a = self.crear_fila_input(card, 3, "Radio Núcleo (a):", "Ej. 25.0", "[µm]", "[Típico: 4 a 50]", "Radio del Núcleo", "Dimensión de la sección interna de la fibra óptica capacitada para canalizar los fotones de luz.")
        ent_na = self.crear_fila_input(card, 4, "Apertura Num. (NA):", "Ej. 0.22", "[Adim]", "[Típico: 0.1 a 0.3]", "Apertura Numérica", "Parámetro intrínseco de diseño que expresa el nivel de capacidad que tiene el núcleo para capturar e incorporar luz externa.")
        
        res = ctk.CTkLabel(card, text="Eficiencia (η): --", font=ctk.CTkFont(size=24, weight="bold")); res.grid(row=5, column=0, columnspan=4, pady=15)
        ctk.CTkButton(card, text="Calcular Eficiencia", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=lambda: self.ejecutar_calculo_tradicional(MotorCalculoOptico.eficiencia_acoplamiento, res, "Eficiencia: {:.4f}", ent_rs, ent_a, ent_na)).grid(row=6, column=0, columnspan=4, pady=10)
        
        self.crear_panel_formula(scroll, "Si rs ≤ a: η = NA²   |   Si rs > a: η = (a/rs)² · NA²", "rs = Radio de Emisión | a = Radio del Núcleo | NA = Apertura Numérica")

    def vista_base_rayleigh(self):
        scroll = self.crear_area_scroll("✨ Rayleigh y Predicción de Potencias")
        card, p_izq, p_der = self.crear_tarjeta_dividida(scroll)
        
        ctk.CTkLabel(p_izq, text="➔ TRADICIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        ctk.CTkLabel(p_izq, text="Llena TODOS los campos.", text_color="#9e9e9e", font=ctk.CTkFont(size=13)).grid(row=1, column=0, columnspan=4, pady=(0, 10))

        ent_n = self.crear_fila_input(p_izq, 2, "Índice Núcleo (n):", "Ej. 1.46", "[Adim]", "[Típico: 1.44 a 1.48]", "Índice de Refracción", "Índice de refracción estático del material dopado base que constituye el núcleo de la fibra.")
        ent_bt = self.crear_fila_input(p_izq, 3, "Compresibilidad (βₜ):", "Ej. 7e-11", "[cm²/dina]", "[Típico: ~7e-11]", "Compresibilidad Isotérmica", "Característica térmica que define cómo responde estructuralmente el volumen del vidrio cuando está sometido a presión constante.")
        ent_tf = self.crear_fila_input(p_izq, 4, "Temp. Fusión (T_f):", "Ej. 1673", "[K]", "[Típico: 1400 a 1700]", "Temperatura de Fusión/Ficticia", "Registro de la temperatura límite en la cual la sílice derretida de fábrica se cristaliza, encapsulando impurezas.")
        ent_lnm = self.crear_fila_input(p_izq, 5, "Longitud Onda (λ):", "Ej. 850.0", "[nm]", "[Típico: 850, 1310, 1550]", "Longitud de Onda de Operación", "Punto específico en el espectro electromagnético en el que operará la señal óptica introducida.")
        
        res_r = ctk.CTkLabel(p_izq, text="α_Rayleigh = -- dB/km", font=ctk.CTkFont(size=18, weight="bold")); res_r.grid(row=6, column=0, columnspan=4, pady=5)
        
        def calc_rayleigh():
            try:
                self.ejecutar_calculo_tradicional(MotorCalculoOptico.atenuacion_rayleigh_eq37, res_r, "α_Rayleigh = {:.4f} dB/km", ent_n, ent_bt, ent_tf, ent_lnm)
                fig = MotorGrafico.plot_rayleigh(float(ent_lnm.get()))
                self.mostrar_grafica(p_der, fig)
            except Exception as e: pass

        ctk.CTkButton(p_izq, text="Calcular y Graficar", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=calc_rayleigh).grid(row=7, column=0, columnspan=4, pady=10)
        self.crear_panel_formula(scroll, "α_R = (8π³ / 3λ⁴) · (n²-1)² · β_T · K_B · T_f", "λ = Long. onda | n = Índice núcleo | β_T = Compresibilidad | T_f = Temp. Fusión")

    def vista_base_curvaturas(self):
        scroll = self.crear_area_scroll("🔄 Análisis Macro y Microcurvaturas")
        
        # Macrocurvaturas
        c1 = ctk.CTkFrame(scroll, corner_radius=10); c1.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c1, text="Relación de Modos Efectivos (Macrocurvatura) ➔ TRADICIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        
        ent_alf = self.crear_fila_input(c1, 2, "Perfil Índice (α):", "Ej. 2.0", "[Adim]", "[Gradual=2, Escalonado>1000]", "Coeficiente del Perfil de Índice", "Magnitud que describe la forma de la distribución del índice de refracción a través del radio de la fibra.")
        ent_del = self.crear_fila_input(c1, 3, "Dif. Relativa (Δ):", "Ej. 0.01", "[Decimal]", "[Típico: 0.01 a 0.02]", "Diferencia de Índice", "Razón matemática representativa de la diferencia porcentual de índices entre el núcleo central y su revestimiento exterior.")
        ent_a = self.crear_fila_input(c1, 4, "Radio Núcleo (a):", "Ej. 25e-6", "[Metros]", "[Ej. 25e-6]", "Radio del Núcleo", "Longitud desde el centro geométrico de la fibra hasta el borde del núcleo conductor de luz.")
        ent_R = self.crear_fila_input(c1, 5, "Radio Curvatura (R):", "Ej. 0.06", "[Metros]", "[Ej. 0.05 a 0.1]", "Radio de Macrocurvatura", "Medida espacial del arco formado al enrollar o curvar físicamente toda la estructura del cable de fibra.")
        ent_n2 = self.crear_fila_input(c1, 6, "Índice Revest. (n₂):", "Ej. 1.46", "[Adim]", "[Típico: 1.44 a 1.46]", "Índice de Refracción del Revestimiento", "Medida del medio periférico (Cladding) diseñado para bloquear la luz y rebotarla hacia el eje interior.")
        ent_lmet = self.crear_fila_input(c1, 7, "Longitud Onda (λ):", "Ej. 1300.0", "[nm]", "[Ej. 1300.0 nm]", "Longitud de Onda", "Longitud de onda de la señal operativa expresada métricamente.") 
        
        res_macro = ctk.CTkLabel(c1, text="Nₑᶠᶠ / N∞ = --", font=ctk.CTkFont(size=18, weight="bold")); res_macro.grid(row=8, column=0, columnspan=4, pady=5)
        
        def calc_macro():
            try:
                l_metros = float(ent_lmet.get()) * 1e-9 
                res = MotorCalculoOptico.modos_efectivos_curvatura(float(ent_alf.get()), float(ent_del.get()), float(ent_a.get()), float(ent_R.get()), float(ent_n2.get()), l_metros)
                res_macro.configure(text=f"Modos Efectivos: {res:.4f}")
            except Exception as e: messagebox.showerror("Error", str(e))
            
        ctk.CTkButton(c1, text="Calcular Macrocurvatura", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=calc_macro).grid(row=9, column=0, columnspan=4, pady=10)
        self.crear_panel_formula(scroll, "N_eff / N_∞ = 1 - [(α+2)/(2αΔ)] · [ 2a/R + (3 / 2n₂kR)^(2/3) ]", "k = 2π/λ  |  R = Radio de macrocurvatura  |  a = Radio del núcleo")

        # Microcurvaturas
        c2 = ctk.CTkFrame(scroll, corner_radius=10); c2.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c2, text="Factor Reducción (Microcurvatura) ➔ TRADICIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        
        ent_ej = self.crear_fila_input(c2, 2, "Módulo Chaqueta (Eⱼ):", "Ej. 12.0", "[MPa]", "[Típico: 10 a 20]", "Módulo de Young (Chaqueta)", "Nivel de firmeza y resistencia elástica ofrecida por la cubierta plástica secundaria del cableado.")
        ent_eg = self.crear_fila_input(c2, 3, "Módulo Vidrio (E_g):", "Ej. 65.0", "[GPa]", "[Típico: 60 a 75]", "Módulo de Young (Sílice/Vidrio)", "Evaluación de la rigidez estática e inherente de los componentes internos de vidrio dentro de la fibra óptica.")
        ent_ba = self.crear_fila_input(c2, 4, "Relación Radios (b/a):", "Ej. 2.5", "[Adim]", "[Típico: 2.0 a 3.0]", "Relación de Aspecto Geométrico (b/a)", "Cociente resultante de dividir el diámetro absoluto del revestimiento entre el diámetro equivalente del núcleo.")
        ent_del2 = self.crear_fila_input(c2, 5, "Diferencia Relativa (Δ):", "Ej. 0.01", "[Decimal]", "[Típico: 0.01 a 0.02]", "Diferencia de Índice", "Razón representativa de la diferencia porcentual de los índices de refracción primarios.")
        
        res_micro = ctk.CTkLabel(c2, text="Factor de Reducción = --", font=ctk.CTkFont(size=18, weight="bold")); res_micro.grid(row=6, column=0, columnspan=4, pady=5)
        ctk.CTkButton(c2, text="Calcular Microcurvatura", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=lambda: self.ejecutar_calculo_tradicional(MotorCalculoOptico.factor_reduccion_keiser, res_micro, "Factor de Reducción: {:.4f}", ent_ej, ent_eg, ent_ba, ent_del2)).grid(row=7, column=0, columnspan=4, pady=10)
        self.crear_panel_formula(scroll, "F = 1 / [ 1 + 0.5(E_g/E_j) · (b/a)⁴ · Δ³ · 13600 ]", "E_g = Módulo Vidrio | E_j = Módulo Chaqueta | b/a = Relación de aspecto")

    def vista_base_modelos(self):
        scroll = self.crear_area_scroll("📊 Modelos y Dispersión Homologada")
        
        # G.652
        card1, p_izq, p_der = self.crear_tarjeta_dividida(scroll)
        ctk.CTkLabel(p_izq, text="Dispersión G.652 ➔ TRADICIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        
        ent_l = self.crear_fila_input(p_izq, 2, "Longitud Onda (λ):", "Ej. 1550.0", "[nm]", "[Típico: 1200 a 1600]", "Longitud de Onda Transmitida", "Punto específico en el espectro bajo el cual se realizará el análisis de dispersión actual.")
        ent_l0 = self.crear_fila_input(p_izq, 3, "Dispersión Cero (λ₀):", "Ej. 1310.0", "[nm]", "[Típico: 1300 a 1324]", "Longitud de Onda de Dispersión Nula", "Valor estandarizado comercialmente en la fibra donde la curva de distorsión total intersecta el punto neutro cero.")
        ent_s0 = self.crear_fila_input(p_izq, 4, "Pendiente Cero (S₀):", "Ej. 0.092", "[ps/(nm²·km)]", "[Típico: 0.08 a 0.095]", "Pendiente de Dispersión Cero", "Magnitud geométrica que registra el grado de inclinación ascendente en la curva de atenuación justo en la zona neutral λ₀.")
        
        res_g652 = ctk.CTkLabel(p_izq, text="D(λ) = -- ps/(nm·km)", font=ctk.CTkFont(size=18, weight="bold")); res_g652.grid(row=5, column=0, columnspan=4, pady=5)
        
        def calc_g652():
            try:
                self.ejecutar_calculo_tradicional(MotorCalculoOptico.calc_317_dispersion_g652, res_g652, "D(λ) = {:.4f} ps/(nm·km)", ent_l, ent_l0, ent_s0)
                fig = MotorGrafico.plot_g652(float(ent_l0.get()), float(ent_s0.get()))
                self.mostrar_grafica(p_der, fig)
            except Exception as e: pass

        ctk.CTkButton(p_izq, text="Calcular y Graficar D", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=calc_g652).grid(row=6, column=0, columnspan=4, pady=10)
        self.crear_panel_formula(scroll, "D(λ) = (S₀ / 4) · [ λ - (λ₀⁴ / λ³) ]", "λ = Long. Onda Operativa | λ₀ = Long. Dispersión Cero | S₀ = Pendiente Cero")

        # Sellmeier
        c2 = ctk.CTkFrame(scroll, corner_radius=10); c2.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c2, text="Ecuación Sellmeier ➔ TRADICIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        
        ent_lum = self.crear_fila_input(c2, 2, "Longitud Onda (λ):", "Ej. 1300.0", "[nm]", "[Típico: 800 a 1600]", "Longitud de Onda Específica", "Conversión a micrómetros del punto de operación para su resolución en el oscilador Sellmeier.")
        ent_e0 = self.crear_fila_input(c2, 3, "Energía Reson. (E₀):", "Ej. 13.4", "[eV]", "[Típico: ~13.4]", "Energía de Resonancia del Oscilador", "Cualidad atómica estipulando en qué nivel se absorben de forma natural las bandas ultravioletas del material óptico.")
        ent_ed = self.crear_fila_input(c2, 4, "Energía Disp. (E_d):", "Ej. 14.7", "[eV]", "[Típico: ~14.7]", "Fuerza del Oscilador de Dispersión", "Elemento constante que vincula matemáticamente cómo cambia el índice de refracción general según las variaciones lumínicas.")
        
        res_sell = ctk.CTkLabel(c2, text="n = --", font=ctk.CTkFont(size=18, weight="bold")); res_sell.grid(row=5, column=0, columnspan=4, pady=5)
        
        def calc_sellmeier():
            try:
                lam_um = float(ent_lum.get()) / 1000.0
                res = MotorCalculoOptico.indice_sellmeier(lam_um, float(ent_e0.get()), float(ent_ed.get()))
                res_sell.configure(text=f"n = {res:.4f}")
            except Exception as e: messagebox.showerror("Error", str(e))
            
        ctk.CTkButton(c2, text="Calcular Índice Sellmeier", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=calc_sellmeier).grid(row=6, column=0, columnspan=4, pady=10)
        self.crear_panel_formula(scroll, "n² = 1 + [ (E₀ · E_d) / (E₀² - E²) ]", "E = Energía Fotónica dependiente de λ | E₀ = Resonancia | E_d = Disp. Oscilatoria")

    # ==========================================
    # VISTAS DEL MOTOR DE DISPERSIÓN
    # ==========================================
    def vista_moda_geometrica(self):
        scroll = self.crear_area_scroll("📐 Óptica Geométrica", color="#d4af37")
        
        # Índice y Velocidad
        c1 = ctk.CTkFrame(scroll, corner_radius=10); c1.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c1, text="Índice de Refracción (n = c/v) ⮀ OMNIDIRECCIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        
        ent_n = self.crear_fila_input(c1, 2, "Índice (n):", "Ej. 1.48", "[Adim]", "[Típico: 1.0 a 2.5]", "Índice de Refracción Evaluado", "Proporción adimensional entre la velocidad de la luz en el espacio vacío frente a su lentitud inherente cruzando la fibra.")
        ent_v = self.crear_fila_input(c1, 3, "Velocidad (v):", "Ej. 2e8", "[m/s]", "[< 3e8 m/s]", "Velocidad del Medio", "Frecuencia cinética constante a la que logran trasladarse los fotones inyectados a través de las moléculas del medio local.")

        def resolver_n_v():
            ents = {"n": ent_n, "v": ent_v}
            for ent in ents.values(): ent.configure(text_color="white")
            vacios = {k: v for k, v in ents.items() if v.get().strip() == ""}
            
            try:
                llenos = {k: float(v.get()) for k, v in ents.items() if v.get().strip() != ""}
                if len(vacios) != 1: return messagebox.showerror("Error", "Deja exactamente UN campo vacío.")
                inc = list(vacios.keys())[0]
                
                if inc == "n": res = MotorModuloA.indice_refraccion(llenos["v"])
                elif inc == "v": res = MotorModuloA.velocidad_medio(llenos["n"])
                
                ents[inc].delete(0, 'end')
                ents[inc].insert(0, f"{res:.2e}" if inc=="v" else f"{res:.4f}")
                ents[inc].configure(text_color="#66bb6a")
                self.reproducir_exito()
            except ValueError:
                messagebox.showerror("Error", "Revisa que todos los campos contengan números válidos.")
            except Exception as e: messagebox.showerror("Error", str(e))

        ctk.CTkButton(c1, text="Resolver Variables n/v", fg_color="#8d6e1f", hover_color="#6b5317", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=resolver_n_v).grid(row=4, column=0, columnspan=4, pady=10)
        self.crear_panel_formula(scroll, "n = c / v", "n = Índice de refracción | c = Velocidad de la luz en el vacío | v = Velocidad local")

        # Snell
        card2, p_izq, p_der = self.crear_tarjeta_dividida(scroll)
        ctk.CTkLabel(p_izq, text="Ley de Snell (Refracción) ⮀ OMNIDIRECCIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        
        ent_sn1 = self.crear_fila_input(p_izq, 2, "Índice Origen (n₁):", "Ej. 1.48", "[Medio 1]", "[Típico: 1.44 a 1.48]", "Índice de Zona Transmisora", "Propiedad óptica del componente estructural del cual están originándose y saliendo los vectores iniciales de la luz.")
        ent_sn2 = self.crear_fila_input(p_izq, 3, "Índice Destino (n₂):", "Ej. 1.46", "[Medio 2]", "[Típico: 1.0 a 1.48]", "Índice de Zona Receptora", "Propiedad del medio estructural secundario que interceptará a los haces lumínicos tras el cruce de frontera óptica.")
        ent_th1 = self.crear_fila_input(p_izq, 4, "Áng. Incidencia (θ₁):", "Ej. 30.0", "[Grados °]", "[0 a 90 °]", "Ángulo de Choque (Incidencia)", "Inclinación originada desde la trayectoria del vector fotónico con respecto a la directriz imaginaria perpendicular (Normal) de la frontera.")
        ent_th2 = self.crear_fila_input(p_izq, 5, "Áng. Refracción (θ₂):", "Ej. 45.0", "[Grados °]", "[0 a 90 °]", "Ángulo de Desviación", "Dirección definitiva a la cual logrará acomodarse la luz interna una vez invadido de lleno la composición espacial del segundo medio.")

        def resolver_snell():
            ents = {"n1": ent_sn1, "n2": ent_sn2, "th1": ent_th1, "th2": ent_th2}
            for ent in ents.values(): ent.configure(text_color="white")
            vacios = {k: v for k, v in ents.items() if v.get().strip() == ""}
            
            try:
                llenos = {k: float(v.get()) for k, v in ents.items() if v.get().strip() != ""}
                if len(vacios) != 1: return messagebox.showerror("Error", "Deja exactamente UN campo vacío.")
                inc = list(vacios.keys())[0]
                
                if inc == "th2": res = MotorModuloA.angulo_refraccion_snell(llenos["n1"], llenos["n2"], llenos["th1"])
                elif inc == "th1": res = MotorModuloA.snell_inverso_theta1(llenos["n1"], llenos["n2"], llenos["th2"])
                elif inc == "n1": res = MotorModuloA.snell_inverso_n1(llenos["n2"], llenos["th1"], llenos["th2"])
                elif inc == "n2": res = MotorModuloA.snell_inverso_n2(llenos["n1"], llenos["th1"], llenos["th2"])
                
                ents[inc].delete(0, 'end'); ents[inc].insert(0, f"{res:.4f}")
                ents[inc].configure(text_color="#66bb6a")
                self.reproducir_exito()
                
                fig = MotorGrafico.plot_snell(float(ent_sn1.get()), float(ent_sn2.get()), float(ent_th1.get()), float(ent_th2.get()))
                self.mostrar_grafica(p_der, fig)
            except ValueError:
                messagebox.showerror("Error", "Revisa que todos los campos contengan números válidos.")
            except Exception as e: messagebox.showerror("Error", str(e))

        ctk.CTkButton(p_izq, text="Resolver y Dibujar Snell", fg_color="#8d6e1f", hover_color="#6b5317", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=resolver_snell).grid(row=6, column=0, columnspan=4, pady=10)
        self.crear_panel_formula(scroll, "n₁ · sin(θ₁) = n₂ · sin(θ₂)", "Relación de ángulos y refracciones al cruzar fronteras ópticas.")

        # Parámetros del Núcleo
        c3 = ctk.CTkFrame(scroll, corner_radius=10); c3.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c3, text="Parámetros del Núcleo ➔ TRADICIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        
        ent_pn1 = self.crear_fila_input(c3, 2, "Índice Núcleo (n₁):", "Ej. 1.48", "[n₁ > n₂]", "[Típico: 1.44 a 1.48]", "Índice de Núcleo (Core)", "Material conductor primario; requiere matemáticamente poseer un valor superior al revestimiento externo para cumplir la reflexión estricta.")
        ent_pn2 = self.crear_fila_input(c3, 3, "Índice Revest. (n₂):", "Ej. 1.46", "[n₂ < n₁]", "[Típico: 1.44 a 1.46]", "Índice de Revestimiento (Cladding)", "Estructura exterior con un déficit de refracción cuidadosamente calibrado para servir enteramente de coraza repulsora ante escapes de luz.")
        
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
        self.crear_panel_formula(scroll, "NA = √(n₁² - n₂²)   |   Δ = (n₁ - n₂)/n₁   |   θ_c = sin⁻¹(n₂/n₁)", "NA = Apertura Num. | Δ = Diferencia Relativa | θ_c = Ángulo Crítico de Fuga")

    def vista_moda_parametros(self):
        scroll = self.crear_area_scroll("🔢 Número V y Modos", color="#d4af37")
        
        card1, p_izq, p_der = self.crear_tarjeta_dividida(scroll)
        ctk.CTkLabel(p_izq, text="Frecuencia Normalizada ⮀ OMNIDIRECCIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        
        ent_a = self.crear_fila_input(p_izq, 2, "Radio Núcleo (a):", "Ej. 25.0", "[µm]", "[Típico: 4 a 50]", "Radio Esférico Interno", "Cuantificación transversal desde el eje del núcleo hasta el contorno inmediato, vital para fijar el nivel de capacidad portadora.")
        ent_lam = self.crear_fila_input(p_izq, 3, "Longitud Onda (λ):", "Ej. 1300.0", "[nm]", "[Típico: 850 a 1550]", "Longitud de Espectro Óptico", "Caracterización electromagnética del tamaño del ciclo de la señal de luz de origen.") 
        ent_na = self.crear_fila_input(p_izq, 4, "Apertura Num. (NA):", "Ej. 0.22", "[Adim]", "[Típico: 0.1 a 0.3]", "Apertura Numérica (NA)", "Determinante fundamental y unívoco rigiendo de forma total la entrada y aceptación máxima de haces permisibles desde espacios vacíos.")
        ent_v = self.crear_fila_input(p_izq, 5, "Número V:", "Ej. 2.4", "[Adim]", "[Monomodo < 2.405]", "Frecuencia Espacial Normalizada", "Cifra adimensional definitoria. Señala inexorablemente si las propiedades compuestas permitirán uno solo, pocos o miles de carriles superpuestos simultáneos.")
        ent_alf = self.crear_fila_input(p_izq, 6, "Perfil Índice (α):", "Ej. 2.0", "[Opcional]", "[Gradual=2]", "Pendiente de Graduación", "Define el escalonamiento de manufactura que modela en la práctica la forma en la que cae o se eleva el índice de las capas de núcleo parabólico.")
        
        res_modos = ctk.CTkLabel(p_izq, text="Modos Guiados: --", text_color="yellow", font=ctk.CTkFont(size=18, weight="bold")); res_modos.grid(row=7, column=0, columnspan=4, pady=5)
        
        def resolver_v():
            ents = {"a": ent_a, "lam": ent_lam, "na": ent_na, "v": ent_v}
            for ent in ents.values(): ent.configure(text_color="white")
            vacios = {k: v for k, v in ents.items() if v.get().strip() == ""}
            
            try:
                llenos = {k: float(v.get()) for k, v in ents.items() if v.get().strip() != ""}
                if len(vacios) != 1: return messagebox.showerror("Error", "Deja exactamente UN campo vacío en a, λ, NA o V.")
                inc = list(vacios.keys())[0]
                
                if "lam" in llenos: llenos["lam"] = llenos["lam"] / 1000.0
                
                if inc == "v": res = MotorModuloA.frecuencia_normalizada_v(llenos["a"], llenos["lam"], llenos["na"])
                elif inc == "a": res = MotorModuloA.v_inverso_a(llenos["v"], llenos["lam"], llenos["na"])
                elif inc == "lam": res = MotorModuloA.v_inverso_lam(llenos["v"], llenos["a"], llenos["na"])
                elif inc == "na": res = MotorModuloA.v_inverso_na(llenos["v"], llenos["a"], llenos["lam"])
                
                if inc == "lam": res = res * 1000.0
                
                ents[inc].delete(0, 'end'); ents[inc].insert(0, f"{res:.4f}")
                ents[inc].configure(text_color="#66bb6a")
                self.reproducir_exito()
                
                v_final = float(ent_v.get())
                m_esc = MotorModuloA.modos_guiados_escalonado(v_final)
                m_grad = MotorModuloA.modos_guiados_gradual(v_final, float(ent_alf.get())) if ent_alf.get() else "--"
                res_modos.configure(text=f"Modos Escalonados: {m_esc} | Graduales: {m_grad}")
                
                fig = MotorGrafico.plot_numero_v(float(ent_a.get()), float(ent_lam.get()) / 1000.0, float(ent_na.get()))
                self.mostrar_grafica(p_der, fig)
            except ValueError:
                messagebox.showerror("Error", "Revisa que todos los campos contengan números válidos.")
            except Exception as e: messagebox.showerror("Error", str(e))
            
        ctk.CTkButton(p_izq, text="Resolver y Graficar V", fg_color="#8d6e1f", hover_color="#6b5317", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=resolver_v).grid(row=8, column=0, columnspan=4, pady=10)
        self.crear_panel_formula(scroll, "V = (2πa / λ) · NA", "Parámetro unívoco adimensional que rige cuántos modos portará la fibra óptica.")

    def vista_moda_dispersion(self):
        scroll = self.crear_area_scroll("⏱️ Dispersión y Retardos", color="#d4af37")

        # Retardo Modal
        c1 = ctk.CTkFrame(scroll, corner_radius=10); c1.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c1, text="Retardo Modal (Fibra Escalonada) ⮀ OMNIDIRECCIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        
        ent_rl = self.crear_fila_input(c1, 3, "Longitud (L):", "Ej. 1000", "[m]", "[En metros]", "Extensión Lineal del Enlace", "Suma métrica y continua de toda la expansión longitudinal del cable físico a lo largo de un medio terrestre o aéreo.")
        ent_rn1 = self.crear_fila_input(c1, 4, "Índice Núcleo (n₁):", "Ej. 1.48", "[Adim]", "[Típico: 1.44 a 1.48]", "Índice Estático Principal", "Valor de refracción estandarizado en donde operan plenamente y de manera constante las pulsaciones continuas ópticas.")
        ent_rdelta = self.crear_fila_input(c1, 5, "Dif. Relativa (Δ):", "Ej. 0.01", "[Decimal]", "[Típico: 0.01 a 0.02]", "Escalamiento Relativo de Medios", "Proporcionalidad estática demostrando el margen fraccionario explícito bajo el que coexisten acoplados los dos dominios de transmisión de vidrio base.")
        ent_rdt = self.crear_fila_input(c1, 6, "Retardo (ΔT):", "Ej. 5e-9", "[s]", "[Ej. 5e-9 s]", "Brecha de Retraso Modal Exclusivo", "Magnitud fraccional indicando qué tan tarde terminará llegando un haz rebotado frente a un haz enteramente horizontal a la meta transcurrida una longitud constante.")
        
        def resolver_retardo():
            ents = {"l": ent_rl, "n1": ent_rn1, "delta": ent_rdelta, "dt": ent_rdt}
            for ent in ents.values(): ent.configure(text_color="white")
            vacios = {k: v for k, v in ents.items() if v.get().strip() == ""}
            
            try:
                llenos = {k: float(v.get()) for k, v in ents.items() if v.get().strip() != ""}
                if len(vacios) != 1: return messagebox.showerror("Error", "Deja exactamente UN campo vacío.")
                inc = list(vacios.keys())[0]
                
                if inc == "dt": res = MotorModuloA.retardo_modal_escalonado(llenos["l"], llenos["n1"], llenos["delta"])
                elif inc == "l": res = MotorModuloA.retardo_inverso_l(llenos["dt"], llenos["n1"], llenos["delta"])
                elif inc == "n1": res = MotorModuloA.retardo_inverso_n1(llenos["dt"], llenos["l"], llenos["delta"])
                elif inc == "delta": res = MotorModuloA.retardo_inverso_delta(llenos["dt"], llenos["l"], llenos["n1"])
                
                ents[inc].delete(0, 'end'); ents[inc].insert(0, f"{res:.3e}" if inc=="dt" else f"{res:.4f}")
                ents[inc].configure(text_color="#66bb6a")
                self.reproducir_exito()
            except ValueError:
                messagebox.showerror("Error", "Revisa que todos los campos contengan números válidos.")
            except Exception as e: messagebox.showerror("Error", str(e))

        ctk.CTkButton(c1, text="Resolver Retardo", fg_color="#8d6e1f", hover_color="#6b5317", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=resolver_retardo).grid(row=7, column=0, columnspan=4, pady=10)
        self.crear_panel_formula(scroll, "ΔT = (L · n₁ · Δ) / c", "Representa la brecha temporal entre el modo más veloz y el más lento tras L metros.")

        # Ensanchamiento Total
        card2, p_izq, p_der = self.crear_tarjeta_dividida(scroll)
        ctk.CTkLabel(p_izq, text="Ensanchamiento Total (Cromático) ➔ TRADICIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        
        ent_ed = self.crear_fila_input(p_izq, 2, "Coef. Dispersión (D):", "Ej. 17.0", "[ps/(nm·km)]", "[Típico: 15 a 18]", "Coeficiente Empírico Cromático", "Tasación volumétrica informando cuántos picosegundos ensanchará el destello el sistema en base al kilómetro superado y las frecuencias espectrales emitidas en conjunto.")
        ent_el = self.crear_fila_input(p_izq, 3, "Longitud (L):", "Ej. 50.0", "[km]", "[Típico: 1 a 100]", "Alcance Completo de Red", "Recorrido logístico del conducto principal, determinante primordial multiplicativo directo de los retardos del material.")
        ent_esig = self.crear_fila_input(p_izq, 4, "Ancho Espectral (σ_λ):", "Ej. 2.0", "[nm]", "[Típico: 0.1 a 5.0]", "Dispersión Óptica de Hardware", "Naturaleza física del aparato emisor demostrando un margen de imperfecta desviación luminosa generadora de errores cromáticos.")
        
        res_ens = ctk.CTkLabel(p_izq, text="σ = -- ps", text_color="yellow", font=ctk.CTkFont(size=18, weight="bold")); res_ens.grid(row=5, column=0, columnspan=4, pady=5)
        
        def calc_ensanchamiento():
            try:
                self.ejecutar_calculo_tradicional(MotorModuloA.ensanchamiento_total, res_ens, "σ = {:.2f} ps", ent_ed, ent_el, ent_esig)
                fig = MotorGrafico.plot_ensanchamiento(MotorModuloA.ensanchamiento_total(float(ent_ed.get()), float(ent_el.get()), float(ent_esig.get())))
                self.mostrar_grafica(p_der, fig)
            except Exception as e: pass

        ctk.CTkButton(p_izq, text="Calcular y Graficar", fg_color="#8d6e1f", hover_color="#6b5317", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=calc_ensanchamiento).grid(row=6, column=0, columnspan=4, pady=10)
        self.crear_panel_formula(scroll, "σ = |D(λ) · L · σ_λ|", "D(λ) = Coeficiente Cromático | L = Longitud KM | σ_λ = Ancho espectral emisor")

        # PMD
        c3 = ctk.CTkFrame(scroll, corner_radius=10); c3.pack(fill="x", pady=10, ipady=5)
        ctk.CTkLabel(c3, text="Dispersión por Modo de Polarización (PMD) ➔ TRADICIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        
        ent_dpmd = self.crear_fila_input(c3, 2, "Coef. PMD (D_PMD):", "Ej. 0.5", "[ps/√km]", "[Típico: 0.1 a 0.5]", "Base Geométrica Oscilatoria", "Índice de imperfección estocástico natural evaluando el choque de ejes longitudinales que genera desfase en el rayo único estricto.")
        ent_pl = self.crear_fila_input(c3, 3, "Longitud (L):", "Ej. 100.0", "[km]", "[Típico: 1 a 100]", "Alcance Completo de Red", "Escala métrica determinante para la acumulación proporcional no-lineal en el desplazamiento de polaridad ortogonal de los modos unificados.")
        
        res_pmd = ctk.CTkLabel(c3, text="Δτ_PMD = -- ps", text_color="yellow", font=ctk.CTkFont(size=18, weight="bold")); res_pmd.grid(row=4, column=0, columnspan=4, pady=5)
        ctk.CTkButton(c3, text="Calcular PMD", fg_color="#8d6e1f", hover_color="#6b5317", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=lambda: self.ejecutar_calculo_tradicional(MotorModuloA.dispersion_polarizacion_pmd, res_pmd, "Δτ_PMD = {:.4f} ps", ent_dpmd, ent_pl)).grid(row=5, column=0, columnspan=4, pady=10)
        self.crear_panel_formula(scroll, "Δτ_PMD = D_PMD · √L", "Acumulación estocástica que retrasa los componentes ortogonales del mismo modo.")

    # ==========================================
    # VISTAS DEL MOTOR MATEMÁTICO (MÓDULO B)
    # ==========================================
    def vista_modb_frecuencia(self):
        scroll = self.crear_area_scroll("🔢 Frecuencia Normalizada y Modos", color="#66bb6a")
        
        card1, p_izq, p_der = self.crear_tarjeta_dividida(scroll)
        ctk.CTkLabel(p_izq, text="Frecuencia Normalizada (V) ⮀ OMNIDIRECCIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        
        ent_a = self.crear_fila_input(p_izq, 2, "Radio Núcleo (a):", "Ej. 25.0", "[µm]", "[Obligatorio: µm]", "Radio del Núcleo (a)", "Propiedad geométrica de la fibra. Debe ingresarse en micrómetros.")
        ent_lam = self.crear_fila_input(p_izq, 3, "Longitud Onda (λ):", "Ej. 1300.0", "[nm]", "[Obligatorio: nm]", "Longitud de Espectro Óptico", "Caracterización electromagnética del tamaño del ciclo de la señal de luz de origen.") 
        ent_na = self.crear_fila_input(p_izq, 4, "Apertura Num. (AN):", "Ej. 0.22", "[Adim]", "[Típico: 0.1 a 0.3]", "Apertura Numérica (NA)", "Determinante fundamental y unívoco rigiendo de forma total la entrada y aceptación máxima de haces permisibles desde espacios vacíos.")
        ent_v = self.crear_fila_input(p_izq, 5, "Frecuencia V:", "Ej. 2.4", "[Adim]", "[Monomodo < 2.4048]", "Frecuencia Espacial Normalizada", "Cifra adimensional definitoria. Señala inexorablemente si las propiedades compuestas permitirán uno solo, pocos o miles de carriles superpuestos simultáneos.")
        ent_alf = self.crear_fila_input(p_izq, 6, "Perfil Índice (α):", "Ej. 2.0", "[Opcional]", "[Gradual=2]", "Pendiente de Graduación", "Define el escalonamiento de manufactura que modela en la práctica la forma en la que cae o se eleva el índice de las capas de núcleo parabólico.")
        
        res_modos = ctk.CTkLabel(p_izq, text="Modos Guiados: --", text_color="#66bb6a", font=ctk.CTkFont(size=18, weight="bold")); res_modos.grid(row=7, column=0, columnspan=4, pady=5)
        
        def resolver_v_modos():
            ents = {"a": ent_a, "lam": ent_lam, "an": ent_na, "v": ent_v}
            for ent in ents.values(): ent.configure(text_color="white")
            vacios = {k: val for k, val in ents.items() if val.get().strip() == ""}
            
            try:
                llenos = {k: float(val.get()) for k, val in ents.items() if val.get().strip() != ""}
                if len(vacios) != 1: return messagebox.showerror("Error", "Deja exactamente UN campo vacío en a, λ, AN o V.")
                inc = list(vacios.keys())[0]
                
                if "lam" in llenos: llenos["lam"] = llenos["lam"] / 1000.0
                
                if inc == "v": res = MotorModuloB.frecuencia_normalizada_v(llenos["a"], llenos["lam"], llenos["an"])
                elif inc == "a": res = MotorModuloB.v_inverso_a(llenos["v"], llenos["lam"], llenos["an"])
                elif inc == "lam": res = MotorModuloB.v_inverso_lam(llenos["v"], llenos["a"], llenos["an"])
                elif inc == "an": res = MotorModuloB.v_inverso_an(llenos["v"], llenos["a"], llenos["lam"])
                
                if inc == "lam": res = res * 1000.0
                
                ents[inc].delete(0, 'end'); ents[inc].insert(0, f"{res:.4f}")
                ents[inc].configure(text_color="#66bb6a")
                self.reproducir_exito()
                
                v_final = float(ent_v.get())
                m_esc = MotorModuloB.modos_step_index(v_final)
                m_grad = MotorModuloB.modos_graded_index(v_final) if not ent_alf.get() else (float(ent_alf.get()) / (float(ent_alf.get()) + 2)) * ((v_final ** 2) / 2)
                
                texto_modos = f"Modos Escalonados: {int(m_esc)}"
                if ent_alf.get(): texto_modos += f" | Graduales: {int(m_grad)}"
                res_modos.configure(text=texto_modos)
                
                fig = MotorGrafico.plot_numero_v(float(ent_a.get()), float(ent_lam.get()) / 1000.0, float(ent_na.get()))
                self.mostrar_grafica(p_der, fig)
            except ValueError:
                messagebox.showerror("Error", "Revisa que todos los campos contengan números válidos.")
            except Exception as e: messagebox.showerror("Error", str(e))

        ctk.CTkButton(p_izq, text="Resolver y Graficar V", fg_color="#1a5a40", hover_color="#12402d", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=resolver_v_modos).grid(row=8, column=0, columnspan=4, pady=10)
        self.crear_panel_formula(scroll, "V = (2πa / λ) · AN", "Matemática subyacente para el dictamen Monomodo / Multimodo.")

    def vista_modb_corte(self):
        scroll = self.crear_area_scroll("✂️ Longitud de Onda de Corte", color="#66bb6a")
        
        card1, p_izq, p_der = self.crear_tarjeta_dividida(scroll)
        ctk.CTkLabel(p_izq, text="Condición de Corte Monomodo ⮀ OMNIDIRECCIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        
        ent_lam_c = self.crear_fila_input(p_izq, 2, "Long. Corte (λ_c):", "Ej. 1200.0", "[nm]", "[Debe ser < λ Op]", "Longitud de Onda de Corte", "Longitud de onda a partir de la cual la fibra se vuelve monomodo puro (se apaga el modo superior). Si la longitud de operación es mayor, es monomodo.") 
        ent_a = self.crear_fila_input(p_izq, 3, "Radio Núcleo (a):", "Ej. 4.0", "[µm]", "[Típico: 4 a 50]", "Radio Esférico Interno", "Cuantificación del tamaño físico del núcleo, clave para dictar los límites frecuenciales de corte.")
        ent_an = self.crear_fila_input(p_izq, 4, "Apertura Num. (AN):", "Ej. 0.12", "[Adim]", "[Típico: 0.1 a 0.3]", "Apertura Numérica (AN)", "Capacidad de aceptación lumínica basada en el contraste de índices. Impacta directamente en el punto de corte.")

        def resolver_corte():
            ents = {"lam_c": ent_lam_c, "a": ent_a, "an": ent_an}
            for ent in ents.values(): ent.configure(text_color="white")
            vacios = {k: val for k, val in ents.items() if val.get().strip() == ""}
            
            try:
                llenos = {k: float(val.get()) for k, val in ents.items() if val.get().strip() != ""}
                if len(vacios) != 1: return messagebox.showerror("Error", "Deja exactamente UN campo vacío.")
                inc = list(vacios.keys())[0]
                
                if "lam_c" in llenos: llenos["lam_c"] = llenos["lam_c"] / 1000.0
                
                if inc == "lam_c": res = MotorModuloB.longitud_corte(llenos["a"], llenos["an"])
                elif inc == "a": res = MotorModuloB.longitud_corte_inverso_a(llenos["lam_c"], llenos["an"])
                elif inc == "an": res = MotorModuloB.longitud_corte_inverso_an(llenos["lam_c"], llenos["a"])
                
                if inc == "lam_c": res = res * 1000.0
                
                ents[inc].delete(0, 'end'); ents[inc].insert(0, f"{res:.4f}")
                ents[inc].configure(text_color="#66bb6a")
                self.reproducir_exito()
                
                fig = MotorGrafico.plot_corte(float(ent_lam_c.get()) / 1000.0, float(ent_a.get()), float(ent_an.get()))
                self.mostrar_grafica(p_der, fig)
            except ValueError:
                messagebox.showerror("Error", "Revisa que todos los campos contengan números válidos.")
            except Exception as e: messagebox.showerror("Error", str(e))

        ctk.CTkButton(p_izq, text="Resolver y Graficar Corte", fg_color="#1a5a40", hover_color="#12402d", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=resolver_corte).grid(row=5, column=0, columnspan=4, pady=10)
        self.crear_panel_formula(scroll, "λ_c = (2πa · AN) / 2.4048", "Punto límite absoluto bajo el cual todos los modos superiores colapsan y la fibra queda Monomodo puro.")

    def vista_modb_mfd(self):
        scroll = self.crear_area_scroll("⭕ Diámetro de Campo Modal (MFD)", color="#66bb6a")
        
        card1, p_izq, p_der = self.crear_tarjeta_dividida(scroll)
        ctk.CTkLabel(p_izq, text="Aproximación de Marcuse ➔ TRADICIONAL", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        
        ent_a = self.crear_fila_input(p_izq, 2, "Radio Núcleo (a):", "Ej. 4.0", "[µm]", "[Típicamente igual a la salida]", "Radio del Núcleo", "Tamaño físico real del núcleo. Recuerda que el MFD siempre será mayor que 2a porque el campo electromagnético se extiende hacia el revestimiento.")
        ent_v = self.crear_fila_input(p_izq, 3, "Valor V:", "Ej. 2.0", "[Adim]", "[Rango ideal: 1.8 a 2.4]", "Frecuencia Normalizada (V)", "El MFD depende fuertemente de V. Marcuse diseñó esta fórmula empírica precisamente para el rango monomodo (V entre 1.8 y 2.4).")
        
        res_mfd = ctk.CTkLabel(p_izq, text="MFD (2ω₀) = --", text_color="#66bb6a", font=ctk.CTkFont(size=18, weight="bold")); res_mfd.grid(row=4, column=0, columnspan=4, pady=5)
        
        def calc_mfd():
            try:
                a_val, v_val = float(ent_a.get()), float(ent_v.get())
                mfd = MotorModuloB.mfd_marcuse(a_val, v_val)
                res_mfd.configure(text=f"MFD (2ω₀) = {mfd:.4f}")
                
                fig = MotorGrafico.plot_mfd(a_val, mfd)
                self.mostrar_grafica(p_der, fig)
            except ValueError:
                messagebox.showerror("Error", "Revisa que todos los campos contengan números válidos.")
            except Exception as e: messagebox.showerror("Error", str(e))
            
        ctk.CTkButton(p_izq, text="Calcular y Graficar MFD", fg_color="#1a5a40", hover_color="#12402d", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=calc_mfd).grid(row=5, column=0, columnspan=4, pady=10)
        self.crear_panel_formula(scroll, "2ω₀ = 2a [ 0.65 + 1.619/(V^1.5) + 2.879/(V^6) ]", "Fórmula empírica de Marcuse para evaluar la dispersión de la campana electromagnética en la cubierta.")

    # ==========================================
    # VISTAS DEL MOTOR DE MODULACIÓN
    # ==========================================
    def vista_modulacion_ask(self):
        scroll = self.crear_area_scroll("📈 Modulación ASK (AM Óptico)", color="#ab47bc")
        card, p_izq, p_der = self.crear_tarjeta_dividida(scroll)
        
        ctk.CTkLabel(p_izq, text="Generador de Ondas ➔ DIRECTO", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        
        ent_es = self.crear_fila_input(p_izq, 2, "Amplitud (E_s):", "Ej. 1.0", "[V/m]", "[Típico: 1.0]", "Amplitud de Portadora", "Intensidad base del láser o fuente de luz antes de la modulación.")
        ent_m = self.crear_fila_input(p_izq, 3, "Índice (m):", "Ej. 0.8", "[Adim]", "[0 < m ≤ 1]", "Índice de Modulación", "Grado en el que la señal de mensaje afecta la amplitud de la portadora.")
        ent_fc = self.crear_fila_input(p_izq, 4, "Frec. Portadora (f_c):", "Ej. 20.0", "[Hz]", "[Recomendado > f_m]", "Frecuencia de la Portadora", "Frecuencia óptica central. Se escala a Hz para propósitos de simulación visual.")
        ent_fm = self.crear_fila_input(p_izq, 5, "Frec. Mensaje (f_m):", "Ej. 2.0", "[Hz]", "[Recomendado: 1 a 5]", "Frecuencia del Mensaje", "Frecuencia de la señal analógica que contiene la información a transmitir.")

        def graficar_ask():
            try:
                fig = MotorModulacion.plot_ask(float(ent_es.get()), float(ent_m.get()), float(ent_fc.get()), float(ent_fm.get()))
                self.mostrar_grafica(p_der, fig)
                self.reproducir_exito()
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingresa números válidos.")

        ctk.CTkButton(p_izq, text="Generar Gráficas", fg_color="#4a148c", hover_color="#38006b", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=graficar_ask).grid(row=6, column=0, columnspan=4, pady=15)
        self.crear_panel_formula(scroll, "E_ASK(t) = E_s [ 1 + m · cos(2π f_m t) ] cos(2π f_c t)", "E_s = Amplitud Portadora | m = Índice de Modulación | f_m = Frecuencia Mensaje | f_c = Frecuencia Portadora")

    def vista_modulacion_psk(self):
        scroll = self.crear_area_scroll("📉 Modulación BPSK (Binaria de Fase)", color="#ab47bc")
        card, p_izq, p_der = self.crear_tarjeta_dividida(scroll)
        
        ctk.CTkLabel(p_izq, text="Codificación BPSK ➔ DIRECTO", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        
        ent_es = self.crear_fila_input(p_izq, 2, "Amplitud (E_s):", "Ej. 1.0", "[V/m]", "[Típico: 1.0]", "Amplitud de Portadora", "Intensidad base constante del haz de luz.")
        ent_fc = self.crear_fila_input(p_izq, 3, "Frec. Portadora (f_c):", "Ej. 5.0", "[Hz]", "[Rec: > 3 para ver ciclos]", "Frecuencia Portadora", "Frecuencia base de la señal para simular correctamente los ciclos de onda visuales.")
        
        lbl_font = ctk.CTkFont(size=14)
        ctk.CTkLabel(p_izq, text="Secuencia Bits:", font=lbl_font).grid(row=4, column=0, padx=15, pady=10, sticky="e")
        ent_bits = ctk.CTkEntry(p_izq, placeholder_text="Ej. 10110", width=150, font=ctk.CTkFont(size=14))
        ent_bits.grid(row=4, column=1, padx=5, pady=10)
        ctk.CTkLabel(p_izq, text="[Cadena de 0s y 1s]", text_color="gray", width=250, anchor="w", font=ctk.CTkFont(size=13)).grid(row=4, column=2, padx=5, sticky="w")
        ctk.CTkButton(p_izq, text="?", width=32, height=32, font=lbl_font, command=lambda: self.abrir_ayuda("Tren de Bits Digital", "Secuencia binaria que modulará directamente la fase de la onda. 1 = 0°, 0 = 180°.")).grid(row=4, column=3, padx=10)

        def graficar_psk():
            try:
                fig = MotorModulacion.plot_psk(float(ent_es.get()), float(ent_fc.get()), ent_bits.get())
                self.mostrar_grafica(p_der, fig)
                self.reproducir_exito()
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingresa números válidos.")

        ctk.CTkButton(p_izq, text="Generar Gráficas BPSK", fg_color="#4a148c", hover_color="#38006b", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=graficar_psk).grid(row=5, column=0, columnspan=4, pady=15)
        self.crear_panel_formula(scroll, "v_{bpsk}(t) = b(t) · √(2P) · cos(2π f_c t)", "b(t) = +1 para bit 1, -1 para bit 0  |  √(2P) equivale a la Amplitud E_s de la portadora.")
        
    def vista_modulacion_fsk(self):
        scroll = self.crear_area_scroll("📊 Modulación FSK (FM Óptico)", color="#ab47bc")
        card, p_izq, p_der = self.crear_tarjeta_dividida(scroll)
        
        ctk.CTkLabel(p_izq, text="Generador de Ondas ➔ DIRECTO", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        
        ent_es = self.crear_fila_input(p_izq, 2, "Amplitud (E_s):", "Ej. 1.0", "[V/m]", "[Típico: 1.0]", "Amplitud de Portadora", "Intensidad base constante.")
        ent_df = self.crear_fila_input(p_izq, 3, "Desviación (Δf):", "Ej. 5.0", "[Hz]", "[Típico: 2 a 10]", "Desviación de Frecuencia", "Cuánto se aleja la frecuencia portadora hacia arriba o hacia abajo en su punto pico.")
        ent_fc = self.crear_fila_input(p_izq, 4, "Frec. Portadora (f_c):", "Ej. 20.0", "[Hz]", "[Debe ser > Δf]", "Frecuencia Portadora", "Centro del espectro de transmisión.")
        ent_fm = self.crear_fila_input(p_izq, 5, "Frec. Mensaje (f_m):", "Ej. 2.0", "[Hz]", "[Recomendado: 1 a 5]", "Frecuencia del Mensaje", "Tasa de cambio analógico.")

        def graficar_fsk():
            try:
                fig = MotorModulacion.plot_fsk(float(ent_es.get()), float(ent_df.get()), float(ent_fc.get()), float(ent_fm.get()))
                self.mostrar_grafica(p_der, fig)
                self.reproducir_exito()
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingresa números válidos.")

        ctk.CTkButton(p_izq, text="Generar Gráficas", fg_color="#4a148c", hover_color="#38006b", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=graficar_fsk).grid(row=6, column=0, columnspan=4, pady=15)
        self.crear_panel_formula(scroll, "E_FSK(t) = E_s · cos[ 2π f_c t + (Δf / f_m) · sin(2π f_m t) ]", "E_s = Amplitud | Δf = Desviación Frecuencial | f_m = Frec. Mensaje | f_c = Frec. Portadora")

    def vista_modulacion_dpsk(self):
        scroll = self.crear_area_scroll("🔢 Modulación DPSK (Diferencial)", color="#ab47bc")
        card, p_izq, p_der = self.crear_tarjeta_dividida(scroll)
        
        ctk.CTkLabel(p_izq, text="Codificación por Bits ➔ DIRECTO", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 0))
        
        ent_es = self.crear_fila_input(p_izq, 2, "Amplitud (E_s):", "Ej. 1.0", "[V/m]", "[Típico: 1.0]", "Amplitud de Portadora", "Intensidad de la onda de luz base.")
        ent_fc = self.crear_fila_input(p_izq, 3, "Frec. Portadora (f_c):", "Ej. 5.0", "[Hz]", "[Rec: > 3 para ver ciclos]", "Frecuencia Portadora", "Frecuencia para que el periodo encaje visualmente dentro de la ventana de un solo bit.")
        
        # Campo especial para bits
        lbl_font = ctk.CTkFont(size=14)
        ctk.CTkLabel(p_izq, text="Secuencia Bits:", font=lbl_font).grid(row=4, column=0, padx=15, pady=10, sticky="e")
        ent_bits = ctk.CTkEntry(p_izq, placeholder_text="Ej. 10110", width=150, font=ctk.CTkFont(size=14))
        ent_bits.grid(row=4, column=1, padx=5, pady=10)
        ctk.CTkLabel(p_izq, text="[Cadena de 0s y 1s]", text_color="gray", width=250, anchor="w", font=ctk.CTkFont(size=13)).grid(row=4, column=2, padx=5, sticky="w")
        ctk.CTkButton(p_izq, text="?", width=32, height=32, font=lbl_font, command=lambda: self.abrir_ayuda("Tren de Bits Digital", "Secuencia binaria cruda que se someterá a codificación diferencial.")).grid(row=4, column=3, padx=10)

        def graficar_dpsk():
            try:
                fig = MotorModulacion.plot_dpsk(float(ent_es.get()), float(ent_fc.get()), ent_bits.get())
                self.mostrar_grafica(p_der, fig)
                self.reproducir_exito()
            except ValueError:
                messagebox.showerror("Error", "Revisa que Amplitud y Frecuencia sean números válidos.")

        ctk.CTkButton(p_izq, text="Generar Gráficas", fg_color="#4a148c", hover_color="#38006b", font=ctk.CTkFont(size=15, weight="bold"), width=180, height=36, command=graficar_dpsk).grid(row=5, column=0, columnspan=4, pady=15)
        self.crear_panel_formula(scroll, "d_k = d_{k-1} ⊕ b_k   |   E_DPSK(t) = E_s · cos(2π f_c t + d_k · π)", "d_k = Bit codificado | b_k = Bit de entrada | E_DPSK = Señal de salto de fase")

if __name__ == "__main__":
    app = App()
    app.mainloop()