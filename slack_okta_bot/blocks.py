#!/usr/bin/env python3
from typing import Dict, List
from .config import (
  HELP_CHANNEL,
  HOME_HEADER,
  RESET_MFA_COMMAND,
  RESET_PASSWORD_COMMAND
)


def get_reset_password_form(email) -> List[Dict]:
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":gear: *Confirm that you want to reset password for {email}. Okta will send you a password reset email.*",
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "*Are you sure?*"},
            "accessory": {
                "action_id": "confirm_password_reset",
                "type": "button",
                "text": {"type": "plain_text", "text": "Reset My Password"},
            },
        },
    ]


def get_reset_mfa_form(email: str, factors: List[Dict[str, str]]) -> List[Dict[str, str]]:
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":gear: *Reset MFA Devices for {email}* :gear:",
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "You can select multiple devices. Resetting all MFA devices will force Okta to prompt you to re-enroll a device on next login. If you reset a single device you will be required to use an existing device for your next login and can add a device in your personal account settings.\n",
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":gear: *Select an MFA device to reset*",
            },
            "accessory": {
                "action_id": "reset_selected_mfa",
                "type": "multi_static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select MFA Devices to Reset",
                },
                "options": [
                    {
                        "text": {"type": "plain_text", "text": factor["name"]},
                        "value": factor["id"],
                    }
                    for factor in factors
                ],
            },
        },
    ]


def get_home_view() -> Dict:
    form = {
        "type": "home",
        "callback_id": "home_view",
        "blocks": [
            {"type": "header", "text": {"type": "plain_text", "text": HOME_HEADER}},
            {"type": "divider"},
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "\n *Available Commands:* \n"},
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"\n\nTo reset MFA devices: `{RESET_MFA_COMMAND}`\nReset your password: `{RESET_PASSWORD_COMMAND}`\n\n",
                },
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"\n\n:slack: For additional help reach out in {HELP_CHANNEL} :slack:",
                },
            },
        ],
    }

    return form
