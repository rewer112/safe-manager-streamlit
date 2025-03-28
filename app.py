import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel, messagebox

#############################
# Diccionarios de idiomas
#############################
LANG_ES = {
    "title": "Safe Manager - Nivel Óptimo",
    "header": "CONTROL DE SAFE Y CAMBIO",
    "label_cajas": "Cajas con $200 cada una:",
    "button_calcular": "¿Cuánto cambio debo ordenar?",
    "button_toggle": "EN/ES",
    "label_optimal_table": "📋 Nivel Óptimo del Safe",
    "label_signature": "By Juan Morillo",
    "ask_iou_msg": "El total es menor a $2300. ¿El resto está en IOU?",
    "ask_iou_title": "¿IOU?",
    "ask_iou_confirm": "Registrado como IOU por ${} para alcanzar los $2300.",
    "order_change_title": "Orden de cambio sugerida",
    "order_change_header": "💵 DEBES HACER UNA ORDEN DE CAMBIO",

    # Nuevos para la tabla y reportes
    "table_headers": ["Denominación", "Cantidad ($)", "Nivel Óptimo"],
    "packs_title": "📦 Total de paquetes actuales:\n",
    "report_small_change": "⚠️ Cambio insuficiente. Debes tener al menos $1200 en billetes pequeños y monedas.",
    "report_incomplete_boxes": "🔔 Solo {} de 4 cajas están completas. Verifica que todas tengan $200.",

    # Versión española de la tabla de nivel óptimo
    "optimal_table": [
        ("💵 $1",  "$25",   "≥ 14 paquetes → $350"),
        ("💵 $5",  "$100",  "≥ 8 paquetes → $800"),
        ("🪙 ¢25", "$10",   "≥ 20 paquetes → $200"),
        ("🪙 ¢10", "$5",    "≥ 20 paquetes → $100"),
        ("🪙 ¢5",  "$2",    "≥ 10 paquetes → $20 (máx 10)"),
        ("🪙 ¢1",  "$0.50", "≥ 60 paquetes → $30 (máx 60)")
    ]
}

LANG_EN = {
    "title": "Safe Manager - Optimal Level",
    "header": "SAFE AND CHANGE CONTROL",
    "label_cajas": "Registers with $200 each:",
    "button_calcular": "How much change should I order?",
    "button_toggle": "ES/EN",
    "label_optimal_table": "📋 Optimal Safe Level",
    "label_signature": "By Juan Morillo",
    "ask_iou_msg": "Total is below $2300. Is the remainder on IOU?",
    "ask_iou_title": "IOU?",
    "ask_iou_confirm": "Recorded IOU of ${} to reach $2300.",
    "order_change_title": "Suggested Change Order",
    "order_change_header": "💵 YOU MUST MAKE A CHANGE ORDER",

    # Nuevos para la tabla y reportes
    "table_headers": ["Denomination", "Amount ($)", "Optimal Level"],
    "packs_title": "📦 Current total packs:\n",
    "report_small_change": "⚠️ Insufficient change. You must have at least $1200 in small bills and coins.",
    "report_incomplete_boxes": "🔔 Only {} of 4 registers are complete. Make sure each has $200.",

    # Versión inglesa de la tabla de nivel óptimo
    "optimal_table": [
        ("💵 $1",  "$25",   "≥ 14 packs → $350"),
        ("💵 $5",  "$100",  "≥ 8 packs → $800"),
        ("🪙 ¢25", "$10",   "≥ 20 packs → $200"),
        ("🪙 ¢10", "$5",    "≥ 20 packs → $100"),
        ("🪙 ¢5",  "$2",    "≥ 10 packs → $20 (max 10)"),
        ("🪙 ¢1",  "$0.50", "≥ 60 packs → $30 (max 60)")
    ]
}

