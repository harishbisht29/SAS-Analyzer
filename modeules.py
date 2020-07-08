import re

def removeComments(text):
    """ remove c-style comments.
        text: blob of text with comments (can include newlines)
        returns: text with comments removed
    """
    pattern = r"""
             ##
           /\*              ##  Start of /* ... */ comment
           [^*]*\*+         ##  Non-* followed by 1-or-more *'s
           (                ##
             [^/*][^*]*\*+  ##
           )*               ##  0-or-more things which don't start with /
                            ##    but do end with '*'
           /                ##  End of /* ... */ comment

    """
    regex = re.compile(pattern, re.VERBOSE|re.MULTILINE|re.DOTALL)
    noncomments = [m.group(2) for m in regex.finditer(text) if m.group(2)]

    return "".join(noncomments)

def commentRemover(text):
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return " " # note: a space and not an empty string
        else:
            return s
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, text)


def defination_search(text):
    libx= r'Libname (\w+)'
    match= re.search(libx, text, re.IGNORECASE)
    if match:
        return {'type':'libref','name':match.group(1)}

    filex= r'Filename (\w+)'
    match= re.search(filex, text, re.IGNORECASE)
    if match: 
        return {'type':'fileref','name':match.group(1)}
        
if __name__ == "__main__":

    with open('code.sas') as f:
        uncmtFile = commentRemover(f.read())
        # cleaning
        uncmtFile= uncmtFile.replace('\n',' ')
        uncmtFile = re.sub('\s+', ' ',uncmtFile);

        statements= uncmtFile.split(';')

    # print(statements)
    s= defination_search('  Filename tis_misops "/just/a/test/location"')
    print(s)