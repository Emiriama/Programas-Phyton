import tkinter as tk
from tkinter import ttk, messagebox

BG_DARK  = "#0f1117"
BG_CARD  = "#1a1d27"
BG_INPUT = "#252836"
ACCENT   = "#e17055"
ACCENT2  = "#43e97b"
TEXT     = "#e8e6f0"
TEXT_DIM = "#8a8aa0"
SUCCESS  = "#43e97b"
ERROR    = "#ff6584"
WARNING  = "#f7971e"
BORDER   = "#2e3148"

LIMITE = 100


# ─── Funciones ───────────────────────────────────────────────

def suma_supera_limite(acumulado: int, limite: int = LIMITE) -> bool:
    return acumulado > limite


def agregar_y_verificar(n: int, lista: list) -> tuple:
    """Agrega n a la lista, retorna (nueva_suma, superado)."""
    lista.append(n)
    total = sum(lista)
    return total, suma_supera_limite(total)


# ─── Lógica de UI ────────────────────────────────────────────

def agregar(var_num, lista, completado, lbl_acum, lbl_barra, tree, lbl_res, btn_ag, ent):
    if completado[0]:
        return

    texto = var_num.get().strip()
    try:
        numero = int(texto)
    except ValueError:
        messagebox.showerror("Dato inválido", "Ingresa un número entero.")
        return

    total, superado = agregar_y_verificar(numero, lista)

    # Barra de progreso
    pct = min(total / LIMITE * 100, 100)
    lbl_barra.config(text=f"Progreso: {total} / {LIMITE}  ({pct:.0f}%)")

    tree.insert("", "end", values=(len(lista), numero, total,
                                   "🔴 ¡Superado!" if superado else "🟡 Continúa"))

    if superado:
        completado[0] = True
        lbl_acum.config(text=f"🚨  ¡Límite superado!  Suma = {total}", fg=ERROR)
        lbl_res.config(
            text=(f"  Números ingresados : {lista}\n"
                  f"  Cantidad           : {len(lista)}\n"
                  f"  Suma final         : {total}  (> {LIMITE})"),
            fg=SUCCESS)
        btn_ag.config(state="disabled")
        ent.config(state="disabled")
        messagebox.showinfo("¡Límite alcanzado!",
                            f"La suma ({total}) superó el límite de {LIMITE}.\n"
                            f"Números ingresados: {len(lista)}")
    else:
        lbl_acum.config(text=f"∑  Suma parcial: {total}  |  Faltan: {LIMITE - total + 1}",
                        fg=WARNING)
        var_num.set("")
        ent.focus()


def reiniciar(lista, completado, var_num, lbl_acum, lbl_barra, tree, lbl_res, btn_ag, ent):
    lista.clear()
    completado[0] = False
    var_num.set("")
    lbl_acum.config(text=f"∑  Suma parcial: 0  |  Faltan: {LIMITE + 1}", fg=TEXT_DIM)
    lbl_barra.config(text=f"Progreso: 0 / {LIMITE}  (0%)")
    lbl_res.config(text="")
    for item in tree.get_children():
        tree.delete(item)
    btn_ag.config(state="normal")
    ent.config(state="normal")
    ent.focus()


# ─── Construcción de ventana ─────────────────────────────────

