from collections import defaultdict, deque
from pprint import pprint
import itertools
import sys

EPS = 'ε'  # epsilon (used to denote empty)
END = '$'  # endmarker (terminal)


class Grammar:
    def __init__(self, prods, start):
        """
        prods: dict mapping lhs -> list of rhs lists (each rhs is list/tuple of symbols)
        start: start symbol (string)
        """
        self.prods = defaultdict(list)
        for A, rhss in prods.items():
            for rhs in rhss:
                # store rhs as list for mutability where needed
                self.prods[A].append(list(rhs))
        self.start = start
        self.aug_start = start + "'"  # S' (simple augmentation)

        # collect nonterminals and terminals
        self.nonterminals = set(self.prods.keys())
        self.terminals = set()
        for A, rhss in self.prods.items():
            for rhs in rhss:
                for s in rhs:
                    if s not in self.nonterminals:
                        self.terminals.add(s)

        # remove possible conflict if the augmented start symbol appears
        if self.aug_start in self.terminals:
            self.terminals.remove(self.aug_start)

        # add augmented production S' -> S
        self.prods[self.aug_start] = [[self.start]]
        self.nonterminals.add(self.aug_start)

        # we'll treat END ('$') as a terminal
        self.terminals.add(END)

    def productions(self):
        for A, rhss in self.prods.items():
            for rhs in rhss:
                yield (A, rhs)


# ---------- FIRST computation ----------

def compute_first(grammar):
    """Compute FIRST sets for all symbols (terminals and nonterminals).
    Returns a dict symbol -> set(symbols)
    """
    first = defaultdict(set)

    # For terminals: FIRST(a) = {a}
    for t in grammar.terminals:
        first[t].add(t)

    # Initialize nonterminals to empty sets (defaultdict already does that)
    changed = True
    while changed:
        changed = False
        for A, rhss in grammar.prods.items():
            for rhs in rhss:
                # rhs is a list; empty rhs denotes epsilon-production
                if len(rhs) == 0:
                    if EPS not in first[A]:
                        first[A].add(EPS)
                        changed = True
                    continue

                # walk symbols of rhs
                i = 0
                all_nullable = True
                while i < len(rhs):
                    X = rhs[i]
                    # add FIRST(X) \ {EPS} to FIRST(A)
                    before = len(first[A])
                    first[A].update(first[X] - {EPS})
                    if len(first[A]) != before:
                        changed = True

                    # if X cannot produce EPS, stop
                    if EPS not in first[X]:
                        all_nullable = False
                        break
                    i += 1

                if all_nullable:
                    if EPS not in first[A]:
                        first[A].add(EPS)
                        changed = True

    return first


def first_of_sequence(seq, first):
    """Return FIRST(seq) as a set. seq is sequence (list/tuple) of symbols.
    If seq is empty, result contains EPS.
    """
    result = set()
    if not seq:
        result.add(EPS)
        return result

    i = 0
    while i < len(seq):
        X = seq[i]
        result.update(first[X] - {EPS})
        if EPS in first[X]:
            i += 1
            if i == len(seq):
                result.add(EPS)
        else:
            break

    return result


# ---------- LR(1) item helpers ----------

def item_core_key(item):
    A, rhs, dot, la = item
    return (A, tuple(rhs), dot)


def lr1_closure(items, grammar, first):
    """
    items: iterable/set of LR(1) items (A, rhs, dot, lookahead)
    returns closure as a set of items
    """
    items = set(items)
    changed = True
    while changed:
        changed = False
        # iterate over snapshot because we may add while looping
        for (A, rhs, dot, la) in list(items):
            if not isinstance(rhs, tuple):
                rhs = tuple(rhs)

            if dot < len(rhs):
                B = rhs[dot]
                if B in grammar.nonterminals:
                    beta = rhs[dot + 1:]
                    # compute FIRST(beta + (la,))
                    seq = tuple(beta) + (la,)
                    lookahead_set = first_of_sequence(seq, first)
                    for prod in grammar.prods[B]:
                        for b in lookahead_set:
                            new_item = (B, tuple(prod), 0, b)
                            if new_item not in items:
                                items.add(new_item)
                                changed = True
    return items


