from SimpleLangParser import SimpleLangParser
from SimpleLangVisitor import SimpleLangVisitor
from custom_types import IntType, FloatType, StringType, BoolType

class TypeCheckVisitor(SimpleLangVisitor):

    def visitProg(self, ctx: SimpleLangParser.ProgContext):
        for stat in ctx.stat():
            self.visit(stat)
        return None
    
    def visitStat(self, ctx: SimpleLangParser.StatContext):
        return self.visit(ctx.expr())

    def visitMulDiv(self, ctx: SimpleLangParser.MulDivContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
            return FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()
        else:
            operator = ctx.getChild(1).getText()
            raise TypeError("Unsupported operand types for {}: {} and {}".format(operator, left_type, right_type))

    def visitAddSub(self, ctx: SimpleLangParser.AddSubContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        operator = ctx.getChild(1).getText()
        
        if operator == '+' and isinstance(left_type, StringType) and isinstance(right_type, StringType):
            return StringType()
        elif isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
            return FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()
        else:
            raise TypeError("Unsupported operand types for {} : {} and {}".format(operator, left_type, right_type))

    def visitEquality(self, ctx: SimpleLangParser.EqualityContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        if (isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType))) or \
           (type(left_type) == type(right_type)):
            return BoolType()
        else:
            operator = ctx.getChild(1).getText()
            raise TypeError("Cannot compare {} and {} for equality with {}".format(left_type, right_type, operator))
    
    def visitComparison(self, ctx: SimpleLangParser.ComparisonContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
            return BoolType()
        else:
            operator = ctx.getChild(1).getText()
            raise TypeError("Cannot compare {} and {} with relational operator {}".format(left_type, right_type, operator))
    
    def visitLogicalOp(self, ctx: SimpleLangParser.LogicalOpContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        if isinstance(left_type, BoolType) and isinstance(right_type, BoolType):
            return BoolType()
        else:
            operator = ctx.getChild(1).getText()
            raise TypeError("Logical operation {} requires boolean operands, got {} and {}".format(operator, left_type, right_type))
    
    def visitLogicalNot(self, ctx: SimpleLangParser.LogicalNotContext):
        expr_type = self.visit(ctx.expr())
        
        if isinstance(expr_type, BoolType):
            return BoolType()
        else:
            raise TypeError("Logical NOT requires boolean operand, got {}".format(expr_type))
    
    def visitModulo(self, ctx: SimpleLangParser.ModuloContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        if isinstance(left_type, IntType) and isinstance(right_type, IntType):
            return IntType()
        else:
            raise TypeError("Modulo operation requires integer operands, got {} and {}".format(left_type, right_type))
    
    def visitInt(self, ctx: SimpleLangParser.IntContext):
        return IntType()

    def visitFloat(self, ctx: SimpleLangParser.FloatContext):
        return FloatType()

    def visitString(self, ctx: SimpleLangParser.StringContext):
        return StringType()

    def visitBool(self, ctx: SimpleLangParser.BoolContext):
        return BoolType()

    def visitParens(self, ctx: SimpleLangParser.ParensContext):
        return self.visit(ctx.expr())