# Ajustes para $1500 exactos
OPTIMAL = {
    "$1":  {"pack_size": 25,  "target_packs": 14},    # 14×$25 = $350
    "$5":  {"pack_size": 100, "target_packs": 8},     # 8×$100 = $800
    "¢25": {"pack_size": 10,  "target_packs": 20},    # 20×$10 = $200
    "¢10": {"pack_size": 5,   "target_packs": 20},    # 20×$5  = $100
    "¢5":  {"pack_size": 2,   "target_packs": 10, "max_packs": 10},  # $20
    "¢1":  {"pack_size": 0.5, "target_packs": 60, "max_packs": 60}   # $30
}

VALUES = {
    "$1": 100,
    "$5": 500,
    "$10": 1000,
    "$20": 2000,
    "$50": 5000,
    "$100": 10000,
    "¢25": 100,
    "¢10": 100,
    "¢5": 100,
    "¢1": 100
}


class SafeManagerGUI:
    def __init__(self, root):
        self.root = root
        self.current_lang = LANG_ES

        self.root.title(self.current_lang["title"])
        self.root.configure(bg="#fefefe")

        self.entries = {}
        self.cajas_check = []

        # Encabezado
        frame_title = tk.Frame(root, bg="#ffc107", pady=10)
        frame_title.grid(row=0, column=0, columnspan=4, sticky="ew")
        self.label_header = tk.Label(
            frame_title,
            text=self.current_lang["header"],
            font=("Helvetica", 18, "bold"),
            bg="#ffc107",
            fg="#212121"
        )
        self.label_header.pack()

        # Botón de idioma
        self.btn_toggle_lang = tk.Button(
            root,
            text=self.current_lang["button_toggle"],
            command=self.toggle_language,
            bg="#e0e0e0",
            fg="#000",
            font=("Arial", 10, "bold"),
            height=1,
            width=6
        )
        self.btn_toggle_lang.grid(row=0, column=3, sticky="e", padx=10)

        # Sección de cajas y tabla
        self.create_checkbox_section(row=1)
        self.create_table_section(start_row=6)

        # Botón Calcular
        self.btn_calcular = tk.Button(
            root,
            text=self.current_lang["button_calcular"],
            command=self.check_recommendations,
            bg="#d32f2f",
            fg="white",
            font=("Arial", 11, "bold"),
            height=2,
            width=30
        )
        self.btn_calcular.grid(row=30, column=0, columnspan=4, pady=20)

        # Label resultados
        self.result_label = tk.Label(
            root, text="", justify="left", anchor="w",
            bg="#fefefe", fg="#212121", font=("Arial", 10)
        )
        self.result_label.grid(row=31, column=0, columnspan=4, sticky="w", padx=10)

        # En vez de show_optimal_table, llamamos redraw_optimal_table
        self.frame_opt = tk.LabelFrame(
            self.root,
            text=self.current_lang["label_optimal_table"],
            font=("Arial", 12, "bold"),
            bg="#fff9db",
            fg="#333"
        )
        self.frame_opt.grid(row=32, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        # Renderizamos la tabla óptima
        self.redraw_optimal_table()

        # Firma
        self.label_signature = tk.Label(
            root,
            text=self.current_lang["label_signature"],
            font=("Arial", 9, "italic"),
            fg="#777",
            bg="#fefefe"
        )
        self.label_signature.grid(row=999, column=3, sticky="e", padx=10, pady=5)

    def toggle_language(self):
        if self.current_lang == LANG_ES:
            self.current_lang = LANG_EN
        else:
            self.current_lang = LANG_ES
        self.set_language()

    def set_language(self):
        # Actualiza títulos
        self.root.title(self.current_lang["title"])
        self.label_header.config(text=self.current_lang["header"])
        self.btn_toggle_lang.config(text=self.current_lang["button_toggle"])
        self.btn_calcular.config(text=self.current_lang["button_calcular"])
        self.frame_cajas.config(text=self.current_lang["label_cajas"])
        self.frame_opt.config(text=self.current_lang["label_optimal_table"])
        self.label_signature.config(text=self.current_lang["label_signature"])

        # Redibuja encabezados de la tabla principal
        self.redraw_table_headers()

        # Redibuja la tabla de nivel óptimo
        self.frame_opt.config(text=self.current_lang["label_optimal_table"])
        self.redraw_optimal_table()

    def redraw_table_headers(self):
        """Redibuja los encabezados de la tabla principal según el idioma actual."""
        headers = self.current_lang["table_headers"]
        start_row = 6
        for col, text in enumerate(headers):
            tk.Label(
                self.root,
                text=text,
                font=("Arial", 10, "bold"),
                bg="#fefefe"
            ).grid(row=start_row, column=col, padx=5, sticky="w")

    def redraw_optimal_table(self):
        """Redibuja la tabla fija 'Nivel Óptimo' (parte amarilla) según el idioma actual."""
        for widget in self.frame_opt.winfo_children():
            widget.destroy()

        # Cabeceras
        headers = self.current_lang["table_headers"]
        for col, text in enumerate(headers):
            tk.Label(
                self.frame_opt,
                text=text,
                font=("Arial", 10, "bold"),
                bg="#fff9db"
            ).grid(row=0, column=col, padx=10, pady=5, sticky="w")

        # Datos de la tabla en el diccionario
        table_data = self.current_lang["optimal_table"]
        row_idx = 1
        for denom, valor, objetivo in table_data:
            tk.Label(
                self.frame_opt,
                text=denom,
                bg="#fff9db"
            ).grid(row=row_idx, column=0, sticky="w", padx=10, pady=2)
            tk.Label(
                self.frame_opt,
                text=valor,
                bg="#fff9db"
            ).grid(row=row_idx, column=1, sticky="w", pady=2)
            tk.Label(
                self.frame_opt,
                text=objetivo,
                bg="#fff9db"
            ).grid(row=row_idx, column=2, sticky="w", pady=2)
            row_idx += 1

    def create_checkbox_section(self, row):
        self.frame_cajas = tk.LabelFrame(
            self.root,
            text=self.current_lang["label_cajas"],
            font=("Arial", 10, "bold"),
            bg="#fefefe"
        )
        self.frame_cajas.grid(row=row, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        cajas = ["Drive Thru 1", "Drive Thru 2", "Front Counter 1", "Front Counter 2"]
        for i, caja in enumerate(cajas):
            var = tk.IntVar()
            chk = tk.Checkbutton(self.frame_cajas, text=caja, variable=var, bg="#fefefe")
            chk.grid(row=i, column=0, sticky="w", padx=10)
            self.cajas_check.append(var)

    def create_table_section(self, start_row):
        headers = self.current_lang["table_headers"]
        for col, text in enumerate(headers):
            tk.Label(
                self.root,
                text=text,
                font=("Arial", 10, "bold"),
                bg="#fefefe"
            ).grid(row=start_row, column=col, padx=5, sticky="w")

        row = start_row + 1
        all_keys = [
            "$1", "$5", "$10", "$20", "$50", "$100",
            "¢25", "¢10", "¢5", "¢1"
        ]
        for key in all_keys:
            tk.Label(
                self.root,
                text=key,
                bg="#fefefe"
            ).grid(row=row, column=0, sticky="w", padx=10)

            entry = tk.Entry(self.root, width=10)
            entry.grid(row=row, column=1, padx=5)
            self.entries[key] = entry

            opt = OPTIMAL.get(key, {})
            pack_word = "paquetes" if self.current_lang == LANG_ES else "packs"
            if 'target_packs' in opt:
                text_opt = f">= {opt['target_packs']} {pack_word}"
            elif 'max_packs' in opt:
                text_opt = f"≤ {opt['max_packs']} {pack_word}"
            else:
                text_opt = "-"
            tk.Label(self.root, text=text_opt, bg="#fefefe").grid(row=row, column=2, sticky="w")
            row += 1

    def ask_iou_confirmation(self, faltan):
        msg = self.current_lang["ask_iou_msg"]
        ttl = self.current_lang["ask_iou_title"]
        cfm = self.current_lang["ask_iou_confirm"]
        response = messagebox.askyesno(ttl, msg)
        if response:
            messagebox.showinfo("Confirmado", cfm.format(f"{faltan:.2f}"))

    def show_order_window(self, suggestions):
        win = Toplevel(self.root)
        win.title(self.current_lang["order_change_title"])
        win.configure(bg="#fffbe6")
        tk.Label(
            win,
            text=self.current_lang["order_change_header"],
            font=("Arial", 12, "bold"),
            bg="#fffbe6",
            fg="#b30000"
        ).pack(pady=10)

        for suggestion in suggestions:
            tk.Label(
                win,
                text=suggestion,
                anchor="w",
                justify="left",
                bg="#fffbe6"
            ).pack(anchor="w", padx=20)

    def check_recommendations(self):
        report = []
        total_dollars = 0
        small_change_dollars = 0
        suggestions = []
        total_packs = {}

        # Phrasing
        phrase_order = "Ordenar" if self.current_lang == LANG_ES else "Order"
        phrase_of = "de" if self.current_lang == LANG_ES else "of"
        phrase_pack_word = "paquetes" if self.current_lang == LANG_ES else "packs"

        for key, entry in self.entries.items():
            try:
                amount = float(entry.get())
            except ValueError:
                amount = 0

            total_dollars += amount
            if key in ["$1", "$5", "¢25", "¢10", "¢5", "¢1"]:
                small_change_dollars += amount

            if key in OPTIMAL:
                config = OPTIMAL[key]
                pack_size = config["pack_size"]
                packs = amount / pack_size
                total_packs[key] = packs

                label_color = "#d4edda"
                if 'target_packs' in config and packs < config['target_packs']:
                    faltan = config['target_packs'] - packs
                    faltan_redondeado = int(round(faltan))
                    total_faltante = faltan_redondeado * pack_size
                    label_color = "#fff3cd"
                    suggestions.append(
                        f"{phrase_order} {faltan_redondeado} {phrase_pack_word} {phrase_of} {key} (≈ ${total_faltante:.2f})"
                    )
                if 'max_packs' in config and packs > config['max_packs']:
                    label_color = "#f8d7da"
                    report.append(
                        f"⚠️ Demasiados {phrase_pack_word} {phrase_of} {key}. Máximo: {config['max_packs']}, tienes: {packs:.1f}."
                    )

                entry.config(bg=label_color)

            if key in ["$10", "$20", "$50", "$100"] and amount > 0:
                if self.current_lang == LANG_ES:
                    report.append(f"⚠️ Tienes billetes de {key}. Cambia por $1 o $5.")
                    suggestions.append(f"Cambiar ${amount:.2f} de {key} por billetes pequeños o monedas.")
                else:
                    report.append(f"⚠️ You have {key} bills. Exchange them for $1 or $5.")
                    suggestions.append(f"Exchange ${amount:.2f} of {key} for small bills or coins.")

        # Sumar cajas
        cajas_checked = sum(var.get() for var in self.cajas_check)
        cajas_total = cajas_checked * 200
        total_dollars += cajas_total

        if small_change_dollars < 1200:
            report.append(self.current_lang["report_small_change"])

        if cajas_checked < 4:
            report.append(self.current_lang["report_incomplete_boxes"].format(cajas_checked))

        result_text = f"💵 Total (safe + cajas): ${total_dollars:.2f}\n"
        if total_packs:
            result_text += self.current_lang["packs_title"]
            for k, v in total_packs.items():
                result_text += f"- {k}: {v:.1f} {phrase_pack_word}\n"

        result_text += "\n"
        result_text += "\n".join(report) if report else "✅ Todo está dentro del nivel óptimo."

        self.result_label.config(text=result_text)

        if suggestions:
            self.show_order_window(suggestions)

        if total_dollars < 2300:
            faltan = 2300 - total_dollars
            self.ask_iou_confirmation(faltan)


def main():
    root = tk.Tk()
    app = SafeManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
