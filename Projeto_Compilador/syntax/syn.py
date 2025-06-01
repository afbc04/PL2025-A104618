import ply.yacc as yacc
import os
from lexical.lex import tokens
import errors.error_handler as eh
from ply.lex import LexToken


def get_first_token(p):

    for sym in p.slice[1:]:
        
        if isinstance(sym,LexToken) is True:
            return sym
        
    return None

# ========== Operator Precedence ==========

precedence = (
    ('nonassoc', 'IFX'),
    ('nonassoc', 'ELSE'),
    ('left', 'RELAOP'),    # = <> > < >= <=
    ('left', 'LOGICOP3'),  # or, xor
    ('left', 'LOGICOP2'),  # and
    ('left', 'ARITOP2'),   # + -
    ('left', 'ARITOP1'),   # * / div mod
    ('right', 'LOGICOP1'), # not
)

# ========== Program Structure ==========

def p_init(p):
    """init : PROGRAM ID ';' vars_declaration_global has_funcproc main_code"""
    
    p[0] = {
            "token" : get_first_token(p),
            "type" : "PROGRAM",
            "program_name" : p[2],
            "global_vars" : p[4],
            "funcproc_list" : p[5][0],
            "local_vars" : p[5][1],
            "code_block" : p[6]
        }

def p_has_funcproc(p):
    """has_funcproc : funcproc_declaration_list_init vars_declaration_local
                    | """
                         
    if len(p) == 1:
        
        local_vars = {
            "token" : None,
            "type" : "VARS_LOCAL",
            "var_local_list" : []
        }
        
        funcproc_list = {
            "token" : None,
            "type" : "FUNCPROC",
            "funcproc_list" : []
        }
        
        p[0] = (funcproc_list,local_vars)
    
    else:
        
        p[0] = (p[1],p[2])


# ========== Variable Declarations ==========

def p_vars_declaration_global(p):
    """vars_declaration_global : VAR vars_declaration_list
                               |"""

    if len(p) == 3:
        p[0] = {
            "token" : get_first_token(p),
            "type" : "VARS_GLOBAL",
            "var_global_list" : p[2]
        }
        
    else:
        p[0] = {
            "token" : get_first_token(p),
            "type" : "VARS_GLOBAL",
            "var_global_list" : []
        }

def p_vars_declaration_local(p):
    """vars_declaration_local : VAR vars_declaration_list
                              |"""

    if len(p) == 3:
        p[0] = {
            "token" : get_first_token(p),
            "type" : "VARS_LOCAL",
            "var_local_list" : p[2]
        }
        
    else:
        p[0] = {
            "token" : get_first_token(p),
            "type" : "VARS_LOCAL",
            "var_local_list" : []
        }
    

def p_vars_declaration_list(p):
    """vars_declaration_list : vars_declaration_list declaration
                             | declaration"""
    
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]
    

def p_declaration(p):
    """declaration : declarations_name_list ':' data_type ';'"""
    
    p[0] = {
        "token" : get_first_token(p),
        "type" : "VAR_DECL",
        "data_type" : p[3],
        "var_names_list" : p[1]
    }
    
def p_declarations_name_list(p):
    """declarations_name_list : declarations_name_list ',' ID
                              | ID"""
                              
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_data_type(p):
    """data_type : DATATYPE
                 | ARRAY '[' NUMBER RANGEOP NUMBER ']' OF DATATYPE"""
                 
    if len(p) == 2:
        p[0] = {
            "token" : get_first_token(p),
            "type" : "DATATYPE",
            "is_array" : False,
            "data_type" : p[1],
        }
        
    else:
        p[0] = {
            "token" : get_first_token(p),
            "type" : "DATATYPE",
            "is_array" : True,
            "data_type" : p[8],
            "min_range" : p[3],
            "max_range" : p[5]
        }

# ========== Functions and Procedures ==========


def p_funcproc_declaration_list_init(p):
    """funcproc_declaration_list_init : funcproc_declaration_list"""
    
    p[0] = {
        "token" : get_first_token(p),
        "type" : "FUNCPROC",
        "funcproc_list" : p[1]
    }

        
def p_funcproc_declaration_list(p):
    """funcproc_declaration_list : funcproc_declaration_list funcproc_declaration
                                 | funcproc_declaration"""
    
    if len(p) == 2:
        p[0] = [p[1]]
        
    else:
        p[0] = p[1] + [p[2]]
    
