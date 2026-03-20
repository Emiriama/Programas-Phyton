import tkinter as tk
from tkinter import ttk

BG_DARK  = "#0f1117"
BG_CARD  = "#1a1d27"
BG_INPUT = "#252836"
ACCENT   = "#fd79a8"
ACCENT2  = "#43e97b"
TEXT     = "#e8e6f0"
TEXT_DIM = "#8a8aa0"
SUCCESS  = "#43e97b"
ERROR    = "#ff6584"
WARNING  = "#f7971e"
BORDER   = "#2e3148"

RANGO_MIN = 0
RANGO_MAX = 20


# ─── Funciones ───────────────────────────────────────────────

def validar_rango(n: int) -> bool:
    return RANGO_MIN < n < RANGO_MAX


def clasificar_intento(n: int) -> str:
    if not validar_rango(n):
        return "❌ Incorrecto"
    return "✅ Correcto"


# ─── Lógica de UI ────────────────────────────────────────────

def intentar(var_num, intentos_lista, completado, lbl_estado, lbl_res, tree, btn_val, ent):
    if completado[0]:
        return

    texto = var_num.get().strip()
    try:
        numero = int(texto)
    except ValueError:
        registro = {"numero": texto, "resultado": "❌ No es entero"}
        intentos_lista.append(registro)
        tree.insert("", "end", values=(len(intentos_lista), texto, "❌ No es entero"),
                    tags=("error",))
        lbl_estado.config(text=f"✘  '{texto}' no es un número entero.  "
                               f"(Intento #{len(intentos_lista)})", fg=ERROR)
        var_num.set(""); ent.focus(); return

    resultado = clasificar_intento(numero)
    registro  = {"numero": numero, "resultado": resultado}
    intentos_lista.append(registro)
    tree.insert("", "end",
                values=(len(intentos_lista), numero, resultado),
                tags=("ok" if validar_rango(numero) else "error",))

    incorrectos = sum(1 for r in intentos_lista if "Incorrecto" in r["resultado"] or "entero" in r["resultado"])

    if validar_rango(numero):
        completado[0] = True
        lbl_estado.config(text="✔  ¡Número válido encontrado!", fg=SUCCESS)
        lbl_res.config(
            text=(f"  Número correcto   : {numero}\n"
                  f"  Intentos totales  : {len(intentos_lista)}\n"
                  f"  Intentos incorrectos: {incorrectos}"),
            fg=SUCCESS)
        btn_val.config(state="disabled")
        ent.config(state="disabled")
    else:
        if numero <= RANGO_MIN:
            msg = f"✘  {numero} ≤ {RANGO_MIN}: fuera de rango."
        else:
            msg = f"✘  {numero} ≥ {RANGO_MAX}: fuera de rango."
        lbl_estado.config(text=f"{msg}  (Intento #{len(intentos_lista)})", fg=ERROR)
        var_num.set(""); ent.focus()


def reiniciar(intentos_lista, completado, var_num, lbl_estado, lbl_res, tree, btn_val, ent):
    intentos_lista.clear()
    completado[0] = False
    var_num.set("")
    lbl_estado.config(text=f"Ingresa números en el rango ({RANGO_MIN}, {RANGO_MAX}).", fg=TEXT_DIM)
    lbl_res.config(text="")
    for item in tree.get_children():
        tree.delete(item)
    btn_val.config(state="normal")
    ent.config(state="normal")
    ent.focus()


# ─── Construcción de ventana ─────────────────────────────────

