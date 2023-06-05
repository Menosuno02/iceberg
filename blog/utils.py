"""
    Fix request.is_ajax() deprecated in django > v3.1
    Args: request (request)
    Returns: _type_: boolean
"""


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
