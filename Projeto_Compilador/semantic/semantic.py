from semantic.sem_classes import *
import errors.error_handler as eh

def default_table():
    table = {}
    
    table['_func'] = SemFuncProc(None,'_func',0,False,True)
    table['write'] = SemFuncProc(None,'write',-1,False,True)
    table['writeln'] = SemFuncProc(None,'writeln',-1,False,True)
    table['read'] = SemFuncProc(None,'read',-1,False,True)
    table['readln'] = SemFuncProc(None,'readln',-1,False,True)
    
    arg_length = SemVar(None,"length",False,True,0,SemDatatype(None,"integer",False),False)
    table['length'] = SemFuncProc(None,'length',-1,True,True,"length",[arg_length])
    
    return table

sem = {}

def run_semantic_analysis(node,allow_opt):
    global sem
        
    sem = {}
    sem['table'] = default_table()
    sem['global_var_counter'] = 0
    sem['local_var_counter'] = 0
    sem['funcproc_counter'] = 1
    sem['current_table'] = None
    sem['allow_opt'] = allow_opt
    
    is_semantically_valid,ast_fully_analised = analyse_program(node)
    
    collect_warnings()
    
    return is_semantically_valid,ast_fully_analised,sem



def collect_warnings():
    global sem
    
    for item_name in sem['table']:
        
        item = get_ID(item_name,None)
                
        if isinstance(item,SemVar):
            
            if item.read_ctr == 0 and item.write_ctr == 0:
                eh.add_semantic_warning(item.token,f"Unused global variable {item_name}")
            
            elif item.read_ctr == 0:
                eh.add_semantic_warning(item.token,f"Global variable {item_name} never read")
                
            elif item.write_ctr == 0:
                eh.add_semantic_warning(item.token,f"Global variable {item_name} never had any value assigned to")
            
        elif isinstance(item,SemFuncProc):
            
            if item.isDefault is False or item.funcproc_name == "_func":
                                
                if item.read_ctr == 0 and item.funcproc_name != '_func':
                    eh.add_semantic_warning(item.token,"Function/Procedure never used")
                    
                else:
                                        
                    sem['current_table'] = item_name
                    
                    for funcproc_item_name in item.table:

                        funcproc_item = get_ID(funcproc_item_name,SemVar)
        
                        if isinstance(funcproc_item,SemVar):

                            if funcproc_item.read_ctr == 0 and funcproc_item.write_ctr == 0:
                                eh.add_semantic_warning(funcproc_item.token,f"Unused local variable {funcproc_item_name}")

                            elif funcproc_item.read_ctr == 0 and funcproc_item.var_name != item_name:
                                eh.add_semantic_warning(funcproc_item.token,f"Local variable {funcproc_item_name} never read")

                            elif funcproc_item.write_ctr == 0:
                                eh.add_semantic_warning(funcproc_item.token,f"Local variable {funcproc_item_name} never had any value assigned to")
                                
                    sem['current_table'] = None
    


def does_name_exist(name):
    global sem
    
    current_funcproc = sem['current_table']
    
    if name in sem['table']:
        return True
    
    elif current_funcproc is not None and name in sem['table'][current_funcproc].table:
        return True
    
    else:
        return False


def get_ID(name,preferenceType):
    global sem
    
    var = None
    current_funcproc = sem['current_table']
    
    if name in sem['table'] and (preferenceType is None or (preferenceType is not None and isinstance(sem['table'][name],preferenceType))):
        var = sem['table'][name]
    
    if current_funcproc is not None and name in sem['table'][current_funcproc].table and (preferenceType is None or (preferenceType is not None and isinstance(sem['table'][current_funcproc].table[name],preferenceType))):
        var = sem['table'][current_funcproc].table[name]
    
    return var
    
    
def set_readOnly_ID(name,bool,isGlobal):
    global sem
    
    current_funcproc = sem['current_table']
    
    if name in sem['table'] and isGlobal is True:
        sem['table'][name].readOnly = bool
    
    elif current_funcproc is not None and name in sem['table'][current_funcproc].table:
        sem['table'][current_funcproc].table[name].readOnly = bool

    
def add_write_ID(name,isGlobal):
    global sem
            
    current_funcproc = sem['current_table']
                                
    if name in sem['table'] and isGlobal is True:
        sem['table'][name].write_ctr += 1
    
    elif current_funcproc is not None and name in sem['table'][current_funcproc].table:
        sem['table'][current_funcproc].table[name].write_ctr += 1
    
    
    
def add_read_ID(name,isGlobal):
    global sem
    
    current_funcproc = sem['current_table']
    
    if name in sem['table'] and isGlobal is True:
        sem['table'][name].read_ctr += 1
    
    elif current_funcproc is not None and name in sem['table'][current_funcproc].table:
        sem['table'][current_funcproc].table[name].read_ctr += 1
    
    

def add_var(var,isGlobal):
    global sem
    
    current_funcproc = sem['current_table']
    
    if isGlobal is True:
        sem['table'][var.var_name] = var
    else:
        sem['table'][current_funcproc].table[var.var_name] = var    



def add_arg_funcproc(funcproc_name,arg):
    global sem
    
    sem['table'][funcproc_name].args.append(arg)
    



def analyse_program(node):
    global sem

    node['sem_return'] = None

    program_name = node['program_name'].lower()
                                                
    if does_name_exist(program_name) is False:

        program = SemProgram(node['token'],program_name)
        sem['table'][program_name] = program
                
        global_vars_valid, global_vars_node = analyse_global_vars(node['global_vars'])
        funcproc_declaration_valid, funcproc_decl_node = analyse_funcproc_declaration(node['funcproc_list'])
                
        sem['current_table'] = '_func'
        sem['local_var_counter'] = 0
        
        local_vars_valid, local_vars_node = analyse_local_vars(node['local_vars'])
        code_block_valid, code_block = analyse_code_block(node['code_block'])
                        
        node['code_block'] = code_block
        node['global_vars'] = global_vars_node
        node['local_vars'] = local_vars_node
        node['funcproc_list'] = funcproc_decl_node
        
        sem['current_table'] = None
        
        if global_vars_valid is True and local_vars_valid is True and code_block_valid is True and funcproc_declaration_valid is True:
            return True, node
        
        else:
            return False, node    
        
    else:
        eh.add_semantic_error(node['token'],f"Program name {program_name} already exists")
        return False,node


def analyse_global_vars(node):
    global sem
                  
    node['sem_return'] = None
                                            
    for global_var in node["var_global_list"]:
                  
        is_var_decl_valid,_ = analyse_var_decl(global_var,True)
                     
        if is_var_decl_valid is False:
            return False, node           
    
    return True,node


