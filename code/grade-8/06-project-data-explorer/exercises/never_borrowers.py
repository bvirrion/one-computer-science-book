def never_borrowers(members, loans):
    """The member_id of the members that no loan mentions."""
    borrowed = {}
    for loan in loans:
        borrowed[loan["member_id"]] = True
    ids = []
    for member in members:
        if member["member_id"] not in borrowed:
            ids.append(member["member_id"])
    return ids
