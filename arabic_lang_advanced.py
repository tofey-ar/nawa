#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
لغة البرمجة العربية - النسخة المتقدمة
Arabic Programming Language - Advanced Version
دعم كامل للمواقع، التطبيقات، قواعد البيانات، والواجهات
"""

import re
import sys
import os
import json
import sqlite3
import hashlib
from datetime import datetime
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union, Callable
from functools import wraps

# ============================================================================
# الكلمات المفتاحية (Keywords)
# ============================================================================

KEYWORDS = {
    # Basic
    'اطبع': 'PRINT',
    'اطبع_سطر': 'PRINTLN',
    'متغير': 'VAR',
    'ثابت': 'CONST',
    'اذا': 'IF',
    'والا': 'ELSE',
    'بينما': 'WHILE',
    'لكل': 'FOR',
    'في': 'IN',
    'دالة': 'FUNCTION',
    'ارجع': 'RETURN',
    'كسر': 'BREAK',
    'استمر': 'CONTINUE',
    'صحيح': 'TRUE',
    'خطأ': 'FALSE',
    'او': 'OR',
    'و': 'AND',
    'ليس': 'NOT',
    'فارغ': 'NULL',
    
    # Types
    'نص': 'STRING_TYPE',
    'رقم': 'NUMBER_TYPE',
    'منطق': 'BOOLEAN',
    'كائن': 'OBJECT',
    'قائمة': 'LIST',
    
    # Advanced
    'جرب': 'TRY',
    'امسك': 'CATCH',
    'اخير': 'FINALLY',
    'استورد': 'IMPORT',
    'فئة': 'CLASS',
    'جديد': 'NEW',
    'هذا': 'THIS',
    'امتداد': 'EXTENDS',
    'واجهة': 'INTERFACE',
    
    # Web
    'موقع': 'WEBSITE',
    'صفحة': 'PAGE',
    'رابط': 'ROUTE',
    'طلب': 'REQUEST',
    'استجابة': 'RESPONSE',
    'هيئة': 'BODY',
    'رأس': 'HEADER',
    
    # Database
    'قاعدة': 'DATABASE',
    'جدول': 'TABLE',
    'سجل': 'RECORD',
    'احفظ': 'SAVE',
    'احذف': 'DELETE',
    'حدث': 'UPDATE',
    'اجلب': 'FETCH',
}

# ============================================================================
# أنواع الرموز (Token Types)
# ============================================================================

class TokenType(Enum):
    # Literals
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    ARABIC_IDENTIFIER = auto()
    
    # Basic Keywords
    PRINT = auto()
    PRINTLN = auto()
    VAR = auto()
    CONST = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    IN = auto()
    FUNCTION = auto()
    RETURN = auto()
    BREAK = auto()
    CONTINUE = auto()
    TRUE = auto()
    FALSE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    NULL = auto()
    
    # Types
    BOOLEAN = auto()
    STRING_TYPE = auto()
    NUMBER_TYPE = auto()
    OBJECT = auto()
    LIST = auto()
    
    # Advanced
    TRY = auto()
    CATCH = auto()
    FINALLY = auto()
    IMPORT = auto()
    CLASS = auto()
    NEW = auto()
    THIS = auto()
    EXTENDS = auto()
    INTERFACE = auto()
    
    # Web
    WEBSITE = auto()
    PAGE = auto()
    ROUTE = auto()
    REQUEST = auto()
    RESPONSE = auto()
    BODY = auto()
    HEADER = auto()
    
    # Database
    DATABASE = auto()
    TABLE = auto()
    RECORD = auto()
    SAVE = auto()
    DELETE = auto()
    UPDATE = auto()
    FETCH = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    POWER = auto()
    
    EQUALS = auto()
    PLUS_EQUALS = auto()
    MINUS_EQUALS = auto()
    MULTIPLY_EQUALS = auto()
    DIVIDE_EQUALS = auto()
    
    EQUAL_EQUAL = auto()
    NOT_EQUAL = auto()
    GREATER = auto()
    LESS = auto()
    GREATER_EQUAL = auto()
    LESS_EQUAL = auto()
    
    ARROW = auto()
    
    # Delimiters
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    COMMA = auto()
    COLON = auto()
    SEMICOLON = auto()
    DOT = auto()
    
    # Special
    EOF = auto()
    NEWLINE = auto()

# ============================================================================
# الرمز (Token)
# ============================================================================

@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, {self.line}, {self.column})"

# ============================================================================
# المحلل.lexical (Lexer)
# ============================================================================

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        
    def error(self, message: str):
        raise SyntaxError(f"خطأ في السطر {self.line}, العمود {self.column}: {message}")
    
    def peek(self, offset: int = 0) -> str:
        pos = self.pos + offset
        if pos >= len(self.source):
            return '\0'
        return self.source[pos]
    
    def advance(self) -> str:
        char = self.peek()
        self.pos += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char
    
    def skip_whitespace(self):
        while self.peek() in ' \t\r':
            self.advance()
    
    def skip_comment(self):
        if self.peek() == '/' and self.peek(1) == '/':
            while self.peek() != '\n' and self.peek() != '\0':
                self.advance()
        elif self.peek() == '/' and self.peek(1) == '*':
            self.advance()
            self.advance()
            while not (self.peek() == '*' and self.peek(1) == '/') and self.peek() != '\0':
                self.advance()
            if self.peek() != '\0':
                self.advance()
                self.advance()
    
    def read_string(self) -> Token:
        start_line = self.line
        start_col = self.column
        quote = self.advance()
        value = ""
        
        while self.peek() != quote and self.peek() != '\0':
            if self.peek() == '\\':
                self.advance()
                escape = self.advance()
                if escape == 'n':
                    value += '\n'
                elif escape == 't':
                    value += '\t'
                elif escape == '\\':
                    value += '\\'
                elif escape == quote:
                    value += quote
                else:
                    value += escape
            else:
                value += self.advance()
        
        if self.peek() == '\0':
            raise SyntaxError(f"خطأ: نص غير مغلق في السطر {start_line}")
        
        self.advance()
        return Token(TokenType.STRING, value, start_line, start_col)
    
    def read_number(self) -> Token:
        start_line = self.line
        start_col = self.column
        value = ""
        
        while self.peek().isdigit():
            value += self.advance()
        
        if self.peek() == '.' and self.peek(1).isdigit():
            value += self.advance()
            while self.peek().isdigit():
                value += self.advance()
            return Token(TokenType.NUMBER, float(value), start_line, start_col)
        
        return Token(TokenType.NUMBER, int(value), start_line, start_col)
    
    def read_identifier(self) -> Token:
        start_line = self.line
        start_col = self.column
        value = ""
        
        while self.peek().isalnum() or self.peek() == '_':
            value += self.advance()
        
        keyword_type = KEYWORDS.get(value)
        if keyword_type:
            token_type = getattr(TokenType, keyword_type)
        else:
            token_type = TokenType.ARABIC_IDENTIFIER
        return Token(token_type, value, start_line, start_col)
    
    def tokenize(self) -> List[Token]:
        tokens = []
        
        while self.peek() != '\0':
            self.skip_whitespace()
            self.skip_comment()
            
            if self.peek() == '\0':
                break
            
            start_line = self.line
            start_col = self.column
            char = self.peek()
            
            if char == '\n':
                self.advance()
                tokens.append(Token(TokenType.NEWLINE, '\n', start_line, start_col))
                continue
            
            if char in '"\'':
                tokens.append(self.read_string())
                continue
            
            if char.isdigit():
                tokens.append(self.read_number())
                continue
            
            if char.isalpha() or char == '_':
                tokens.append(self.read_identifier())
                continue
            
            self.advance()
            
            # Two-character operators
            two_char = char + self.peek()
            if two_char == '==':
                self.advance()
                tokens.append(Token(TokenType.EQUAL_EQUAL, '==', start_line, start_col))
            elif two_char == '!=':
                self.advance()
                tokens.append(Token(TokenType.NOT_EQUAL, '!=', start_line, start_col))
            elif two_char == '>=':
                self.advance()
                tokens.append(Token(TokenType.GREATER_EQUAL, '>=', start_line, start_col))
            elif two_char == '<=':
                self.advance()
                tokens.append(Token(TokenType.LESS_EQUAL, '<=', start_line, start_col))
            elif two_char == '&&':
                self.advance()
                tokens.append(Token(TokenType.AND, '&&', start_line, start_col))
            elif two_char == '||':
                self.advance()
                tokens.append(Token(TokenType.OR, '||', start_line, start_col))
            elif two_char == '=>':
                self.advance()
                tokens.append(Token(TokenType.ARROW, '=>', start_line, start_col))
            elif two_char == '+=':
                self.advance()
                tokens.append(Token(TokenType.PLUS_EQUALS, '+=', start_line, start_col))
            elif two_char == '-=':
                self.advance()
                tokens.append(Token(TokenType.MINUS_EQUALS, '-=', start_line, start_col))
            elif two_char == '*=':
                self.advance()
                tokens.append(Token(TokenType.MULTIPLY_EQUALS, '*=', start_line, start_col))
            elif two_char == '/=':
                self.advance()
                tokens.append(Token(TokenType.DIVIDE_EQUALS, '/=', start_line, start_col))
            elif two_char == '**':
                self.advance()
                tokens.append(Token(TokenType.POWER, '**', start_line, start_col))
            # Single-character operators
            elif char == '+':
                tokens.append(Token(TokenType.PLUS, '+', start_line, start_col))
            elif char == '-':
                tokens.append(Token(TokenType.MINUS, '-', start_line, start_col))
            elif char == '*':
                tokens.append(Token(TokenType.MULTIPLY, '*', start_line, start_col))
            elif char == '/':
                tokens.append(Token(TokenType.DIVIDE, '/', start_line, start_col))
            elif char == '%':
                tokens.append(Token(TokenType.MODULO, '%', start_line, start_col))
            elif char == '=':
                tokens.append(Token(TokenType.EQUALS, '=', start_line, start_col))
            elif char == '>':
                tokens.append(Token(TokenType.GREATER, '>', start_line, start_col))
            elif char == '<':
                tokens.append(Token(TokenType.LESS, '<', start_line, start_col))
            elif char == '(':
                tokens.append(Token(TokenType.LEFT_PAREN, '(', start_line, start_col))
            elif char == ')':
                tokens.append(Token(TokenType.RIGHT_PAREN, ')', start_line, start_col))
            elif char == '{':
                tokens.append(Token(TokenType.LEFT_BRACE, '{', start_line, start_col))
            elif char == '}':
                tokens.append(Token(TokenType.RIGHT_BRACE, '}', start_line, start_col))
            elif char == '[':
                tokens.append(Token(TokenType.LEFT_BRACKET, '[', start_line, start_col))
            elif char == ']':
                tokens.append(Token(TokenType.RIGHT_BRACKET, ']', start_line, start_col))
            elif char == ',':
                tokens.append(Token(TokenType.COMMA, ',', start_line, start_col))
            elif char == ':':
                tokens.append(Token(TokenType.COLON, ':', start_line, start_col))
            elif char == ';':
                tokens.append(Token(TokenType.SEMICOLON, ';', start_line, start_col))
            elif char == '.':
                tokens.append(Token(TokenType.DOT, '.', start_line, start_col))
            else:
                self.error(f"رمز غير معروف: {char}")
        
        tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return tokens

# ============================================================================
# المكتبات المتقدمة (Advanced Libraries)
# ============================================================================

class WebServer:
    """خادم ويب بسيط"""
    
    def __init__(self, port=8080):
        self.port = port
        self.routes = {}
        self.static_dir = './static'
        
    def route(self, path):
        def decorator(func):
            self.routes[path] = func
            return func
        return decorator
    
    def html(self, content):
        return {
            'type': 'html',
            'content': content,
            'headers': {'Content-Type': 'text/html; charset=utf-8'}
        }
    
    def json_response(self, data):
        return {
            'type': 'json',
            'content': json.dumps(data, ensure_ascii=False),
            'headers': {'Content-Type': 'application/json; charset=utf-8'}
        }
    
    def redirect(self, url):
        return {
            'type': 'redirect',
            'url': url,
            'headers': {'Location': url}
        }
    
    def serve(self):
        from http.server import HTTPServer, BaseHTTPRequestHandler
        
        server = self
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                path = self.path.split('?')[0]
                
                if path in server.routes:
                    result = server.routes[path]()
                    if isinstance(result, dict):
                        content = result['content']
                        headers = result.get('headers', {})
                    else:
                        content = str(result)
                        headers = {'Content-Type': 'text/html; charset=utf-8'}
                    
                    self.send_response(200)
                    for key, value in headers.items():
                        self.send_header(key, value)
                    self.end_headers()
                    self.wfile.write(content.encode('utf-8'))
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b'404 - Page Not Found')
            
            def do_POST(self):
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length).decode('utf-8')
                
                path = self.path.split('?')[0]
                if path in server.routes:
                    result = server.routes[path](body)
                    if isinstance(result, dict):
                        content = result['content']
                        headers = result.get('headers', {})
                    else:
                        content = str(result)
                        headers = {'Content-Type': 'text/html; charset=utf-8'}
                    
                    self.send_response(200)
                    for key, value in headers.items():
                        self.send_header(key, value)
                    self.end_headers()
                    self.wfile.write(content.encode('utf-8'))
                else:
                    self.send_response(404)
                    self.end_headers()
            
            def log_message(self, format, *args):
                print(f"[Web] {args[0]}")
        
        httpd = HTTPServer(('localhost', self.port), Handler)
        print(f"🌐 الخادم يعمل على http://localhost:{self.port}")
        print("اضغط Ctrl+C للإيقاف")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nإيقاف الخادم...")
            httpd.shutdown()

class Database:
    """قاعدة بيانات SQLite"""
    
    def __init__(self, name='app.db'):
        self.name = name
        self.conn = sqlite3.connect(name, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
    
    def create_table(self, table_name, columns):
        cols = ', '.join([f"{k} {v}" for k, v in columns.items()])
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({cols})"
        self.cursor.execute(sql)
        self.conn.commit()
    
    def insert(self, table_name, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(sql, list(data.values()))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def select(self, table_name, where=None, params=None):
        sql = f"SELECT * FROM {table_name}"
        if where:
            sql += f" WHERE {where}"
        self.cursor.execute(sql, params or [])
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    
    def update(self, table_name, data, where, params=None):
        set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {where}"
        self.cursor.execute(sql, list(data.values()) + (params or []))
        self.conn.commit()
        return self.cursor.rowcount
    
    def delete(self, table_name, where, params=None):
        sql = f"DELETE FROM {table_name} WHERE {where}"
        self.cursor.execute(sql, params or [])
        self.conn.commit()
        return self.cursor.rowcount
    
    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or [])
        self.conn.commit()
        return self.cursor.fetchall()
    
    def نفذ(self, sql, params=None):
        """Alias for execute with Arabic name"""
        return self.execute(sql, params)
    
    def close(self):
        self.conn.close()

class FileSystem:
    """نظام الملفات"""
    
    @staticmethod
    def read_file(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    
    @staticmethod
    def write_file(path, content):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    @staticmethod
    def append_file(path, content):
        with open(path, 'a', encoding='utf-8') as f:
            f.write(content)
    
    @staticmethod
    def exists(path):
        return os.path.exists(path)
    
    @staticmethod
    def is_file(path):
        return os.path.isfile(path)
    
    @staticmethod
    def is_dir(path):
        return os.path.isdir(path)
    
    @staticmethod
    def list_dir(path='.'):
        return os.listdir(path)
    
    @staticmethod
    def make_dir(path):
        os.makedirs(path, exist_ok=True)
    
    @staticmethod
    def remove(path):
        if os.path.isfile(path):
            os.remove(path)
        else:
            import shutil
            shutil.rmtree(path)
    
    @staticmethod
    def copy(src, dst):
        import shutil
        shutil.copy2(src, dst)
    
    @staticmethod
    def move(src, dst):
        import shutil
        shutil.move(src, dst)

class HTTPClient:
    """عميل HTTP"""
    
    @staticmethod
    def get(url):
        import urllib.request
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                return {
                    'status': 200,
                    'body': response.read().decode('utf-8'),
                    'headers': dict(response.headers)
                }
        except Exception as e:
            return {'status': 500, 'error': str(e)}
    
    @staticmethod
    def post(url, data, headers=None):
        import urllib.request
        try:
            data_bytes = json.dumps(data).encode('utf-8')
            req = urllib.request.Request(url, data=data_bytes, method='POST')
            req.add_header('Content-Type', 'application/json')
            if headers:
                for key, value in headers.items():
                    req.add_header(key, value)
            with urllib.request.urlopen(req, timeout=10) as response:
                return {
                    'status': 200,
                    'body': response.read().decode('utf-8'),
                    'headers': dict(response.headers)
                }
        except Exception as e:
            return {'status': 500, 'error': str(e)}

class Crypto:
    """التشفير والهاش"""
    
    @staticmethod
    def md5(text):
        return hashlib.md5(text.encode()).hexdigest()
    
    @staticmethod
    def sha256(text):
        return hashlib.sha256(text.encode()).hexdigest()
    
    @staticmethod
    def sha512(text):
        return hashlib.sha512(text.encode()).hexdigest()

# ============================================================================
# المكتبة القياسية (Standard Library)
# ============================================================================

STANDARD_LIBRARY = {
    # Basic
    'طول': lambda x: len(x),
    'نص_الى_رقم': lambda x: float(x) if '.' in str(x) else int(x),
    'رقم_الى_نص': str,
    'نوع': lambda x: type(x).__name__,
    'مدى': lambda *args: list(range(*args)),
    'مطلق': abs,
    'تقريب': round,
    'اقصى': max,
    'ادنى': min,
    'مجموع': sum,
    'فرز': sorted,
    'عكس': lambda x: list(reversed(x)) if isinstance(x, list) else -x,
    
    # Web
    'خادم_ويب': lambda port=8080: WebServer(port),
    'html': lambda content: {'type': 'html', 'content': content},
    'رد_جسون': lambda data: {'type': 'json', 'content': json.dumps(data, ensure_ascii=False)},
    
    # Database
    'قاعدة_بيانات': lambda name='app.db': Database(name),
    
    # File System
    'اقرا_ملف': FileSystem.read_file,
    'اكتب_ملف': FileSystem.write_file,
    'الصق_ملف': FileSystem.append_file,
    'ملف_موجود': FileSystem.exists,
    'مجلد_موجود': FileSystem.exists,
    'قائمة_ملفات': FileSystem.list_dir,
    'انشئ_مجلد': FileSystem.make_dir,
    'احذف_ملف': FileSystem.remove,
    'احذف_مجلد': FileSystem.remove,
    'احذف': FileSystem.remove,
    'انسخ': FileSystem.copy,
    'انقل': FileSystem.move,
    
    # HTTP
    'http_جلب': HTTPClient.get,
    'http_ارسل': HTTPClient.post,
    
    # Crypto
    'هاش_مد5': Crypto.md5,
    'هاش_شا256': Crypto.sha256,
    'هاش_شا512': Crypto.sha512,
    
    # JSON
    'من_جسون': json.loads,
    'الى_جسون': lambda data: json.dumps(data, ensure_ascii=False),
    
    # Time
    'وقت_الآن': lambda: datetime.now().isoformat(),
    'تاريخ_الآن': lambda: datetime.now().strftime('%Y-%m-%d'),
    
    # System
    'نظام': os.name,
    'مسار_عمل': os.getcwd,
    'تغيير_مسار': os.chdir,
}

# ============================================================================
# العقد (AST Nodes) - نفس العقد السابقة
# ============================================================================

@dataclass
class ASTNode:
    pass

@dataclass
class NumberNode(ASTNode):
    value: Union[int, float]

@dataclass
class StringNode(ASTNode):
    value: str

@dataclass
class BooleanNode(ASTNode):
    value: bool

@dataclass
class NullNode(ASTNode):
    pass

@dataclass
class IdentifierNode(ASTNode):
    name: str

@dataclass
class BinaryOpNode(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode

@dataclass
class UnaryOpNode(ASTNode):
    operator: str
    operand: ASTNode

@dataclass
class AssignNode(ASTNode):
    name: str
    value: ASTNode

@dataclass
class VarDeclNode(ASTNode):
    name: str
    value: Optional[ASTNode] = None
    is_const: bool = False

@dataclass
class PrintNode(ASTNode):
    value: ASTNode
    newline: bool = True

@dataclass
class IfNode(ASTNode):
    condition: ASTNode
    then_block: List[ASTNode]
    else_block: Optional[List[ASTNode]] = None

@dataclass
class WhileNode(ASTNode):
    condition: ASTNode
    body: List[ASTNode]

@dataclass
class ForNode(ASTNode):
    variable: str
    iterable: ASTNode
    body: List[ASTNode]

@dataclass
class FunctionDefNode(ASTNode):
    name: str
    params: List[str]
    body: List[ASTNode]

@dataclass
class CallNode(ASTNode):
    function: ASTNode
    arguments: List[ASTNode]

@dataclass
class ReturnNode(ASTNode):
    value: Optional[ASTNode] = None

@dataclass
class BreakNode(ASTNode):
    pass

@dataclass
class ContinueNode(ASTNode):
    pass

@dataclass
class ListNode(ASTNode):
    elements: List[ASTNode]

@dataclass
class IndexNode(ASTNode):
    collection: ASTNode
    index: ASTNode

@dataclass
class ObjectNode(ASTNode):
    properties: Dict[str, ASTNode]

@dataclass
class PropertyAccessNode(ASTNode):
    object: ASTNode
    property: str

@dataclass
class ProgramNode(ASTNode):
    statements: List[ASTNode]

# ============================================================================
# المحلل النحوي (Parser)
# ============================================================================

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def current(self) -> Token:
        if self.pos >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[self.pos]
    
    def peek(self, offset: int = 0) -> Token:
        pos = self.pos + offset
        if pos >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[pos]
    
    def advance(self) -> Token:
        token = self.current()
        self.pos += 1
        return token
    
    def expect(self, token_type: TokenType) -> Token:
        if self.current().type != token_type:
            raise SyntaxError(f"خطأ: متوقع {token_type} لكن وجد {self.current().type} في السطر {self.current().line}")
        return self.advance()
    
    def match(self, *token_types: TokenType) -> bool:
        return self.current().type in token_types
    
    def skip_newlines(self):
        while self.match(TokenType.NEWLINE):
            self.advance()
    
    def parse(self) -> ProgramNode:
        statements = []
        self.skip_newlines()
        
        while not self.match(TokenType.EOF):
            statements.append(self.parse_statement())
            self.skip_newlines()
        
        return ProgramNode(statements)
    
    def parse_statement(self) -> ASTNode:
        self.skip_newlines()
        
        if self.match(TokenType.PRINT):
            return self.parse_print()
        elif self.match(TokenType.PRINTLN):
            return self.parse_println()
        elif self.match(TokenType.VAR):
            return self.parse_var_decl()
        elif self.match(TokenType.CONST):
            return self.parse_const_decl()
        elif self.match(TokenType.IF):
            return self.parse_if()
        elif self.match(TokenType.WHILE):
            return self.parse_while()
        elif self.match(TokenType.FOR):
            return self.parse_for()
        elif self.match(TokenType.FUNCTION):
            return self.parse_function()
        elif self.match(TokenType.RETURN):
            return self.parse_return()
        elif self.match(TokenType.BREAK):
            self.advance()
            return BreakNode()
        elif self.match(TokenType.CONTINUE):
            self.advance()
            return ContinueNode()
        else:
            return self.parse_expression_statement()
    
    def parse_print(self) -> PrintNode:
        self.advance()
        self.skip_newlines()
        value = self.parse_expression()
        return PrintNode(value, newline=False)
    
    def parse_println(self) -> PrintNode:
        self.advance()
        self.skip_newlines()
        value = self.parse_expression()
        return PrintNode(value, newline=True)
    
    def parse_var_decl(self) -> VarDeclNode:
        self.advance()
        self.skip_newlines()
        name = self.expect(TokenType.ARABIC_IDENTIFIER).value
        self.skip_newlines()
        
        value = None
        if self.match(TokenType.EQUALS):
            self.advance()
            self.skip_newlines()
            value = self.parse_expression()
        
        return VarDeclNode(name, value, is_const=False)
    
    def parse_const_decl(self) -> VarDeclNode:
        self.advance()
        self.skip_newlines()
        name = self.expect(TokenType.ARABIC_IDENTIFIER).value
        self.skip_newlines()
        
        self.expect(TokenType.EQUALS)
        self.skip_newlines()
        value = self.parse_expression()
        
        return VarDeclNode(name, value, is_const=True)
    
    def parse_if(self) -> IfNode:
        self.advance()
        self.skip_newlines()
        condition = self.parse_expression()
        self.skip_newlines()
        
        self.expect(TokenType.LEFT_BRACE)
        self.skip_newlines()
        then_block = []
        while not self.match(TokenType.RIGHT_BRACE):
            then_block.append(self.parse_statement())
            self.skip_newlines()
        self.expect(TokenType.RIGHT_BRACE)
        
        self.skip_newlines()
        else_block = None
        
        if self.match(TokenType.ELSE):
            self.advance()
            self.skip_newlines()
            
            if self.match(TokenType.IF):
                else_block = [self.parse_if()]
            else:
                self.expect(TokenType.LEFT_BRACE)
                self.skip_newlines()
                else_block = []
                while not self.match(TokenType.RIGHT_BRACE):
                    else_block.append(self.parse_statement())
                    self.skip_newlines()
                self.expect(TokenType.RIGHT_BRACE)
        
        return IfNode(condition, then_block, else_block)
    
    def parse_while(self) -> WhileNode:
        self.advance()
        self.skip_newlines()
        condition = self.parse_expression()
        self.skip_newlines()
        
        self.expect(TokenType.LEFT_BRACE)
        self.skip_newlines()
        body = []
        while not self.match(TokenType.RIGHT_BRACE):
            body.append(self.parse_statement())
            self.skip_newlines()
        self.expect(TokenType.RIGHT_BRACE)
        
        return WhileNode(condition, body)
    
    def parse_for(self) -> ForNode:
        self.advance()
        self.skip_newlines()
        variable = self.expect(TokenType.ARABIC_IDENTIFIER).value
        self.skip_newlines()
        self.expect(TokenType.IN)
        self.skip_newlines()
        iterable = self.parse_expression()
        self.skip_newlines()
        
        self.expect(TokenType.LEFT_BRACE)
        self.skip_newlines()
        body = []
        while not self.match(TokenType.RIGHT_BRACE):
            body.append(self.parse_statement())
            self.skip_newlines()
        self.expect(TokenType.RIGHT_BRACE)
        
        return ForNode(variable, iterable, body)
    
    def parse_function(self) -> FunctionDefNode:
        self.advance()
        self.skip_newlines()
        name = self.expect(TokenType.ARABIC_IDENTIFIER).value
        self.skip_newlines()
        
        self.expect(TokenType.LEFT_PAREN)
        params = []
        self.skip_newlines()
        
        while not self.match(TokenType.RIGHT_PAREN):
            param = self.expect(TokenType.ARABIC_IDENTIFIER).value
            params.append(param)
            self.skip_newlines()
            if self.match(TokenType.COMMA):
                self.advance()
                self.skip_newlines()
        
        self.expect(TokenType.RIGHT_PAREN)
        self.skip_newlines()
        
        self.expect(TokenType.LEFT_BRACE)
        self.skip_newlines()
        body = []
        while not self.match(TokenType.RIGHT_BRACE):
            body.append(self.parse_statement())
            self.skip_newlines()
        self.expect(TokenType.RIGHT_BRACE)
        
        return FunctionDefNode(name, params, body)
    
    def parse_return(self) -> ReturnNode:
        self.advance()
        self.skip_newlines()
        
        value = None
        if not self.match(TokenType.NEWLINE, TokenType.RIGHT_BRACE, TokenType.EOF):
            value = self.parse_expression()
        
        return ReturnNode(value)
    
    def parse_expression_statement(self) -> ASTNode:
        if self.match(TokenType.ARABIC_IDENTIFIER) and self.peek(1).type == TokenType.EQUALS:
            name = self.advance().value
            self.advance()
            self.skip_newlines()
            value = self.parse_expression()
            return AssignNode(name, value)
        
        expr = self.parse_expression()
        return expr
    
    def parse_expression(self) -> ASTNode:
        return self.parse_or()
    
    def parse_or(self) -> ASTNode:
        left = self.parse_and()
        
        while self.match(TokenType.OR):
            op = self.advance().value
            right = self.parse_and()
            left = BinaryOpNode(left, op, right)
        
        return left
    
    def parse_and(self) -> ASTNode:
        left = self.parse_equality()
        
        while self.match(TokenType.AND):
            op = self.advance().value
            right = self.parse_equality()
            left = BinaryOpNode(left, op, right)
        
        return left
    
    def parse_equality(self) -> ASTNode:
        left = self.parse_comparison()
        
        while self.match(TokenType.EQUAL_EQUAL, TokenType.NOT_EQUAL):
            op = self.advance().value
            right = self.parse_comparison()
            left = BinaryOpNode(left, op, right)
        
        return left
    
    def parse_comparison(self) -> ASTNode:
        left = self.parse_term()
        
        while self.match(TokenType.GREATER, TokenType.LESS, TokenType.GREATER_EQUAL, TokenType.LESS_EQUAL):
            op = self.advance().value
            right = self.parse_term()
            left = BinaryOpNode(left, op, right)
        
        return left
    
    def parse_term(self) -> ASTNode:
        left = self.parse_factor()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.advance().value
            right = self.parse_factor()
            left = BinaryOpNode(left, op, right)
        
        return left
    
    def parse_factor(self) -> ASTNode:
        left = self.parse_power()
        
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op = self.advance().value
            right = self.parse_power()
            left = BinaryOpNode(left, op, right)
        
        return left
    
    def parse_power(self) -> ASTNode:
        left = self.parse_unary()
        
        if self.match(TokenType.POWER):
            op = self.advance().value
            right = self.parse_power()
            return BinaryOpNode(left, op, right)
        
        return left
    
    def parse_unary(self) -> ASTNode:
        if self.match(TokenType.MINUS, TokenType.NOT):
            op = self.advance().value
            operand = self.parse_unary()
            return UnaryOpNode(op, operand)
        
        return self.parse_primary()
    
    def parse_primary(self) -> ASTNode:
        if self.match(TokenType.NUMBER):
            return NumberNode(self.advance().value)
        
        if self.match(TokenType.STRING):
            return StringNode(self.advance().value)
        
        if self.match(TokenType.TRUE):
            self.advance()
            return BooleanNode(True)
        
        if self.match(TokenType.FALSE):
            self.advance()
            return BooleanNode(False)
        
        if self.match(TokenType.NULL):
            self.advance()
            return NullNode()
        
        if self.match(TokenType.ARABIC_IDENTIFIER):
            name = self.advance().value
            
            # Property access
            if self.match(TokenType.DOT):
                self.advance()
                prop = self.expect(TokenType.ARABIC_IDENTIFIER).value
                return PropertyAccessNode(IdentifierNode(name), prop)
            
            # Function call
            if self.match(TokenType.LEFT_PAREN):
                self.advance()
                args = []
                self.skip_newlines()
                
                while not self.match(TokenType.RIGHT_PAREN):
                    args.append(self.parse_expression())
                    self.skip_newlines()
                    if self.match(TokenType.COMMA):
                        self.advance()
                        self.skip_newlines()
                
                self.expect(TokenType.RIGHT_PAREN)
                return CallNode(IdentifierNode(name), args)
            
            # Array indexing
            if self.match(TokenType.LEFT_BRACKET):
                self.advance()
                index = self.parse_expression()
                self.expect(TokenType.RIGHT_BRACKET)
                return IndexNode(IdentifierNode(name), index)
            
            return IdentifierNode(name)
        
        if self.match(TokenType.LEFT_PAREN):
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RIGHT_PAREN)
            return expr
        
        if self.match(TokenType.LEFT_BRACKET):
            self.advance()
            elements = []
            self.skip_newlines()
            
            while not self.match(TokenType.RIGHT_BRACKET):
                elements.append(self.parse_expression())
                self.skip_newlines()
                if self.match(TokenType.COMMA):
                    self.advance()
                    self.skip_newlines()
            
            self.expect(TokenType.RIGHT_BRACKET)
            return ListNode(elements)
        
        if self.match(TokenType.LEFT_BRACE):
            # Object literal
            self.advance()
            properties = {}
            self.skip_newlines()
            
            while not self.match(TokenType.RIGHT_BRACE):
                key = self.expect(TokenType.ARABIC_IDENTIFIER).value
                self.skip_newlines()
                self.expect(TokenType.COLON)
                self.skip_newlines()
                value = self.parse_expression()
                properties[key] = value
                self.skip_newlines()
                if self.match(TokenType.COMMA):
                    self.advance()
                    self.skip_newlines()
            
            self.expect(TokenType.RIGHT_BRACE)
            return ObjectNode(properties)
        
        raise SyntaxError(f"خطأ: تعبير غير متوقع في السطر {self.current().line}")

# ============================================================================
# المفسر (Interpreter)
# ============================================================================

class InterpreterError(Exception):
    pass

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass

class Interpreter:
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.constants: set = set()
        self.functions: Dict[str, FunctionDefNode] = {}
        self.builtins = STANDARD_LIBRARY.copy()
    
    def error(self, message: str, line: int = 0):
        raise InterpreterError(f"خطأ: {message}")
    
    def interpret(self, node: ASTNode) -> Any:
        if isinstance(node, ProgramNode):
            return self.execute_program(node)
        elif isinstance(node, NumberNode):
            return node.value
        elif isinstance(node, StringNode):
            return node.value
        elif isinstance(node, BooleanNode):
            return node.value
        elif isinstance(node, NullNode):
            return None
        elif isinstance(node, IdentifierNode):
            return self.evaluate_identifier(node)
        elif isinstance(node, BinaryOpNode):
            return self.evaluate_binary(node)
        elif isinstance(node, UnaryOpNode):
            return self.evaluate_unary(node)
        elif isinstance(node, AssignNode):
            return self.execute_assign(node)
        elif isinstance(node, VarDeclNode):
            return self.execute_var_decl(node)
        elif isinstance(node, PrintNode):
            return self.execute_print(node)
        elif isinstance(node, IfNode):
            return self.execute_if(node)
        elif isinstance(node, WhileNode):
            return self.execute_while(node)
        elif isinstance(node, ForNode):
            return self.execute_for(node)
        elif isinstance(node, FunctionDefNode):
            return self.execute_function_def(node)
        elif isinstance(node, CallNode):
            return self.execute_call(node)
        elif isinstance(node, ReturnNode):
            value = self.interpret(node.value) if node.value else None
            raise ReturnException(value)
        elif isinstance(node, BreakNode):
            raise BreakException()
        elif isinstance(node, ContinueNode):
            raise ContinueException()
        elif isinstance(node, ListNode):
            return [self.interpret(elem) for elem in node.elements]
        elif isinstance(node, ObjectNode):
            return {k: self.interpret(v) for k, v in node.properties.items()}
        elif isinstance(node, IndexNode):
            return self.evaluate_index(node)
        elif isinstance(node, PropertyAccessNode):
            return self.evaluate_property(node)
        else:
            self.error(f"عقدة غير معروفة: {type(node)}")
    
    def execute_program(self, node: ProgramNode) -> Any:
        result = None
        for stmt in node.statements:
            result = self.interpret(stmt)
        return result
    
    def evaluate_identifier(self, node: IdentifierNode) -> Any:
        name = node.name
        
        if name in self.variables:
            return self.variables[name]
        
        if name in self.builtins:
            return self.builtins[name]
        
        if name in self.functions:
            return self.functions[name]
        
        self.error(f"متغير غير معرف: {name}")
    
    def evaluate_binary(self, node: BinaryOpNode) -> Any:
        left = self.interpret(node.left)
        
        # Short-circuit evaluation
        if node.operator == 'او' or node.operator == '||':
            if left:
                return left
            return self.interpret(node.right)
        
        if node.operator == 'و' or node.operator == '&&':
            if not left:
                return left
            return self.interpret(node.right)
        
        right = self.interpret(node.right)
        
        if node.operator == '+':
            return left + right
        elif node.operator == '-':
            return left - right
        elif node.operator == '*':
            return left * right
        elif node.operator == '/':
            if right == 0:
                self.error("القسمة على صفر")
            return left / right
        elif node.operator == '%':
            return left % right
        elif node.operator == '**':
            return left ** right
        elif node.operator == '==':
            return left == right
        elif node.operator == '!=':
            return left != right
        elif node.operator == '>':
            return left > right
        elif node.operator == '<':
            return left < right
        elif node.operator == '>=':
            return left >= right
        elif node.operator == '<=':
            return left <= right
        else:
            self.error(f"معمل غير معروف: {node.operator}")
    
    def evaluate_unary(self, node: UnaryOpNode) -> Any:
        operand = self.interpret(node.operand)
        
        if node.operator == '-':
            return -operand
        elif node.operator == 'ليس' or node.operator == '!':
            return not operand
        else:
            self.error(f"معمل أحادي غير معروف: {node.operator}")
    
    def execute_assign(self, node: AssignNode) -> Any:
        if node.name in self.constants:
            self.error(f"لا يمكن تعديل الثابت: {node.name}")
        
        value = self.interpret(node.value)
        self.variables[node.name] = value
        return value
    
    def execute_var_decl(self, node: VarDeclNode) -> None:
        if node.name in self.variables or node.name in self.constants:
            self.error(f"متغير معرف مسبقاً: {node.name}")
        
        value = self.interpret(node.value) if node.value else None
        
        if node.is_const:
            self.constants.add(node.name)
        
        self.variables[node.name] = value
    
    def execute_print(self, node: PrintNode) -> None:
        value = self.interpret(node.value)
        if isinstance(value, (dict, list)):
            print(value)
        elif isinstance(value, bool):
            print('صحيح' if value else 'خطأ')
        elif value is None:
            print('فارغ')
        else:
            print(value, end='' if not node.newline else '\n')
        if node.newline:
            print()
    
    def execute_if(self, node: IfNode) -> None:
        condition = self.interpret(node.condition)
        
        if condition:
            for stmt in node.then_block:
                self.interpret(stmt)
        elif node.else_block:
            for stmt in node.else_block:
                self.interpret(stmt)
    
    def execute_while(self, node: WhileNode) -> None:
        while self.interpret(node.condition):
            try:
                for stmt in node.body:
                    self.interpret(stmt)
            except ContinueException:
                continue
            except BreakException:
                break
    
    def execute_for(self, node: ForNode) -> None:
        iterable = self.interpret(node.iterable)
        
        if isinstance(iterable, int):
            iterable = range(iterable)
        
        for item in iterable:
            try:
                self.variables[node.variable] = item
                for stmt in node.body:
                    self.interpret(stmt)
            except ContinueException:
                continue
            except BreakException:
                break
    
    def execute_function_def(self, node: FunctionDefNode) -> None:
        self.functions[node.name] = node
    
    def execute_call(self, node: CallNode) -> Any:
        func = self.interpret(node.function)
        args = [self.interpret(arg) for arg in node.arguments]
        
        # Built-in function
        if callable(func):
            return func(*args)
        
        # User-defined function
        if isinstance(func, FunctionDefNode):
            old_vars = self.variables.copy()
            
            for param, arg in zip(func.params, args):
                self.variables[param] = arg
            
            try:
                for stmt in func.body:
                    self.interpret(stmt)
                return None
            except ReturnException as e:
                return e.value
            finally:
                self.variables = old_vars
        
        self.error(f"الكائن ليس دالة قابلة للاستدعاء")
    
    def evaluate_index(self, node: IndexNode) -> Any:
        collection = self.interpret(node.collection)
        index = self.interpret(node.index)
        
        if isinstance(collection, (list, str, dict)):
            return collection[index]
        
        self.error(f"لا يمكن الفهرسة على {type(collection).__name__}")
    
    def evaluate_property(self, node: PropertyAccessNode) -> Any:
        obj = self.interpret(node.object)
        
        if isinstance(obj, dict):
            return obj.get(node.property)
        elif hasattr(obj, node.property):
            return getattr(obj, node.property)
        
        self.error(f"خاصية غير موجودة: {node.property}")

# ============================================================================
# البرنامج الرئيسي
# ============================================================================

def run_file(filename: str):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.interpret(ast)
    
    except FileNotFoundError:
        print(f"خطأ: الملف '{filename}' غير موجود")
        sys.exit(1)
    except Exception as e:
        print(f"خطأ: {e}")
        sys.exit(1)

def repl():
    interpreter = Interpreter()
    print("=== مترجم اللغة العربية - النسخة المتقدمة ===")
    print("اكتب 'خروج' للخروج\n")
    
    while True:
        try:
            source = input(">>> ")
            
            if source.strip() == 'خروج':
                break
            
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            
            parser = Parser(tokens)
            ast = parser.parse()
            
            result = interpreter.interpret(ast)
            
            if result is not None:
                print(result)
        
        except Exception as e:
            print(f"خطأ: {e}")

def main():
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        repl()

if __name__ == '__main__':
    main()
