# Book 1 (grades 1–9 and the typing appendix): chapter briefs

Phase A, written 2026-11-20 by the Book 1 writer. Binding inputs: `OUTLINE.md` (chapter list and ownership
maps), `sources/BATCH_BOOKS_1-5.md`, `sources/SERIES_DEFINITIONS.md`, `CONTRIBUTING.md`, `../book_style.md`.
Every term and label is listed in `sources/book1/DEFINITIONS.md`; this file says what each chapter does.
Items marked **(proposed)** go beyond the outline's one-paragraph description and wait for the sync.

## 0. Conventions for every chapter of this book

- **Bands.** Grades 1–5: 10–11 exercises, mostly ★, stars never decreasing, no weekend problem, no code
  printed. Grades 6–9: exactly 12 exercises, stars never decreasing (this book's default ramp is
  4★ / 5★★ / 3★★★), one weekend problem of 10–14 questions in Parts I–III, except the three project
  chapters (g7/06, g8/06, g9/07), which have milestones and no problem.
- **Kinds of exercise** (grades 6–9), coded in the briefs: **P** predict the output, **B** find and fix the
  bug, **S** write to a specification (tested solution under `exercises/`), **C** prove or count (prose
  solution). Grades 1–5, coded: **M** the machine, **F** files and windows, **N** numbers and binary,
  **A** an algorithm followed by hand, **R** reading a figure.
- **Code layout**: `code/grade-N/NN-slug/{listings,outputs,exercises,tests,figures}`. Every runnable
  listing is captured by `tools/capture_output.py`; every listing meant to work is called from a pytest
  file in `tests/` (Python only in this book); every `S` exercise has `exercises/<stem>.py` and a test.
  Listings are 3–25 lines, PEP 8, 88 columns, standard library only, no f-string tricks (plain
  `print(a, b)` and simple f-strings `f"{name} is {age}"` only, from g6/02).
- **Typed input** comes from `listings/<stem>.stdin` (echoed by the capture tool).
- **Turtle (g6/03 and later turtle exercises)** (sync): turtle listings are in `listings/NORUN.txt` (there
  is no display); `code/shared/turtlerec/` (written by Book 1, frozen) runs the unchanged listing with a
  recording stand-in for `turtle` and writes the path as `.dat` for the figure; `tests/` check each path
  against the expected polygon. The text says the reader sees the drawing in a window.
- **Town data** (sync): `town.load()` in Python listings where the reader need not see a file; a CSV copy
  under `listings/` only with a byte-equality test against `data/town/`; `copy=` in sessions.
- **Capture** (sync): `# capture: scratch` for listings that write files; toy `--trace` through a session with
  `copy=`; `code/grade-N/lib/` for modules shared by a grade's chapters.
- **Figures are uncounted**: referred to by place ("the drawing below"), never `\cref{fig:...}`.
- **Ledger**: ids `g<N>:<slug-word>:<fact>` and `typ:<fact>`, rows in `sources/ledger/book1.md`, cited by
  `% ledger:` next to the first use. Volatile facts in `dated{2026}` boxes.
- **Figures**: schematics ~3 per chapter in grades 1–5, ~4 in grades 6–9 (TikZ, `styles/onecs.sty`);
  AI illustrations of generic scenes, mostly grades 1–6 (file names `<prefix>-<slug>-<what>.jpg`);
  photographs of real hardware and historic machines, free licence only, read on the licence page first.
  Candidate photographs below are *what to look for*, not files already chosen.
- **Recall boxes** name the owner chapter (`\cref` inside this book) or the sister series in prose.
- No curriculum, country's school system, exam or university is named in print.

## 1. Programme check (Phase A requirement)

The outline's Book 1 list was written from knowledge of the programmes. On 2026-11-20 the current official
texts were read (fetched pages are data; the extracted text is in the writer's scratchpad,
`…/scratchpad/book1/prog/*.txt`). The 2020 consolidated primary and lower-secondary texts that the outline
had in mind have been replaced in the last three years, so the check is against the new texts.

| Key | Text (as printed on it) | Where | Grades here |
|---|---|---|---|
| C2-ST | *Programme de sciences et technologie du cycle 2*, annexe 1, BO n° 24 du 11 juin 2026 (CP from 2026-27) | education.gouv.fr/sites/default/files/document/annexe-1-programme-de-sciences-et-technologie-du-cycle-2-519020.pdf | 1–3 |
| C3-ST | *Programme de sciences et technologie du cycle 3*, annexe 2, BO n° 24 du 11 juin 2026 | education.gouv.fr/sites/default/files/document/annexe-2-programme-de-sciences-et-technologie-du-cycle-3-519023.pdf | 4–6 |
| C3-M | *Programme de mathématiques pour le cycle 3* (section *Initiation à la pensée informatique*; it also summarises what cycle 2 did) | education.gouv.fr/sites/default/files/ensel620_annexe2-v2.pdf (BO reference not printed on the extract; a secondary page dates it to the 2024 reform, in force from 2025) | 4–6 |
| C4-M | *Programme de mathématiques pour le cycle 4*, annexe 2 of the arrêté of 18 February 2026, BO n° 10 du 5 mars 2026 (5e from 2026-27) | education.gouv.fr/sites/default/files/document/Annexe%202%20%E2%80%93%20Programme%20de%20math%C3%A9matiques%20pour%20le%20cycle%204-480716.pdf | 7–9 |
| C4-T | *Programme de technologie du cycle 4*, annexe, BO n° 9 du 29 février 2024 | education.gouv.fr/sites/default/files/ensel802_annexe.pdf | 7–9 |
| CRCN | *Cadre de référence des compétences numériques* (16 competences in 5 domains; article D. 121-1), eduscol "repères de progressivité" document | eduscol.education.gouv.fr/sites/default/files/document/reperesprogressiviteaccessible1125453pdf-80451.pdf | 1–9 |

All accessed 2026-11-20. The block-programming items of C3-M, C4-M and C4-T are met in Python from grade 6
(user ruling, 2026-11-19); "the link between block and text programming" has nothing to map to.

### 1a. Item → chapter

