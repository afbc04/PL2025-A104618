from errors.error_lex_class import LexicalError, SyntaxError, SemanticError, SemanticWarning

"""
LEXICAL ERRORS
"""

error_lex_list = []

# Function that adds a lexical error to the lexical errors list
def add_lexical_error(token_type,token_line,token_pos):
    
    def should_join_lexical_error(last_token,_,current_line,current_pos):
        
        return current_line == last_token.line and last_token.pos + len(last_token.type) == current_pos
        
    
    if len(error_lex_list) > 0:
    
        last_error = error_lex_list.pop()
        
        if should_join_lexical_error(last_error,token_type,token_line,token_pos) == True:

            last_error.type += token_type
            error_lex_list.append(last_error)
            
        else:
            
            error_lex_list.append(last_error)
            
            new_error = LexicalError(token_type,token_line,token_pos)
            error_lex_list.append(new_error)
            
    else:
        
        new_error = LexicalError(token_type,token_line,token_pos)
        error_lex_list.append(new_error)
    
# Function that indicates how many lexical errors exist
def how_many_lexical_errors():
    return len(error_lex_list)

# Function that prints lexical errors detection
def print_lexical_errors(pascalCode):
    
    initial_spacing = 5
    
    pascalCode_lines = pascalCode.splitlines()
    
    for error in error_lex_list:
        
        print(f"\033[1;91mLexical Error:\033[0;0m \033[1m'{error.type}'\033[0m token unknown")
        
        print(f"{str(error.line).rjust(initial_spacing)} | ",end='')
        
        current_pos = sum(len(s) + 1 for s in pascalCode_lines[:error.line - 1])
        last_pos_error = error.pos + len(str(error.type))
        
        for char in pascalCode_lines[error.line -1]:
            
            if current_pos >= error.pos and current_pos < last_pos_error:
                print(f"\033[1;91m{char}\033[0;0m",end='')
                
            else:
                print(char,end='')
            
            current_pos += 1

        print(f"\n{' '.rjust(initial_spacing)} | ",end='')
        
        
        current_pos = sum(len(s) + 1 for s in pascalCode_lines[:error.line - 1])
        
        for _ in pascalCode_lines[error.line -1]:
            
            if current_pos >= error.pos and current_pos < last_pos_error:
                
                if current_pos == error.pos:
                    print(f"\033[1;91m^\033[0;0m",end='')
                    
                else:
                    print(f"\033[1;91m~\033[0;0m",end='')
                    
            else:
                print(" ",end='')
            
            current_pos += 1
            
        print("")
        
        
"""
SYNTAX ERRORS
"""

error_syn_list = []

# Function that adds a syntax error to the syntax errors list
def add_syntax_error(token_type,token_line,token_pos):
    
    new_error = SyntaxError(token_type,token_line,token_pos)
    error_syn_list.append(new_error)
            
# Function that indicates how many syntax errors exist
def how_many_syntax_errors():
    return len(error_syn_list)

# Function that prints syntax errors detection
def print_syntax_errors(pascalCode):
    
    initial_spacing = 5
    
    pascalCode_lines = pascalCode.splitlines()
    
    for error in error_syn_list:
        
        print(f"\033[1;91mSyntax Error:\033[0;0m \033[1m'{error.type}'\033[0m unexpected token")
        
        print(f"{str(error.line).rjust(initial_spacing)} | ",end='')
                
        current_pos = sum(len(s) + 1 for s in pascalCode_lines[:error.line - 1])
        last_pos_error = error.pos + len(str(error.type))
        
        for char in pascalCode_lines[error.line -1]:
            
            if current_pos >= error.pos and current_pos < last_pos_error:
                print(f"\033[1;91m{char}\033[0;0m",end='')
                
            else:
                print(char,end='')
            
            current_pos += 1

        print(f"\n{' '.rjust(initial_spacing)} | ",end='')
                
        current_pos = sum(len(s) + 1 for s in pascalCode_lines[:error.line - 1])
                
        for _ in pascalCode_lines[error.line -1]:
                        
            if current_pos >= error.pos and current_pos < last_pos_error:
                                
                if current_pos == error.pos:
                    print(f"\033[1;91m^\033[0;0m",end='')
                    
                else:
                    print(f"\033[1;91m~\033[0;0m",end='')
                    
            else:
                print(" ",end='')
            
            current_pos += 1
            
        print("")

"""
SEMANTIC ERRORS
"""

error_sem_list = []

# Function that adds a semantic error to the semantic errors list
def add_semantic_error(token,message_error):
        
    if token is None:
        return
        
    token_type = token.value
    token_line = token.lineno
    token_pos = token.lexpos

    new_error = SemanticError(token_type,token_line,token_pos,message_error)
    error_sem_list.append(new_error)
            
# Function that indicates how many semantic errors exist
def how_many_semantic_errors():
    return len(error_sem_list)

