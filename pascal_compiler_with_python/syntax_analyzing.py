class SyntaxAnalyzer:
    def __init__(self, list_of_tokens) -> None:

        # yield from list_of_tokens
        def _yield_from_list_of_tokens(list_of_tokens):
            for token in list_of_tokens:
                yield token

        self.tokens = _yield_from_list_of_tokens(list_of_tokens)
        self.currentToken = next(self.tokens)

        self.previousToken = self.currentToken
        self.currentState = str()
        self.currentScope = 0

    def __nextToken(self):

        try:
            self.previousToken = self.currentToken
            self.currentToken = next(self.tokens)
        except StopIteration:
            self.currentToken = None
            return

    def _parse(self):
        self.__program()
        print("this program is in th right syntax")
        pass

    def __program(self):
        self.currentScope += 1
        self.__match("tk_program")
        self.__match("tk_id")
        self.__match("tk_simi_colon")
        self.__declarations()
        self.__subprogram_declarations()
        self.__compound_stmt()
        self.__match("tk_dot")

    def __declarations(self):
        if self.currentToken._getName() == "tk_var":
            self.__nextToken()
            self.__list_ids_same_type()
            self.__match("tk_simi_colon")
            self.__declarations()
        ...

    def __list_ids_same_type(self):
        self.__identifier_list()
        self.__match("tk_colon")
        self.__type()

    def __identifier_list(self):
        self.__match("tk_id")
        if self.currentToken._getName() == "tk_comma":
            self.__nextToken()
            self.__identifier_list()
        pass

    def __type(self):
        self.currentState = "type name"
        if self.__sd_type():
            return
        elif self.currentToken._getName() == "tk_array":
            self.__nextToken()
            self.__match("tk_left_sq_pracket")
            self.__match("tk_num")
            self.__match("tk_dot")
            self.__match("tk_dot")
            self.__match("tk_num")
            self.__match("tk_right_sq_pracket")
            self.__match("tk_of")
            self.__sd_type()
            return
        self.__error()

    def __sd_type(self):
        if self.currentToken._getName() in [
            "tk_string_type",
            "tk_int_type",
            "tk_bool_type",
            "tk_real_type",
        ]:
            self.__nextToken()
            return True
        self.__error()

    def __subprogram_declarations(self):
        if not self.currentToken._getName() == "tk_begin":  # not compound_stmt
            self.__subprogram_declaration()
            self.__match("tk_simi_colon")
            self.__subprogram_declarations()
        pass

    def __subprogram_declaration(self):
        self.__subprogeram_head()
        self.__declarations()
        self.__compound_stmt()

    def __subprogeram_head(self):
        if self.currentToken._getName() == "tk_func":
            self.__nextToken()
            self.__function()
            return
        elif self.currentToken._getName() == "tk_proc":
            self.__nextToken()
            self.__procedure()
            return

        self.__error()

    def __function(self):
        self.__match("tk_id")
        if self.currentToken._getName() == "tk_left_paren":
            self.__arguments(inProcedureStmt=False)
        self.__match("tk_colon")
        self.__sd_type()
        self.__match("tk_simi_colon")

    def __procedure(self):
        self.__match("tk_id")
        self.__arguments(inProcedureStmt=True)
        self.__match("tk_simi_colon")

    def __arguments(self, inProcedureStmt: bool):
        self.__match("tk_left_paren")
        if not self.currentToken._getName() == "tk_right_paren":
            self.__parameter_list(inProcedureStmt=inProcedureStmt)
        self.__match("tk_right_paren")
        pass

    def __parameter_list(self, inProcedureStmt: bool):
        if self.currentToken._getName() == "tk_var" and inProcedureStmt:
            # new declaration for new variable/s
            self.__nextToken()

        self.__list_ids_same_type()
        if self.currentToken._getName() == "tk_simi_colon":
            self.__nextToken()
            self.__parameter_list(inProcedureStmt=inProcedureStmt)
        pass

    def __compound_stmt(self):
        self.__match("tk_begin")
        self.__optional_stmts()
        self.__match("tk_end")
        pass

    def __optional_stmts(self):
        if not self.currentToken._getName() == "tk_end":
            self.__stmt()
            self.__optional_stmts()
        pass

    def __stmt(self):

        if self.currentToken._getName() == "tk_id":
            self.__var_proc_stmt()
            self.__match("tk_simi_colon")
            return

        if self.currentToken._getName() == "tk_begin":
            self.__compound_stmt()
            self.__match("tk_simi_colon")
            return

        if self.currentToken._getName() == "tk_if":
            self.__if_stmt()
            return

        if self.currentToken._getName() == "tk_while":
            self.__while_stmt()
            return

        if self.currentToken._getName() == "tk_for":
            self.__for_stmt()
            return

        if self.currentToken._getName() in ["tk_read", "tk_read_ln"]:
            self.__read_stmt()
            self.__match("tk_simi_colon")
            return

        if self.currentToken._getName() in ["tk_write", "tk_write_ln"]:
            self.__write_stmt()
            self.__match("tk_simi_colon")
            return

        self.__error()

    def __var_proc_stmt(self):
        # dont know if it is an arithmatic process or a procedure call
        self.__nextToken()
        # variable statement
        if self.currentToken._getName() == "tk_assign_op":
            self.__nextToken()
            self.__exp()
            return

        # procedure call statement or sunction
        if self.currentToken._getName() == "tk_left_paren":
            self.__nextToken()
            self.__exp_list()
            self.__match("tk_right_paren")
            return

        self.__error()

    def __exp_list(self):
        if not self.currentToken._getName() == "tk_right_paren":
            self.__exp()
            if self.currentToken._getName() == "tk_comma":
                self.__nextToken()
                self.__exp_list()
        pass

    def __if_stmt(self):
        self.__nextToken()
        self.__match("tk_left_paren")
        self.__exp()
        self.__match("tk_right_paren")
        self.__match("tk_then")
        self.__stmt()
        if self.currentToken._getName() == "tk_else":
            self.__nextToken()
            self.__stmt()

    def __for_stmt(self):
        self.__nextToken()
        self.__match("tk_id")
        self.__match("tk_assign_op")
        self.__exp()
        self.__match("tk_to")
        self.__exp()
        self.__match("tk_do")
        self.__stmt()

    def __while_stmt(self):
        self.__nextToken()
        self.__exp()
        self.__match("tk_do")
        self.__stmt()

    def __read_stmt(self):
        self.__nextToken()
        self.__match("tk_left_paren")
        self.__identifier_list()
        self.__match("tk_right_paren")

    def __write_stmt(self):
        self.__nextToken()
        self.__match("tk_left_paren")
        self.__exp()
        self.__match("tk_right_paren")

    def __exp(self):
        self.__simple_exp()
        if self.__rel_op():
            self.__simple_exp()
        pass

    def __rel_op(self) -> bool:
        if self.currentToken._getName() in [
            "tk_eq",
            "tk_ne",
            "tk_lt",
            "tk_gt",
            "tk_le",
            "tk_ge",
            "tk_in",
        ]:
            self.__nextToken()
            return True
        return False

    def __simple_exp(self):
        self.__term()
        if self.__add_op() or self.currentToken._getName() == "tk_assign_op":
            self.__nextToken()
            self.__simple_exp()

        pass

    def __add_op(self) -> bool:
        if self.currentToken._getName() in ["tk_plus", "tk_minus", "tk_or"]:
            return True
        return False

    def __term(self):
        self.__factor()
        if self.__mul_op():
            self.__term()
        pass

    def __mul_op(self) -> bool:
        if self.currentToken._getName() in ["tk_div", "tk_mod", "tk_and", "tk_mul"]:
            self.__nextToken()
            return True
        return False

    def __factor(self):
        if self.currentToken._getName() == "tk_id":
            self.__nextToken()
            if self.currentToken._getName() == "tk_left_paren":  # calling function
                self.__nextToken()
                self.__exp_list()
                self.__match("tk_right_paren")
            return
        elif self.currentToken._getName() == "tk_num":
            self.__nextToken()
            return
        elif self.currentToken._getName() == "tk_string":
            self.__nextToken()
            return
        elif self.currentToken._getName() == "tk_left_paren":
            self.__nextToken()
            self.__exp()
            self.__match("tk_right_paren")
            return
        elif self.currentToken._getName() == "tk_not":
            self.__nextToken()
            self.__factor()
            return

        self.__error()

    def __match(self, expected_type) -> bool:

        if expected_type == self.currentToken._getName():
            # self.currentToken.__setitem__('Scope', self.currentScope)
            self.__nextToken()
            return

        self.__error()
        ...

    def __error(self):
        print(
            f"error in synatax at line {self.currentToken._getLineNo()}, "
            + f'after "{self.previousToken._getValue()}" '
            + f'it got "{self.currentToken._getValue()}" token that is ambiguous'
        )

        exit(1)
