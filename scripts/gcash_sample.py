#!/usr/bin/env python3
"""Send an SMS using the sender name "GCash Sample".

Providers:
  free (default) - Textbelt, no signup, 1 free SMS per day per IP.
                   Uses only Python standard library.
  twilio         - Paid after trial. Supports custom sender IDs in some regions.

Examples:
  # Free - no account needed (1 SMS/day limit)
  python scripts/gcash_sample.py --to 5551234567 --message "Hello"

  # Twilio - requires credentials
  export TWILIO_ACCOUNT_SID=ACxxxxxxxx
  export TWILIO_AUTH_TOKEN=your_auth_token
  python scripts/gcash_sample.py --provider twilio --to +639171234567
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

SENDER_NAME = "GCash Sample"
TEXTBELT_URL = "https://textbelt.com/text"
TEXTBELT_FREE_KEY = "textbelt"


def _format_body(message: str) -> str:
    if message.startswith(f"[{SENDER_NAME}]"):
        return message
    return f"[{SENDER_NAME}] {message}"


def send_sms_free(to: str, message: str) -> str:
    """Send via Textbelt free tier (1 SMS/day, no API key required)."""
    payload = urllib.parse.urlencode(
        {
            "phone": to,
            "message": _format_body(message),
            "key": TEXTBELT_FREE_KEY,
            "sender": SENDER_NAME,
        }
    ).encode("utf-8")

    request = urllib.request.Request(
        TEXTBELT_URL,
        data=payload,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Textbelt request failed ({exc.code}): {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Could not reach Textbelt: {exc.reason}") from exc

    if not body.get("success"):
        error = body.get("error", "Unknown error")
        raise RuntimeError(
            f"Free SMS failed: {error}. "
            "The free tier allows 1 SMS per day and works best with US/Canada numbers."
        )

    quota = body.get("quotaRemaining")
    if quota is not None:
        print(f"Free quota remaining today: {quota}")

    return str(body.get("textId", "sent"))


def send_sms_twilio(to: str, message: str) -> str:
    """Send via Twilio (paid; new accounts get trial credit)."""
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    fallback_from = os.environ.get("TWILIO_FROM_NUMBER")

    if not account_sid or not auth_token:
        raise RuntimeError(
            "Missing Twilio credentials. Set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN."
        )

    try:
        from twilio.rest import Client
    except ImportError as exc:
        raise RuntimeError(
            "Twilio SDK not installed. Run: pip install twilio"
        ) from exc

    client = Client(account_sid, auth_token)
    body = _format_body(message)

    try:
        result = client.messages.create(
            to=to,
            from_=SENDER_NAME,
            body=body,
        )
    except Exception as exc:
        if not fallback_from:
            raise RuntimeError(
                f"Failed to send with sender name '{SENDER_NAME}'. "
                "Alphanumeric sender IDs require carrier approval in many regions. "
                "Set TWILIO_FROM_NUMBER to use a Twilio phone number instead."
            ) from exc

        result = client.messages.create(
            to=to,
            from_=fallback_from,
            body=body,
        )

    return result.sid


def send_sms(
    to: str,
    message: str,
    *,
    provider: str = "free",
    dry_run: bool = False,
) -> str:
    if dry_run:
        print("Dry run - SMS not sent.")
        print(f"  Provider: {provider}")
        print(f"  From:     {SENDER_NAME}")
        print(f"  To:       {to}")
        print(f"  Body:     {_format_body(message)}")
        return "dry-run"

    if provider == "free":
        return send_sms_free(to, message)
    if provider == "twilio":
        return send_sms_twilio(to, message)

    raise RuntimeError(f"Unknown provider: {provider}. Use 'free' or 'twilio'.")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Send an SMS with the sender name "GCash Sample".'
    )
    parser.add_argument(
        "--to",
        required=True,
        help="Recipient phone number (E.164 for international, e.g. +639171234567).",
    )
    parser.add_argument(
        "--message",
        "-m",
        default="This is a sample SMS from GCash Sample.",
        help="SMS message body.",
    )
    parser.add_argument(
        "--provider",
        choices=("free", "twilio"),
        default="free",
        help="SMS provider: 'free' (Textbelt, 1/day, no signup) or 'twilio' (paid).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the SMS details without sending.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    try:
        sid = send_sms(
            args.to,
            args.message,
            provider=args.provider,
            dry_run=args.dry_run,
        )
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if not args.dry_run:
        print(f"SMS sent successfully. ID: {sid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
