import tkinter as tk
from tkinter import ttk, messagebox

# ─── Paleta de colores ───────────────────────────────────────
BG_DARK  = "#0f1117"
BG_CARD  = "#1a1d27"
BG_INPUT = "#252836"
ACCENT   = "#6c63ff"
ACCENT2  = "#ff6584"
TEXT     = "#e8e6f0"
TEXT_DIM = "#8a8aa0"
SUCCESS  = "#43e97b"
WARNING  = "#f7971e"
BORDER   = "#2e3148"


# ─── Funciones de cálculo ────────────────────────────────────

def calcular_porcentaje(sueldo: float) -> float:
    """Retorna el porcentaje de aumento según el sueldo base."""
    if sueldo < 4000:
        return 0.15
    elif sueldo <= 7000:
        return 0.10
    else:
        return 0.08


def calcular_nuevo_sueldo(sueldo: float) -> tuple:
    """Retorna (porcentaje, monto_aumento, nuevo_sueldo)."""
    pct    = calcular_porcentaje(sueldo)
    monto  = sueldo * pct
    nuevo  = sueldo + monto
    return pct, monto, nuevo


# ─── Lógica de UI ────────────────────────────────────────────

def procesar(nombre_var, sueldo_var, lista, lbl_res, tree):
    """Valida, calcula y registra al trabajador."""
    nombre = nombre_var.get().strip()
    if not nombre:
        messagebox.showwarning("Campo vacío", "Ingresa el nombre del trabajador.")
        return

    try:
        sueldo = float(sueldo_var.get().strip())
        if sueldo <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Dato inválido", "El sueldo debe ser un número mayor a 0.")
        return

    pct, monto, nuevo = calcular_nuevo_sueldo(sueldo)

    lista.append({
        "nombre": nombre,
        "base": sueldo,
        "porcentaje": pct * 100,
        "aumento": monto,
        "nuevo": nuevo,
    })

    lbl_res.config(
        text=(f"✔  {nombre}\n"
              f"   Base        : ${sueldo:,.2f}\n"
              f"   Aumento ({pct*100:.0f}%) : ${monto:,.2f}\n"
              f"   Nuevo sueldo: ${nuevo:,.2f}"),
        fg=SUCCESS,
    )

    tree.insert("", "end", values=(
        nombre,
        f"${sueldo:,.2f}",
        f"{pct*100:.0f}%",
        f"${monto:,.2f}",
        f"${nuevo:,.2f}",
    ))


def resumen(lista):
    """Muestra un cuadro con totales generales."""
    if not lista:
        messagebox.showinfo("Sin datos", "No hay trabajadores registrados aún.")
        return
    base_total  = sum(t["base"]  for t in lista)
    nuevo_total = sum(t["nuevo"] for t in lista)
    messagebox.showinfo(
        "Resumen general",
        f"Trabajadores registrados : {len(lista)}\n"
        f"Suma sueldos base        : ${base_total:,.2f}\n"
        f"Suma nuevos sueldos      : ${nuevo_total:,.2f}\n"
        f"Incremento total         : ${nuevo_total - base_total:,.2f}",
    )


# ─── Construcción de ventana ─────────────────────────────────

