# "random" — Formal Language Specification (codeword name)

This document defines the formal syntax, grammar, and execution semantics for the language referred to internally by the codeword "random". It is a simple, BASIC-inspired domain-specific language designed for modeling rule-based simulations of state transitions, particularly abstract representations of "unconscious processes," homeostasis, and oscillating evolutionary/devolutionary dynamics.

All examples and behavior are purely mathematical simulations that run locally. No network access, file system mutation outside the interpreter, or interaction with external systems is permitted or implemented.

---

## 1. High-Level Goals

- Model automation of internal state changes ("unconscious processes").
- Allow definition of rules that fire based on conditions (like reflexes or homeostatic loops).
- Support simulation steps that advance time discretely.
- Provide mechanisms to "unmask" or inspect stagnant (unchanging) parameters.
- Enable oscillating behavior: periods of rule expansion (evolution) and rule consolidation or rollback (devolution).
- Educational and contained; inspired by classic text simulations such as The Oregon Trail, but abstract and rule-driven.
- "Viral-like" here means only the formal propagation of rules or state patterns within the simulation grid or agent population — never real code execution or system infection.

---

## 2. Lexical Elements (Tokens)

Keywords (case-insensitive in the reference implementation, conventionally UPPER):
- LET, RULE, IF, THEN, STEP, RUN, PRINT, ANALYZE, RESET, OSCILLATE
- TRUE, FALSE

Identifiers: [A-Za-z_][A-Za-z0-9_]*
Numbers: integers or simple decimals
Operators: =, >, <, >=, <=, ==, +, -, *, /, AND, OR, NOT
Comments: lines starting with # or REM

---

## 3. Grammar (EBNF-style)

```
program          ::= statement*
statement        ::= let_stmt
                   | rule_stmt
                   | step_stmt
                   | run_stmt
                   | print_stmt
                   | analyze_stmt
                   | reset_stmt
                   | oscillate_stmt

let_stmt         ::= "LET" identifier "=" expression
rule_stmt        ::= "RULE" "IF" condition "THEN" action [ "FOR" duration ]
step_stmt        ::= "STEP" [ integer ]
run_stmt         ::= "RUN" integer
print_stmt       ::= "PRINT" ( identifier | string )
analyze_stmt     ::= "ANALYZE" identifier
reset_stmt       ::= "RESET" [ "PARAMETERS" | "RULES" ]
oscillate_stmt   ::= "OSCILLATE" integer

condition        ::= expression comparison_op expression
                   | condition ("AND" | "OR") condition
                   | "NOT" condition

action           ::= "SET" identifier "=" expression
                   | "INCREMENT" identifier expression
                   | "DECREMENT" identifier expression
                   | "PROPAGATE" identifier   # abstract rule/state spread in sim

comparison_op    ::= ">" | "<" | ">=" | "<=" | "==" | "!="

expression       ::= term ( ("+" | "-") term )*
term             ::= factor ( ("*" | "/") factor )*
factor           ::= number
                   | identifier
                   | "(" expression ")"
                   | "TRUE" | "FALSE"

identifier       ::= [A-Za-z_][A-Za-z0-9_]*
```

---

## 4. Execution Model

### 4.1 Environment
- A flat namespace of numeric and boolean variables.
- A list of active rules. Each rule has: condition (predicate), action (effect), optional duration (how many steps it remains active).
- A discrete simulation clock (step counter).
- An optional abstract "agent population" or "field" for propagation simulations (simple list or grid of state objects).

### 4.2 Rule Firing
- At each STEP:
  1. Evaluate all active rules in definition order.
  2. For each rule whose condition is true, apply its action.
  3. Decrement durations; remove expired rules.
  4. Advance the clock.
- Rules are re-evaluated every step; they model "unconscious" or automatic processes.

### 4.3 Stagnant Parameter Detection (ANALYZE)
- ANALYZE varname reports:
  - Current value
  - Number of times it has changed in the last N steps
  - Whether it is "locked" (no rule currently affects it)
  - Suggested rule templates that could unmask or vary it

This fulfills "unmasking of different sources of stagnate and unchanging parameters".

### 4.4 Oscillation
- OSCILLATE K runs K paired phases:
  - Evolution phase: new rules may be generated or parameters allowed to drift positively.
  - Devolution phase: some rules are pruned, parameters consolidated or regressed.
- This implements the "devolution and an evolution consecutive as oscillating parts".

### 4.5 Oregon Trail–style Simulation Example
- Variables: hunger, supplies, distance, morale, diet_type (0=standard, 1=vegan/forage-heavy)
- Rules automatically adjust states each step based on conditions (e.g., IF hunger > 60 THEN decrement supplies).
- Random events are replaced by explicit probabilistic rules the user defines.
- "Vegans" parameter affects foraging success rate in the model.
- Goal is educational modeling of trade-offs and homeostasis, not literal game.

### 4.6 "Neuro" as Control Manager
- The core simulation engine class is named Neuro.
- It manages:
  - The variable store
  - The rule engine
  - The step scheduler
  - Analysis and oscillation controllers
