import ast
import os
import time
import sys

class CodeAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        with open(file_path, 'r') as file:
            self.content = file.read()
        self.tree = ast.parse(self.content)

    def analyze(self):
        return {
            'performance': self.analyze_performance(),
            'efficiency': self.analyze_efficiency(),
            'consistency': self.analyze_consistency(),
            'usability': self.analyze_usability()
        }

    def analyze_performance(self):
        score = 100
        for node in ast.walk(self.tree):
            if isinstance(node, ast.For):
                # Check for list comprehensions that could replace for loops
                score -= 5
            elif isinstance(node, ast.ListComp):
                score += 5
            elif isinstance(node, ast.Global):
                # Global variables can slow down performance
                score -= 10
        return max(0, score)

    def analyze_efficiency(self):
        score = 100
        function_complexities = {}
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                complexity = self.calculate_cyclomatic_complexity(node)
                function_complexities[node.name] = complexity
                if complexity > 10:
                    score -= 10
                elif complexity > 5:
                    score -= 5
        return max(0, score)

    def analyze_consistency(self):
        score = 100
        naming_conventions = {
            'camel_case': 0,
            'snake_case': 0,
            'pascal_case': 0
        }
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Name)):
                name = node.name if hasattr(node, 'name') else node.id
                if self.is_camel_case(name):
                    naming_conventions['camel_case'] += 1
                elif self.is_snake_case(name):
                    naming_conventions['snake_case'] += 1
                elif self.is_pascal_case(name):
                    naming_conventions['pascal_case'] += 1
        
        # Check if one naming convention is predominantly used
        total = sum(naming_conventions.values())
        if total > 0:
            consistency = max(naming_conventions.values()) / total
            score = int(consistency * 100)
        return score

    def analyze_usability(self):
        score = 100
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                if not ast.get_docstring(node):
                    # Deduct points for functions without docstrings
                    score -= 10
                if len(node.args.args) > 5:
                    # Deduct points for functions with too many parameters
                    score -= 5
        return max(0, score)

    @staticmethod
    def calculate_cyclomatic_complexity(node):
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.Assert)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, ast.BoolOp) and isinstance(child.op, ast.And):
                complexity += len(child.values) - 1
        return complexity

    @staticmethod
    def is_camel_case(s):
        return s != s.lower() and s != s.upper() and "_" not in s and s[0].islower()

    @staticmethod
    def is_snake_case(s):
        return s == s.lower() and "_" in s and not s.startswith("_")

    @staticmethod
    def is_pascal_case(s):
        return s != s.lower() and s != s.upper() and "_" not in s and s[0].isupper()
def __init__(self, file_path):
    self.file_path = file_path
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            self.content = file.read()
    except UnicodeDecodeError:
        # If UTF-8 fails, try with 'latin-1' which can read all 8-bit encodings
        with open(file_path, 'r', encoding='latin-1') as file:
            self.content = file.read()
    self.tree = ast.parse(self.content)mp
def main():
    if len(sys.argv) < 2:
        print("Usage: python script_analyzer.py <path_to_python_script>")
        sys.exit(1)

    script_path = sys.argv[1]
    if not os.path.exists(script_path):
        print(f"File not found: {script_path}")
        sys.exit(1)

    analyzer = CodeAnalyzer(script_path)
    results = analyzer.analyze()

    print(f"Analysis results for {script_path}:")
    for key, value in results.items():
        print(f"{key.capitalize()}: {value}/100")

if __name__ == "__main__":
    CodeAnalyzer('C:\\Users\\Zack\\OneDrive\\Desktop\\LinkedIn Meeting Assistant\\my_telegram_bot\\telegram_bot.py')
    main()