def abrir(root):
    win = tk.Toplevel(root)
    win.title("Ejercicio 1 – Aumento de Sueldos")
    win.configure(bg=BG_DARK)
    win.geometry("780x610")
    win.resizable(False, False)

    lista = []

    # Encabezado
    hdr = tk.Frame(win, bg=ACCENT, height=56)
    hdr.pack(fill="x")
    tk.Label(hdr, text="💼  SISTEMA DE AUMENTO DE SUELDOS",
             bg=ACCENT, fg="white", font=("Consolas", 14, "bold")).pack(pady=14)

    body = tk.Frame(win, bg=BG_DARK)
    body.pack(fill="both", expand=True, padx=20, pady=16)

    # ── Panel izquierdo: formulario ──
    left = tk.Frame(body, bg=BG_CARD, highlightthickness=1,
                    highlightbackground=BORDER)
    left.pack(side="left", fill="y", padx=(0, 12), ipadx=14, ipady=14)

    def lbl(parent, text, size=10, color=TEXT, bold=False):
        w = "bold" if bold else "normal"
        return tk.Label(parent, text=text, fg=color, bg=parent["bg"],
                        font=("Consolas", size, w))

    def entry(parent, var, w=26):
        return tk.Entry(parent, textvariable=var, width=w,
                        bg=BG_INPUT, fg=TEXT, insertbackground=ACCENT,
                        relief="flat", font=("Consolas", 11),
                        highlightthickness=1, highlightcolor=ACCENT,
                        highlightbackground=BORDER)

    def btn(parent, text, cmd, color=ACCENT, fg="white"):
        return tk.Button(parent, text=text, command=cmd,
                         bg=color, fg=fg, relief="flat",
                         font=("Consolas", 10, "bold"),
                         padx=12, pady=6, cursor="hand2",
                         activebackground=ACCENT2, activeforeground="white")

    lbl(left, "NUEVO TRABAJADOR", color=ACCENT, bold=True).pack(
        anchor="w", padx=8, pady=(10, 2))
    tk.Frame(left, bg=BORDER, height=1).pack(fill="x", pady=4)

    lbl(left, "Nombre completo", color=TEXT_DIM).pack(anchor="w", padx=8, pady=(8, 2))
    var_nombre = tk.StringVar()
    ent_n = entry(left, var_nombre)
    ent_n.pack(padx=8, pady=(0, 8))

    lbl(left, "Sueldo básico ($)", color=TEXT_DIM).pack(anchor="w", padx=8, pady=(0, 2))
    var_sueldo = tk.StringVar()
    entry(left, var_sueldo).pack(padx=8, pady=(0, 10))

    # Tabla de reglas
    tk.Frame(left, bg=BORDER, height=1).pack(fill="x", pady=4)
    lbl(left, "REGLAS DE AUMENTO", size=9, color=ACCENT, bold=True).pack(
        anchor="w", padx=8, pady=(4, 4))
    for rango, pct in [("< $4,000", "15%"), ("$4,000 – $7,000", "10%"), ("> $7,000", "8%")]:
        row = tk.Frame(left, bg=BG_CARD)
        row.pack(fill="x", padx=8, pady=1)
        lbl(row, rango, size=9, color=TEXT_DIM).pack(side="left")
        lbl(row, pct,   size=9, color=WARNING, bold=True).pack(side="right")

    tk.Frame(left, bg=BORDER, height=1).pack(fill="x", pady=6)

    lbl_res = tk.Label(left, text="", bg=BG_CARD, fg=SUCCESS,
                       font=("Consolas", 9), justify="left", wraplength=215)
    lbl_res.pack(padx=8, pady=(0, 10), anchor="w")

    bframe = tk.Frame(left, bg=BG_CARD)
    bframe.pack(padx=8, pady=(0, 8))

    btn(bframe, "  Calcular  ",
        lambda: procesar(var_nombre, var_sueldo, lista, lbl_res, tree)
        ).pack(side="left", padx=(0, 6))

    def limpiar():
        var_nombre.set("")
        var_sueldo.set("")
        lbl_res.config(text="")
        ent_n.focus()

    btn(bframe, "Limpiar", limpiar, color=BG_INPUT, fg=TEXT_DIM).pack(side="left")

    # ── Panel derecho: historial ──
    right = tk.Frame(body, bg=BG_CARD, highlightthickness=1,
                     highlightbackground=BORDER)
    right.pack(side="left", fill="both", expand=True, ipadx=8, ipady=8)

    lbl(right, "HISTORIAL DE TRABAJADORES", color=ACCENT, bold=True).pack(
        anchor="w", padx=12, pady=(10, 4))

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("S.Treeview", background=BG_INPUT, foreground=TEXT,
                    fieldbackground=BG_INPUT, rowheight=26, font=("Consolas", 9))
    style.configure("S.Treeview.Heading", background=ACCENT, foreground="white",
                    font=("Consolas", 9, "bold"), relief="flat")
    style.map("S.Treeview", background=[("selected", ACCENT)],
              foreground=[("selected", "white")])

    cols = ("Nombre", "Base", "%", "Aumento", "Nuevo")
    tf = tk.Frame(right, bg=BG_CARD)
    tf.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    tree = ttk.Treeview(tf, columns=cols, show="headings",
                        style="S.Treeview", height=16)
    for col, w in zip(cols, [145, 90, 50, 90, 105]):
        tree.heading(col, text=col)
        tree.column(col, width=w, anchor="center")

    sb = ttk.Scrollbar(tf, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sb.set)
    tree.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")

    btn(right, "Ver resumen general",
        lambda: resumen(lista), color=ACCENT2).pack(pady=(0, 8))

    ent_n.focus()
