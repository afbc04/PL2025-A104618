from semantic.sem_classes import *

output_file = None
table = {}
code_machine_table = {}

def add_line(line):
    global code_machine_table, output_file
    
    output_file.write('\t' * code_machine_table['space_line'])
    output_file.write(line)
    output_file.write('\n')
    
    

def add_space():
    global code_machine_table
    
    code_machine_table['space_line'] += 1
    
def remove_space():
    global code_machine_table
    
    code_machine_table['space_line'] -= 1
    
    

def init_code_machine_table():
    
    table = {}
    table['label_id'] = 0
    table['funcproc_id'] = 0
    table['space_line'] = 0
    
    return table



def generate_code(output_file_name,ast,sem_table):
    global output_file, table, code_machine_table

    code_machine_table = init_code_machine_table()
    table = sem_table
    output_file = open(output_file_name,"w+")
    
    rec_program(ast)
    
    output_file.close()
    




def get_ID(name,preferenceType):
    global table, code_machine_table
    
    name = name.lower()
    var = None
    
    if name in table['table'] and (preferenceType is None or (preferenceType is not None and isinstance(table['table'][name],preferenceType))):
        var = table['table'][name]
    
    if table['current_table'] is not None and name in table['table'][table['current_table']].table and (preferenceType is None or (preferenceType is not None and isinstance(table['table'][table['current_table']].table[name],preferenceType))):
        var = table['table'][table['current_table']].table[name]
    
    
    return var





def rec_program(node):
    global table, code_machine_table
    
    add_line(f"// Pascal Compiler - Processamento de Linguagens")
    add_line(f"// --------------------------------------------")
    add_line(f"// André Campos - a104618")
    add_line(f"// Beatriz Peixoto - a104170")
    add_line(f"// Sara Lopes - a104179")
    add_line(f"// --------------------------------------------")
    add_line("")
    add_line(f"// Program Name : {node['program_name']}\n")
        
    rec_global_vars(node['global_vars'])
    
    table['current_table'] = '_func'
    
    add_line(f"\n//Main function\nfuncproc{code_machine_table['funcproc_id']}:\n")
    add_space()
    
    code_machine_table['funcproc_id'] += 1
    
    add_line("START")
        
    rec_local_vars(node['local_vars'],False,False)
    rec_code_block(node['code_block'])
    
    table['current_table'] = None
    add_line("STOP\n")
    remove_space()
    
    add_line(f"// #####")
    
    rec_funcproc_def(node['funcproc_list'])
    
    
    
def rec_funcproc_def(node):
    global table, code_machine_table
    
    for funcproc in node['funcproc_list']:
        
        if funcproc['type'] == "FUNCTION":
            rec_function_def(funcproc)
            
        elif funcproc['type'] == "PROCEDURE":
            rec_procedure_def(funcproc)
            
        add_line(f"// #####")
         
         
         
def rec_procedure_def(node):
    global table, code_machine_table
    
    procedure_name = node['procedure_name'].lower()
            
    table['current_table'] = procedure_name
    add_line(f"\n// Procedure Name : {table['current_table']}\nfuncproc{code_machine_table['funcproc_id']}:")
    code_machine_table['funcproc_id'] += 1
    add_space()
        
    rec_local_vars(node['local_vars'],True,True)
    
    procedure = table['table'][procedure_name]
    
    rec_code_block(node['procedure_code'])
    table['current_table'] = None
    
    add_line(f"POP {len(procedure.table.values())}")
    add_line(f"RETURN")
    remove_space()
    
    
    
def rec_function_def(node):
    global table, code_machine_table
    
    function_name = node['function_name'].lower()
            
    table['current_table'] = function_name
    add_line(f"\n// Function Name : {table['current_table']}\nfuncproc{code_machine_table['funcproc_id']}:")
    code_machine_table['funcproc_id'] += 1
    add_space()
        
    rec_local_vars(node['local_vars'],True,True)
    
    function = table['table'][function_name]
    
    rec_code_block(node['function_code'])
    table['current_table'] = None
    
    add_line(f"POP {len(function.table.values()) - 1}")
    add_line(f"RETURN")
    remove_space()
    
