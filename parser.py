def parse_cnf_file(path):
    clause_list = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(('c', 'p', '%', '0')):
                continue
            try:
                literals = list(map(int, line.split()))
                clause = set(literals[:-1])
                clause_list.append(clause)
            except ValueError as e:
                print(f"Skipping line due to error: {line} ({e})")
    print(f"Parsed clauses: {len(clause_list)}")
    return clause_list # type: ignore