%token IF C THEN ELSE OTHER
%%
s : IF C THEN s
  | IF C THEN s ELSE s
  | OTHER
  ;
%%
