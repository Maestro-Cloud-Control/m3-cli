"""
The custom logic for the command m3 report.
This logic is created to convert parameters from the Human readable format to
appropriate for M3 SDK API request.
"""
import json
from m3cli.services.request_service import BaseRequest

from m3cli.plugins.utils.plugin_utilities import processing_report_format
from m3cli.utils.utilities import timestamp_to_iso
from m3cli.plugins import parse_and_set_date_range


def create_custom_request(request: BaseRequest) -> BaseRequest:
    """ Transform 'total-report' command parameters from the Human
    readable format to appropriate for M3 SDK API request.

    :param request: Dictionary with command name, api action, method and
    parameters
    :type request: BaseRequest
    """
    processing_report_format(request)
    parse_and_set_date_range(request.parameters)

    params = request.parameters
    params['target'] = {
        'tenantGroup': params.pop('tenantGroup'),
        'reportUnit': 'TENANT_GROUP'
    }
    target = params['target']
    if params.get('onlyAdjustments'):
        target.update({
            'onlyAdjustments': params.pop('onlyAdjustments'),
        })

    if params.get('clouds'):
        target.update({
            'clouds': params.pop('clouds'),
            'reportUnit': 'TENANT_GROUP_AND_CLOUD'
        })
    elif params.get('region'):
        target.update({
            'region': params.pop('region'),
        })
    return request


def create_custom_response(
        request,
        response,
        view_type: str,
):
    """ Transform the command 'total-report' response from M3 SDK API
    to the more human readable format.

    :param response: Server response with data as a string representation
    of a dictionary
    """
    try:
        response = json.loads(response)
    except json.decoder.JSONDecodeError:
        return response

    if response.get('message') and response.get('s3ReportLink'):
        return f"{response.get('message')} Link: `{response.get('s3ReportLink')}`"

    response_processed = []
    grand_total = response.get('grandTotal')
    if isinstance(grand_total, (float, int)):
        for each_row in response.get('records'):
            if each_row.get('billingPeriodStartDate'):
                each_row['billingPeriodStartDate'] = \
                    timestamp_to_iso(each_row.get('billingPeriodStartDate'))
            if each_row.get('billingPeriodEndDate'):
                each_row['billingPeriodEndDate'] = \
                    timestamp_to_iso(each_row.get('billingPeriodEndDate'))
            response_processed.append(each_row)
        response_processed.append({
            'recordType': 'grandTotal',
            'totalPrice': grand_total,
            'currencyCode': 'USD',
        })
        return response_processed
    if response.get('message'):
        return response.get('message')
    return response
