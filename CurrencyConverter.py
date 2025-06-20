import argparse
import logging
import requests
import customtkinter

def button_pressed():
    print("Button gedrückt")

argumentparser = argparse.ArgumentParser(description="Währungskonverter - Entweder alle drei Argumente (--amount, --fromcurrency, --tocurrency) "
                    "oder keines für GUI Oberfläche.")
argumentparser.add_argument('--log-level', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], 
                            help="Logging Level auswählen")
argumentparser.add_argument("--amount", "-a", type=float, help="Betrag welcher konvertiert werden soll")
argumentparser.add_argument("--fromcurrency", "-f", type=str, help="Währung des Inputs")
argumentparser.add_argument("--tocurrency", "-t", type=str, help="Währung des Outputs")

args = argumentparser.parse_args()


currency_args = [args.amount, args.fromcurrency, args.tocurrency]
provided_count = len(list(filter(None, currency_args)))

if provided_count != 0 and provided_count != 3:
    logging.error("Entweder alle drei Argumente (--amount, --fromcurrency, --tocurrency) "
                    "oder keines für GUI Oberfläche.")

conversion_url = "https://api.frankfurter.dev/v1/latest"
parameters = {
    "base": args.fromcurrency,
    "symbols": args.tocurrency
}

if provided_count == 3:
    logging.info(f"Konvertiere {args.amount} {args.fromcurrency} nach {args.tocurrency}")
    response = requests.get(conversion_url, parameters)
    logging.info(f"URL Aufruf gestartet an: {response.url}")
    if response.status_code == 200:
        data = response.json()
        result = data["rates"][args.tocurrency]
        logging.info(f"Konvertierungsrate: {result}")
    else:
        logging.error(response.status_code)

    converted_result = float(result) * args.amount
    print(f"{args.amount} {args.fromcurrency} sind zur Zeit umgerechnet {converted_result:.2f} {args.tocurrency}!")

#TODO CLI Use with arguments, otherwise GUI
#TODO Textfields erstellen
#TODO Währungen beziehen und via Drop Down neben Textfields
if provided_count == 0:
    app = customtkinter.CTk()
    app.geometry("300x150")
    app.title("Currency Converter")

    button = customtkinter.CTkButton(app, text="Convert", command=button_pressed)
    button.pack(padx=20, pady=20)
    app.mainloop()