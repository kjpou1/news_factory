from urllib.parse import urljoin


class Utils:
    @staticmethod
    def create_full_url(base_url, href):
        return urljoin(base_url, href)
