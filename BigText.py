import sublime, sublime_plugin

SHOW_AHEAD_SIZE = 100

class TextCommand(sublime_plugin.TextCommand):
    parameterBegin = None
    parameterEnd = None
    showBegin = None
    showEnd = None

    def run(self, edit):
        parameters = self.getParameters()

        text = self.loadTextFromFile(parameters['path'])

        if parameters['needContinue']:
            start = self.getStartPointWithContinue(parameters, text)
        else:
            start = self.getStartPoint(parameters, text)
        end = min(len(text), start + parameters['pageSize'])

        #self.view.replace(edit, startRegion, str(start))
        if parameters['needContinue']:
            self.updateParameters(edit, parameters, start, end)

        if parameters['searchKey']:
            self.updateSearchOutput(edit, parameters, text[start:end])
        else:
            self.updateOutput(edit, parameters, text[start:end])

    def getStartPoint(self, parameters, text):
        if parameters['searchKey']:
            return self.getStartWithSearch(parameters, text)
        return parameters['start']

    def getStartPointWithContinue(self, parameters, text):
        if parameters['searchKey']:
            return self.getStartWithSearch(parameters, text)
        else:
            if parameters['appendingEnd']:
                return parameters['appendingEnd']
        return parameters['start']


    def getStartWithSearch(self, parameters, text):
        i = text.find(parameters['searchKey'], parameters['searchFrom'])
        #start = self.getStartPointSeveralLinesAhead(text, parameters['searchFrom'], i)
        start = i
        parameters['searchFrom'] = i + 1
        return start


    def getParameters(self):
        parametersBeginRegion = self.view.find(r'\{', 0)
        parametersEndRegion = self.view.find(r'\}', parametersBeginRegion.a)
        parametersRegion = sublime.Region(parametersBeginRegion.a, parametersEndRegion.b)
        parametersStr = self.view.substr(parametersRegion)

        self.parameterBegin = parametersBeginRegion.a
        self.parameterEnd = parametersEndRegion.b
        self.showBegin = min(self.parameterEnd + 2, self.view.size())
        self.showEnd = self.view.size()
        return eval(parametersStr)


    def getStartPointSeveralLinesAhead(self, text, start, keyMatchPoint):
        if keyMatchPoint <= 0:
            return start
        if keyMatchPoint <= SHOW_AHEAD_SIZE:
            return start
        i = keyMatchPoint - SHOW_AHEAD_SIZE
        i = text.rfind('\n', 0, i)
        if i > 0:
            return i


    def updateSearchOutput(self, edit, parameters, text):
        outputRegion = sublime.Region(len(str(parameters)) + 2, self.view.size())
        self.view.replace(edit, outputRegion, text)


    def updateOutput(self, edit, parameters, text):
        if parameters['needContinue']:
            self.appendText(edit, text)
        else:
            showRegion = sublime.Region(self.showBegin, self.showEnd)
            self.view.replace(edit, showRegion, text)


    def updateParameters(self, edit, parameters, start, end):
        parameters['appendingBegin'] = start
        parameters['appendingEnd'] = end
        text = self.formartDictStr(str(parameters))
        print(str(parameters))
        print(text)
        self.view.replace(edit,
                          sublime.Region(self.parameterBegin, self.parameterEnd),
                          text)


    def formartDictStr(self, dictStr):
        return dictStr.replace(',', ',\n').replace('{', '{\n').replace('}', '\n}')


    def insertText(self, edit, position, text):
        self.view.insert(edit, position, text)


    def appendText(self, edit, text):
        self.view.insert(edit, self.view.size(), text)


    def loadTextFromFile(self, filePath):
        with open(filePath, 'r') as f:
            return f.read()




'''
{
'searchFrom': None,
 'start': 0,
 'searchKey': '',
 'path': '/Users/wingman/GitHub/big_text_reader/xml/small.xml',
 'needContinue': True,
 'appendingBegin': None,
 'appendingEnd': None,
 'pageSize': 300
}
'''