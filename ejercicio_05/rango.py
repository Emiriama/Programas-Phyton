import tkinter as tk

BG_DARK  = "#0f1117"
BG_CARD  = "#1a1d27"
BG_INPUT = "#252836"
ACCENT   = "#a29bfe"
ACCENT2  = "#43e97b"
TEXT     = "#e8e6f0"
TEXT_DIM = "#8a8aa0"
SUCCESS  = "#43e97b"
ERROR    = "#ff6584"
WARNING  = "#f7971e"
BORDER   = "#2e3148"

RANGO_MIN = 0
RANGO_MAX = 20


# ─── Función reutilizable de validación ─────────────────────

def validar_rango(n: int, minimo: int = RANGO_MIN, maximo: int = RANGO_MAX) -> bool:
    """Retorna True si n está dentro del rango (minimo, maximo) exclusivo."""
    return minimo < n < maximo


# ─── Lógica de UI ────────────────────────────────────────────

def intentar(var_num, intentos, lbl_estado, lbl_res, btn_val, ent):
    texto = var_num.get().strip()

    try:
        numero = int(texto)
    except ValueError:
        intentos[0] += 1
        lbl_estado.config(
            text=f"✘  '{texto}' no es un número entero válido.  (Intento #{intentos[0]})",
            fg=ERROR)
        var_num.set(""); ent.focus(); return

    intentos[0] += 1

    if validar_rango(numero):
        lbl_estado.config(text="✔  ¡Número dentro del rango!", fg=SUCCESS)
        lbl_res.config(
            text=(f"  Número válido   : {numero}\n"
                  f"  Intentos totales: {intentos[0]}"),
            fg=SUCCESS)
        btn_val.config(state="disabled")
        ent.config(state="disabled")
    else:
        if numero <= RANGO_MIN:
            msg = f"✘  {numero} es demasiado pequeño (debe ser > {RANGO_MIN})."
        else:
            msg = f"✘  {numero} es demasiado grande (debe ser < {RANGO_MAX})."
        lbl_estado.config(text=f"{msg}  (Intento #{intentos[0]})", fg=ERROR)
        var_num.set(""); ent.focus()


def reiniciar(intentos, var_num, lbl_estado, lbl_res, btn_val, ent):
    intentos[0] = 0
    var_num.set("")
    lbl_estado.config(text=f"Ingresa un número en el rango ({RANGO_MIN}, {RANGO_MAX}).", fg=TEXT_DIM)
    lbl_res.config(text="")
    btn_val.config(state="normal")
    ent.config(state="normal")
    ent.focus()


# ─── Construcción de ventana ─────────────────────────────────

def abrir(root):
    win = tk.Toplevel(root)
    win.title("Ejercicio 5 – Rango (0, 20)")
    win.configure(bg=BG_DARK)
    win.geometry("500x430")
    win.resizable(False, False)

    hdr = tk.Frame(win, bg=ACCENT, height=56)
    hdr.pack(fill="x")
    tk.Label(hdr, text="🎯  VALIDACIÓN: RANGO (0, 20)",
             bg=ACCENT, fg="white", font=("Consolas",13,"bold")).pack(pady=10)
    tk.Label(hdr, text="El número debe ser estrictamente mayor que 0 y menor que 20",
             bg=ACCENT, fg="#e8e6ff", font=("Consolas",8)).pack()

    card = tk.Frame(win, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER)
    card.pack(padx=40, pady=24, fill="both", expand=True)

    def lbl(p, t, size=10, color=TEXT, bold=False):
        return tk.Label(p, text=t, fg=color, bg=p["bg"],
                        font=("Consolas", size, "bold" if bold else "normal"))

    # Visualización del rango
    rango_frame = tk.Frame(card, bg=BG_INPUT)
    rango_frame.pack(padx=20, pady=(18,10), fill="x")
    lbl(rango_frame, f"  Rango válido: ({RANGO_MIN}  <  n  <  {RANGO_MAX})  ",
        size=11, color=WARNING, bold=True).pack(pady=6)

    lbl(card, "Ingresa un número entero:", color=TEXT_DIM).pack(anchor="w", padx=20, pady=(4,4))

    var_num = tk.StringVar()
    ent = tk.Entry(card, textvariable=var_num, width=20, bg=BG_INPUT, fg=TEXT,
                   insertbackground=ACCENT, relief="flat", font=("Consolas",14),
                   highlightthickness=1, highlightcolor=ACCENT, highlightbackground=BORDER,
                   justify="center")
    ent.pack(padx=20, pady=(0,12))

    intentos = [0]

    lbl_estado = tk.Label(card, text=f"Ingresa un número en el rango ({RANGO_MIN}, {RANGO_MAX}).",
                          fg=TEXT_DIM, bg=BG_CARD, font=("Consolas",9), wraplength=400)
    lbl_estado.pack(padx=20, pady=(0,10))

    lbl_res = tk.Label(card, text="", fg=SUCCESS, bg=BG_CARD,
                       font=("Consolas",11,"bold"), justify="left")
    lbl_res.pack(padx=20, pady=(0,14))

    bf = tk.Frame(card, bg=BG_CARD); bf.pack(pady=(0,16))

    btn_val = tk.Button(bf, text="  Validar  ", bg=ACCENT, fg="white", relief="flat",
                        font=("Consolas",10,"bold"), padx=12, pady=6, cursor="hand2",
                        activebackground=ACCENT2, activeforeground=BG_DARK)
    btn_val.pack(side="left", padx=(0,8))

    btn_r = tk.Button(bf, text="Reiniciar", bg=BG_INPUT, fg=TEXT_DIM, relief="flat",
                      font=("Consolas",10,"bold"), padx=12, pady=6, cursor="hand2")

    btn_val.config(command=lambda: intentar(var_num, intentos, lbl_estado, lbl_res, btn_val, ent))
    btn_r.config(command=lambda: reiniciar(intentos, var_num, lbl_estado, lbl_res, btn_val, ent))
    btn_r.pack(side="left")

    ent.bind("<Return>", lambda e: intentar(var_num, intentos, lbl_estado, lbl_res, btn_val, ent))
    ent.focus()
