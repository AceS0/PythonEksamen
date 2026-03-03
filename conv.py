import argparse
import os
import sys

import requests
from dotenv import load_dotenv, set_key

ENV_FILE = ".env"


def save_api_key(api_key: str) -> None:
    """Save API key to .env file for future use."""
    set_key(ENV_FILE, "API_KEY", api_key)
    print(f"API key saved to {ENV_FILE}")


def get_api_key() -> str | None:
    """Load and return API key from .env file."""
    load_dotenv(ENV_FILE)
    return os.getenv("API_KEY")


def convert_currency(api_key: str, from_currency: str, to_currency: str, amount: float) -> None:
    """Fetch conversion rate from exchangerate-api.com and print the result."""
    url = (
        f"https://v6.exchangerate-api.com/v6/{api_key}"
        f"/pair/{from_currency}/{to_currency}/{amount}"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the exchange rate API. Check your internet connection.")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("Error: The request timed out. Please try again.")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP error occurred: {e}")
        sys.exit(1)

    data = response.json()

    if data.get("result") == "success":
        conversion_result = data["conversion_result"]
        rate = data["conversion_rate"]
        print(f"\n  {amount} {from_currency} = {conversion_result:.2f} {to_currency}")
        print(f"  Exchange rate: 1 {from_currency} = {rate} {to_currency}\n")
    else:
        error_type = data.get("error-type", "unknown-error")
        error_messages = {
            "invalid-key": "The API key is invalid. Use --key to set a valid key.",
            "inactive-account": "Your API account is inactive. Check your account at exchangerate-api.com.",
            "malformed-request": "The request was malformed. Check the currency codes and amount.",
        }
        print(f"Error: {error_messages.get(error_type, error_type)}")
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Currency Converter CLI - Convert between currencies using live exchange rates.",
        epilog=(
            "Examples:\n"
            "  First run:       py conv.py --key YOUR_API_KEY USD EUR 100\n"
            "  Subsequent runs: py conv.py USD EUR 100\n"
            "  Save key only:   py conv.py --key YOUR_API_KEY"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--key",
        metavar="API_KEY",
        help="Your exchangerate-api.com API key. Saved to .env for future runs.",
    )
    parser.add_argument(
        "from_currency",
        nargs="?",
        metavar="FROM",
        help="Currency code to convert from (e.g. USD)",
    )
    parser.add_argument(
        "to_currency",
        nargs="?",
        metavar="TO",
        help="Currency code to convert to (e.g. EUR)",
    )
    parser.add_argument(
        "amount",
        nargs="?",
        type=float,
        metavar="AMOUNT",
        help="Amount to convert (e.g. 100)",
    )

    args = parser.parse_args()

    # --- API key handling ---
    if args.key:
        save_api_key(args.key)

    api_key = args.key or get_api_key()

    if not api_key:
        print(
            "Error: No API key found.\n"
            "  Get a free key at https://www.exchangerate-api.com/\n"
            "  Then run: py conv.py --key YOUR_API_KEY\n"
        )
        sys.exit(1)

    # --- Conversion ---
    conversion_args = [args.from_currency, args.to_currency, args.amount]

    if all(a is not None for a in conversion_args):
        convert_currency(
            api_key,
            args.from_currency.upper(),
            args.to_currency.upper(),
            args.amount,
        )
    elif any(a is not None for a in conversion_args):
        # Some but not all conversion arguments given
        print("Error: Please provide all three arguments: FROM TO AMOUNT")
        print("  Example: py conv.py USD EUR 100")
        sys.exit(1)
    elif args.key:
        # Key was saved, no conversion requested — that is fine
        print("Run 'py conv.py FROM TO AMOUNT' to convert currencies.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
