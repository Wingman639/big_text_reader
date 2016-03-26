import sublime, sublime_plugin

PAGE_SIZE = 10000

class TextCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        filePath, start = self.getParameter()
        text = self.loadTextFromFile(filePath)
        self.insertText(edit, '\n\n')
        self.insertText(edit, text[start:min(len(text), PAGE_SIZE)])

    def getParameter(self):
        filePath = self.view.substr(self.view.line(0))
        startStr = self.view.substr(self.view.line(len(filePath) + 1))
        print(filePath)
        print(startStr)
        return filePath, int(startStr)


    def insertText(self, edit, text):
        self.view.insert(edit, self.view.size(), text)

    def loadTextFromFile(self, filePath):
        with open(filePath, 'r') as f:
            return f.read()