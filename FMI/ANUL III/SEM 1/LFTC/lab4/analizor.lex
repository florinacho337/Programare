%{
    #include "y.tab.h"
    extern int yylineno;
%}
      
CONST   0|-?[1-9][0-9]*(\.[0-9]+)?                                                                           

%%
"int"                             { return INT_KEYWORD; }
"float"                           { return FLOAT_KEYWORD; }
"cin"                             { return CIN_KEYWORD; }
"cout"                            { return COUT_KEYWORD; }
"while"                           { return WHILE_KEYWORD; }
"if"                              { return IF_KEYWORD; }
0|-?[1-9][0-9]*                   { yylval.int_val = atoi(yytext); return INT_CONST; }
-?(0\.[0-9]*|[1-9][0-9]*\.[0-9]*) { yylval.float_val = atof(yytext); return FLOAT_CONST; }
[a-zA-Z_][a-zA-Z0-9_]{0,254}      { yylval.id = strdup(yytext); return ID; }
"++"                              { return PLUS_PLUS; }
"--"                              { return MINUS_MINUS; }
"<"                               { return LT; }
">"                               { return GT; }
"<="                              { return LE; }
">="                              { return GE; }
"=="                              { return EQ; }
"!="                              { return NE; }
"<<"                              { return SHIFT_LEFT; }
">>"                              { return SHIFT_RIGHT; }
"+"                               { return '+'; }
"-"                               { return '-'; }
"*"                               { return '*'; }
"/"                               { return '/'; }
"%"                               { return '%'; }
"("                               { return '('; }
")"                               { return ')'; }
","                               { return ','; }
";"                               { return ';'; }
"{"                               { return '{'; }
"}"                               { return '}'; }
"="                               { return '='; }
[ \t\r]+                          { /* Ignore */ }
\n                                { yylineno++; }
.                                 {     
                                      fprintf(stderr, "Eroare lexicală la linia %d: caracter nevalid '%s'\n", yylineno, yytext);
                                      exit(0);
                                  }
%%