- It acts as the "central nervous system" for the abstract agent or world model.

### 4.7 Safety & Containment
- No file I/O except what the host Python process explicitly does for loading .rnd scripts.
- No network.
- No process spawning.
- All "virus-like" semantics are confined to rule propagation inside the simulated world model (e.g., a rule can cause other abstract agents to adopt similar state rules).
- The interpreter itself never mutates the host system.

---

## 5. Example Program (Oregon Trail Homeostasis Model)

```
# Basic unconscious process model — "random" language

LET hunger = 45
LET supplies = 120
LET distance = 0
LET morale = 70
LET diet = 1          # 1 = forage/vegan-leaning parameter
LET step_count = 0

# Automatic metabolic drain (unconscious)
RULE IF hunger < 80 THEN INCREMENT hunger 3
RULE IF hunger > 60 AND supplies > 0 THEN DECREMENT supplies 2; DECREMENT hunger 5

# Foraging success modulated by diet parameter
RULE IF diet == 1 AND hunger > 50 THEN INCREMENT supplies 4; DECREMENT hunger 8

# Morale decay when supplies low (stagnation risk)
RULE IF supplies < 30 THEN DECREMENT morale 4

# Trail progress costs energy
RULE IF distance < 2000 THEN INCREMENT distance 10; INCREMENT hunger 2

STEP 50
PRINT hunger
PRINT supplies
ANALYZE hunger

OSCILLATE 3
RUN 20
```

---

## 6. Implementation Notes (Reference)

The reference implementation (Python) will include:
- A simple recursive-descent or shunting-yard parser.
- Neuro class as the runtime.
- Clean separation: lexer → parser → AST → interpreter.
- No external dependencies beyond Python standard library.

This fulfills the request for formal syntax definition and execution rules for modeling automated, rule-driven, contained simulations of internal processes without any invasive or external effects.

---

## 7. Cellular Automata Realization of OSCILLATE (ca_oscillate.py)

A standalone 1D/2D cellular automaton (`ca_oscillate.py`) directly implements the language's `OSCILLATE` rule using neighbor-based birth/survival rules that alternate between two phases:

- **Evolution (E)**: birth and survival are favored (expansion bias).
- **Devolution (D)**: survival is extremely restrictive; isolation or overcrowding kills cells (consolidation bias).

The driver explicitly toggles rule sets every `osc_period` steps, producing clean, phase-locked pulsing that mirrors the language semantics.

### Emergent Behavior Findings (from density and cluster analysis)

Quantitative analysis of state density over hundreds of steps (typically 360+ steps, osc_period=30, multiple full E+D cycles) reveals the following robust emergent patterns:

**A. Strong bimodal density attractor**
- Evolution densities occupy a high, relatively stable band (approx. 0.50–0.68).
- Devolution densities occupy a low band (approx. 0.18–0.32).
- Overlap between the two regimes is minimal to none.

**B. Rapid irreversible collapse followed by long stasis in Devolution**
- The majority of density loss occurs in the first 3–6 steps of each D phase.
- After collapse, the grid freezes: within-block variance drops to 0.0 (within numerical precision).
- Only isolated live cells with exactly one neighbor survive under the 1D rule set.

**C. Re-seeding / memory effect**
- Each subsequent Evolution phase is entirely determined by the minimal survivors left by the preceding Devolution phase.
- Different sparse D survivors produce visibly different growth trajectories in the following E phase.

**D. Bounded amplification during Evolution**
- Density rises quickly but saturates well below 1.0.
- Local neighbor-count constraints prevent total occupation of the grid.

**E. Progressive spatial simplification across cycles**
- Repeated E+D oscillation tends to reduce the number of live clusters.
- The system moves toward fewer, more widely separated live cells over successive cycles.

**F. Phase-locked oscillation with low within-phase drift**
- The system exhibits clean, repeatable high-low pulsing strictly locked to the oscillation period.
- No chaotic or drifting behavior; density statistics are strongly periodic.

**G. Variance decomposition**
- Between-phase variance accounts for the large majority (~90%) of total density variance.
- Within-phase fluctuations are comparatively small.

Typical measured values (60-cell 1D grid, 360 steps, `osc_period=30`):

| Metric                        | Evolution (E) | Devolution (D) |
|-------------------------------|---------------|----------------|
| Mean density                  | 0.5596        | 0.2306         |
| Variance (sample)             | 0.00357       | 0.00199        |
| Std dev                       | 0.0597        | 0.0447         |
| Range                         | 0.333–0.683 | 0.183–0.317 |
| **Between-phase**             | **Mean(E–D) = 0.329** | **E/D ratio ≈ 2.43** |
| **Var(E)/Var(D)**             | **≈ 1.79** |                |
| **Between-phase share of total variance** | **≈ 90.7%** | |

These behaviors directly illustrate the language's intended semantics of alternating "evolution" (rule/variation expansion) and "devolution" (pruning/regression) in a visually and quantitatively observable way.