def rec_local_vars(node,isUserFuncProc,isFunc):
    global table, code_machine_table
        
    new_table = [
        var for var in table['table'][table['current_table']].table.values()
        if isinstance(var, SemVar) and var.isGlobal is False and var.var_name != table['current_table']
    ]
        
    new_table = sorted(new_table, key=lambda v: v.vm_id)
    
    add_line(f"// Local Variables:")
    
    if isFunc is True:
        add_line("")
        add_line(f"ALLOC 1")
        add_line(f"STOREL 0 // Return Value")
        
    for i,var in enumerate(new_table):            
            
        if var.isArgument is False:
            
            if var.is_array is False:

                add_line("")
                add_line(f"ALLOC 1")
                add_line(f"STOREL {var.vm_id} //Local Variable Name : {var.var_name}")

            if var.is_array is True:

                array_size = var.max_range - var.min_range + 1

                add_line("")
                add_line(f"PUSHI {array_size} // Array Length : {array_size}")
                add_line(f"ALLOCN")
                add_line(f"STOREL {var.vm_id} // Local Variable Name : {var.var_name}")
                
        else:
            
            add_line("")
            add_line(f"PUSHFP")
            add_line(f"LOAD -{i+1}")
            
    add_line(f"// -----")
            
    
def rec_global_vars(node):
    global table, code_machine_table
        
    new_table = [
        var for var in table['table'].values()
        if isinstance(var, SemVar) and var.isGlobal
    ]
    
    new_table = sorted(new_table, key=lambda v: v.vm_id)
    
    add_line(f"// Global Variables:")
    
    for var in new_table:
            
        if var.is_array is False:
            
            add_line("")
            add_line(f"ALLOC 1")
            add_line(f"STOREG {var.vm_id} //Global Variable Name : {var.var_name}")
                    
        if var.is_array is True:
            
            array_size = var.max_range - var.min_range + 1
            
            add_line("")
            add_line(f"PUSHI {array_size} //Array Length : {array_size}")
            add_line(f"ALLOCN")
            add_line(f"STOREG {var.vm_id} //Global Variable Name : {var.var_name}")
            
    add_line(f"// -----")
    
def rec_code_block(node):
    global table, code_machine_table
                                                
    for instruction in node['instructions_list']:
        
        rec_instruction(instruction)


def rec_mini_code_block(node):
    global table, code_machine_table
                                                                                         
    if node['type'] == "CODE_BLOCK":
        return rec_code_block(node)
    else:
        return rec_instruction(node)  


def rec_instruction(node):
    global table, code_machine_table
        
    add_line("")
        
    match node['type']:
        
        case "INSTRUCTION_FUNCPROC":
            return rec_instruction_funcproc(node)
            
        case "INSTRUCTION_IF_ELSE":
            rec_instruction_if_else(node)
        
        case "INSTRUCTION_FOR":
            rec_instruction_for(node)
        
        case "INSTRUCTION_WHILE":
            rec_instruction_while(node)
        
        case "INSTRUCTION_WALRUS":
            rec_instruction_walrus(node)
                
        case _:
            pass
    
def rec_instruction_if_else(node):
    global table, code_machine_table
        
    else_id = code_machine_table['label_id']
    code_machine_table['label_id'] += 1
        
    rec_expression(node['condition'])
    add_line(f"JZ ElseBody{else_id}")
        
    rec_mini_code_block(node['body_if'])
    add_line(f"JUMP IfEnd{else_id}")
    
    remove_space()
    add_line(f"ElseBody{else_id}:")
    add_space()
        
    if node['body_else'] is not None:
        rec_mini_code_block(node['body_else'])
        
    remove_space()
    add_line(f"IfEnd{else_id}:")
    add_space()
    
    
def rec_instruction_while(node):
    global table, code_machine_table
        
    while_label = code_machine_table['label_id']
    code_machine_table['label_id'] += 1
        
    remove_space()
    add_line(f"InitWhile{while_label}:")
    add_space()
    
    rec_expression(node['condition'])
    add_line(f"JZ EndWhile{while_label}")
        
    rec_mini_code_block(node['body'])
    add_line(f"JUMP InitWhile{while_label}")
    
    remove_space()
    add_line(f"EndWhile{while_label}:")
    add_space()
    
def rec_instruction_for(node):
    global table, code_machine_table
        
    for_label = code_machine_table['label_id']
    code_machine_table['label_id'] += 1
            
    rec_instruction_walrus(node['var_control'])
    
    remove_space()
    add_line(f"InitFor{for_label}:")
    add_space()
    
    rec_instruction_for_condition(node)
        
    add_line(f"JZ EndFor{for_label}")
        
    rec_mini_code_block(node['body'])
    
    rec_instruction_for_step(node)
    
    add_line(f"JUMP InitFor{for_label}")
    
    remove_space()
    add_line(f"EndFor{for_label}:")
    add_space()
    
    
