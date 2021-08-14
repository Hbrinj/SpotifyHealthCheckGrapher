import lxml.html as lh
from Confluence import Confluence
from HealthCheck import Result
from HealthCheck import HealthCheck
from datetime import datetime

class HealthCheckParser:
    questions = [
        "",
        "Easy To release",
        "Suitable Process",
        "Tech Quality",
        "Value",
        "Speed",
        "Mission",
        "Fun",
        "Learning",
        "Support",
        "Pawns or Players"
        ]

    def __init__(self, config):
        self.config = config
        self.confluence = Confluence(self.config.username, self.config.api_key, self.config.confluenceURL, self.config.cloud)

    def __getTable(self, html): 
        doc = lh.fromstring(html)
        return doc.xpath('//tr')

    def __getPageChildList(self, parent_page_id):
        return self.confluence.conf.get_child_id_list(parent_page_id)

    def __getPage(self, page_id):
        return self.confluence.conf.get_page_by_id(page_id, expand='body.storage')

    def __getPageBody(self, page):
        return page.get('body').get('storage').get('value')

    def __averageScore(self, row):
        countOfViableScores = 0
        scoresTotal = 0
        for col in range(1, len(row)):
            content = row[col].text_content()
            if (content):
                try:
                    value = int(content)
                    countOfViableScores += 1
                    scoresTotal += value
                except:
                    print("found non int value")

        return scoresTotal/countOfViableScores

    def getHealthChecks(self):
        hcs = []
        childrenIDs = self.__getPageChildList(self.config.parent_page_id)

        for childID in childrenIDs:
            page = self.__getPage(childID)
            pageTitle = page.get('title')
            timestamp = datetime.fromisoformat(pageTitle)
            table = self.__getTable(self.__getPageBody(page))
            results = []
            for row in range(1, len(table)):
                results.append(Result(self.questions[row], self.__averageScore(table[row])))

            hcs.append(HealthCheck(timestamp,results))

        return hcs