def p_funcproc_declaration(p):
    """funcproc_declaration : FUNCTION ID '(' funcproc_args_declaration ')' ':' data_type ';' vars_declaration_local code_block ';'
                            | PROCEDURE ID '(' funcproc_args_declaration ')' ';' vars_declaration_local code_block ';'"""
    
    if len(p) == 12:
        p[0] = {
            "token" : get_first_token(p),
            "type" : "FUNCTION",
            "is_default" : False,
            "function_name" : p[2],
            "return_value" : p[7],
            "args" : p[4],
            "local_vars" : p[9],
            "function_code" : p[10]
        }
    else:
        p[0] = {
            "token" : get_first_token(p),
            "type" : "PROCEDURE",
            "is_default" : False,
            "procedure_name" : p[2],
            "args" : p[4],
            "local_vars" : p[7],
            "procedure_code" : p[8]
        }

def p_funcproc_args_declaration(p):
    """funcproc_args_declaration : funcproc_args_declaration_continue
                                 |"""
    
    if len(p) == 1:
        p[0] = {
            "token" : get_first_token(p),
            "type" : "FUNCPROC_DECL_ARGS_LIST",
            "args_list" : [],
        }
        
    else:
        p[0] = {
            "token" : get_first_token(p),
            "type" : "FUNCPROC_DECL_ARGS_LIST",
            "args_list" : p[1],
        }

def p_funcproc_args_declaration_continue(p):
    """funcproc_args_declaration_continue : funcproc_args_declaration_continue ',' ID ':' data_type
                                          | ID ':' data_type"""
    
    if len(p) == 4:
        p[0] = [
                {
                    "token" : get_first_token(p),
                    "type" : "FUNCPROC_DECL_ARG",
                    "var_name" : p[1],
                    "data_type" : p[3]
                }
                ]
    else:
        p[0] = p[1] + [
                        {
                            "token" : get_first_token(p),
                            "type" : "FUNCPROC_DECL_ARG",
                            "var_name" : p[3],
                            "data_type" : p[5]
                        }
                      ]

# ========== Main Code Block ==========

def p_main_code(p):
    """main_code : code_block '.'"""
    
    p[0] = p[1]

def p_code_block(p):
    """code_block : BEGIN instruction_list END"""
    
    p[0] = {
        "token" : get_first_token(p),
        "type" : "CODE_BLOCK",
        "instructions_list" : p[2],
    }

def p_instruction_list(p):
    """instruction_list : instruction_list instruction ';'
                        |"""
                        
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1] + [p[2]]

def p_mini_code_block(p):
    """mini_code_block : instruction
                       | code_block"""
    
    p[0] = p[1]
    
# ========== Instructions ==========

def p_instruction(p):
    """instruction : instruction_funcproc
                   | instruction_if
                   | instruction_for
                   | instruction_while
                   | instruction_walrus"""
    
    p[0] = p[1]
    
def p_instruction_funcproc_args(p):
    """instruction_funcproc_args : '(' funcproc_args ')'"""
    
    p[0] = p[2]

def p_instruction_funcproc(p):
    """instruction_funcproc : ID instruction_funcproc_args"""

    p[0] = {
        "token" : get_first_token(p),
        "type" : "INSTRUCTION_FUNCPROC",
        "funcproc_name" : p[1],
        "funcproc_args" : p[2]
    }

def p_funcproc_args(p):
    """funcproc_args : funcproc_args_continue
                     |"""
                     
    if len(p) == 1:
        p[0] = {
            "token" : get_first_token(p),
            "type" : "FUNCPROC_ARGS",
            "args_list" : [],
        }
        
    else:
        p[0] = {
            "token" : get_first_token(p),
            "type" : "FUNCPROC_ARGS",
            "args_list" : p[1],
        }

def p_funcproc_args_continue(p):
    """funcproc_args_continue : funcproc_args_continue ',' expression
                              | expression"""
    
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_instruction_if(p):
    """instruction_if : IF expression THEN mini_code_block ELSE mini_code_block"""
    
    p[0] = {
        "token" : get_first_token(p),
        "type" : "INSTRUCTION_IF_ELSE",
        "condition" : p[2],
        "body_if" : p[4],
        "body_else" : p[6]
    }
    