def abrir(root):
    win = tk.Toplevel(root)
    win.title("Ejercicio 6 – Registro de Intentos")
    win.configure(bg=BG_DARK)
    win.geometry("620x560")
    win.resizable(False, False)

    hdr = tk.Frame(win, bg=ACCENT, height=56)
    hdr.pack(fill="x")
    tk.Label(hdr, text="📋  REGISTRO DE INTENTOS DE VALIDACIÓN",
             bg=ACCENT, fg="white", font=("Consolas",13,"bold")).pack(pady=10)
    tk.Label(hdr, text=f"Rango válido: ({RANGO_MIN} < n < {RANGO_MAX})",
             bg=ACCENT, fg="#ffe8f0", font=("Consolas",9)).pack()

    body = tk.Frame(win, bg=BG_DARK)
    body.pack(fill="both", expand=True, padx=24, pady=16)

    # ── Entrada ──
    card = tk.Frame(body, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER)
    card.pack(fill="x", pady=(0,12), ipadx=12, ipady=10)

    def lbl(p, t, size=10, color=TEXT, bold=False):
        return tk.Label(p, text=t, fg=color, bg=p["bg"],
                        font=("Consolas", size, "bold" if bold else "normal"))

    lbl(card, "Ingresa un número:", color=TEXT_DIM).pack(anchor="w", padx=12, pady=(6,2))

    var_num = tk.StringVar()
    ent = tk.Entry(card, textvariable=var_num, width=24, bg=BG_INPUT, fg=TEXT,
                   insertbackground=ACCENT, relief="flat", font=("Consolas",12),
                   highlightthickness=1, highlightcolor=ACCENT, highlightbackground=BORDER)
    ent.pack(padx=12, pady=(0,8), anchor="w")

    intentos_lista = []
    completado     = [False]

    lbl_estado = tk.Label(card, text=f"Ingresa números en el rango ({RANGO_MIN}, {RANGO_MAX}).",
                          fg=TEXT_DIM, bg=BG_CARD, font=("Consolas",9), wraplength=540)
    lbl_estado.pack(padx=12, pady=(0,6), anchor="w")

    lbl_res = tk.Label(card, text="", fg=SUCCESS, bg=BG_CARD,
                       font=("Consolas",10,"bold"), justify="left")
    lbl_res.pack(padx=12, pady=(0,8), anchor="w")

    bf = tk.Frame(card, bg=BG_CARD); bf.pack(padx=12, pady=(0,6), anchor="w")

    btn_val = tk.Button(bf, text="  Validar  ", bg=ACCENT, fg="white", relief="flat",
                        font=("Consolas",10,"bold"), padx=12, pady=5, cursor="hand2",
                        activebackground=ACCENT2, activeforeground=BG_DARK)
    btn_val.pack(side="left", padx=(0,8))

    btn_r = tk.Button(bf, text="Reiniciar", bg=BG_INPUT, fg=TEXT_DIM, relief="flat",
                      font=("Consolas",10,"bold"), padx=12, pady=5, cursor="hand2")
    btn_r.pack(side="left")

    # ── Historial de intentos ──
    hist = tk.Frame(body, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER)
    hist.pack(fill="both", expand=True, ipadx=8, ipady=8)

    lbl(hist, "HISTORIAL DE INTENTOS", color=ACCENT, bold=True).pack(anchor="w", padx=12, pady=(8,4))

    style = ttk.Style(); style.theme_use("clam")
    style.configure("T6.Treeview", background=BG_INPUT, foreground=TEXT,
                    fieldbackground=BG_INPUT, rowheight=24, font=("Consolas",9))
    style.configure("T6.Treeview.Heading", background=ACCENT, foreground="white",
                    font=("Consolas",9,"bold"), relief="flat")
    style.map("T6.Treeview", background=[("selected",ACCENT)], foreground=[("selected","white")])

    tf = tk.Frame(hist, bg=BG_CARD); tf.pack(fill="both", expand=True, padx=8, pady=(0,8))
    tree = ttk.Treeview(tf, columns=("Intento","Número","Resultado"),
                        show="headings", style="T6.Treeview", height=8)
    for col, w in zip(("Intento","Número","Resultado"), (70,120,250)):
        tree.heading(col, text=col); tree.column(col, width=w, anchor="center")
    tree.tag_configure("ok",    foreground=SUCCESS)
    tree.tag_configure("error", foreground=ERROR)

    sb = ttk.Scrollbar(tf, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sb.set)
    tree.pack(side="left", fill="both", expand=True); sb.pack(side="right", fill="y")

    # Conectar botones
    btn_val.config(command=lambda: intentar(
        var_num, intentos_lista, completado, lbl_estado, lbl_res, tree, btn_val, ent))
    btn_r.config(command=lambda: reiniciar(
        intentos_lista, completado, var_num, lbl_estado, lbl_res, tree, btn_val, ent))
    ent.bind("<Return>", lambda e: intentar(
        var_num, intentos_lista, completado, lbl_estado, lbl_res, tree, btn_val, ent))

    ent.focus()
