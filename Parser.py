from scanner import *

NODEKIND = ['StmtK', 'ExpK']
STMTKIND = ['IfK', 'RepeatK', 'AssignK', 'ReadK', 'WriteK']
EXPKIND = ['OpK', 'ConstK', 'IdK']


class TreeNode:
    def __init__(self, nodekind, kind, attr, lineno):
        self.nodekind = nodekind
        self.kind = kind
        self.attr = attr
        self.lineno = lineno
        self.childnodes = [0,0,0]
        self.sibling = 0



tokens = getToken()
token_type = 0
token_value = 0


def parser():
    global token_type, token_value
    token_type, token_value = tokens.__next__()
    t = stmt_squence()
    return t


def match(expected):
    global token_type, token_value
    if token_type == expected:
        token_type, token_value = tokens.__next__()
    else:
        print("unexpected token:" + token_type + " " + token_value)
        exit()


def stmt_squence():
    p = statement()
    t = p
    v = p
    while t != 0:
        match('SEMI')
        t = statement()
        v.sibling = t
        v = t
    return p


def statement():
    handle = {"IF": if_stmt, "REPEAT": repeat_stmt, "ID": assign_stmt, "READ": read_stmt, "WRITE": write_stmt}
    if handle.__contains__(token_type):
        return handle[token_type]()
    else:
        return 0


def write_stmt():
    match('WRITE')
    t = TreeNode('StmtK', "WriteK", token_value, line)
    t.childnodes[0] = exp()
    return t


def read_stmt():
    match('READ')
    t = TreeNode('StmtK', "ReadK", token_value, line)
    match('ID')
    return t


def assign_stmt():
    t = TreeNode('StmtK', "AssignK", token_value, line)
    match(token_type)
    match('ASSIGN')
    t.childnodes[0] = exp()
    return t


def repeat_stmt():
    t = TreeNode('StmtK', 'RepeatK', token_value, line)
    match('REPEAT')
    t.childnodes[0] = stmt_squence()
    match('UNTIL')
    t.childnodes[1] = exp()
    return t


def if_stmt():
    t = TreeNode('StmtK', 'IfK', token_value, line)
    match('IF')
    t.childnodes[0] = exp()
    match('THEN')
    t.childnodes[1] = stmt_squence()
    if token_type == 'ELSE':
        match('ELSE')
        t.childnodes[2] = stmt_squence()
    match('END')
    return t


def exp():
    t = simple_exp()
    if token_type == 'LT' or token_type == 'EQ':
        p = TreeNode('ExpK', "OpK", token_value, line)
        p.childnodes[0] = t
        t = p
        match(token_type)
        t.childnodes[1] = simple_exp()
    return t


def simple_exp():
    t = term()
    while token_type == 'PLUS' or token_type == 'MINUS':
        p = TreeNode('ExpK', "OpK", token_value, line)
        p.childnodes[0] = t
        t = p
        match(token_type)
        t.childnodes[1] = term()
    return t


def term():
    t = factor()
    while token_type == 'TIMES' or token_type == 'DIV':
        p = TreeNode('ExpK', 'OpK', token_value, line)
        p.childnodes[0] = t
        t = p
        match(token_type)
        t.childnodes[1] = factor()
    return t


def factor():
    if token_type == 'NUM':
        t = TreeNode('ExpK', 'ConstK', int(token_value), line)
        match(token_type)
        return t
    elif token_type == 'ID':
        t = TreeNode('ExpK', 'IdK', token_value, line)
        match(token_type)
        return t
    elif token_type == 'LPARAM':
        match('LPARAM')
        t = exp()
        match('RPARAM')
        return t
    else:
        print("unexpected token:" + token_type + " " + token_value)
        exit()


parser()
