from syntax_analyzing import SyntaxAnalyzer
from lexical_analyzing import LexeicalAnalyzer


def main():

    # object of LexeicalAnalyzer class to analyze file lines to tokens
    # the table information is filled with tokens in the processes inside this class
    lexer = LexeicalAnalyzer()
    lexer._scan()
    print(lexer)

    # object of SyntaxAnalyzer class to analyze tokens to syntax
    parser = SyntaxAnalyzer(list_of_tokens=lexer._getTokens())
    parser._parse()


if __name__ == '__main__':
    main()
    pass
# end of file