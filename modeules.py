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

def getMetadata(statments):
    pattern= {
    'libname':r'\s*Libname\s+(\w+)',
    'include': r'\s*%include\s+',
    'fileref': r'\s*Filename\s+(\w+)',
    'proc_import':r'\s*proc\s+import',
    'proc_export':r'\s*proc\s+export'
    }
    metadata= {
        'libname':[],
        'include':[],
        'fileref':[],
        'proc_import':[],
        'proc_export':[]
    }
    for stmt in statments:
        p= pattern['libname']
        match= re.search(p, stmt, re.IGNORECASE)
        if match:
            path= getUnixPath(stmt)
            if path:
                obj= {'name':match.group(1),'location':path}
                metadata['libname'].append(obj)

        
        p= pattern['fileref']
        match= re.search(p, stmt, re.IGNORECASE)
        if match: 
            path= getUnixPath(stmt)
            if path:
                obj= {'name':match.group(1),'location':path}
                metadata['fileref'].append(obj)
        
        p= pattern['include']
        match= re.search(p, stmt, re.IGNORECASE)
        if match: 
            path= getUnixPath(stmt)
            if path:
                obj= {'location':path}
                metadata['include'].append(obj)
       
        p= pattern['proc_import']
        match= re.search(p, stmt, re.IGNORECASE)
        if match: 
            path= getUnixPath(stmt)
            if path:
                obj= {'location':path}
                metadata['proc_import'].append(obj)

        p= pattern['proc_export']
        match= re.search(p, stmt, re.IGNORECASE)
        if match: 
            path= getUnixPath(stmt)
            if path:
                obj= {'location':path}
                metadata['proc_export'].append(obj)
                
    print(metadata)


def getUnixPath(input):

    regx= r'(/[\w]+)+(\.\w{1,7})?'
    
    unix_path= re.search(regx, input)
    if unix_path:
        return unix_path.group(0)
    else:
        return None

if __name__ == "__main__":

    with open("code.sas") as c:
        uncmtFile = commentRemover(c.read())
        # cleaning
        uncmtFile= uncmtFile.replace('\n',' ')
        uncmtFile = re.sub('\s+', ' ',uncmtFile)
        statements= uncmtFile.split(';')
        getMetadata(statements)
    