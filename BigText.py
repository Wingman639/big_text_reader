import sublime, sublime_plugin

PAGE_SIZE = 10000

class TextCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        filePath, start, searchKey = self.getParameters()
        text = self.loadTextFromFile(filePath)
        self.insertText(edit, '\n\n')
        if searchKey:
            i = text.find(searchKey, start)
            if i > 0:
                start = i
        self.insertText(edit, text[start:min(len(text), PAGE_SIZE)])

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


    def insertText(self, edit, text):
        self.view.insert(edit, self.view.size(), text)

    def loadTextFromFile(self, filePath):
        with open(filePath, 'r') as f:
            return f.read()