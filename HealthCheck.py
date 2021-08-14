
class Result:
    def __init__(self, question, avgAnswer):
        self.question = question
        self.avgAnswer = avgAnswer
    
    def getQuestion(self):
        return self.question

    def getAvgAnswer(self):
        return self.avgAnswer

class HealthCheck:
    def __init__(self, timestamp, results):
        self.results = results
        self.timestamp = timestamp

    def getResults(self):
        return self.results

    def getScores(self):
        return [T.getAvgAnswer() for T in self.results]

    def getQuestions(self):
        return [T.getQuestion() for T in self.results]

    def getTimestamp(self):
        return self.timestamp