#!/usr/bin/env python3
"""Generate Google Contacts search queries for phone-number reconciliation."""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any


def digits_only(value: str | None) -> str:
    return re.sub(r"\D+", "", value or "")


def spaced_last10(digits: str) -> str | None:
    if len(digits) < 10:
        return None
    last10 = digits[-10:]
    return f"{last10[:3]} {last10[3:6]} {last10[6:]}"


def add_variant(variants: list[dict[str, str]], seen: set[str], query: str, kind: str, reason: str) -> None:
    if query and query not in seen:
        variants.append({"query": query, "kind": kind, "reason": reason})
        seen.add(query)


def variants_for_phone(raw: str) -> dict[str, Any]:
    digits = digits_only(raw)
    variants: list[dict[str, str]] = []
    seen: set[str] = set()

    if not digits:
        return {
            "input": raw,
            "digits": "",
            "last10": "",
            "search_queries": [],
            "notes": ["No digits found."],
        }

    if len(digits) >= 10:
        add_variant(variants, seen, f"+{digits}", "e164_raw", "Raw digits with leading plus.")

    if digits.startswith("521") and len(digits) == 13:
        normalized = "52" + digits[3:]
        add_variant(
            variants,
            seen,
            f"+{normalized}",
            "mexico_contacts_e164",
            "Mexico WhatsApp mobile form 521... converted to Google Contacts +52...",
        )
    elif digits.startswith("52") and len(digits) == 12:
        whatsapp_form = "521" + digits[2:]
        add_variant(
            variants,
            seen,
            f"+{whatsapp_form}",
            "mexico_whatsapp_e164",
            "Google Contacts +52... converted to WhatsApp Mexico 521... form.",
        )
    elif len(digits) == 10:
        add_variant(
            variants,
            seen,
            f"+52{digits}",
            "mexico_contacts_e164",
            "Ten-digit Mexico local number converted to Google Contacts +52...",
        )
        add_variant(
            variants,
            seen,
            f"+521{digits}",
            "mexico_whatsapp_e164",
            "Ten-digit Mexico local number converted to WhatsApp Mexico 521... form.",
        )

    if len(digits) == 11 and digits.startswith("1"):
        add_variant(variants, seen, f"+{digits}", "north_america_e164", "North America +1... form.")

    add_variant(variants, seen, digits, "raw_digits", "Raw digits fallback; often less reliable.")
    spaced = spaced_last10(digits)
    if spaced:
        add_variant(variants, seen, spaced, "last10_spaced", "Human-spaced last 10 digits fallback.")

    notes: list[str] = []
    if digits.startswith("521") and len(digits) == 13:
        notes.append("Try the +52... Google Contacts variant before declaring this unresolved.")

    return {
        "input": raw,
        "digits": digits,
        "last10": digits[-10:] if len(digits) >= 10 else digits,
        "search_queries": variants,
        "notes": notes,
    }


def phones_from_whatsapp_json(path: str) -> list[str]:
    if path == "-":
        payload = json.load(sys.stdin)
    else:
        with open(path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)

    chats = payload.get("data", {}).get("chats", [])
    phones: list[str] = []
    for chat in chats:
        if chat.get("chat_type") != "direct":
            continue
        phone = chat.get("phone_number") or chat.get("display_name") or chat.get("name")
        digits = digits_only(phone)
        if digits:
            phones.append(phone)
    return phones


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate Google Contacts phone search queries.")
    parser.add_argument("phones", nargs="*", help="Phone numbers or WhatsApp phone strings.")
    parser.add_argument(
        "--from-whatsapp-json",
        metavar="PATH",
        help="Read whatsapp --json chats list output from PATH, or '-' for stdin.",
    )
    parser.add_argument("--json", action="store_true", help="Emit stable JSON output.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    phones = list(args.phones)
    if args.from_whatsapp_json:
        phones.extend(phones_from_whatsapp_json(args.from_whatsapp_json))

    if not phones:
        parser.error("provide at least one phone number or --from-whatsapp-json PATH")

    results = [variants_for_phone(phone) for phone in phones]

    if args.json:
        print(json.dumps({"ok": True, "phones": results}, indent=2, ensure_ascii=False))
    else:
        for result in results:
            print(result["input"])
            for variant in result["search_queries"]:
                print(f"  {variant['query']}  # {variant['kind']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
