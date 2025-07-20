grammar SimpleLang;

prog: stat+ ;
stat: expr NEWLINE ;

expr: expr op=('*'|'/') expr           # MulDiv
    | expr op=('+'|'-') expr           # AddSub
    | expr ('=='|'!=') expr            # Equality
    | expr ('<'|'>'|'<='|'>=') expr    # Comparison
    | expr ('&&'|'||') expr            # LogicalOp
    | '!' expr                         # LogicalNot
    | expr '%' expr                    # Modulo
    | INT                              # Int
    | FLOAT                            # Float
    | STRING                           # String
    | BOOL                             # Bool
    | '(' expr ')'                     # Parens
    ;

INT: [0-9]+ ;
FLOAT: [0-9]+'.'[0-9]* ;
STRING: '"' .*? '"' ;
BOOL: 'true' | 'false' ;
NEWLINE: '\r'? '\n' ;
WS: [ \t]+ -> skip ;