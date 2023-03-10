grammar Expression;

start_rule: (dec)*(expr)*;

typed_var: INT| DOUBLE | FLOAT |CHAR;

const : CONST;
pointer_variable: (pointer)* var=ID;
pointer:MULT;

to_pointer: (pointer)* pri ;
to_reference: REF pri ;

dec:(const)? typed_var (pointer)* ID EQ (char_expr|expr) |(pointer)* ID EQ (char_expr|expr);
variable_dec:typed_var ID;

comparators: GT | LT | AND | OR |NEQ | ISEQ | GOE | LOE ;
binop: MIN | PLUS | ;

bin_lhs: NOT | MOD;
bin_rhs: PLUS PLUS | MIN MIN;

binop_md: MULT| DIV ;

expr: cterm | term | expr binop term | bin_lhs term | term bin_rhs;

cterm : cterm comparators fac | fac ;
term: fac | term binop_md fac;

fac:LBRAK expr RBRAK|pri;

pri: NUM | ID;

char_op: PLUS | MIN;
char_expr: char_pri| char_expr char_op char_expr;
char_pri:CHAR_ID ID CHAR_ID ;

INT     : 'int'     ;
DOUBLE  : 'double'  ;
FLOAT   : 'float'   ;
CHAR    : 'char'    ;
CONST   : 'const'   ;
REF     : '&'       ;

MULT : '*' ;
NUM  : [0-9]+ ;
ID   : [a-zA-Z_][a-zA-Z_0-9]*;
WS   : [ \t\n\r\f]+ -> skip ;
GT   : '>' ;
LT   : '<' ;
DIV  : '/' ;
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
NEQ  :  '!=';
MOD  :  '%' ;
CHAR_ID:'\'';

EOL: ';' -> skip;
NLINE:';' .*? '\n' -> skip;





