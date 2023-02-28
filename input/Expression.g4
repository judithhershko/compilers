grammar Expression;

start_rule: (dec)*(expr)*;

dec : ID EQ NUM;

binop:
     MULT |DIV| PLUS| MIN| GT| LT| AND| OR| ISEQ| GOE| LOE
     ;

expr:
     LBRAK expr RBRAK
    | NOT  expr
    | expr binop expr
    | expr MIN  MIN
    | PLUS PLUS expr
    | MIN MIN expr
    | ID
    | NUM
    ;

ID   : [a-zA-Z_][a-zA-Z_0-9]*;
NUM  : [0-9]+ ;
WS   : [ \t\n\r\f]+ -> skip ;
GT   : '>' ;
LT   : '<' ;
DIV  : '/' ;
MULT : '*' ;
MIN  : '-' ;
PLUS : '+' ;
EQ   : '=' ;
LBRAK: '(' ;
RBRAK: ')' ;
ISEQ : '==';
AND  : '&&';
OR   : '||';
NOT  :  '!';
GOE  :  '>=';
LOE  :  '<=';
MOD  :  '%' ;

NLINE:';' .*? '\n' -> skip;

