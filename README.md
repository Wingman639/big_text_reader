# big_text_reader
Show big text file quickly.

I need a text file viewer to show big text file content in seconds.

First version is a SublimeText 3 plugin.
line 1: file path
line 2: start point
page size: 10000 char

How to use it:
1. fill parameters:
{'needContinue': True,
'path': '/Users/wingman/GitHub/big_text_reader/xml/small.XML',
'searchKey': '',
'searchFrom': 0,
'appendingEnd': None,
'start': 0,
'pageSize': 10000,
'appendingBegin': None}

2. Cmd+Alt+T


Keyword will be searched in text, and renew start point to 1st found point.
One page of text from start point of the file will show in SublimeText editer view.