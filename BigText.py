import sublime, sublime_plugin

SHOW_AHEAD_SIZE = 100

class TextCommand(sublime_plugin.TextCommand):
    parameterBegin = None
    parameterEnd = None
    def run(self, edit):
        parameters = self.getParameters()
        filePath = parameters['path']
        needContinue = parameters['needContinue']
        appendingBegin = parameters['appendingBegin']
        appendingEnd = parameters['appendingEnd']

        text = self.loadTextFromFile(filePath)

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
            self.appendText(edit, text[start:end])

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
        parametersEndRegion = self.view.find(r'\}', 0)
        self.parameterBegin = parametersBeginRegion.a
        self.parameterEnd = parametersEndRegion.b
        parametersRegion = sublime.Region(self.parameterBegin, self.parameterEnd)
        parametersStr = self.view.substr(parametersRegion)
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

    def updateParameters(self, edit, parameters, start, end):
        parameters['appendingBegin'] = start
        parameters['appendingEnd'] = end
        self.view.replace(edit,
                          sublime.Region(self.parameterBegin, self.parameterEnd),
                          str(parameters) + '\n\n')

    '''
    def dictStr(self, parameters):
        ' ''
        {
        'path': '/Users/wingman/GitHub/big_text_reader/xml/example_400M.XML',
        'pageSize': 1000,
        'start': 0,
        'needContinue': True,
        'appendingBegin': None,
        'appendingEnd': None,
        'searchKey': None,
        'searchFrom': None,
        }
        ' ''
        items = ['{', '\n',
                'path: ', parameters['path'], ',\n',
                'pageSize: ', str(parameters['pageSize']), ',\n',
                'start: ', str(parameters['start']), ',\n',
                'needContinue: ', str(parameters['needContinue']), ',\n',
                'appendingBegin: ', str(parameters['appendingBegin']), ',\n',
                'appendingEnd: ', str(parameters['appendingEnd']), ',\n',
                'searchKey: ', str(parameters['searchKey']), ',\n',
                'searchFrom: ', str(parameters['searchFrom']), ',\n',
                '}',
                ]
        return ''.join(items)
    '''

    def insertText(self, edit, position, text):
        self.view.insert(edit, position, text)

    def appendText(self, edit, text):
        self.view.insert(edit, self.view.size(), text)

    def loadTextFromFile(self, filePath):
        with open(filePath, 'r') as f:
            return f.read()




'''
{'needContinue': True,
'path': '/Users/wingman/GitHub/big_text_reader/xml/small.XML',
'searchKey': '',
'searchFrom': 0,
'appendingEnd': None,
'start': 0,
'pageSize': 10000,
'appendingBegin': None}
'''