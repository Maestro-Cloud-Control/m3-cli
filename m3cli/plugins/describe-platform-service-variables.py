"""The custom logic for the command m3 describe-platform-service-variables.py"""
import json
from typing import Any

from m3cli.services.request_service import BaseRequest


def create_custom_request(
        request: BaseRequest,
        # view_type: str | None = None,
) -> BaseRequest:
    params = request.parameters
    if not params.get('all'):
        params['all'] = False
    return request


def create_custom_response(
        request: BaseRequest,
        response: str,
        # view_type: str | None = None,
) -> list[dict[str, Any]]:
    """
    Transform the command 'describe-platform-service-variables' response from M3 SDK
    API to a human-readable key-value format.

    :param request: Original CLI request
    :param response: Server response as a JSON string containing 'serviceId'
    and 'params' fields
    :return: List of dicts with 'parameter' and 'value' keys, one entry per param
    """
    try:
        response_data = json.loads(response)
    except (json.decoder.JSONDecodeError, TypeError):
        return [{"parameter": "raw_response", "value": str(response)}]

    if not isinstance(response_data, dict):
        return [{"parameter": "raw_response", "value": str(response_data)}]

    service_id = response_data.get('serviceId', 'N/A')
    params = response_data.get('params', {})

    if not params:
        return [{
            "serviceId": service_id,
            "parameter": "N/A",
            "value": "No params found",
        }]

    return [
        {
            "serviceId": service_id,
            "parameter": key,
            "value": str(value) if value is not None else "",
        }
        for key, value in params.items()
    ]
