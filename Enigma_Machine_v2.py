from sys import argv
from os import path

def encrypt(inp, rotors):
    index, N = 0, len(rotors[0])
    out_ch, out_str = 0, []
    for ch in inp:
        out_ch = ch
        for i in range(1, len(rotors)):
            out_ch = rotors[i][(rotors[0].index(out_ch) + index) %N]
            index += 1
        out_str.append(out_ch)
    return bytes(out_str)

def decrypt(inp, rotors):
    index, N = (len(rotors)-1) * len(inp), len(rotors[0])
    out_ch, out_str = 0, []
    for ch in inp[::-1]:
        out_ch = ch
        for i in range(len(rotors)-1, 0, -1):
            index -= 1
            out_ch = rotors[0][(rotors[i].index(out_ch) - index) %N]
        out_str.append(out_ch)
    return bytes(out_str[::-1])

def convert_kwargs(kwargs):
    return {i.split('=')[0]:i.split('=')[1] for i in kwargs}

def get_output_filename(inp_file, will_decrypt):
    ext = inp_file.split('.')
    if len(ext) > 1:
        ext = ext[-1]
        return '%s_%s.%s' % (inp_file[:(-len(ext)-1)], ('decrypted' if will_decrypt else 'encrypted'), ext)
    else:
        return '%s_%s' % (inp_file, ('decrypted' if will_decrypt else 'encrypted'))

def validate_input(inp, kwargs):
    if len(inp) < 2:
        return 'Too few inputs'
    try:
        kwargs = convert_kwargs(kwargs)
    except IndexError:
        return 'Unknown format, optional args must begin in "--" and seperate argument and value with "="'
    for i in kwargs:
        if i[:2] != '--':
            return 'Unknown format, optional args must begin in "--" and seperate argument and value with "="'
        if i[2:].lower() not in ['decrypt', 'inplace']:
            return 'Unknown optional argument'
        if kwargs[i].lower() not in ['true', 'false']:
            return 'Keyword arguments must be either "true", or "false"'
    for i, err in enumerate(['Input', 'Key']):
        if not path.isfile(inp[i]):
            return '%s file not found.' % err
    return ''
        

if __name__=="__main__":
    # Define helpful constants / functions
    help_str = 'py Enigma_Machinev2.py <path_to_file> <path_to_key> (--decrypt=<false/true> --inplace=<false/true>)'
    boolean_inp = lambda x: True if x.lower() == 'true' else False

    # Gather input and validate
    args, kwargs = argv[1:3], argv[3:]
    err_str = validate_input(args, kwargs)
    if err_str:
        print(err_str)
        print(help_str)
    else:
        # Gather input values
        inp_file, key_file = args[0], args[1]
        kwargs = convert_kwargs(kwargs)
        will_decrypt = boolean_inp(kwargs['--decrypt']) if '--decrypt' in kwargs.keys() else False
        inplace = boolean_inp(kwargs['--inplace']) if '--inplace' in kwargs.keys() else False
        # Open and read files
        with open(inp_file, 'rb') as f:
            inp = f.read()
        rotors = [[] for _ in range(4)]
        with open(key_file,'rb') as f:
            for i, b in enumerate(f.read().decode('utf-8')):
                rotors[i//256].append(ord(b))
        # Encrypt / decrypt based on parameters
        output = decrypt(inp, rotors) if will_decrypt else encrypt(inp, rotors)
        out_file = inp_file if inplace else get_output_filename(inp_file, will_decrypt)
        with open(out_file,'wb') as f:
            f.write(output)
    