

class SemProgram:
    
    def __init__(self,token,name):
        self.token = token
        self.name = name
        
    def __repr__(self):
        return f"Program(name='{self.name}')"
    
    def to_dict(self):
        return {
            "name": self.name
        }
    
class SemDatatype:
    
    def __init__(self,token,datatype,is_array,min_range=0,max_range=0):
        self.token = token
        self.datatype = datatype.lower()
        self.is_array = is_array
        self.min_range = min_range
        self.max_range = max_range
        
    def __repr__(self):
        return f"Datatype(datatype='{self.datatype}',isArray={self.is_array},minRange={self.min_range},maxRange={self.max_range})"
    
    def to_dict(self):
        return {
            "datatype": self.datatype,
            "is_array": self.is_array,
            "min_range": self.min_range,
            "max_range": self.max_range
        }
    
class SemVar:
    
    def __init__(self,token,name,isGlobal,isArgument,vm_id,datatype,readOnly=False):
        self.token = token
        self.var_name = name.lower()
        self.read_ctr = 0
        self.write_ctr = 0
        self.isGlobal = isGlobal
        self.isArgument = isArgument
        self.vm_id = vm_id
        self.datatype = datatype.datatype
        self.is_array = datatype.is_array
        self.min_range = datatype.min_range
        self.max_range = datatype.max_range
        self.readOnly = readOnly
        
    def __repr__(self):
        return f"Var(name='{self.var_name},isGlobal={self.isGlobal},readOnly={self.readOnly},read_ctr={self.read_ctr},write_ctr={self.write_ctr},vm_id={self.vm_id},'datatype='{self.datatype}',isArray={self.is_array},minRange={self.min_range},maxRange={self.max_range})"
    
    def to_dict(self):
        return {
            "var_name": self.var_name,
            "isGlobal": self.isGlobal,
            "vm_id": self.vm_id,
            "datatype": self.datatype.to_dict() if hasattr(self.datatype, 'to_dict') else str(self.datatype),
            "readOnly": self.readOnly,
            "write_ctr": self.write_ctr,
            "read_ctr": self.read_ctr
        }
    
class SemFuncProc:
    
    def __init__(self,token,name,vm_id,isFunction,isDefault,return_id=None,args=[]):
        self.token = token
        self.funcproc_name = name.lower()
        self.vm_id = vm_id
        self.read_ctr = 0
        self.write_ctr = 0
        self.isFunction = isFunction
        self.isDefault = isDefault
        self.args = args
        self.return_id = return_id
        self.table = {}
        
    def __repr__(self):
        return f"FuncProc(name='{self.funcproc_name},isFunction={self.isFunction},isDefault={self.isDefault},read_ctr={self.read_ctr},write_ctr={self.write_ctr},return_value={self.return_id},args={self.args},table={self.table})"
    
    def to_dict(self):
        return {
            "funcproc_name": self.funcproc_name,
            "isFunction": self.isFunction,
            "isDefault": self.isDefault,
            "read_ctr": self.read_ctr,
            "write_ctr": self.write_ctr,
            "return_id": self.return_id,
            "args": [arg.to_dict() if hasattr(arg, 'to_dict') else str(arg) for arg in self.args],
            "table": {k: v.to_dict() if hasattr(v, 'to_dict') else str(v) for k, v in self.table.items()}
        }
    
class SemValue:
    
    def __init__(self,isStatic,datatype,value,varName):
        self.isStatic = isStatic
        self.datatype = datatype.lower()
        self.value = value
        self.varName = varName
        
    def __repr__(self):
        return f"Value(isStatic='{self.isStatic},DataType={self.datatype},value={self.value},isVar={self.varName})"
    
    def to_dict(self):
        return {
            "isStatic": self.isStatic,
            "datatype": self.datatype,
            "value": self.value,
            "varName": self.varName
        }