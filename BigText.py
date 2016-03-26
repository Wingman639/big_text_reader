import sublime, sublime_plugin

PAGE_SIZE = 10000
SHOW_AHEAD_SIZE = 100

class TextCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        filePath, start, searchKey = self.getParameters()
        text = self.loadTextFromFile(filePath)
        self.insertText(edit, '\n\n')
        if searchKey:
            i = text.find(searchKey, start)
            start = self.getStartPointSeveralLinesAhead(text, start, i)
        end = min(len(text), start + PAGE_SIZE)
        self.insertText(edit, text[start:end])

    def getParameters(self):
        filePath = self.view.substr(self.view.line(0))
        i = len(filePath) + 1
        print(filePath)
        startStr = self.view.substr(self.view.line(i))
        print(startStr)
        i += len(startStr) + 1
        searchKey = self.view.substr(self.view.line(i))
        print(searchKey)
        return filePath, int(startStr), searchKey

    def getStartPointSeveralLinesAhead(self, text, start, keyMatchPoint):
        if keyMatchPoint <= 0:
            return start
        if keyMatchPoint <= SHOW_AHEAD_SIZE:
            return start
        i = keyMatchPoint - SHOW_AHEAD_SIZE
        i = text.rfind('\n', 0, i)
        if i > 0:
            return i


    def insertText(self, edit, text):
        self.view.insert(edit, self.view.size(), text)

    def loadTextFromFile(self, filePath):
        with open(filePath, 'r') as f:
            return f.read()