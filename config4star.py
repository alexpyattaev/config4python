
def writeconf(fname, config_dict):
    with open(fname, 'wt') as out_file:
        for secname, section in config_dict.items():
            out_file.write(f'{secname} {{\n')
            for varname, var in section.items():
                out_file.write(f'    {varname} = "{var}";\n')
            out_file.write(f'}};\n\n')


def readconf(fname):
    nonprint = ' \t\n'
    with open(fname, 'rt') as in_file:
        buf = in_file.read(5000).replace('\n', '')  # Read original file stripping EoL chars
        scopes = {}
        scopename = ""
        reading_scope = False
        for c in buf:
            if c == "{":  # Scope starts
                reading_scope = True
                scopes[scopename] = ""
            elif c == "}":  # Scope ends
                reading_scope = False
                scopename = ""
            elif reading_scope:
                scopes[scopename] += c
            else:
                if c in "; \n\t":
                    continue
                scopename += c

        for sn in list(scopes.keys()):
            text = scopes[sn]
            scopes[sn] = {}
            for line in text.split(";"):
                line = line.strip()
                if "=" in line:
                    k, v = line.split("=", 1)
                    scopes[sn][k.strip(nonprint)] = v.strip(nonprint).lstrip('"').rstrip('"')
    return scopes


def test_readconf():
    fname = 'LSRC.conf.testing'
    scopes = readconf(fname)
    print(scopes['debug']['debug_file'])
    print(scopes['global']['node_id'])
    print(scopes['global']['my_mac'])
    print(scopes['global']['db_connect_string'])
    writeconf(fname + "_new", scopes)
