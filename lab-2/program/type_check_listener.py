from SimpleLangListener import SimpleLangListener
from SimpleLangParser import SimpleLangParser
from custom_types import IntType, FloatType, StringType, BoolType

class TypeCheckListener(SimpleLangListener):

    def __init__(self):
        self.errors = []
        self.types = {}

    def enterMulDiv(self, ctx: SimpleLangParser.MulDivContext):
        pass

    def exitMulDiv(self, ctx: SimpleLangParser.MulDivContext):
        left_type = self.types[ctx.expr(0)]
        right_type = self.types[ctx.expr(1)]
        if not self.is_valid_arithmetic_operation(left_type, right_type):
            self.errors.append(f"Unsupported operand types for * or /: {left_type} and {right_type}")
        self.types[ctx] = FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()

    def enterAddSub(self, ctx: SimpleLangParser.AddSubContext):
        pass

    def exitAddSub(self, ctx: SimpleLangParser.AddSubContext):
        left_type = self.types[ctx.expr(0)]
        right_type = self.types[ctx.expr(1)]
        
        operator = ctx.getChild(1).getText()
        
        if operator == '+' and isinstance(left_type, StringType) and isinstance(right_type, StringType):
            self.types[ctx] = StringType()
        elif self.is_valid_arithmetic_operation(left_type, right_type):
            self.types[ctx] = FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()
        else:
            self.errors.append(f"Unsupported operand types for {operator}: {left_type} and {right_type}")
            self.types[ctx] = IntType()  

    def enterEquality(self, ctx: SimpleLangParser.EqualityContext):
        pass

    def exitEquality(self, ctx: SimpleLangParser.EqualityContext):
        left_type = self.types[ctx.expr(0)]
        right_type = self.types[ctx.expr(1)]
        
        if self.is_valid_equality_operation(left_type, right_type):
            self.types[ctx] = BoolType()
        else:
            self.errors.append(f"Cannot compare {left_type} and {right_type} for equality")

    def enterComparison(self, ctx: SimpleLangParser.ComparisonContext):
        pass

    def exitComparison(self, ctx: SimpleLangParser.ComparisonContext):
        left_type = self.types[ctx.expr(0)]
        right_type = self.types[ctx.expr(1)]
        
        if self.is_valid_arithmetic_operation(left_type, right_type):
            self.types[ctx] = BoolType()
        else:
            self.errors.append(f"Cannot compare {left_type} and {right_type} with relational operators")

    def enterLogicalOp(self, ctx: SimpleLangParser.LogicalOpContext):
        pass

    def exitLogicalOp(self, ctx: SimpleLangParser.LogicalOpContext):
        left_type = self.types[ctx.expr(0)]
        right_type = self.types[ctx.expr(1)]
        
        if isinstance(left_type, BoolType) and isinstance(right_type, BoolType):
            self.types[ctx] = BoolType()
        else:
            self.errors.append(f"Logical operations require boolean operands, got {left_type} and {right_type}")

    def enterLogicalNot(self, ctx: SimpleLangParser.LogicalNotContext):
        pass

    def exitLogicalNot(self, ctx: SimpleLangParser.LogicalNotContext):
        expr_type = self.types[ctx.expr()]
        
        if isinstance(expr_type, BoolType):
            self.types[ctx] = BoolType()
        else:
            self.errors.append(f"Logical NOT requires boolean operand, got {expr_type}")

    def enterModulo(self, ctx: SimpleLangParser.ModuloContext):
        pass

    def exitModulo(self, ctx: SimpleLangParser.ModuloContext):
        left_type = self.types[ctx.expr(0)]
        right_type = self.types[ctx.expr(1)]
        
        if isinstance(left_type, IntType) and isinstance(right_type, IntType):
            self.types[ctx] = IntType()
        else:
            self.errors.append(f"Modulo operation requires integer operands, got {left_type} and {right_type}")

    def enterInt(self, ctx: SimpleLangParser.IntContext):
        self.types[ctx] = IntType()

    def enterFloat(self, ctx: SimpleLangParser.FloatContext):
        self.types[ctx] = FloatType()

    def enterString(self, ctx: SimpleLangParser.StringContext):
        self.types[ctx] = StringType()

    def enterBool(self, ctx: SimpleLangParser.BoolContext):
        self.types[ctx] = BoolType()

    def enterParens(self, ctx: SimpleLangParser.ParensContext):
        pass

    def exitParens(self, ctx: SimpleLangParser.ParensContext):
        self.types[ctx] = self.types[ctx.expr()]

    def is_valid_arithmetic_operation(self, left_type, right_type):
        return isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType))

    def is_valid_equality_operation(self, left_type, right_type):
        if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
            return True
        return type(left_type) == type(right_type)