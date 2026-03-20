import tkinter as tk
from tkinter import ttk, messagebox

BG_DARK  = "#0f1117"
BG_CARD  = "#1a1d27"
BG_INPUT = "#252836"
ACCENT   = "#6c63ff"
ACCENT2  = "#43e97b"
TEXT     = "#e8e6f0"
TEXT_DIM = "#8a8aa0"
SUCCESS  = "#43e97b"
ERROR    = "#ff6584"
WARNING  = "#f7971e"
BORDER   = "#2e3148"


# ─── Funciones ───────────────────────────────────────────────

def agregar_numero(n: int, lista: list) -> int:
    """Agrega n a la lista y retorna la suma acumulada."""
    lista.append(n)
    return sum(lista)


def resumen_final(lista: list) -> dict:
    """Retorna un diccionario con estadísticas finales."""
    return {
        "numeros":   lista[:],
        "cantidad":  len(lista),
        "suma":      sum(lista),
    }


# ─── Lógica de UI ────────────────────────────────────────────

def agregar(var_num, lista, completado, lbl_acum, tree, lbl_res, btn_agregar, ent):
    if completado[0]:
        return

    texto = var_num.get().strip()
    try:
        numero = int(texto)
    except ValueError:
        messagebox.showerror("Dato inválido", "Ingresa un número entero.")
        return

    if numero == 0:
        # Finalizar
        completado[0] = True
        datos = resumen_final(lista)
        lbl_acum.config(text=f"🏁  Proceso finalizado  |  Suma total: {datos['suma']}", fg=SUCCESS)
        lbl_res.config(
            text=(f"  Números ingresados : {datos['numeros']}\n"
                  f"  Cantidad           : {datos['cantidad']}\n"
                  f"  Suma total         : {datos['suma']}"),
            fg=SUCCESS)
        btn_agregar.config(state="disabled")
        ent.config(state="disabled")
        messagebox.showinfo("Proceso terminado",
                            f"Ingresaste {datos['cantidad']} números.\n"
                            f"Suma total: {datos['suma']}")
    else:
        acum = agregar_numero(numero, lista)
        tree.insert("", "end", values=(len(lista), numero, acum))
        lbl_acum.config(text=f"∑  Suma acumulada: {acum}", fg=WARNING)
        var_num.set("")
        ent.focus()


def reiniciar(lista, completado, var_num, lbl_acum, tree, lbl_res, btn_agregar, ent):
    lista.clear()
    completado[0] = False
    var_num.set("")
    lbl_acum.config(text="∑  Suma acumulada: 0", fg=TEXT_DIM)
    lbl_res.config(text="")
    for item in tree.get_children():
        tree.delete(item)
    btn_agregar.config(state="normal")
    ent.config(state="normal")
    ent.focus()


# ─── Construcción de ventana ─────────────────────────────────

def abrir(root):
    win = tk.Toplevel(root)
    win.title("Ejercicio 8 – Suma Acumulativa")
    win.configure(bg=BG_DARK)
    win.geometry("580x580")
    win.resizable(False, False)

    hdr = tk.Frame(win, bg=ACCENT, height=56)
    hdr.pack(fill="x")
    tk.Label(hdr, text="➕  SISTEMA DE SUMA ACUMULATIVA",
             bg=ACCENT, fg="white", font=("Consolas",13,"bold")).pack(pady=10)
    tk.Label(hdr, text="Ingresa números enteros. Escribe 0 para finalizar.",
             bg=ACCENT, fg="#d0ccff", font=("Consolas",9)).pack()

    body = tk.Frame(win, bg=BG_DARK)
    body.pack(fill="both", expand=True, padx=22, pady=14)

    def lbl(p, t, size=10, color=TEXT, bold=False):
        return tk.Label(p, text=t, fg=color, bg=p["bg"],
                        font=("Consolas", size, "bold" if bold else "normal"))

    # ── Entrada ──
    card = tk.Frame(body, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER)
    card.pack(fill="x", pady=(0,12), ipadx=14, ipady=10)

    lbl(card, "Número a ingresar (0 para finalizar):", color=TEXT_DIM).pack(
        anchor="w", padx=14, pady=(8,2))

    var_num = tk.StringVar()
    ent = tk.Entry(card, textvariable=var_num, width=22, bg=BG_INPUT, fg=TEXT,
                   insertbackground=ACCENT, relief="flat", font=("Consolas",13),
                   highlightthickness=1, highlightcolor=ACCENT, highlightbackground=BORDER)
    ent.pack(padx=14, pady=(0,8), anchor="w")

    lbl_acum = tk.Label(card, text="∑  Suma acumulada: 0",
                        fg=TEXT_DIM, bg=BG_CARD, font=("Consolas",11,"bold"))
    lbl_acum.pack(padx=14, pady=(0,8), anchor="w")

    lbl_res = tk.Label(card, text="", fg=SUCCESS, bg=BG_CARD,
                       font=("Consolas",9), justify="left")
    lbl_res.pack(padx=14, pady=(0,6), anchor="w")

    lista = []; completado = [False]

    bf = tk.Frame(card, bg=BG_CARD); bf.pack(padx=14, pady=(0,8), anchor="w")

    btn_agregar = tk.Button(bf, text="  Agregar  ", bg=ACCENT, fg="white", relief="flat",
                            font=("Consolas",10,"bold"), padx=12, pady=5, cursor="hand2",
                            activebackground=ACCENT2, activeforeground="white")
    btn_agregar.pack(side="left", padx=(0,8))

    btn_r = tk.Button(bf, text="Reiniciar", bg=BG_INPUT, fg=TEXT_DIM, relief="flat",
                      font=("Consolas",10,"bold"), padx=12, pady=5, cursor="hand2")
    btn_r.pack(side="left")

    # ── Historial ──
    hist = tk.Frame(body, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER)
    hist.pack(fill="both", expand=True, ipadx=8, ipady=8)

    lbl(hist, "REGISTRO DE NÚMEROS", color=ACCENT, bold=True).pack(
        anchor="w", padx=12, pady=(8,4))

    style = ttk.Style(); style.theme_use("clam")
    style.configure("T8.Treeview", background=BG_INPUT, foreground=TEXT,
                    fieldbackground=BG_INPUT, rowheight=24, font=("Consolas",9))
    style.configure("T8.Treeview.Heading", background=ACCENT, foreground="white",
                    font=("Consolas",9,"bold"), relief="flat")
    style.map("T8.Treeview", background=[("selected",ACCENT)], foreground=[("selected","white")])

    tf = tk.Frame(hist, bg=BG_CARD); tf.pack(fill="both", expand=True, padx=8, pady=(0,8))
    tree = ttk.Treeview(tf, columns=("#","Número","Acumulado"),
                        show="headings", style="T8.Treeview", height=10)
    for col, w in zip(("#","Número","Acumulado"), (60,160,200)):
        tree.heading(col, text=col); tree.column(col, width=w, anchor="center")
    sb = ttk.Scrollbar(tf, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sb.set)
    tree.pack(side="left", fill="both", expand=True); sb.pack(side="right", fill="y")

    btn_agregar.config(command=lambda: agregar(
        var_num, lista, completado, lbl_acum, tree, lbl_res, btn_agregar, ent))
    btn_r.config(command=lambda: reiniciar(
        lista, completado, var_num, lbl_acum, tree, lbl_res, btn_agregar, ent))
    ent.bind("<Return>", lambda e: agregar(
        var_num, lista, completado, lbl_acum, tree, lbl_res, btn_agregar, ent))

    ent.focus()
