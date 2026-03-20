import tkinter as tk
from tkinter import ttk, messagebox

# ─── Paleta de colores ───────────────────────────────────────
BG_DARK  = "#0f1117"
BG_CARD  = "#1a1d27"
BG_INPUT = "#252836"
ACCENT   = "#ff6584"   # Rosa/rojo – temática parque
ACCENT2  = "#ffd166"   # Amarillo
TEXT     = "#e8e6f0"
TEXT_DIM = "#8a8aa0"
SUCCESS  = "#43e97b"
WARNING  = "#f7971e"
BORDER   = "#2e3148"
INFO     = "#4facfe"

COSTO_POR_JUEGO = 50  # soles


# ─── Funciones de cálculo ────────────────────────────────────

def calcular_descuento(edad: int) -> float:
    """Retorna el porcentaje de descuento según la edad."""
    if edad < 10:
        return 0.25
    elif edad <= 17:
        return 0.10
    else:
        return 0.0


def calcular_total(edad: int, juegos: int) -> tuple:
    """
    Retorna (subtotal, descuento_pct, monto_descuento, total_a_pagar).
    """
    subtotal        = juegos * COSTO_POR_JUEGO
    descuento_pct   = calcular_descuento(edad)
    monto_descuento = subtotal * descuento_pct
    total           = subtotal - monto_descuento
    return subtotal, descuento_pct, monto_descuento, total


def categoria_edad(edad: int) -> str:
    """Retorna la categoría de visitante según la edad."""
    if edad < 10:
        return "Niño (< 10)"
    elif edad <= 17:
        return "Joven (10-17)"
    else:
        return "Adulto (18+)"


# ─── Lógica de UI ────────────────────────────────────────────

def procesar(vars_: dict, lista: list, lbl_res, tree, lbl_recaudado):
    """Valida, calcula y registra al visitante."""
    nombre = vars_["nombre"].get().strip()
    if not nombre:
        messagebox.showwarning("Campo vacío", "Ingresa el nombre del visitante.")
        return

    try:
        edad = int(vars_["edad"].get().strip())
        if edad <= 0 or edad > 120:
            raise ValueError
    except ValueError:
        messagebox.showerror("Dato inválido", "La edad debe ser un número entero entre 1 y 120.")
        return

    try:
        juegos = int(vars_["juegos"].get().strip())
        if juegos <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Dato inválido", "La cantidad de juegos debe ser un número entero positivo.")
        return

    subtotal, pct, descuento, total = calcular_total(edad, juegos)
    categoria = categoria_edad(edad)

    registro = {
        "nombre":    nombre,
        "edad":      edad,
        "categoria": categoria,
        "juegos":    juegos,
        "subtotal":  subtotal,
        "descuento": pct * 100,
        "monto_dto": descuento,
        "total":     total,
    }
    lista.append(registro)

    # Resultado visual
    pct_txt = f"{pct*100:.0f}%" if pct > 0 else "Sin descuento"
    lbl_res.config(
        text=(f"✔  {nombre}  |  {edad} años  |  {categoria}\n"
              f"   Juegos utilizados : {juegos}  ×  S/. {COSTO_POR_JUEGO:.2f}\n"
              f"   Subtotal          : S/. {subtotal:.2f}\n"
              f"   Descuento ({pct_txt:>13}) : - S/. {descuento:.2f}\n"
              f"   ─────────────────────────────\n"
              f"   TOTAL A PAGAR      : S/. {total:.2f}"),
        fg=SUCCESS,
    )

    # Historial
    tree.insert("", "end", values=(
        nombre,
        edad,
        categoria,
        juegos,
        f"S/. {subtotal:.2f}",
        f"{pct*100:.0f}%",
        f"S/. {total:.2f}",
    ))

    # Actualizar recaudado
    total_rec = sum(v["total"] for v in lista)
    lbl_recaudado.config(
        text=f"💰  Total recaudado por el parque:   S/. {total_rec:,.2f}",
        fg=ACCENT2,
    )


def limpiar(vars_: dict, lbl_res, entry_nombre):
    for v in vars_.values():
        v.set("")
    lbl_res.config(text="")
    entry_nombre.focus()


