import tkinter as tk
from tkinter import ttk, messagebox

BG_DARK  = "#0f1117"
BG_CARD  = "#1a1d27"
BG_INPUT = "#252836"
ACCENT   = "#00cec9"
ACCENT2  = "#6c63ff"
TEXT     = "#e8e6f0"
TEXT_DIM = "#8a8aa0"
SUCCESS  = "#43e97b"
WARNING  = "#f7971e"
BORDER   = "#2e3148"

EXTRA_FACTOR      = 1.5   # hora extra = 50% más que hora normal
BONIF_POR_HIJO    = 0.5   # bonificación por cada hijo


# ─── Funciones de cálculo ────────────────────────────────────

def calcular_pago_normal(horas: float, pago_hora: float) -> float:
    return horas * pago_hora


def calcular_pago_extra(horas_extra: float, pago_hora: float) -> float:
    return horas_extra * pago_hora * EXTRA_FACTOR


def calcular_bonificacion(num_hijos: int) -> float:
    return num_hijos * BONIF_POR_HIJO


def calcular_pago_total(horas: float, pago_hora: float,
                        horas_extra: float, num_hijos: int) -> dict:
    """Retorna un diccionario con todos los componentes del pago."""
    pago_normal = calcular_pago_normal(horas, pago_hora)
    pago_extra  = calcular_pago_extra(horas_extra, pago_hora)
    bonif       = calcular_bonificacion(num_hijos)
    total       = pago_normal + pago_extra + bonif
    return {
        "pago_normal": pago_normal,
        "pago_extra":  pago_extra,
        "bonificacion": bonif,
        "total":        total,
    }


# ─── Lógica de UI ────────────────────────────────────────────

def procesar(vars_, lista, lbl_res, tree, lbl_total):
    nombre = vars_["nombre"].get().strip()
    if not nombre:
        messagebox.showwarning("Campo vacío", "Ingresa el nombre del trabajador.")
        return

    campos = {
        "horas":      ("Horas normales",  False),
        "pago_hora":  ("Pago por hora",   True),
        "horas_extra":("Horas extras",    False),
        "hijos":      ("Número de hijos", False),
    }
    valores = {}
    for key, (label, decimal) in campos.items():
        try:
            v = float(vars_[key].get().strip())
            if v < 0:
                raise ValueError
            valores[key] = v
        except ValueError:
            messagebox.showerror("Dato inválido",
                                 f"'{label}' debe ser un número mayor o igual a 0.")
            return

    pagos = calcular_pago_total(
        valores["horas"], valores["pago_hora"],
        valores["horas_extra"], int(valores["hijos"])
    )

    registro = {"nombre": nombre, **valores, **pagos}
    lista.append(registro)

    lbl_res.config(
        text=(f"✔  {nombre}\n"
              f"   Pago normal  ({valores['horas']:.0f}h × S/.{valores['pago_hora']:.2f})  : S/. {pagos['pago_normal']:,.2f}\n"
              f"   Pago extras  ({valores['horas_extra']:.0f}h × ×1.5)               : S/. {pagos['pago_extra']:,.2f}\n"
              f"   Bonif. hijos ({int(valores['hijos'])} × S/.{BONIF_POR_HIJO})               : S/. {pagos['bonificacion']:,.2f}\n"
              f"   ──────────────────────────────────────\n"
              f"   PAGO TOTAL                            : S/. {pagos['total']:,.2f}"),
        fg=SUCCESS,
    )

    tree.insert("", "end", values=(
        nombre,
        f"{valores['horas']:.0f}h",
        f"S/.{valores['pago_hora']:.2f}",
        f"{valores['horas_extra']:.0f}h",
        int(valores["hijos"]),
        f"S/. {pagos['pago_normal']:,.2f}",
        f"S/. {pagos['pago_extra']:,.2f}",
        f"S/. {pagos['bonificacion']:,.2f}",
        f"S/. {pagos['total']:,.2f}",
    ))

    total_pag = sum(t["total"] for t in lista)
    lbl_total.config(text=f"💵  Total pagado a todos los trabajadores:   S/. {total_pag:,.2f}",
                     fg=WARNING)


def limpiar(vars_, lbl_res, ent_nombre):
    for v in vars_.values():
        v.set("")
    lbl_res.config(text="")
    ent_nombre.focus()


# ─── Construcción de ventana ─────────────────────────────────

