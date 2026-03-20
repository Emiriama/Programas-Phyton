import tkinter as tk
from tkinter import messagebox

BG_DARK  = "#0f1117"
BG_CARD  = "#1a1d27"
BG_INPUT = "#252836"
ACCENT   = "#00b894"
ACCENT2  = "#6c63ff"
TEXT     = "#e8e6f0"
TEXT_DIM = "#8a8aa0"
SUCCESS  = "#43e97b"
ERROR    = "#ff6584"
BORDER   = "#2e3148"


# ─── Funciones de cálculo ────────────────────────────────────

def calcular_suma(n: int) -> int:
    """Calcula la suma de los primeros n números enteros positivos."""
    total = 0
    for i in range(1, n + 1):
        total += i
    return total


def generar_secuencia(n: int) -> list:
    """Retorna la lista de números del 1 al n."""
    return list(range(1, n + 1))


# ─── Lógica de UI ────────────────────────────────────────────

def calcular(var_n, txt_secuencia, lbl_res):
    texto = var_n.get().strip()

    try:
        n = int(texto)
        if n <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Dato inválido", "Ingresa un número entero positivo (n > 0).")
        return

    secuencia = generar_secuencia(n)
    suma      = calcular_suma(n)

    # Mostrar secuencia en el cuadro de texto
    txt_secuencia.config(state="normal")
    txt_secuencia.delete("1.0", "end")

    # Construir línea de secuencia con suma parcial
    lineas = []
    acum = 0
    for i, num in enumerate(secuencia):
        acum += num
        flecha = " + " if i < len(secuencia) - 1 else " = "
        lineas.append(f"  Paso {i+1:>3}: {num:>5}  →  acumulado = {acum}")
    txt_secuencia.insert("end", "\n".join(lineas))
    txt_secuencia.config(state="disabled")

    # Mostrar resultado
    seq_txt = " + ".join(str(x) for x in secuencia)
    if n <= 15:
        lbl_res.config(
            text=(f"  Secuencia: {seq_txt}\n"
                  f"  ─────────────────────\n"
                  f"  Suma (1 → {n})  =  {suma}"),
            fg=SUCCESS)
    else:
        lbl_res.config(
            text=(f"  Suma (1 + 2 + ... + {n})  =  {suma}\n"
                  f"  (Secuencia completa en el panel de pasos)"),
            fg=SUCCESS)


# ─── Construcción de ventana ─────────────────────────────────

def abrir(root):
    win = tk.Toplevel(root)
    win.title("Ejercicio 7 – Suma de n números")
    win.configure(bg=BG_DARK)
    win.geometry("560x540")
    win.resizable(False, False)

    hdr = tk.Frame(win, bg=ACCENT, height=56)
    hdr.pack(fill="x")
    tk.Label(hdr, text="🧮  SUMA DE LOS PRIMEROS N ENTEROS",
             bg=ACCENT, fg="white", font=("Consolas",13,"bold")).pack(pady=10)
    tk.Label(hdr, text="Calcula 1 + 2 + 3 + ... + n",
             bg=ACCENT, fg="#d0fff5", font=("Consolas",9)).pack()

    body = tk.Frame(win, bg=BG_DARK)
    body.pack(fill="both", expand=True, padx=24, pady=16)

    def lbl(p, t, size=10, color=TEXT, bold=False):
        return tk.Label(p, text=t, fg=color, bg=p["bg"],
                        font=("Consolas", size, "bold" if bold else "normal"))

    # ── Entrada ──
    card = tk.Frame(body, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER)
    card.pack(fill="x", pady=(0,12), ipadx=14, ipady=12)

    lbl(card, "Ingresa el valor de n:", color=TEXT_DIM).pack(anchor="w", padx=14, pady=(8,2))

    var_n = tk.StringVar()
    ent = tk.Entry(card, textvariable=var_n, width=20, bg=BG_INPUT, fg=TEXT,
                   insertbackground=ACCENT, relief="flat", font=("Consolas",14),
                   highlightthickness=1, highlightcolor=ACCENT, highlightbackground=BORDER,
                   justify="center")
    ent.pack(padx=14, pady=(0,10), anchor="w")

    lbl_res = tk.Label(card, text="", fg=SUCCESS, bg=BG_CARD,
                       font=("Consolas",10), justify="left")
    lbl_res.pack(padx=14, pady=(0,8), anchor="w")

    bf = tk.Frame(card, bg=BG_CARD); bf.pack(padx=14, pady=(0,8), anchor="w")

    tk.Button(bf, text="  Calcular  ", bg=ACCENT, fg="white", relief="flat",
              font=("Consolas",10,"bold"), padx=12, pady=6, cursor="hand2",
              activebackground=ACCENT2, activeforeground="white",
              command=lambda: calcular(var_n, txt_sec, lbl_res)
              ).pack(side="left", padx=(0,8))

    def limpiar():
        var_n.set("")
        lbl_res.config(text="")
        txt_sec.config(state="normal")
        txt_sec.delete("1.0","end")
        txt_sec.config(state="disabled")
        ent.focus()

    tk.Button(bf, text="Limpiar", bg=BG_INPUT, fg=TEXT_DIM, relief="flat",
              font=("Consolas",10,"bold"), padx=12, pady=6, cursor="hand2",
              command=limpiar).pack(side="left")

    # ── Secuencia de pasos ──
    sec_frame = tk.Frame(body, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER)
    sec_frame.pack(fill="both", expand=True, ipadx=8, ipady=8)

    lbl(sec_frame, "PASOS DE LA SUMA", color=ACCENT, bold=True).pack(anchor="w", padx=12, pady=(8,4))

    txt_sec = tk.Text(sec_frame, bg=BG_INPUT, fg=TEXT, font=("Consolas",9),
                      relief="flat", state="disabled", wrap="none",
                      highlightthickness=0, insertbackground=ACCENT)
    sb_v = tk.Scrollbar(sec_frame, orient="vertical",   command=txt_sec.yview)
    sb_h = tk.Scrollbar(sec_frame, orient="horizontal", command=txt_sec.xview)
    txt_sec.configure(yscrollcommand=sb_v.set, xscrollcommand=sb_h.set)

    sb_v.pack(side="right", fill="y")
    sb_h.pack(side="bottom", fill="x")
    txt_sec.pack(fill="both", expand=True, padx=8, pady=(0,4))

    ent.bind("<Return>", lambda e: calcular(var_n, txt_sec, lbl_res))
    ent.focus()