def analyse_funcproc_declaration(node):
    global sem
                               
    node['sem_return'] = None
                            
    isValid = True
                                
    for i,funcproc_decl in enumerate(node["funcproc_list"]):
                                    
        sem['local_var_counter'] = 0
                          
        if funcproc_decl['type'] == "FUNCTION":
            
            is_func_valid, func_node = analyse_function_decl(funcproc_decl)
            node['funcproc_list'][i] = func_node
            
            if is_func_valid is False:
                isValid = False
            
        elif funcproc_decl['type'] == "PROCEDURE":
            
            is_proc_valid, proc_node = analyse_procedure_decl(funcproc_decl)
            node['funcproc_list'][i] = proc_node
            
            if is_proc_valid is False:
                isValid = False
            
        else:
            isValid = False         
    
    return isValid,node


def analyse_function_decl(node):
    global sem
                  
    node['sem_return'] = None
    func_name = node['function_name'].lower()
    
    if does_name_exist(func_name) is True:
        return False, node
    
    is_return_value_valid, return_value_node = analyse_datatype(node['return_value'])
    return_value = return_value_node['sem_return']
    
    if is_return_value_valid is False or isinstance(return_value,SemDatatype) is False:
        return False, node
    
    sem["current_table"] = func_name
    
    return_value_var = SemVar(node['token'],func_name,False,True,0,return_value,False)
    sem['local_var_counter'] += 1
    
    funcproc_vm_id = sem['funcproc_counter']
    sem['funcproc_counter'] += 1
    sem['table'][func_name] = SemFuncProc(node['token'],func_name,funcproc_vm_id,True,False,func_name,[])
    
    add_var(return_value_var,False)
    
    are_args_valid, args_node = analyse_funcproc_args_decl(func_name,node['args'])
             
    if are_args_valid is False:
        sem["current_table"] = None
        return False, node
    
    
    is_local_vars_valid, local_vars_node = analyse_local_vars(node['local_vars'])
    is_func_code_valid, func_code = analyse_code_block(node['function_code'])
    
    if is_local_vars_valid is False or is_func_code_valid is False:
        sem["current_table"] = None
        return False, node
    
    else:
        
        node['function_code'] = func_code
        node['args'] = args_node
        node['local_vars'] = local_vars_node
        
        return_value_var = get_ID(func_name,SemVar)
        sem["current_table"] = None
        
        if return_value_var.write_ctr == 0:
            eh.add_semantic_error(node['token'],f"No return value in {func_name} function assigned")
            return False, node
                        
        
        return True, node
    
    
    
def analyse_procedure_decl(node):
    global sem
                  
    node['sem_return'] = None
    proc_name = node['procedure_name'].lower()
    
    if does_name_exist(proc_name) is True:
        return False, node
    
    sem["current_table"] = proc_name
    
    proc_vm_id = sem['funcproc_counter']
    sem['funcproc_counter'] += 1
    sem['table'][proc_name] = SemFuncProc(node['token'],proc_name,proc_vm_id,False,False,proc_name,[])
        
    are_args_valid, args_node = analyse_funcproc_args_decl(proc_name,node['args'])
             
    if are_args_valid is False:
        sem["current_table"] = None
        return False, node
    
    
    is_local_vars_valid, local_vars_node = analyse_local_vars(node['local_vars'])
    is_proc_code_valid, proc_code = analyse_code_block(node['procedure_code'])
    
    if is_local_vars_valid is False or is_proc_code_valid is False:
        sem["current_table"] = None
        return False, node
    
    else:
        
        node['procedure_code'] = proc_code
        node['args'] = args_node
        node['local_vars'] = local_vars_node
        sem["current_table"] = None
        return True, node
    
    
    
def analyse_funcproc_args_decl(funcproc_name,node):
    global sem

    for arg_decl in node['args_list']:
        
        is_datatype_valid, datatype_node = analyse_datatype(arg_decl['data_type'])
        datatype = datatype_node['sem_return']
        
        if is_datatype_valid is False or isinstance(datatype,SemDatatype) is False:
            return False, node
                
        arg_name = arg_decl['var_name'].lower()
        
        if does_name_exist(arg_name) is True:
            return False, node
        
        arg_vm_id = sem['local_var_counter']
        sem['local_var_counter'] += 1
        
        arg_declaration = SemVar(node['token'],arg_name,False,True,arg_vm_id,datatype)
        add_arg_funcproc(funcproc_name,arg_declaration)
        add_var(arg_declaration,False)
        
    return True, node
    
    

def analyse_local_vars(node):
    global sem
           
    node['sem_return'] = None
                                                            
    for i,local_var in enumerate(node["var_local_list"]):

        is_var_decl_valid,local_var_node = analyse_var_decl(local_var,False)                   
        node['var_local_list'][i] = local_var_node
                                         
        if is_var_decl_valid is False:
            return False, node            
        
    return True,node



def analyse_var_decl(node,isGlobal):
    global sem
              
    node['sem_return'] = None
                
    isValid = True
    
    is_datatype_valid,data_type_node = analyse_datatype(node['data_type'])
    data_type = data_type_node['sem_return']
                                
    if is_datatype_valid is False:
        return False,node
                
                
    for var_name in node["var_names_list"]:
            
        var_name = var_name.lower()
        
        if isGlobal is True:
            
            if does_name_exist(var_name) is True:
                eh.add_semantic_error(node['token'],f"Global variable {var_name} has duplicate ID")
                isValid = False
                
            else:
                
                global_id = sem['global_var_counter']
                sem['global_var_counter'] += 1
                    
                var = SemVar(node['token'],var_name,True,False,global_id,data_type)
                add_var(var,isGlobal)
                
        else:
                        
            if does_name_exist(var_name) is True:
                eh.add_semantic_error(node['token'],f"Local variable {var_name} has duplicate ID")
                isValid = False
                
            else:
                
                local_id = sem['local_var_counter']
                sem['local_var_counter'] += 1
                
                var = SemVar(node['token'],var_name,False,False,local_id,data_type)
                add_var(var,isGlobal)
        
    return isValid,node



def analyse_datatype(node):
    global sem
       
    node['sem_return'] = None
       
    datatype = node['data_type'].lower()
    is_array = node['is_array']
        
    if is_array is True:
        
        min_range = int(node['min_range'])
        max_range = int(node['max_range'])
        
        if min_range < max_range:
            
            node['sem_return'] = SemDatatype(node['token'],datatype,is_array,min_range,max_range)
            return True,node
        
        else:
            eh.add_semantic_error(node['token'],f"Array minimal range has to be equal or smaller that maximum range")
            return False, node
        
    else:
        
        node['sem_return'] = SemDatatype(node['token'],datatype,is_array)
        return True,node



