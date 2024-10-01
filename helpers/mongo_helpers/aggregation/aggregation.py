def group_by_field(collection, field):
    """Group by a specific field and return the count of occurrences."""
    pipeline = [
        {"$group": {"_id": f"${field}", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    return list(collection.aggregate(pipeline))

def aggregate_with_match(collection, match_criteria, group_field):
    """Perform an aggregation with a match and group."""
    pipeline = [
        {"$match": match_criteria},
        {"$group": {"_id": f"${group_field}", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    return list(collection.aggregate(pipeline))
