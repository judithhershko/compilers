grammar Expression;

start_rule: (dec)*(expr)*;

typed_var: (INT| DOUBLE | FLOAT | CHAR);

dec : typed_var ID EQ expr;

binop:MIN | PLUS | GT | LT | AND | OR | ISEQ | GOE | LOE ;

binop_md: MULT| DIV ;

expr: term| expr binop term ;

term: fac |term binop_md fac;

fac:LBRAK expr RBRAK|pri;

pri:ID| NUM;

INT     : 'int'     ;
DOUBLE  : 'double'  ;
FLOAT   : 'float'   ;
CHAR    : 'char'    ;

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

EOL: ';' -> skip;
NLINE:';' .*? '\n' -> skip;





