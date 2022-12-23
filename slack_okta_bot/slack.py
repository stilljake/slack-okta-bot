#!/usr/bin/env python3
from os import environ
from time import time

from slack_bolt import App

from .blocks import (
  get_home_view,
  get_reset_password_form,
  get_reset_mfa_form
)
from .config import (
    HELP_CHANNEL,
    LOGGER,
    RESET_MFA_COMMAND,
    RESET_PASSWORD_COMMAND,
)
from .okta import (
  get_mfa_for_user,
  get_uid_by_email,
  reset_factor,
  send_password_email
)


try:
    SLACK_BOT_TOKEN = environ["SLACK_BOT_TOKEN"]
    SLACK_SIGNING_SECRET = environ["SLACK_SIGNING_SECRET"]
except KeyError as e:
    LOGGER.error(f"Missing env var: {e}")

TEST_USER = environ.get("TEST_USER")

# Bolt app handler
slack_app = App(
    process_before_response=bool(environ.get("AWS_LAMBDA_FUNCTION_VERSION")),
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET,
)


@slack_app.event("message")
def handle_message(_, __) -> None:
    pass


@slack_app.command(RESET_PASSWORD_COMMAND)
def reset_password_prompt(ack, body) -> None:
    """
    Ack and send the form for resetting password
    """
    user = body["user_id"]
    email = TEST_USER or slack_app.client.users_info(
        user=user)["user"]["profile"]["email"]

    ack(blocks=get_reset_password_form(email))


@slack_app.action("confirm_password_reset")
def reset_password(ack, body, respond) -> None:
    """
    Look up the user's Okta ID and send a password reset email
    """
    ack()
    user = body["user"]["id"]
    email = TEST_USER or slack_app.client.users_info(user=user)["user"]["profile"]["email"]

    try:
        send_password_email(email)
        respond(
            f":email: Password email has been sent to {email}. Check your email and follow the link."
        )
    except Exception:
        respond(
            f":exclamation: Could not reset password for {email}. Reach out in {HELP_CHANNEL} for further help."
        )


@slack_app.command(RESET_MFA_COMMAND)
def reset_mfa_prompt(ack, body) -> None:
    """
    Look up the user's MFA devices and return a form with a drop list containing the options
    """
    user = body["user_id"]
    email = TEST_USER or slack_app.client.users_info(user=user)["user"]["profile"]["email"]

    try:
        factors = get_mfa_for_user(email)
    except Exception:
        ack(
            f"Could not find MFA devices for {email}. Reach out in {HELP_CHANNEL} for help."
        )
        return

    if not factors:
        ack(
            f":exclamation: It lools like you have no registered factors. Try logging in and if you are not prompted to configure MFA contact us at {HELP_CHANNEL}"
        )
        return

    blocks = get_reset_mfa_form(email, factors)

    ack(blocks=blocks)


@slack_app.action("reset_selected_mfa")
def exec_reset_mfa(ack, body, respond):
    ack()
    user = body["user"]["id"]
    email = TEST_USER or slack_app.client.users_info(user=user)["user"]["profile"]["email"]
    okta_user = get_uid_by_email(email)
    selected = [opt["value"] for opt in body["actions"][0]["selected_options"]]

    for factor in selected:
        try:
            reset_factor(okta_user, factor)
            respond(f"Factor with id {factor} has been reset")
        except Exception:
            respond(f"Could not reset MFA device with id {factor}")


@slack_app.event("app_home_opened")
def opened(client, event) -> None:
    """
    Sends home view to app
    """

    try:
        # views.publish is the method that your app uses to push a view to the Home tab
        client.views_publish(
            trigger_id=time(), user_id=event["user"], view=get_home_view()
        )

    except Exception as e:
        LOGGER.error(f"Error publishing home tab: {e}")


# For local runs
def run_local():
    LOGGER.info("Logging to stdout")
    try:
        slack_app.start(port=int(environ.get("PORT", 3000)))
    except KeyboardInterrupt as e:
        LOGGER.info(f"{e} Exiting")
    
