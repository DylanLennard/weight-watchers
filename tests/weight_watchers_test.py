from src import weight_watchers
from unittest.mock import patch
import vcr

# some vars for use w/ unit tests below
failure_html = "<html><p>nah</p></html>"
success_html = f'''
    <html>
        <p class="ship-mode-message">
        {weight_watchers.IN_STOCK_MSG}
        </p>
    </html>
    '''
req_list = [
    {
        "size": "25",
        "url": "https://www.dickssportinggoods.com/p/ethos-25-" +
               "lbolympic-rubber-bumper" +
               "-plate-17au6uthsbmprpltswplb/17au6uthsbmprpltswplb"},
    {
        "size": "35",
        "url": "https://www.dickssportinggoods.com/p/ethos-35-" +
               "lbolympic-rubber-bumper-plate-" +
               "17au6uthsbmprpltswplc/17au6uthsbmprpltswplc"
    }
]


def test_get_endpoints_from_file():
    fp = 'endpoints/endpoints.json'
    req_list = weight_watchers.get_endpoints_from_file(fp)
    assert len(req_list) != 0


@vcr.use_cassette("tests/fixtures/test_request_endpoints.yaml")
def test_request_endpoints():
    res = weight_watchers.request_endpoints(req_list)
    for result in res:
        assert "response" in result


def test_check_for_success_test():
    res_list = [{'response': success_html}, {'response': failure_html}]
    res_list = weight_watchers.check_for_success(res_list)
    for res in res_list:
        assert 'available' in res


def test_is_available():
    assert weight_watchers.is_available(success_html)
    assert not weight_watchers.is_available(failure_html)


@patch('src.weight_watchers.boto3.client')
def test_publish(mock_client):
    res_list = req_list

    # one successful message, one failure message
    res_list[0]['available'] = True
    res_list[1]['available'] = False

    weight_watchers.QA = False
    weight_watchers.publish(res_list)

    mock_client.assert_called_once_with('sns')
    mock_client.return_value.publish.assert_called_once()
