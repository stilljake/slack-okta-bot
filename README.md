# slack-okta-bot

### Provides the backend service for an Okta application that gives users the ability to execute common tasks
The backend can run:
* As a standalone server
* AWS Lambda Function URL
* AWS Lambda as an ELB target

Current features:
* Reset MFA Factors
* Reset password

## Configuration
The following env vars are used for configuration

| Name                   | Description                                                               | Required | Default                                              |   |
|------------------------|---------------------------------------------------------------------------|----------|------------------------------------------------------|---|
| HELP_CHANNEL           | Help channel displayed in responses to user                               | no       | #devops-help                                         |   |
| HOME_HEADER            | Header displayed in app home page                                         | no       | :gear: Get help with common DevOps Okta tasks :gear: |   |
| HOME_VIEW              | Additional info to show in app home page                                  | no       |                                                      |   |
| RESET_MFA_COMMAND      | Command the user sends to reset MFA                                       | no       | /reset-mfa                                           |   |
| RESET_PASSWORD_COMMAND | Command the user sends to reset password                                  | no       | /reset-password                                      |   |
| TEST_USER              | An email address that, if set, be used instead of the user's slack email. | no       |                                                      |   |
| PORT                   | Port to run the local server on                                           | no       | 3000                                                 |   |
| SLACK_BOT_TOKEN        | Slack Bot User Oauth Token                                                | yes      |                                                      |   |
| SLACK_SIGNING_SECRET   | Slack Signing Secret                                                      | yes      |                                                      |   |
| OKTA_API_URL           | Okta api endpoint <yourdomain.okta.com/api/v1>                            | yes      |                                                      |   |
| OKTA_TOKEN             | Okta API token                                                            | yes      |                                                      |   |



## Usage

### With AWS Lambda: The easy way
For convenience, if you don't need any additional logic in your handler, you can just
build your package using `build_lambda.sh` (Described below) and set your Lambda's handler to `slack_okta_bot.aws_lambda.lambda_handler`.



### AWS Lambda: Manual way
```python
from json import dumps
from logging import getLogger

from slack_okta_bot.slack import slack_app
from slack_okta_bot.aws_lambda import LambdaHandler


getLogger().setLevel("INFO")


def handler(event, context):
  getLogger().info(dumps(event, indent=2))
  handler = LambdaHandler(slack_app)
  try:
    res = handler.handle(event, context)
    getLogger().info(res)
    return res
  except Exception as e:
    getLogger().info(e)
```

In your Lambda config You would set your lambda handler to `module.handler` where `module` is the name of your Lambda package module


## Building a basic Lambda package

From source:
* Run `build_with_poetry.sh`. It requires that `poetry` be installed and will install it if missing.
* Upload the created zip file to S3 and configure your Lambda to pull from S3
* Optionally upload the package manually in the AWS Lambda console
* Set your Lambda's handler to `slack_okta_bot.aws_lambda.lambda_handler`

Using PIP
* Run `pip install slack-okta-bot -t packages`
* `cd` into ./packages directory
* Run `zip -r ../lambda.zip . -x '*.pyc'`
* Upload ../lambda.zip to S3 and configure your Lambda to pull from S3
* Optionally upload the package manually in the AWS Lambda console
* Set your Lambda's handler to `slack_okta_bot.aws_lambda.lambda_handler`


### Running as a server
The package will install a shell script that can run a server

```
> slack-okta-bot
INFO:slack_okta_bot:Logging to stdout
⚡️ Bolt app is running! (development server)
127.0.0.1 - - [23/Dec/2022 12:11:02] "POST /slack/events HTTP/1.1" 200 -
```

If you need to import and run from your own script:

```python
from slack_okta_bot import run_local

# do cool stuff

run_local()

```

## Slack App
To install in Slack:

* Update slack-okta-bot.yaml with the domain you will be using
* Update any other options you would like to change
* Go to applications in your Slack org's admin area (https://api.slack.com/apps)
* Click the "Create New App" button
* Click "From an app manifest"
* Select workspace to install to
* Make sure that "YAML" tab is selected
* Under "Basic Information" save your Signing Secret so you can export it to the required env var
* Get the Bot User Oauth Token from the "Oauth & Permissions" tab so you can export it to the required env var
* Deploy your application backend
* In the Slack app configuration page go to "Event Subscriptions"
* If the Request URL is not marked as "Verified" click the verify button/link

Your app's homepage should now show and commands will become active. Test by entering a slash command in any channel in slack. Your interaction with the bot will be private and won't be displayed to other users in the chat. If the application is installed into the Apps side pane in Slack then you can also access the app's home page to see the description and available commands.
