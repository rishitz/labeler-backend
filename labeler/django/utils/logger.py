import logging

from slack_sdk.webhook import WebhookClient

from labeler import settings


class SlackLoggingHandler(logging.Handler):
    """
    Custom logging handler to send error logs to Slack.
    """

    def emit(self, record):
        if not settings.SLACK_WEBHOOK_URL or not settings.ENABLE_SLACK_ALERTS:
            return

        try:
            message = self.format(record)
            webhook = WebhookClient(settings.SLACK_WEBHOOK_URL)
            webhook.send(text=f":warning: *Server Error Notification*\n```{message}```")
        except Exception as e:
            logging.error(f"Failed to send Slack alert: {e}")