def analyse_mini_code_block(node):
    global sem
                 
    node['sem_return'] = None
                                                                                         
    if node['type'] == "CODE_BLOCK":
        return analyse_code_block(node)
    else:
        return analyse_instruction(node)    



def analyse_code_block(node):
    global sem
            
    node['sem_return'] = None
                                
    isValid = True
                
    for i,instruction in enumerate(node['instructions_list']):
        
        is_instruction_valid,instruction_node = analyse_instruction(instruction)

        if is_instruction_valid is False:
            isValid = False
        else:
            node['instructions_list'][i] = instruction_node

    return isValid,node



def analyse_instruction(node):
    global sem
        
    node['sem_return'] = None
        
    match node['type']:
        
        case "INSTRUCTION_FUNCPROC":
            return analyse_instruction_funcproc(node)
            
        case "INSTRUCTION_IF_ELSE":
            return analyse_instruction_if_else(node)
        
        case "INSTRUCTION_FOR":
            return analyse_instruction_for(node)
        
        case "INSTRUCTION_WHILE":
            return analyse_instruction_while(node)
        
        case "INSTRUCTION_WALRUS":
            return analyse_instruction_walrus(node)
                
        case _:
            eh.add_semantic_error(node['token'],f"The {node['type']} instruction is invalid")
            return False, node



def analyse_instruction_for(node):
    global sem
    
    node['sem_return'] = None
    
    is_var_valid, var = analyse_instruction_walrus(node['var_control'])
    var_value = var['sem_return']
    
    if is_var_valid is False and isinstance(var_value,SemValue) and var_value.varName is not None:
        return False, node

    if var_value.datatype in ['integer','boolean','char']:
        
        var_control = get_ID(var_value.varName,SemVar)
        
        set_readOnly_ID(var_value.varName, True,var_control.isGlobal)
        is_body_valid, body = analyse_mini_code_block(node['body'])
        set_readOnly_ID(var_value.varName,False,var_control.isGlobal)
        
        is_condition_valid, condition_node = analyse_instruction_for_final(node['condition'])
        
        if is_condition_valid is False or is_body_valid is False or isinstance(condition_node['sem_return'],SemValue) is False:
            return False, node
        
        
        elif var_value.datatype != condition_node['sem_return'].datatype:
            eh.add_semantic_error(node['token'],f"Control variable datatype has to be the same as for value range")
            return False, node
        
        else:
            
            node['var_control'] = var
            node['body'] = body
            node['condition'] = condition_node
            
            return True, node
        
    else:
        eh.add_semantic_error(node['token'],f"Control variable in for loop doesn't allow {var_value.datatype} datatype")
        return False, node
    
    
    
def analyse_instruction_for_final(node):
    global sem
    
    node['sem_return'] = None
    
    is_value_valid, value_node = analyse_expression(node['value'])
    value = value_node['sem_return']
    
    if is_value_valid is False or isinstance(value,SemValue) is False:
        return False, node
    
    if value.datatype in ['integer','boolean','char']:
        
        node['value'] = value_node
        node['sem_return'] = value
        
        match node['type']:
            
            case "INSTRUCTION_FOR_DOWNTO":
                return True,node
                
            case "INSTRUCTION_FOR_TO":
                return True,node
            
            case _:
                eh.add_semantic_error(node['token'],f"Unknown for instruction")
                return False, node
        
    else:
        eh.add_semantic_error(node['token'],f"End point of for loop has an incompatible type")
        return False, node
    


def analyse_instruction_if_else(node):
    global sem
    
    node['sem_return'] = None
    
    is_condition_valid, condition = analyse_expression(node['condition'])
    condition_value = condition['sem_return']
    
    is_body_if_valid, body_if = analyse_mini_code_block(node['body_if'])
    
    if is_condition_valid is False or is_body_if_valid is False:
        return False, node
    
    
    if isinstance(condition_value,SemValue) is False:
        eh.add_semantic_error(node['token'],f"If condition has to be a value")
        return False, node


    if condition_value.datatype == "boolean":
        
        body_else = None
        
        if node['body_else'] is not None:
        
            is_body_else_valid, body_else_node = analyse_mini_code_block(node['body_else'])
        
            if is_body_else_valid is False:
                return False, node
            else:
                body_else = body_else_node
        
        node['body_if'] = body_if
        node['body_else'] = body_else
        node['condition'] = condition
        return True, node        
        
    else:
        eh.add_semantic_error(node['token'],f"If conditions only accept boolean values")
        return False, node



def analyse_instruction_while(node):
    global sem
    
    node['sem_return'] = None
    
    is_condition_valid, condition = analyse_expression(node['condition'])
    condition_value = condition['sem_return']
    
    is_body_valid, body = analyse_mini_code_block(node['body'])
    
    if is_condition_valid is False or is_body_valid is False:
        return False, node
    
    if isinstance(condition_value,SemValue) is False:
        eh.add_semantic_error(node['token'],f"While condition has to be a value")
        return False, node

    if condition_value.datatype == "boolean":
        
        node['body'] = body
        node['condition'] = condition
        return True, node        
        
    else:
        eh.add_semantic_error(node['token'],f"While condition has to be a boolean value")
        return False, node



def analyse_instruction_walrus(node):
    global sem
        
    node['sem_return'] = None
        
    is_var_valid, var = analyse_value(node['var'],False)
    var_value = var['sem_return']
        
    if is_var_valid is False or isinstance(var_value,SemValue) is False or var_value.varName is None:
        return False, node

    is_value_valid, value_node = analyse_expression(node['value'])
    value = value_node['sem_return']
        
    if is_value_valid is False or isinstance(value,SemValue) is False:
        return False, node
    
    if var_value.datatype == value.datatype:
        
        var_obj = get_ID(var_value.varName,SemVar)
        
        if var_obj.readOnly is False:
            
            node['value'] = value_node
            node['var'] = var
            add_write_ID(var_value.varName,var_obj.isGlobal)
            
            node['sem_return'] = SemValue(False,var_value.datatype,None,var_value.varName)
        
            return True, node
            
        else:
            eh.add_semantic_error(node['token'],f"Cannot assign value to a read-only variable")
            return False, node
        
    else:
        eh.add_semantic_error(node['token'],f"Datatype of variable is different of datatype of value assigned into")
        return False, node


def default_procedure_read_assign_value(arg):
    
    if arg['sem_return'] is not None and isinstance(arg['sem_return'],SemValue) is True:
    
        var = get_ID(arg['sem_return'].varName,SemVar)
        add_write_ID(var.var_name,var.isGlobal)
    


