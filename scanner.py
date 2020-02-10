import string

TOKEN_TYPE = ['PLUS','MINUS','TIMES','DIV','LT','EQ','LPARAM','RPARAM','SEMI','ASSIGN'
              "ID",'NUM',
              'IF','THEN','ELSE','END','REPEAT','UNTIL','READ','WRITE',
              'ENDFILE','ERROR']


WHILE_SPACE = [" ","\t"]
DIGIT = string.digits
SPECIAL_SYMBOLS = {'+':'PLUS','-':'MINUS','*':"TIMES",'/':'DIV','<':'LT','=':'EQ','(':'LPARAM',')':'RPARAM',';':'SEMI'}
LETTER = string.ascii_letters
REVERSED_WORDS = {'if':'IF','then':'THEN','else':'ELSE','end':'END','repeat':'REPEAT',
                  'until':'UNTIL','read':'READ','write':'WRITE'}

line = 0
def getToken():
    global line
    srcfile = open("sample.tny","r")
    srclines = srcfile.readlines()
    # print(srclines)
    srcfile.close()

    cur_line = 0

    state = 'START'
    token_type = ""
    token_value = ""
    for line in srclines:
        cur_index = -1
        cur_line += 1
        print(str(cur_line)+":",end="")
        print(line)
        while True:
            if state == 'START':
                if line[cur_index+1] == '\n':
                    break
                if line[cur_index+1] == '{':
                    cur_index += 1
                    state = 'IN_COMMENT'
                elif line[cur_index+1] in WHILE_SPACE:
                    cur_index +=1
                elif line[cur_index+1] in DIGIT:
                    cur_index +=1
                    state = 'IN_NUM'
                    token_type = 'NUM'
                    token_value += line[cur_index]
                elif line[cur_index+1] == ':':
                    cur_index +=1
                    state = 'IN_ASSIGN'
                    token_value += line[cur_index]
                elif line[cur_index+1] in SPECIAL_SYMBOLS.keys():
                    cur_index +=1
                    token_type = SPECIAL_SYMBOLS[line[cur_index]]
                    state = 'DONE'
                    token_value += line[cur_index]
                elif line[cur_index+1] in LETTER:
                    cur_index +=1
                    token_type = 'ID'
                    state = 'IN_ID'
                    token_value += line[cur_index]
            elif state == 'IN_COMMENT':
                if line[cur_index+1] == '}':
                    cur_index += 1
                    state = 'START'
                elif line[cur_index+1] == '\n':
                    break
                else:
                    cur_index += 1

            elif state == 'IN_NUM':
                if line[cur_index+1] in DIGIT:
                    cur_index += 1
                    state = 'IN_NUM'
                    token_value += line[cur_index]
                elif line[cur_index+1] not in DIGIT:
                    state = 'DONE'

            elif state == 'IN_ID':
                if line[cur_index+1] in LETTER:
                    cur_index +=1
                    state = 'IN_ID'
                    token_value += line[cur_index]
                else:
                    if token_value in REVERSED_WORDS.keys():
                        token_type = REVERSED_WORDS[token_value]
                    state = 'DONE'
            elif state == 'IN_ASSIGN':
                if line[cur_index+1] =='=':
                    cur_index +=1
                    token_value += line[cur_index]
                    token_type = 'ASSIGN'
                    state = 'DONE'
                else:
                    state = 'ERROR'
            if state == 'DONE':
                print(str(cur_line)+":",end="")
                print(token_type + ':' + token_value)
                yield token_type, token_value
                token_type = ''
                token_value = ''
                state = 'START'
                if line[cur_index+1] == '\n':
                    break

            if state == 'ERROR':
                print("ERROR:"+ str(cur_line)+','+str(cur_index))
                yield 'ERROR', 0
                break
    yield 'ENDFILE',0
