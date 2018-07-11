def return_value(instring):
    """Function to convert a string to corresponding number format"""
    from ast import literal_eval
    try:
        return literal_eval(instring)
    except:
        return instring