def rec_instruction_for_condition(node):
    global table, code_machine_table
        
    var = node['var_control']['var']
    rec_expression(var)
    
    condition = node['condition']
    
    rec_expression(condition['value'])
    
    if condition['type'] == "INSTRUCTION_FOR_TO":
        add_line(f"INFEQ")
    elif condition['type'] == "INSTRUCTION_FOR_DOWNTO":
        add_line(f"SUPEQ")
        
def rec_instruction_for_step(node):
    global table, code_machine_table
        
    var = node['var_control']['var']
    rec_expression(var)
    
    add_line(f"PUSHI 1")
    
    condition = node['condition']
        
    if condition['type'] == "INSTRUCTION_FOR_TO":
        add_line(f"ADD")
    elif condition['type'] == "INSTRUCTION_FOR_DOWNTO":
        add_line(f"SUB")
        
    rec_store_value_assign(var)

    
def rec_instruction_funcproc(node):
    global table, code_machine_table
        
    funcproc_name = node['funcproc_name'].lower()
    
    funcproc = get_ID(funcproc_name,SemFuncProc)
    
    if funcproc.isDefault is True:
        
        if funcproc_name in ['write','writeln']:
            rec_instruction_procedure_write(node['funcproc_args'], funcproc_name == 'writeln')
            
        elif funcproc_name in ['read','readln']:
            rec_instruction_procedure_read(node['funcproc_args'], funcproc_name == 'readln')
        
        elif funcproc_name == "length":
            rec_instruction_function_length(node['funcproc_args'])
            
        
    else:
        
        rec_instruction_funcproc_args(node['funcproc_args'])
        add_line(f"PUSHA funcproc{funcproc.vm_id}")
        add_line(f"CALL")
  
def rec_instruction_funcproc_args(node):
    global table, code_machine_table
        
    for arg in reversed(node['args_list']):
                
        rec_expression(arg)
        
  
def rec_instruction_function_length(node):
    global table, code_machine_table
        
    for arg in node['args_list']:
                                
        match arg['type']:
            
            case "VALUE_STRING":
                rec_expression(arg)
                add_line(f"STRLEN")
                
            case "VALUE_VAR":
                
                var_name = arg['name_var']
                var = get_ID(var_name,SemVar)
                
                if var.is_array is True:
                
                    var_length = var.max_range - var.min_range + 1
                    add_line(f"PUSHI {var_length}")
                    
                elif var.datatype == "string":
                    rec_expression(arg)
                    add_line(f"STRLEN")
                
                
  
def rec_instruction_procedure_write(node,needs_new_line):
    global table, code_machine_table
        
    for arg in node['args_list']:
        
        rec_expression(arg)
        
        sem_value = arg['sem_return']

        match sem_value.datatype:
            
            case "integer":
                add_line(f"WRITEI")
            case "real":
                add_line(f"WRITEF")
            case "string":
                add_line(f"WRITES")
            case "char":
                add_line(f"WRITECHR")
            case "boolean":
                add_line(f"WRITEI")
        
    if needs_new_line is True:
        add_line(f"WRITELN")
            
        
def rec_instruction_procedure_read(node,needs_new_line):
    global table, code_machine_table
                
    for arg in node['args_list']:
        
        rec_store_value_load(arg)
        add_line(f"READ")
        
        add_line(f"DUP 1")
        add_line(f"WRITES")
        
        sem_value = arg['sem_return']

        match sem_value.datatype:
            
            case "integer":
                add_line(f"ATOI")
            case "real":
                add_line(f"ATOF")
            case "char":
                add_line(f"ATOI")
            case "boolean":
                add_line(f"ATOI")
        
        rec_store_value_assign(arg)
        
    if needs_new_line is True:
        add_line(f"WRITELN")
        
            
    
def rec_instruction_walrus(node):
    global table, code_machine_table
        
    rec_store_value_load(node['var'])
    rec_expression(node['value'])
    rec_store_value_assign(node['var'])
        
    
