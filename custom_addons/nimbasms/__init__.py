# -*- coding: utf-8 -*-

import os
import logging

from . import tools
from . import models
from . import controllers


_logger = logging.getLogger(__name__)

__all__ = [
    'tools',
    'models',
    'controllers',
]


def post_init_hook(env):
    service_id = (os.getenv('NIMBA_SERVICE_ID') or '').strip()
    secret_token = (os.getenv('NIMBA_SECRET_TOKEN') or '').strip()
    sender_name = (os.getenv('NIMBA_SENDER_NAME') or '').strip()
    webhook_secret = (os.getenv('NIMBA_WEBHOOK_SECRET') or '').strip()

    if webhook_secret:
        env['ir.config_parameter'].sudo().set_param(
            'sms.nimba_webhook_secret',
            webhook_secret,
        )

    if not (service_id and secret_token and sender_name):
        _logger.info(
            "Nimba SMS: NIMBA_SERVICE_ID / NIMBA_SECRET_TOKEN "
            "/ NIMBA_SENDER_NAME not fully set; "
            "skipping auto-configuration."
        )
        return

    companies = env['res.company'].sudo().search([])
    for company in companies:
        company.write({
            'sms_provider': 'nimba',
            'sms_nimba_service_id': service_id,
            'sms_nimba_secret_token': secret_token,
            'sms_nimba_sender_name': sender_name,
        })
