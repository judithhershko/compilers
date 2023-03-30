grammar Expression;

start_rule: (print|expr|dec|comments|line)*;

line:NLINE;
print   : PRINT LBRAK (char_pri | pri) RBRAK ;
comments: ML_COMMENT | SL_COMMENT;
typed_var: INT| DOUBLE | FLOAT |CHAR | BOOL;

const : CONST;
pointer:MULT;
ref_ref: (REF)? ID;
pointers: (pointer)+ ID (EQ ref_ref)? |  REF (EQ ref_ref)?;
suf_dec: pointers | ID EQ (char_expr|expr);

//dec:(const)? typed_var  suf_dec;
/variable_dec:typed_var ID;

dec:(const)? typed_var (pointer)* ID EQ (ref_ref|char_expr|expr) |(pointer)* ID EQ (ref_ref|char_expr|expr)
| (const)? typed_var (pointer)* ID;

binop:MIN | PLUS ;
binop_md: MULT| DIV | MOD;
equality: ISEQ | NEQ;
comparator: LOE | GOE | LT | GT;
or_and: OR | AND ;
prefix_op: NOT | PP | MM ;
suffix_op: PP | MM ;

expr: expr suffix_op | prefix_op expr | expr binop_md expr | expr binop expr | expr comparator expr |  expr equality expr | expr or_and expr  | fac;
fac : brackets|pri;
brackets: LBRAK expr RBRAK;
pri:  ID | num+ '.' num* | '.' num+ | num;
fnum: num | num+ '.' num* | '.' num+ ;
num: NUM;

char_op: PLUS | MIN;
char_expr: char_pri| char_expr char_op char_expr;

char_pri:CHAR_ID (ID | NUM)* CHAR_ID ;

INT     : 'int'     ;
DOUBLE  : 'double'  ;
FLOAT   : 'float'   ;
CHAR    : 'char'    ;
BOOL    : 'bool'    ;
CONST   : 'const'   ;
REF     : '&'       ;
PRINT   : 'printf'  ;

//SEARCH_TYPE: '"' ~'"'* '"';
PT   : '.' ;
MULT : '*' ;
NUM  : [0-9]+ ;
ID   : [a-zA-Z_][a-zA-Z_0-9]*;
WS   : [ \t\n\r\f]+ -> skip ;
NEQ  : '!=';
PP   : '++';
MM   : '--';
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
MOD  :  '%' ;
CHAR_ID:'\'';
ONE_LINE_COMMENT:'//';
STRT_COMMENT:'/**';
END_COMMENT:'**/' ;
ML_COMMENT:  '/*' .* '*/';
SL_COMMENT:  '//' ~('\r' | '\n')*;


EOL: ';' -> skip;
LINE: '\n';
//NLINE:';' .*? -> skip;
NLINE:';' .*? '\n' ;
//NLINE:';' .*? '\n' -> skip;