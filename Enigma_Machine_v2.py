from copy import deepcopy as dc

def getPerms(elms):
    if len(elms) < 2: return [elms]
    elif len(elms) == 2: return [elms,elms[::-1]]
    else:
        out = []
        for i in range(len(elms)):
            nex = dc(elms)
            tmp = nex[i]
            nex[i] = nex[0]
            nex[0] = tmp
            perms = getPerms(nex[1:])
            out += [ [nex[0]] + j for j in perms]
        return out


if __name__=="__main__":
    elms = [1,2,3,4]
    perms = getPerms(elms)
    for i in perms: print(i)