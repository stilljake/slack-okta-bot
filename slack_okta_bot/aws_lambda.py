#!/usr/bin/env python3
from datetime import datetime
from json import dumps
from os import environ

from logging import getLogger
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
from slack_bolt import App

from .config import LOGGER
from .slack import slack_app


IS_LAMBDA = bool(environ.get("AWS_LAMBDA_FUNCTION_VERSION"))


class LambdaHandler:
    def __init__(self, app: App = slack_app):
        self.app = app
        self.handler = SlackRequestHandler(app=app)

    def handle(self, event, context):
        if event["requestContext"].get("elb"):
            try:
                event = parse_from_alb(event)
            except Exception as e:
                LOGGER.exception(f"Could not parse event from ELB: {e}")

        try:
            res = self.handler.handle(event, context)
            LOGGER.info(res)
            return res
        except Exception as e:
            LOGGER.exception(e)


def parse_from_alb(event: dict) -> dict:
    """
    Update the event to mimic a Lambda URL direct invocation. Bolt doesn't know how to handle
    events from ELB's
    """

    ts = int(event["headers"]["x-slack-request-timestamp"])
    dt = datetime.fromtimestamp(ts).strftime("%d/%b/%Y:%H:%M:%S +0000")
    event["rawPath"] = event["path"]
    req = {
        "accountId": "anonymous",
        "apiId": "",
        "domainName": event["headers"]["host"],
        "domainPrefix": "",
        "http": {
            "method": "POST",
            "path": event["path"],
            "protocol": "HTTP/1.1",
            "sourceIp": "",
            "userAgent": event["headers"].get("user-agent", "unknown"),
        },
        "requestId": "",
        "routeKey": "$default",
        "stage": "$default",
        "time": dt,
        "timeEpoch": ts,
    }
    event["requestContext"].update(req)

    return event


def lambda_handler(event, context):
    LOGGER.info(dumps(event, indent=2))
    handler = LambdaHandler(slack_app)
    try:
        res = handler.handle(event, context)
        LOGGER.info(res)
        return res
    except Exception as e:
        LOGGER.exception(e)
