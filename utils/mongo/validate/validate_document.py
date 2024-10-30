def validate_document_schema(document, schema):
    """
    Validate a document against a simple schema.
    The schema is a dictionary where keys are field names, and values are expected types.
    """
    for field, field_type in schema.items():
        if field in document:
            if not isinstance(document[field], field_type):
                return False, f"Field '{field}' is not of type {field_type}"
        else:
            return False, f"Field '{field}' is missing"
    return True, "Document is valid"
