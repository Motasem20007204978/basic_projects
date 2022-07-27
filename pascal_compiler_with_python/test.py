
from unittest import case
from syntax_analyzing import SyntaxAnalyzer


class Test:
    def __init__(self) -> None:
        self.syntax  = SyntaxAnalyzer()

    def test(self) -> bool:
        return self.syntax.__nextToken()['Type'] == 'identifier'


dic = {
    'name':'motasem',
    'family':'almobayyed',
}

dic.__setitem__('middle', 'anwar')

print(dic)

print(not not not True)

if 1:
    print('motasem', flush=True)
    len('hello')
    print(locals())

if list(filter('block'.startswith, [':=', '<=', '>=', '<>'])):
    print('motasem almobayyed')


print(all(map(lambda x: x == 'Name', 
                ['Name', 'Name'])))

