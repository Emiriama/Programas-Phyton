"""
main.py – Menú principal
Lanza cada ejercicio desde su propia carpeta.
"""
import tkinter as tk
from tkinter import messagebox

# Importaciones de cada ejercicio
from ejercicio_01 import sueldos  # Ejercicio 1 listo
# from ejercicio_02 import ...    # Se irán agregando


# ─── Paleta ──────────────────────────────────────────────────
BG_DARK  = "#0f1117"
BG_CARD  = "#1a1d27"
ACCENT   = "#6c63ff"
ACCENT2  = "#ff6584"
TEXT     = "#e8e6f0"
TEXT_DIM = "#8a8aa0"
BORDER   = "#2e3148"

COLORES = [
    "#6c63ff", "#ff6584", "#43e97b", "#f7971e", "#4facfe",
    "#f093fb", "#a8edea", "#ffecd2", "#96fbc4", "#fccb90",
]

EJERCICIOS = [
    {"num": "01", "titulo": "Aumento de\nSueldos",       "icono": "💼", "modulo": sueldos},
    {"num": "02", "titulo": "Próximamente",               "icono": "🔧", "modulo": None},
    {"num": "03", "titulo": "Próximamente",               "icono": "📊", "modulo": None},
    {"num": "04", "titulo": "Próximamente",               "icono": "📐", "modulo": None},
    {"num": "05", "titulo": "Próximamente",               "icono": "🗂️", "modulo": None},
    {"num": "06", "titulo": "Próximamente",               "icono": "📈", "modulo": None},
    {"num": "07", "titulo": "Próximamente",               "icono": "🧮", "modulo": None},
    {"num": "08", "titulo": "Próximamente",               "icono": "📋", "modulo": None},
    {"num": "09", "titulo": "Próximamente",               "icono": "🔢", "modulo": None},
    {"num": "10", "titulo": "Próximamente",               "icono": "🏁", "modulo": None},
]


def abrir_ejercicio(root, modulo, num):
    if modulo is None:
        messagebox.showinfo(
            "Próximamente",
            f"El ejercicio {num} aún no está disponible.\n"
            "Se agregará en la siguiente entrega.",
        )
        return
    modulo.abrir(root)


def main():
    root = tk.Tk()
    root.title("Ejercicios de Programación – Interfaz Gráfica con Tkinter")
    root.configure(bg=BG_DARK)
    root.geometry("700x560")
    root.resizable(False, False)

    # ── Banner ──────────────────────────────────────────────
    banner = tk.Frame(root, bg=ACCENT, height=76)
    banner.pack(fill="x")
    tk.Label(banner, text="⬡  EJERCICIOS DE PROGRAMACIÓN",
             bg=ACCENT, fg="white",
             font=("Consolas", 15, "bold")).pack(pady=(14, 2))
    tk.Label(banner, text="Interfaz Gráfica con Tkinter  ·  Python",
             bg=ACCENT, fg="#d0ccff",
             font=("Consolas", 9)).pack()

    # ── Subtítulo ───────────────────────────────────────────
    tk.Label(root, text="Selecciona un ejercicio para comenzar",
             bg=BG_DARK, fg=TEXT_DIM,
             font=("Consolas", 10)).pack(pady=(14, 6))

    # ── Grid de tarjetas ────────────────────────────────────
    grid = tk.Frame(root, bg=BG_DARK)
    grid.pack(padx=28, pady=4, fill="both", expand=True)

    for idx, ej in enumerate(EJERCICIOS):
        row, col = divmod(idx, 5)
        color = COLORES[idx]
        activo = ej["modulo"] is not None

        card = tk.Frame(grid, bg=BG_CARD, highlightthickness=1,
                        highlightbackground=color if activo else BORDER,
                        cursor="hand2" if activo else "arrow")
        card.grid(row=row, column=col, padx=7, pady=7,
                  ipadx=6, ipady=8, sticky="nsew")
        grid.columnconfigure(col, weight=1)
        grid.rowconfigure(row, weight=1)

        # Número de ejercicio
        tk.Label(card, text=f"#{ej['num']}", bg=BG_CARD,
                 fg=color if activo else BORDER,
                 font=("Consolas", 8, "bold")).pack(pady=(6, 0))

        # Ícono
        tk.Label(card, text=ej["icono"], bg=BG_CARD,
                 font=("Segoe UI Emoji", 20)).pack(pady=2)

        # Título
        tk.Label(card, text=ej["titulo"], bg=BG_CARD,
                 fg=color if activo else TEXT_DIM,
                 font=("Consolas", 8, "bold" if activo else "normal"),
                 justify="center").pack(pady=(0, 6))

        # Botón abrir
        tk.Button(
            card,
            text="Abrir →" if activo else "—",
            command=lambda m=ej["modulo"], n=ej["num"]: abrir_ejercicio(root, m, n),
            bg=color if activo else BG_CARD,
            fg="white" if activo else TEXT_DIM,
            relief="flat",
            font=("Consolas", 8, "bold"),
            padx=8, pady=3,
            cursor="hand2" if activo else "arrow",
            activebackground=ACCENT2,
            activeforeground="white",
        ).pack(pady=(0, 6))

    # ── Footer ──────────────────────────────────────────────
    tk.Label(root,
             text="Programación con Interfaz Gráfica  ·  Tkinter",
             bg=BG_DARK, fg=TEXT_DIM,
             font=("Consolas", 8)).pack(side="bottom", pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
