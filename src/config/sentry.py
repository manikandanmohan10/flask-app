import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="https://136687f6f35145abbf197db61f6b95f7@o1423025.ingest.sentry.io/4503981457801216",
    integrations=[
        FlaskIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)
