import argparse
import sys
import logging
import requests
import customtkinter


def get_available_currencies():
    frankfurter_currencies_url = "https://api.frankfurter.dev/v1/currencies"
    try:
        response = requests.get(frankfurter_currencies_url, timeout=5)
        logging.info(f"URL Aufruf gestartet an: {frankfurter_currencies_url}")
        response.raise_for_status()
        return list(response.json().keys())
    except requests.RequestException as e:
        logging.error(f"Fehler beim Abruf der Währungen: {e}")
        sys.exit("Fehler: Keine Verbindung zur API möglich.")


def get_conversion_rate(from_currency, to_currency):
    frankfurter_url = "https://api.frankfurter.dev/v1/latest"
    parameters = {"base": from_currency, "symbols": to_currency}
    try:
        response = requests.get(frankfurter_url, parameters, timeout=5)
        logging.info(f"URL Aufruf gestartet an: {response.url}")
        response.raise_for_status()
        data = response.json()
        result = data["rates"][to_currency]
        logging.info(f"{response.status_code}: Konvertierungsrate: {result}")
        return result
    except requests.RequestException as e:
        logging.error(f"Fehler beim Abruf der Umrechnungsrate: {e}")
        sys.exit("Fehler: Keine Verbindung zur API möglich.")


def parse_arguments():
    argument_parser = argparse.ArgumentParser(
        description=(
            "Währungskonverter - Entweder alle drei Argumente (--amount, --fromcurrency, "
            "--tocurrency) oder keines für GUI Oberfläche."
        )
    )
    argument_parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging Level auswählen",
    )
    argument_parser.add_argument(
        "--amount", "-a", type=float, help="Betrag welcher konvertiert werden soll"
    )
    argument_parser.add_argument(
        "--fromcurrency", "-f", type=str, help="Währung des Inputs"
    )
    argument_parser.add_argument(
        "--tocurrency", "-t", type=str, help="Währung des Outputs"
    )

    return argument_parser.parse_args()


# CLI USAGE
def run_cli(args):
    logging.info(
        f"Konvertiere {args.amount} {args.fromcurrency} nach {args.tocurrency}"
    )
    conversion_rate = get_conversion_rate(args.fromcurrency, args.tocurrency)
    converted_result = float(conversion_rate) * args.amount
    print(
        f"{args.amount} {args.fromcurrency} sind zur Zeit umgerechnet {converted_result:.2f} {args.tocurrency}!"
    )


# GUI USAGE
def run_gui():
    root = customtkinter.CTk()
    root.geometry("450x200")
    root.title("Währungsrechner")
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    amount = customtkinter.CTkEntry(root, placeholder_text="Betrag eingeben")
    amount.grid(columnspan=2, sticky="ew", row=0, padx=10, pady=10)

    from_label = customtkinter.CTkLabel(root, text="Von:")
    from_label.grid(row=1, column=0, padx=10, pady=1, sticky="w")
    to_label = customtkinter.CTkLabel(root, text="Nach:")
    to_label.grid(row=1, column=1, padx=10, pady=1, sticky="w")

    from_currency_cb = customtkinter.CTkComboBox(
        root, values=get_available_currencies()
    )
    from_currency_cb.set("USD")
    from_currency_cb.grid(row=1, column=0, padx=5, pady=5)
    to_currency_cb = customtkinter.CTkComboBox(root, values=get_available_currencies())
    to_currency_cb.set("EUR")
    to_currency_cb.grid(row=1, column=1, padx=5, pady=5)
    result = ""

    # Interne Funktionen
    def button_pressed():
        calculate_result(
            from_currency_cb.get(),
            amount.get(),
            to_currency_cb.get(),
            get_conversion_rate(from_currency_cb.get(), to_currency_cb.get()),
        )

    def calculate_result(from_currency, amount, to_currency, conversion_rate):
        try:
            amount = amount.strip().replace(",", ".")
            calculation = float(amount) * conversion_rate    
            calculation_label.configure(
            text=f"{amount} {from_currency} sind umgerechnet {calculation:.2f} {to_currency}"
            )
        except ValueError:
            calculation_label.configure(
            text="Bitte gültige Zahl eingeben (z.B. 12.34)"
        )
        

    button = customtkinter.CTkButton(root, text="Umrechnen", command=button_pressed)
    button.grid(columnspan=2, sticky="ew", row=2, padx=5, pady=5)
    calculation_label = customtkinter.CTkLabel(master=root, text=result)
    calculation_label.grid(columnspan=2, sticky="ew", row=3, padx=5, pady=5)
    footnote_label = customtkinter.CTkLabel(
        root,
        text="Umrechnungsraten von 'frankfurter.dev' - Entwickelt von Lukas Esch",
        anchor="center",
        font=(None, 10, "italic"),
    )
    footnote_label.grid(columnspan=2, sticky="ew", row=4, padx=5)

    root.mainloop()


# MAIN METHOD
def main():
    args = parse_arguments()
    logging.basicConfig(level=getattr(logging, args.log_level))
    currency_args = [args.amount, args.fromcurrency, args.tocurrency]
    provided_count = len(list(filter(None, currency_args)))

    if provided_count != 0 and provided_count != 3:
        logging.error(
            "Entweder alle drei Argumente (--amount, --fromcurrency, --tocurrency) "
            "oder keines für GUI Oberfläche."
        )
        sys.exit()

    if provided_count == 3:
        run_cli(args)

    if provided_count == 0:
        run_gui()


if __name__ == "__main__":
    main()
