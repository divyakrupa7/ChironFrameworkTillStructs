<<<<<<< HEAD

from ChironAST import ChironAST
from ChironHooks import Chironhooks
import turtle

Release="Chiron v5.3"

def addContext(s):
    return str(s).strip().replace(":", "self.prg.")

class Interpreter:
    # Turtle program should not contain variable with names "ir", "pc", "t_screen"
    ir = None
    pc = None
    t_screen = None
    trtl = None

    def __init__(self, irHandler, params):
        self.ir = irHandler.ir
        self.cfg = irHandler.cfg
        self.pc = 0
        self.t_screen = turtle.getscreen()
        self.trtl = turtle.Turtle()
        self.trtl.shape("turtle")
        self.trtl.color("blue", "yellow")
        self.trtl.fillcolor("green")
        self.trtl.begin_fill()
        self.trtl.pensize(4)
        self.trtl.speed(1) # TODO: Make it user friendly

        if params is not None:
            self.args = params
        else:
            self.args = None

        turtle.title(Release)
        turtle.bgcolor("white")
        turtle.hideturtle()

    def handleAssignment(self, stmt,tgt):
        raise NotImplementedError('Assignments are not handled!')

    def handleCondition(self, stmt, tgt):
        raise NotImplementedError('Conditions are not handled!')

    def handleMove(self, stmt, tgt):
        raise NotImplementedError('Moves are not handled!')

    def handlePen(self, stmt, tgt):
        raise NotImplementedError('Pens are not handled!')

    def handleGotoCommand(self, stmt, tgt):
        raise NotImplementedError('Gotos are not handled!')

    def handleNoOpCommand(self, stmt, tgt):
        raise NotImplementedError('No-Ops are not handled!')

    def handlePauseCommand(self, stmt, tgt):
        raise NotImplementedError('No-Ops are not handled!')

    def sanityCheck(self, irInstr):
        stmt, tgt = irInstr
        # if not a condition command, rel. jump can't be anything but 1
        if not isinstance(stmt, ChironAST.ConditionCommand):
            if tgt != 1:
                raise ValueError("Improper relative jump for non-conditional instruction", str(stmt), tgt)
    
    def interpret(self):
        pass

    def initProgramContext(self, params):
        pass

class ProgramContext:
    pass

# TODO: move to a different file
class ConcreteInterpreter(Interpreter):
    # Ref: https://realpython.com/beginners-guide-python-turtle
    cond_eval = None # used as a temporary variable within the embedded program interpreter
    prg = None

    def __init__(self, irHandler, params):
        super().__init__(irHandler, params)
        self.prg = ProgramContext()
        # Hooks Object:
        if self.args is not None and self.args.hooks:
            self.chironhook = Chironhooks.ConcreteChironHooks()
        self.pc = 0

    def interpret(self):
        print("Program counter : ", self.pc)
        stmt, tgt = self.ir[self.pc]
        print(stmt, stmt.__class__.__name__, tgt)

        self.sanityCheck(self.ir[self.pc])

        if isinstance(stmt, ChironAST.AssignmentCommand):
            ntgt = self.handleAssignment(stmt, tgt)
        elif isinstance(stmt, ChironAST.ConditionCommand):
            ntgt = self.handleCondition(stmt, tgt)
        elif isinstance(stmt, ChironAST.MoveCommand):
            ntgt = self.handleMove(stmt, tgt)
        elif isinstance(stmt, ChironAST.PenCommand):
            ntgt = self.handlePen(stmt, tgt)
        elif isinstance(stmt, ChironAST.GotoCommand):
            ntgt = self.handleGotoCommand(stmt, tgt)
        elif isinstance(stmt, ChironAST.NoOpCommand):
            ntgt = self.handleNoOpCommand(stmt, tgt)
        else:
            raise NotImplementedError("Unknown instruction: %s, %s."%(type(stmt), stmt))

        # TODO: handle statement
        self.pc += ntgt

        if self.pc >= len(self.ir):
            # This is the ending of the interpreter.
            self.trtl.write("End, Press ESC", font=("Arial", 15, "bold"))
            if self.args is not None and self.args.hooks:
                self.chironhook.ChironEndHook(self)
            return True
        else:
            return False
    
    def initProgramContext(self, params):
        # This is the starting of the interpreter at setup stage.
        if self.args is not None and self.args.hooks:
            self.chironhook.ChironStartHook(self)
        self.trtl.write("Start", font=("Arial", 15, "bold"))
        for key,val in params.items():
            var = key.replace(":","")
            exec("setattr(self.prg,\"%s\",%s)" % (var, val))
    
    def handleAssignment(self, stmt, tgt):
        print("  Assignment Statement")
        lhs = str(stmt.lvar).replace(":","")
        rhs = addContext(stmt.rexpr)
        exec("setattr(self.prg,\"%s\",%s)" % (lhs,rhs))
        return 1

    def handleCondition(self, stmt, tgt):
        print("  Branch Instruction")
        condstr = addContext(stmt)
        exec("self.cond_eval = %s" % (condstr))
        return 1 if self.cond_eval else tgt

    def handleMove(self, stmt, tgt):
        print("  MoveCommand")
        exec("self.trtl.%s(%s)" % (stmt.direction,addContext(stmt.expr)))
        return 1

    def handleNoOpCommand(self, stmt, tgt):
        print("  No-Op Command")
        return 1

    def handlePen(self, stmt, tgt):
        print("  PenCommand")
        exec("self.trtl.%s()"%(stmt.status))
        return 1

    def handleGotoCommand(self, stmt, tgt):
        print(" GotoCommand")
        xcor = addContext(stmt.xcor)
        ycor = addContext(stmt.ycor)
        exec("self.trtl.goto(%s, %s)" % (xcor, ycor))
        return 1
