%token ID
%%
s : l '=' r | r ;
l : '*' r | ID ;
r : l ;
%%
