"""
The custom logic for the command m3 describe-tenants.
This logic is created to convert parameters from the Human readable format to
appropriate for M3 SDK API request; wraps tag key
"""
import json

from m3cli.utils.utilities import timestamp_to_iso


def create_custom_request(request):
    params = request.parameters
    if params.get('hidden') and params.get('inactive'):
        raise AssertionError(
            '\'hidden\' and \'inactive\' parameters cannot be both specified')
    return request


def create_custom_response(request, response):
    try:
        response = json.loads(response)
    except json.decoder.JSONDecodeError:
        return response
    for each in response:
        tenant_group = each.get('tenantGroup')
        tenant_name = each.get('tenantName')
        if tenant_group and tenant_group != tenant_name:
            each['parentTenant'] = each.pop('tenantGroup')

        if each.get('activationDate'):
            each['activationDate'] = timestamp_to_iso(each.get('activationDate'))
    return response