=======

from ChironAST import ChironAST
from ChironHooks import Chironhooks
import turtle

Release="Chiron v5.3"

def addContext(s):
    if isinstance(s, ChironAST.StructFieldAccess):
        return addContext(s.struct_var) + f".get('{s.field_name}')"
    return str(s).strip().replace(":", "self.prg.")


class Interpreter:
    # Turtle program should not contain variable with names "ir", "pc", "t_screen"
    ir = None
    pc = None
    t_screen = None
    trtl = None

    def __init__(self, irHandler, params):
        self.ir = irHandler.ir
        self.cfg = irHandler.cfg
        self.pc = 0
        self.t_screen = turtle.getscreen()
        self.trtl = turtle.Turtle()
        self.trtl.shape("turtle")
        self.trtl.color("blue", "yellow")
        self.trtl.fillcolor("green")
        self.trtl.begin_fill()
        self.trtl.pensize(4)
        self.trtl.speed(1) # TODO: Make it user friendly

        if params is not None:
            self.args = params
        else:
            self.args = None

        turtle.title(Release)
        turtle.bgcolor("white")
        turtle.hideturtle()

    def handleAssignment(self, stmt,tgt):
        raise NotImplementedError('Assignments are not handled!')

    def handleCondition(self, stmt, tgt):
        raise NotImplementedError('Conditions are not handled!')

    def handleMove(self, stmt, tgt):
        raise NotImplementedError('Moves are not handled!')

    def handlePen(self, stmt, tgt):
        raise NotImplementedError('Pens are not handled!')

    def handleGotoCommand(self, stmt, tgt):
        raise NotImplementedError('Gotos are not handled!')

    def handleNoOpCommand(self, stmt, tgt):
        raise NotImplementedError('No-Ops are not handled!')

    def handlePauseCommand(self, stmt, tgt):
        raise NotImplementedError('No-Ops are not handled!')

    def sanityCheck(self, irInstr):
        stmt, tgt = irInstr
        # if not a condition command, rel. jump can't be anything but 1
        if not isinstance(stmt, ChironAST.ConditionCommand):
            if tgt != 1:
                raise ValueError("Improper relative jump for non-conditional instruction", str(stmt), tgt)
    
    def interpret(self):
        pass

    def initProgramContext(self, params):
        pass

class ProgramContext:
    pass

