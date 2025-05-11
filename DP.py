from multiprocessing import Process, Queue

def simplify_clauses(clause_list, assignment):
    simplified = []
    for clause in clause_list:
        if any(lit in assignment and assignment[lit] for lit in clause):
            continue
        new_clause = {lit for lit in clause if -lit not in assignment or assignment[-lit]}
        simplified.append(new_clause)
    return simplified

def unit_propagate(clause_list, assignment):
    changed = True
    while changed:
        changed = False
        unit_clauses = [c for c in clause_list if len(c) == 1]
        if not unit_clauses:
            break
        for unit in unit_clauses:
            lit = next(iter(unit))
            if -lit in assignment and assignment[-lit]:
                return None, None
            assignment[lit] = True
            assignment[-lit] = False
            clause_list = simplify_clauses(clause_list, assignment)
            changed = True
            break
    return clause_list, assignment

def pure_literal_assign(clause_list, assignment):
    literals = {lit for clause in clause_list for lit in clause}
    pure_literals = {lit for lit in literals if -lit not in literals}
    for lit in pure_literals:
        assignment[lit] = True
        assignment[-lit] = False
    new_clauses = [c for c in clause_list if not any(l in c for l in pure_literals)]
    return new_clauses, assignment

def dp_solver(clause_list):
    def recursive_solve(clause_list, assignment):
        clause_list, assignment = unit_propagate(clause_list, assignment)
        if clause_list is None:
            return False
        if not clause_list:
            return True
        clause_list, assignment = pure_literal_assign(clause_list, assignment)
        if not clause_list:
            return True
        var = next(iter(next(iter(clause_list))))
        for value in [True, False]:
            new_assignment = assignment.copy()
            new_assignment[var] = value
            new_assignment[-var] = not value
            new_clause_list = simplify_clauses(clause_list, new_assignment)
            if recursive_solve(new_clause_list, new_assignment):
                return True
        return False
    return recursive_solve([set(c) for c in clause_list], {})

def dp_worker(clauses, queue):
    try:
        result = dp_solver(clauses)
        queue.put(result)
    except Exception as e:
        print(f"[dp_worker] Exception: {e}")
        queue.put(None)

def run_dp_with_timeout(clauses, timeout=60):
    queue = Queue()
    p = Process(target=dp_worker, args=(clauses, queue))
    p.start()
    p.join(timeout)
    if p.is_alive():
        print("Timeout! Killing process...")
        p.terminate()
        p.join()
        return None
    return queue.get()

