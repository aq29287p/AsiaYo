import json
from typing import Union, Dict, List

from flask import Response


def api_response(
        http_status: int = 200,
        data: Union[dict, list] = None,
        message: str = None,
        http_headers: Dict[str, Union[str, List[str]]] = None,
        **kwargs
) -> Response:
    """API Response"""
    http_status = int(http_status)
    payload = {**kwargs}
    if isinstance(data, (dict, list)):
        payload['data'] = data
    if message:
        payload['message'] = message

    http_headers = {**http_headers} if isinstance(http_headers, dict) else {}
    http_headers['Content-Type'] = 'application/json; charset=utf-8'

    return Response(
        json.dumps(payload, ensure_ascii=False),
        http_status,
        http_headers
    )