def abrir(root):
    win = tk.Toplevel(root)
    win.title("Ejercicio 9 – Suma hasta superar 100")
    win.configure(bg=BG_DARK)
    win.geometry("600x600")
    win.resizable(False, False)

    hdr = tk.Frame(win, bg=ACCENT, height=56)
    hdr.pack(fill="x")
    tk.Label(hdr, text="🎯  SUMA HASTA SUPERAR EL LÍMITE",
             bg=ACCENT, fg="white", font=("Consolas",13,"bold")).pack(pady=10)
    tk.Label(hdr, text=f"El proceso se detiene cuando la suma supere {LIMITE}",
             bg=ACCENT, fg="#ffe5de", font=("Consolas",9)).pack()

    body = tk.Frame(win, bg=BG_DARK)
    body.pack(fill="both", expand=True, padx=22, pady=14)

    def lbl(p, t, size=10, color=TEXT, bold=False):
        return tk.Label(p, text=t, fg=color, bg=p["bg"],
                        font=("Consolas", size, "bold" if bold else "normal"))

    # ── Entrada ──
    card = tk.Frame(body, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER)
    card.pack(fill="x", pady=(0,12), ipadx=14, ipady=10)

    lbl(card, f"Ingresa un número entero (se detiene cuando suma > {LIMITE}):",
        color=TEXT_DIM).pack(anchor="w", padx=14, pady=(8,2))

    var_num = tk.StringVar()
    ent = tk.Entry(card, textvariable=var_num, width=22, bg=BG_INPUT, fg=TEXT,
                   insertbackground=ACCENT, relief="flat", font=("Consolas",13),
                   highlightthickness=1, highlightcolor=ACCENT, highlightbackground=BORDER)
    ent.pack(padx=14, pady=(0,8), anchor="w")

    lbl_acum = tk.Label(card, text=f"∑  Suma parcial: 0  |  Faltan: {LIMITE + 1}",
                        fg=TEXT_DIM, bg=BG_CARD, font=("Consolas",11,"bold"))
    lbl_acum.pack(padx=14, pady=(0,4), anchor="w")

    lbl_barra = tk.Label(card, text=f"Progreso: 0 / {LIMITE}  (0%)",
                         fg=TEXT_DIM, bg=BG_CARD, font=("Consolas",9))
    lbl_barra.pack(padx=14, pady=(0,6), anchor="w")

    lbl_res = tk.Label(card, text="", fg=SUCCESS, bg=BG_CARD,
                       font=("Consolas",9), justify="left")
    lbl_res.pack(padx=14, pady=(0,6), anchor="w")

    lista = []; completado = [False]

    bf = tk.Frame(card, bg=BG_CARD); bf.pack(padx=14, pady=(0,8), anchor="w")

    btn_ag = tk.Button(bf, text="  Agregar  ", bg=ACCENT, fg="white", relief="flat",
                       font=("Consolas",10,"bold"), padx=12, pady=5, cursor="hand2",
                       activebackground=ACCENT2, activeforeground="white")
    btn_ag.pack(side="left", padx=(0,8))

    btn_r = tk.Button(bf, text="Reiniciar", bg=BG_INPUT, fg=TEXT_DIM, relief="flat",
                      font=("Consolas",10,"bold"), padx=12, pady=5, cursor="hand2")
    btn_r.pack(side="left")

    # ── Historial ──
    hist = tk.Frame(body, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER)
    hist.pack(fill="both", expand=True, ipadx=8, ipady=8)

    lbl(hist, "REGISTRO DE NÚMEROS", color=ACCENT, bold=True).pack(
        anchor="w", padx=12, pady=(8,4))

    style = ttk.Style(); style.theme_use("clam")
    style.configure("T9.Treeview", background=BG_INPUT, foreground=TEXT,
                    fieldbackground=BG_INPUT, rowheight=24, font=("Consolas",9))
    style.configure("T9.Treeview.Heading", background=ACCENT, foreground="white",
                    font=("Consolas",9,"bold"), relief="flat")
    style.map("T9.Treeview", background=[("selected",ACCENT)], foreground=[("selected","white")])

    tf = tk.Frame(hist, bg=BG_CARD); tf.pack(fill="both", expand=True, padx=8, pady=(0,8))
    tree = ttk.Treeview(tf, columns=("#","Número","Suma parcial","Estado"),
                        show="headings", style="T9.Treeview", height=10)
    for col, w in zip(("#","Número","Suma parcial","Estado"), (50,120,140,160)):
        tree.heading(col, text=col); tree.column(col, width=w, anchor="center")
    sb = ttk.Scrollbar(tf, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sb.set)
    tree.pack(side="left", fill="both", expand=True); sb.pack(side="right", fill="y")

    btn_ag.config(command=lambda: agregar(
        var_num, lista, completado, lbl_acum, lbl_barra, tree, lbl_res, btn_ag, ent))
    btn_r.config(command=lambda: reiniciar(
        lista, completado, var_num, lbl_acum, lbl_barra, tree, lbl_res, btn_ag, ent))
    ent.bind("<Return>", lambda e: agregar(
        var_num, lista, completado, lbl_acum, lbl_barra, tree, lbl_res, btn_ag, ent))

    ent.focus()
