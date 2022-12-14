"""
This module contains functions for extracting and parsing details out
of comic book filenames.

@author: cbanack
"""

import re

__failed_regex = None

# ==============================================================================


def regex(filename_s, regex_s):
    """
    Takes the filename of a comic book, and extracts three strings out of it
    using the given regular expression, which must match the filename and create
    regex groups called "series", "num", and "year".  The extracted details
    will be the series name, the issue number, and the issue year.  These three
    details are returned as a triple, i.e. ("batman", "344", "2004").

    As long as AT LEAST a series name is found, this function will return the
    triple (missing values will be "").  Otherwise, it returns None.
    """
    global __failed_regex

    results = None
    if regex_s != __failed_regex:
        try:
            match = re.match(regex_s, filename_s)
            if match:
                founddict = {
                    x: match.group(x)
                    for x in match.groupdict()
                    if match.group(x) and match.group(x).strip()
                }
                if "series" in founddict:
                    results = (
                        match.group("series"),
                        match.group("num") if "num" in founddict else "",
                        match.group("year") if "year" in founddict else "",
                    )
        except:
            __failed_regex = regex_s
            results = None
    return results


# ==============================================================================


def extract(name_s):
    """
    Takes the filename of a comic book, and extracts three strings out of it: the
    series name, the issue number, and the issue year. These three pieces
    of information are returned as a triple, i.e. ("batman", "344", "2004").

    This function never returns None, and it will ALWAYS return the triple with
    at least a non-empty series name (even if it is just "unknown"), but the
    issue number and year may be "" if they couldn't be determined.
    """

    # 1. 's' is the name of our 'working' series name.  we'll slowly strip the
    #    'non-series name' data out of it, til what's left is the series name
    s = name_s

    # 2. but first, see if there's a volume/year in there.
    volume_year_s = __extract_year(s)

    # 3. strip out all bracketed data from the name
    def recurse_sub(pattern, s):
        while re.search(pattern, s):
            s = re.sub(pattern, "", s)
        return s

    s = recurse_sub(r"\([^\(]*?\)", s)
    s = recurse_sub(r"\{[^\{]*?\}", s)
    s = recurse_sub(r"\[[^\[]*?\]", s)

    # 4. clean out underscores
    s = re.sub(r"_", " ", s)

    # 5. remove all trace of volume from the name (like "vol. 2a" and "vol -3.1")
    s = re.sub(r"(?i)(\b((v|vol)\.?|volume))\s*-?\s*[0-9]+[.0-9a-z]*", "", s)

    # 6. remove all page counts, ie. "245p" or "50 pages"
    s = re.sub(r"(?i)\b[.,]?\s*\d+\s*(p|pg|pgs|pages)\b[.,]?", "", s)

    # 7. remove anything following a similar pattern to "02 of 02 covers"
    s = re.sub(r"(?i)(\d+\s*of\s*\d+\s*covers)", "", s)

    # 8. if the name has things like "4 of 5", remove the " of 5" part
    #    also, if the name has 3-6, remove the -6 part.  note that we'll
    #    try to handle the word "of" in a few common languages, like french/
    #    spanish (de), italian (di), german (von), dutch (van) or polish (z)
    s = re.sub(r"(?i)(?<=\d)(\s*(of|de|di|von|van|z)\s*#*\d+)", "", s)
    s = re.sub(r"(?<=\d)(-\d+)", "", s)

    # 9. iff this is one of those comic books that replaces all spaces with
    #    dashes, then strip the dashes out.  otherwise leave them in (because
    #    they might be important, like minus signs or something.)
    if "-" in s and " " not in s:
        s = re.sub(r"(?<![-_# ])-", " ", s)

    # 10. get an ordered list of issue number-like strings in the filename
    #    for example:  3, #4, 5a, 6.00, 10.0b, .5, -1.0
    #    also, remove numbers that look like years, EXCEPT on the "2000AD" series
    matches = __extract_numbers(s)

    # 11. if there's multiple numbers in the filename, and it starts with
    #    something like "05. " or "12 - " we assuming these files are part of
    #    a reading list, and we strip out that first part.
    pattern = r"^\s*\d+(\.\s+|\s*-\s*(?=\D))"
    if len(matches) > 1 and re.match(pattern, s):
        s = re.sub(pattern, "", s, 1)
        matches = __extract_numbers(s)
    # 12. if we parsed out some potential issue numbers, designate the LAST
    #    (rightmost) one as the actual issue number, and remove it from the name
    if len(matches) > 0:
        issue_num_s = matches[-1].group()
        issue_num_s = issue_num_s.replace(matches[-1].group(1), "")
        # series_s = s[:matches[-1].start(0)] + s[matches[-1].end(0):]
        series_s = s[: matches[-1].start(0)]
        # 10a. strip off leading/trailing zeroes
        matches = re.match("^(0+)([0-9].*)$", issue_num_s)
        issue_num_s = matches.group(2) if matches else issue_num_s
        if re.match(r"^-?[.0-9]+.?\w+$", issue_num_s) and __is_number(issue_num_s):
            issue_num_s = __sstr(
                float(issue_num_s) if "." in issue_num_s else int(issue_num_s)
            )
    else:
        issue_num_s = ""
        series_s = s

    # 13. contract repeating whitespace, and strip bad chars off the ends
    series_s = re.sub(r"\s{2,}", " ", series_s).strip(" ,-_")

    return [series_s, issue_num_s, volume_year_s]


