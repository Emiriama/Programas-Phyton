import tkinter as tk
from tkinter import ttk, messagebox

BG_DARK  = "#0f1117"
BG_CARD  = "#1a1d27"
BG_INPUT = "#252836"
ACCENT   = "#4facfe"
ACCENT2  = "#43e97b"
TEXT     = "#e8e6f0"
TEXT_DIM = "#8a8aa0"
SUCCESS  = "#43e97b"
WARNING  = "#f7971e"
BORDER   = "#2e3148"

MESES_VALIDOS = [
    "enero","febrero","marzo","abril","mayo","junio",
    "julio","agosto","septiembre","octubre","noviembre","diciembre"
]

PROMOCIONES = {
    "octubre": 0.15,
    "diciembre": 0.20,
    "julio": 0.10,
}


# ─── Funciones de cálculo ────────────────────────────────────

def validar_mes(mes: str) -> bool:
    return mes.lower().strip() in MESES_VALIDOS


def calcular_descuento(mes: str) -> float:
    return PROMOCIONES.get(mes.lower().strip(), 0.0)


def calcular_total(importe: float, descuento_pct: float) -> tuple:
    monto_dto = importe * descuento_pct
    total     = importe - monto_dto
    return monto_dto, total


# ─── Lógica de UI ────────────────────────────────────────────

def procesar(vars_: dict, lista: list, lbl_res, tree, lbl_total):
    nombre  = vars_["nombre"].get().strip()
    mes     = vars_["mes"].get().strip()
    importe_str = vars_["importe"].get().strip()

    if not nombre:
        messagebox.showwarning("Campo vacío", "Ingresa el nombre del cliente.")
        return
    if not validar_mes(mes):
        messagebox.showerror("Mes inválido",
                             f"'{mes}' no es un mes válido.\n"
                             "Escribe el nombre completo (ej: octubre).")
        return
    try:
        importe = float(importe_str)
        if importe <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Dato inválido", "El importe debe ser un número mayor a 0.")
        return

    mes_n     = mes.lower().strip()
    pct       = calcular_descuento(mes_n)
    dto, total = calcular_total(importe, pct)

    lista.append({"nombre": nombre, "mes": mes_n.capitalize(),
                  "importe": importe, "descuento": pct*100,
                  "monto_dto": dto, "total": total})

    pct_txt = f"{pct*100:.0f}%" if pct > 0 else "Sin promoción"
    lbl_res.config(
        text=(f"✔  {nombre}  |  {mes_n.capitalize()}\n"
              f"   Importe     : S/. {importe:,.2f}\n"
              f"   Descuento ({pct_txt:>12}) : - S/. {dto:,.2f}\n"
              f"   ─────────────────────────────\n"
              f"   TOTAL FINAL  : S/. {total:,.2f}"),
        fg=SUCCESS,
    )

    tree.insert("", "end", values=(
        nombre, mes_n.capitalize(),
        f"S/. {importe:,.2f}",
        f"{pct*100:.0f}%",
        f"S/. {dto:,.2f}",
        f"S/. {total:,.2f}",
    ))

    total_dia = sum(v["total"] for v in lista)
    lbl_total.config(text=f"🏪  Total vendido en el día:   S/. {total_dia:,.2f}", fg=ACCENT2)


def limpiar(vars_, lbl_res, ent_nombre):
    for v in vars_.values():
        v.set("")
    lbl_res.config(text="")
    ent_nombre.focus()


# ─── Construcción de ventana ─────────────────────────────────

