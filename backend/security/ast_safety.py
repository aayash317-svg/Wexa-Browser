import ast
from typing import Tuple, List

class ASTCodeSafetyAnalyzer:
    """
    Statically analyzes generated Python code using the Abstract Syntax Tree (AST)
    to block harmful operations (shell commands, network calls, filesystem destruction)
    BEFORE code is executed in the sandbox or proposed to the user.
    """

    # Modules that are completely prohibited in practice code
    FORBIDDEN_IMPORTS = {
        "os", "subprocess", "shutil", "socket", "urllib", "requests",
        "httpx", "aiohttp", "ctypes", "pty", "posix", "winreg",
        "sys.modules", "_posixsubprocess", "webbrowser"
    }

    # Built-in functions that allow arbitrary execution
    FORBIDDEN_CALLS = {
        "eval", "exec", "__import__", "compile", "breakpoint"
    }

    # Sensitive attributes that could indicate sandbox escape attempts
    FORBIDDEN_ATTRS = {
        "__subclasses__", "__bases__", "__globals__", "__builtins__",
        "__code__", "__reduce__"
    }

    @classmethod
    def analyze_python_code(cls, code_string: str) -> Tuple[bool, str]:
        """
        Parses and inspects code. Returns (is_safe, violation_reason).
        """
        if not code_string.strip():
            return True, "Empty code."

        try:
            tree = ast.parse(code_string)
        except SyntaxError as e:
            return False, f"Syntax error prevents AST safety check: {e}"

        for node in ast.walk(tree):
            # 1. Check imports: import os, from os import system
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root_pkg = alias.name.split(".")[0]
                    if root_pkg in cls.FORBIDDEN_IMPORTS or alias.name in cls.FORBIDDEN_IMPORTS:
                        return False, f"Forbidden import detected: '{alias.name}'"

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    root_pkg = node.module.split(".")[0]
                    if root_pkg in cls.FORBIDDEN_IMPORTS or node.module in cls.FORBIDDEN_IMPORTS:
                        return False, f"Forbidden from-import detected: '{node.module}'"

            # 2. Check dangerous function calls: eval(), exec(), etc.
            elif isinstance(node, ast.Call):
                func_name = None
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    func_name = node.func.attr

                if func_name in cls.FORBIDDEN_CALLS:
                    return False, f"Forbidden function call detected: '{func_name}()'"

            # 3. Check dangerous attribute access (__subclasses__, __globals__)
            elif isinstance(node, ast.Attribute):
                if node.attr in cls.FORBIDDEN_ATTRS:
                    return False, f"Forbidden attribute access detected: '{node.attr}'"

        return True, "Code passed all static AST safety checks."
