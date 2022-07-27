
class Token:

    def __init__(self, Name, Value, lineNo, Type=None) -> None:
        self.name = Name 
        self.value = Value
        self.lineNo = lineNo
        self.type = Type
        pass


    def _setType(self, type: str) -> None:
        self.type = type
        pass

    def _getName(self) -> str:
        return self.name

    def _getValue(self) -> str:
        return self.value
    
    def _getType(self) -> str:
        return self.type

    def _getLineNo(self) -> int:
        return self.lineNo

  
# class Node:
#     """docstring for Node"""
#     def __init__(self, record: SymbolTable) -> None:
#         self.record:SymbolTable = record
#         self.next:Node = None
    
#     def _getRecord(self) -> SymbolTable:
#         return self.record



# class LinkedList:

#     def __init__(self) -> None:
#         self._Node:Node = None

#     def _add(self,record:SymbolTable) -> None:
        
#         __newNode = Node(record)

#         if self._Node is None: 
#             self._Node = __newNode
#             return
        
#         __currentNode = self._Node
#         while __currentNode.next is not None:
#             __currentNode = __currentNode.next
        
#         __currentNode.next = __newNode
    
    
#     def _printTable(self) -> str:

#         __currentNode = self._Node

#         _str = '\n' + '=' * 100 + '\n'
#         _str += 'Token Table\n'
#         _str += '=' * 100 + '\n'
#         _str += 'Name'.ljust(20) + '| Value'.ljust(50) + '| Line No.' + '\n'
#         _str += '-' * 100 + '\n'
#         while __currentNode is not None:
#             record = __currentNode._getRecord()
#             _str += record._getName().ljust(20) + '| ' + record._getValue().ljust(50) + '| ' + str(record._getLineNo()).ljust(10) + '\n'
#             _str += '-' * 100 + '\n'
#             __currentNode = __currentNode.next
#         _str += '=' * 100 + '\n'

#         return _str

#     # yield the next node in the list
#     def _getTokens(self) -> Node:
#         __currentNode = self._Node
#         while __currentNode is not None:
#             yield __currentNode
#             __currentNode = __currentNode.next
            