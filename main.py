"""
main.py – Menú principal
Lanza cada ejercicio desde su propia carpeta.
"""
import tkinter as tk
from tkinter import messagebox

from ejercicio_01 import sueldos
from ejercicio_02 import parque
from ejercicio_03 import tienda
from ejercicio_04 import validacion
from ejercicio_05 import rango
from ejercicio_06 import intentos
from ejercicio_07 import suma
from ejercicio_08 import acumulativa
from ejercicio_09 import limite
from ejercicio_10 import trabajadores

BG_DARK  = "#0f1117"
BG_CARD  = "#1a1d27"
ACCENT   = "#6c63ff"
ACCENT2  = "#ff6584"
TEXT     = "#e8e6f0"
TEXT_DIM = "#8a8aa0"
BORDER   = "#2e3148"

EJERCICIOS = [
    {"num": "01", "titulo": "Aumento de\nSueldos",        "icono": "💼", "color": "#6c63ff", "modulo": sueldos},
    {"num": "02", "titulo": "Parque de\nDiversiones",     "icono": "🎡", "color": "#ff6584", "modulo": parque},
    {"num": "03", "titulo": "Descuentos\npor Mes",        "icono": "🏪", "color": "#4facfe", "modulo": tienda},
    {"num": "04", "titulo": "Número\nMenor que 10",       "icono": "🔢", "color": "#f7971e", "modulo": validacion},
    {"num": "05", "titulo": "Número en\nRango (0,20)",    "icono": "🎯", "color": "#a29bfe", "modulo": rango},
    {"num": "06", "titulo": "Registro de\nIntentos",      "icono": "📋", "color": "#fd79a8", "modulo": intentos},
    {"num": "07", "titulo": "Suma de\nn Enteros",         "icono": "🧮", "color": "#00b894", "modulo": suma},
    {"num": "08", "titulo": "Suma\nAcumulativa",          "icono": "➕", "color": "#6c63ff", "modulo": acumulativa},
    {"num": "09", "titulo": "Suma hasta\nsuperar 100",    "icono": "🎯", "color": "#e17055", "modulo": limite},
    {"num": "10", "titulo": "Pago de\nTrabajadores",      "icono": "💵", "color": "#00cec9", "modulo": trabajadores},
]


def main():
    root = tk.Tk()
    root.title("Ejercicios de Programación – Interfaz Gráfica con Tkinter")
    root.configure(bg=BG_DARK)
    root.geometry("720x520")
    root.resizable(False, False)

    banner = tk.Frame(root, bg=ACCENT, height=76)
    banner.pack(fill="x")
    tk.Label(banner, text="⬡  EJERCICIOS DE PROGRAMACIÓN",
             bg=ACCENT, fg="white", font=("Consolas", 15, "bold")).pack(pady=(14, 2))
    tk.Label(banner, text="Interfaz Gráfica con Tkinter  ·  Python",
             bg=ACCENT, fg="#d0ccff", font=("Consolas", 9)).pack()

    tk.Label(root, text="Selecciona un ejercicio para comenzar",
             bg=BG_DARK, fg=TEXT_DIM, font=("Consolas", 10)).pack(pady=(14, 6))

    grid = tk.Frame(root, bg=BG_DARK)
    grid.pack(padx=24, pady=4, fill="both", expand=True)

    for idx, ej in enumerate(EJERCICIOS):
        row, col = divmod(idx, 5)
        color = ej["color"]

        card = tk.Frame(grid, bg=BG_CARD, highlightthickness=1,
                        highlightbackground=color, cursor="hand2")
        card.grid(row=row, column=col, padx=6, pady=6,
                  ipadx=6, ipady=6, sticky="nsew")
        grid.columnconfigure(col, weight=1)
        grid.rowconfigure(row, weight=1)

        tk.Label(card, text=f"#{ej['num']}", bg=BG_CARD,
                 fg=color, font=("Consolas", 8, "bold")).pack(pady=(6, 0))
        tk.Label(card, text=ej["icono"], bg=BG_CARD,
                 font=("Segoe UI Emoji", 20)).pack(pady=2)
        tk.Label(card, text=ej["titulo"], bg=BG_CARD, fg=color,
                 font=("Consolas", 8, "bold"), justify="center").pack(pady=(0, 4))

        tk.Button(
            card, text="Abrir ->",
            command=lambda m=ej["modulo"]: m.abrir(root),
            bg=color, fg="white", relief="flat",
            font=("Consolas", 8, "bold"),
            padx=8, pady=3, cursor="hand2",
            activebackground=ACCENT2, activeforeground="white",
        ).pack(pady=(0, 6))

    tk.Label(root, text="Programacion con Interfaz Grafica  .  Tkinter",
             bg=BG_DARK, fg=TEXT_DIM, font=("Consolas", 8)).pack(side="bottom", pady=8)

    root.mainloop()


if __name__ == "__main__":
    main()