def abrir(root):
    win = tk.Toplevel(root)
    win.title("Ejercicio 3 – Descuentos por Mes")
    win.configure(bg=BG_DARK)
    win.geometry("860x620")
    win.resizable(False, False)

    hdr = tk.Frame(win, bg=ACCENT, height=56)
    hdr.pack(fill="x")
    tk.Label(hdr, text="🏪  SISTEMA DE DESCUENTOS POR MES",
             bg=ACCENT, fg="white", font=("Consolas", 13, "bold")).pack(pady=10)
    tk.Label(hdr, text="Promociones: Julio 10% · Octubre 15% · Diciembre 20%",
             bg=ACCENT, fg="#dff4ff", font=("Consolas", 9)).pack()

    body = tk.Frame(win, bg=BG_DARK)
    body.pack(fill="both", expand=True, padx=20, pady=14)

    # ── Formulario ──
    left = tk.Frame(body, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER)
    left.pack(side="left", fill="y", padx=(0,12), ipadx=14, ipady=10)

    def lbl(p, t, size=10, color=TEXT, bold=False):
        return tk.Label(p, text=t, fg=color, bg=p["bg"],
                        font=("Consolas", size, "bold" if bold else "normal"))

    def ent(p, var, w=26):
        return tk.Entry(p, textvariable=var, width=w, bg=BG_INPUT, fg=TEXT,
                        insertbackground=ACCENT, relief="flat", font=("Consolas",11),
                        highlightthickness=1, highlightcolor=ACCENT, highlightbackground=BORDER)

    def btn(p, t, cmd, color=ACCENT, fg="white", **kw):
        return tk.Button(p, text=t, command=cmd, bg=color, fg=fg, relief="flat",
                         font=("Consolas",10,"bold"), padx=12, pady=6, cursor="hand2",
                         activebackground=ACCENT2, activeforeground=BG_DARK, **kw)

    lbl(left, "NUEVA COMPRA", color=ACCENT, bold=True).pack(anchor="w", padx=8, pady=(10,2))
    tk.Frame(left, bg=BORDER, height=1).pack(fill="x", pady=4)

    vars_ = {k: tk.StringVar() for k in ("nombre","mes","importe")}

    lbl(left, "Nombre del cliente", color=TEXT_DIM).pack(anchor="w", padx=8, pady=(8,2))
    ent_n = ent(left, vars_["nombre"])
    ent_n.pack(padx=8, pady=(0,8))

    lbl(left, "Mes de la compra", color=TEXT_DIM).pack(anchor="w", padx=8, pady=(0,2))
    ent(left, vars_["mes"]).pack(padx=8, pady=(0,8))

    lbl(left, "Importe de compra (S/.)", color=TEXT_DIM).pack(anchor="w", padx=8, pady=(0,2))
    ent(left, vars_["importe"]).pack(padx=8, pady=(0,10))

    tk.Frame(left, bg=BORDER, height=1).pack(fill="x", pady=4)
    lbl(left, "PROMOCIONES", size=9, color=ACCENT, bold=True).pack(anchor="w", padx=8, pady=(4,4))
    for mes, pct in [("Julio","10%"),("Octubre","15%"),("Diciembre","20%"),("Otros meses","0%")]:
        r = tk.Frame(left, bg=BG_CARD); r.pack(fill="x", padx=8, pady=1)
        lbl(r, mes, size=9, color=TEXT_DIM).pack(side="left")
        lbl(r, pct, size=9, color=WARNING, bold=True).pack(side="right")

    tk.Frame(left, bg=BORDER, height=1).pack(fill="x", pady=6)

    lbl_res = tk.Label(left, text="", bg=BG_CARD, fg=SUCCESS,
                       font=("Consolas",9), justify="left", wraplength=240)
    lbl_res.pack(padx=8, pady=(0,8), anchor="w")

    lista = []
    lbl_total = None

    bf = tk.Frame(left, bg=BG_CARD); bf.pack(padx=8, pady=(0,4))
    btn(bf, "  Registrar  ",
        lambda: procesar(vars_, lista, lbl_res, tree, lbl_total)).pack(side="left", padx=(0,6))
    btn(bf, "Limpiar", lambda: limpiar(vars_, lbl_res, ent_n),
        color=BG_INPUT, fg=TEXT_DIM).pack(side="left")

    # ── Historial ──
    right = tk.Frame(body, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER)
    right.pack(side="left", fill="both", expand=True, ipadx=8, ipady=8)

    lbl(right, "HISTORIAL DE COMPRAS", color=ACCENT, bold=True).pack(anchor="w", padx=12, pady=(10,4))

    style = ttk.Style(); style.theme_use("clam")
    style.configure("T3.Treeview", background=BG_INPUT, foreground=TEXT,
                    fieldbackground=BG_INPUT, rowheight=26, font=("Consolas",9))
    style.configure("T3.Treeview.Heading", background=ACCENT, foreground="white",
                    font=("Consolas",9,"bold"), relief="flat")
    style.map("T3.Treeview", background=[("selected",ACCENT)], foreground=[("selected","white")])

    cols = ("Cliente","Mes","Importe","Dto.","Ahorro","Total")
    widths = [130,90,90,50,80,90]
    tf = tk.Frame(right, bg=BG_CARD); tf.pack(fill="both", expand=True, padx=8, pady=(0,8))
    tree = ttk.Treeview(tf, columns=cols, show="headings", style="T3.Treeview", height=14)
    for col,w in zip(cols,widths):
        tree.heading(col,text=col); tree.column(col,width=w,anchor="center")
    sb = ttk.Scrollbar(tf, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sb.set)
    tree.pack(side="left", fill="both", expand=True); sb.pack(side="right", fill="y")

    tk.Frame(right, bg=BORDER, height=1).pack(fill="x", padx=8, pady=4)
    lbl_total = tk.Label(right, text="🏪  Total vendido en el día:   S/. 0.00",
                         bg=BG_CARD, fg=TEXT_DIM, font=("Consolas",10,"bold"))
    lbl_total.pack(pady=(4,8))

    ent_n.focus()
