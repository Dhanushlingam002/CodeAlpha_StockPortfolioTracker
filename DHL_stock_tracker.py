import csv
import os
from datetime import datetime

STOCK_PRICES: dict[str, float] = {
    "AAPL":  189.50,
    "TSLA":  248.75,
    "GOOGL": 175.30,
    "AMZN":  192.10,
    "MSFT":  415.60,
    "NFLX":  635.80,
    "META":  520.40,
    "NVDA":  875.25,
}

PORTFOLIO: list[dict] = []   # Stores {"stock", "qty", "price", "total"}


def show_available_stocks() -> None:
    print("\n  📈  Available stocks & prices (USD):")
    print("  " + "-" * 30)
    for ticker, price in STOCK_PRICES.items():
        print(f"  {ticker:<8}  ${price:>8.2f}")
    print("  " + "-" * 30 + "\n")


def add_stock() -> None:
    show_available_stocks()
    ticker = input("  Enter stock ticker (e.g. AAPL): ").strip().upper()

    if ticker not in STOCK_PRICES:
        print(f"  ⚠  '{ticker}' not found in our database. Check the list above.")
        return

    try:
        qty = int(input(f"  How many shares of {ticker}? ").strip())
        if qty <= 0:
            raise ValueError
    except ValueError:
        print("  ⚠  Please enter a positive whole number.")
        return

    price = STOCK_PRICES[ticker]
    total = price * qty

    for entry in PORTFOLIO:
        if entry["stock"] == ticker:
            entry["qty"] += qty
            entry["total"] = STOCK_PRICES[ticker] * entry["qty"]
            print(f"  ✅  Updated {ticker}: now holding {entry['qty']} shares.")
            return

    PORTFOLIO.append({"stock": ticker, "qty": qty, "price": price, "total": total})
    print(f"  ✅  Added {qty} × {ticker} @ ${price:.2f} = ${total:,.2f}")


def view_portfolio() -> None:
    if not PORTFOLIO:
        print("\n  ℹ  Your portfolio is empty. Add some stocks first.\n")
        return

    print("\n  📊  Your Portfolio")
    print("  " + "=" * 52)
    print(f"  {'Ticker':<8}  {'Qty':>6}  {'Price (USD)':>12}  {'Total (USD)':>12}")
    print("  " + "-" * 52)

    grand_total = 0.0
    for entry in PORTFOLIO:
        print(
            f"  {entry['stock']:<8}  {entry['qty']:>6}  "
            f"${entry['price']:>11.2f}  ${entry['total']:>11,.2f}"
        )
        grand_total += entry["total"]

    print("  " + "-" * 52)
    print(f"  {'TOTAL INVESTMENT':>28}  ${grand_total:>11,.2f}")
    print("  " + "=" * 52 + "\n")


def remove_stock() -> None:
    if not PORTFOLIO:
        print("\n  ℹ  Portfolio is empty.\n")
        return

    ticker = input("  Enter ticker to remove: ").strip().upper()
    for i, entry in enumerate(PORTFOLIO):
        if entry["stock"] == ticker:
            PORTFOLIO.pop(i)
            print(f"  ✅  {ticker} removed from portfolio.")
            return
    print(f"  ⚠  {ticker} not found in your portfolio.")


def save_to_csv() -> None:
    if not PORTFOLIO:
        print("\n  ℹ  Nothing to save — portfolio is empty.\n")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"portfolio_{timestamp}.csv"

    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["stock", "qty", "price", "total"])
        writer.writeheader()
        writer.writerows(PORTFOLIO)

        grand_total = sum(e["total"] for e in PORTFOLIO)
        writer.writerow({"stock": "TOTAL", "qty": "", "price": "", "total": f"{grand_total:.2f}"})

    print(f"  ✅  Portfolio saved to '{filename}' in the current directory.")



def main() -> None:
    print("\n" + "=" * 50)
    print("   💼  CodeAlpha Stock Portfolio Tracker")
    print("=" * 50)

    menu = {
        "1": ("Add / update a stock",   add_stock),
        "2": ("View portfolio summary", view_portfolio),
        "3": ("Remove a stock",         remove_stock),
        "4": ("Save portfolio to CSV",  save_to_csv),
        "5": ("Exit",                   None),
    }

    while True:
        print("\n  MENU")
        for key, (label, _) in menu.items():
            print(f"  [{key}] {label}")

        choice = input("\n  Enter choice (1-5): ").strip()

        if choice == "5":
            print("\n  Goodbye! Happy investing. 📈\n")
            break
        elif choice in menu:
            menu[choice][1]()
        else:
            print("  ⚠  Invalid option. Please enter 1–5.")


if __name__ == "__main__":
    main()
