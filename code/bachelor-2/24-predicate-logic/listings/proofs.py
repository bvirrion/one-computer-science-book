"""proofs.py: proof trees as data, written as nested steps."""
from checker import step as s

MODUS_PONENS = (["P -> Q", "P"],
                s("imp_e", "Q", s("hyp", "P -> Q"), s("hyp", "P")))

SYLLOGISM = (["P -> Q", "Q -> R"],
             s("imp_i", "P -> R",
               s("imp_e", "R", s("hyp", "Q -> R"),
                 s("imp_e", "Q", s("hyp", "P -> Q"), s("hyp", "P")))))

NO_COUNTEREXAMPLE = ([],  # (P -> Q) -> ~(P & ~Q)
                     s("imp_i", "(P -> Q) -> ~(P & ~Q)",
                       s("not_i", "~(P & ~Q)",
                         s("not_e", "false",
                           s("imp_e", "Q", s("hyp", "P -> Q"),
                             s("and_e1", "P", s("hyp", "P & ~Q"))),
                           s("and_e2", "~Q", s("hyp", "P & ~Q"))))))

ALL = (["forall x. P(x) -> Q(x)", "forall x. P(x)"],
       s("forall_i", "forall x. Q(x)",
         s("imp_e", "Q(y)",
           s("forall_e", "P(y) -> Q(y)", s("hyp", "forall x. P(x) -> Q(x)"), term="y"),
           s("forall_e", "P(y)", s("hyp", "forall x. P(x)"), term="y")),
         term="y"))

WRONG_ALL = (["P(y)"],  # one element has the property, so all do?
             s("forall_i", "forall x. P(x)", s("hyp", "P(y)"), term="y"))