# ─── Construcción de ventana ─────────────────────────────────

def abrir(root):
    win = tk.Toplevel(root)
    win.title("Ejercicio 2 – Parque de Diversiones")
    win.configure(bg=BG_DARK)
    win.geometry("860x640")
    win.resizable(False, False)

    # ── Encabezado ──
    hdr = tk.Frame(win, bg=ACCENT, height=60)
    hdr.pack(fill="x")
    tk.Label(hdr, text="🎡  SISTEMA DE PAGO – PARQUE DE DIVERSIONES",
             bg=ACCENT, fg="white",
             font=("Consolas", 13, "bold")).pack(pady=10)
    tk.Label(hdr, text=f"Costo por juego: S/. {COSTO_POR_JUEGO:.2f}",
             bg=ACCENT, fg="#ffe0e8",
             font=("Consolas", 9)).pack()

    body = tk.Frame(win, bg=BG_DARK)
    body.pack(fill="both", expand=True, padx=20, pady=14)

    # ════════════════════════════════
    # Panel izquierdo – formulario
    # ════════════════════════════════
    left = tk.Frame(body, bg=BG_CARD, highlightthickness=1,
                    highlightbackground=BORDER)
    left.pack(side="left", fill="y", padx=(0, 12), ipadx=14, ipady=10)

    def lbl(parent, text, size=10, color=TEXT, bold=False):
        return tk.Label(parent, text=text, fg=color, bg=parent["bg"],
                        font=("Consolas", size, "bold" if bold else "normal"))

    def entry(parent, var, w=26):
        return tk.Entry(parent, textvariable=var, width=w,
                        bg=BG_INPUT, fg=TEXT, insertbackground=ACCENT,
                        relief="flat", font=("Consolas", 11),
                        highlightthickness=1, highlightcolor=ACCENT,
                        highlightbackground=BORDER)

    def btn(parent, text, cmd, color=ACCENT, fg="white", **kw):
        return tk.Button(parent, text=text, command=cmd,
                         bg=color, fg=fg, relief="flat",
                         font=("Consolas", 10, "bold"),
                         padx=12, pady=6, cursor="hand2",
                         activebackground=ACCENT2, activeforeground=BG_DARK, **kw)

    lbl(left, "NUEVO VISITANTE", color=ACCENT, bold=True).pack(
        anchor="w", padx=8, pady=(10, 2))
    tk.Frame(left, bg=BORDER, height=1).pack(fill="x", pady=4)

    # Nombre
    lbl(left, "Nombre completo", color=TEXT_DIM).pack(anchor="w", padx=8, pady=(8, 2))
    vars_ = {k: tk.StringVar() for k in ("nombre", "edad", "juegos")}
    ent_nombre = entry(left, vars_["nombre"])
    ent_nombre.pack(padx=8, pady=(0, 8))

    # Edad
    lbl(left, "Edad (años)", color=TEXT_DIM).pack(anchor="w", padx=8, pady=(0, 2))
    entry(left, vars_["edad"]).pack(padx=8, pady=(0, 8))

    # Juegos
    lbl(left, "Cantidad de juegos", color=TEXT_DIM).pack(anchor="w", padx=8, pady=(0, 2))
    entry(left, vars_["juegos"]).pack(padx=8, pady=(0, 10))

    # Tabla de descuentos
    tk.Frame(left, bg=BORDER, height=1).pack(fill="x", pady=4)
    lbl(left, "TABLA DE DESCUENTOS", size=9, color=ACCENT, bold=True).pack(
        anchor="w", padx=8, pady=(4, 4))

    descuentos = [
        ("🧒 Niño  (< 10 años)",    "25%"),
        ("🧑 Joven (10 – 17 años)", "10%"),
        ("👤 Adulto (18+ años)",    "0%"),
    ]
    for cat, pct in descuentos:
        row = tk.Frame(left, bg=BG_CARD)
        row.pack(fill="x", padx=8, pady=1)
        lbl(row, cat, size=9, color=TEXT_DIM).pack(side="left")
        lbl(row, pct, size=9, color=WARNING, bold=True).pack(side="right")

    tk.Frame(left, bg=BORDER, height=1).pack(fill="x", pady=6)

    # Resultado
    lbl_res = tk.Label(left, text="", bg=BG_CARD, fg=SUCCESS,
                       font=("Consolas", 9), justify="left", wraplength=240)
    lbl_res.pack(padx=8, pady=(0, 8), anchor="w")

    # Botones
    bframe = tk.Frame(left, bg=BG_CARD)
    bframe.pack(padx=8, pady=(0, 4))

    lista = []
    lbl_recaudado = None   # se asigna tras crear el widget

    btn(bframe, "  Registrar  ",
        lambda: procesar(vars_, lista, lbl_res, tree, lbl_recaudado)
        ).pack(side="left", padx=(0, 6))

    btn(bframe, "Limpiar",
        lambda: limpiar(vars_, lbl_res, ent_nombre),
        color=BG_INPUT, fg=TEXT_DIM).pack(side="left")

    # ════════════════════════════════
    # Panel derecho – historial
    # ════════════════════════════════
    right = tk.Frame(body, bg=BG_CARD, highlightthickness=1,
                     highlightbackground=BORDER)
    right.pack(side="left", fill="both", expand=True, ipadx=8, ipady=8)

    lbl(right, "HISTORIAL DE VISITANTES", color=ACCENT, bold=True).pack(
        anchor="w", padx=12, pady=(10, 4))

    # Treeview
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Park.Treeview",
                    background=BG_INPUT, foreground=TEXT,
                    fieldbackground=BG_INPUT, rowheight=26,
                    font=("Consolas", 9))
    style.configure("Park.Treeview.Heading",
                    background=ACCENT, foreground="white",
                    font=("Consolas", 9, "bold"), relief="flat")
    style.map("Park.Treeview",
              background=[("selected", ACCENT)],
              foreground=[("selected", "white")])

    cols = ("Nombre", "Edad", "Categoría", "Juegos", "Subtotal", "Dto.", "Total")
    widths = [130, 45, 100, 55, 80, 45, 80]

    tf = tk.Frame(right, bg=BG_CARD)
    tf.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    tree = ttk.Treeview(tf, columns=cols, show="headings",
                        style="Park.Treeview", height=14)
    for col, w in zip(cols, widths):
        tree.heading(col, text=col)
        tree.column(col, width=w, anchor="center")

    sb = ttk.Scrollbar(tf, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sb.set)
    tree.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")

    # ── Total recaudado ──
    tk.Frame(right, bg=BORDER, height=1).pack(fill="x", padx=8, pady=4)

    lbl_recaudado = tk.Label(
        right,
        text="💰  Total recaudado por el parque:   S/. 0.00",
        bg=BG_CARD, fg=TEXT_DIM,
        font=("Consolas", 10, "bold"),
    )
    lbl_recaudado.pack(pady=(4, 8))

    # Botón resumen
    def mostrar_resumen():
        if not lista:
            messagebox.showinfo("Sin datos", "Aún no hay visitantes registrados.")
            return

        total_rec   = sum(v["total"]     for v in lista)
        total_dto   = sum(v["monto_dto"] for v in lista)
        total_juego = sum(v["juegos"]    for v in lista)

        # Contar por categoría
        ninos   = sum(1 for v in lista if v["edad"] < 10)
        jovenes = sum(1 for v in lista if 10 <= v["edad"] <= 17)
        adultos = sum(1 for v in lista if v["edad"] > 17)

        messagebox.showinfo(
            "Resumen del Parque",
            f"Visitantes totales  : {len(lista)}\n"
            f"  • Niños           : {ninos}\n"
            f"  • Jóvenes         : {jovenes}\n"
            f"  • Adultos         : {adultos}\n"
            f"\n"
            f"Juegos utilizados   : {total_juego}\n"
            f"Total descuentos    : S/. {total_dto:,.2f}\n"
            f"─────────────────────────────────\n"
            f"TOTAL RECAUDADO     : S/. {total_rec:,.2f}",
        )

    btn(right, "Ver resumen del parque",
        mostrar_resumen, color=INFO, fg="white").pack(pady=(0, 8))

    ent_nombre.focus()
