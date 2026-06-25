# ÓpticaSuite Pro: Suite de Simulación Electrónica y Óptica

**ÓpticaSuite Pro** es una herramienta computacional interactiva desarrollada para el modelado, cálculo y visualización de sistemas de fibra óptica y esquemas de modulación digital. Este proyecto integra conceptos avanzados de la Maestría en Ciencias en Electrónica de la Universidad de Sonora, proporcionando una interfaz gráfica omnidireccional capaz de resolver incógnitas dinámicas basándose en el ecosistema matemático de la óptica física y geométrica.

La aplicación está construida sobre **Python**, utilizando **Flet** para la interfaz gráfica y **Matplotlib** para el renderizado de gráficos físicos y señales de telecomunicación.

## Arquitectura del Sistema

El proyecto está modularizado para separar la lógica matemática, la generación de visualizaciones y el control de la interfaz de usuario. 

| Módulo | Archivo | Descripción |
| :--- | :--- | :--- |
| **Controlador Principal** | `main.py` | Motor central de la aplicación interactiva. Gestiona el enrutamiento de la UI, la lógica omnidireccional (despeje automático de variables) y el despliegue del framework Flet. |
| **Motor Óptico** | `motor_optico.py` | Contiene los algoritmos para cálculo de atenuación, eficiencia de acoplamiento, dispersión de Rayleigh térmica y modelos estándar G.652. |
| **Motor Dispersión (A)** | `motor_modulo_a.py` | Implementa leyes de óptica geométrica, refracción de Snell, apertura numérica y cálculos de ensanchamiento cromático. |
| **Motor Matemático (B)** | `motor_modulo_b.py` | Evalúa parámetros de fibra como la Frecuencia Normalizada (V), condiciones de corte monomodo y el Diámetro de Campo Modal (MFD) mediante la aproximación de Marcuse. |
| **Motor Modulación** | `motor_modulacion.py` | Generador de señales digitales y ópticas para esquemas de modulación BASK/OOK, BPSK, BFSK y DPSK. |
| **Motor Gráfico** | `motor_grafico.py` | Wrapper de Matplotlib que exporta figuras adaptativas en Base64 para su inyección fluida en la interfaz gráfica. |

## Fundamento Matemático

El motor de cálculo opera utilizando resoluciones exactas y aproximaciones estandarizadas en telecomunicaciones. Algunos de los modelos físicos evaluados incluyen:

* Ley de Snell para refracción y reflexión interna total: $n_1 \cdot \sin(\theta_1) = n_2 \cdot \sin(\theta_2)$
* Atenuación termodinámica de Rayleigh: $\alpha_r = \frac{8\pi^3}{3\lambda^4} (n^2 - 1)^2 \beta_T k_B T_f$
* Frecuencia Normalizada y dictamen de modos: $V = \frac{2\pi a}{\lambda} \text{NA}$
* Aproximación de Marcuse para MFD: $2\omega_0 = 2a \left[ 0.65 + 1.619 V^{-1.5} + 2.879 V^{-6} \right]$
* Ecuaciones portadoras de fase digital (ej. DPSK): $s(t) = A \cdot \cos(2\pi f_c t + d_k \pi)$

## Requisitos del Sistema

Para ejecutar el entorno de simulación localmente, asegúrese de contar con las siguientes dependencias instaladas:

* Python 3.8+
* Flet
* NumPy
* Matplotlib

Puede instalar las librerías necesarias ejecutando:
`pip install flet numpy matplotlib`

## Uso y Ejecución

Para iniciar la suite de simulación, ejecute el controlador principal desde la terminal:

`python main.py`

La interfaz cuenta con **Tarjetas OMNI**. Para utilizarlas, ingrese los parámetros conocidos y deje **exactamente un campo en blanco**. El sistema identificará la incógnita, realizará el despeje algebraico correspondiente, mostrará el resultado numérico y generará la representación gráfica del fenómeno.

## Créditos y Autores

El desarrollo de esta herramienta fue un esfuerzo interdisciplinario de investigación y programación:

* **Óscar Rosas**: Autor principal. Programación integral del controlador visual (`main.py`), arquitectura de la aplicación, refactorización/integración de todos los motores e implementación algorítmica de modulación (ASK, FSK) y modelos físicos.
* **Issac Gómez**: Investigación matemática y co-desarrollo de los módulos de Motor Gráfico y Motor Óptico.
* **Margarita y Patricia**: Investigación matemática para los algoritmos del Motor de Dispersión (Módulo A) y modulación ASK.
* **Germán**: Investigación y estructura base para la modulación PSK y algoritmos del Motor Matemático (Módulo B).
* **Emilio**: Investigación y estructura base para la modulación DPSK y algoritmos del Motor Matemático (Módulo B).
