#!/usr/bin/env python3
"""Send an SMS using the sender name "GCash Sample".

Uses Twilio. Set credentials via environment variables:
  TWILIO_ACCOUNT_SID
  TWILIO_AUTH_TOKEN
  TWILIO_FROM_NUMBER  (optional fallback if alphanumeric sender ID is unavailable)

Example:
  export TWILIO_ACCOUNT_SID=ACxxxxxxxx
  export TWILIO_AUTH_TOKEN=your_auth_token
  python scripts/gcash_sample.py --to +639171234567 --message "Your payment was received."
"""

from __future__ import annotations

import argparse
import os
import sys

SENDER_NAME = "GCash Sample"


def send_sms(to: str, message: str, *, dry_run: bool = False) -> str:
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    fallback_from = os.environ.get("TWILIO_FROM_NUMBER")

    if dry_run:
        print("Dry run - SMS not sent.")
        print(f"  From: {SENDER_NAME}")
        print(f"  To:   {to}")
        print(f"  Body: {message}")
        return "dry-run"

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

    try:
        result = client.messages.create(
            to=to,
            from_=SENDER_NAME,
            body=message,
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
            body=f"[{SENDER_NAME}] {message}",
        )

    return result.sid


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Send an SMS with the sender name "GCash Sample".'
    )
    parser.add_argument(
        "--to",
        required=True,
        help="Recipient phone number in E.164 format (e.g. +639171234567).",
    )
    parser.add_argument(
        "--message",
        "-m",
        default="This is a sample SMS from GCash Sample.",
        help="SMS message body.",
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
        sid = send_sms(args.to, args.message, dry_run=args.dry_run)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if not args.dry_run:
        print(f"SMS sent successfully. Message SID: {sid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
