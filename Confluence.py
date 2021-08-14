from atlassian import Confluence as cf

class Confluence:
    def __init__(self, username, api_key, url, cloud):
        self.conf = cf(
            url=url,
            username=username,
            password=api_key,
            cloud=cloud
        )