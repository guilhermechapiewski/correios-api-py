import requests
from bs4 import BeautifulSoup


class RoyalMail(object):

    def __init__(self):
        self.url = "http://www.royalmail.com/trackdetails"
        self.op = "Track item"
        self.form_id = "bt_tracked_track_trace_form"

    def _get_infos(self, track_id):
        response = requests.post(self.url, data={
                                                 'tracking_number': track_id,
                                                 'op': self.op,
                                                 'form_id': self.form_id
                                                 })
        soup = BeautifulSoup(response.text)
        table = soup.table
        results = []
        items = table.find_all('td')
        for item in items:
            results.append(item.text)

        return results

    def get(self, track_id):
        items = self._get_infos(track_id)
        result = []
        key = ['data', 'hora', 'status', 'local']
        count = 0
        data = dict()

        for item in items:
            if count < 4:
                data[key[count]] = item
                count += 1
            else:
                result.append(data)
                count = 0

        return result