def rec_binary_operation(node):
    global table, code_machine_table
        
    operator = node['operator'].lower()
            
    rec_expression(node['value_1'])
    rec_expression(node['value_2'])
            
    sem_value = node['sem_return']

    match operator:
        
        case "+":
                                                   
            if sem_value.datatype == "real":
                add_line(f"FADD")
                
            elif sem_value.datatype == "string":
                add_line(f"CONCAT")
                
            else:
                add_line(f"ADD")
            
            
        case "-":
            
            if sem_value.datatype == "real":
                add_line(f"FSUB")
                
            else:
                add_line(f"SUB")
            
        case "*":
            
            if sem_value.datatype == "real":
                add_line(f"FMUL")
                
            else:
                add_line(f"MUL")
            
        case "/":
            
            if sem_value.datatype == "real":
                add_line(f"FDIV")
                
            else:
                add_line(f"DIV")
            
        case "mod":
            
            add_line(f"MOD")
            
        case "div":
            
            add_line(f"DIV")
            
        case "=":
            
            add_line("EQUAL")
            
        case "<>":
            
            add_line("EQUAL")
            add_line("NOT")
            
        case ">":
            
            if sem_value.datatype == "real":
                add_line(f"FSUP")
                
            elif sem_value.datatype == "string":
                add_line(f"NOP //no string compare")
                
            else:
                add_line(f"SUP")
            
        case ">=":
            
            if sem_value.datatype == "real":
                add_line(f"FSUPEQ")
                
            elif sem_value.datatype == "string":
                add_line(f"NOP //no string compare")
                
            else:
                add_line(f"SUPEQ")
            
        case "<":
            
            if sem_value.datatype == "real":
                add_line(f"FINF")
                
            elif sem_value.datatype == "string":
                add_line(f"NOP //no string compare")
                
            else:
                add_line(f"INF")
            
        case "<=":
            
            if sem_value.datatype == "real":
                add_line(f"FINFEQ")
                
            elif sem_value.datatype == "string":
                add_line(f"NOP //no string compare")
                
            else:
                add_line(f"INFEQ")
            
        case "and":
            
            add_line(f"AND")
            
        case "or":
            
            add_line(f"OR")
            
        case "xor":
            
            add_line(f"NOP //XOR")


def rec_expression(node):
    global table, code_machine_table
                
    match node['type']:
        
        case "OPERATION_BINARY":
            return rec_binary_operation(node)
        
        case "OPERATION_UNARY":
            
            operator = node['operator']
            
            if operator.lower() == "not":
                
                rec_expression(node['value'])
                add_line(f"NOT")
        
        case "INSTRUCTION_FUNCPROC":
            rec_instruction_funcproc(node)
        
        case _ :
            rec_value(node)
            

def rec_value(node):
    global f,table
                
    sem_value = node['sem_return']

    match node['type']:
        
        case "VALUE_NUMBER":
            add_line(f"PUSHI {sem_value.value}")
            
        case "VALUE_NUMBER_REAL":
            add_line(f"PUSHF {sem_value.value}")
        
        case "VALUE_STRING":
            add_line(f"PUSHS \"{sem_value.value}\"")
        
        case "VALUE_CHAR":
            add_line(f"PUSHS \"{sem_value.value}\"")
            add_line(f"CHRCODE")
        
        case "VALUE_BOOLEAN":
            add_line(f"PUSHI {1 if sem_value.value is True else 0}")
        
        case "VALUE_VAR":
            
            var = get_ID(node['name_var'],SemVar)
            
            if var.isGlobal is True:
                add_line(f"PUSHG {var.vm_id}")
            else:        
                add_line(f"PUSHL {var.vm_id}")
            
        case "ARRAY_INDEX":
            
            array = get_ID(node['array_name'],SemVar)
                        
            if array.isGlobal is True:
                add_line(f"PUSHG {array.vm_id}")

            else:
                add_line(f"PUSHL {array.vm_id}")

            rec_expression(node['index'])

            if array.is_array is True:
                add_line(f"PUSHI {array.min_range}")
                add_line(f"SUB")
                add_line(f"LOADN")
                
            elif array.datatype == "string":
                add_line(f"PUSHI 1")
                add_line(f"SUB")
                add_line(f"CHARAT")
                
            
            
            
def rec_store_value_load(node):
    global f,table
                
    match node['type']:

        case "ARRAY_INDEX":
            
            array = get_ID(node['array_name'],SemVar)
                        
            if array.isGlobal is True:
                add_line(f"PUSHG {array.vm_id}")
            else:        
                add_line(f"PUSHL {array.vm_id}")
                
            rec_expression(node['index'])
            add_line(f"PUSHI {array.min_range}")
            add_line(f"SUB")
                
                
                
def rec_store_value_assign(node):
    global f,table
                
    match node['type']:

        case "VALUE_VAR":
            
            var = get_ID(node['name_var'],SemVar)
                        
            if var.isGlobal is True:
                add_line(f"STOREG {var.vm_id}")
            else:        
                add_line(f"STOREL {var.vm_id}")
            
        case "ARRAY_INDEX":
            
            array = get_ID(node['array_name'],SemVar)
                        
            if array.isGlobal is True:
                add_line(f"STOREN")
            else:        
                add_line(f"STOREN")
                                