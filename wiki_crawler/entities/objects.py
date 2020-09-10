class Link:
    """object Link from wiki"""
    def __init__(self, title, url):
        self.title = title
        self.url = url

    def print(self):
        print('{} : {}'.format(self.title, self.url))