def analyse_instruction_funcproc(node):
    global sem
        
    isValid = True
    
    node['sem_return'] = None
    funcproc_name = node['funcproc_name'].lower()
    funcproc = get_ID(funcproc_name,SemFuncProc)
                                
    if does_name_exist(funcproc_name) is True and isinstance(funcproc,SemFuncProc) is True:

        
        if funcproc.isDefault is True:

            limited_args = True
            limit_of_args = 0
            arg_condition = None
            arg_transformation = None
            arg_condition_error_string = "..."

            if funcproc_name in ['writeln','write']:
                    
                limited_args = False
                    
            elif funcproc_name in ['read','readln']:
                
                limited_args = False
                arg_condition = lambda arg : isinstance(arg['sem_return'],SemValue) is True and arg['sem_return'].varName is not None
                arg_transformation = default_procedure_read_assign_value
                arg_condition_error_string = "Read default procedure only applies to variables"

            elif funcproc_name == "length":
                
                limited_args = True
                limit_of_args = 1
                arg_condition = lambda arg : isinstance(arg['sem_return'],SemValue) is True and (arg['sem_return'].datatype == "string" or (arg['sem_return'].varName is not None and isinstance(get_ID(arg['sem_return'].varName,SemVar),SemVar) is True and get_ID(arg['sem_return'].varName,SemVar).is_array is True))
                arg_condition_error_string = "Length default function only applies to string and arrays"
                node['sem_return'] = SemValue(False,"integer",None,None)

            else:
                eh.add_semantic_error(node['token'],f"Unknown default function name : {funcproc_name}")
                return False, node

            funcproc_args_valid, funcproc_args = analyse_instruction_funcproc_default_args(node['funcproc_args'],limited_args,limit_of_args,arg_condition,arg_condition_error_string,arg_transformation)
        
            if funcproc_args_valid is True:
                node['funcproc_args'] = funcproc_args
                return True, node
                
            else:
                return False, node

        else:
            
            funcproc_args_valid, funcproc_args = analyse_instruction_funcproc_args(funcproc_name,node['funcproc_args'])
            
            if funcproc_args_valid is False:
                return False, node   
            
            node['funcproc_args'] = funcproc_args
            add_read_ID(funcproc_name,True)
        
            if funcproc.isFunction is False:
                node['sem_return'] = None
                
            else:
                
                return_value = funcproc.table[funcproc.return_id]
                node['sem_return'] = SemValue(False,return_value.datatype,None,None)
            
            return True,node    
        
            
    else:
        eh.add_semantic_error(node['token'],f"Unknown function name : {funcproc_name}")
        return False, node



def analyse_instruction_funcproc_args(funcproc_name,node):
    global sem
        
    isValid = True
    
    funcproc = get_ID(funcproc_name,SemFuncProc)
    args_limit = len(funcproc.args)
    args_list = funcproc.args
    
    for i,arg in enumerate(node['args_list']):
                
        is_arg_valid,arg_collected = analyse_expression(arg)
        arg_sem = arg_collected['sem_return']
                                                
        if is_arg_valid is False:
            isValid = False
            
        if isinstance(arg_sem,SemValue) is False:
            eh.add_semantic_error(node['token'],f"Arguments in a procedure or function must be values")
            isValid = False
            
        node['args_list'][i] = arg_collected
         
        if args_limit < 0:
            eh.add_semantic_error(node['token'],f"Less arguments that expected")
            return False, node
         
        var = get_ID(arg_sem.varName,SemVar)
        
        if arg_sem.varName is None and args_list[i].datatype != arg_sem.datatype:
            eh.add_semantic_error(node['token'],f"Invalid datatype in arguments")
            return False, node
            
        elif arg_sem.varName is not None:
            
            if args_list[i].datatype != var.datatype:
                eh.add_semantic_error(node['token'],f"Invalid datatype in arguments")
                return False, node
            
            elif args_list[i].datatype == var.datatype and args_list[i].is_array != var.is_array:
                eh.add_semantic_error(node['token'],f"Invalid datatype in arguments. Array and variable are not compatible")
                return False, node
            
                
        args_limit -= 1
      
    if args_limit != 0:
        eh.add_semantic_error(node['token'],f"More arguments expected")
        return False, node
      
    
    return isValid, node




def analyse_instruction_funcproc_default_args(node,limited_args,limit_of_args, arg_cond = None,arg_cond_false_string = None,arg_transformation = None):
    global sem
    
    isValid = True
    
    for i,arg in enumerate(node['args_list']):
        
        limit_of_args -= 1
        
        is_arg_valid,arg_collected = analyse_expression(arg)
        arg_sem = arg_collected['sem_return']
                        
        if is_arg_valid is False:
            isValid = False
            
        if isinstance(arg_sem,SemValue) is False:
            eh.add_semantic_error(node['token'],f"Procedure or function arguments must be values")
            isValid = False
            
        node['args_list'][i] = arg_collected
                
        if arg_cond is not None and arg_cond(arg_collected) is False:
            eh.add_semantic_error(node['token'],f"{arg_cond_false_string}")
            isValid = False
            
        if arg_transformation is not None:
            arg_transformation(arg)
            
    if limited_args is True and limit_of_args != 0:
        eh.add_semantic_error(node['token'],f"Miscount number of arguments in function/procedure calls")
        isValid = False
    
    return isValid, node




