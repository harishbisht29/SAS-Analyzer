from modeules import commentRemover

output= {}
output["name"]= None
output["includes"]= None
output["count"]= None
output["program_location"]= None
output["output_location"]= None
output["output_files"]= None
output["input_sources"]= None
output["is_active"]= None

with open("code.sas") as c:
    uncmtFile = commentRemover(c.read())
    # cleaning
    uncmtFile= uncmtFile.replace('\n',' ')
    uncmtFile = re.sub('\s+', ' ',uncmtFile)
    statements= uncmtFile.split(';')