# TODO: move to a different file
class ConcreteInterpreter(Interpreter):
    # Ref: https://realpython.com/beginners-guide-python-turtle
    cond_eval = None # used as a temporary variable within the embedded program interpreter
    prg = None

    def __init__(self, irHandler, params):
        self.functions = {}
        self.struct_defs = {}
        super().__init__(irHandler, params)
        self.prg = ProgramContext()
        # Hooks Object:
        if self.args is not None and self.args.hooks:
            self.chironhook = Chironhooks.ConcreteChironHooks()
        self.pc = 0
        
    def setFunctions(self, func_map): 
        self.functions = func_map
    
    def setStructs(self, struct_map):
        self.struct_defs = struct_map

        
    # def handleCall(self, stmt): 
    #     func_name = stmt.name 
    #     args = stmt.args
    #     if func_name not in self.functions:
    #         raise Exception(f"Function '{func_name}' is not defined.")
    #     param_list, body_ir = self.functions[func_name]
    #     if len(args) != len(param_list):
    #         raise Exception(f"Function '{func_name}' expects {len(param_list)} args, got {len(args)}")
    def handleCall(self, stmt):
        func_name = stmt.name 
        args = stmt.args
        if func_name not in self.functions:
           raise Exception(f"Function '{func_name}' is not defined.")
        param_list, body_ir = self.functions[func_name]
        if len(args) != len(param_list):
           raise Exception(f"Function '{func_name}' expects {len(param_list)} args, got {len(args)}")
     # Save current variable context (for nested calls)
        prev_context = self.prg

    # Create new context for the function
        local_ctx = ProgramContext()
        for param, arg_expr in zip(param_list, args):
            value = eval(addContext(arg_expr))
            setattr(local_ctx, param.replace(":", ""), value)
        self.prg = local_ctx
        pc = 0
        return_value = None  # Track return value
        while pc < len(body_ir):
            inst, jump = body_ir[pc]
            self.sanityCheck((inst, jump))

            if isinstance(inst, ChironAST.AssignmentCommand):
               self.handleAssignment(inst, jump)
            # capture latest assignment if variable is :result
               if str(inst.lvar) == ":result":
                    return_value = eval(addContext(inst.rexpr))
            elif isinstance(inst, ChironAST.CallCommand):
                self.handleCall(inst)
            elif isinstance(inst, ChironAST.GotoCommand):
                self.handleGotoCommand(inst, jump)
            elif isinstance(inst, ChironAST.MoveCommand):
                self.handleMove(inst, jump)
            elif isinstance(inst, ChironAST.PenCommand):
                self.handlePen(inst, jump)
            # elif isinstance(inst, ChironAST.ConditionCommand):
            #     cond_eval_str = addContext(inst)
            #     exec("self.cond_eval = %s" % (cond_eval_str))
            #     if not self.cond_eval:
            #         pc += jump
            #         continue
            elif isinstance(inst, ChironAST.ConditionCommand):
                pc += self.handleCondition(inst, jump)
                continue
            elif isinstance(inst, ChironAST.NoOpCommand):
                self.handleNoOpCommand(inst, jump)
            elif isinstance(inst, ChironAST.PauseCommand):
                self.handlePauseCommand(inst, jump)
            elif isinstance(inst, ChironAST.StructDeclaration):
                self.struct_defs[inst.name] = inst.fields
               # print(f"Struct '{inst.name}' declared with fields: {inst.fields}")
            else:
                raise Exception(f"Unsupported instruction in function body: {type(inst)}")
               
               
            pc += jump
        if return_value is None:    
            return_value = getattr(self.prg, "result", None)

        self.prg = prev_context
        return return_value

            
    def evalStructInit(self, expr):
        struct_name = expr.name
       # print(f"StructInit called for: {struct_name}")
        if struct_name not in self.struct_defs:
           raise Exception(f"Struct '{struct_name}' is not defined.")
        obj = {}
        for field in self.struct_defs[struct_name]:
            obj[field.replace(":", "")] = 0  # default 0
        return obj


    def interpret(self):
        print("Program counter : ", self.pc)
        stmt, tgt = self.ir[self.pc]
        print(stmt, stmt.__class__.__name__, tgt)

        self.sanityCheck(self.ir[self.pc])

        if isinstance(stmt, ChironAST.AssignmentCommand):
            ntgt = self.handleAssignment(stmt, tgt)
        elif isinstance(stmt, ChironAST.ConditionCommand):
            ntgt = self.handleCondition(stmt, tgt)
        elif isinstance(stmt, ChironAST.MoveCommand):
            ntgt = self.handleMove(stmt, tgt)
        elif isinstance(stmt, ChironAST.PenCommand):
            ntgt = self.handlePen(stmt, tgt)
        elif isinstance(stmt, ChironAST.GotoCommand):
            ntgt = self.handleGotoCommand(stmt, tgt)
        elif isinstance(stmt, ChironAST.NoOpCommand):
            ntgt = self.handleNoOpCommand(stmt, tgt)
        elif isinstance(stmt, ChironAST.CallCommand): 
            self.handleCall(stmt)
            ntgt = 1
        elif isinstance(stmt, ChironAST.StructDeclaration):
            self.struct_defs[stmt.name] = stmt.fields
            ntgt = 1
        else:
            raise NotImplementedError("Unknown instruction: %s, %s."%(type(stmt), stmt))

        # TODO: handle statement
        self.pc += ntgt

        if self.pc >= len(self.ir):
            # This is the ending of the interpreter.
            self.trtl.write("End, Press ESC", font=("Arial", 15, "bold"))
            if self.args is not None and self.args.hooks:
                self.chironhook.ChironEndHook(self)
            return True
        else:
            return False
    
    def initProgramContext(self, params):
        # This is the starting of the interpreter at setup stage.
        if self.args is not None and self.args.hooks:
            self.chironhook.ChironStartHook(self)
        self.trtl.write("Start", font=("Arial", 15, "bold"))
        for key,val in params.items():
            var = key.replace(":","")
            exec("setattr(self.prg,\"%s\",%s)" % (var, val))
    
    

    
    # def handleAssignment(self, stmt, tgt):
    #     print("  Assignment Statement")
    #     lhs = str(stmt.lvar).replace(":","")
    #     # rhs = addContext(stmt.rexpr)
    #     # exec("setattr(self.prg,\"%s\",%s)" % (lhs,rhs))
    #     rhs_expr = stmt.rexpr
    #     if isinstance(rhs_expr, ChironAST.StructInit):
    #         rhs = self.evalStructInit(rhs_expr)
    #     elif isinstance(rhs_expr, ChironAST.StructFieldAccess):
    #         rhs = eval(addContext(rhs_expr.struct_var) + f".get('{rhs_expr.field_name}')")
    #     else:
    #         rhs = eval(addContext(rhs_expr))
    #         setattr(self.prg, lhs, rhs)
    #         return 1
    
    def handleAssignment(self, stmt, tgt):
        lhs_expr = stmt.lvar         # could be Var or StructFieldAccess
        rhs_expr = stmt.rexpr        # could be Num, CallCommand, StructInit, etc.

       # Evaluate RHS
        if isinstance(rhs_expr, ChironAST.CallCommand):
           rhs = self.handleCall(rhs_expr)
        elif isinstance(rhs_expr, ChironAST.StructInit):
           rhs = self.evalStructInit(rhs_expr)
        else:
           rhs = eval(addContext(rhs_expr))

        # Assign to LHS
        if isinstance(lhs_expr, ChironAST.Var):
            lhs = str(lhs_expr).replace(":", "")
            setattr(self.prg, lhs, rhs)
            # exec(f"setattr(self.prg, '{lhs}', {rhs})")

        elif isinstance(lhs_expr, ChironAST.StructFieldAccess):
            struct_obj = eval(addContext(lhs_expr.struct_var))  # get struct object like self.prg.p
            field = lhs_expr.field_name
            # struct_obj[field] = rhs  # directly update field value
            struct_varname = lhs_expr.struct_var.varname.replace(":", "")
            struct_instance = getattr(self.prg, struct_varname, None)
            
            # Try to infer struct type from field match
            matched_type = None
            for typename, fields in self.struct_defs.items():
                expected_fields = [f.replace(":", "") for f in fields]
                if all(f in struct_instance for f in expected_fields):
                    matched_type = typename
                    break
                
            if matched_type:
                valid_fields = [f.replace(":", "") for f in self.struct_defs[matched_type]]
                if field not in valid_fields:
                    raise Exception(f" Error: Field '{field}' is not declared in struct '{matched_type}'")
            else:
                raise Exception(f" Error: Struct variable '{struct_varname}' does not match any declared struct")   
        

            struct_obj[field] = rhs

        else:
            raise Exception("Unsupported LHS in assignment")

        return 1



    def handleCondition(self, stmt, tgt):
        print("  Branch Instruction")
        condstr = addContext(stmt)
        exec("self.cond_eval = %s" % (condstr))
        return 1 if self.cond_eval else tgt

    def handleMove(self, stmt, tgt):
        print("  MoveCommand")
        exec("self.trtl.%s(%s)" % (stmt.direction,addContext(stmt.expr)))
        return 1

    def handleNoOpCommand(self, stmt, tgt):
        print("  No-Op Command")
        return 1

    def handlePen(self, stmt, tgt):
        print("  PenCommand")
        exec("self.trtl.%s()"%(stmt.status))
        return 1

    def handleGotoCommand(self, stmt, tgt):
        print(" GotoCommand")
        xcor = addContext(stmt.xcor)
        ycor = addContext(stmt.ycor)
        exec("self.trtl.goto(%s, %s)" % (xcor, ycor))
        return 1
>>>>>>> origin/main