def analyse_binary_operation(node):
    global sem
 
    node['sem_return'] = None
        
    operator = node['operator'].lower()
            
    value1_is_valid, value1_node = analyse_expression(node['value_1'])
    value2_is_valid, value2_node = analyse_expression(node['value_2'])
        
    value1 = value1_node['sem_return']
    value2 = value2_node['sem_return']
        
    if value1_is_valid is False or value2_is_valid is False or isinstance(value1,SemValue) is False or isinstance(value2,SemValue) is False:
        return False,node
                
    node['value_1'] = value1_node
    node['value_2'] = value2_node
                
    match operator:
        
        case "+":
                                                   
            if value1.datatype in ['integer','real'] and value2.datatype in ['integer','real']:
                         
                if value1.datatype == "real" or value2.datatype == "real":
                    
                    if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                        new_value = float(value1.value) + float(value2.value)
                        
                        new_node = {
                            "token" : value1_node['token'],
                            "type" : "VALUE_NUMBER_REAL",
                            "value" : new_value
                        }
                    
                        new_node['sem_return'] = SemValue(True,"real",new_value,None)
                        return True,new_node
                    
                    else:
                        
                        node['sem_return'] = SemValue(False,"real",None,None)
                        return True,node
                    
                else:
                    
                    if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                        new_value = int(value1.value) + int(value2.value)
                        
                        new_node = {
                            "token" : value1_node['token'],
                            "type" : "VALUE_NUMBER",
                            "value" : new_value
                        }
                    
                        new_node['sem_return'] = SemValue(True,"integer",new_value,None)
                        return True,new_node
                    
                    else:
                        
                        node['sem_return'] = SemValue(False,"integer",None,None)
                        return True,node
                            
                
                
                            
            elif value1.datatype in ['string','char'] and value2.datatype in ['string','char']:
                    
                if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                    new_value = value1.value + value2.value
                        
                    new_node = {
                        "token" : value1_node['token'],
                        "type" : "VALUE_STRING",
                        "value" : new_value
                    }
                    
                    new_node['sem_return'] = SemValue(True,"string",new_value,None)
                    return True,new_node
                    
                else:
                    
                    node['sem_return'] = SemValue(False,"string",None,None)
                    return True,node
                    
            else:
                eh.add_semantic_error(node['token'],f"Incompatible types in add operation")
                return False,node
            
            
        case "-":
            
            if value1.datatype in ['integer','real'] and value2.datatype in ['integer','real']:
                         
                if value1.datatype == "real" or value2.datatype == "real":
                    
                    if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                        new_value = float(value1.value) - float(value2.value)
                        
                        new_node = {
                            "token" : value1_node['token'],
                            "type" : "VALUE_NUMBER_REAL",
                            "value" : new_value
                        }
                    
                        new_node['sem_return'] = SemValue(True,"real",new_value,None)
                        return True,new_node
                    
                    else:
                        
                        node['sem_return'] = SemValue(False,"real",None,None)
                        return True,node
                    
                else:
                    
                    if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                        new_value = int(value1.value) - int(value2.value)
                        
                        new_node = {
                            "token" : value1_node['token'],
                            "type" : "VALUE_NUMBER",
                            "value" : new_value
                        }
                    
                        new_node['sem_return'] = SemValue(True,"integer",new_value,None)
                        return True,new_node
                    
                    else:
                        
                        node['sem_return'] = SemValue(False,"integer",None,None)
                        return True,node

            else:
                eh.add_semantic_error(node['token'],f"Incompatible types in subtraction operation")
                return False,node
            
        case "*":
            
            if value1.datatype in ['integer','real'] and value2.datatype in ['integer','real']:
                         
                if value1.datatype == "real" or value2.datatype == "real":
                    
                    if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                        new_value = float(value1.value) * float(value2.value)
                        
                        new_node = {
                            "token" : value1_node['token'],
                            "type" : "VALUE_NUMBER_REAL",
                            "value" : new_value
                        }
                    
                        new_node['sem_return'] = SemValue(True,"real",new_value,None)
                        return True,new_node
                    
                    else:
                        
                        node['sem_return'] = SemValue(False,"real",None,None)
                        return True,node
                    
                else:
                    
                    if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                        new_value = int(value1.value) * int(value2.value)
                        
                        new_node = {
                            "token" : value1_node['token'],
                            "type" : "VALUE_NUMBER",
                            "value" : new_value
                        }
                    
                        new_node['sem_return'] = SemValue(True,"integer",new_value,None)
                        return True,new_node
                    
                    else:
                        
                        node['sem_return'] = SemValue(False,"integer",None,None)
                        return True,node

            else:
                eh.add_semantic_error(node['token'],f"Incompatible types in multiplication operation")
                return False,node
            
        case "/":
            
            if value1.datatype in ['integer','real'] and value2.datatype in ['integer','real']:
                                             
                if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                    
                    if value2.value != 0:
                    
                        new_value = float(value1.value) / float(value2.value)

                        new_node = {
                            "token" : value1_node['token'],
                            "type" : "VALUE_NUMBER_REAL",
                            "value" : new_value
                        }

                        new_node['sem_return'] = SemValue(True,"real",new_value,None)
                        return True,new_node
                    
                    else:
                        eh.add_semantic_warning(node['token'],f"Division by zero")
                        node['sem_return'] = SemValue(False,"real",None,None)
                        return True,node
                    
                else:
                    
                    node['sem_return'] = SemValue(False,"real",None,None)
                    return True,node
                    

            else:
                eh.add_semantic_error(node['token'],f"Incompatible types in division operation")
                return False,node
            
        case "mod":
            
            if value1.datatype == "integer" and value2.datatype == "integer":
                                             
                if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                    
                    new_value = int(value1.value) % int(value2.value)
                    
                    new_node = {
                        "token" : value1_node['token'],
                        "type" : "VALUE_NUMBER",
                        "value" : new_value
                    }
                    
                    new_node['sem_return'] = SemValue(True,"integer",new_value,None)
                    return True,new_node
                    
                else:
                    
                    node['sem_return'] = SemValue(False,"integer",None,None)
                    return True,node

            else:
                eh.add_semantic_error(node['token'],f"Incompatible types in mod operation")
                return False,node
            
        case "div":
            
            if value1.datatype == "integer" and value2.datatype == "integer":
                                             
                if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                    
                    new_value = int(value1.value) / int(value2.value)
                    
                    new_node = {
                        "token" : value1_node['token'],
                        "type" : "VALUE_NUMBER",
                        "value" : new_value
                    }
                    
                    new_node['sem_return'] = SemValue(True,"integer",new_value,None)
                    return True,new_node
                    
                else:
                    
                    node['sem_return'] = SemValue(False,"integer",None,None)
                    return True,node

            else:
                eh.add_semantic_error(node['token'],f"Incompatible types in div operation")
                return False,node
            
        case "=":
            
            if value1.datatype in ['integer','real'] and value2.datatype in ['integer','real']:
                         
                if value1.datatype == "real" or value2.datatype == "real":
                    
                    if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                        new_value = float(value1.value) == float(value2.value)
                        
                        new_node = {
                            "token" : value1_node['token'],
                            "type" : "VALUE_BOOLEAN",
                            "value" : new_value
                        }

                        new_node['sem_return'] = SemValue(True,"boolean",new_value,None)
                        return True,new_node
                    
                    else:
                        
                        node['sem_return'] = SemValue(False,"boolean",None,None)
                        return True,node
                    
                else:
                    
                    if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                        new_value = int(value1.value) == int(value2.value)
                        
                        new_node = {
                            "token" : value1_node['token'],
                            "type" : "VALUE_BOOLEAN",
                            "value" : new_value
                        }
                    
                        new_node['sem_return'] = SemValue(True,"boolean",new_value,None)
                        return True,new_node
                    
                    else:
                        
                        node['sem_return'] = SemValue(False,"boolean",None,None)
                        return True,node
                            
                
                
                            
            elif value1.datatype in ['string','char'] and value2.datatype in ['string','char']:
                    
                if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                    new_value = value1.value == value2.value
                        
                    new_node = {
                        "token" : value1_node['token'],
                        "type" : "VALUE_BOOLEAN",
                        "value" : new_value
                    }
                    
                    new_node['sem_return'] = SemValue(True,"boolean",new_value,None)
                    return True,new_node
                    
                else:
                    
                    node['sem_return'] = SemValue(False,"boolean",None,None)
                    return True,node
                
            elif value1.datatype == "boolean" and value2.datatype == "boolean":
                    
                if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                    new_value = value1.value == value2.value
                        
                    new_node = {
                        "token" : value1_node['token'],
                        "type" : "VALUE_BOOLEAN",
                        "value" : new_value
                    }
                    
                    new_node['sem_return'] = SemValue(True,"boolean",new_value,None)
                    return True,new_node
                    
                else:
                    
                    node['sem_return'] = SemValue(False,"boolean",None,None)
                    return True,node
                    
            else:
                eh.add_semantic_error(node['token'],f"Incompatible types in equals operation")
                return False,node
            
        case "<>":
            
            if value1.datatype in ['integer','real'] and value2.datatype in ['integer','real']:
                         
                if value1.datatype == "real" or value2.datatype == "real":
                    
                    if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                        new_value = float(value1.value) != float(value2.value)
                        
                        new_node = {
                            "token" : value1_node['token'],
                            "type" : "VALUE_BOOLEAN",
                            "value" : new_value
                        }
                    
                        new_node['sem_return'] = SemValue(True,"boolean",new_value,None)
                        return True,new_node
                    
                    else:
                        
                        node['sem_return'] = SemValue(False,"boolean",None,None)
                        return True,node
                    
                else:
                    
                    if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                        new_value = int(value1.value) != int(value2.value)
                        
                        new_node = {
                            "token" : value1_node['token'],
                            "type" : "VALUE_BOOLEAN",
                            "value" : new_value
                        }
                    
                        new_node['sem_return'] = SemValue(True,"boolean",new_value,None)
                        return True,new_node
                    
                    else:
                        
                        node['sem_return'] = SemValue(False,"boolean",None,None)
                        return True,node
                            
                
                
                            
            elif value1.datatype in ['string','char'] and value2.datatype in ['string','char']:
                    
                if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                    new_value = value1.value != value2.value
                        
                    new_node = {
                        "token" : value1_node['token'],
                        "type" : "VALUE_BOOLEAN",
                        "value" : new_value
                    }
                    
                    new_node['sem_return'] = SemValue(True,"boolean",new_value,None)
                    return True,new_node
                    
                else:
                    
                    node['sem_return'] = SemValue(False,"boolean",None,None)
                    return True,node
                
            elif value1.datatype == "boolean" and value2.datatype == "boolean":
                    
                if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                    new_value = value1.value != value2.value
                        
                    new_node = {
                        "token" : value1_node['token'],
                        "type" : "VALUE_BOOLEAN",
                        "value" : new_value
                    }
                    
                    new_node['sem_return'] = SemValue(True,"boolean",new_value,None)
                    return True,new_node
                    
                else:
                    
                    node['sem_return'] = SemValue(False,"boolean",None,None)
                    return True,node
                    
            else:
                eh.add_semantic_error(node['token'],f"Incompatible types in not equal operation")
                return False,node
            
        case ">":
            
            if value1.datatype in ['integer','real'] and value2.datatype in ['integer','real']:
                         
                if value1.datatype == "real" or value2.datatype == "real":
                    
                    if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                        new_value = float(value1.value) > float(value2.value)
                        
                        new_node = {
                            "token" : value1_node['token'],
                            "type" : "VALUE_BOOLEAN",
                            "value" : new_value
                        }
                    
                        new_node['sem_return'] = SemValue(True,"boolean",new_value,None)
                        return True,new_node
                    
                    else:
                        
                        node['sem_return'] = SemValue(False,"boolean",None,None)
                        return True,node
                    
                else:
                    
                    if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                        new_value = int(value1.value) > int(value2.value)
                        
                        new_node = {
                            "token" : value1_node['token'],
                            "type" : "VALUE_BOOLEAN",
                            "value" : new_value
                        }
                        
                        new_node['sem_return'] = SemValue(True,"boolean",new_value,None)
                        return True,new_node
                    
                    else:
                        
                        node['sem_return'] = SemValue(False,"boolean",None,None)
                        return True,node
                            
                
                
                            
            elif value1.datatype in ['string','char'] and value2.datatype in ['string','char']:
                    
                if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                    new_value = value1.value > value2.value
                        
                    new_node = {
                        "token" : value1_node['token'],
                        "type" : "VALUE_BOOLEAN",
                        "value" : new_value
                    }
                    
                    new_node['sem_return'] = SemValue(True,"boolean",new_value,None)
                    return True,new_node
                    
                else:
                    
                    node['sem_return'] = SemValue(False,"boolean",None,None)
                    return True,node
                
            elif value1.datatype == "boolean" and value2.datatype == "boolean":
                    
                if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                    new_value = value1.value > value2.value
                        
                    new_node = {
                        "token" : value1_node['token'],
                        "type" : "VALUE_BOOLEAN",
                        "value" : new_value
                    }
                    
                    new_node['sem_return'] = SemValue(True,"boolean",new_value,None)
                    return True,new_node
                    
                else:
                    
                    node['sem_return'] = SemValue(False,"boolean",None,None)
                    return True,node
                    
            else:
                eh.add_semantic_error(node['token'],f"Incompatible types in greater than operation")
                return False,node
            
        case ">=":
            
            if value1.datatype in ['integer','real'] and value2.datatype in ['integer','real']:
                         
                if value1.datatype == "real" or value2.datatype == "real":
                    
                    if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                        new_value = float(value1.value) >= float(value2.value)
                        
                        new_node = {
                            "token" : value1_node['token'],
                            "type" : "VALUE_BOOLEAN",
                            "value" : new_value
                        }
                    
                        new_node['sem_return'] = SemValue(True,"boolean",new_value,None)
                        return True,new_node
                    
                    else:
                        
                        node['sem_return'] = SemValue(False,"boolean",None,None)
                        return True,node
                    
                else:
                    
                    if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                        new_value = int(value1.value) >= int(value2.value)
                        
                        new_node = {
                            "token" : value1_node['token'],
                            "type" : "VALUE_BOOLEAN",
                            "value" : new_value
                        }
                    
                        new_node['sem_return'] = SemValue(True,"boolean",new_value,None)
                        return True,new_node
                    
                    else:
                        
                        node['sem_return'] = SemValue(False,"boolean",None,None)
                        return True,node
                            
                
                
                            
            elif value1.datatype in ['string','char'] and value2.datatype in ['string','char']:
                    
                if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                    new_value = value1.value >= value2.value
                        
                    new_node = {
                        "token" : value1_node['token'],
                        "type" : "VALUE_BOOLEAN",
                        "value" : new_value
                    }
                    
                    new_node['sem_return'] = SemValue(True,"boolean",new_value,None)
                    return True,new_node
                    
                else:
                    
                    node['sem_return'] = SemValue(False,"boolean",None,None)
                    return True,node
                
            elif value1.datatype == "boolean" and value2.datatype == "boolean":
                    
                if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                    new_value = value1.value >= value2.value
                        
                    new_node = {
                        "token" : value1_node['token'],
                        "type" : "VALUE_BOOLEAN",
                        "value" : new_value
                    }
                    
                    new_node['sem_return'] = SemValue(True,"boolean",new_value,None)
                    return True,new_node
                    
                else:
                    
                    node['sem_return'] = SemValue(False,"boolean",None,None)
                    return True,node
                    
            else:
                eh.add_semantic_error(node['token'],f"Incompatible types in greater or equal than operation")
                return False,node
            
        case "<":
            
            if value1.datatype in ['integer','real'] and value2.datatype in ['integer','real']:
                         
                if value1.datatype == "real" or value2.datatype == "real":
                    
                    if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                        new_value = float(value1.value) < float(value2.value)
                        
                        new_node = {
                            "token" : value1_node['token'],
                            "type" : "VALUE_BOOLEAN",
                            "value" : new_value
                        }
                    
                        new_node['sem_return'] = SemValue(True,"boolean",new_value,None)
                        return True,new_node
                    
                    else:
                        
                        node['sem_return'] = SemValue(False,"boolean",None,None)
                        return True,node
                    
                else:
                    
                    if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                        new_value = int(value1.value) < int(value2.value)
                        
                        new_node = {
                            "token" : value1_node['token'],
                            "type" : "VALUE_BOOLEAN",
                            "value" : new_value
                        }
                    
                        new_node['sem_return'] = SemValue(True,"boolean",new_value,None)
                        return True,new_node
                    
                    else:
                        
                        node['sem_return'] = SemValue(False,"boolean",None,None)
                        return True,node
                            
                
                
                            
            elif value1.datatype in ['string','char'] and value2.datatype in ['string','char']:
                    
                if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                    new_value = value1.value < value2.value
                        
                    new_node = {
                        "token" : value1_node['token'],
                        "type" : "VALUE_BOOLEAN",
                        "value" : new_value
                    }
                    
                    new_node['sem_return'] = SemValue(True,"boolean",new_value,None)
                    return True,new_node
                    
                else:
                    
                    node['sem_return'] = SemValue(False,"boolean",None,None)
                    return True,node
                
            elif value1.datatype == "boolean" and value2.datatype == "boolean":
                    
                if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                    new_value = value1.value < value2.value
                        
                    new_node = {
                        "token" : value1_node['token'],
                        "type" : "VALUE_BOOLEAN",
                        "value" : new_value
                    }
                    
                    new_node['sem_return'] = SemValue(True,"boolean",new_value,None)
                    return True,new_node
                    
                else:
                    
                    node['sem_return'] = SemValue(False,"boolean",None,None)
                    return True,node
                    
            else:
                eh.add_semantic_error(node['token'],f"Incompatible types in smaller than operation")
                return False,node
            
        case "<=":
            
            if value1.datatype in ['integer','real'] and value2.datatype in ['integer','real']:
                         
                if value1.datatype == "real" or value2.datatype == "real":
                    
                    if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                        new_value = float(value1.value) <= float(value2.value)
                        
                        new_node = {
                            "token" : value1_node['token'],
                            "type" : "VALUE_BOOLEAN",
                            "value" : new_value
                        }
                    
                        new_node['sem_return'] = SemValue(True,"boolean",new_value,None)
                        return True,new_node
                    
                    else:
                        
                        node['sem_return'] = SemValue(False,"boolean",None,None)
                        return True,node
                    
                else:
                    
                    if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                        new_value = int(value1.value) <= int(value2.value)
                        
                        new_node = {
                            "token" : value1_node['token'],
                            "type" : "VALUE_BOOLEAN",
                            "value" : new_value
                        }
                    
                        new_node['sem_return'] = SemValue(True,"boolean",new_value,None)
                        return True,new_node
                    
                    else:
                        
                        node['sem_return'] = SemValue(False,"boolean",None,None)
                        return True,node
                            
                
                
                            
            elif value1.datatype in ['string','char'] and value2.datatype in ['string','char']:
                    
                if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                    new_value = value1.value <= value2.value
                        
                    new_node = {
                        "token" : value1_node['token'],
                        "type" : "VALUE_BOOLEAN",
                        "value" : new_value
                    }
                    
                    new_node['sem_return'] = SemValue(True,"boolean",new_value,None)
                    return True,new_node
                    
                else:
                    
                    node['sem_return'] = SemValue(False,"boolean",None,None)
                    return True,node
                
            elif value1.datatype == "boolean" and value2.datatype == "boolean":
                    
                if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                    new_value = value1.value <= value2.value
                        
                    new_node = {
                        "token" : value1_node['token'],
                        "type" : "VALUE_BOOLEAN",
                        "value" : new_value
                    }
                    
                    new_node['sem_return'] = SemValue(True,"boolean",new_value,None)
                    return True,new_node
                    
                else:
                    
                    node['sem_return'] = SemValue(False,"boolean",None,None)
                    return True,node
                    
            else:
                eh.add_semantic_error(node['token'],f"Incompatible types in smaller or equals than operation")
                return False,node
            
        case "and":
            
            if value1.datatype == 'integer' and value2.datatype == 'integer':
                         
                if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                    
                    new_value = int(value1.value) and int(value2.value)
                    
                    new_node = {
                        "token" : value1_node['token'],
                        "type" : "VALUE_NUMBER",
                        "value" : new_value
                    }
                
                    new_node['sem_return'] = SemValue(True,"integer",new_value,None)
                    return True,new_node
                    
                else:
                    
                    node['sem_return'] = SemValue(False,"integer",None,None)
                    return True,node
                            
            elif value1.datatype == "boolean" and value2.datatype == "boolean":
                    
                if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                    new_value = value1.value and value2.value
                        
                    new_node = {
                        "token" : value1_node['token'],
                        "type" : "VALUE_BOOLEAN",
                        "value" : new_value
                    }
                    
                    new_node['sem_return'] = SemValue(True,"boolean",new_value,None)
                    return True,new_node
                    
                else:
                    
                    node['sem_return'] = SemValue(False,"boolean",None,None)
                    return True,node
                    
            else:
                eh.add_semantic_error(node['token'],f"Incompatible types in and operation")
                return False,node
            
        case "or":
            
            if value1.datatype == 'integer' and value2.datatype == 'integer':
                         
                if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                    
                    new_value = int(value1.value) or int(value2.value)
                    
                    new_node = {
                        "token" : value1_node['token'],
                        "type" : "VALUE_NUMBER",
                        "value" : new_value
                    }
                
                    new_node['sem_return'] = SemValue(True,"integer",new_value,None)
                    return True,new_node
                    
                else:
                    
                    node['sem_return'] = SemValue(False,"integer",None,None)
                    return True,node
                            
            elif value1.datatype == "boolean" and value2.datatype == "boolean":
                    
                if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                    new_value = value1.value or value2.value
                        
                    new_node = {
                        "token" : value1_node['token'],
                        "type" : "VALUE_BOOLEAN",
                        "value" : new_value
                    }
                    
                    new_node['sem_return'] = SemValue(True,"boolean",new_value,None)
                    return True,new_node
                    
                else:
                    
                    node['sem_return'] = SemValue(False,"boolean",None,None)
                    return True,node
                    
            else:
                eh.add_semantic_error(node['token'],f"Incompatible types in or operation")
                return False,node
            
        case "xor":
            
            if value1.datatype == 'integer' and value2.datatype == 'integer':
                         
                if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                    
                    new_value = int(value1.value) ^ int(value2.value)
                    
                    new_node = {
                        "token" : value1_node['token'],
                        "type" : "VALUE_NUMBER",
                        "value" : new_value
                    }
                
                    new_node['sem_return'] = SemValue(True,"integer",new_value,None)
                    return True,new_node
                    
                else:
                    
                    node['sem_return'] = SemValue(False,"integer",None,None)
                    return True,node
                            
            elif value1.datatype == "boolean" and value2.datatype == "boolean":
                    
                if value1.isStatic is True and value2.isStatic is True and sem['allow_opt'] is True : #OPT
                        
                    new_value = value1.value ^ value2.value
                        
                    new_node = {
                        "token" : value1_node['token'],
                        "type" : "VALUE_BOOLEAN",
                        "value" : new_value
                    }
                    
                    new_node['sem_return'] = SemValue(True,"boolean",new_value,None)
                    return True,new_node
                    
                else:
                    
                    node['sem_return'] = SemValue(False,"boolean",None,None)
                    return True,node
                    
            else:
                eh.add_semantic_error(node['token'],f"Incompatible types in xor operation")
                return False,node
            
        case _:
            eh.add_semantic_error(node['token'],f"Unknow {operator} binary operator")
            return False,node
        