# ==============================================================================
def __extract_year(s):
    """
    Searches through the given string left-to-right, seeing if an intelligible
    publication year can be extracted.  if it can, it will be returned as a
    four digit string, otherwise "" will be returned.
    """

    retval = ""

    # type one years appear exactly as "V2003".  there's a popular comicrack
    # script that creates dates that look like this, so parse em if we can
    results = [
        x[1]
        for x in re.findall(r"(?i)(^|[, -_])v(\d{4})($|[, -_])", s)
        if __isYear(x[1])
    ]

    if len(results) == 1:
        retval = results[0]
    else:
        # roughly, we're looking for a year or year range inside brackets
        # so: [2003], (2004-6), {2000-2010}, etc.

        # 1. get everything substring is strictly inside only one set of brackets
        results = re.findall(r"\([^[\](){}]*?\)", s)
        results += re.findall(r"\[[^[\](){}]*?\]", s)
        results += re.findall(r"\{[^[\](){}]*?\}", s)
        # 2. strip off the outer brackets and spaces
        results = [x.strip(r"()[]{}").strip() for x in results]
        # 3. if there is a year range, strip of the second half "2006-2009" -> "2006"
        results = [re.sub(r"(\d{4})\s*-\s*\d{1,4}", r"\1", x) for x in results]
        # 4. only keep strings that are valid 4 digit years
        results = [x for x in results if __isYear(x)]
        retval = results[-1] if results else ""

    return retval


# ==============================================================================
def __extract_numbers(s):
    """
    Searches through the given string left-to-right, building an ordered list of
    "issue number-like" re.match objects.  For example, this method finds
    matches substrings like:  3, #4, 5a, 6.00, 10.0b, .5, -1.0
    """
    matches = list(re.finditer(r"(?u)(^|[_\s#])(-?\d*\.?\d\w*)(\.?\w*$|)", s))
    # remove matches that look like years, EXCEPT on the "2000AD" series,
    # the  "The Beano" series, and any year that starts with '#' (i.e. #1950)
    is2000AD = re.match(r"(?i)\s*2000[\s\.-_]*a[\s.-_]*d.*", s)
    isBeano = re.match(r"(?i)\s*the[\s\.-_]+beano[\s.-_]+#?\d{4}", s)
    if not is2000AD and not isBeano:
        matches = [
            x
            for x in matches
            if not __isYear(x.group(2)) or (x.start(2) > 0 and s[x.start(2) - 1] == "#")
        ]
    return matches


# ==============================================================================
def __isYear(d):
    """Returns true iff the give stream appears to be a valid 4 digit year."""
    return re.match(r"^\d{4}$", d) and int(d) > 1900 and int(d) < 2100


# ==============================================================================
def __sstr(object):
    """safely converts the given object into a string (sstr = safestr)"""
    if object is None:
        return "<None>"
    if __is_string(object):
        # this is needed, because str() breaks on some strings that have unicode
        # characters, due to a python bug.  (all strings in python are unicode.)
        return object
    return str(object)


# ==============================================================================
def __is_number(s):
    """returns a boolean indicating whether the given object is a number, or
    a string that can be converted to a number."""
    try:
        float(s)
        return True
    except:
        return False


# ==============================================================================
def __is_string(object):
    """returns a boolean indicating whether the given object is a string"""

    if object is None:
        return False
    return True
