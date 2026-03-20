import tkinter as tk
from tkinter import messagebox

BG_DARK  = "#0f1117"
BG_CARD  = "#1a1d27"
BG_INPUT = "#252836"
ACCENT   = "#f7971e"
ACCENT2  = "#43e97b"
TEXT     = "#e8e6f0"
TEXT_DIM = "#8a8aa0"
SUCCESS  = "#43e97b"
ERROR    = "#ff6584"
BORDER   = "#2e3148"


# ─── Función de validación ───────────────────────────────────

def es_menor_que_10(n: int) -> bool:
    return n < 10


# ─── Lógica de UI ────────────────────────────────────────────

def intentar(var_num, intentos, lbl_estado, lbl_res, btn_intentar, ent):
    texto = var_num.get().strip()

    try:
        numero = int(texto)
    except ValueError:
        intentos[0] += 1
        lbl_estado.config(
            text=f"✘  '{texto}' no es un número entero válido.  (Intento #{intentos[0]})",
            fg=ERROR)
        var_num.set("")
        ent.focus()
        return

    intentos[0] += 1

    if es_menor_que_10(numero):
        lbl_estado.config(text=f"✔  ¡Número válido ingresado!", fg=SUCCESS)
        lbl_res.config(
            text=(f"  Número correcto  : {numero}\n"
                  f"  Intentos totales : {intentos[0]}"),
            fg=SUCCESS,
        )
        btn_intentar.config(state="disabled")
        ent.config(state="disabled")
    else:
        lbl_estado.config(
            text=f"✘  {numero} no es menor que 10.  (Intento #{intentos[0]})",
            fg=ERROR)
        var_num.set("")
        ent.focus()


def reiniciar(intentos, var_num, lbl_estado, lbl_res, btn_intentar, ent):
    intentos[0] = 0
    var_num.set("")
    lbl_estado.config(text="Ingresa un número entero menor que 10.", fg=TEXT_DIM)
    lbl_res.config(text="")
    btn_intentar.config(state="normal")
    ent.config(state="normal")
    ent.focus()


# ─── Construcción de ventana ─────────────────────────────────

def abrir(root):
    win = tk.Toplevel(root)
    win.title("Ejercicio 4 – Número menor que 10")
    win.configure(bg=BG_DARK)
    win.geometry("480x400")
    win.resizable(False, False)

    hdr = tk.Frame(win, bg=ACCENT, height=56)
    hdr.pack(fill="x")
    tk.Label(hdr, text="🔢  VALIDACIÓN: NÚMERO MENOR QUE 10",
             bg=ACCENT, fg="white", font=("Consolas",13,"bold")).pack(pady=16)

    card = tk.Frame(win, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER)
    card.pack(padx=40, pady=30, fill="both", expand=True)

    def lbl(p, t, size=10, color=TEXT, bold=False):
        return tk.Label(p, text=t, fg=color, bg=p["bg"],
                        font=("Consolas", size, "bold" if bold else "normal"))

    lbl(card, "Ingresa un número entero:", color=TEXT_DIM).pack(anchor="w", padx=20, pady=(20,4))

    var_num = tk.StringVar()
    ent = tk.Entry(card, textvariable=var_num, width=20, bg=BG_INPUT, fg=TEXT,
                   insertbackground=ACCENT, relief="flat", font=("Consolas",14),
                   highlightthickness=1, highlightcolor=ACCENT, highlightbackground=BORDER,
                   justify="center")
    ent.pack(padx=20, pady=(0,12))

    intentos = [0]

    lbl_estado = tk.Label(card, text="Ingresa un número entero menor que 10.",
                          fg=TEXT_DIM, bg=BG_CARD, font=("Consolas",9), wraplength=380)
    lbl_estado.pack(padx=20, pady=(0,12))

    lbl_res = tk.Label(card, text="", fg=SUCCESS, bg=BG_CARD,
                       font=("Consolas",11,"bold"), justify="left")
    lbl_res.pack(padx=20, pady=(0,16))

    bf = tk.Frame(card, bg=BG_CARD); bf.pack(pady=(0,16))

    btn_intentar = tk.Button(bf, text="  Validar  ",
                             bg=ACCENT, fg="white", relief="flat",
                             font=("Consolas",10,"bold"), padx=12, pady=6, cursor="hand2",
                             activebackground=ACCENT2, activeforeground=BG_DARK)
    btn_intentar.pack(side="left", padx=(0,8))

    btn_reiniciar = tk.Button(bf, text="Reiniciar",
                              bg=BG_INPUT, fg=TEXT_DIM, relief="flat",
                              font=("Consolas",10,"bold"), padx=12, pady=6, cursor="hand2")

    btn_intentar.config(command=lambda: intentar(
        var_num, intentos, lbl_estado, lbl_res, btn_intentar, ent))
    btn_reiniciar.config(command=lambda: reiniciar(
        intentos, var_num, lbl_estado, lbl_res, btn_intentar, ent))
    btn_reiniciar.pack(side="left")

    # Enter también valida
    ent.bind("<Return>", lambda e: intentar(
        var_num, intentos, lbl_estado, lbl_res, btn_intentar, ent))

    ent.focus()
