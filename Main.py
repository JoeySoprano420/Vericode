# main.py
from lexer import Lexer

source_code = '''
init count = 10
check count > 0 {
    make process() {
        await process()
    }
}
'''

lexer = Lexer(source_code)
token = lexer.next_token()
while token.type != TokenType.EOF:
    print(token)
    token = lexer.next_token()