def analyse_unary_operation(node):
    global sem
 
    node['sem_return'] = None
    
    operator = node['operator']
            
    if operator.lower() == "not":
        
        value_is_valid, value_node = analyse_expression(node['value'])
        value = value_node['sem_return']
        node['sem_return'] = value
        node['value'] = value_node
        
        if value_is_valid is True and isinstance(value,SemValue):
        
            value.varName = None
            
            if value.isStatic is False:
                                            
                if value.datatype in ["boolean","integer"]:
                    return True,node
                        
                else:
                    eh.add_semantic_error(node['token'],f"Incompatible type in not operation")
                    return False,node                              
                    
                
            elif value_node['type'] in ["VALUE_BOOLEAN","VALUE_NUMBER"]: #OPT
                
                value_node['value'] = not value.value
                value.value = not value.value
                value_node['sem_return'] = value
                
                return True,value_node    
                
            else:
                eh.add_semantic_error(node['token'],f"Incompatible type in not operation")
                return False,node
            
        else:
            return False,node
                
    else:
        eh.add_semantic_error(node['token'],f"Unknown {operator} unary operator")
        return False,node
        
        
        

def analyse_expression(node):
    global sem
              
    node['sem_return'] = None
                                
    match node['type']:
        
        case "OPERATION_BINARY":
            return analyse_binary_operation(node)
        
        case "OPERATION_UNARY":
            return analyse_unary_operation(node)
        
        case "INSTRUCTION_FUNCPROC":
            return analyse_instruction_funcproc(node)
        
        case _ :
            return analyse_value(node,True)
            