# Function that prints semantic errors detection
def print_semantic_errors(pascalCode):
    
    initial_spacing = 5
    
    pascalCode_lines = pascalCode.splitlines()
    
    for error in error_sem_list:
        
        print(f"\033[1;91mSemantic Error:\033[0;0m \033[1m'{error.type}'\033[0m {error.message_error}")
        
        print(f"{str(error.line).rjust(initial_spacing)} | ",end='')
                
        current_pos = sum(len(s) + 1 for s in pascalCode_lines[:error.line - 1])
        last_pos_error = error.pos + len(str(error.type))
        
        for char in pascalCode_lines[error.line -1]:
            
            if current_pos >= error.pos and current_pos < last_pos_error:
                print(f"\033[1;91m{char}\033[0;0m",end='')
                
            else:
                print(char,end='')
            
            current_pos += 1

        print(f"\n{' '.rjust(initial_spacing)} | ",end='')
                
        current_pos = sum(len(s) + 1 for s in pascalCode_lines[:error.line - 1])
                
        for _ in pascalCode_lines[error.line -1]:
                        
            if current_pos >= error.pos and current_pos < last_pos_error:
                                
                if current_pos == error.pos:
                    print(f"\033[1;91m^\033[0;0m",end='')
                    
                else:
                    print(f"\033[1;91m~\033[0;0m",end='')
                    
            else:
                print(" ",end='')
            
            current_pos += 1
            
        print("")

"""
SEMANTIC WARNINGS
"""

warning_sem_list = []

# Function that adds a semantic warning to the semantic warning list
def add_semantic_warning(token,message_warning):
        
    if token is None:
        return
        
    token_type = token.value
    token_line = token.lineno
    token_pos = token.lexpos
    
    new_warning = SemanticWarning(token_type,token_line,token_pos,message_warning)
    warning_sem_list.append(new_warning)
            
# Function that indicates how many semantic warnings exist
def how_many_semantic_warnings():
    return len(warning_sem_list)

# Function that prints semantic warning detection
def print_semantic_warning(pascalCode):
    
    initial_spacing = 5
    
    pascalCode_lines = pascalCode.splitlines()
    
    for warning in warning_sem_list:
        
        print(f"\033[1;35mSemantic Warning:\033[0;0m \033[1m'{warning.type}'\033[0m {warning.message_warning}")
        
        print(f"{str(warning.line).rjust(initial_spacing)} | ",end='')
                
        current_pos = sum(len(s) + 1 for s in pascalCode_lines[:warning.line - 1])
        last_pos_warning = warning.pos + len(str(warning.type))
        
        for char in pascalCode_lines[warning.line -1]:
            
            if current_pos >= warning.pos and current_pos < last_pos_warning:
                print(f"\033[1;35m{char}\033[0;0m",end='')
                
            else:
                print(char,end='')
            
            current_pos += 1

        print(f"\n{' '.rjust(initial_spacing)} | ",end='')
                
        current_pos = sum(len(s) + 1 for s in pascalCode_lines[:warning.line - 1])
                
        for _ in pascalCode_lines[warning.line -1]:
                        
            if current_pos >= warning.pos and current_pos < last_pos_warning:
                                
                if current_pos == warning.pos:
                    print(f"\033[1;35m^\033[0;0m",end='')
                    
                else:
                    print(f"\033[1;35m~\033[0;0m",end='')
                    
            else:
                print(" ",end='')
            
            current_pos += 1
            
        print("")



# Function which prints the summary of the whole compilation process
def print_compilation_summary(output_file_name,pascalCode,startTime=None, compilingTime=None, lexTime = None, syntaxTime = None, semanticTime = None):
    
    errorsCount = 0
    warningsCount = 0
    
    if how_many_lexical_errors() + how_many_syntax_errors() + how_many_semantic_warnings() + how_many_semantic_errors() > 1:
        print("")
    
    if how_many_lexical_errors() > 0:
        print_lexical_errors(pascalCode)
        errorsCount += how_many_lexical_errors()
        
    if how_many_syntax_errors() > 0:
        print_syntax_errors(pascalCode)
        errorsCount += how_many_syntax_errors()
        
    if how_many_semantic_errors() > 0:
        print_semantic_errors(pascalCode)
        errorsCount += how_many_semantic_errors()
        
    if how_many_semantic_warnings() > 0:
        print_semantic_warning(pascalCode)
        warningsCount += how_many_semantic_warnings()
    
    
    print(f"\033[1m\n{'='*30}\nSummary:\033[0m")
    
    if how_many_lexical_errors() > 0:
        print(f"\033[1;31mLexical:\033[0;0m { how_many_lexical_errors() } errors encountered")
        
    else:
        print(f"\033[1;32mLexical:\033[0;0m No errors encountered ({lexTime - startTime:.6f} seconds)")
        
        if how_many_syntax_errors() > 0:
            print(f"\033[1;31mSyntax:\033[0;0m { how_many_syntax_errors() } errors encountered")

        else:
            print(f"\033[1;32mSyntax:\033[0;0m No errors encountered ({syntaxTime - lexTime:.6f} seconds)")

            if how_many_semantic_errors() > 0:
                print(f"\033[1;31mSemantic:\033[0;0m { how_many_semantic_errors() } errors encountered")

            else:
                print(f"\033[1;32mSemantic:\033[0;0m No errors encountered ({semanticTime - syntaxTime:.6f} seconds)")


    print(f"{'-'*30}")

    if compilingTime is None:
        print(f"\033[1;91mCompilation Failed:\033[0;0m \033[1m{ errorsCount }\033[0m erros & \033[1m{ warningsCount }\033[0m warnings")
        
    else:
        print(f"\033[1;32mCompilation Complete:\033[0;0m \033[1m{ errorsCount }\033[0m erros & \033[1m{ warningsCount }\033[0m warnings ({compilingTime - startTime:.6f} seconds)")
        print(f"\033[1m >>> \033[0m\033[1;32m{ output_file_name }\033[0;0m\033[0m file generated")


    print(f"\033[1m{'='*30}\033[0m")