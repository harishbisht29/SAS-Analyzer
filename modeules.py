import re
import os

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
    'proc_export':r'\s*proc\s+export',
    'input_table':r'\s+(from|set|join)\s+(\w+\.?\w*)',
    'output_table':r'\s+(data|create table)\s+(\w+\.?\w*)',
    # 'output_table':,
    }
    metadata= {
        'libname':[],
        'include':[],
        'fileref':[],
        'proc_import':[],
        'proc_export':[],
        'input_table':[],
        'output_table':[]
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

        p =pattern['input_table']
        match= re.search(p, stmt, re.IGNORECASE)
        if match:
            for m in re.findall(p,stmt):
                table= m[1]
                if table.upper() == "CONNECTION":
                    continue
                # print(m)
                if table not in metadata['output_table']:
                    metadata['input_table'].append(table)

        p =pattern['output_table']
        match= re.search(p, stmt, re.IGNORECASE)
        if match:
            table= match.group(2)
            metadata['output_table'].append(table)
    print(metadata)
    return metadata

def getFileName(location):
    return(os.path.basename(location))

def resolveReference(input, references):
    output= []

    for i in input:
        
        if 'ACCS_PRODV' in i.upper():
            if '.' in i:
                output.append(i.split('.')[1])
            else:
                output.append(i)
        elif '.' in i:
            ref= i.split('.')[0]
            f =i.split('.')[1]

            for l in references:
                if l['name'].upper() == ref.upper():
                    resolved= os.path.join(l['location'], f)
                    output.append(resolved)
                    break
    return output

def generateOutputFile(metadata, code_file):

    code= getFileName(code_file)
    # Application name
    application_name= os.path.splitext(code)[0]
    # Command Programs
    common_programs= [i['location'] for i in metadata['include']]
    # Program Location
    program_location= os.path.dirname(code_file)
    # output Location
    export_locations= [i['location'] for i in metadata['proc_export']]
    resolved= resolveReference(metadata['output_table'], metadata['libname'])

    output_location= resolved+ export_locations

    output={
        "application_name":application_name,
        "program_name":code,
        "common_programs":common_programs,
        "program_location":program_location,
        "output_location":output_location,
        # "output_file":,
        # "status":,
        # "input_file":
    }
    print(output)

def getUnixPath(input):

    regx= r'(/[\w]+)+(\.\w{1,7})?'
    
    unix_path= re.search(regx, input)
    if unix_path:
        return unix_path.group(0)
    else:
        return None

if __name__ == "__main__":
    code= '/home/immortal/Codes/SAS-Analyzer/code.sas'
    with open(code) as c:
        cfile= getFileName(code)
        uncmtFile = commentRemover(c.read())
        # cleaning
        uncmtFile= uncmtFile.replace('\n',' ')
        uncmtFile = re.sub('\s+', ' ',uncmtFile)
        statements= uncmtFile.split(';')
        metadata= getMetadata(statements)
        generateOutputFile(metadata, cfile)
    