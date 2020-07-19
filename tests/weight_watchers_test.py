import weight_watchers


def test_get_endpoints_from_file():
    fp = 'endpoints/endpoints.json'
    req_list = weight_watchers.get_endpoints_from_file(fp)
    assert len(req_list) != 0


def test_request_endpoints_test():
    pass


def check_for_success_test():
    pass


def publish():
    pass


def _is_available_test():
    pass


def run():
    pass