def analyse_value(node,isReadingValue):
    global sem
             
    node['sem_return'] = None
                
    match node['type']:
        
        case "VALUE_NUMBER":
            node['sem_return'] = SemValue(True,"integer",int(node['value']),None)
            return True,node
            
        case "VALUE_NUMBER_REAL":
            node['sem_return'] = SemValue(True,"real",float(node['value']),None)
            return True,node
        
        case "VALUE_STRING":
            node['sem_return'] = SemValue(True,"string",node['value'],None)
            return True,node
        
        case "VALUE_CHAR":
            node['sem_return'] = SemValue(True,"char",node['value'],None)
            return True,node
        
        case "VALUE_BOOLEAN":
            node['sem_return'] = SemValue(True,"boolean",bool(node['value']),None)
            return True,node
        
        case "VALUE_VAR":
            
            var_name = node['name_var'].lower()
            
            if does_name_exist(var_name) is True:
                
                var = get_ID(var_name,SemVar)
                
                if isinstance(var,SemVar) is True:
                    
                    if isReadingValue is True:
                        add_read_ID(var_name,var.isGlobal)
                    node['sem_return'] = SemValue(False,var.datatype,None,var_name)
                    return True,node

                else:
                    eh.add_semantic_error(node['token'],f"ID is not a variable as expected")
                    return False, node
                
            else:
                eh.add_semantic_error(node['token'],f"Variable name does not exist")
                return False,node
            
        case "ARRAY_INDEX":
            
            array_name = node['array_name'].lower()
            
            if does_name_exist(array_name) is True:
                
                array = get_ID(array_name,SemVar)
                
                is_value_valid, value_node = analyse_expression(node['index'])
                value = value_node['sem_return']
                
                if is_value_valid is True and isinstance(value,SemValue) is True:
                        
                    if array.is_array is True:
                                                
                        if value.datatype == "integer":
                            
                            if value.varName is None and (value.value < array.min_range or value.value > array.max_range):
                                eh.add_semantic_warning(node['token'],f"Index out of bound of array")
                                  
                            if isReadingValue is True:
                                add_read_ID(array_name,array.isGlobal)
                            
                            node['sem_return'] = SemValue(False,array.datatype,None,array_name)
                            node['index'] = value_node
                                       
                            return True, node

                        else:
                            eh.add_semantic_error(node['token'],f"Index of an array must be an integer")
                            return False,node

                    elif array.datatype == "string":
                                       
                        if isReadingValue is True:                                                         
                            add_read_ID(array_name,array.isGlobal)
                            
                        node['sem_return'] = SemValue(False,"char",None,None)
                        node['index'] = value_node
                        
                        return True, node
                        
                    else:
                        eh.add_semantic_error(node['token'],f"Variable is not an array as expected")
                        return False,node
                    
                else:
                    return False,node
                
                
            else:
                eh.add_semantic_error(node['token'],f"Variable name does not exist")
                return False,node
            
        case _:
            eh.add_semantic_error(node['token'],f"Unknown value type")
            return False,node