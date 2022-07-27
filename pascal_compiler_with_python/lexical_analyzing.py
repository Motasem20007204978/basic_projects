import re
from token_info import Token

class LexeicalAnalyzer:

    _booked = [
        {'Name': 'tk_program', 'Value': 'program'},
        {'Name': 'tk_begin', 'Value': 'begin'},
        {'Name': 'tk_end', 'Value': 'end'},
        {'Name': 'tk_var', 'Value': 'var'},
        {'Name': 'tk_array', 'Value': 'array'},
        {'Name': 'tk_of', 'Value': 'of'},
        {'Name': 'tk_int_type', 'Value': 'integer'},
        {'Name': 'tk_bool_type', 'Value': 'boolean'},
        {'Name': 'tk_real_type', 'Value': 'real'},
        {'Name': 'tk_string_type', 'Value': 'string'},
        {'Name': 'tk_proc', 'Value': 'procedure'},
        {'Name': 'tk_func', 'Value': 'function'},
        {'Name': 'tk_for', 'Value': 'for'},
        {'Name': 'tk_while', 'Value': 'while'},
        {'Name': 'tk_not', 'Value': 'not'},
        {'Name': 'tk_do', 'Value': 'do'},
        {'Name': 'tk_if', 'Value': 'if'},
        {'Name': 'tk_then', 'Value': 'then'},
        {'Name': 'tk_else', 'Value': 'else'},
        {'Name': 'tk_read', 'Value': 'read'},
        {'Name': 'tk_read_ln', 'Value': 'readln'},
        {'Name': 'tk_write', 'Value': 'write'},
        {'Name': 'tk_write_ln', 'Value': 'write_ln'},
        {'Name': 'tk_left_sq_pracket', 'Value': '['},
        {'Name': 'tk_right_sq_pracket', 'Value': ']'},
        {'Name': 'tk_le', 'Value': '<='},
        {'Name': 'tk_ge', 'Value': '>='},
        {'Name': 'tk_ne', 'Value': '<>'},
        {'Name': 'tk_lt', 'Value': '<'},
        {'Name': 'tk_gt', 'Value': '>'},
        {'Name': 'tk_eq', 'Value': '='},
        {'Name': 'tk_in', 'Value': 'in'},
        {'Name': 'tk_assign_op', 'Value': ':='},
        {'Name': 'tk_plus', 'Value': '+'},
        {'Name': 'tk_minus', 'Value': '-'},
        {'Name': 'tk_or', 'Value': 'or'},
        {'Name': 'tk_mul', 'Value': '*'},
        {'Name': 'tk_div', 'Value': 'div'},
        {'Name': 'tk_mod', 'Value': 'mod'},
        {'Name': 'tk_and', 'Value': 'and'},
        {'Name': 'tk_left_paren', 'Value': '('},
        {'Name': 'tk_right_paren', 'Value': ')'},
        {'Name': 'tk_colon', 'Value': ':'},
        {'Name': 'tk_comma', 'Value': ','},
        {'Name': 'tk_simi_colon', 'Value': ';'},
        {'Name': 'tk_dot', 'Value': '.'},
    ]

    def __init__(self) -> None:
        self.__booked_tokens = __class__._booked
        self.__symbol_list = []
        
        
    def __implementLexemes(self, line: str, lineNo: int) -> list:
        """_summary_

        Args:
            chars (str): _description_
            parameter might be a block of mixed lexemes such as a:=5;
            this method split the block to basic lexemes:
                alpha lexemes such as 'a' appended to lexemes list
                non-alpha lexemes such as ':=' appended to lexemes list
                numeric lexemes such as '5' appended to lexemes list
                non-alpha lexemes such as ';' appended to lexemes list

        Returns:
            list: _description_
            add all three lists of lexemes together in one list
        """

        lexemes = []

        def exportLexeme(line: str, pattern: str) -> str:
            """_summary_

            Args:
                line (str): to export lexeme from
                pattern (str): re pattern for exporting lexemes
                patterns for alpha, non-alpha, numerical characters

            Returns:
                str: return the remain not checked characters from the line
            """

            lexeme = re.search(pattern, line)
            if lexeme:
                lexemes.append(lexeme[0])
                line = line[len(str(lexeme[0])):]

            return line

        while line:

            rel_op = list(filter(line.startswith, [':=', '<=', '>=', '<>']))
            if rel_op:
                lexemes.append(rel_op[0])
                line = line[len(str(rel_op[0])):]  # index 2 and -->

            if line.startswith('"') or line.startswith("'"):
                try:
                    line = exportLexeme(line, r'^".*"|^\'.*\'')
                except:
                    print('Error: Lexical Error at line {}'.format(lineNo) + '\n' + 
                        line  + '\n' + ' ' * (len(line) + 1) + 
                        '^' + '\n' + 'Lexical Error: Unrecognized token' + '\n'  
                        + ' ' * (len(line) + 1) + '^')
                    exit()
            
            # if start with numbers
            if re.search(r'^[0-9]', line):
                line = exportLexeme(line, r'^[0-9]+')
                if line.startswith('.'):
                    lexemes[-1] += '.'
                    line = line[1:]
                    if not re.search(r'^[0-9]', line):
                        print('Error: invalid number format at line {}'.format(lineNo))
                        exit(1)
                    lexemes[-1] += re.search(r'^[0-9]+', line)[0]
                    line = line[len(str(re.search(r'^[0-9]+', line)[0])):]

            line = exportLexeme(line=line, pattern=r'^[a-z_]\w*')
            
            # if white spaces
            white_space = re.search(r'^\s+', line)
            if white_space:
                line = line[1:]
            
            if not white_space:
                line = exportLexeme(line=line,
                                pattern=r'^[\W]')  # non-alpha lexemes

        return lexemes

    def __getToken(self, lexeme: str, lineNo: int) -> Token:
        """_summary_

        Args:
            token (str): _description_ 
            lineNo (int): _description_
            checks each elements from list that returned from splitWord method
            give each elements a type related to 
        Returns:
            dict: _description_
            return token as dictionary consists of name, type, line number in code files
        """

        for booked_token in self.__booked_tokens:
            if booked_token['Value'] == lexeme:
                record = Token(Name=booked_token['Name'], Value=lexeme, lineNo=lineNo)
                return record

        # search string
        if re.search(r'^".*"|^\'.*\'', lexeme):
            return Token(Name='tk_string', Value=lexeme, lineNo=lineNo)
        if re.search(r'^[a-z_][\w]*$', lexeme):
            return Token(Name='tk_id', Value=lexeme, lineNo=lineNo)

        if re.search(r'^[0-9]+$|^[0-9]+\.[0-9]+$', lexeme):
            return Token(Name='tk_num', Value=lexeme, lineNo=lineNo)
        
        print('Error: Lexical Error at line {}'.format(lineNo) + '\n' + 
            lexeme  + '\n' + ' ' * (len(lexeme) + 1) + 
            '^' + '\n' + 'Lexical Error: Unrecognized token' + '\n'  
            + ' ' * (len(lexeme) + 1) + '^')
        exit()

    def __parseLine(self, line: str, lineNo: int) -> None:
        """_summary_
            splits the line into sequence of blocks
            calls splitWord method to devide analyze each block
            gets token information for each element returned by splitWord method
            adds these information in a dictionary to compose a table of tokens information  
        """

        for lexeme in self.__implementLexemes(line=line, lineNo=lineNo):
            record = self.__getToken(lexeme, lineNo)
            self.__symbol_list.append(record)
            # self.__linkedList._add(record)

    def _scan(self) -> None:

        with open(file='pascalcode.txt', mode='r') as code:

            for lineNo, line in enumerate(code.readlines(), 1):

                # remove comments
                line = re.sub(r'(\{.*?\})', '', line)
                line = re.sub(r'(\(\*.*?\*\))', '', line)

                # convert to lower case and remove spaces
                line = line.lower().strip()

                #  ignore empty lines
                if line:
                    self.__parseLine(line=line, lineNo=lineNo)
                
            code.close()


    def __str__(self): 
        _str = '\n' + '=' * 100 + '\n'
        _str += 'Token Table\n'
        _str += '=' * 100 + '\n'
        _str += 'Name'.ljust(20) + '| Value'.ljust(50) + '| Line No.' + '\n'
        _str += '-' * 100 + '\n'

        for record in self.__symbol_list:
            _str += record._getName().ljust(20) + '| ' + record._getValue().ljust(50) + '| ' + str(record._getLineNo()) + '\n'
            _str += '-' * 100 + '\n'
        
        return _str

    # yields the next token in the file
    def __iter__(self):
        return self
    
    # returns the next token in the file
    def __next__(self):
        if self.__index >= len(self.__symbol_list):
            raise StopIteration
        else:
            self.__index += 1
            return self.__symbol_list[self.__index - 1]

    def __getitem__(self, index):
        return self.__symbol_list[index]
    
    def __len__(self):
        return len(self.__symbol_list)

    # return list of tokens
    def _getTokens(self):
        return self.__symbol_list
    