def lr1_goto(items, X, grammar, first):
    moved = set()
    for (A, rhs, dot, la) in items:
        if not isinstance(rhs, tuple):
            rhs = tuple(rhs)
        if dot < len(rhs) and rhs[dot] == X:
            moved.add((A, rhs, dot + 1, la))

    if not moved:
        return frozenset()
    return frozenset(lr1_closure(moved, grammar, first))


# ---------- Build canonical LR(1) collection ----------

def build_canonical_lr1(grammar, first):
    start_item = (grammar.aug_start, tuple(grammar.prods[grammar.aug_start][0]), 0, END)
    I0 = frozenset(lr1_closure({start_item}, grammar, first))

    states = [I0]
    state_idx = {I0: 0}
    transitions = {}  # (i, X) -> j

    queue = deque([I0])
    symbols = list(grammar.nonterminals | grammar.terminals)

    while queue:
        I = queue.popleft()
        i = state_idx[I]
        for X in symbols:
            J = lr1_goto(I, X, grammar, first)
            if not J:
                continue
            if J not in state_idx:
                state_idx[J] = len(states)
                states.append(J)
                queue.append(J)
            transitions[(i, X)] = state_idx[J]

    return states, transitions


# ---------- Merge LR(1) states to produce LALR by LR(0) cores ----------

def core_of_state(I):
    """Return LR(0) core frozenset of (A, rhs, dot)"""
    return frozenset((A, rhs, dot) for (A, rhs, dot, la) in I)


def merge_lr1_states_to_lalr(lr1_states, lr1_trans):
    # group states by core
    core_map = {}
    for idx, I in enumerate(lr1_states):
        core = core_of_state(I)
        core_map.setdefault(core, []).append(idx)

    # build merged states: map lr1_state_idx -> merged_idx
    merged_states = []
    lr1_to_merged = {}

    for merged_idx, (core, group) in enumerate(core_map.items()):
        # merged_items: (A, rhs, dot) -> set(lookaheads)
        merged_items = {}
        for lr1_idx in group:
            for (A, rhs, dot, la) in lr1_states[lr1_idx]:
                key = (A, rhs, dot)
                merged_items.setdefault(key, set()).add(la)
            lr1_to_merged[lr1_idx] = merged_idx

        # convert merged_items to LR(1) item representation (tuples)
        itemset = set()
        for (A, rhs, dot), las in merged_items.items():
            for la in las:
                itemset.add((A, rhs, dot, la))
        merged_states.append(frozenset(itemset))

    # build merged transitions
    merged_trans = {}
    for (i, X), j in lr1_trans.items():
        mi = lr1_to_merged[i]
        mj = lr1_to_merged[j]
        merged_trans[(mi, X)] = mj

    return merged_states, merged_trans


# ---------- Build parsing tables (ACTION, GOTO) ----------

def build_parsing_tables(merged_states, merged_trans, grammar):
    ACTION = defaultdict(dict)  # ACTION[state][terminal] = ("shift", t) or ("reduce", (A, rhs)) or ("accept",)
    GOTO = defaultdict(dict)  # GOTO[state][nonterminal] = state

    # helper: populate shifts and gotos from transitions
    for (i, X), j in merged_trans.items():
        if X in grammar.terminals:
            ACTION[i][X] = ("shift", j)
        else:
            GOTO[i][X] = j

    # reductions & accept
    for i, I in enumerate(merged_states):
        for (A, rhs, dot, la) in I:
            if dot == len(rhs):
                # completed production
                if A == grammar.aug_start and la == END:
                    ACTION[i][END] = ("accept",)
                else:
                    new = ("reduce", (A, list(rhs)))
                    existing = ACTION[i].get(la)
                    if existing is not None and existing != new:
                        # record conflict list
                        ACTION[i].setdefault("_conflicts", []).append((la, existing, new))
                    else:
                        ACTION[i][la] = new

    return ACTION, GOTO


# ---------- Parser runtime (drives shift/reduce using ACTION/GOTO) ----------

