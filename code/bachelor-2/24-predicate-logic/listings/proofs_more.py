"""proofs_more.py: the proof trees of exercises 7, 10 and 11."""
from checker import step as s

DE_MORGAN = (["~(P | Q)"],
             s("and_i", "~P & ~Q",
               s("not_i", "~P",
                 s("not_e", "false", s("or_i1", "P | Q", s("hyp", "P")),
                   s("hyp", "~(P | Q)"))),
               s("not_i", "~Q",
                 s("not_e", "false", s("or_i2", "P | Q", s("hyp", "Q")),
                   s("hyp", "~(P | Q)")))))

SWAP = (["exists x. forall y. R(x, y)"],
        s("forall_i", "forall y. exists x. R(x, y)",
          s("exists_e", "exists x. R(x, v)",
            s("hyp", "exists x. forall y. R(x, y)"),
            s("exists_i", "exists x. R(x, v)",
              s("forall_e", "R(u, v)", s("hyp", "forall y. R(u, y)"), term="v"),
              term="u"),
            term="u"),
          term="v"))

CONVERSE = (["forall y. exists x. R(x, y)"],  # an attempt; the checker refuses a step
            s("exists_e", "exists x. forall y. R(x, y)",
              s("forall_e", "exists x. R(x, v)",
                s("hyp", "forall y. exists x. R(x, y)"), term="v"),
              s("exists_i", "exists x. forall y. R(x, y)",
                s("forall_i", "forall y. R(u, y)", s("hyp", "R(u, v)"), term="v"),
                term="u"),
              term="u"))

EXCLUDED_MIDDLE = ([],
                   s("raa", "P | ~P",
                     s("not_e", "false",
                       s("or_i2", "P | ~P",
                         s("not_i", "~P",
                           s("not_e", "false", s("or_i1", "P | ~P", s("hyp", "P")),
                             s("hyp", "~(P | ~P)")))),
                       s("hyp", "~(P | ~P)"))))
