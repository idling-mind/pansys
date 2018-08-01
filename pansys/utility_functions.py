def return_value(instring):
    """Function to convert a string to corresponding number format"""
    from ast import literal_eval
    try:
        return literal_eval(instring)
    except:
        return instring


def calculate_skip_rows(f, count_of_unique):
    """Function to calculate the number of rows to be skipped in a
    column based output file

    Args:
        f (str): The file from which the number of rows to skip are to be found
        count_of_unique (int): The number of rows which should show the same
            number of fields and characters in a line after which the number of
            header rows can be calculated.
    """
    line_stats = []
    with open(f, 'r') as f:
        for line in f:
            # A list is made with number of characters and number of fields as
            # tuples
            nfields = len(line.split())
            nline = len(line)
            line_stats.append((nline, nfields))
            # Once the number or rows read in are more than count_of_unique,
            # then comparison of the last items can start
            if len(line_stats) > count_of_unique:
                if len(set(line_stats[-count_of_unique:])) == 1:
                    # Checking if the last count_of_unique lines in the file
                    # are having the same number of fields and characters
                    return len(line_stats) - count_of_unique - 1
        # if all lines are read in and still couldnt find column data
        # then go reverse and find the number of rows with same number of
        # characters and fields
        for i in reversed(range(count_of_unique)):
            if len(set(line_stats[-i:])) == 1:
                return len(line_stats) - i
