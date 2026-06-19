import flet as ft
import io
import base64
import matplotlib.pyplot as plt

# Intento de importar winsound (nativo en Windows) para feedback auditivo
try:
    import winsound
except ImportError:
    winsound = None

from motor_optico import MotorCalculoOptico
from motor_modulo_a import MotorModuloA
from motor_modulo_b import MotorModuloB
from motor_grafico import MotorGrafico
from motor_modulacion import MotorModulacion

class OpticaApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Suite de Simulación Electrónica y Óptica"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 0
        self.page.bgcolor = "#121212"
        
        # Configuración de ventana nativa
        self.page.window.width = 1450
        self.page.window.height = 900
        self.page.window.resizable = False

        self.crear_interfaz()

    def reproducir_exito(self):
        if winsound:
            winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC)

    def mostrar_error(self, mensaje):
        sb = ft.SnackBar(content=ft.Text(mensaje, color=ft.Colors.WHITE), bgcolor="#d32f2f")
        
        # 1. Se añade el control a la capa de superposición (overlay) de la página
        self.page.overlay.append(sb)
        # 2. Se invoca su apertura directamente desde el componente
        sb.open = True
        self.page.update()

    def abrir_ayuda(self, concepto, definicion):
        dlg = ft.AlertDialog(
            title=ft.Text(f"Ayuda: {concepto}", weight=ft.FontWeight.BOLD),
            content=ft.Column(
                controls=[
                    ft.Text(definicion, size=15),
                    ft.Divider(),
                    ft.Text("Para más información y derivación de fórmulas, consulte el marco teórico.", color=ft.Colors.GREY, italic=True, size=12)
                ], tight=True, width=400
            )
        )
        
        def cerrar_dlg(e):
            dlg.open = False
            self.page.update()
            
        dlg.actions = [ft.TextButton("Cerrar", on_click=cerrar_dlg)]
        
        # Misma lógica: al overlay y se cambia su estado a abierto
        self.page.overlay.append(dlg)
        dlg.open = True
        self.page.update()

    # ==========================================
    # HERRAMIENTAS DE CONSTRUCCIÓN VISUAL
    # ==========================================
    def crear_fila_input(self, label_text, placeholder, unit_text, rango_text="", help_title="Info", help_desc="Detalle"):
        ent = ft.TextField(hint_text=placeholder, width=150, text_size=14, height=45, content_padding=10, border_color="#555555")
        row = ft.Row(
            controls=[
                ft.Container(content=ft.Text(label_text, size=14), width=180, alignment=ft.Alignment.CENTER_RIGHT),
                ent,
                ft.Container(content=ft.Text(f"{unit_text}  {rango_text}", size=13, color="#d4af37" if rango_text else ft.Colors.GREY), width=270),
                ft.IconButton(icon=ft.Icons.HELP_OUTLINE, icon_size=20, on_click=lambda e: self.abrir_ayuda(help_title, help_desc))
            ], spacing=5
        )
        return row, ent

    def crear_tarjeta_dividida(self):
        p_izq = ft.Column(expand=True, spacing=10)
        p_der = ft.Container(
            width=480, bgcolor="#212121", border_radius=8, alignment=ft.Alignment.CENTER,
            content=ft.Text("[ La gráfica adaptativa aparecerá aquí ]", color=ft.Colors.GREY)
        )
        card = ft.Container(
            content=ft.Row(controls=[p_izq, p_der], vertical_alignment=ft.CrossAxisAlignment.START),
            bgcolor="#1e1e1e", padding=20, border_radius=10, margin=15
        )
        return card, p_izq, p_der

    def crear_panel_formula(self, formula_str, descripcion_variables):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(formula_str, size=22, weight=ft.FontWeight.BOLD, color="#d4af37", font_family="Cambria Math"),
                    ft.Text(descripcion_variables, size=13, color="#aaaaaa")
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            bgcolor="#2b2b2b", padding=15, border_radius=8, margin=10,
            alignment=ft.Alignment.CENTER
        )

    def mostrar_grafica(self, contenedor, figura_matplotlib):
        buf = io.BytesIO()
        figura_matplotlib.savefig(buf, format="png", bbox_inches="tight", transparent=True, facecolor="#212121")
        buf.seek(0)
        img_b64 = base64.b64encode(buf.read()).decode("utf-8")
        
        contenedor.content = ft.Image(src=img_b64, fit=ft.BoxFit.CONTAIN)
        
        plt.close(figura_matplotlib) 
        self.page.update()

    def set_main_content(self, title_text, title_color, controls_list):
        self.main_column.controls.clear()
        self.main_column.controls.append(ft.Text(title_text, size=28, weight=ft.FontWeight.BOLD, color=title_color))
        self.main_column.controls.extend(controls_list)
        self.page.update()

    def _resolver_omni(self, ents_dict, func_dict):
        for ent in ents_dict.values(): 
            ent.color = ft.Colors.WHITE
            ent.border_color = "#555555"
        
        vacios = {k: v for k, v in ents_dict.items() if not v.value or not v.value.strip()}
        if len(vacios) != 1:
            self.mostrar_error("Error: Deja exactamente UN campo vacío para resolver.")
            self.page.update()
            return None, None
            
        try:
            llenos = {k: float(v.value) for k, v in ents_dict.items() if v.value and v.value.strip()}
            inc = list(vacios.keys())[0]
            
            if "lam" in llenos: llenos["lam"] /= 1000.0
            res = func_dict[inc](llenos)
            if inc == "lam": res *= 1000.0

            ents_dict[inc].value = f"{res:.4f}"
            ents_dict[inc].color = "#66bb6a"
            ents_dict[inc].border_color = "#66bb6a"
            self.reproducir_exito()
            self.page.update()
            return inc, res
        except ValueError:
            self.mostrar_error("Error: Revisa que todos los campos contengan números válidos.")
        except Exception as e:
            self.mostrar_error(f"Error matemático: {str(e)}")
        return None, None

    # ==========================================
    # ACORDEÓN Y ESTRUCTURA PRINCIPAL
    # ==========================================
    def crear_btn_menu(self, texto, icono_str, color_hover, al_hacer_click):
        def al_pasar_mouse(e):
            e.control.bgcolor = color_hover if e.data == "true" else None
            e.control.update()

        return ft.Container(
            content=ft.Row(controls=[ft.Icon(icon=icono_str, size=18), ft.Text(texto, size=14)]),
            padding=10, 
            border_radius=5, ink=True, on_click=al_hacer_click,
            on_hover=al_pasar_mouse
        )

    def toggle_menu(self, e, sub_menu, btn_text_ref, title_open, title_closed):
        for menu, btn, t_open, t_closed in self.menus:
            if menu != sub_menu:
                menu.visible = False
                btn.value = t_closed
        sub_menu.visible = not sub_menu.visible
        btn_text_ref.value = title_open if sub_menu.visible else title_closed
        self.page.update()

    def crear_interfaz(self):
        self.sub_base = ft.Column(controls=[
            self.crear_btn_menu("Atenuación", ft.Icons.TRENDING_DOWN, "#333333", lambda e: self.v_atenuacion()),
            self.crear_btn_menu("Eficiencia", ft.Icons.ADS_CLICK, "#333333", lambda e: self.v_eficiencia()),
            self.crear_btn_menu("Presupuesto Potencia", ft.Icons.BOLT, "#333333", lambda e: self.v_presupuesto()),
            self.crear_btn_menu("Rayleigh y Potencias", ft.Icons.AUTO_AWESOME, "#333333", lambda e: self.v_rayleigh()),
            self.crear_btn_menu("Análisis Curvaturas", ft.Icons.U_TURN_RIGHT, "#333333", lambda e: self.v_curvaturas()),
            self.crear_btn_menu("Modelos Estándar", ft.Icons.BAR_CHART, "#333333", lambda e: self.v_modelos()),
        ], visible=True)

        self.sub_moda = ft.Column(controls=[
            self.crear_btn_menu("Óptica Geométrica", ft.Icons.SQUARE_FOOT, "#4d3d11", lambda e: self.v_geom()),
            self.crear_btn_menu("Número V y Modos", ft.Icons.PIN, "#4d3d11", lambda e: self.v_parametros()),
            self.crear_btn_menu("Dispersión y Retardos", ft.Icons.TIMER, "#4d3d11", lambda e: self.v_dispersion()),
        ], visible=False)

        self.sub_modb = ft.Column(controls=[
            self.crear_btn_menu("Frecuencia y Modos", ft.Icons.PIN, "#12402d", lambda e: self.v_modb_freq()),
            self.crear_btn_menu("Longitud de Corte", ft.Icons.CONTENT_CUT, "#12402d", lambda e: self.v_modb_corte()),
            self.crear_btn_menu("Campo Modal (MFD)", ft.Icons.RADIO_BUTTON_UNCHECKED, "#12402d", lambda e: self.v_modb_mfd()),
        ], visible=False)

        self.sub_modc = ft.Column(controls=[
            self.crear_btn_menu("Modulación ASK", ft.Icons.INSERT_CHART, "#38006b", lambda e: self.v_ask()),
            self.crear_btn_menu("Modulación PSK", ft.Icons.WAVES, "#38006b", lambda e: self.v_psk()),
            self.crear_btn_menu("Modulación FSK", ft.Icons.GRAPHIC_EQ, "#38006b", lambda e: self.v_fsk()),
            self.crear_btn_menu("Modulación DPSK", ft.Icons.SWAP_HORIZ, "#38006b", lambda e: self.v_dpsk()),
        ], visible=False)

        t_base = ft.Text("▼ Motor de Atenuación", weight=ft.FontWeight.BOLD, size=15)
        t_moda = ft.Text("▶ Motor de Dispersión", weight=ft.FontWeight.BOLD, size=15, color="#d4af37")
        t_modb = ft.Text("▶ Motor Matemático", weight=ft.FontWeight.BOLD, size=15, color="#66bb6a")
        t_modc = ft.Text("▶ Motor de Modulación", weight=ft.FontWeight.BOLD, size=15, color="#ab47bc")

        self.menus = [
            (self.sub_base, t_base, "▼ Motor de Atenuación", "▶ Motor de Atenuación"),
            (self.sub_moda, t_moda, "▼ Motor de Dispersión", "▶ Motor de Dispersión"),
            (self.sub_modb, t_modb, "▼ Motor Matemático", "▶ Motor Matemático"),
            (self.sub_modc, t_modc, "▼ Motor de Modulación", "▶ Motor de Modulación"),
        ]

        sidebar = ft.Container(
            width=330, bgcolor="#1a1a1a", padding=20,
            content=ft.Column(controls=[
                ft.Text("ÓpticaSuite Pro", size=26, weight=ft.FontWeight.BOLD),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                ft.Container(content=ft.Row(controls=[ft.Icon(icon=ft.Icons.HOME), ft.Text("Inicio", size=15)]), on_click=lambda e: self.mostrar_inicio(), ink=True, padding=10),
                
                ft.Container(content=t_base, on_click=lambda e: self.toggle_menu(e, self.sub_base, t_base, "▼ Motor de Atenuación", "▶ Motor de Atenuación"), padding=10, ink=True),
                self.sub_base,
                
                ft.Container(content=t_moda, on_click=lambda e: self.toggle_menu(e, self.sub_moda, t_moda, "▼ Motor de Dispersión", "▶ Motor de Dispersión"), padding=10, ink=True),
                self.sub_moda,

                ft.Container(content=t_modb, on_click=lambda e: self.toggle_menu(e, self.sub_modb, t_modb, "▼ Motor Matemático", "▶ Motor Matemático"), padding=10, ink=True),
                self.sub_modb,

                ft.Container(content=t_modc, on_click=lambda e: self.toggle_menu(e, self.sub_modc, t_modc, "▼ Motor de Modulación", "▶ Motor de Modulación"), padding=10, ink=True),
                self.sub_modc,
            ])
        )

        self.main_column = ft.Column(scroll=ft.ScrollMode.AUTO)
        contenedor_principal = ft.Container(content=self.main_column, padding=30, expand=True)
        
        self.page.add(ft.Row(controls=[sidebar, contenedor_principal], expand=True))
        self.mostrar_inicio()

    def mostrar_inicio(self):
        self.main_column.controls.clear()
        self.main_column.controls.extend([
            ft.Text("Bienvenido a ÓpticaSuite Pro", size=34, weight=ft.FontWeight.BOLD),
            ft.Text("Selecciona un módulo en la barra lateral para comenzar.", size=18, color=ft.Colors.GREY),
            ft.Text("¡Deja un campo vacío en las tarjetas OMNI para calcular su valor automáticamente!", size=16, color="#64b5f6")
        ])
        self.page.update()

    # ==========================================
    # VISTAS DEL MOTOR DE ATENUACIÓN
    # ==========================================
    def v_atenuacion(self):
        content = []
        card, p_izq, p_der = self.crear_tarjeta_dividida()
        p_izq.controls.extend([ft.Text("⮀ OMNIDIRECCIONAL", size=16, weight=ft.FontWeight.BOLD), ft.Text("Deja exactamente UN campo vacío para resolver.", size=13, color="#64b5f6")])

        r1, e_pin = self.crear_fila_input("Potencia (Pᵢₙ):", "Ej. 1.0", "[mW]", "[Típico: 0.1 a 10]", "Potencia Entrada", "Inyectada por transmisor.")
        r2, e_pout = self.crear_fila_input("Potencia (Pₒᵤₜ):", "Ej. 0.5", "[mW]", "[Debe ser < Pᵢₙ]", "Potencia Salida", "Medida al final.")
        r3, e_z = self.crear_fila_input("Distancia (z):", "Ej. 20.0", "[km]", "[Típico: 1 a 100]", "Distancia Enlace", "Longitud física del cable.")
        r4, e_alf = self.crear_fila_input("Atenuación (α):", "Ej. 0.25", "[dB/km]", "[Típico: 0.2 a 3.0]", "Coeficiente Atenuación", "Pérdida intrínseca.")
        p_izq.controls.extend([r1, r2, r3, r4])

        def resolver(e):
            ents = {"pin": e_pin, "pout": e_pout, "z": e_z, "alpha": e_alf}
            funcs = {
                "alpha": lambda ll: MotorCalculoOptico.calcular_atenuacion_db_km(ll["pin"], ll["pout"], ll["z"]),
                "pout": lambda ll: MotorCalculoOptico.calcular_potencia_salida(ll["pin"], ll["alpha"], ll["z"]),
                "pin": lambda ll: MotorCalculoOptico.calcular_potencia_entrada(ll["pout"], ll["alpha"], ll["z"]),
                "z": lambda ll: MotorCalculoOptico.calcular_distancia_atenuacion(ll["pin"], ll["pout"], ll["alpha"]),
            }
            inc, res = self._resolver_omni(ents, funcs)
            if inc:
                fig = MotorGrafico.plot_atenuacion(float(e_pin.value), float(e_alf.value), float(e_z.value))
                self.mostrar_grafica(p_der, fig)

        p_izq.controls.append(ft.Button("Resolver y Graficar", on_click=resolver, bgcolor="#333333", color=ft.Colors.WHITE))
        content.extend([card, self.crear_panel_formula("P_out = P_in · 10^(-α · z / 10)", "P_out = Potencia Final | P_in = Inicial | α = Coef. Atenuación | z = Distancia")])
        self.set_main_content("📉 Cálculo de Atenuación", ft.Colors.WHITE, content)

    def v_presupuesto(self):
        content = []
        card, p_izq, p_der = self.crear_tarjeta_dividida()
        p_izq.controls.extend([ft.Text("⮀ OMNIDIRECCIONAL", size=16, weight=ft.FontWeight.BOLD), ft.Text("Deja exactamente UN campo vacío.", size=13, color="#64b5f6")])

        r1, e_tx = self.crear_fila_input("Potencia Tx:", "Ej. 3.0", "[dBm]", "", "Tx", "Potencia emisor.")
        r2, e_rx = self.crear_fila_input("Sensibilidad Rx:", "Ej. -32.0", "[dBm]", "", "Rx", "Sensibilidad receptor.")
        r3, e_cab = self.crear_fila_input("Pérdida Cable:", "Ej. 15.0", "[dB]", "", "Cable", "Atenuación total fibra.")
        r4, e_emp = self.crear_fila_input("Empalmes:", "Ej. 1.0", "[dB]", "", "Empalmes", "Pérdidas uniones.")
        r5, e_con = self.crear_fila_input("Conectores:", "Ej. 2.0", "[dB]", "", "Conectores", "Atenuación mecánicas.")
        r6, e_mar = self.crear_fila_input("Margen Sistema:", "Ej. 5.0", "[dB]", "", "Margen", "Reserva de seguridad.")
        p_izq.controls.extend([r1, r2, r3, r4, r5, r6])

        def resolver(e):
            ents = {"tx": e_tx, "rx": e_rx, "cab": e_cab, "emp": e_emp, "con": e_con, "mar": e_mar}
            funcs = {
                "mar": lambda ll: ll["tx"] - ll["rx"] - ll["cab"] - ll["emp"] - ll["con"],
                "tx": lambda ll: ll["mar"] + ll["rx"] + ll["cab"] + ll["emp"] + ll["con"],
                "rx": lambda ll: ll["tx"] - ll["mar"] - ll["cab"] - ll["emp"] - ll["con"],
                "cab": lambda ll: ll["tx"] - ll["rx"] - ll["mar"] - ll["emp"] - ll["con"],
                "emp": lambda ll: ll["tx"] - ll["rx"] - ll["mar"] - ll["cab"] - ll["con"],
                "con": lambda ll: ll["tx"] - ll["rx"] - ll["mar"] - ll["cab"] - ll["emp"],
            }
            inc, res = self._resolver_omni(ents, funcs)
            if inc:
                fig = MotorGrafico.plot_presupuesto(float(e_tx.value), float(e_rx.value), float(e_cab.value), float(e_emp.value), float(e_con.value))
                self.mostrar_grafica(p_der, fig)

        p_izq.controls.append(ft.Button("Resolver y Graficar", on_click=resolver, bgcolor="#333333", color=ft.Colors.WHITE))
        content.extend([card, self.crear_panel_formula("P_Rx = P_Tx - P_Cable - P_Empalmes - P_Conectores - Margen", "En dominio logarítmico (dB / dBm)")])
        self.set_main_content("⚡ Presupuesto de Potencia", ft.Colors.WHITE, content)

    def v_eficiencia(self):
        content = []
        card = ft.Container(bgcolor="#1e1e1e", padding=20, border_radius=10, margin=15)
        col = ft.Column(controls=[ft.Text("➔ TRADICIONAL (Llena TODOS los campos)", size=16, weight=ft.FontWeight.BOLD)])
        
        r1, e_rs = self.crear_fila_input("Radio Fuente (rs):", "Ej. 50.0", "[µm]", "", "rs", "Radio emisor.")
        r2, e_a = self.crear_fila_input("Radio Núcleo (a):", "Ej. 25.0", "[µm]", "", "a", "Radio núcleo.")
        r3, e_na = self.crear_fila_input("Apertura Num. (NA):", "Ej. 0.22", "[Adim]", "", "NA", "Apertura Numérica.")
        lbl_res = ft.Text("Eficiencia (η): --", size=24, weight=ft.FontWeight.BOLD, color="#66bb6a")
        
        def calcular(e):
            try:
                res = MotorCalculoOptico.eficiencia_acoplamiento(float(e_rs.value), float(e_a.value), float(e_na.value))
                lbl_res.value = f"Eficiencia (η): {res:.4f}"
                self.page.update()
            except Exception as ex: self.mostrar_error(str(ex))

        col.controls.extend([r1, r2, r3, ft.Container(content=lbl_res, padding=10), ft.Button("Calcular", on_click=calcular)])
        card.content = col
        content.extend([card, self.crear_panel_formula("Si rs ≤ a: η = NA²   |   Si rs > a: η = (a/rs)² · NA²", "Fórmulas de eficiencia óptica")])
        self.set_main_content("🎯 Eficiencia de Acoplamiento", ft.Colors.WHITE, content)

    def v_rayleigh(self):
        content = []
        card, p_izq, p_der = self.crear_tarjeta_dividida()
        p_izq.controls.append(ft.Text("➔ TRADICIONAL", size=16, weight=ft.FontWeight.BOLD))

        r1, e_n = self.crear_fila_input("Índice Núcleo (n):", "Ej. 1.46", "[Adim]", "", "n", "Índice base.")
        r2, e_bt = self.crear_fila_input("Compresibilidad (βₜ):", "Ej. 7e-11", "[cm²/dina]", "", "Compresibilidad", "Respuesta térmica.")
        r3, e_tf = self.crear_fila_input("Temp. Fusión (T_f):", "Ej. 1673", "[K]", "", "T_f", "Punto cristalización.")
        r4, e_lnm = self.crear_fila_input("Longitud Onda (λ):", "Ej. 850.0", "[nm]", "", "λ", "Espectro.")
        lbl_res = ft.Text("α_Rayleigh = -- dB/km", size=18, weight=ft.FontWeight.BOLD, color="#66bb6a")
        p_izq.controls.extend([r1, r2, r3, r4, ft.Container(content=lbl_res, padding=10)])

        def calcular(e):
            try:
                res = MotorCalculoOptico.atenuacion_rayleigh_eq37(float(e_n.value), float(e_bt.value), float(e_tf.value), float(e_lnm.value))
                lbl_res.value = f"α_Rayleigh = {res:.4f} dB/km"
                fig = MotorGrafico.plot_rayleigh(float(e_lnm.value))
                self.mostrar_grafica(p_der, fig)
            except Exception as ex: self.mostrar_error(str(ex))

        p_izq.controls.append(ft.Button("Calcular y Graficar", on_click=calcular))
        content.extend([card, self.crear_panel_formula("α_R = (8π³ / 3λ⁴) · (n²-1)² · β_T · K_B · T_f", "Dispersión molecular")])
        self.set_main_content("✨ Rayleigh y Predicción", ft.Colors.WHITE, content)

    def v_curvaturas(self):
        content = []
        card = ft.Container(bgcolor="#1e1e1e", padding=20, border_radius=10, margin=15)
        col = ft.Column(controls=[ft.Text("Relación de Modos Efectivos (Macrocurvatura) ➔ TRADICIONAL", size=16, weight=ft.FontWeight.BOLD)])
        
        r1, e_alf = self.crear_fila_input("Perfil Índice (α):", "Ej. 2.0", "[Adim]", "", "α", "Perfil.")
        r2, e_del = self.crear_fila_input("Dif. Relativa (Δ):", "Ej. 0.01", "[Decimal]", "", "Δ", "Diferencia de índice.")
        r3, e_a = self.crear_fila_input("Radio Núcleo (a):", "Ej. 25e-6", "[Metros]", "", "a", "Radio en metros.")
        r4, e_R = self.crear_fila_input("Radio Curvatura (R):", "Ej. 0.06", "[Metros]", "", "R", "Radio del doblez.")
        r5, e_n2 = self.crear_fila_input("Índice Revest. (n₂):", "Ej. 1.46", "[Adim]", "", "n₂", "Revestimiento.")
        r6, e_lam = self.crear_fila_input("Longitud Onda (λ):", "Ej. 1300.0", "[nm]", "", "λ", "Longitud en nm.")
        lbl_res = ft.Text("Nₑᶠᶠ / N∞ = --", size=18, weight=ft.FontWeight.BOLD, color="#66bb6a")

        def calcular(e):
            try:
                l_metros = float(e_lam.value) * 1e-9
                res = MotorCalculoOptico.modos_efectivos_curvatura(float(e_alf.value), float(e_del.value), float(e_a.value), float(e_R.value), float(e_n2.value), l_metros)
                lbl_res.value = f"Modos Efectivos: {res:.4f}"
                self.page.update()
            except Exception as ex: self.mostrar_error(str(ex))

        col.controls.extend([r1, r2, r3, r4, r5, r6, ft.Container(content=lbl_res, padding=10), ft.Button("Calcular", on_click=calcular)])
        card.content = col
        content.extend([card, self.crear_panel_formula("N_eff / N_∞ = 1 - [(α+2)/(2αΔ)] · [ 2a/R + (3 / 2n₂kR)^(2/3) ]", "Cálculo macrocurvaturas")])
        self.set_main_content("🔄 Análisis Macrocurvaturas", ft.Colors.WHITE, content)

    def v_modelos(self):
        content = []
        card, p_izq, p_der = self.crear_tarjeta_dividida()
        p_izq.controls.append(ft.Text("Dispersión G.652 ➔ TRADICIONAL", size=16, weight=ft.FontWeight.BOLD))

        r1, e_l = self.crear_fila_input("Long. Onda (λ):", "Ej. 1550.0", "[nm]", "", "λ", "Punto análisis.")
        r2, e_l0 = self.crear_fila_input("Disp. Cero (λ₀):", "Ej. 1310.0", "[nm]", "", "λ₀", "Punto nulo.")
        r3, e_s0 = self.crear_fila_input("Pendiente (S₀):", "Ej. 0.092", "[ps/(nm²·km)]", "", "S₀", "Pendiente nula.")
        lbl_res = ft.Text("D(λ) = -- ps/(nm·km)", size=18, weight=ft.FontWeight.BOLD, color="#66bb6a")
        p_izq.controls.extend([r1, r2, r3, ft.Container(content=lbl_res, padding=10)])

        def calcular(e):
            try:
                res = MotorCalculoOptico.calc_317_dispersion_g652(float(e_l.value), float(e_l0.value), float(e_s0.value))
                lbl_res.value = f"D(λ) = {res:.4f} ps/(nm·km)"
                fig = MotorGrafico.plot_g652(float(e_l0.value), float(e_s0.value))
                self.mostrar_grafica(p_der, fig)
            except Exception as ex: self.mostrar_error(str(ex))

        p_izq.controls.append(ft.Button("Calcular y Graficar D", on_click=calcular))
        content.extend([card, self.crear_panel_formula("D(λ) = (S₀ / 4) · [ λ - (λ₀⁴ / λ³) ]", "Dispersión G.652")])
        self.set_main_content("📊 Modelos Estándar", ft.Colors.WHITE, content)

    # ==========================================
    # VISTAS DEL MOTOR DE DISPERSIÓN 
    # ==========================================
    def v_geom(self):
        content = []
        card1 = ft.Container(bgcolor="#1e1e1e", padding=20, border_radius=10, margin=15)
        col1 = ft.Column(controls=[ft.Text("Índice de Refracción (n = c/v) ⮀ OMNIDIRECCIONAL", size=16, weight=ft.FontWeight.BOLD)])
        r1, e_n = self.crear_fila_input("Índice (n):", "Ej. 1.48", "[Adim]", "", "n", "Índice de refracción.")
        r2, e_v = self.crear_fila_input("Velocidad (v):", "Ej. 2e8", "[m/s]", "", "v", "Velocidad de luz.")
        
        def resolver_nv(e):
            ents = {"n": e_n, "v": e_v}
            funcs = { "n": lambda ll: MotorModuloA.indice_refraccion(ll["v"]), "v": lambda ll: MotorModuloA.velocidad_medio(ll["n"]) }
            inc, res = self._resolver_omni(ents, funcs)
            if inc == "v": e_v.value = f"{res:.2e}"

        col1.controls.extend([r1, r2, ft.Button("Resolver n/v", on_click=resolver_nv, bgcolor="#8d6e1f", color=ft.Colors.WHITE)])
        card1.content = col1
        content.extend([card1, self.crear_panel_formula("n = c / v", "Fórmula base geométrica")])

        card2, p_izq2, p_der2 = self.crear_tarjeta_dividida()
        p_izq2.controls.append(ft.Text("Ley de Snell (Refracción) ⮀ OMNIDIRECCIONAL", size=16, weight=ft.FontWeight.BOLD))
        r1_s, e_sn1 = self.crear_fila_input("Índice Origen (n₁):", "Ej. 1.48", "[Medio 1]", "", "n₁", "Índice de Zona Transmisora")
        r2_s, e_sn2 = self.crear_fila_input("Índice Destino (n₂):", "Ej. 1.46", "[Medio 2]", "", "n₂", "Índice de Zona Receptora")
        r3_s, e_th1 = self.crear_fila_input("Áng. Incidencia (θ₁):", "Ej. 30.0", "[Grados °]", "", "θ₁", "Ángulo de Choque (Incidencia)")
        r4_s, e_th2 = self.crear_fila_input("Áng. Refracción (θ₂):", "Ej. 45.0", "[Grados °]", "", "θ₂", "Ángulo de Desviación")
        p_izq2.controls.extend([r1_s, r2_s, r3_s, r4_s])

        def resolver_snell(e):
            ents = {"n1": e_sn1, "n2": e_sn2, "th1": e_th1, "th2": e_th2}
            funcs = {
                "th2": lambda ll: MotorModuloA.angulo_refraccion_snell(ll["n1"], ll["n2"], ll["th1"]),
                "th1": lambda ll: MotorModuloA.snell_inverso_theta1(ll["n1"], ll["n2"], ll["th2"]),
                "n1":  lambda ll: MotorModuloA.snell_inverso_n1(ll["n2"], ll["th1"], ll["th2"]),
                "n2":  lambda ll: MotorModuloA.snell_inverso_n2(ll["n1"], ll["th1"], ll["th2"])
            }
            inc, res = self._resolver_omni(ents, funcs)
            if inc:
                fig = MotorGrafico.plot_snell(float(e_sn1.value), float(e_sn2.value), float(e_th1.value), float(e_th2.value))
                self.mostrar_grafica(p_der2, fig)

        p_izq2.controls.append(ft.Button("Resolver y Dibujar Snell", on_click=resolver_snell, bgcolor="#8d6e1f", color=ft.Colors.WHITE))
        content.extend([card2, self.crear_panel_formula("n₁ · sin(θ₁) = n₂ · sin(θ₂)", "Relación de ángulos y refracciones en fronteras.")])

        self.set_main_content("📐 Óptica Geométrica", "#d4af37", content)

    def v_parametros(self):
        content = []
        card, p_izq, p_der = self.crear_tarjeta_dividida()
        p_izq.controls.append(ft.Text("Frecuencia Normalizada ⮀ OMNIDIRECCIONAL", size=16, weight=ft.FontWeight.BOLD))

        r1, e_a = self.crear_fila_input("Radio Núcleo (a):", "Ej. 25.0", "[µm]", "", "a", "Radio Esférico Interno")
        r2, e_lam = self.crear_fila_input("Longitud Onda (λ):", "Ej. 1300.0", "[nm]", "", "λ", "Longitud Espectro Óptico")
        r3, e_na = self.crear_fila_input("Apertura Num. (NA):", "Ej. 0.22", "[Adim]", "", "NA", "Apertura Numérica (NA)")
        r4, e_v = self.crear_fila_input("Número V:", "Ej. 2.4", "[Adim]", "", "V", "Frecuencia Normalizada")
        lbl_modos = ft.Text("Modos Guiados: --", size=18, weight=ft.FontWeight.BOLD, color="#d4af37")
        p_izq.controls.extend([r1, r2, r3, r4, ft.Container(content=lbl_modos, padding=10)])

        def resolver(e):
            ents = {"a": e_a, "lam": e_lam, "na": e_na, "v": e_v}
            funcs = {
                "v": lambda ll: MotorModuloA.frecuencia_normalizada_v(ll["a"], ll["lam"], ll["na"]),
                "a": lambda ll: MotorModuloA.v_inverso_a(ll["v"], ll["lam"], ll["na"]),
                "lam": lambda ll: MotorModuloA.v_inverso_lam(ll["v"], ll["a"], ll["na"]),
                "na": lambda ll: MotorModuloA.v_inverso_na(ll["v"], ll["a"], ll["lam"])
            }
            inc, res = self._resolver_omni(ents, funcs)
            if inc:
                v_final = float(e_v.value)
                m_esc = MotorModuloA.modos_guiados_escalonado(v_final)
                lbl_modos.value = f"Modos Escalonados: {m_esc}"
                
                fig = MotorGrafico.plot_numero_v(float(e_a.value), float(e_lam.value)/1000.0, float(e_na.value))
                self.mostrar_grafica(p_der, fig)

        p_izq.controls.append(ft.Button("Resolver y Graficar V", on_click=resolver, bgcolor="#8d6e1f", color=ft.Colors.WHITE))
        content.extend([card, self.crear_panel_formula("V = (2πa / λ) · NA", "Parámetro unívoco adimensional que rige los modos.")])
        self.set_main_content("🔢 Número V y Modos", "#d4af37", content)

    def v_dispersion(self):
        content = []
        card, p_izq, p_der = self.crear_tarjeta_dividida()
        p_izq.controls.append(ft.Text("Ensanchamiento Total (Cromático) ➔ TRADICIONAL", size=16, weight=ft.FontWeight.BOLD))
        
        r1, e_ed = self.crear_fila_input("Coef. Dispersión (D):", "Ej. 17.0", "[ps/(nm·km)]", "", "D", "Coeficiente Empírico Cromático")
        r2, e_el = self.crear_fila_input("Longitud (L):", "Ej. 50.0", "[km]", "", "L", "Alcance Completo de Red")
        r3, e_esig = self.crear_fila_input("Ancho Espectral (σ_λ):", "Ej. 2.0", "[nm]", "", "σ_λ", "Dispersión Óptica de Hardware")
        lbl_ens = ft.Text("σ = -- ps", size=18, weight=ft.FontWeight.BOLD, color="#d4af37")
        p_izq.controls.extend([r1, r2, r3, ft.Container(content=lbl_ens, padding=10)])
        
        def calc_ensanchamiento(e):
            try:
                res = MotorModuloA.ensanchamiento_total(float(e_ed.value), float(e_el.value), float(e_esig.value))
                lbl_ens.value = f"σ = {res:.2f} ps"
                fig = MotorGrafico.plot_ensanchamiento(res)
                self.mostrar_grafica(p_der, fig)
                self.reproducir_exito()
            except Exception as ex: self.mostrar_error(str(ex))

        p_izq.controls.append(ft.Button("Calcular y Graficar", on_click=calc_ensanchamiento, bgcolor="#8d6e1f", color=ft.Colors.WHITE))
        content.extend([card, self.crear_panel_formula("σ = |D(λ) · L · σ_λ|", "D(λ) = Coeficiente Cromático | L = Longitud | σ_λ = Ancho espectral")])
        self.set_main_content("⏱️ Dispersión y Retardos", "#d4af37", content)


    # ==========================================
    # VISTAS DEL MOTOR MATEMÁTICO (MÓDULO B)
    # ==========================================
    def v_modb_freq(self):
        content = []
        card, p_izq, p_der = self.crear_tarjeta_dividida()
        p_izq.controls.append(ft.Text("Frecuencia Normalizada (V) ⮀ OMNIDIRECCIONAL", size=16, weight=ft.FontWeight.BOLD))
        
        r1, e_a = self.crear_fila_input("Radio Núcleo (a):", "Ej. 25.0", "[µm]", "", "a", "Radio Esférico Interno")
        r2, e_lam = self.crear_fila_input("Longitud Onda (λ):", "Ej. 1300.0", "[nm]", "", "λ", "Longitud de Onda")
        r3, e_na = self.crear_fila_input("Apertura Num. (AN):", "Ej. 0.22", "[Adim]", "", "AN", "Apertura Numérica")
        r4, e_v = self.crear_fila_input("Frecuencia V:", "Ej. 2.4", "[Adim]", "", "V", "Monomodo < 2.4048")
        lbl_modos = ft.Text("Modos Guiados: --", size=18, weight=ft.FontWeight.BOLD, color="#66bb6a")
        p_izq.controls.extend([r1, r2, r3, r4, ft.Container(content=lbl_modos, padding=10)])
        
        def resolver_v_modos(e):
            ents = {"a": e_a, "lam": e_lam, "an": e_na, "v": e_v}
            funcs = {
                "v": lambda ll: MotorModuloB.frecuencia_normalizada_v(ll["a"], ll["lam"], ll["an"]),
                "a": lambda ll: MotorModuloB.v_inverso_a(ll["v"], ll["lam"], ll["an"]),
                "lam": lambda ll: MotorModuloB.v_inverso_lam(ll["v"], ll["a"], ll["an"]),
                "an": lambda ll: MotorModuloB.v_inverso_an(ll["v"], ll["a"], ll["lam"])
            }
            inc, res = self._resolver_omni(ents, funcs)
            if inc:
                v_final = float(e_v.value)
                m_esc = MotorModuloB.modos_step_index(v_final)
                lbl_modos.value = f"Modos Escalonados: {int(m_esc)}"
                fig = MotorGrafico.plot_numero_v(float(e_a.value), float(e_lam.value)/1000.0, float(e_na.value))
                self.mostrar_grafica(p_der, fig)

        p_izq.controls.append(ft.Button("Resolver y Graficar V", on_click=resolver_v_modos, bgcolor="#12402d", color=ft.Colors.WHITE))
        content.extend([card, self.crear_panel_formula("V = (2πa / λ) · AN", "Dictamen matemático Monomodo / Multimodo.")])
        self.set_main_content("🔢 Frecuencia Normalizada y Modos", "#66bb6a", content)

    def v_modb_corte(self):
        content = []
        card, p_izq, p_der = self.crear_tarjeta_dividida()
        p_izq.controls.append(ft.Text("Condición de Corte Monomodo ⮀ OMNIDIRECCIONAL", size=16, weight=ft.FontWeight.BOLD))
        
        r1, e_lam_c = self.crear_fila_input("Long. Corte (λ_c):", "Ej. 1200.0", "[nm]", "", "λ_c", "Longitud de onda de corte absoluto")
        r2, e_a = self.crear_fila_input("Radio Núcleo (a):", "Ej. 4.0", "[µm]", "", "a", "Radio Esférico")
        r3, e_an = self.crear_fila_input("Apertura Num. (AN):", "Ej. 0.12", "[Adim]", "", "AN", "Apertura Numérica")
        p_izq.controls.extend([r1, r2, r3])

        def resolver_corte(e):
            ents = {"lam_c": e_lam_c, "a": e_a, "an": e_an}
            funcs = {
                "lam_c": lambda ll: MotorModuloB.longitud_corte(ll["a"], ll["an"]),
                "a": lambda ll: MotorModuloB.longitud_corte_inverso_a(ll["lam_c"], ll["an"]),
                "an": lambda ll: MotorModuloB.longitud_corte_inverso_an(ll["lam_c"], ll["a"])
            }
            for ent in ents.values(): 
                ent.color = ft.Colors.WHITE
                ent.border_color = "#555555"
            vacios = {k: v for k, v in ents.items() if not v.value.strip()}
            if len(vacios) != 1: return self.mostrar_error("Deja exactamente UN campo vacío.")
            try:
                ll = {k: float(v.value) for k, v in ents.items() if v.value.strip()}
                inc = list(vacios.keys())[0]
                if "lam_c" in ll: ll["lam_c"] /= 1000.0
                res = funcs[inc](ll)
                if inc == "lam_c": res *= 1000.0
                
                ents[inc].value = f"{res:.4f}"
                ents[inc].color = "#66bb6a"
                ents[inc].border_color = "#66bb6a"
                
                fig = MotorGrafico.plot_corte(float(e_lam_c.value) / 1000.0, float(e_a.value), float(e_an.value))
                self.mostrar_grafica(p_der, fig)
                self.reproducir_exito()
            except Exception as ex: self.mostrar_error(str(ex))

        p_izq.controls.append(ft.Button("Resolver y Graficar Corte", on_click=resolver_corte, bgcolor="#12402d", color=ft.Colors.WHITE))
        content.extend([card, self.crear_panel_formula("λ_c = (2πa · AN) / 2.4048", "Punto límite absoluto bajo el cual todos los modos superiores colapsan.")])
        self.set_main_content("✂️ Longitud de Onda de Corte", "#66bb6a", content)

    def v_modb_mfd(self):
        content = []
        card, p_izq, p_der = self.crear_tarjeta_dividida()
        p_izq.controls.append(ft.Text("Aproximación de Marcuse ➔ TRADICIONAL", size=16, weight=ft.FontWeight.BOLD))
        
        r1, e_a = self.crear_fila_input("Radio Núcleo (a):", "Ej. 4.0", "[µm]", "", "a", "Tamaño físico real del núcleo.")
        r2, e_v = self.crear_fila_input("Valor V:", "Ej. 2.0", "[Adim]", "", "V", "Frecuencia Normalizada (V)")
        lbl_mfd = ft.Text("MFD (2ω₀) = --", size=18, weight=ft.FontWeight.BOLD, color="#66bb6a")
        p_izq.controls.extend([r1, r2, ft.Container(content=lbl_mfd, padding=10)])
        
        def calc_mfd(e):
            try:
                a_val, v_val = float(e_a.value), float(e_v.value)
                mfd = MotorModuloB.mfd_marcuse(a_val, v_val)
                lbl_mfd.value = f"MFD (2ω₀) = {mfd:.4f}"
                fig = MotorGrafico.plot_mfd(a_val, mfd)
                self.mostrar_grafica(p_der, fig)
                self.reproducir_exito()
            except Exception as ex: self.mostrar_error(str(ex))
            
        p_izq.controls.append(ft.Button("Calcular y Graficar MFD", on_click=calc_mfd, bgcolor="#12402d", color=ft.Colors.WHITE))
        content.extend([card, self.crear_panel_formula("2ω₀ = 2a [ 0.65 + 1.619/(V^1.5) + 2.879/(V^6) ]", "Fórmula de Marcuse para dispersión de campana.")])
        self.set_main_content("⭕ Diámetro de Campo Modal (MFD)", "#66bb6a", content)


    # ==========================================
    # VISTAS DEL MOTOR DE MODULACIÓN
    # ==========================================
    def v_ask(self):
        content = []
        card, p_izq, p_der = self.crear_tarjeta_dividida()
        p_izq.controls.append(ft.Text("Generador de Ondas ➔ DIRECTO", size=16, weight=ft.FontWeight.BOLD))

        r1, e_es = self.crear_fila_input("Amplitud (E_s):", "Ej. 1.0", "[V/m]", "", "Amplitud Portadora", "Intensidad base.")
        r2, e_m = self.crear_fila_input("Índice (m):", "Ej. 0.8", "[Adim]", "", "Índice Modulación", "Grado de afectación de la amplitud.")
        r3, e_fc = self.crear_fila_input("Frec. Portadora (f_c):", "Ej. 20.0", "[Hz]", "", "f_c", "Frecuencia base simulada.")
        r4, e_fm = self.crear_fila_input("Frec. Mensaje (f_m):", "Ej. 2.0", "[Hz]", "", "f_m", "Frecuencia analógica del mensaje.")
        p_izq.controls.extend([r1, r2, r3, r4])

        def graficar_ask(e):
            try:
                fig = MotorModulacion.plot_ask(float(e_es.value), float(e_m.value), float(e_fc.value), float(e_fm.value))
                self.mostrar_grafica(p_der, fig)
                self.reproducir_exito()
            except ValueError: self.mostrar_error("Por favor, ingresa números válidos.")

        p_izq.controls.append(ft.Button("Generar Gráficas ASK", on_click=graficar_ask, bgcolor="#38006b", color=ft.Colors.WHITE))
        content.extend([card, self.crear_panel_formula("E_ASK(t) = E_s [ 1 + m · cos(2π f_m t) ] cos(2π f_c t)", "Modulación en Amplitud.")])
        self.set_main_content("📈 Modulación ASK (AM Óptico)", "#ab47bc", content)

    def v_psk(self):
        content = []
        card, p_izq, p_der = self.crear_tarjeta_dividida()
        p_izq.controls.append(ft.Text("Codificación BPSK ➔ DIRECTO", size=16, weight=ft.FontWeight.BOLD))

        r1, e_es = self.crear_fila_input("Amplitud (E_s):", "Ej. 1.0", "[V/m]", "", "Amplitud Portadora", "Intensidad base constante.")
        r2, e_fc = self.crear_fila_input("Frec. Portadora (f_c):", "Ej. 5.0", "[Hz]", "[Recomendado: 2 a 5 Hz]", "Frecuencia Portadora", "Usa valores bajos para ver saltos de fase (180°).")
        r3, e_bits = self.crear_fila_input("Secuencia Bits:", "Ej. 10110", "[Cualquier texto 0s y 1s]", "", "Tren de Bits BPSK", "Secuencia binaria libre (ej. 111000101).")
        p_izq.controls.extend([r1, r2, r3])

        def graficar_psk(e):
            try:
                fig = MotorModulacion.plot_psk(float(e_es.value), float(e_fc.value), e_bits.value)
                self.mostrar_grafica(p_der, fig)
                self.reproducir_exito()
            except ValueError: self.mostrar_error("Por favor, ingresa números válidos.")

        p_izq.controls.append(ft.Button("Generar Gráficas BPSK", on_click=graficar_psk, bgcolor="#38006b", color=ft.Colors.WHITE))
        content.extend([card, self.crear_panel_formula("v_{bpsk}(t) = b(t) · √(2P) · cos(2π f_c t)", "b(t) es ±1 según el bit. √(2P) equivale a la Amplitud E_s.")])
        self.set_main_content("📉 Modulación BPSK (Binaria de Fase)", "#ab47bc", content)

    def v_fsk(self):
        content = []
        card, p_izq, p_der = self.crear_tarjeta_dividida()
        p_izq.controls.append(ft.Text("Generador FSK ➔ DIRECTO", size=16, weight=ft.FontWeight.BOLD))

        r1, e_es = self.crear_fila_input("Amplitud (E_s):", "Ej. 1.0", "[V/m]", "", "Amplitud", "Intensidad base constante.")
        r2, e_df = self.crear_fila_input("Desviación (Δf):", "Ej. 5.0", "[Hz]", "", "Δf", "Desviación pico hacia arriba/abajo.")
        r3, e_fc = self.crear_fila_input("Frec. Portadora (f_c):", "Ej. 20.0", "[Hz]", "", "f_c", "Frecuencia central simulada.")
        r4, e_fm = self.crear_fila_input("Frec. Mensaje (f_m):", "Ej. 2.0", "[Hz]", "", "f_m", "Frecuencia de la tasa de cambio.")
        p_izq.controls.extend([r1, r2, r3, r4])

        def graficar_fsk(e):
            try:
                fig = MotorModulacion.plot_fsk(float(e_es.value), float(e_df.value), float(e_fc.value), float(e_fm.value))
                self.mostrar_grafica(p_der, fig)
                self.reproducir_exito()
            except ValueError: self.mostrar_error("Por favor, ingresa números válidos.")

        p_izq.controls.append(ft.Button("Generar Gráficas FSK", on_click=graficar_fsk, bgcolor="#38006b", color=ft.Colors.WHITE))
        content.extend([card, self.crear_panel_formula("E_FSK(t) = E_s · cos[ 2π f_c t + (Δf / f_m) · sin(2π f_m t) ]", "Desplazamiento analógico de frecuencia.")])
        self.set_main_content("📊 Modulación FSK", "#ab47bc", content)

    def v_dpsk(self):
        content = []
        card, p_izq, p_der = self.crear_tarjeta_dividida()
        p_izq.controls.append(ft.Text("Codificación DPSK ➔ DIRECTO", size=16, weight=ft.FontWeight.BOLD))

        r1, e_es = self.crear_fila_input("Amplitud (E_s):", "Ej. 1.0", "[V/m]", "", "Amplitud Portadora", "Intensidad de la onda luz base.")
        r2, e_fc = self.crear_fila_input("Frec. Portadora (f_c):", "Ej. 5.0", "[Hz]", "[Recomendado: 2 a 5 Hz]", "Frecuencia", "Igual que PSK, usa valores bajos.")
        r3, e_bits = self.crear_fila_input("Secuencia Bits:", "Ej. 10110", "[0s y 1s]", "", "Tren Bits", "Secuencia binaria libre.")
        p_izq.controls.extend([r1, r2, r3])

        def graficar_dpsk(e):
            try:
                fig = MotorModulacion.plot_dpsk(float(e_es.value), float(e_fc.value), e_bits.value)
                self.mostrar_grafica(p_der, fig)
                self.reproducir_exito()
            except ValueError: self.mostrar_error("Revisa que Amplitud y Frecuencia sean válidos.")

        p_izq.controls.append(ft.Button("Generar Gráficas DPSK", on_click=graficar_dpsk, bgcolor="#38006b", color=ft.Colors.WHITE))
        content.extend([card, self.crear_panel_formula("d_k = d_{k-1} ⊕ b_k   |   E_DPSK(t) = E_s · cos(2π f_c t + d_k · π)", "Modulación Diferencial de Fase.")])
        self.set_main_content("🔢 Modulación DPSK", "#ab47bc", content)


def main(page: ft.Page):
    OpticaApp(page)

if __name__ == "__main__":
    ft.run(main)