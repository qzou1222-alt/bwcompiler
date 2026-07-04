"""
Compile a .bw file into a Python dictionary.

It is primarily used by py3dbuilder to load game data.

Of course, you can also create .bw files yourself. We plan to release a BW Companion extension for VS Code in the future to provide syntax highlighting, diagnostics, and other editing tools.

bwcompiler is mainly intended for the py3dbuilder ecosystem, so it may not be useful for most Python projects.

If you find this project interesting, please consider giving it a star:
https://github.com/qzou1222-alt/py3dbuilder
"""
from pathlib import Path as _P
class TypeMismatchError(Exception): pass
class TypeInvalidRepeatError(Exception): pass
class TypeMissingError(Exception): pass
class InvalidSyntaxError(Exception): pass

def read(filearg: str | _P):
    with open(filearg, "r", encoding="utf-8") as fp:
        r=fp.read()
    return r
def compile(filearg: str | _P):
    filearg = str(filearg)

    if not filearg.endswith(".bw"):
        raise InvalidSyntaxError("Not a .bw file")
    strdct=""
    strbw=read(filearg).replace("[","").\
        replace("]","").\
            replace("<(","[").\
                replace(")>","]").\
                    replace("<","{").\
                        replace(">","}")
    lines=strbw.splitlines()
    if len(lines)<2:
        lines=strbw.split(",")
    for line in lines[2:]:
        if "=" in line:
            thisline=line.replace(line[:line.index("=")].strip(),'"'+line[:line.index("=")].strip()+'"')+"\n"
            if "name" in line:
                thisline=thisline.replace(line[line.index("=")+1:-1].strip(),'"'+line[line.index("=")+1:-1].strip()+'"')
            strdct+=thisline
        else:
            strdct+=line+"\n"
    strdct=strdct.replace("=",":")
    import tempfile
    import json
    with tempfile.TemporaryDirectory() as tempstr:
        with open(tempstr+"\\__example.json","w") as f:
            f.write(strdct)
        with open(tempstr+"\\__example.json","r") as p:
            dct:dict=json.load(p)
    return dct

            