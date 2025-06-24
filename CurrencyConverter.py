import argparse
import logging
import requests
import customtkinter

def button_pressed():
    print("Button gedrückt")
    
def get_available_currencies():
    frankfurter_currencies_url = "https://api.frankfurter.dev/v1/currencies"
    response = requests.get(frankfurter_currencies_url)
    logging.info(f"URL Aufruf gestartet an: {frankfurter_currencies_url}")
    if response.status_code == 200:
        logging.info(f"{response.status_code}: Daten erfolgreich erhalten")
        data = response.json()
        result = list(data.keys())
        return result
    else:
        logging.error(response.status_code)
        return None
    
def argument_parser():
    argumentparser = argparse.ArgumentParser(description="Währungskonverter - Entweder alle drei Argumente (--amount, --fromcurrency, --tocurrency) "
                        "oder keines für GUI Oberfläche.")
    argumentparser.add_argument('--log-level', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], 
                                help="Logging Level auswählen")
    argumentparser.add_argument("--amount", "-a", type=float, help="Betrag welcher konvertiert werden soll")
    argumentparser.add_argument("--fromcurrency", "-f", type=str, help="Währung des Inputs")
    argumentparser.add_argument("--tocurrency", "-t", type=str, help="Währung des Outputs")

    return argumentparser.parse_args()

## CLI USAGE
def cli_access(args):
    frankfurter_url = "https://api.frankfurter.dev/v1/latest"
    parameters = {
        "base": args.fromcurrency,
        "symbols": args.tocurrency
    }
    logging.info(f"Konvertiere {args.amount} {args.fromcurrency} nach {args.tocurrency}")
    response = requests.get(frankfurter_url, parameters)
    logging.info(f"URL Aufruf gestartet an: {response.url}")
    if response.status_code == 200:
        data = response.json()
        result = data["rates"][args.tocurrency]
        logging.info(f"{response.status_code}: Konvertierungsrate: {result}")
    else:
        logging.error(response.status_code)

    converted_result = float(result) * args.amount
    print(f"{args.amount} {args.fromcurrency} sind zur Zeit umgerechnet {converted_result:.2f} {args.tocurrency}!")

## GUI USAGE    
def gui_access():
    root = customtkinter.CTk()
    root.geometry("450x170")
    root.title("Currency Converter")
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    amount = customtkinter.CTkEntry(root, placeholder_text="Betrag eingeben")
    amount.grid(columnspan = 2, sticky = 'ew', row = 0, padx = 10, pady=10)
    
    from_label = customtkinter.CTkLabel(root, text="Von:")
    from_label.grid(row=1, column=0, padx=10, pady=(0,5), sticky='w')
    to_label = customtkinter.CTkLabel(root, text="Nach:")
    to_label.grid(row=1, column=1, padx=10, pady=(0,5), sticky='w')

    fromcurrency_cb = customtkinter.CTkComboBox(root, values=get_available_currencies())
    fromcurrency_cb.set("USD")
    fromcurrency_cb.grid(row = 1, column = 0, padx = 5, pady=5)
    tocurrency_cb = customtkinter.CTkComboBox(root, values=get_available_currencies())
    tocurrency_cb.set("EUR")
    tocurrency_cb.grid(row = 1, column = 1, padx = 5, pady=5)
    button = customtkinter.CTkButton(root, text="Convert", command=button_pressed)
    button.grid(columnspan = 2, sticky = 'ew', row = 2, padx = 5, pady=5)
    label = customtkinter.CTkLabel(master=root, text="CTkLabel")
    label.grid(columnspan = 2, sticky = 'ew', row = 3, padx = 5, pady=5)
        
    root.mainloop()

# MAIN METHOD
def main():
    args = argument_parser()
    currency_args = [args.amount, args.fromcurrency, args.tocurrency]
    provided_count = len(list(filter(None, currency_args)))

    if provided_count != 0 and provided_count != 3:
        logging.error("Entweder alle drei Argumente (--amount, --fromcurrency, --tocurrency) "
                        "oder keines für GUI Oberfläche.")

    if provided_count == 3:
        cli_access(args)

    if provided_count == 0:
        gui_access()

if __name__  == "__main__":
    main()