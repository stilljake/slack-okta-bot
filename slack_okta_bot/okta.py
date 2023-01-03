#!/usr/bin/env python3
from json import dumps
from os import environ
from typing import Dict, List

from requests import Session

from .config import LOGGER


# Okta auth config
OKTA_SESSION = Session()
try:
    OKTA_TOKEN = environ["OKTA_TOKEN"]
    OKTA_URL = environ["OKTA_API_URL"]
except KeyError as e:
    LOGGER.error(f"Missing env var: {e}")

OKTA_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"SSWS {OKTA_TOKEN}",
}
OKTA_SESSION.headers = OKTA_HEADERS


def get_mfa_for_user(email: str) -> List[Dict[str, str]]:
    uid = get_uid_by_email(email)
    res = OKTA_SESSION.get(
        f"{OKTA_URL}/users/{uid}/authenticatorEnrollments").json()
    LOGGER.info(dumps(res, indent=2))

    factors = {}
    for factor in res:
        if factor["type"] in ("password", "email"):
            continue
        name = factor["name"]
        if device := factor.get("profile", {}).get("deviceName"):
            name += f" ({device})"

        factors[factor["id"]] = name

    return factors


def get_uid_by_email(email: str) -> str:
    email = email.replace("@", "%40")
    res = OKTA_SESSION.get(f"{OKTA_URL}/users/{email}")
    res.raise_for_status()
    uid = res.json()["id"]
    return uid


def reset_factor(uid: str, factor_id: str) -> int:
    url = f"{OKTA_URL}/users/{uid}/factors/{factor_id}"
    res = OKTA_SESSION.delete(url)
    try:
        res.raise_for_status()
    except Exception as e:
        if res.status_code not in (404, 400):
            raise e from e
    return res.status_code


def send_password_email(email: str) -> int:
    # Get Okta user id from Slack email address
    res = OKTA_SESSION.get(f"{OKTA_URL}/users/{email}")
    res.raise_for_status()
    link = res.json()["_links"]["resetPassword"]["href"]
    
    # Send a password reset email
    res = OKTA_SESSION.post(f"{link}?sendEmail=true")
    res.raise_for_status()
    return res.status_code

