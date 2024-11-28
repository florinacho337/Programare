/* A Bison parser, made by GNU Bison 3.8.2.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2021 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
   especially those whose name start with YY_ or yy_.  They are
   private implementation details that can be changed or removed.  */

#ifndef YY_YY_Y_TAB_H_INCLUDED
# define YY_YY_Y_TAB_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int yydebug;
#endif

/* Token kinds.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    YYEMPTY = -2,
    YYEOF = 0,                     /* "end of file"  */
    YYerror = 256,                 /* error  */
    YYUNDEF = 257,                 /* "invalid token"  */
    INT_CONST = 258,               /* INT_CONST  */
    FLOAT_CONST = 259,             /* FLOAT_CONST  */
    ID = 260,                      /* ID  */
    INT_KEYWORD = 261,             /* INT_KEYWORD  */
    FLOAT_KEYWORD = 262,           /* FLOAT_KEYWORD  */
    CIN_KEYWORD = 263,             /* CIN_KEYWORD  */
    COUT_KEYWORD = 264,            /* COUT_KEYWORD  */
    WHILE_KEYWORD = 265,           /* WHILE_KEYWORD  */
    IF_KEYWORD = 266,              /* IF_KEYWORD  */
    PLUS_PLUS = 267,               /* PLUS_PLUS  */
    MINUS_MINUS = 268,             /* MINUS_MINUS  */
    LT = 269,                      /* LT  */
    GT = 270,                      /* GT  */
    LE = 271,                      /* LE  */
    GE = 272,                      /* GE  */
    EQ = 273,                      /* EQ  */
    NE = 274,                      /* NE  */
    SHIFT_LEFT = 275,              /* SHIFT_LEFT  */
    SHIFT_RIGHT = 276              /* SHIFT_RIGHT  */
  };
  typedef enum yytokentype yytoken_kind_t;
#endif
/* Token kinds.  */
#define YYEMPTY -2
#define YYEOF 0
#define YYerror 256
#define YYUNDEF 257
#define INT_CONST 258
#define FLOAT_CONST 259
#define ID 260
#define INT_KEYWORD 261
#define FLOAT_KEYWORD 262
#define CIN_KEYWORD 263
#define COUT_KEYWORD 264
#define WHILE_KEYWORD 265
#define IF_KEYWORD 266
#define PLUS_PLUS 267
#define MINUS_MINUS 268
#define LT 269
#define GT 270
#define LE 271
#define GE 272
#define EQ 273
#define NE 274
#define SHIFT_LEFT 275
#define SHIFT_RIGHT 276

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
union YYSTYPE
{
#line 11 "analizor.y"

    int int_val;
    float float_val;
    char *id;

#line 115 "y.tab.h"

};
typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;


int yyparse (void);


#endif /* !YY_YY_Y_TAB_H_INCLUDED  */