def abrir(root):
    win = tk.Toplevel(root)
    win.title("Ejercicio 10 – Pago de Trabajadores")
    win.configure(bg=BG_DARK)
    win.geometry("1000x660")
    win.resizable(False, False)

    hdr = tk.Frame(win, bg=ACCENT, height=60)
    hdr.pack(fill="x")
    tk.Label(hdr, text="💵  SISTEMA DE PAGO DE TRABAJADORES",
             bg=ACCENT, fg="white", font=("Consolas",13,"bold")).pack(pady=10)
    tk.Label(hdr,
             text=f"Hora extra = ×{EXTRA_FACTOR}  ·  Bonificación por hijo = S/. {BONIF_POR_HIJO}",
             bg=ACCENT, fg="#d0fffd", font=("Consolas",9)).pack()

    body = tk.Frame(win, bg=BG_DARK)
    body.pack(fill="both", expand=True, padx=18, pady=14)

    # ── Formulario ──
    left = tk.Frame(body, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER)
    left.pack(side="left", fill="y", padx=(0,12), ipadx=14, ipady=10)

    def lbl(p, t, size=10, color=TEXT, bold=False):
        return tk.Label(p, text=t, fg=color, bg=p["bg"],
                        font=("Consolas", size, "bold" if bold else "normal"))

    def ent(p, var, w=24):
        return tk.Entry(p, textvariable=var, width=w, bg=BG_INPUT, fg=TEXT,
                        insertbackground=ACCENT, relief="flat", font=("Consolas",11),
                        highlightthickness=1, highlightcolor=ACCENT, highlightbackground=BORDER)

    def btn(p, t, cmd, color=ACCENT, fg="white", **kw):
        return tk.Button(p, text=t, command=cmd, bg=color, fg=fg, relief="flat",
                         font=("Consolas",10,"bold"), padx=12, pady=6, cursor="hand2",
                         activebackground=ACCENT2, activeforeground="white", **kw)

    lbl(left, "NUEVO TRABAJADOR", color=ACCENT, bold=True).pack(anchor="w", padx=8, pady=(10,2))
    tk.Frame(left, bg=BORDER, height=1).pack(fill="x", pady=4)

    vars_ = {k: tk.StringVar() for k in
             ("nombre","horas","pago_hora","horas_extra","hijos")}

    campos_ui = [
        ("nombre",      "Nombre del trabajador"),
        ("horas",       "Horas normales trabajadas"),
        ("pago_hora",   "Pago por hora normal (S/.)"),
        ("horas_extra", "Horas extras trabajadas"),
        ("hijos",       "Número de hijos"),
    ]

    ent_nombre = None
    for key, label in campos_ui:
        lbl(left, label, color=TEXT_DIM).pack(anchor="w", padx=8, pady=(8,2))
        e = ent(left, vars_[key])
        e.pack(padx=8, pady=(0,4))
        if key == "nombre":
            ent_nombre = e

    # Reglas
    tk.Frame(left, bg=BORDER, height=1).pack(fill="x", pady=6)
    lbl(left, "REGLAS DE PAGO", size=9, color=ACCENT, bold=True).pack(anchor="w", padx=8, pady=(4,4))
    for reg in [
        ("Hora extra", "Hora normal × 1.5"),
        ("Por hijo",   "S/. 0.50 bonif."),
    ]:
        r = tk.Frame(left, bg=BG_CARD); r.pack(fill="x", padx=8, pady=1)
        lbl(r, reg[0], size=9, color=TEXT_DIM).pack(side="left")
        lbl(r, reg[1], size=9, color=WARNING, bold=True).pack(side="right")

    tk.Frame(left, bg=BORDER, height=1).pack(fill="x", pady=6)

    lista = []
    lbl_total = None   # se asigna abajo

    lbl_res = tk.Label(left, text="", bg=BG_CARD, fg=SUCCESS,
                       font=("Consolas",8), justify="left", wraplength=250)
    lbl_res.pack(padx=8, pady=(0,8), anchor="w")

    bf = tk.Frame(left, bg=BG_CARD); bf.pack(padx=8, pady=(0,6))
    btn(bf, "  Calcular  ",
        lambda: procesar(vars_, lista, lbl_res, tree, lbl_total)
        ).pack(side="left", padx=(0,6))
    btn(bf, "Limpiar",
        lambda: limpiar(vars_, lbl_res, ent_nombre),
        color=BG_INPUT, fg=TEXT_DIM).pack(side="left")

    # ── Reporte ──
    right = tk.Frame(body, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER)
    right.pack(side="left", fill="both", expand=True, ipadx=6, ipady=8)

    lbl(right, "REPORTE DE PAGOS", color=ACCENT, bold=True).pack(
        anchor="w", padx=12, pady=(10,4))

    style = ttk.Style(); style.theme_use("clam")
    style.configure("T10.Treeview", background=BG_INPUT, foreground=TEXT,
                    fieldbackground=BG_INPUT, rowheight=26, font=("Consolas",8))
    style.configure("T10.Treeview.Heading", background=ACCENT, foreground="white",
                    font=("Consolas",8,"bold"), relief="flat")
    style.map("T10.Treeview", background=[("selected",ACCENT)],
              foreground=[("selected","white")])

    cols = ("Nombre","H.Norm","$/h","H.Extra","Hijos","P.Normal","P.Extra","Bonif.","Total")
    widths = [130,55,65,60,45,90,80,65,90]

    tf = tk.Frame(right, bg=BG_CARD); tf.pack(fill="both", expand=True, padx=6, pady=(0,8))
    tree = ttk.Treeview(tf, columns=cols, show="headings", style="T10.Treeview", height=16)
    for col, w in zip(cols, widths):
        tree.heading(col, text=col); tree.column(col, width=w, anchor="center")
    sb = ttk.Scrollbar(tf, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sb.set)
    tree.pack(side="left", fill="both", expand=True); sb.pack(side="right", fill="y")

    tk.Frame(right, bg=BORDER, height=1).pack(fill="x", padx=8, pady=4)
    lbl_total = tk.Label(right,
                         text="💵  Total pagado a todos los trabajadores:   S/. 0.00",
                         bg=BG_CARD, fg=TEXT_DIM, font=("Consolas",10,"bold"))
    lbl_total.pack(pady=(4,8))

    ent_nombre.focus()
