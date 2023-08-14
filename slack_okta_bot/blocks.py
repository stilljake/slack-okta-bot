#!/usr/bin/env python3
from typing import Dict, List
from .config import HELP_CHANNEL, HOME_HEADER, RESET_MFA_COMMAND, RESET_PASSWORD_COMMAND, HOME_VIEW


def get_reset_password_form(email) -> List[Dict]:
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":gear: *Confirm that you want to reset the password for the Okta account {email}. You can choose to recieve a password reset email or a reset link as a slack message.*",
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":gear: *Select reset method*",
            },
            "accessory": {
                "action_id": "confirm_password_reset",
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Click to select Email or Slack",
                },
                "options": [
                    {
                        "text": {"type": "plain_text", "text": "Send password reset email to @taxfix/personal email"},
                        "value": "send_email",
                    },
                    {
                        "text": {"type": "plain_text", "text": "Send password reset link as a Slack message here"},
                        "value": "send_reset_link",
                    }

                ],
            },
        },
    ]


def get_reset_mfa_form(
    email: str, factors: List[Dict[str, str]]
) -> List[Dict[str, str]]:
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":gear: *Reset MFA Devices for the Okta account {email}* :gear:",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "You can select multiple factors. Resetting all MFA factors will force Okta to prompt you to re-enroll a factor on next login. If you reset a single factor you will be required to use an existing factor for your next login and can add a factor in your personal account settings.\n",
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":gear: *Select MFA factors to reset*",
            },
            "accessory": {
                "action_id": "reset_selected_mfa",
                "type": "multi_static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Click to select MFA Factors",
                },
                "options": [
                    {
                        "text": {"type": "plain_text", "text": name},
                        "value": id,
                    }
                    for id, name in factors.items()
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
                    "text": f"\n\nTo reset MFA factors: `{RESET_MFA_COMMAND}`\nReset your password: `{RESET_PASSWORD_COMMAND}`\n\n",
                },
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"\n\nWhen resetting MFA you won't be prompted on login to re-enroll if you have any other methods still enrolled. If you have at least one working MFA you can add or remove authenticators under your personal settings in Okta. Resetting all MFA factors will cause Okta to prompt you to enroll a factor after a successful password login.\n\n:ticket: For additional help submit a ticket here: {HELP_CHANNEL} :ticket:",
                },
            },
        ],
    }

    if HOME_VIEW:
        homeview = [
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": HOME_VIEW
                }
            }
        ]
        form["blocks"] += homeview

    return form
