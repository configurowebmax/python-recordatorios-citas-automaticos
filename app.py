"""
=====================================================================
 Generador de Recordatorios de Citas
 ConfiguroWeb · 2026 · Python real en el navegador (PyScript)
=====================================================================
"""
from pyscript import document, window
from js import localStorage
import json
import math

APP_CLAVE = "python_recordatorios_citas_automaticos_datos"
VERSION = "1.0.0"


# =====================================================================
#  Lógica de negocio
# =====================================================================
class Calculadora:
    """Modelo de cálculo de Generador de Recordatorios de Citas."""

    def __init__(self, cliente, fecha, hora, servicio, duracion):
        self.cliente = float(cliente)
        self.fecha = float(fecha)
        self.hora = float(hora)
        self.servicio = float(servicio)
        self.duracion = float(duracion)

    def calcular(self):
        """Ejecuta el cálculo principal y devuelve un dict de resultados."""

        plantilla = (f"Hola {self.cliente}, te recordamos tu cita de "
                     f"{self.servicio} el {self.fecha} a las {self.hora}. "
                     f"Duración aproximada: {int(self.duracion)} min. "
                     f"¡Te esperamos! Responde para confirmar.")
        return {"mensaje": plantilla, "caracteres": len(plantilla)}


    def diagnostico(self, resultados):
        """Texto explicativo del resultado."""

        if resultados["caracteres"] > 160:
            return "⚠️ El mensaje supera 160 caracteres (límite SMS). Considera acortarlo."
        return "✅ Mensaje listo para enviar por SMS o WhatsApp."



# =====================================================================
#  Formateadores
# =====================================================================
def fmt_moneda(v):
    if v is None:
        return "—"
    if math.isinf(v):
        return "∞"
    return f"${v:,.0f}"

def fmt_num(v):
    if v is None:
        return "—"
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return f"{v:,}"

def fmt_pct(v):
    if v is None:
        return "—"
    return f"{v:.1f}%"


# =====================================================================
#  Persistencia localStorage
# =====================================================================
def cargar_guardado():
    try:
        raw = localStorage.getItem(APP_CLAVE)
        if raw:
            return json.loads(raw)
    except Exception:
        pass
    return None

def guardar_ls(datos):
    try:
        localStorage.setItem(APP_CLAVE, json.dumps(datos))
        return True
    except Exception:
        return False


# =====================================================================
#  UI helpers
# =====================================================================
def input_float(eid):
    el = document.querySelector(f"#{eid}")
    if not el or not el.value:
        return 0.0
    try:
        return float(el.value)
    except (ValueError, TypeError):
        return 0.0

def mostrar(html, clase=""):
    caja = document.querySelector("#resultado")
    caja.innerHTML = html
    caja.classList.remove("hidden", "is-error", "is-success")
    if clase:
        caja.classList.add(clase)


# =====================================================================
#  Handlers
# =====================================================================
def calcular_handler(event=None):
    """Lee inputs, instancia, calcula y muestra."""

    c = Calculadora(
        input_float("cliente") if False else document.querySelector("#cliente").value or "",
        document.querySelector("#fecha").value or "",
        document.querySelector("#hora").value or "",
        document.querySelector("#servicio").value or "",
        input_float("duracion"),
    )
    r = c.calcular()
    html = f"""
      <div class="result-value">📅 Recordatorio generado</div>
      <p class="result-detail" style="white-space:pre-wrap; background:#fff; padding:1rem; border-radius:8px; border:1px solid var(--cweb-border);">{r["mensaje"]}</p>
      <p class="result-detail">📝 {r["caracteres"]} caracteres · {c.diagnostico(r)}</p>
      <button class="btn btn-primary mt-2" onclick="navigator.clipboard.writeText(`{r['mensaje']}`);alert('Copiado!')">📋 Copiar</button>
    """
    mostrar(html, clase="is-success")



def guardar_datos(event=None):
    datos = {
            "cliente": input_float("cliente"),
            "fecha": input_float("fecha"),
            "hora": input_float("hora"),
            "servicio": input_float("servicio"),
            "duracion": input_float("duracion"),
        "version": VERSION,
    }
    ok = guardar_ls(datos)
    if ok:
        mostrar("💾 Datos guardados en este navegador.", clase="is-success")
    else:
        mostrar("❌ No se pudieron guardar los datos.", clase="is-error")


def cargar_al_inicio():
    datos = cargar_guardado()
    if not datos:
        return
    try:
        if "cliente" in datos:
            document.querySelector("#cliente").value = datos["cliente"]
        if "fecha" in datos:
            document.querySelector("#fecha").value = datos["fecha"]
        if "hora" in datos:
            document.querySelector("#hora").value = datos["hora"]
        if "servicio" in datos:
            document.querySelector("#servicio").value = datos["servicio"]
        if "duracion" in datos:
            document.querySelector("#duracion").value = datos["duracion"]
        aviso = document.querySelector("#resultado")
        aviso.innerHTML = "📂 Datos cargados. Pulsa <em>Calcular</em>."
        aviso.classList.remove("hidden")
    except Exception:
        pass


def inicializar():
    cargar_al_inicio()
    window.dispatchEvent(window.Event.new("py:ready"))

inicializar()
