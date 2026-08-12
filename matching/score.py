def compatibility_score(perfume_a: dict, perfume_b: dict) -> float:
    """
    perfume_a/b: {"accord_name": strength, ...}
    Retorna score de 0 a 1: quão bem os dois combinam para layering.
    """
    accords_a = set(perfume_a.keys())
    accords_b = set(perfume_b.keys())

    shared = accords_a & accords_b
    all_accords = accords_a | accords_b

    if not all_accords:
        return 0.0

    # similaridade base (Jaccard)
    jaccard = len(shared) / len(all_accords)

    # penaliza perfumes quase idênticos (queremos complementaridade, não clones)
    overlap_ratio = len(shared) / min(len(accords_a), len(accords_b))
    identity_penalty = max(0, overlap_ratio - 0.7) * 0.5

    score = jaccard - identity_penalty
    return max(0.0, min(1.0, score))