def parse_input(tokens, ACTION, GOTO):
    input_buf = list(tokens) + [END]
    stack = [0]
    ip = 0
    steps = []

    while True:
        s = stack[-1]
        a = input_buf[ip]
        act = ACTION.get(s, {}).get(a)
        steps.append((list(stack), a, act))

        if act is None:
            steps.append(("error", s, a))
            return False, steps

        if act[0] == "shift":
            t = act[1]
            stack.append(a)  # symbol
            stack.append(t)  # state
            ip += 1
            continue

        if act[0] == "reduce":
            A, rhs = act[1]
            # special-case EPS: if production is [EPS] treat as empty
            if len(rhs) == 1 and rhs[0] == EPS:
                pop_count = 0
            else:
                pop_count = 2 * len(rhs)

            for _ in range(pop_count):
                stack.pop()

            s2 = stack[-1]
            g = GOTO.get(s2, {}).get(A)
            if g is None:
                steps.append(("goto_error", s2, A))
                return False, steps
            stack.append(A)
            stack.append(g)
            continue

        if act[0] == "accept":
            steps.append(("accept",))
            return True, steps

        steps.append(("unknown_action", act))
        return False, steps


# ---------- Utilities to display tables and conflicts ----------

def show_tables(ACTION, GOTO, grammar):
    print("ACTION table:")
    all_states = sorted(set(list(ACTION.keys()) + list(GOTO.keys())))
    for state in all_states:
        row = ACTION.get(state, {})
        entries = []
        for t, v in row.items():
            if t == "_conflicts":
                continue
            if v[0] == "shift":
                entries.append(f"{t}: shift {v[1]}")
            elif v[0] == "reduce":
                A, rhs = v[1]
                rhs_str = '.'.join(rhs) if rhs else EPS
                entries.append(f"{t}: reduce ({A} -> {rhs_str})")
            elif v[0] == "accept":
                entries.append(f"{t}: accept")
        print(f"State {state}: " + ", ".join(entries))

    print("\nGOTO table:")
    for s in sorted(GOTO.keys()):
        row = GOTO[s]
        print(f"State {s}: " + ", ".join(f"{A} -> {t}" for A, t in row.items()))
    print()


def show_conflicts(ACTION):
    conflicts = []
    for s, row in ACTION.items():
        if "_conflicts" in row:
            for rec in row["_conflicts"]:
                conflicts.append((s, rec))

    if conflicts:
        print("Conflicts detected:")
        for s, (la, existing, new) in conflicts:
            print(f" State {s}, lookahead {la}: existing={existing}, new={new}")
    else:
        print("No conflicts detected.")


# ---------- Example grammars and main ----------

def example_grammar():
    # classic example: S -> C C ; C -> c C | d
    prods = {
        'S': [['C', 'C']],
        'C': [['c', 'C'], ['d']]
    }
    start = 'S'
    return Grammar(prods, start)


def main():
    # simple arithmetic expression grammar with tokens like id, +, *, (, )
    prods = {
        'E': [['E', '+', 'T'], ['T']],
        'T': [['T', '*', 'F'], ['F']],
        'F': [['(', 'E', ')'], ['id']]
    }
    grammar = Grammar(prods, 'E')

    print("Nonterminals:", grammar.nonterminals)
    print("Terminals:", grammar.terminals)
    print("Augmented start:", grammar.aug_start)
    print()

    first = compute_first(grammar)
    print("FIRST sets:")
    for sym, s in first.items():
        print(f" {sym}: {s}")
    print()

    lr1_states, lr1_trans = build_canonical_lr1(grammar, first)
    print(f"Built {len(lr1_states)} LR(1) states.")

    merged_states, merged_trans = merge_lr1_states_to_lalr(lr1_states, lr1_trans)
    print(f"Merged into {len(merged_states)} LALR states.\n")

    ACTION, GOTO = build_parsing_tables(merged_states, merged_trans, grammar)
    show_tables(ACTION, GOTO, grammar)
    show_conflicts(ACTION)
    print()

    # parse example input (token list)
    tokens = ['id', '+', 'id', '*', 'id']
    print("Parsing tokens:", tokens)
    ok, steps = parse_input(tokens, ACTION, GOTO)
    for s in steps:
        print(s)
    print("Accepted?", ok)


if __name__ == "__main__":
    main()
