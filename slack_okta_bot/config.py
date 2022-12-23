#!/usr/bin/env python3
from logging import basicConfig, getLogger
from os import environ
from sys import stdout


HELP_CHANNEL = environ.get("HELP_CHANNEL", "#devops-help")
HOME_HEADER = environ.get(
    "HOME_HEADER", ":gear: Get help with common DevOps Okta tasks :gear:"
)
RESET_MFA_COMMAND = environ.get("RESET_MFA_COMMAND", "/reset-mfa")
RESET_PASSWORD_COMMAND = environ.get("RESET_PASSWORD_COMMAND", "/reset-password")
LOGGER = getLogger(__name__.split(".")[0])

LOGGER.setLevel(environ.get("LOG_LEVEL", "INFO"))

if not environ.get("AWS_LAMBDA_FUNCTION_VERSION"):
    basicConfig(stream=stdout)