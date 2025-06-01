class LexicalError:
    
    def __init__(self,token_type,token_line,token_pos):
        self.type = token_type
        self.line = token_line
        self.pos = token_pos
        
class SyntaxError:
    
    def __init__(self,token_type,token_line,token_pos):
        self.type = token_type
        self.line = token_line
        self.pos = token_pos
        
class SemanticError:
    
    def __init__(self,token_type,token_line,token_pos,message_error):
        self.type = token_type
        self.line = token_line
        self.pos = token_pos
        self.message_error = message_error
        
class SemanticWarning:
    
    def __init__(self,token_type,token_line,token_pos,message_warning):
        self.type = token_type
        self.line = token_line
        self.pos = token_pos
        self.message_warning = message_warning