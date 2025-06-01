import ply.lex as lex
import sys
import errors.error_handler as eh

states = [
    ("INBLOCK", "exclusive")
]

stack_begins = []

literals = ["(",")","[","]",".",";",",",":"]

tokens_any = [
    "BEGIN",
    "END",
    "ID",
    "NUMBER",
    "NUMBERREAL"
    ]

tokens_out_block = [
    "PROGRAM",
    "VAR",
    "DATATYPE",
    "ARRAY",
    "RANGEOP",         # ..
    "OF",
    "FUNCTION",
    "PROCEDURE"
]

tokens_in_block = [
    "STRING",
    "CHAR",
    "WALRUS",     # :=
    "ARITOP1",    # * / div mod
    "ARITOP2",    # + - 
    "FOR",
    "TO",
    "DO",
    "RELAOP", 
    "LOGICOP1",   # not 
    "LOGICOP2",   # and 
    "LOGICOP3",   # or xor 
    "WHILE",
    "IF",
    "ELSE",
    "THEN",
    "LOGICVALUE",
    "DOWNTO"
]

tokens = tokens_any + tokens_in_block + tokens_out_block 

def t_ANY_COMMENT(t):
    r"\(\*[\s\S]*?\*\)|\{[\s\S]*?\}"
    pass

def t_INBLOCK_CHAR(t):
    r"'.'"
    
    t.value = t.value[1:-1]
    return t

def t_INBLOCK_STRING(t):
    r"'.*?'"

    t.value = t.value[1:-1]
    return t

def t_PROGRAM(t):
    r"^(?i:PROGRAM)\b"
    return t

def t_ANY_BEGIN(t):
    r"(^|\b)(?i:BEGIN)\b"
    
    if (not stack_begins):
        t.lexer.begin("INBLOCK")
    
    stack_begins.append("begin")
    
    return t

def t_ANY_END(t):
    r"(^|\b)(?i:END)"
    
    if len(stack_begins) > 0:
        stack_begins.pop()
    
    if not stack_begins:
        t.lexer.begin("INITIAL")
    
    return t 

def t_RANGEOP(t):
    r'\.\.'
    return t
    
def t_VAR(t):
    r"(?i:VAR)"
    return t
    
def t_DATATYPE(t):
    r'\b(?i:integer|real|char|string|boolean)\b'
    return t

def t_FUNCTION(t):
    r'\b(?i:function)\b'
    return t

def t_PROCEDURE(t):
    r'\b(?i:procedure)\b'
    return t

def t_ARRAY(t):
    r'\b(?i:array)\b'
    return t

def t_OF(t):
    r'\b(?i:of)\b'
    return t

def t_ANY_NUMBERREAL(t):
    r"\b\-?\d+\.\d+\b"
    t.value = float(t.value)
    return t

def t_ANY_NUMBER(t):
    r"\b\-?\d+\b"
    t.value = int(t.value)
    return t

def t_INBLOCK_ARITOP1(t):
    r"(?i:\*|\/|div|mod)"
    return t

def t_INBLOCK_ARITOP2(t):
    r"(\+|\-)"
    return t
    
def t_INBLOCK_RELAOP(t):
    r"(?i:=|<>|>=|<=|<|>|in)"
    return t
    
def t_INBLOCK_LOGICOP1(t):
    r"(?i:not)"
    return t

def t_INBLOCK_LOGICOP2(t):
    r"(?i:and)"
    return t

def t_INBLOCK_LOGICOP3(t):
    r"(?i:or|xor)"
    return t

def t_INBLOCK_TO(t):
    r"\b(?i:to)\b"
    return t

def t_INBLOCK_DO(t):
    r"\b(?i:do)\b"
    return t

def t_INBLOCK_FOR(t):
    r"\b(?i:for)\b"
    return t

def t_INBLOCK_WALRUS(t):
    r":="
    return t

def t_INBLOCK_LOGICVALUE(t):
    r"(?i:false|true)"
    
    if t.value.lower() == "false":
        t.value = False
    else:
        t.value = True
    
    return t

def t_INBLOCK_DOWNTO(t):
    r"\b(?i:downto)\b"
    return t

def t_INBLOCK_WHILE(t):
    r"\b(?i:while)"
    return t

def t_INBLOCK_IF(t):
    r"\b(?i:if)"
    return t

def t_INBLOCK_ELSE(t):
    r"(?i:else)"
    return t

def t_INBLOCK_THEN(t):
    r"(?i:then)"
    return t

def t_ANY_ID(t):
    r"[a-zA-Z][a-zA-Z_0-9]*"
    return t

def t_ANY_NEWLINE(t):
    r"\n+"
    t.lexer.lineno += len(t.value) 
    pass

t_ANY_ignore = "\t "

def t_ANY_error(t):
    r'.'
    t.lexer.skip(1)

    eh.add_lexical_error(t.value[0],t.lineno,t.lexpos)

lexer = lex.lex()