def p_instruction_if_simple(p):
    """instruction_if : IF expression THEN mini_code_block %prec IFX"""
    
    p[0] = {
        "token" : get_first_token(p),
        "type" : "INSTRUCTION_IF_ELSE",
        "condition" : p[2],
        "body_if" : p[4],
        "body_else" : None
    }

def p_instruction_for(p):
    """instruction_for : FOR instruction_walrus instruction_for_final DO mini_code_block"""

    p[0] = {
        "token" : get_first_token(p),
        "type" : "INSTRUCTION_FOR",
        "var_control" : p[2],
        "condition" : p[3],
        "body" : p[5]
    }


def p_instruction_for_final_to(p):
    """instruction_for_final : TO expression"""

    p[0] = {
        "token" : get_first_token(p),
        "type" : "INSTRUCTION_FOR_TO",
        "value" : p[2],
    }
    
def p_instruction_for_final_downto(p):
    """instruction_for_final : DOWNTO expression"""
    
    p[0] = {
        "token" : get_first_token(p),
        "type" : "INSTRUCTION_FOR_DOWNTO",
        "value" : p[2],
    }

def p_instruction_while(p):
    """instruction_while : WHILE expression DO mini_code_block"""
    
    p[0] = {
        "token" : get_first_token(p),
        "type" : "INSTRUCTION_WHILE",
        "condition" : p[2],
        "body" : p[4],
    }
    

def p_instruction_walrus(p):
    """instruction_walrus : expression WALRUS expression"""
    
    p[0] = {
        "token" : get_first_token(p),
        "type" : "INSTRUCTION_WALRUS",
        "var" : p[1],
        "value" : p[3],
    }
        

# ========== Expressions ==========

def p_expression_operations(p):
    """expression : expression ARITOP1 expression
                  | expression ARITOP2 expression
                  | expression RELAOP expression
                  | expression LOGICOP2 expression
                  | expression LOGICOP3 expression"""

    p[0] = {
        "token" : get_first_token(p),
        "type" : "OPERATION_BINARY",
        "operator" : p[2],
        "value_1" : p[1],
        "value_2" : p[3]
    }

def p_expression_operations_not(p):
    """expression : LOGICOP1 expression"""
    
    p[0] = {
        "token" : get_first_token(p),
        "type" : "OPERATION_UNARY",
        "operator" : p[1],
        "value" : p[2]
    }

def p_expression_paren(p):
    """expression : '(' expression ')'"""
    
    p[0] = p[2]

def p_expression_value_number(p):
    """expression : NUMBER"""
    
    p[0] = {
        "token" : get_first_token(p),
        "type" : "VALUE_NUMBER",
        "value" : p[1]
    }
    
def p_expression_value_number_real(p):
    """expression : NUMBERREAL"""
    
    p[0] = {
        "token" : get_first_token(p),
        "type" : "VALUE_NUMBER_REAL",
        "value" : p[1]
    }
    
def p_expression_value_string(p):
    """expression : STRING"""
    
    p[0] = {
        "token" : get_first_token(p),
        "type" : "VALUE_STRING",
        "value" : p[1]
    }
    
    
def p_expression_value_char(p):
    """expression : CHAR"""
    
    p[0] = {
        "token" : get_first_token(p),
        "type" : "VALUE_CHAR",
        "value" : p[1]
    }
    
def p_expression_value_boolean(p):
    """expression : LOGICVALUE"""
    
    p[0] = {
        "token" : get_first_token(p),
        "type" : "VALUE_BOOLEAN",
        "value" : p[1]
    }
    
def p_expression_value_variable(p):
    """expression : ID"""
    
    p[0] = {
        "token" : get_first_token(p),
        "type" : "VALUE_VAR",
        "name_var" : p[1]
    }
    
def p_expression_value(p):
    """expression : instruction_funcproc
                  | get_array_index_value"""
    
    p[0] = p[1]

def p_get_array_index_value(p):
    """get_array_index_value : ID '[' expression ']'"""
    
    p[0] = {
        "token" : get_first_token(p),
        "type" : "ARRAY_INDEX",
        "array_name" : p[1],
        "index" : p[3]
    }

# ========== Error Handling ==========

def p_error(p):

    if p:
    
        eh.add_syntax_error(p.value,p.lineno,p.lexpos)
        
        parser.errok()
        parser.token()
    

parser = yacc.yacc()


def SyntaxParser(PascalCode,lexer):

    lexer.lineno = 1
    ast = parser.parse(PascalCode, debug=False, lexer = lexer)

    return ast

        
        
