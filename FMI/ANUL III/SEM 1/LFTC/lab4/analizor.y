%{
    #include <stdio.h>
    #include <stdlib.h> 

    void yyerror(const char *s);
    extern int yylineno;
    extern FILE *yyin; 
    int yylex();
%}

%token INT_CONST FLOAT_CONST ID
%token INT_KEYWORD FLOAT_KEYWORD CIN_KEYWORD COUT_KEYWORD WHILE_KEYWORD IF_KEYWORD 
%token PLUS_PLUS MINUS_MINUS '+' '-' '*' '/' '%' '='
%token LT GT LE GE EQ NE
%token SHIFT_LEFT SHIFT_RIGHT
%token PE ME TE DE MOD

%union {
    int int_val;
    float float_val;
    char *id;
}

%left '+' '-'
%left '*' '/' '%'

%%
program:
    functie 
    | functie program
    ;

functie:
    antet_functie '{' instructiuni '}'
    ;

antet_functie:
    tip ID '(' parametrii ')'
    ;

tip:
    INT_KEYWORD
    | FLOAT_KEYWORD
    ;

parametrii:

    | tip ID
    | tip ID ',' parametrii
    ;

instructiuni:
    instructiune
    | instructiune instructiuni
    ;

instructiune:
    declarare
    | atribuire
    | citire
    | afisare
    | ciclare
    | conditional
    | op_unar
    ;

declarare:
    tip ID ';'
    ;

atribuire:
    ID '=' expresie ';'
    | ID atribuire_compusa expresie ';'
    ;

citire:
    CIN_KEYWORD SHIFT_RIGHT ID ';'
    ;

afisare:
    COUT_KEYWORD SHIFT_LEFT conditie ';'
    ;

ciclare:
    WHILE_KEYWORD '(' conditie ')' '{' instructiuni '}'
    ;

conditional:
    IF_KEYWORD '(' conditie ')' '{' instructiuni '}'
    ;

expresie:
    INT_CONST
    | FLOAT_CONST
    | ID
    | expresie '+' expresie
    | expresie '-' expresie
    | expresie '*' expresie
    | expresie '/' expresie
    | expresie '%' expresie
    ;

conditie:
    expresie
    | expresie op_relational expresie
    ;

op_relational:
    LT
    | GT
    | LE
    | GE
    | EQ
    | NE
    ;

atribuire_compusa:
    PE
    | ME
    | TE
    | DE
    | MOD

op_unar:
    PLUS_PLUS ID
    | MINUS_MINUS ID
    | ID PLUS_PLUS
    | ID MINUS_MINUS
    ;
%%

void yyerror(const char *s) {
    fprintf(stderr, "Eroare sintactică la linia %d: %s\n", yylineno, s);
    exit(0);
}

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Utilizare: %s <nume_fisier>\n", argv[0]);
        return 1;
    }

    FILE *fisier = fopen(argv[1], "r");
    if (!fisier) {
        perror("Eroare la deschiderea fișierului");
        return 1;
    }

    yyin = fisier;

    yyparse();
    printf("Fișier analizat cu succes!\n");

    fclose(fisier);
    return 0;
}
