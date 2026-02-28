import json
import re
from pathlib import Path
from typing import Any

def task1(s: str) -> bool:
    return bool(re.fullmatch(r"ab*", s))
def task2(s: str) -> bool:
    return bool(re.fullmatch(r"ab{2,3}", s))
def task3(s: str) -> bool:
    return bool(re.fullmatch(r"[a-z]+_[a-z]+", s))
def task4(s: str) -> bool:
    return bool(re.fullmatch(r"[A-Z][a-z]+", s))
def task5(s: str) -> bool:
    return bool(re.fullmatch(r"a.*b", s))
def task6(s: str) -> str:
    return re.sub(r"[ ,\.]", ":", s)
def task7(s: str) -> str:
    return re.sub(r"_([a-z])", lambda m: m.group(1).upper(), s)
def task8(s: str) -> list[str]:
    return [part for part in re.split(r"(?=[A-Z])", s) if part]
def task9(s: str) -> str:
    return re.sub(r"(?<!^)([A-Z])", r" \1", s)
def task10(s: str) -> str:
    return re.sub(r"(?<!^)([A-Z])", r"_\1", s).lower()


def run_regex_examples():
    return {
        "task1": {"abbb": task1("abbb"), "a": task1("a"), "ac": task1("ac")},
        "task2": {"abb": task2("abb"), "abbb": task2("abbb"), "abbbb": task2("abbbb")},
        "task3": {"abc_def": task3("abc_def"), "abc_": task3("abc_"), "Abc_def": task3("Abc_def")},
        "task4": {"Hello": task4("Hello"), "HELLO": task4("HELLO"), "hello": task4("hello")},
        "task5": {"axxxb": task5("axxxb"), "ab": task5("ab"), "ba": task5("ba")},
        "task6": {"input": "hello, world. test", "output": task6("hello, world. test")},
        "task7": {"hello_world_test": task7("hello_world_test")},
        "task8": {"HelloWorldTest": task8("HelloWorldTest")},
        "task9": {"HelloWorldTest": task9("HelloWorldTest")},
        "task10": {"helloWorldTest": task10("helloWorldTest")},
    }


RAW_PATH = Path(__file__).with_name("raw.txt")


def money_to_float(s: str) -> float:
    return float(s.replace("\u00A0", " ").replace(" ", "").replace(",", "."))


def extract_datetime(text: str) -> str | None:
    m = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})", text)
    if not m:
        return None
    return f"{m.group(1)} {m.group(2)}"


def extract_payment_method(text: str) -> str | None:
    if re.search(r"Банковская\s+карта", text, flags=re.IGNORECASE):
        return "BANK_CARD"
    if re.search(r"Наличные", text, flags=re.IGNORECASE):
        return "CASH"
    return None


def extract_total(text: str) -> float | None:
    m = re.search(r"ИТОГО:\s*\n\s*([\d ]+,\d{2})", text, flags=re.IGNORECASE)
    if not m:
        return None
    return money_to_float(m.group(1))


def extract_items_europharma(text: str) -> list[dict[str, Any]]:
    """
    Parses items in EUROPHARMA receipt format:

    1.
    Product name
    2,000 x 154,00
    308,00
    Стоимость
    308,00
    """
    item_pat = re.compile(
        r"(?m)^(?P<idx>\d+)\.\s*\n"
        r"(?P<name>.+?)\n"
        r"(?P<qty>\d+,\d+)\s*x\s*(?P<unit>[\d ]+,\d{2})\n"
        r"(?P<line_total>[\d ]+,\d{2})"
    )

    items: list[dict[str, Any]] = []
    for m in item_pat.finditer(text):
        name = m.group("name").strip()
        qty = float(m.group("qty").replace(",", "."))
        unit_price = money_to_float(m.group("unit"))
        line_total = money_to_float(m.group("line_total"))

        items.append({
            "name": name,
            "qty": qty,
            "unit_price": unit_price,
            "line_total": line_total
        })

    return items


def extract_all_prices(text: str) -> list[float]:
    """
    Extract all money-like values in receipt.
    Note: will include many numbers (unit prices, totals, VAT 0,00, etc.)
    """
    money_pat = re.compile(r"(?<!\d)(?:\d{1,3}(?:[ \u00A0]\d{3})*|\d+),\d{2}(?!\d)")
    prices = [money_to_float(m.group(0)) for m in money_pat.finditer(text)]
    return prices


def parse_receipt(text: str) -> dict[str, Any]:
    items = extract_items_europharma(text)
    total_from_receipt = extract_total(text)

    computed_total = round(sum(it["line_total"] for it in items), 2)

    return {
        "datetime": extract_datetime(text),
        "payment_method": extract_payment_method(text),
        "items": items,
        "total_from_receipt": total_from_receipt,
        "total_computed_from_items": computed_total,
        "all_prices_found": extract_all_prices(text),
    }


def main() -> None:
    print("=== RegEx exercises demo (tasks 1–10) ===")
    print(json.dumps(run_regex_examples(), ensure_ascii=False, indent=2))

    print("\n=== Receipt parsing from raw.txt ===")
    if not RAW_PATH.exists():
        print(f"ERROR: raw.txt not found at: {RAW_PATH}")
        return

    text = RAW_PATH.read_text(encoding="utf-8", errors="ignore")
    parsed = parse_receipt(text)
    print(json.dumps(parsed, ensure_ascii=False, indent=2))

    if parsed["total_from_receipt"] is not None:
        ok = abs(parsed["total_from_receipt"] - parsed["total_computed_from_items"]) < 0.01
        print("\nTOTAL CHECK:", "OK ✅" if ok else "NOT MATCH ❌")


if __name__ == "__main__":
    main()