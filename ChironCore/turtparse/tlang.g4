
grammar tlang;

start : (structDecl | functionDecl)* instruction_list EOF ;


functionDecl : TO NAME (VAR)* strict_ilist END;

structDecl : STRUCT NAME (VAR)* END ;


instruction_list : (instruction)*
		 ;

strict_ilist : (instruction)+
             ;

instruction : assignment
	    | conditional
	    | loop
	    | moveCommand
	    | penCommand
	    | gotoCommand
	    | pauseCommand
		| expression    
	    ;

conditional : ifConditional | ifElseConditional ;

ifConditional : 'if' condition '[' strict_ilist ']' ;

ifElseConditional : 'if' condition '[' strict_ilist ']' 'else' '[' strict_ilist ']' ;

loop : 'repeat' value '[' strict_ilist ']' ;

gotoCommand : 'goto' '(' expression ',' expression ')';

assignment : (VAR | fieldAccess) '=' expression
	   ;

moveCommand : moveOp expression ;
moveOp : 'forward' | 'backward' | 'left' | 'right' ;

penCommand : 'penup' | 'pendown' ;

pauseCommand : 'pause' ;

expression : 
             unaryArithOp expression               #unaryExpr
           | expression multiplicative expression  #mulExpr
		   | expression additive expression        #addExpr
		   | value                                 #valueExpr
		   | '(' expression ')'                    #parenExpr
 	   ;


functionCall : NAME '(' (expression (',' expression)*)? ')' ;

structInit : NAME '(' ')' ;         // e.g., Point()
fieldAccess : VAR '.' NAME ;        // e.g., :p.x


multiplicative : MUL | DIV;
additive : PLUS | MINUS;

unaryArithOp : MINUS ;

PLUS     : '+' ;
MINUS    : '-' ;
MUL  	 : '*' ;
DIV      : '/' ;


// TODO :
// procedure_declaration : 'to' NAME (VAR)+ strict_ilist 'end' ;

condition : NOT condition
          |expression binCondOp expression
	  | condition logicOp condition
	  | PENCOND
	  | '(' condition ')'
	  ;


binCondOp :  EQ | NEQ | LT | GT | LTE | GTE
	 ;

logicOp : AND | OR ;

TO       : 'to' ;
END      : 'end' ;
STRUCT   : 'struct' ;

PENCOND : 'pendown?';
LT : '<' ;
GT : '>' ;
EQ : '==';
NEQ: '!=';
LTE: '<=';
GTE: '>=';
AND: '&&';
OR : '||';
NOT: '!' ;

value : NUM
      | VAR
	  | structInit 
	  | functionCall    
      | fieldAccess     
      ;

NAME : [a-zA-Z]+     ;

NUM  : [0-9]+        ;

VAR  : ':'[a-zA-Z_] [a-zA-Z0-9]* ;

Whitespace: [ \t\n\r]+ -> skip;