| Text | Item (French wording shortened) | Chapter(s) |
|---|---|---|
| C2-ST CE1 | Commander un robot ... en programmant un déplacement | g1/02, g4/03 |
| C2-ST CE2 | Identifier les dispositifs de saisie, traitement, restitution (clavier, processeur, écran) | g1/01, g3/02 |
| C2-ST CE2 | Utiliser un ordinateur ou une tablette pour saisir un texte; correcteur orthographique; mise en forme et mise en page; sauvegarder | g3/01 (typing), g2/02 (saving); **word processing: g2/02 (proposed section)** |
| C2-ST CE2 | Utiliser un moteur de recherche | g5/03 (told) |
| C2-ST CE2 | Initier à la programmation d'objets techniques par des algorithmes simples; identifier le programme d'un déplacement observé | g1/02, g4/03 (by hand) |
| C2-ST CE2 | Technologies numériques présentes dans les objets | g1/01 (hidden computers) |
| C3-ST CM1 | Traduire un programme simple en langage naturel; agir sur un objet par un programme; comparer des programmes pour un trajet en un temps minimum | g4/03 (counting steps of two algorithms) |
| C3-ST CM2 | Comprendre un algorithme; repérer boucles et conditions; modifier, tester, valider; essai-erreur | g4/03, g6/03–05, g7/05 |
| C3-M | Codages de déplacements (quartier, ville), programmation de robot | g1/02, g4/03 |
| C3-M | Programmes de construction géométrique | g6/03 (turtle) |
| C3-M | Programmes de calcul (jusqu'à trois instructions) | g6/01, g6/02 |
| C3-M | Suites évolutives, termes éloignés (blocs ou tableur) | g6/03 and g6/05 exercises; **spreadsheet: g8/03 (proposed section)** |
| C3-M | Algorithmes des opérations posées | g4/03 (column addition as an algorithm, proposed example), g8/01 (binary addition) |
| C3-M 6e | Instruction, séquence, entrées, sorties, répétitions; répéter à la main; programmer un chemin simple | g1/02, g4/03, g6/01–03 |
| C4-M 5e | Instructions séquencées; entrées et sorties; expression informatique; prévoir une valeur; analyser et modifier un programme; boucle inconditionnelle | g6/01–03 |
| C4-M 4e | Conditions simples; instruction conditionnelle; variable; écrire et modifier un programme | g6/02, g6/04 |
| C4-M 3e | Variables approfondies; conditions composées; boucle conditionnelle; structurer des programmes | g6/04, g6/05, g7/01 |
| C4-M | Conjectures à l'aide d'un algorithme ou d'un tableur | g9/04, g9/05 (algorithm); spreadsheet: g8/03 (proposed) |
| C4-M | Simuler des expériences aléatoires; stabilisation des fréquences | g9/05 |
| C4-M (prolongement) | Algorithmes d'extraction de racines carrées | **g9/04 (proposed section: a square root by halving)** |
| C4-M (prolongement) | L'échiquier de Sissa (puissances) | g8/01 weekend problem |
| C4-T | Fichiers (texte, image, tableur ou CSV), dossiers, arborescence | g3/03, g8/03 |
| C4-T | Extension et format de fichiers | g3/03 |
| C4-T | Droits d'écriture et de lecture sur les fichiers | told in g3/03; defined in Book 2 (g11 permissions) |
| C4-T | Bit, octet et leurs multiples; ordre de grandeur de la taille d'un fichier image, son, vidéo | g4/01, g5/01, g5/02 |
| C4-T | Incidences du stockage et des flux de données | g8/05 `dated` box on the electricity of data centres (proposed; ledger) |
| C4-T | Vocabulaire des données: objet, descripteur, collection (liste), type (chaîne, nombre, booléen), données structurées | g6/02, g6/04, g7/02, g8/02, g8/03 |
| C4-T | Le bit; représentation des booléens, des mots (code ASCII étendu), des entiers naturels | g5/01, g5/02, g6/04, g8/01 (one-byte extensions: Book 2 g10) |
| C4-T | Traitement de données (calculs, filtre, tri) dans un tableur | g8/03 in Python; **spreadsheet section proposed** |
| C4-T | Capteurs, microcontrôleur, interface humain–machine (boutons, afficheurs) | g1/01, g3/02 (told); owned by Book 2 g10 |
| C4-T | Réseau local et Internet; terminal, carte réseau, liaisons filaires et sans fil, commutateur, routeur, serveur | g5/03, g8/05 (switch and network interface added to the brief) |
| C4-T | Rôle et structure d'une adresse IP; rôle des tables de routage | g8/05 (address: four bytes; routing tables told; defined in Book 2 g11) |
| C4-T | Paramétrer une adresse IP fixe | told in g8/05 (no real configuration printed: no real network) |
| C4-T | Le débit et les ordres de grandeur | g8/05 (bit rate, latency) |
| C4-T | Affectation, variable, opérateurs arithmétiques et logiques (ET, OU, NON), conditionnelle, itératives, listes, séquences | g6/01–05, g7/02 |
| C4-T | Événement; déclenchement d'une séquence par un événement | not defined in Book 1 (Book 2 g10, state machines); g9/07 project's turn loop reacts to each typed move |
| C4-T | Entrées/sorties: capteurs, IHM, actionneur, fichiers | g6/02 (keyboard input), g8/03 (files); sensors and actuators: Book 2 g10 |
| C4-T | Modularité: sous-programme, fonction; structuration, commentaires | g6/01 (comments), g7/01, project chapters |
| C4-T | Protocole de test; mise au point | g7/05, g7/06, g8/06, g9/07 |
| C4-T | Cybersécurité: identification, authentification | g5/03 (password, authentication proposed) |
| CRCN 1.1 | Recherche d'information | g5/03 (search engines, told) |
| CRCN 1.2 | Gérer des données (sauvegarder, retrouver, organiser des dossiers, formats) | g2/02, g3/03, g4/01 (backups) |
| CRCN 1.3 | Traiter des données | g8/03 |
| CRCN 3.1 | Documents textuels | g2/02 (proposed), g3/01 |
| CRCN 3.2 | Documents multimédia | g5/02 (representation only) |
| CRCN 3.4 | Programmer | g6–g9 |
| CRCN 4.1 | Sécuriser l'environnement numérique | g4/02 (updates), g5/03 (passwords) safety boxes |
| CRCN 4.3 | Santé (posture) | g2/01, g3/01 (sitting well) |
| CRCN 5.1, 5.2 | Résoudre des problèmes techniques; évoluer dans un environnement numérique | g2/02, g3/03, g4/02, g7/05 |

### 1b. Items no chapter of Book 1 covers

| Item | Why | Proposal |
|---|---|---|
| Spreadsheet: formulas, filter, sort (C3-M, C4-M, C4-T, CRCN 1.3) | no chapter names a spreadsheet; the series prints no product screenshots | add a section to g8/03: the same CSV table opened in "a spreadsheet program", drawn generically in TikZ; a formula, a sort, a filter; why a program repeats exactly (proposed) |
| Word processing: spell checker, formatting, layout (C2-ST, CRCN 3.1) | g2/02 is about windows and saving | add a section to g2/02: a text editor versus a word processor, drawn generically (proposed) |
| Square-root extraction algorithm (C4-M) | g9/04 stops at the square root but does not compute one | add a short section to g9/04: approximating √n by halving an interval, which reuses g8's halving (proposed) |
| Events (C4-T) | no Book 1 chapter has events; Book 2 g10 owns the state machine | none in Book 1; Book 2 g10 defines *event* |
| Read and write rights on files (C4-T) | permissions belong to Book 2 g11 | told in one sentence in g3/03 |
| Microcontroller, sensors, actuators (C4-T) | Book 2 g10 owns sensors and actuators | told in g1/01 and g3/02; no definition here |
| Routing tables (C4-T) | Book 2 g11 owns the routing table | told in g8/05 ("each router keeps a table of directions") |
| Personal data, cookies and traces, intellectual property, cyberviolence, e-mail and collaboration tools (C4-T, CRCN 2.x, 4.2) | "technical content only" (outline rule) | none: deliberately out of scope; cookies are Book 2 g10 |
| Environmental cost of storage and networks (C4-T) | technical, but no chapter has it | a `dated{2026}` box in g8/05 (proposed; needs a ledger row from an energy agency's report) |

Nothing the official texts ask for in computing is missing from Books 1–2 taken together, except the
excluded civic items; the gaps above that are Book 1's own are four small additions inside existing
chapters. The outline brings much down earlier than the texts do (functions, lists, strings, dictionaries,
the processor, logic gates, HTML, cryptography), as `outline_sources.md` says.

## 2. Page budget

| Band | Chapters | Pages per chapter (with solutions) | Pages |
|---|---:|---:|---:|
| grades 1–5 | 13 | ~7 | ~91 |
| grades 6–9, ordinary | 21 | ~11 | ~231 |
| grades 7–9, projects | 3 | ~11 | ~33 |
| typing appendix | 1 | ~12 | ~12 |
| front matter, part pages, index | | | ~15 |
| **total** | **38** | | **~382** (target ~380) |

## 3. Grades 1–5 (no code; ~7 pp each; 10–11 exercises, mostly ★)

Register: short sentences, one idea per paragraph, a worked example after each definition, precise words
from the first page (computer, input, output, processor, memory, storage, file, folder, algorithm, bit,
byte). No invented object names a concept. Children in the scenes have ordinary names (Mia, Tom, Lina,
Sami, Noor, Leo) and no surnames.

### g1/01 What Is a Computer? (`what-is-a-computer`)

- **Hook.** Mia counts the computers in her kitchen: the laptop on the table, her father's phone, and
  three she cannot see (in the oven's timer, the washing machine, the car key in the bowl).
- **Sections.**
  1. *Computers around us*: desktop computer, laptop, tablet, phone; the hidden computers inside a washing
     machine, a car, a toy, a lift; a computer is a machine.
  2. *A machine that follows instructions*: a computer does exactly what its instructions say, very fast,
     without getting tired, and nothing else; people write the instructions (a word for them, *program*,
     comes in grade 4: here only "instructions").
  3. *What goes in and what comes out*: input (a key pressed, a click, a sound, a photo taken), the
     computer works on it, output (letters on the screen, a sound, a printed page). A washing machine's
     input is a turn of the dial and the water level it measures (told; no definition of *sensor*).
  4. *The parts we can see and touch*: screen, keyboard, mouse, touchpad, speakers, microphone, camera,
     printer; sorting them into input devices, output devices, and devices for both (a touch screen).
- **Defines.** computer; input; output; input device; output device.
- **Recalls.** — (first chapter).
- **Figures.** Schematics (3): (a) the input → computer → output diagram with three worked examples
  (key → letter on screen; click → song plays; dial → drum turns); (b) a labelled drawing of a laptop and
  a desktop computer with its screen, keyboard, mouse, speakers, camera (generic shapes, no brand);
  (c) a three-column sorting chart (input / output / both) with drawn device icons.
  AI: `g1-what-is-a-computer-kitchen.jpg` (a family kitchen with a laptop, a phone, a washing machine and a
  microwave oven, nothing readable), `g1-what-is-a-computer-devices.jpg` (a child's desk with a tablet,
  headphones and a mouse). Photo (history box *The first computers filled a room*): ENIAC in the late 1940s
  (US Army photograph, public domain on Commons; licence page to be read).
- **Exercises (11: 8★, 3★★).** M: which of these objects contain a computer (lamp, phone, oven with a
  timer, chair, car); M: input or output for each of eight devices; M: what comes in and goes out when you
  take a photo with a tablet; M: a touch screen is both — why; R: name the labelled parts in figure (b);
  M: three computers in a school; M: a calculator — is it a computer? (★★, explain with
  "follows instructions"); M: the washing machine's input and output (★★); M: design-your-own: a toy robot
  that stops when it meets a wall — what goes in, what comes out (★★).
- **Ledger.** `g1:eniac:dates` (completion 1945/46 and size, from a museum or university page, e.g. the
  Smithsonian or Penn Engineering); nothing else.

### g1/02 Instructions in Order (`instructions-in-order`)

- **Hook.** Tom writes the steps for making a jam sandwich for his little brother; his brother follows
  them exactly and spreads jam on the closed jar.
- **Sections.**
  1. *A task as a list of steps*: a recipe, getting dressed, brushing teeth; each step is one instruction.
  2. *The order matters*: socks before shoes; swapping two steps breaks the result; some steps can swap
     without harm (putting on gloves).
  3. *Guiding on a grid*: a robot on a squared mat understands three instructions: forward one square,
     turn left (a quarter turn), turn right; reading and writing a list of arrows; the robot turns on the
     spot.
  4. *Finding the wrong step*: run the steps one at a time with a finger on the grid, find where the robot
     leaves the path, fix that one step.
- **Defines.** instruction; sequence of instructions.
- **Recalls.** g1/01 (a computer follows instructions).
- **Figures.** Schematics (4): (a) the sandwich steps as numbered cards, correct and swapped; (b) the
  robot grid (6 × 5) with start, a goal, and the drawn path for a printed sequence; (c) the three
  instruction symbols (forward arrow, curved left, curved right) with the robot's heading before and
  after; (d) a sequence with one wrong step, the path drawn until it goes wrong, and the corrected path.
  AI: `g1-instructions-in-order-floor-robot.jpg` (two children with a small round floor robot on a
  squared mat, no brand, no letters).
- **Exercises (10: 7★, 3★★).** A: put five steps of getting dressed in order; A: which two steps can be
  swapped; A: follow a printed sequence on the grid and mark where the robot ends; A: write the sequence
  that reaches the star; A: the robot ends one square too far — find the wrong instruction; R: which
  sequence draws the drawn path (three choices); A: count the instructions of two sequences that reach the
  same square; A (★★): the shortest sequence to the goal around an obstacle; A (★★): a sequence that goes
  back to the start; A (★★): the same goal with only "forward" and "turn right" allowed.
- **Ledger.** none.

### g2/01 The Keyboard and the Mouse (`keyboard-and-mouse`)

- **Hook.** Lina types her name for the first time; the first letter comes out small, and a space appears
  where she wanted a new line.
- **Sections.**
  1. *The keys*: letter keys, digit keys, the space bar, Enter, Backspace (and Delete), Shift (a capital
     while it is held), Caps Lock (told), the arrow keys; what each does to the text and to the cursor.
  2. *Sitting well*: back against the chair, feet flat, forearms level, the screen at about arm's length
     and the top of the screen near eye height, hands resting loosely; a break every so often.
  3. *The pointer*: moving the mouse moves the pointer; pointing, clicking, double-clicking,
     right-clicking (told), dragging; the cursor in a text versus the pointer.
  4. *Touchpad and touch screen*: one finger moves the pointer; a tap is a click; on a touch screen the
     finger is the pointer: tap, press and hold, swipe, pinch to zoom.
- **Defines.** key (of a keyboard); cursor; pointer; click; double-click; drag; touchpad; touch screen.
- **Recalls.** g1/01 (keyboard, mouse, touch screen as input devices).
- **Figures.** Schematics (3): (a) a drawn keyboard (TikZ `keycap`, layout-neutral: letter keys left blank
  except the ones the text names, special keys labelled with `\key{...}` names) with the five key groups
  coloured; (b) the pointer actions as small strips (press–release; press–release twice; press–move–
  release); (c) a side view of a child sitting well, with the three angles marked qualitatively.
  AI: `g2-keyboard-and-mouse-sitting-well.jpg` (a child at a desk with a desktop computer, side view),
  `g2-keyboard-and-mouse-touchpad.jpg` (a hand on a laptop touchpad, keys out of focus, no letters).
- **Exercises (11: 8★, 3★★).** M: which key makes a capital, which deletes the letter before the cursor,
  which starts a new line; M: what Shift + 1 might give (look at your own keyboard); M: the difference
  between the cursor and the pointer; M: name each action from its strip; M: three things that are wrong
  in a drawn posture; M: tap, swipe or pinch for three tasks; R: in figure (a), which group is each named
  key in; M (★★): type "Hi Sam" — list the keys in order; M (★★): drag versus click; M (★★): a word was
  typed with Caps Lock on — what happened and how to fix it.
- **Ledger.** `g2:ergonomics:screen` (screen distance and height, from a health-and-safety agency's
  workstation guidance, e.g. a national occupational-safety page; fetched, not remembered).

### g2/02 Using a Computer (`using-a-computer`)

- **Hook.** Sami's drawing is gone: he closed the program without saving, and the computer did not keep it.
- **Sections.**
  1. *Switching on and shutting down properly*: the power button; waiting for the computer to be ready;
     shutting down from the menu so that the computer can finish writing what it is saving; never pulling
     the plug on purpose.
  2. *The desktop, icons and windows*: the desktop; an icon stands for a program or a file; a window shows
     one program's work; opening, closing, moving (drag the title bar), resizing (drag a corner),
     minimising; several windows at once.
  3. *Starting a program*: from an icon or a menu; a program opens in a window; closing it ends it.
  4. **(proposed)** *Writing a text*: a text editor keeps only letters; a word processor also keeps bold,
     sizes, colours and the page layout, and can underline misspelt words; the same short letter in both,
     drawn as two generic windows.
  5. *Saving and finding work again*: saving copies the work so that it is still there after the
     computer is switched off (the reason, storage, is grade 3); "Save" and "Save as"; choosing where;
     a good name: short, says what it is, with a date if there are several versions; finding it again
     from the folder where it was saved (folders are grade 3: here, "the place where it was saved").
- **Defines.** desktop; icon; window; menu; saving (to save work).
- **Recalls.** g2/01 (pointer, click, drag); g1/01 (screen).
- **Figures.** Schematics (4): (a) a desktop with three icons and two overlapping windows (TikZ `window`
  pics); (b) one window with its parts labelled (title bar, close, minimise and maximise buttons, a menu,
  the work area, the resizing corner); (c) (proposed) the same letter in a text editor and in a word
  processor; (d) a generic "Save as" dialog with a name box and a place list, the good name filled in.
  AI: `g2-using-a-computer-saving.jpg` (a child at a laptop in a classroom, screen not readable).
  Safety box: save often; shut down from the menu.
- **Exercises (11: 8★, 3★★).** F: name the parts of a drawn window; F: how to move a window, how to make
  it bigger; F: why shut down from the menu; F: three good and three bad file names, sorted; F: "Save" or
  "Save as" for a new copy; F: Sami's lost drawing — what should he have done; R: which window is in front
  in figure (a); F (proposed): bold in a text editor? (★); F (★★): two versions of a story — name them;
  F (★★): a program does not answer — what to try first (wait; then close the window); F (★★): order the
  steps from switching on to finding yesterday's work.
- **Ledger.** none.

### g3/01 Typing with Ten Fingers (`typing-with-ten-fingers`)

- **Hook.** Noor types with two fingers, eyes going from the keys to the screen; her big sister types
  without looking and twice as fast.
- **Sections.**
  1. *The home row*: the eight fingers rest on the middle row of letters; the two marked keys (a small
     bump) under the index fingers let the hands find the row without looking; the thumbs on the space bar.
  2. *Which finger strikes which key*: each finger owns a column, slanted; the index fingers own two
     columns each; the little fingers own the edge keys (Shift, Enter, Backspace); every finger comes back
     home after each key.
  3. *Eyes on the screen*: why looking at the keys slows typing; reading the screen to catch mistakes.
  4. *Capitals, digits and punctuation*: capitals with the Shift of the other hand; reaching up to the
     digit row; the punctuation keys.
  5. *Accuracy before speed*: practising slowly and without mistakes first; counting speed in words per
     minute (a word counts as five characters, spaces included); a short timed test computed by hand.
  Keyboard layouts differ between countries: the chapter draws QWERTY, AZERTY and QWERTZ side by side
  (the technique is the same; the keys under the fingers change) and points to the appendix drills.
- **Defines.** touch typing; home row; keyboard layout; words per minute.
- **Recalls.** g2/01 (the keys, Shift, sitting well).
- **Figures.** Schematics (4): (a) the home row with the hands' resting fingers and the two marked keys
  (QWERTY in the body; the other layouts in figure c); (b) the finger zones coloured on a full QWERTY
  keyboard (eight colours, legend); (c) three small keyboards, QWERTY, AZERTY, QWERTZ, letter rows only,
  the keys that differ highlighted (positions checked against the layout files, ledger); (d) the "Shift
  with the other hand" diagram (left little finger on right Shift for a capital J, and the reverse).
  AI: `g3-typing-with-ten-fingers-hands.jpg` (two hands resting on a keyboard's middle row, seen from
  above at an angle; keys without letters). Photo (history box *Why the letters are in this order*): an
  1870s typewriter with the first QWERTY-like layout (Commons; public domain if the photograph allows).
- **Exercises (11: 7★, 4★★).** M: which finger types each of eight letters (QWERTY; the solution also
  gives AZERTY and QWERTZ where they differ); M: which Shift for a capital A, a capital L; M: what the
  bumps are for; N: a child typed 150 characters in 2 minutes — words per minute; N: 30 words per minute
  for 3 minutes — how many characters; M: three things that slow down typing; R: in figure (c), which
  letters move between QWERTY and AZERTY; M (★★): list the fingers used to type "home"; N (★★): two
  children compared — 120 characters in one minute with 6 mistakes or 100 with none, which is the better
  practice and why; N (★★): plan a practice: 10 minutes a day — how many days to reach 15 hours; M (★★):
  why the index fingers own two columns.
- **Ledger.** `typ:layout:us`, `typ:layout:fr`, `typ:layout:de` (key positions, from the xkeyboard-config
  symbol files `us`, `fr`, `de`: source the upstream repository URL, version and access date; the local
  copy in `/usr/share/X11/xkb/symbols/` is the same data); `typ:bumps` (marked home keys: a primary source
  to be found, e.g. a standard's public abstract or a keyboard maker's specification; if none, the
  sentence is reworded as "most keyboards have"); `typ:qwerty:patent` (Sholes, Glidden and Soule's
  typewriter patent, 1868, from a patent office record) for the history box. The words-per-minute
  convention is a definition of the book, not a ledger fact.

### g3/02 Inside the Computer (`inside-the-computer`)

- **Hook.** The school's old computer is opened on the teacher's desk: wires, a fan, a big green board,
  and small black squares.
- **Sections.**
  1. *The processor*: the part that carries out the instructions, one after another, very fast; it gets
     hot.
  2. *The memory*: holds what the computer is working on right now (the open drawing, the program
     running); it forgets when the power goes off (the details are grade 4).
  3. *The storage*: keeps files when the power is off.
  4. *The motherboard, the power and the heat*: the board links all parts; the power supply or the
     battery; heat and the fan, why air vents must stay free.
  5. *Ports and devices*: sockets on the outside where devices plug in; input, output, or both; cables and
     radio (a wireless mouse); some ports carry power (charging).
  A remark tells that a washing machine has a small computer on one chip (no definition).
- **Defines.** processor; memory (of a computer); storage; motherboard; device (plugged-in device,
  peripheral). (*memory* here is the working memory; *RAM* is defined in g4/01.)
- **Recalls.** g1/01 (computer, input, output devices).
- **Figures.** Schematics (3): (a) a block diagram: processor, memory, storage, ports, arrows for data;
  (b) a labelled drawing of an open desktop case (motherboard, processor under its fan, memory sticks,
  storage, power supply), generic; (c) the outside of a laptop with its ports drawn generically and
  labelled by what they connect (a screen, a mouse, headphones, power), names of the standards in the
  caption only if ledgered.
  Photos: a desktop motherboard (Commons, CC), a processor chip seen close, an open desktop case.
  AI: `g3-inside-the-computer-open-case.jpg` (a teacher and two children looking into an open computer
  case on a desk, no brand).
- **Exercises (10: 7★, 3★★).** M: which part carries out the instructions; M: where a saved file is kept;
  M: what is lost when the power goes off without saving, and why; M: label figure (b); M: why a laptop's
  vents must not be covered; M: input, output or both for six things plugged into ports; R: follow the
  arrows of figure (a) when a key is pressed; M (★★): memory or storage for five situations; M (★★): a
  tablet has no fan — where does its heat go (told answer: through its case); M (★★): what the battery
  replaces in a laptop.
- **Ledger.** `g3:ports:usb` and `g3:ports:hdmi` only if the names are printed (the standards bodies'
  pages); a `dated{2026}` box "a laptop in 2026" (memory and storage sizes of a typical school laptop) with
  `g3:laptop:2026` from a maker's specification page.

### g3/03 Files and Folders (`files-and-folders`)

- **Hook.** Leo cannot find his poem: the desktop is covered with forty icons called "untitled".
- **Sections.**
  1. *A file holds one piece of work*: a story, a drawing, a song, a program; a file has a name.
  2. *Kinds of file and their extensions*: the end of the name after the dot tells the kind (`.txt` text,
     `.png` and `.jpg` picture, `.mp3` sound, `.mp4` video, `.py` a program); a program opens the kinds
     it knows; changing the extension does not change what is inside. A sentence tells that a file can be
     made read-only (rights are defined in a later year).
  3. *Folders inside folders*: a folder holds files and other folders; the folders form a tree, drawn
     upside down, with one folder at the top.
  4. *The path to a file*: the folders from the top down to the file, written with `/` (other systems
     write `\`, told); reading and writing a path.
  5. *Copying, moving, renaming, deleting*: copy keeps both, move keeps one; renaming; deleting sends the
     file to the bin, from which it can still come back until the bin is emptied.
- **Defines.** file; file name; extension (of a file name); folder; folder tree; file path; copy and move
  (one definition); bin (recycle bin).
- **Recalls.** g2/02 (saving, a good name); g3/02 (storage keeps files).
- **Figures.** Schematics (4): (a) a folder tree (`forest`) for Leo's computer (Documents → School →
  Poems → `poem.txt`, Pictures, Music); (b) the same tree with one path highlighted and written below;
  (c) a generic file-manager window (TikZ `window`) showing a folder's contents as icons with names and
  extensions; (d) copy versus move as before/after trees.
  AI: `g3-files-and-folders-desk.jpg` (a tidy desk with labelled paper folders in a box, no readable
  text), echoing the computer's folders.
- **Exercises (11: 8★, 3★★).** F: the kind of each of eight files from its extension; F: write the path to
  a file in figure (a); F: which folder holds a given path's file; F: copy or move for three situations;
  F: where a deleted file goes; F: draw the tree for a short description; F: a good folder plan for a
  school year; R: count the files and folders in figure (a); F (★★): Leo renames `poem.txt` to `poem.jpg` —
  what happens when he opens it; F (★★): two files can have the same name in two folders, but not in one
  — why; F (★★): the shortest list of moves to tidy a drawn desktop into a tree.
- **Ledger.** `g3:extensions` (media types for the named extensions, from the IANA media-types registry),
  only if the chapter names the format behind an extension.

### g4/01 Memory and Storage (`memory-and-storage`)

- **Hook.** The power goes off in the middle of a game; when it comes back, the game starts from the last
  save, not from where Mia was.
- **Sections.**
  1. *RAM: fast, and emptied when the power goes*: what the memory of g3/02 is made of (chips on small
     boards); fast to read and write; everything in it is lost at power-off.
  2. *Storage that keeps everything*: the hard disk (spinning platters coated with a magnetic layer, a
     read–write head on an arm that never touches, a motor); the SSD (flash memory, no moving part, faster,
     quieter, tougher); the USB stick and the memory card (flash memory too); comparing them (speed,
     moving parts, what happens if dropped).
  3. *Measuring size in bytes*: the byte as the unit (one byte holds one letter of plain text); kilobyte,
     megabyte, gigabyte, terabyte, each a thousand times the one before (a remark: some programs count by
     1,024, told); scale comparisons computed in the text: a page of text (about 2,000 letters, so about
     2 kilobytes), a photo kept as three numbers per pixel (computed for a stated size; compression is
     Book 2's), a film (told with its own computation per second).
  4. *Why keep a backup*: a disk can fail, a laptop can be lost; a second copy somewhere else; how often
     (safety box).
- **Defines.** RAM; hard disk; flash memory; SSD; byte; kilobyte, megabyte, gigabyte, terabyte (one
  definition); backup. **Ownership note:** the outline's g4 text names "byte" while the map gives
  "bit, byte" to g5; this brief defines the byte as a *unit of size* here and leaves g5 the bit and the fact
  that a byte is eight bits (proposed; see DEFINITIONS.md).
- **Recalls.** g3/02 (memory, storage).
- **Figures.** Schematics (3): (a) a hard-disk schematic (platters, spindle, arm, head, the head above
  the surface), drawn to show the moving parts; (b) the RAM/storage diagram: power on, power off, what
  stays; (c) a size ladder from a letter to a terabyte, each step ×1,000, with the computed examples placed
  on it. Photos: an opened hard disk (Commons), an SSD, a RAM module, a USB stick and memory card;
  history box *Five megabytes on fifty disks*: the IBM 350 disk unit of 1956 (photograph from Commons
  or a museum, licence read). AI: `g4-memory-and-storage-backup.jpg` (a family plugging an external disk
  into a laptop).
- **Exercises (11: 8★, 3★★).** M: which keeps the work at power-off, RAM or SSD; M: two differences
  between a hard disk and an SSD; N: how many kilobytes in 3 megabytes; N: a 2-kilobyte page — how many
  pages in 1 megabyte; N: order five sizes; M: why a backup is kept in another place; R: read figure (c)
  for the size of a stated example; N: a 64-gigabyte stick and 4-megabyte photos — how many photos
  (computed); N (★★): a text of 12,000 letters — how many kilobytes; M (★★): Mia's game lost its progress —
  which part forgot it; M (★★): a plan of backups for a school class.
- **Ledger.** `g4:si:prefixes` (kilo = 10^3 … tera = 10^12, from the SI brochure of the BIPM);
  `g4:iec:binary-prefixes` (kibi = 1,024, from the IEC's or a standards body's page) for the remark;
  `g4:ibm350` (1956, capacity, from IBM's archives or the Computer History Museum); `g4:hdd:rpm` (typical
  spindle speeds, from a maker's datasheet) if printed; a `dated{2026}` box of typical capacities
  (laptop SSD, USB stick) with `g4:sizes:2026` from makers' pages.

### g4/02 Programs and the Operating System (`programs-and-operating-system`)

- **Hook.** Tom's tablet shows "updating…" and he cannot play; what is being changed, and by whom?
- **Sections.**
  1. *A program is a list of instructions*: written by people, kept as a file in storage, copied into
     memory to run; the processor carries out its instructions (recall g3/02).
  2. *Applications*: programs for a task (drawing, writing, a game, a browser); one application can run in
     several windows.
  3. *The operating system*: the program that starts first and runs the others; it manages files, memory,
     devices and users (accounts, passwords told); the user talks to applications, applications ask the
     operating system, the operating system drives the hardware.
  4. *Starting up*: what happens between the power button and the desktop (a small program in the
     motherboard starts the operating system from storage), told as a sequence.
  5. *Installing and updating*: installing copies a program into storage; an update replaces parts of a
     program to fix mistakes and close security holes (safety box: accept updates, install only from
     trusted places). A `dated{2026}` box: the main families of operating systems for computers, phones and
     tablets.
- **Defines.** program; application; operating system; starting up (start-up); installing and updating
  (one definition: installation, update); user account.
- **Recalls.** g3/02 (processor, memory, storage); g3/03 (file); g2/02 (window, starting a program).
- **Figures.** Schematics (3): (a) the layers: user, applications, operating system, hardware, with the
  arrows of a request ("save this drawing") going down and up; (b) the start-up sequence as a timeline;
  (c) what the operating system manages, as four arrows to files, memory, devices and users.
  AI: `g4-programs-and-operating-system-update.jpg` (a child waiting by a tablet showing a progress
  circle, nothing readable).
- **Exercises (10: 7★, 3★★).** M: program or not (a recipe card, a game, a photo, a text editor);
  M: three jobs of the operating system; M: where a program is kept when the computer is off; M: put the
  start-up steps in order; M: why updates matter; R: follow figure (a) for "print this page"; M: an
  application or the operating system for five tasks; M (★★): two users on one computer — what the
  operating system keeps apart; M (★★): why a program must be copied into memory to run; M (★★): a
  message offers an update from an unknown website — what to do.
- **Ledger.** `g4:os:families:2026` (names and kinds of devices, from each maker's or project's own
  page) for the dated box; `g4:unix:1969` and `g4:linux:1991` only if a history sentence names them (Bell
  Labs or Nokia Bell Labs page; the first Linux announcement archive).

### g4/03 Algorithms: Repeat and Decide (`algorithms-repeat-and-decide`)

- **Hook.** At the card table, Lina finds the largest card of a row without sorting them: she keeps the
  best card so far in her hand and looks at each card once.
- **Sections.**
  1. *What an algorithm is*: a precise method, written as instructions, that always ends and gives its
     result; the same steps work for any row of cards, any grid; written in words, no programming
     language; the written method for adding two numbers in columns is an algorithm (proposed example).
  2. *Repeating*: repeat a group of steps a given number of times ("repeat 4 times: forward, turn
     right" draws a square on the grid); repeat until something happens ("forward until the wall").
  3. *Deciding*: if … then … otherwise; a condition is a question whose answer is yes or no.
  4. *Following an algorithm by hand*: the robot on a grid with a repeat and a decision ("until the
     goal: if the square ahead is free, forward, otherwise turn right"); the largest card of a row, with a
     table of "card looked at / best so far"; counting the steps of two algorithms that reach the same
     goal, and choosing the shorter.
- **Defines.** algorithm; loop (repetition); condition.
- **Recalls.** g1/02 (instruction, sequence, the robot grid).
- **Figures.** Schematics (4): (a) "repeat 4 times" drawn as a bracket around two cards and the square it
  draws on the grid; (b) a repeat-until on a grid with a wall; (c) a decision drawn as a diamond with yes
  and no arrows (a first flowchart, no defined term); (d) the row of cards with the best-so-far card
  marked at each step (the table beside it).
  AI: `g4-algorithms-repeat-and-decide-cards.jpg` (children playing with numbered cards on a table; the
  numbers are drawn over in TikZ if the image's are not legible, else the image has none).
- **Exercises (11: 8★, 3★★).** A: follow "repeat 3 times: forward 2, turn left" on the grid; A: write
  a repeat that draws a rectangle; A: the largest card of a printed row with the table; A: the smallest
  card (change one word of the algorithm); A: yes or no — which are conditions; A: follow a robot with an
  if; A: a column addition, step by step, as an algorithm; R: which of two drawn programs draws figure X;
  A (★★): count the steps of two algorithms for the same path; A (★★): an algorithm that never ends — what
  is missing; A (★★): an algorithm that counts the red cards of a row.
- **Ledger.** none.

### g5/01 Bits and Bytes: Counting in Binary (`bits-and-bytes`)

- **Hook.** Sami and Noor signal across the playground with a torch: on or off; with two torches they
  agree on four messages.
- **Sections.**
  1. *Two states are enough*: on/off, magnetised one way or the other, charged or not; the bit is one
     such choice, written 0 or 1.
  2. *Counting with two digits*: five cards showing 1, 2, 4, 8 and 16 dots, face up (1) or face down (0);
     each card has twice the dots of the one on its right; any number from 0 to 31 is one way of turning
     the cards; reading and writing numbers in binary.
  3. *A byte is eight bits*: eight cards, the largest worth 128; 0 to 255 on one byte; the byte of g4/01
     is eight bits (recall, adds the bits).
  4. *Each extra bit doubles the patterns*: one bit, two patterns; two bits, four; three bits, eight
     (drawn as a tree of choices); counted by doubling only (no powers notation: the mathematics books
     bring powers in grade 8).
- **Defines.** bit; binary (writing a number in binary, binary number). (The byte is g4/01's; this
  chapter adds that it is eight bits.)
- **Recalls.** g4/01 (byte as a unit); g3/02 (storage).
- **Figures.** Schematics (4): (a) the five dot cards with 13 shown as 01101; (b) a row of eight lamps,
  on and off, for a byte, with the card values above; (c) the tree of choices for 1, 2 and 3 bits; (d) a
  hard-disk surface or flash cells as two states (a simplified drawing, told).
  AI: `g5-bits-and-bytes-torches.jpg` (two children signalling with torches in a playground at dusk).
- **Exercises (11: 8★, 3★★).** N: write 5, 9, 20 in binary with the cards; N: which number is 10110;
  N: the largest number on four cards, on five, on eight; N: how many patterns on 4 bits (doubling);
  N: count from 0 to 7 in binary; N: the number of bits needed for 40 (try cards); R: read the lamps of a
  drawn byte; M: two states in three machines; N (★★): add 1 to 0111 with the cards — what happens to the
  cards; N (★★): a code of 6 bits for 50 classmates — enough?; N (★★): why the card values double.
- **Ledger.** none (the content is arithmetic).

### g5/02 Text, Pictures and Sound as Numbers (`text-pictures-sound-as-numbers`)

- **Hook.** Lina sends "HI" to her cousin; what travels is not two letters but sixteen 0s and 1s.
- **Sections.**
  1. *Every character has a number*: a first code table (capital letters 65 to 90, small letters 97 to
     122, digits 48 to 57, the space 32); a word as a list of numbers, then of bytes; the table is
     agreed by everyone (history box: the table's name and year, ledgered; the larger table for every
     alphabet, told, is Book 2's).
  2. *A picture is a grid of pixels*: black and white as 0 and 1 (a smiley on 8 × 8); grey levels as one
     number from 0 (black) to 255 (white); colour as three numbers, red, green and blue, each 0–255;
     mixing light on a screen (red + green looks yellow, told).
  3. *More pixels, more detail, a bigger file*: the same drawing at 8 × 8 and 32 × 32; the size of a
     picture kept as three bytes per pixel, computed for a small screen image.
  4. *Sound as a long list of numbers* (told): a microphone measures many times a second; each
     measurement is a number; played back, the numbers become sound again.
  5. *Everything in a file is bits*: text, pictures, sounds and programs are all numbers kept as bits; the
     extension tells which program reads them (recall g3/03).
- **Defines.** character code (code table); pixel; grey level; red–green–blue colour (RGB); resolution
  (of a picture, its number of pixels).
- **Recalls.** g5/01 (bit, byte, binary); g3/03 (extension); g4/01 (size in bytes).
- **Figures.** Schematics (4): (a) an excerpt of the code table (a TikZ table in two blocks) and "HI"
  turned into numbers and bits; (b) an 8 × 8 smiley as a grid of 0/1 beside its drawing; (c) the same
  shape at two resolutions; (d) three overlapping coloured circles (red, green, blue light) with the
  mixtures labelled, and a pixel's three numbers. (A sampled sound wave as dots on a curve is an optional
  fifth.) Photo: a screen seen through a magnifier, showing its red, green and blue sub-pixels (Commons,
  CC; licence read). AI: `g5-text-pictures-sound-as-numbers-drawing.jpg` (a child drawing on a tablet with
  a stylus, nothing readable).
- **Exercises (11: 8★, 3★★).** N: encode "CAT" with the table; N: decode 72 73; N: why 'A' and 'a' have
  different numbers; N: draw the 5 × 5 picture given by 0/1 rows; N: the grey level of white, of black;
  N: the three numbers of pure red; N: the size in bytes of a 10 × 10 colour picture; R: read figure (b)'s
  third row; N (★★): the colour (255, 255, 0); N (★★): a 100 × 100 colour picture against a 200 × 200 one —
  how many times bigger; N (★★): "digits are characters too": the code of '7' is not 7 — explain.
- **Ledger.** `g5:ascii:codes` (code values of A, a, 0 and the space, and the table's date, from RFC 20
  on the RFC Editor site, `RFC-EDITOR`); `g5:subpixels` none (the photograph shows it).

### g5/03 Networks and the Internet: A First Look (`networks-first-look`)

- **Hook.** Noor's grandmother, two countries away, sees Noor's drawing a second after Noor sends it.
- **Sections.**
  1. *A network*: computers linked by cables or by radio (wi-fi) to exchange data; the home network and
     the school network.
  2. *The Internet is a network of networks*: networks joined to other networks, worldwide; no one
     computer is the Internet.
  3. *The web*: a web page is a file kept on a distant computer, a server; the browser asks for it and
     shows it; the address of a page; links from page to page make the web.
  4. *Search engines* (told): a program visits pages in advance, keeps a list of which words appear
     where, and answers from that list; the order of the answers is chosen by the search engine.
  5. *A password is a key*: what a password protects; proving who you are (authentication, proposed);
     a strong password is long; counting the possibilities shows why (4 digits: 10,000; 12 letters and
     digits: computed); never share one; a different one for each place (safety box).
- **Defines.** network; Internet; server; web page; browser; web address; link (on a web page); World
  Wide Web; password; authentication (proposed).
- **Recalls.** g5/02 (everything is bits); g3/03 (file); g4/02 (application).
- **Figures.** Schematics (4): (a) a home network (laptop, tablet, phone, printer, the box that joins it
  to the Internet; wired and wireless links drawn differently); (b) the Internet as networks of networks
  (four clouds of networks joined), with one path from Noor to her grandmother; (c) browser and server:
  a generic browser window (TikZ `window`) with an address bar showing an example address, an arrow to a
  server, the page file coming back; (d) four pages and their links as a small directed drawing.
  AI: `g5-networks-first-look-family.jpg` (a family with devices at home, a small router box on a shelf),
  `g5-networks-first-look-data-centre.jpg` (a data-centre aisle with server racks). Photo (history box):
  the first web server computer at CERN, if a free photograph exists (licence read).
- **Exercises (11: 8★, 3★★).** M: three devices of a home network and how each is linked; M: is the
  Internet one computer?; M: what a browser does; M: what a server keeps; M: follow the links of figure
  (d) from page A to page D; M: strong or weak for five passwords; N: how many 3-digit codes; N: how many
  4-letter passwords of small letters (computed in the solution: 26 × 26 × 26 × 26); M (★★): why a
  different password for each place; N (★★): each added character multiplies the possibilities — by how
  much for digits, for small letters; M (★★): what the search engine has done before you search.
- **Ledger.** `g5:web:cern` (the web proposed at CERN in 1989, first site 1991, from CERN's own pages);
  `g5:arpanet:1969` if the history box dates the first network (a museum page); `g5:example-domains`
  (reserved example names, RFC 2606 / RFC 6761) so that the drawn address is a reserved example;
  `g5:passwords:guidance` (length over complexity, from a national cybersecurity agency's guidance) for the
  safety box.

## 4. Grade 6 (Python begins; ~11 pp each; 12 exercises 4★/5★★/3★★★; weekend problem 10–14 questions)

Register: one new idea at a time; every listing (3–15 lines) is followed by its captured output; a trace
table by hand whenever a value changes. No negative numbers in examples (the mathematics books reach them
in grade 7); decimals and whole division with remainder are known.

### g6/01 A First Python Program (`first-python-program`)

- **Hook.** Sami asks the computer to add up the prices of thirty items on a shopping list and gets the
  answer before he can lift his pencil.
- **Sections.**
  1. *A language precise enough for a machine*: a programming language has a few words and strict rules;
     Python is the one this book uses; the same program gives the same result on every computer.
  2. *The editor and the interpreter*: the program is a text file (`.py`) written in an editor; the
     interpreter reads it and carries out its instructions; running a file (the command printed as the
     first line of every output in this book); the interactive prompt, told.
  3. *`print` and numbers*: printing text in quotes and numbers; `+ - * /`; whole division `//` and
     remainder `%` (recall the mathematics books' division with a remainder); order of operations and
     brackets as in mathematics; `/` always gives a decimal number.
  4. *From top to bottom*: instructions run one after another, in order (recall g1/02).
  5. *Reading an error message; comments*: a misspelt `print` and a missing quote, staged; the last line
     says what went wrong, the line number says where; `#` comments are for people and are skipped.
- **Defines.** programming language; interpreter; source file (a program file); comment; error message.
- **Recalls.** g4/02 (program, a file in storage); g1/02 (sequence); g4/03 (algorithm).
- **Listings** (`code/grade-6/01-first-python-program/listings/`): `hello.py` (print a greeting);
  `prices.py` (sum of prices, `print` of a calculation); `operations.py` (the four operations, `/` gives a
  decimal); `share.py` (`23 // 5`, `23 % 5`: sweets shared between five friends); `order.py` (three prints
  run top to bottom; brackets change a result); `typo.py` (staged: `pritn` → `NameError`, with `exit`
  directive); `quote.py` (staged: missing quote → `SyntaxError`); `comments.py`. All captured.
- **Figures.** Schematics (4): (a) source file → interpreter → output (the file drawn as a generic
  window, the output as a terminal box); (b) the 23 sweets in groups of 5 with 3 left over beside
  `23 // 5` and `23 % 5`; (c) the order of execution drawn as arrows down a listing's margin; (d) an
  annotated error message (where, what kind, which line). AI: `g6-first-python-program-desk.jpg`
  (a child typing at a laptop, screen not readable).
- **Exercises (12: 4★, 5★★, 3★★★).** P: what `print(7 + 3 * 2)` prints; P: `17 // 3` and `17 % 3`; P:
  three prints in a given order; S: print a three-line poster; B: fix a missing bracket; B: fix `Print`;
  S: compute the number of whole weeks and days left in 100 days; P: `10 / 4` versus `10 // 4`;
  S: the price for 7 tickets at 4.50; C: count the lines a program prints; B (★★★): a program meant to
  share 50 cards between 6 players prints a wrong leftover — find and fix; C (★★★): explain why
  `(n // 5) * 5 + n % 5` gives back `n` for any whole number `n` tried (checked on a table of 10 values).
- **Weekend problem — The school trip (Parts I–III, 11 questions).** 137 pupils, buses of 50 seats,
  tickets for a museum in groups of 12. I: by hand, buses needed, empty seats, groups. II: a program
  computing them for any number of pupils typed (`input` is next chapter: here the number is written in
  the program and changed by the reader). III: why `(n + 49) // 50` gives the number of buses; a second
  program prints the number of buses for 1 to 200 pupils (a `for` loop is given ready-made and only
  read) and the reader counts where the answer changes. Result: **the bus count changes exactly at 51,
  101 and 151**, and the formula agrees with "divide and round up" on all 200 values.
- **Ledger.** `g6:python:origin` (Python's first public release, 1991, and its author, from the Python
  documentation's history page, `PYTHON-DOCS`); `g6:python:3.12` in a `dated{2026}` box (the version this
  book runs).

### g6/02 Variables and Input (`variables-and-input`)

- **Hook.** A game keeps Noor's score while she plays: the number on the screen changes, but its name,
  "score", stays.
- **Sections.**
  1. *A name for a value*: a variable; assignment `score = 0`; using a variable in a calculation.
  2. *Assignment is not equality*: `score = score + 10` reads right to left; the old value is replaced;
     `=` versus the mathematics books' equals sign.
  3. *Types*: whole numbers (`int`), decimal numbers (`float`), text in quotes (`str`; the word *string*
     is defined in grade 7); `type(...)`; `"3" + "4"` versus `3 + 4`.
  4. *Input and conversions*: `input` always gives text; `int(...)`, `float(...)`, `str(...)`; a
     program that asks, computes and answers; a simple f-string to print a sentence.
  5. *Following a program by hand*: a trace table, one column per variable, one row per line run.
- **Defines.** variable; assignment; value; type; type conversion; trace table (proposed ownership; see
  DEFINITIONS.md).
- **Recalls.** g6/01 (`print`, numbers, operations, error message).
- **Listings.** `score.py`; `update.py` (`score = score + 10` three times); `swap.py` (exchanging two
  values with a third variable); `types.py`; `glue.py` (`"3" + "4"`); `greet.py` + `greet.stdin`
  (name typed); `add_wrong.py` + `.stdin` (staged: two typed numbers glued as text); `add_right.py` +
  `.stdin` (with `int`); `rectangle.py` + `.stdin` (area and perimeter of a typed rectangle);
  `trace_me.py` (five lines, traced in the text). All captured.
- **Figures.** Schematics (4): (a) a variable as a labelled box holding a value, before and after an
  assignment; (b) `score = score + 10` drawn as "read the box, add, write the box"; (c) the three types
  as three kinds of box; (d) input flow: keyboard → `input` → text → `int` → number → calculation →
  `print` → screen.
- **Exercises (12: 4★, 5★★, 3★★★).** P: the value of `a` after three assignments; P: `type(4.0)`;
  P: `"5" * 3`; S: ask for a name and an age, print a sentence; B: a program adds typed numbers as text;
  S: minutes typed → hours and minutes; P: a trace table for a swap; S: the cost of a typed number of
  notebooks; B: `int("2.5")` fails — fix with `float`; C: how many assignments a given program makes;
  S (★★★): seconds typed → days, hours, minutes, seconds; C (★★★): show that swapping with two
  assignments only (`a = b` then `b = a`) loses a value, with a trace table.
- **Weekend problem — The clock of the day (Parts I–III, 11 questions).** I: by hand, 5,000 seconds and
  50,000 seconds into hours, minutes, seconds. II: a program reading a number of seconds and printing
  `h:m:s`; and the reverse program. III: why the answer always has minutes and seconds below 60 (the
  remainder by 60 is below 60), why the two programs undo each other, and how many different `h:m:s`
  times a day holds. Result: **86,400 seconds, each written in exactly one way as `h:m:s` with
  h < 24, m < 60, s < 60** (counted as 24 × 60 × 60 and checked against the conversion).
- **Ledger.** none.

### g6/03 Repeating with `for`: Turtle Drawings (`for-loops-turtle`)

- **Hook.** Leo draws a square with four copies of the same two lines; for a 36-sided shape he would need
  72 lines, unless the computer repeats them for him.
- **Sections.**
  1. *The turtle*: a pen that moves on the screen: `forward`, `left`, `right` (angles in degrees, recall
     the mathematics books' angles), `penup`, `pendown`; the drawing appears in a window (here, drawn from
     the recorded path).
  2. *The `for` loop*: `for i in range(4):` repeats the indented block four times; indentation marks the
     block; what is inside and what is after.
  3. *Regular polygons and their angles*: walking once round a closed shape, the turtle turns one full
     turn in all, so each turn of a regular polygon with n sides is 360 ÷ n degrees; the star turning
     144°.
  4. *The loop variable and `range`*: printing `i`; `range(n)`, `range(a, b)`, `range(a, b, step)`;
     using `i` in a drawing (a spiral of growing sides).
  5. *A loop inside a loop*: a row of squares; a multiplication table printed with two loops.
- **Defines.** turtle graphics; for loop; block (indented block); loop variable; nested loop.
- **Recalls.** g4/03 (repetition by hand); g6/02 (variable).
- **Listings.** Turtle files in `NORUN.txt`, recorded by `figures/record_turtle.py`: `square_long.py`,
  `square.py`, `polygon.py` (n written in the program), `star.py`, `spiral.py`, `row_of_squares.py`.
  Captured listings: `count.py` (print `i` for `range(5)`), `ranges.py` (three `range` forms),
  `times_table.py` (nested loops), `stairs.py` (printing `#` rows of growing length).
  Tests: `tests/test_drawings.py` (each recorded path: number of sides, side length, closed or not);
  `tests/test_listings.py` (captured listings).
- **Figures.** Schematics (4): (a) the turtle's state (a position and a heading arrow) before and after
  `forward 50, left 90`; (b) the turning angle of a regular hexagon with the full turn shown;
  (c) four drawings from the recorded `.dat` files (square, hexagon, star, spiral) in one panel;
  (d) the nested loop of `row_of_squares` with the outer and inner repeats bracketed. History box (Logo,
  the turtle language of the late 1960s): a photograph of a floor turtle robot if a free one exists.
- **Exercises (12: 4★, 5★★, 3★★★).** P: what `for i in range(3): print(i)` prints; P: `range(2, 10, 3)`;
  P: how many lines a nested loop prints; S: draw a triangle (turtle, recorded); B: a polygon that does not
  close (wrong angle); B: a block that is not indented, so only the last line repeats; S: print the 7
  times table; S: a regular octagon; C: the angle for a 10-sided polygon and why; S: a row of 5
  triangles; C (★★★): the turtle turns 144° five times: how many full turns, and why the star closes;
  S (★★★): the first 20 terms of the sequence 1, 4, 7, 10, … (a number pattern, the far term by loop).
- **Weekend problem — Stars of every size (Parts I–III, 12 questions).** A star with n points made by
  turning 360 × k ÷ n degrees after each of n equal sides. I: draw by hand the 5-point star (k = 2) and
  the pentagon (k = 1); what k = 3 gives. II: a program with `n` and `k` written at the top draws the
  shape (recorded); for n = 8, which k from 1 to 7 give a single star and which give two squares (k = 2)
  or a square drawn twice. III: the total turning for {n, k} is k full turns; count for n = 5 to 12 how
  many k give a single closed star through all n points (counted from the drawings; the rule "k and n
  share no divisor other than 1" is told, the mathematics books prove it later). Result: **for n = 12,
  only k = 1, 5, 7 and 11 draw all 12 points in one line**.
- **Ledger.** `g6:logo:1967` (Logo's date and the floor turtle, from the Logo Foundation's or MIT's own
  pages) for the history box.

### g6/04 Decisions: `if` and `else` (`if-else`)

- **Hook.** A cinema charges children, adults and seniors differently; the ticket machine asks one
  question and decides.
- **Sections.**
  1. *Comparisons give true or false*: `==`, `!=`, `<`, `<=`, `>`, `>=`; the two Boolean values `True`
     and `False`; `=` versus `==`.
  2. *`if` and `else`*: one block or the other; the colon and the indentation.
  3. *`elif`*: a chain of cases checked in order; the first true one wins; ticket prices by age.
  4. *`and`, `or`, `not`*: combining conditions; the four cases of `a and b` in a small table (the logic
     gates of grade 9 will reuse it); a leap year rule written with `and` and `or`.
  5. *Testing every branch*: choosing inputs that reach each block; the boundaries (exactly 12, exactly
     65); a `for` loop over ages printing each price.
- **Defines.** comparison; Boolean value; conditional statement (if statement); branch; compound
  condition (with `and`, `or`, `not`).
- **Recalls.** g4/03 (condition: yes/no question); g6/02 (variables, input); g6/03 (for loop).
- **Listings.** `compare.py`; `even_odd.py` + `.stdin`; `ticket.py` + `.stdin` (if/elif/else);
  `wrong_order.py` (staged: `elif` cases in the wrong order make one branch unreachable); `assign_vs_equal.py`
  (staged `SyntaxError` from `if x = 3:`); `leap.py` + `.stdin`; `all_prices.py` (loop over ages 0 to 80
  by fives, every branch reached); `boundaries.py` (11, 12, 64, 65).
- **Figures.** Schematics (4): (a) `if/else` as a fork with two blocks rejoining; (b) the `elif` chain as a
  ladder of questions; (c) the table of the four cases for `and` and for `or`; (d) a number line of ages
  with the price bands and the boundary values marked.
- **Exercises (12: 4★, 5★★, 3★★★).** P: `print(3 < 5)`, `print(4 == 4.0)`; P: which branch runs for
  x = 7; P: `not (a and b)` for given values; S: "positive or zero" for a typed number; B: `if x = 3`; B:
  an `elif` chain that never prints "senior"; S: the largest of three typed numbers; S: a grade letter
  from a mark out of 20; C: list inputs that reach every branch of a given program; S: a password-length
  check (at least 12 characters, using `len` as given); C (★★★): two programs, one with nested `if`s and
  one with `and`: show they agree on every pair of `True`/`False`; B (★★★): a leap-year program wrong for
  1900 — fix it and give a year that proves it fixed.
- **Weekend problem — The calendar's leap years (Parts I–III, 12 questions).** I: the rule (every fourth
  year, except centuries, except every fourth century) applied by hand to 2024, 2100, 2000, 1900.
  II: a program that decides a typed year; a loop that counts the leap years from 1901 to 2100 and from
  2001 to 2400. III: the days in 400 years and the average year. Result: **97 leap years in every 400, so
  146,097 days and an average year of 365.2425 days**.
- **Ledger.** `g6:gregorian:rule` (the leap-year rule, from an astronomical almanac office's or a
  national observatory's page).

### g6/05 Repeating with `while` (`while-loops`)

- **Hook.** Tom saves 3 coins a week for a 50-coin game; how many weeks? The number of turns is not known
  in advance, so a `for` loop does not fit.
- **Sections.**
  1. *Repeating as long as a condition holds*: `while`; the condition is checked before every turn;
     a countdown.
  2. *Counters and running totals*: a counter goes up by one, a total adds each new value; summing typed
     numbers until 0 is typed; the average of typed marks.
  3. *The loop that never ends*: a condition that never becomes false; how to stop it (`Ctrl` + `C`);
     staged: a silent infinite loop stopped by the capture's time limit (`timeout=2`, printed as
     "[killed after 2 s]"); fixing it by changing the variable in the loop.
  4. *Choosing between `for` and `while`*: known number of turns, or a condition.
  5. *A number-guessing game*: one player types a secret, the other guesses, the program answers
     "higher" or "lower" and counts the guesses (no random numbers: those are grade 9).
- **Defines.** while loop; counter; running total; infinite loop.
- **Recalls.** g6/03 (for loop); g6/04 (comparison, Boolean value); g4/03 (repeat until).
- **Listings.** `countdown.py`; `savings.py` (weeks to reach 50 coins); `sum_until_zero.py` + `.stdin`;
  `average.py` + `.stdin`; `forever.py` (staged, `# capture: timeout=2`); `fixed_forever.py`;
  `digits.py` (number of digits by repeated `// 10`); `guess.py` + `.stdin` (two-player game).
- **Figures.** Schematics (4): (a) the `while` loop as a cycle with the test before the block; (b) a
  trace table of `savings.py` drawn as a filling bar; (c) `for` versus `while` side by side for the same
  countdown; (d) the guessing game's possible numbers shrinking after each answer (1–100 drawn as a bar).
- **Exercises (12: 4★, 5★★, 3★★★).** P: what a countdown from 5 by 2 prints; P: the number of turns of a
  given loop; P: the final total; S: sum of 1 to 100 with `while`; B: a loop that never ends — fix it;
  B: a total that misses the last value; S: the first power of 2 above 1,000 by doubling (no exponent);
  S: count the digits of a typed number; C: how many turns `while n > 1: n = n // 2` takes for n = 100
  (trace); S: repeat a question until the answer is "yes"; C (★★★): show that `savings.py` always
  stops, whatever whole-number saving per week above 0 is written; S (★★★): the guessing game with a
  limit of 7 guesses.
- **Weekend problem — The 3n + 1 game (Parts I–III, 12 questions).** Start from a whole number; if it is
  even halve it, otherwise triple it and add 1; stop at 1. I: by hand from 6 and from 7, counting steps.
  II: a program counting the steps for a typed start; a loop over every start below 100 printing the
  number with the most steps. III: the highest number reached on the way, and why nobody knows whether
  every start reaches 1 (told: an open question). Result: **below 100, the start 97 takes the most
  steps, 118** (computed by the chapter's program; the printed figure is its captured output).
- **Ledger.** `g6:collatz:open` (the problem's statement and that it is unsolved, with its author's name
  and decade, from a mathematics department's or journal's page) for one history sentence.

## 5. Grade 7 (~11 pp each; 12 exercises 4★/5★★/3★★★; weekend problem except the project)

### g7/01 Functions (`functions`)

- **Hook.** Lina's program computes the area of five rooms and has the same three lines five times;
  when she finds a mistake in them, she must fix it five times.
- **Sections.**
  1. *Defining and calling a function*: `def`, the body, the call; a function runs only when called;
     calling it many times.
  2. *Parameters and arguments*: values passed in; several parameters; the order of arguments.
  3. *`return` is not `print`*: a function gives a value back to the caller; printing shows a value to
     the reader; staged: a function that prints instead of returning makes `area(3, 4) + 1` fail
     (`None`).
  4. *Local variables*: names made inside a function exist only during the call; staged `NameError`
     outside it.
  5. *Cutting a problem into functions; checking on examples*: a receipt printer built from three small
     functions; each function checked by calls whose answers are worked out by hand first, printed
     side by side ("expected 12, got 12"). (Assertions and test files are Book 2's.)
- **Defines.** function; function call; parameter; argument; return value; local variable.
- **Recalls.** g6/02 (variable, value); g6/01 (`print`); g6/04 (if, used inside functions).
- **Listings.** `greet.py` (a function with no parameter, called three times); `area.py`; `two_params.py`;
  `print_not_return.py` (staged `TypeError` on `None + 1`, `exit`); `local.py` (staged `NameError`);
  `largest.py` (largest of two and of three, the second calling the first); `receipt.py` (three functions);
  `check_examples.py`. Tests: `tests/test_functions.py` imports the functions (listings that run code at
  import are guarded by `if __name__ == "__main__":` only from this chapter on, introduced in a remark).
- **Figures.** Schematics (4): (a) a function as a machine with inputs (parameters) and an output (return
  value); (b) a call's journey: the caller pauses, the body runs, the value comes back (arrows on the
  listing); (c) local boxes that appear during the call and disappear after; (d) the receipt program's
  functions as a call diagram.
- **Exercises (12: 4★, 5★★, 3★★★).** P: what a program with two calls prints; P: `print(f(2) + f(3))`;
  P: a function that prints and returns — what appears; S: `perimeter(width, height)`; B: a function
  that prints instead of returning; B: arguments in the wrong order; S: `is_even(n)` returning a Boolean
  value; S: `minutes_to_hours(m)` returning hours and printing nothing; C: how many times the body runs in
  a program with a call inside a loop; S: `price(age)` reusing g6/04's ticket rules; C (★★★): for
  `largest3(a, b, c)` built from `largest2`, list the cases needed to check every branch; S (★★★):
  `digit_sum(n)` with a `while` loop, checked on five examples.
- **Weekend problem — The check digit of a barcode (Parts I–III, 13 questions).** A 13-digit product code
  ends with a check digit chosen so that the weighted sum (weights 1, 3, 1, 3, …) is a multiple of 10.
  I: by hand, check a printed code; compute a missing check digit. II: functions `weighted_sum(code)` and
  `check_digit(first12)` working on the code as a whole number (digits taken off with `% 10` and `// 10`,
  strings are next chapter); a function `is_valid(code)`. III: change one digit of a valid code in every
  possible way and count how many changes are caught; swap two neighbouring different digits and count.
  Result: **every single wrong digit is caught; 80 of the 90 swaps of two different neighbouring digits
  are caught, and the 10 missed swaps are exactly the digits that differ by 5**.
- **Ledger.** `g7:ean13:rule` (the weights and the modulus of the 13-digit product code, from the
  standards body's own check-digit page).

### g7/02 Lists (`lists`)

- **Hook.** The thirty-one January rainfall readings at Hilltop: thirty-one variables would be absurd.
- **Sections.**
  1. *A list holds many values in order*: `[...]`; the index from 0; `len`; the last element at index
     `len(L) - 1`; staged `IndexError`.
  2. *Walking through a list*: `for x in L`; `for i in range(len(L))` when the position matters.
  3. *Appending and removing*: `append`, `pop`, `remove`, `insert`, `L[i] = v`.
  4. *Computed by walking*: the sum, the largest value (the best-so-far method of g4/03 in Python), a
     count of the values that pass a test, the position of the largest.
  5. *A list is changed in place*: `append` changes the same list, it does not make a new one (shown by
     printing the list after each step; two names for one list are Book 2's).
- **Defines.** list; item (of a list; *element* is kept for HTML in g9/01); index; length (of a list);
  list traversal (walking through a list).
- **Recalls.** g6/03 (for loop, `range`); g4/03 (largest card); g6/05 (counter, running total).
- **Listings.** `rain.py` (the January list, written as a literal produced from the town by
  `figures/town_tables.py`, a test checking it equals `data/town/weather.csv`); `index_error.py` (staged);
  `walk.py`; `positions.py`; `shopping.py` (append, remove, pop); `total_max_count.py`;
  `position_of_max.py`; `in_place.py`.
- **Figures.** Schematics (4): (a) a list drawn as a row of cells with indices 0 … n−1 under them and
  `len` beside; (b) the walk as an arrow moving along the cells with the running total above; (c) `insert`
  and `pop` as before/after rows; (d) a bar chart of the January rainfall from the chapter's `.dat`
  (written by a figures script from the same list), with the largest bar marked.
- **Exercises (12: 4★, 5★★, 3★★★).** P: `L[0]`, `L[-1]`, `len(L)`; P: a list after three operations;
  P: what a walk prints; S: the average of a list; B: an off-by-one `range(len(L) + 1)`; B: a largest
  value that starts at 0 and fails for a list of winter temperatures all below zero (negative numbers
  are known from the mathematics books' grade 7); S: count the dry days (rain 0.0); S: a new list of the values
  above 5; C: how many comparisons the best-so-far walk makes for 31 values; S: reverse a list by walking;
  C (★★★): show the best-so-far walk always ends with the largest value (the value kept is the largest
  of those seen so far, at every step); S (★★★): the longest run of equal neighbouring values.
- **Weekend problem — Dry spells at Hilltop (Parts I–III, 12 questions).** I: from the printed January
  list, by hand: the wettest day, the number of dry days. II: a program for the longest run of dry days
  in a row and where it starts. III: the same for all twelve months (twelve lists produced by the
  chapter's script and printed as a table), the longest dry spell of the year at Hilltop. Result: **the
  length and dates of 2025's longest dry spell at Hilltop**, as the program computes them (a captured
  output; no number is typed).
- **Ledger.** none (town data).

### g7/03 Strings (`strings`)

- **Hook.** Sami wants to know which vowel is the most frequent in his favourite story.
- **Sections.**
  1. *A string is a sequence of characters*: index and `len` as for lists; a character cannot be
     replaced in place (a new string is built instead, told as a fact of Python).
  2. *Slices*: `s[a:b]`, `s[:b]`, `s[a:]`, `s[::-1]`.
  3. *Walking through text*: `for ch in s`; counting vowels; building a new string.
  4. *Useful string methods*: `upper`, `lower`, `strip`, `split`, `join`, `find`, `replace`, `count`;
     each returns a new value.
  5. *The code of a character*: `ord` and `chr`, recall g5/02's table; Python's table holds the
     characters of every alphabet (told; Book 2 explains how they are stored); counting letters and words
     in a passage.
- **Defines.** string; character; slice; string method; character code is g5/02's (recalled).
- **Recalls.** g5/02 (character code); g7/02 (index, length, traversal).
- **Listings.** `string_basics.py`; `immutable.py` (staged `TypeError` on `s[0] = "J"`); `slices.py`;
  `vowels.py`; `methods.py`; `words.py` (split and count); `codes.py` (`ord`, `chr`, uppercase by
  subtracting 32 and why `upper` is better); `palindrome.py`; `passage_stats.py` (on a short invented
  passage kept in the listing).
- **Figures.** Schematics (4): (a) a string as cells with positive and negative indices; (b) three
  slices shown as brackets on the cells; (c) `split` and `join` as cutting and gluing; (d) a bar chart of
  the letter counts of the passage from a figures script's `.dat`.
- **Exercises (12: 4★, 5★★, 3★★★).** P: `s[1:4]`, `s[::-1]`; P: `"a,b,c".split(",")`; P: `ord("C")`,
  `chr(100)`; S: count the spaces of a sentence; B: `s[len(s)]`; B: a palindrome test that ignores
  capitals wrongly; S: initials from a full name; S: replace every vowel by `*`; C: how many slices of
  length 3 a string of length 10 has; S: the longest word of a sentence; C (★★★): why `s[::-1][::-1]`
  is `s`, and why `s[:k] + s[k:]` is `s` for every `k` from 0 to `len(s)`; S (★★★): a "mirror word" test
  (the word reads the same after reversing and swapping b/d, p/q — a small dictionary-free version with
  two strings).
- **Weekend problem — Palindrome dates (Parts I–III, 12 questions).** A date written DDMMYYYY that reads
  the same backwards. I: check 02-02-2020 and 12-02-2021 by hand. II: a function that writes a date
  as an 8-character string (with leading zeros, built with slices of `"0" + str(d)`), a palindrome test,
  a loop over every day of every year 2001–2099 (days per month given as a list; leap years from g6/04).
  III: list them, find the first and the last, count them. Result: **29 palindrome dates between 2001 and
  2099** (the chapter's captured output).
- **Ledger.** none.

### g7/04 How a Processor Runs a Program (`how-a-processor-runs-a-program`)

- **Hook.** A processor understands neither Python nor words; how does `3 + 4` become 7 inside the chip?
- **Sections.**
  1. *Instructions are numbers in memory*: memory as numbered cells, each holding one byte (recall
     g3/02, g4/01, g5/01); the series' toy machine with 256 cells; the program and its data side by
     side in the same memory (told; the model is Book 2's).
  2. *Registers and the program counter*: four registers R0–R3, one byte each; the program counter holds
     the address of the next instruction.
  3. *Fetch, decode, execute, at the beat of a clock*: each step reads two bytes at the program counter,
     adds 2 to it, finds what the instruction is, does it; the clock ticks; billions of steps a second
     (`dated{2026}` box).
  4. *Tracing a program by hand*: the toy machine's `add_two.toy` and `sum.toy` (a loop with `JNZ`)
     traced by hand in a table, then the toy machine's own trace (`--trace`) compared with it; the
     instructions used: `IN`, `OUT`, `LOADI`, `ADD`, `SUB`, `JNZ`, `HALT` (the full set is Book 2's).
  5. *Machine language, and why Python needs an interpreter* (told): the processor's only language is
     its numbered instructions; the interpreter is itself a program in machine language that carries out
     a Python program; several cores run several streams of instructions at once.
- **Defines.** memory cell; memory address; machine instruction; machine language; register; program
  counter; fetch–decode–execute cycle; clock (of a processor); core.
- **Recalls.** g3/02 (processor, memory); g5/01 (byte, binary); g6/01 (interpreter); g6/05 (loops).
- **Listings.** `add_two.toy` + `.stdin`; `add_two_trace.toy` (the same program with
  `; capture: args=--trace`; see the Phase A report on one listing per output); `sum.toy` + `.stdin`;
  `sum_trace.toy`; `countdown.toy`; `encode.py` (prints the two bytes of each instruction of `add_two.toy`
  in decimal and binary with `from toymachine import assemble`; the module path is set by the capture
  tool); `multiply.toy` + `.stdin` (weekend problem). Tests: `tests/test_toy.py` runs each `.toy` with
  `Machine` and checks outputs and step counts.
- **Figures.** Schematics (4): (a) the toy machine: processor (R0–R3, PC, flags drawn but not explained),
  memory of 256 cells (first 16 drawn), the path between them; (b) `add_two.toy` in memory: addresses,
  bytes, the instruction each pair encodes; (c) the fetch–decode–execute cycle as a loop of three boxes
  with the PC update; (d) a clock signal (square wave, pgfplots) with one instruction per tick drawn
  under it (simplified: real processors take several ticks, told). Photos: ENIAC (history box *Programs
  as wiring, then programs in memory*), a processor chip on a motherboard (Commons).
- **Exercises (12: 4★, 5★★, 3★★★).** P: the registers after three given instructions; P: the PC after
  each of four steps; P: what `countdown.toy` prints; S: a toy program that reads two numbers and prints
  their sum plus 1; B: a toy program whose loop never ends (wrong jump target); B: a program that
  forgets `HALT`; S: a toy program that prints 5, 4, 3, 2, 1; P: the bytes of `LOADI R1, 7` (opcode × 4
  + register, from the table given in the chapter); C: how many steps `sum.toy` takes for n = 4 (trace);
  C: the toy memory holds 256 bytes and each instruction takes 2 — the longest program; C (★★★): the
  steps of `sum.toy` for any n, as an expression (3 per turn plus a fixed number), checked against the
  machine's step count for n = 1 to 10; S (★★★): a toy program that prints the larger of two numbers
  (with `CMP` and `JN`, both given with their meaning).
- **Weekend problem — Multiplying on a machine that cannot multiply (Parts I–III, 12 questions).**
  The toy machine has no multiplication. I: multiplying 6 × 4 by repeated addition, by hand with a trace
  table. II: `multiply.toy` reads a and b and adds a to a total b times; run it, count the steps the
  machine reports for b = 1 to 10 (a Python listing that runs `Machine` and prints the steps). III: the
  steps as an expression in b; why 7 × 200 cannot be printed (one byte holds at most 255, told; overflow
  is Book 2's); which order, 3 × 50 or 50 × 3, takes fewer steps. Result: **the step count grows by the
  same number for each extra unit of b (a fixed cost per turn), so 3 × 50 takes far more steps than
  50 × 3** (exact counts from the captured output).
- **Ledger.** `g7:eniac:programming` (ENIAC set up by wiring and switches, its dates; museum or
  university page); `g7:edvac:1945` (the 1945 report describing a program kept in memory, from an
  archival or university page) for the history box; `g7:clock:2026` and `g7:cores:2026` (a current
  processor's clock speed and core count, from a maker's datasheet) for the dated box.

### g7/05 Finding and Fixing Bugs (`finding-and-fixing-bugs`)

- **Hook.** Leo's average of five marks prints 13.2 for marks that are all between 8 and 12.
- **Sections.**
  1. *Three kinds of error*: the program does not start (syntax error), it starts and stops (runtime
     error), it finishes with a wrong answer (logic error, the hardest: nothing warns).
  2. *Reading an error report from the bottom*: the last line names the error, the lines above show the
     path of calls from the top of the program to the failing line (a traceback through two functions).
  3. *Tracing*: by hand with a trace table (recall g6/02), and with extra `print` lines that show values
     as the program runs; removing them afterwards.
  4. *The smallest input that shows the bug*: reproduce the bug first; shrink the input; a bug found
     with a list of one element.
  5. *Changing one thing at a time*: one change, run again, keep or undo; a method box. History box: the
     moth found in a relay in 1947 and taped in a log book.
- **Defines.** bug; syntax error; runtime error; logic error; traceback; debugging.
- **Recalls.** g6/01 (error message); g6/02 (trace table); g7/01 (function call); g7/02 (lists).
- **Listings.** `missing_colon.py` (syntax error); `zero_division.py` (runtime, `exit`);
  `traceback_two_calls.py` (an error inside a function called from a function); `average_bug.py` (logic
  error: divides by 4 instead of `len`); `average_trace.py` (with tracing prints); `average_fixed.py`;
  `first_word_bug.py` (fails only on a one-word sentence); `first_word_fixed.py`.
- **Figures.** Schematics (4): (a) the three kinds as a decision chart (does it start? does it stop? is
  the answer right?); (b) an annotated traceback (bottom line, the call path); (c) the debugging cycle
  (reproduce → shrink → guess → change one thing → run); (d) the off-by-one "fence" drawing (n posts,
  n − 1 gaps). Photo: the 1947 log-book page with the moth (US Navy, public domain; museum page and
  Commons licence read).
- **Exercises (12: 4★, 5★★, 3★★★).** P: which kind of error for six descriptions; P: the last line of a
  given traceback; P: what tracing prints add to an output; B: a missing bracket; B: a loop that adds one
  value too many; B: a function that returns too early (inside the loop); S: add tracing prints to a given
  function and read the trace; B: a comparison written `=<`; C: the smallest input that shows a given
  bug; B: an average that fails for an empty list — guard it; C (★★★): a program with two bugs — show
  that fixing them in either order gives the same final program, and why one-at-a-time still matters;
  B (★★★): a "largest" function wrong only when the largest is first — find the input and fix.
- **Weekend problem — The bug hunt (Parts I–III, 11 questions).** A 25-line program that grades a quiz
  has four planted bugs (one syntax, one runtime, two logic). I: predict and read the first error report;
  fix the syntax and runtime bugs. II: a checking program runs the grader on the inputs 0 to 99 and counts
  the answers that differ from the expected ones (computed in a second, simpler way); the count before and
  after each fix. III: the smallest input for each logic bug. Result: **the number of wrong answers among
  the 100 inputs falls from N₀ to N₁ to 0 as the bugs are fixed** (counts from the captured outputs).
- **Ledger.** `g7:bug:1947` (the log-book entry's date and place, from the museum that holds it).

### g7/06 Project: A Quiz Game (`project-quiz-game`)

- **Specification (one paragraph, printed first).** A quiz asks ten questions read from lists, accepts an
  answer typed in any capitals with extra spaces, gives one point per right answer and a second chance
  for half a point, shows the score at the end, and can play an easy and a hard level.
- **Milestones (one `\section` each, each with listings, outputs and tests).**
  1. *What must it do?* The specification turned into a numbered list of requirements, and a plan of
     functions (a call diagram).
  2. *Questions in lists*: two parallel lists (questions, answers); printing them all; a check that
     both have the same length.
  3. *Asking one question*: `ask(question, answer)` returns the points; normalising the typed answer
     (`strip`, `lower`); tested with scripted answers.
  4. *The whole quiz*: a loop over the questions, the score, the final message; `.stdin` runs for a
     perfect game and a poor one.
  5. *Second chances and levels*: half points, then two levels as two pairs of lists; the menu.
  6. *Improving it*: shuffling the order is left for grade 9 (randomness); a results line written to the
     screen in a fixed format.
- **Defines.** nothing: *specification* is Book 2 g10's (ownership map), so the word is used here in its
  everyday sense, in prose, without a definition pair.
- **Recalls.** g7/01 (functions), g7/02 (lists), g7/03 (string methods), g7/05 (debugging), g6/05 (loops).
- **Listings.** `quiz_v1.py` … `quiz_v5.py` (one per milestone, each a full runnable program) with
  `.stdin` files; tests `tests/test_quiz.py` call `ask`, `normalise`, `play` with scripted input
  (`monkeypatch` on `input`, explained in a comment only).
- **Figures.** Schematics (4): (a) the call diagram of the final program; (b) one turn as a flowchart
  (ask → right? → point; wrong → second chance); (c) the two parallel lists drawn as two rows with
  matching indices; (d) the milestones as a timeline with the tests that each adds.
- **Exercises (12: 4★, 5★★, 3★★★)**, about the project: P: what `normalise("  Paris ")` returns; P: the
  score printed for a given `.stdin`; S: a "skip" answer that gives 0 points; B: an index mismatch
  between the lists; S: a percentage at the end; B: the half point added even for a right first answer;
  S: a third level; C: how many lines of output a game of 10 questions prints at most; S: stop early
  when the player types "quit"; S: the longest streak of right answers; C (★★★): the highest and lowest
  possible scores and every score in between reachable in steps of 0.5 — count them; S (★★★): questions
  with several accepted answers (a list of lists).
- **Ledger.** none.

## 6. Grade 8 (~11 pp each; 12 exercises 4★/5★★/3★★★; weekend problem except the project)

### g8/01 Binary and Hexadecimal (`binary-and-hexadecimal`)

- **Hook.** A web page writes its orange as `#FF8800`; Noor wants to know why a colour is written with
  letters.
- **Sections.**
  1. *Place value in base 2*: recall the mathematics books' place value (grade 6) and powers (grade 8);
     a binary number as a sum of powers of two; the dot cards of g5/01 were the powers.
  2. *Converting both ways*: binary to decimal by adding the powers; decimal to binary by repeated
     division by 2 (the remainders read upwards); by hand, then by program, then with `bin` and
     `int(s, 2)` to check.
  3. *Adding in binary*: the column method with carries (recall the written addition of g4/03); 1 + 1 =
     10; a carry out of the leftmost column on eight bits (what the machine then does is Book 2's).
  4. *Hexadecimal*: base 16, digits 0–9 and A–F; one hexadecimal digit for four bits; converting by
     groups of four; `hex`; the `0x` prefix.
  5. *Colours in hexadecimal; n bits give 2^n values*: `#RRGGBB` as three bytes (recall g5/02);
     proposition: n bits give 2^n patterns, and the largest number on n bits is 2^n − 1 (proof by
     doubling: one more bit doubles the patterns; all ones plus one is the next power).
- **Defines.** number base; hexadecimal; hexadecimal digit; carry (in a column addition of bits).
  Proposition: *patterns of n bits* (labelled `prop:g8:binary-and-hexadecimal:patterns`).
- **Recalls.** g5/01 (bit, byte, counting in binary with cards); mathematics: place value (grade 6),
  powers (grade 8), in prose; g5/02 (RGB).
- **Listings.** `to_decimal.py` (walk the binary string, doubling); `to_binary.py` (repeated division,
  remainders collected in a list); `builtins.py` (`bin`, `int(s, 2)`, `hex`, `int(s, 16)`); `add_binary.py`
  (column addition on two strings with a carry variable); `to_hex.py` (groups of four);
  `colours.py` (split `#FF8800` into three numbers); `count_patterns.py` (all 3-bit patterns listed by
  nested loops, then the counts for 1 to 10 bits by doubling).
- **Figures.** Schematics (4): (a) a place-value table in base 10 and in base 2 side by side; (b) the
  repeated-division ladder for 44; (c) a column addition of two bytes with the carries above;
  (d) a byte split into two groups of four, each mapped to a hexadecimal digit, plus three colour swatches
  whose fills are defined from the same codes the text prints (checked: the TikZ colour values equal the
  listing's numbers).
- **Exercises (12: 4★, 5★★, 3★★★).** P: `bin(10)`, `int("1101", 2)`; P: `hex(255)`; P: what
  `to_binary.py` prints for 13; S: decimal to binary by repeated division, as a function; B: a
  conversion that reads the remainders downwards; B: `int("102", 2)` raises an error — why, and a check
  before converting; S: add two binary strings (no `int`); S: a hexadecimal colour to three numbers;
  C: how many patterns on 12 bits; C: the largest number on 16 bits, in decimal and in hexadecimal; C
  (★★★): prove that every whole number from 0 to 2^n − 1 has exactly one n-bit writing (count the
  patterns and the numbers); S (★★★): convert between any two bases from 2 to 16.
- **Weekend problem — The chessboard and the grains of rice (Parts I–III, 12 questions).** The story: one
  grain on the first square, two on the second, double each time. I: grains on squares 1 to 8 and their
  total, by hand; the total is one less than the next square's count. II: a program for all 64 squares;
  the total written in binary (64 ones) and in hexadecimal. III: how many bytes the total needs; how many
  bits a computer needs to count every grain. Result: **18,446,744,073,709,551,615 grains = 2^64 − 1,
  written as sixteen F's in hexadecimal, exactly what 8 bytes can hold** (from the captured output).
- **Ledger.** `g8:css:hex-colour` (the `#RRGGBB` notation, from the W3C CSS Color specification,
  `W3C-CSS`).

### g8/02 Dictionaries (`dictionaries`)

- **Hook.** Lina's phone finds "Grandma" among two hundred contacts at once: it looks up the name, it
  does not walk a list.
- **Sections.**
  1. *Looking a value up by its key*: `{key: value}`; `d[key]`; staged `KeyError`; `key in d`;
     `d.get(key, default)`.
  2. *Creating, changing, walking through*: adding and changing entries, `del`; `for key in d`,
     `d.items()`; keys are unique.
  3. *Counting with a dictionary*: letter counts of a passage, word counts; the counting pattern
     `counts[w] = counts.get(w, 0) + 1`.
  4. *A record as a dictionary, a table as a list of records*: a book as `{"title": …, "author": …,
     "year": …}`; three records in a list; walking the list and reading fields.
- **Defines.** dictionary; key (of a dictionary; see DEFINITIONS.md for the three senses of *key* in this
  book); entry; record; field. (*value* is g6/02's, used in the same sense.)
- **Recalls.** g7/02 (lists, traversal); g7/03 (`split`, strings).
- **Listings.** `contacts.py`; `key_error.py` (staged); `get_default.py`; `change_walk.py`;
  `count_letters.py`; `count_words.py`; `books.py` (three records in a list, fields printed).
- **Figures.** Schematics (4): (a) a dictionary drawn as two columns, keys and values, with lookup
  arrows; (b) a list walked versus a dictionary looked up (the list's scanning arrow against the
  dictionary's single arrow, told: why it is fast is Year 1's); (c) the counting pattern after each of
  six words; (d) a list of three records drawn as a small table whose header row is the field names.
- **Exercises (12: 4★, 5★★, 3★★★).** P: `d["b"]` for a given `d`; P: `len(d)` after adding a key twice;
  P: what a walk over `items()` prints; S: a capital-city lookup with a "not known" answer; B: a
  `KeyError` on a missing word — fix with `get`; B: counting that resets the count each time; S: the
  most frequent word of a sentence; S: invert a dictionary of unique values; C: how many entries a
  word-count dictionary has for a given sentence (by hand); S: the oldest book in a list of records;
  C (★★★): two ways to count votes — show how many times each looks at the ballots (see the weekend
  problem); S (★★★): group words by their first letter (a dictionary of lists).
- **Weekend problem — Counting the votes (Parts I–III, 12 questions).** A class of 40 votes for one of 6
  candidates; the ballots are a list of names. I: by hand, a tally of 12 ballots. II: two programs: one
  walks the whole list once per candidate and counts; the other walks it once with a dictionary; both
  print the winner and the margin; each also counts how many ballots it looked at. III: the counts for 40
  ballots and 6 candidates, for 400 ballots and 20 candidates; the rule behind them. Result: **the
  list-per-candidate method looks at candidates × ballots names (240, then 8,000), the dictionary at
  ballots only (40, then 400)**, as the programs count.
- **Ledger.** `g8:python:dict-order` (dictionaries keep insertion order, from the Python documentation,
  `PYTHON-DOCS`), only if the text relies on the printed order.

### g8/03 Files and Data Tables (`files-and-data-tables`)

- **Hook.** The town library of Brenmoor lends 400 books a year; its loans are a text file of 401 lines.
- **Sections.**
  1. *Text files*: writing and reading a file line by line with `open(…, encoding="utf-8")` and `with`;
     the end-of-line character; a file kept in storage after the program ends (recall g3/03, g4/01).
  2. *A table saved as text*: one record per line, fields separated by commas, a header line; the CSV
     format; `split(",")` and its limit (a comma inside a title), then the `csv` module.
  3. *Loading a table as a list of records*: `csv.DictReader` gives one dictionary per line (recall
     g8/02); every value is text: converting the numbers.
  4. *Questions about a table*: selecting rows (loans still out: an empty return date), counting,
     the largest (the longest book), averaging (the mean of a column, recall the mathematics books'
     grade 7 mean); a report written to a file. A remark: some weather readings are missing or say
     −99.0; this chapter skips empty values and names the problem (cleaning data is Book 2's).
  5. **(proposed)** *The same table in a spreadsheet*: the CSV file opened in a spreadsheet program
     (drawn generically, no product); a cell, a formula adding a column, sorting by a column, a filter;
     a program does the same steps the same way every time and on a thousand files, a spreadsheet keeps
     them visible.
- **Defines.** text file; end of line (newline character); CSV file; data table (table of records);
  header row; (proposed) spreadsheet; formula (of a spreadsheet).
- **Recalls.** g8/02 (record, field, dictionary); g3/03 (file, extension, path); g7/03 (`split`, `strip`).
- **Data.** `listings/books.csv`, `loans.csv`, `weather.csv`: copies of `data/town/*.csv` made by
  `figures/town_tables.py`, checked byte for byte by `tests/test_town_copy.py` (pending the sync: see the
  report).
- **Listings.** `write_notes.py` (writes `notes.txt`, then reads it back; see the report on files written
  by listings); `read_lines.py`; `split_line.py` (and the staged wrong split of a title with a comma);
  `load_books.py` (`DictReader`); `still_out.py` (loans not returned); `longest_book.py`; `mean_temp.py`
  (Hilltop, skipping empty values); `report.py` (writes and prints a short report).
- **Figures.** Schematics (4): (a) a CSV file's text beside the table it means (header, rows, fields);
  (b) `DictReader` turning one line into one dictionary; (c) the selection of rows as a funnel (all loans
  → still out); (d) (proposed) a generic spreadsheet grid with column letters, row numbers, a formula cell
  and a sorted column. A chart (pgfplots, from the chapter's `.dat`): Hilltop's monthly mean temperature.
- **Exercises (12: 4★, 5★★, 3★★★).** P: what `read_lines.py` prints for a three-line file; P:
  `"a,b,,c".split(",")`; P: the type of a value read by `DictReader`; S: count the books of each genre;
  B: a sum of a column that adds text (forgotten `int`); B: a file opened without `encoding` and an
  accented letter (Lighthouse Café) — fix; S: the member with the most loans; S: the number of late
  returns (due date before return date, compared as text in the YYYY-MM-DD form, and why that works);
  C: how many lines a table of 400 records has as a file, and why; S: write the books of one genre to a
  new CSV file; C (★★★): why comparing dates as text works for YYYY-MM-DD and fails for DD-MM-YYYY (a
  counterexample and a reason); S (★★★): the rainiest week of the year at Riverside.
- **Weekend problem — A year of weather at Hilltop (Parts I–III, 13 questions).** I: read the first lines
  of `weather.csv` by hand; how many lines for two stations over a year. II: load the table, keep
  Hilltop, the total rain per month (a dictionary from month to total), the wettest month; the days above
  25 °C. III: the missing readings and the −99.0 values: how many, and how much the mean temperature
  changes if they are left in. Result: **the wettest month at Hilltop in 2025 and the shift of the year's
  mean temperature caused by the two error codes** (computed values; the planted defects are known from
  `TOWN.md`).
- **Ledger.** `g8:csv:rfc4180` (the CSV format, RFC 4180, `RFC-EDITOR`); `g8:python:open-encoding`
  (default encoding of `open`, `PYTHON-DOCS`) if the remark is printed.

### g8/04 Searching and Sorting (`searching-and-sorting`)

- **Hook.** Finding a word in a paper dictionary: nobody starts at the first page.
- **Sections.**
  1. *Searching item by item*: linear search returns the position or −1; counting the comparisons; the
     worst case looks at every item.
  2. *Searching a sorted list by halving*: the guessing game of g6/05 as a strategy; binary search with
     low and high; 1–100 in at most 7 guesses, because seven doublings pass 100 (2^7 = 128, from g8/01);
     the list must be sorted.
  3. *Selection sort*: find the smallest, swap it to the front, repeat on the rest.
  4. *Insertion sort*: take each item and slide it back to its place among the ones already sorted.
  5. *Counting comparisons to compare two methods*: both sorts instrumented with a counter; counts for
     lists of 10, 100 and 1,000 items, sorted, reversed and mixed (a fixed shuffle written in the
     listing, no random numbers); selection sort always makes n(n − 1)/2 comparisons, insertion sort
     between n − 1 and n(n − 1)/2 (observed and explained by counting; the proofs and the word *cost*
     are Book 2's). `sorted` and `list.sort` told as the tools to use in practice.
- **Defines.** linear search; binary search; sorted list (in increasing order); selection sort;
  insertion sort.
- **Recalls.** g7/02 (lists, index); g6/05 (guessing game); g8/01 (powers of two); g7/01 (functions).
- **Listings.** `linear_search.py`; `binary_search.py`; `binary_search_trace.py` (prints low, middle,
  high at each step); `unsorted_binary.py` (staged: binary search on an unsorted list gives a wrong
  answer); `selection_sort.py`; `insertion_sort.py`; `count_comparisons.py` (the table of counts).
  `figures/comparisons.py` writes the chart's `.dat` from the same functions.
- **Figures.** Schematics (4): (a) linear search as an arrow scanning cells; (b) binary search as nested
  brackets halving a sorted row of 16 cells, the target found in four steps; (c) selection sort's passes
  on 6 cards; (d) insertion sort's passes on the same 6 cards. Chart: comparisons against n for the two
  sorts on reversed and sorted lists (pgfplots from `.dat`).
- **Exercises (12: 4★, 5★★, 3★★★).** P: the steps of binary search for 37 in a printed list; P: the list
  after two passes of selection sort; P: after two passes of insertion sort; S: linear search returning
  all positions of a value; B: binary search with `high = mid` that loops forever on a two-item list —
  fix; B: insertion sort that skips the first item; S: the maximum number of guesses for 1–1,000
  (count by program); S: sort a list of words by length (own selection sort); C: the comparisons of
  selection sort on 5 items, counted by hand; C: why binary search needs a sorted list (a counterexample);
  C (★★★): show that insertion sort makes exactly n − 1 comparisons on a sorted list and n(n − 1)/2 on a
  reversed one (count per pass, then add); S (★★★): sort the town's books by year, then by title for the
  same year, with your own insertion sort.
- **Weekend problem — Finding one word among a million (Parts I–III, 12 questions).** I: by hand,
  halving 1–16 and 1–1,000. II: a program counting the guesses binary search needs in the worst case for
  10, 100, …, 1,000,000 items; the counts grow by about 3 or 4 each time the size is multiplied by 10.
  III: sorting first: comparisons of selection and insertion sort on 1,000 items, against 1,000 linear
  searches. Result: **binary search finds any of 1,000,000 sorted words in at most 20 comparisons,
  because 2^20 = 1,048,576 ≥ 1,000,000** (the doubling of g8/01; the counts are the captured output).
- **Ledger.** none.

### g8/05 How the Internet Works (`how-the-internet-works`)

- **Hook.** Sami's photo of a fox reaches his cousin abroad in less than a second, cut into two thousand
  pieces that do not all travel the same way.
- **Sections.**
  1. *Messages cut into packets*: a packet carries a piece of the data and a header (where from, where
     to, which piece); packets travel separately and are put back in order (a program cuts a message,
     mixes the packets in a fixed order, and rebuilds it).
  2. *An address for every machine*: the IP address as four bytes written in decimal (recall g8/01),
     2^32 possible addresses, the newer 128-bit addresses (told); the local network: devices, network
     interfaces, cables and wi-fi, a switch that joins the devices of one network.
  3. *Routers*: a router joins networks and passes each packet one step closer, choosing from a table of
     directions it keeps (told; routing tables are Book 2's); the path of a packet as a list of routers.
  4. *Names turned into addresses*: a domain name; the name system that answers "which address is this
     name?"; a toy name table as a dictionary.
  5. *Client and server; from typing an address to seeing the page*: the client asks, the server answers;
     the sequence name → address → request → packets → page → display, told as a timeline (the request's
     format is Book 2's).
  6. *Speed and delay*: bit rate (bits per second) and latency; light in a glass fibre travels at about
     two thirds of its speed in vacuum (told, recall from the physics books later); computing the
     propagation delay over 20,000 km and the sending time of a photo; a `dated{2026}` box with typical
     home bit rates; (proposed) a `dated{2026}` box on the electricity data centres use.
- **Defines.** packet; packet header; IP address; network interface;
  network switch; router; domain name; name system (DNS); client; bit rate; latency. (*server*,
  *network*, *Internet* are g5/03's.)
- **Recalls.** g5/03 (network, Internet, server, browser, web address); g8/01 (bytes, binary, powers of
  two); g8/02 (dictionary).
- **Listings.** `packets.py` (cut, number, mix in a fixed order, rebuild); `lost_packet.py` (staged: one
  packet missing, the rebuilt message has a hole); `ip_bytes.py` (an address to four bytes and 32 bits);
  `count_addresses.py`; `names.py` (a toy name table); `path.py` (a toy network of six routers as a
  dictionary of next steps, the path of one packet; the word *routing table* is not used); `delay.py`
  (propagation and sending times). No listing touches a real network.
- **Figures.** Schematics (4): (a) a photo cut into numbered packets, each with a small header, arriving
  out of order and rebuilt; (b) two local networks with switches and devices, joined through routers to
  the rest of the Internet; (c) an IP address as four bytes (`bytefield`, 32 bits); (d) the timeline from
  typing a name to seeing the page (name system, server, packets). Photo: a network switch with its cables
  or a bundle of optical fibres (Commons); AI: `g8-how-the-internet-works-data-centre.jpg` (a technician
  in a data-centre aisle).
- **Exercises (12: 4★, 5★★, 3★★★).** P: what `ip_bytes.py` prints for a given address; P: the rebuilt
  message from four mixed packets; P: the path `path.py` prints from router A to F; S: cut a text into
  packets of 10 characters with numbers; B: a rebuild that sorts packets as text ("10" before "2") —
  fix; B: a dotted address with a part above 255 accepted — add the check; S: a function that tells
  whether two addresses share their first three bytes (told: same local network in many homes); S: the
  sending time of a file for a given bit rate; C: how many addresses with four bytes; C: the propagation
  delay over 6,000 km of fibre; C (★★★): a file of 3 megabytes in packets of 1,500 bytes with 40 bytes of
  header — how many packets and how many bytes in all; S (★★★): reassemble packets that may arrive twice
  (keep one copy of each number).
- **Weekend problem — A photo to the other side of the world (Parts I–III, 12 questions).** I: a
  3-megabyte photo, packets of 1,500 bytes of which 40 are header: the number of packets, the extra bytes.
  II: a program for the propagation delay over 20,000 km of fibre and the sending time at 10 and at
  100 megabits per second. III: which part dominates, and what a ten-times faster connection changes.
  Result: **about 2,055 packets; 0.1 s of propagation whatever the connection, against 2.5 s or 0.25 s of
  sending: past a certain speed, only distance matters** (exact values from the captured output).
- **Ledger.** `g8:ipv4:32bits` (RFC 791), `g8:ipv6:128bits` (RFC 8200), `g8:dns` (RFC 1034/1035),
  `g8:packet:1500` (the common 1,500-byte payload limit, RFC 894 or the IEEE standard's public summary),
  `g8:headers:40` (20-byte IPv4 and 20-byte TCP minimum headers, RFC 791 and RFC 9293),
  `g8:fibre:index` (group index of a standard single-mode fibre, from a maker's datasheet),
  `g8:arpanet:1969` (museum page) for a history box, `g8:broadband:2026` (a telecoms regulator's report)
  and, if kept, `g8:datacentres:energy` (an energy agency's report) for the dated boxes.

### g8/06 Project: A Data Explorer (`project-data-explorer`)

- **Specification (one paragraph).** A program that loads the town library's books and loans, offers a
  menu (count loans by genre, the ten most borrowed books, the books never borrowed, the loans still out
  on a date typed by the user), answers each question, and saves the last answer as a report file.
- **Milestones.**
  1. *The menu and its loop*: the choices, a `while` loop, a quit choice; tested with `.stdin`.
  2. *Loading the two tables*: `load_books`, `load_loans`; checks on the counts (80 and 400, read from the
     data and asserted, not typed).
  3. *Filtering and counting*: loans per genre (a dictionary), books never borrowed.
  4. *Sorting and the top ten*: `sorted(..., key=a_function)` with a named function as the key (no
     `lambda`); ties broken by title; the top ten printed as a table.
  5. *Dates and the report*: loans still out on a typed date (text comparison of g8/03); writing the last
     answer to `report.txt`.
- **Defines.** nothing new (a project chapter: every word is recalled).
- **Recalls.** g8/02, g8/03, g8/04, g7/01, g7/06 (milestones and tests).
- **Listings.** `explorer_v1.py` … `explorer_v5.py`, each runnable with a `.stdin`; tests
  `tests/test_explorer.py` (each function on the copied town tables).
- **Figures.** Schematics (4): (a) the data flow: CSV files → lists of records → dictionaries → answers →
  report; (b) the menu loop; (c) the join of a loan to its book by `book_id` drawn as matched rows (the
  word *join* is Book 2's: here "looking up the book of each loan"); (d) a bar chart of loans per genre
  (from the program's own `.dat`).
- **Exercises (12: 4★, 5★★, 3★★★)**, about the project: P: the output of a given menu session; P: the
  top three for a three-book toy table; S: add "books by an author"; B: the top ten that counts a book
  twice; S: the busiest month; B: a date typed as 3/5/2025 — reject it with a message; S: members who
  never borrowed; C: how many dictionary lookups the genre count makes; S: save the report as CSV; S:
  the average loan length in days (dates converted with `datetime`, introduced in a remark); C (★★★): show
  that the top-ten list is the same whatever the order of the loans file; S (★★★): the pair of books most
  often borrowed by the same member.
- **Ledger.** none.

## 7. Grade 9 (~11 pp each; 12 exercises 4★/5★★/3★★★; weekend problem except the project)

### g9/01 Web Pages: HTML and CSS (`html-and-css`)

- **Hook.** Lina saves a web page and opens the file in a text editor: no picture of the page, only
  words between angle brackets.
- **Sections.**
  1. *A web page is a text file*: an `.html` file opened by the browser (recall g5/03); the same file seen
     as text and as a page.
  2. *Elements and tags*: start tag, content, end tag; attributes; headings, paragraphs, lists, links
     (`a` with `href`), images (`img` with `src` and `alt`), tables; the skeleton `html`, `head`, `body`.
  3. *The page as a tree*: elements inside elements; the document tree drawn from the file; a Python
     program (`html.parser`, standard library) prints the tree with indentation.
  4. *Content apart from appearance*: CSS rules (selector, property, value) in a separate file; selecting
     by element, by class; colours (recall g8/01's hexadecimal), sizes, fonts.
  5. *Boxes*: every element is a box with content, padding, border and margin; the same page with two
     style sheets.
- **Defines.** HTML; element; tag (start tag, end tag); attribute; document tree; CSS; CSS rule; selector;
  class (of an HTML element; qualified, Book 2 owns *class* in programming); box model.
- **Recalls.** g5/03 (web page, browser, link, web address); g8/01 (hexadecimal colours); g3/03 (file,
  extension).
- **Listings.** `first_page.html`, `lists_links.html`, `table.html`, `style.css`, `styled_page.html`,
  `two_styles.css` (all in `NORUN.txt`: shown, not run); `show_tree.py` (prints the element tree of
  `first_page.html`); `count_tags.py` (counts each element); `unclosed.py` (staged: a page with a missing
  end tag, the tree printed shows where it goes wrong). No server is run (the request and the response are
  Book 2's).
- **Figures.** Schematics (4): (a) `first_page.html` drawn as a page in a generic browser window, by hand
  from the HTML and checked against it (no screenshot); (b) its document tree (`forest`), matching the
  captured `show_tree` output; (c) the box model (content, padding, border, margin) with sizes from
  `style.css`; (d) the same page with the two style sheets, side by side. History box: the first web page
  and its server (CERN; ledger), photograph if free.
- **Exercises (12: 4★, 5★★, 3★★★).** P: the tree printed for a short given page; P: which elements a
  selector matches; P: the total width of a box from its CSS; S: a page with a heading, a list and a link;
  B: a page with tags closed in the wrong order — fix and redraw the tree; B: an image with no `alt`
  text — why it matters, fix; S: a two-column table of the town's places; S: a style sheet that colours
  every second-level heading; C: count the elements and the depth of a given page's tree; S: a program
  that lists every link (`href`) of a page; C (★★★): show that in a well-formed page the start and end
  tags pair up like brackets (every end tag closes the most recent open one), with a counterexample when
  they do not; S (★★★): turn a CSV table of g8/03 into an HTML table by program.
- **Weekend problem — The tree of a page (Parts I–III, 11 questions).** I: draw the tree of a given
  20-line page by hand; its depth and number of elements. II: a program computing the depth and the count
  for any page; on three pages. III: a page with a list of n items: how the count and depth grow with n,
  checked for n = 1 to 10. Result: **a list page with n items has n + k elements (k fixed by the
  skeleton) and a depth that does not change with n** (exact k from the captured output).
- **Ledger.** `g9:html:elements` (element names, from the WHATWG HTML standard), `g9:css:box` (the box
  model, from the W3C CSS specification), `g9:web:first-page` (CERN's page on the first website).

### g9/02 Logic Gates and Boolean Algebra (`logic-gates`)

- **Hook.** A lift moves only if the door is closed AND a floor button is pressed; a hall light comes on if
  this switch OR that one is on.
- **Sections.**
  1. *True and false as 1 and 0*: recall g6/04's Boolean values; a bit as a Boolean value; Python's
     `True + True`.
  2. *Gates and their truth tables*: NOT, AND, OR, XOR; a gate's truth table lists every input; drawn
     symbols; Python functions that print the tables.
  3. *Circuits of gates*: wiring outputs to inputs; the truth table of a circuit from all 2^n inputs
     (recall g8/01); two circuits that compute the same thing.
  4. *Rules of Boolean algebra*: NOT NOT a = a, a AND 1 = a, a OR 1 = 1, and the others; De Morgan's laws
     for gates (proposition, proved by the four rows of the truth table).
  5. *The half adder; the transistor as a switch*: adding two bits gives a sum bit (XOR) and a carry bit
     (AND), recall g8/01's carries; a transistor is a switch worked by electricity (told: the physics
     books' circuits and switches recalled in prose), two switches in series act as AND, in parallel as
     OR.
- **Defines.** logic gate; truth table (of a gate or a circuit); NOT gate, AND gate, OR gate, XOR gate
  (one definition); logic circuit; half adder. Proposition: De Morgan's laws for gates (indexed in the
  proposition, this chapter only).
- **Recalls.** g6/04 (Boolean value, `and`, `or`, `not`, the four-case table); g8/01 (binary addition,
  carry, 2^n patterns); physics books (electric circuit, switch), in prose.
- **Listings.** `gates.py` (four functions, their truth tables printed); `circuit.py` (a three-input
  circuit's truth table by nested loops); `same_circuit.py` (two circuits compared on every input);
  `de_morgan.py`; `half_adder.py`; `nand_only.py` (NOT, AND and OR made from NAND alone).
- **Figures.** Schematics (4): (a) the four gate symbols with their truth tables (circuitikz ports);
  (b) a three-input circuit and its table (the table must match `circuit.py`'s output); (c) the half
  adder (an XOR and an AND sharing their inputs); (d) switches in series and in parallel with a lamp
  (circuitikz), next to the AND and OR they behave like. Photo: an early transistor (a museum's replica
  of the first point-contact transistor, Commons, licence read) or a chip under a magnifier.
- **Exercises (12: 4★, 5★★, 3★★★).** P: the output of a two-gate circuit for given inputs; P: XOR's
  table; P: what `nand_only.py` prints; S: a function for "exactly one of three"; B: a truth table that
  misses a row (two loops over `range(1)`); B: a circuit drawn with an OR where the table needs XOR; S: the
  truth table of `(a AND b) OR (NOT c)`; S: test whether two functions agree on every input; C: how many
  rows for 5 inputs; C: prove `a OR (a AND b) = a` with a table; C (★★★): show that any truth table of
  two inputs can be built from NAND gates only (there are 16; build NOT, AND, OR, then argue);
  S (★★★): a two-bit adder from two half adders and an OR, checked on all 16 inputs (the full adder's
  name is Book 2's; the circuit is not called that here).
- **Weekend problem — Three judges and a buzzer (Parts I–III, 12 questions).** A buzzer sounds when at
  least two of three judges press. I: the truth table (8 rows) by hand; which rows sound. II: a circuit of
  AND and OR gates for it, its table by program, compared with the specification on all 8 inputs; a
  second circuit from a different idea, shown equivalent. III: the number of two-input gates each circuit
  uses; for five judges and "at least three", the number of rows. Result: **"at least two of three" is
  (a AND b) OR (b AND c) OR (a AND c): five two-input gates, and the program checks it on all 8 inputs;
  five judges need a table of 32 rows**.
- **Ledger.** `g9:boole:1854` (the book's year, from a library's catalogue page); `g9:shannon:1938`
  (the switching-circuits thesis, from the university repository's record); `g9:transistor:1947` (the
  first transistor, from the Nobel Prize's own page); a `dated{2026}` box on transistors per chip only if
  sourced from a maker's page.

### g9/03 Grids and Images (`grids-and-images`)

- **Hook.** Noor zooms into a photo until it becomes squares; each square is a number in a table.
- **Sections.**
  1. *A list of lists as a grid*: `grid[r][c]`; rows and columns; building a grid with loops (and the
     staged trap of `[[0] * 3] * 3`, explained only as "the same row three times", the reason being
     Book 2's).
  2. *Neighbours*: the four and the eight neighbours of a cell; the edge cells; counting neighbours that
     satisfy a test.
  3. *A grey-level image as a grid*: recall g5/02's pixels and grey levels; a colour image as three grids.
  4. *A plain-text image file*: the PGM text format (a header, then the numbers), read and written by
     program; small images (24 × 16) so that outputs stay printable.
  5. *Changing an image*: negative (255 − v), mirror (reverse each row), threshold, blur by averaging a
     cell with its neighbours; each transformation prints the new file's text, from which the figures are
     drawn (no file is written by the listings: see the Phase A report).
- **Defines.** grid (list of lists, with its rows and columns described, not defined: *row* would collide
  with the keyboard's home row); cell (of a grid; qualified, see DEFINITIONS.md); neighbour (of a cell);
  plain image file (the PGM text format); blur and threshold are named in method boxes, not defined.
- **Recalls.** g7/02 (lists, index); g5/02 (pixel, grey level, RGB, resolution); g8/03 (text files).
- **Listings.** `grid_basics.py`; `print_grid.py`; `shared_rows.py` (staged trap); `neighbours.py`;
  `make_image.py` (prints a 24 × 16 PGM of a simple shape); `read_pgm.py` (reads `shape.pgm`, a data
  file in `listings/` written by `figures/make_shape.py` and tested); `negative.py`, `mirror.py`,
  `threshold.py`, `blur.py` (each reads `shape.pgm` and prints the new PGM text). `figures/draw_images.py`
  turns the captured outputs into `.dat` grids for pgfplots `matrix plot`.
- **Figures.** Schematics (4): (a) a grid with row and column indices and `grid[1][2]` marked; (b) the
  4- and 8-neighbourhoods, and an edge cell's shorter list; (c) the 3 × 3 averaging window over a cell;
  (d) a panel of five images: original, negative, mirror, threshold, blur (drawn from the captured
  outputs).
- **Exercises (12: 4★, 5★★, 3★★★).** P: `grid[2][0]` of a printed grid; P: the neighbours listed for a
  corner; P: the output of `negative.py` on a 2 × 2 image; S: the transpose of a grid; B: a neighbour
  function that reads outside the grid — fix; B: a mirror that reverses the rows' order instead of each
  row; S: a brightness change clipped to 0–255; S: rotate an image a quarter turn (rotating by quarters
  by recursion is Book 2's: here a direct double loop); C: the number of 4-neighbours summed over a 5 × 4
  grid; S: count the white cells of a threshold image; C (★★★): the size in bytes of a PGM text file of
  w × h pixels at most (count characters), against three bytes per pixel; S (★★★): one generation of a
  cellular automaton on a grid (a cell lives if it has 2 or 3 living neighbours — rules given), checked on
  a blinker.
- **Weekend problem — The blur that spreads (Parts I–III, 12 questions).** One white pixel in a black
  image, blurred again and again with the 3 × 3 average. I: by hand, the first blur on a 7 × 7 image.
  II: a program blurring k times with decimal values and counting the cells that are not 0; the counts for
  k = 1 to 5. III: the same with whole grey levels (as a PGM must store them): the spreading stops when the
  values round to 0. Result: **with decimal values, after k blurs exactly (2k + 1) × (2k + 1) cells are
  lit (away from the edges); with whole grey levels the light dies out after a few blurs** (the exact
  number from the captured output).
- **Ledger.** `g9:pgm:format` (the plain PGM format, from the Netpbm project's documentation page).

### g9/04 Algorithms on Numbers (`algorithms-on-numbers`)

- **Hook.** Is 1,000,003 a prime number? Trying every divisor by hand would take a week; a program
  answers in a moment, and a better program in a thousandth of that.
- **Sections.**
  1. *Divisors and primality by trial division*: recall the mathematics books' divisors and prime
     numbers (grade 9); listing divisors with `%`; a primality test that tries every number below n;
     counting the divisions.
  2. *Stopping at the square root*: proposition: if n is not prime it has a divisor d with d × d ≤ n
     (proof: a pair of divisors cannot both exceed √n); the test with `d * d <= n`; the count of divisions
     falls from about n to about √n (counted for n = 1,000,003).
  3. *The sieve for all primes below n*: a list of Booleans, crossing out multiples (method, Eratosthenes
     named in a history box); the 1–100 grid drawn from the program's output.
  4. *Euclid's algorithm programmed*: recall the mathematics books' Euclid's algorithm; by subtraction and
     by division; counting the steps.
  5. *Why Euclid is fast*: proposition: after two steps the remainder is less than half (proof by two
     cases); so the steps grow very slowly with the numbers.
  6. **(proposed)** *A square root by halving*: √2 between 1 and 2, halve the interval, keep the half
     whose ends' squares straddle 2; ten halvings, three decimals (the halving of g8/04 on numbers).
- **Defines.** trial division (method); primality test; sieve of Eratosthenes (method, indexed in the
  method box); (proposed) interval halving for a square root (method). Euclid's algorithm is the
  mathematics books' (recalled, not indexed).
- **Recalls.** mathematics (divisor, prime number, gcd, Euclid's algorithm, square root), in prose; g8/04
  (halving); g7/01 (functions); g6/05 (while loops).
- **Listings.** `divisors.py`; `is_prime_slow.py`; `is_prime.py`; `count_divisions.py`; `sieve.py`;
  `sieve_grid.py` (prints the 10 × 10 grid the figure draws); `gcd_subtract.py`; `gcd.py`;
  `gcd_steps.py`; `sqrt_halving.py`; `primes_timing.py` (in `MEASURED.txt`: trial division against the
  sieve for all primes below 100,000, caption "on the author's laptop").
- **Figures.** Schematics (4): (a) divisor pairs of 36 as rectangles, the square 6 × 6 in the middle;
  (b) the sieve grid 1–100 with primes highlighted (from `sieve_grid.py`'s output); (c) Euclid on
  (21, 13) drawn as squares cut from a rectangle; (d) chart: Euclid's steps for consecutive pairs, from
  the program's `.dat`.
- **Exercises (12: 4★, 5★★, 3★★★).** P: the divisors printed for 28; P: the sieve after crossing out 2
  and 3 on 1–30; P: the steps of `gcd(48, 18)`; S: perfect numbers below 10,000; B: `is_prime(1)` says
  true — fix; B: `d * d < n` misses squares of primes (49) — fix; S: the gcd of three numbers; S: twin
  primes below 1,000; C: why the sieve may start crossing out at p × p; C: the number of divisions the
  fast test makes for 10,007; C (★★★): prove that after two steps of Euclid's algorithm the remainder is
  less than half of the starting larger number; S (★★★): the smallest prime above a typed number, and a
  count of the divisions used.
- **Weekend problem — The slowest pairs for Euclid (Parts I–III, 12 questions).** I: steps of Euclid for
  (13, 8), (21, 13), (100, 1) by hand. II: a program finding, among all pairs below 1,000, the pair that
  takes the most steps; the pairs that hold the record as the bound grows (each a pair of neighbouring
  numbers of 1, 1, 2, 3, 5, 8, …). III: why neighbouring numbers of that sequence are slow (each step
  goes back exactly one place). Result: **below 1,000, the pair (987, 610) takes the most division steps,
  14** (captured output).
- **Ledger.** `g9:eratosthenes` (dates, from a university history-of-mathematics archive);
  `g9:largest-prime:2026` (the largest known prime, from the search project's own page) for a dated box.

### g9/05 Randomness and Simulation (`randomness-and-simulation`)

- **Hook.** Tom throws a die 60 times and gets four sixes, not ten: is the die unfair, or is that luck?
- **Sections.**
  1. *Pseudo-random numbers and the seed*: a computer follows instructions, so its "random" numbers come
     from a rule; a small generator written in the chapter (multiply, add, take the remainder) and its
     cycle; Python's `random`, `seed`, `randint`, `random()`, `choice`, `shuffle`; the same seed gives
     the same numbers (why every output in this book reruns identically).
  2. *Simulating dice, coins and draws*: one die, two dice, a deck of cards, a draw from a bag.
  3. *Frequencies settle near the probability*: recall the mathematics books' probability and
     frequency; 10, 100, …, 100,000 throws; the frequency of six against 1/6, charted.
  4. *A random walk*: a token moving left or right on a line by coin; where it ends after 100 steps;
     its farthest point.
  5. *Estimating by simulation*: the chance that two dice sum to 7, by simulation and exactly (6 of 36);
     estimating π from points in a square (the area of a quarter disc, recalled from the mathematics
     books).
- **Defines.** pseudo-random number generator; seed; simulation; estimation by simulation (method).
- **Recalls.** mathematics (probability, frequency, mean, area of a disc), in prose; g7/02 (lists);
  g8/02 (counting with a dictionary).
- **Listings.** `tiny_generator.py` (a generator with small numbers; its cycle printed); `seed_demo.py`;
  `die.py`; `two_dice.py`; `frequencies.py` (the table the chart uses); `deck.py` (`shuffle`, deal);
  `random_walk.py`; `sum_seven.py`; `estimate_pi.py`. Every listing sets a seed.
- **Figures.** Schematics (4): (a) the tiny generator's numbers on a circle, showing its cycle; (b) chart:
  frequency of a six against the number of throws (log scale on the x axis), from `.dat`; (c) chart: a
  random walk's path over 100 steps; (d) the quarter disc with simulated points (pgfplots scatter from
  `.dat`). AI: `g9-randomness-and-simulation-dice.jpg` (dice on a table).
- **Exercises (12: 4★, 5★★, 3★★★).** P: two programs with the same seed — same output?; P: the cycle of
  the tiny generator for a given start; P: what `choice` can return; S: a coin-toss simulation printing
  the longest run of heads; B: `randint(1, 6)` written `randint(0, 6)` — what changes in the
  frequencies; B: a seed set inside the loop gives the same throw every time — fix; S: simulate drawing
  two cards and the chance of a pair; S: a random walk on a grid (four directions); C: the exact chance of
  a double with two dice; C: the length of the tiny generator's cycle and why it cannot be longer than its
  modulus; C (★★★): explain why a simulation with 100 throws can be far from 1/6 and one with 100,000
  rarely is, with the chapter's chart (no formula: the observed spread); S (★★★): estimate the chance that
  a random walk of 20 steps ends where it started, and compare with the exact count of paths (computed
  by program).
- **Weekend problem — The birthday surprise (Parts I–III, 12 questions).** How likely is it that two
  pupils of a class share a birthday? I: by hand, why 366 pupils make it certain. II: a simulation of
  10,000 classes of 23 (birthdays as numbers 1 to 365), the frequency of a shared birthday; the same for
  sizes 5 to 60, charted. III: the exact chance as a product of fractions computed by program; the
  smallest class with a chance above one half. Result: **23 pupils already give a chance of about 0.507;
  simulation and the exact product agree to two decimals** (captured outputs).
- **Ledger.** `g9:python:mersenne-twister` (the generator behind `random` and its period, `PYTHON-DOCS`).

### g9/06 Secret Codes: A First Look at Cryptography (`first-cryptography`)

- **Hook.** Lina and Sami pass notes in class that only they can read; their teacher reads them anyway.
- **Sections.**
  1. *Encrypting and decrypting with a key*: plaintext, ciphertext, cipher, key; the key is the secret,
     not the method.
  2. *The shift cipher and its 25 keys*: each letter moved k places round the alphabet (with `ord`,
     `chr` and `%`, recall g7/03); breaking it by trying every key (a brute-force search).
  3. *Substitution ciphers and letter frequencies*: any mixing of the alphabet is a key; the number of
     keys (26 × 25 × … × 1, computed by a loop: far too many to try); frequency analysis: the most common
     letters of a long text, counted on the chapter's own invented passage, matched with the ciphertext's.
  4. *A cipher with a keyword*: each letter shifted by the next letter of a keyword; the frequencies
     flatten; why a longer keyword helps.
  5. *Why a long random key resists; the padlock in a browser* (told): a key as long as the message and
     never reused; the browser's padlock means the page travels encrypted and the server proved its name
     (how is Book 2's).
- **Defines.** cipher; plaintext; ciphertext; encryption and decryption (one definition); key (of a
  cipher; qualified, see DEFINITIONS.md); shift cipher; substitution cipher; frequency analysis;
  brute-force search; keyword cipher.
- **Recalls.** g7/03 (strings, `ord`, `chr`); g8/02 (counting with a dictionary); g9/05 (randomness for a
  random key); g5/03 (password, server).
- **Listings.** `shift.py`; `shift_back.py`; `brute_force.py` (all 25 decryptions of a ciphertext);
  `substitution.py`; `count_keys.py`; `frequencies.py` (on `passage.txt`, an invented passage kept in
  `listings/` as data); `guess_substitution.py` (first guess from frequency ranks, then two corrections
  typed in the listing); `keyword_cipher.py`; `keyword_frequencies.py` (flattened counts).
- **Figures.** Schematics (4): (a) a cipher wheel (two rings of letters, shift 3); (b) message flow:
  sender, key, ciphertext on the open channel, receiver, someone listening; (c) chart: letter frequencies
  of the passage and of its ciphertext (two bar charts from `.dat`); (d) the keyword cipher as a row of
  shifts over the message. Photo (history box): a fifteenth- or sixteenth-century cipher disk or a
  historical cipher manuscript (Commons, public domain, licence read).
- **Exercises (12: 4★, 5★★, 3★★★).** P: encrypt "CODE" with shift 3; P: decrypt a word with shift 23;
  P: the output of `count_keys.py`; S: a shift cipher that keeps capitals and leaves spaces and
  punctuation; B: a shift that runs past 'Z' (no `% 26`) — fix; B: decryption that shifts the wrong way;
  S: a brute-force search that prints only the decryption containing the most common English words from
  a given list; S: the keyword cipher's decryption; C: why shifting by 26 changes nothing, and why there
  are 25 useful keys; C: the time to try every substitution key at a billion keys per second (computed);
  C (★★★): why frequency analysis needs a long ciphertext (counts on 20, 100 and 1,000 letters of the
  passage); S (★★★): find a keyword's length by counting repeated three-letter groups (a guided version).
- **Weekend problem — Breaking a message without the key (Parts I–III, 12 questions).** A ciphertext of
  the shift cipher. I: count its letters by hand on the first line; guess the key from the most common
  letter. II: a program guessing the key from frequencies alone, checked on the whole message. III: cut
  the message to its first 10, 20, 50, 100, 200 letters and count, over 100 different messages taken
  from the passage, how often the guess is right. Result: **the share of right guesses for each length**,
  rising to (nearly) all for the longest (captured output; no number typed).
- **Ledger.** `g9:caesar:shift` (the shift of three, from a translation of Suetonius on a university
  site); `g9:al-kindi` (the ninth-century treatise on frequency analysis, from a library's or
  university's page); `g9:bellaso:1553` (the keyword cipher's first publication, from a library's page)
  for the history box; `g9:https` (what the padlock means, from RFC 8446/RFC 9110, `RFC-EDITOR`) only if a
  protocol name is printed.

### g9/07 Project: A Game on a Grid (`project-grid-game`)

- **Specification (one paragraph).** A maze game in the terminal: the player starts at S, must reach the
  treasure T without stepping on walls, collects every gem to open the gate, has a limited number of moves, and
  sees the maze redrawn after each typed move; mazes are read from text files.
- **Milestones.**
  1. *Representing the state*: the maze as a grid of characters (g9/03), the player's row and column, the
     gems collected, the moves left; a dictionary for the state (g8/02).
  2. *Reading a maze file*: one text file per level, checked (exactly one S and one T, every row the same
     length).
  3. *Drawing as text*: the grid printed with the player.
  4. *The rules as functions*: `can_move`, `move`, collecting a gem, opening the gate; each tested on small
     hand-made grids.
  5. *A turn and the game loop*: read a move (`w`, `a`, `s`, `d`), apply the rules, redraw, check for a win
     or no moves left; scripted games from `.stdin` files (a win and a loss); the program reacts to each
     move the player types (the word *event* is Book 2's).
  6. *A second level and a solver's check*: a level file that is impossible to win; a test that tries
     every sequence of up to N moves on a tiny maze to prove a level winnable (counting the sequences:
     4^N, from g8/01's doubling).
- **Defines.** nothing new (project).
- **Recalls.** g9/03 (grids, neighbours), g8/02 (dictionary), g8/03 (text files), g7/01 (functions),
  g7/06 and g8/06 (milestones and tests).
- **Listings.** `maze_v1.py` … `maze_v5.py` with `level1.txt`, `level2.txt` and `.stdin` files;
  `try_all_moves.py` (milestone 6, counts sequences). Tests `tests/test_maze.py`.
- **Figures.** Schematics (4): (a) the maze of level 1 drawn as a grid with S, T, walls, gems and the gate;
  (b) the state as a diagram (grid, position, gems, moves left); (c) one turn as a flowchart; (d) the
  tree of move sequences of length 1 and 2 (four branches each), with the count 4^N.
- **Exercises (12: 4★, 5★★, 3★★★)**, about the project: P: the drawn maze after three given moves; P:
  what `can_move` returns at a wall; S: a "wait" move; B: a move that wraps round the edge; S: count the
  moves of a winning game; B: a gate that opens before every gem is collected; S: a teleport square; C: how many sequences
  of 6 moves there are; S: a maze checker that finds unreachable treasure by trying all moves on a 3 × 3
  maze; S: the cellular automaton of g9/03's exercise as a second game mode; C (★★★): show that a maze with
  no gate is winnable in at most (number of free cells − 1) moves if it is winnable at all (a path never
  needs to visit a cell twice); S (★★★): the shortest winning sequence on a small maze by trying lengths
  1, 2, 3, … in order.
- **Ledger.** none.

## 8. Appendix: Typing Drills (`parts/typing/01-typing-drills.tex`, label prefix `typ`)

Written right after grade 3 (run file). Owned by g3/01, which teaches the technique; the appendix holds
only practice lines and their keyboards. No exercises and no solutions (the calibration gate does not
apply to `typing`; the solutions appendix inputs no typing file).

- **Opening (half a page).** How to use the drills: warm-up, home row first, no looking, accuracy before
  speed, ten minutes a day; how to time a passage and compute words per minute (recall g3/01's
  definition, no new pair).
- **One section per layout: QWERTY, AZERTY, QWERTZ** (the same structure in each):
  1. the full keyboard with finger zones (a TikZ figure; positions from the layout files, ledger
     `typ:layout:*`);
  2. home row drills (letters of the home row only: `asdf jkl;` / `qsdf jklm` / `asdf jklö`, then words
     made only of those letters, then short lines);
  3. top row and bottom row, one finger at a time, then mixed;
  4. capitals with the opposite Shift;
  5. digits (on AZERTY with Shift, said once) and common punctuation;
  6. words and sentences (English words for all three layouts in this edition; a language edition may
     use its own words: noted in a source comment);
  7. three timed passages of growing length with their character counts printed beside them.
- **Code.** The chapter file is written by hand; a test only *checks* it, so that each drill line uses
  only the keys it claims and every printed character count is right:
  `code/typing/01-typing-drills/tests/test_drills.py` reads `parts/typing/01-typing-drills.tex`, extracts
  each drill line with its declared key set and count (from a source comment beside it), and checks both
  against the layout files. Whether `code/typing/` is allowed is a question for the sync.
- **Figures.** Three keyboards with finger zones (one per layout); one hands-on-the-home-row figure reused
  from g3/01's drawing style. No AI image, no photograph.
- **Ledger.** `typ:layout:us`, `typ:layout:fr`, `typ:layout:de` (shared with g3/01).
- **Length.** about 12 pages (4 per layout).

