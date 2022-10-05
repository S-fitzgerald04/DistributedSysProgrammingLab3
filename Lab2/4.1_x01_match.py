class X01MatchBuilder:
    """
    This could be extended to include dynamic key-value pair parameters (see object_factory.py),
    or make it a singleton, etc.
    """
    def __init__(self):
        pass

    def __call__(self):
        return X01Match()
