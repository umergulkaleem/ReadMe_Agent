import ast
import zipfile
import io

def extract_py_files(uploaded_files):
    files = {}
    for file in uploaded_files:
        if file.name.endswith('.zip'):
            with zipfile.ZipFile(io.BytesIO(file.read())) as z:
                for fname in z.namelist():
                    if fname.endswith('.py'):
                        files[fname] = z.read(fname).decode('utf-8')
        elif file.name.endswith('.py'):
            files[file.name] = file.read().decode('utf-8')
    return files

def parse_files(uploaded_files):
    files = extract_py_files(uploaded_files)
    analysis = {}
    for fname, code in files.items():
        try:
            tree = ast.parse(code)
            functions = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
            classes = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
            imports = [n.names[0].name for n in ast.walk(tree) if isinstance(n, ast.Import)]
            docstrings = ast.get_docstring(tree)
            analysis[fname] = {
                "functions": functions,
                "classes": classes,
                "imports": imports,
                "docstring": docstrings,
                "code": code
            }
        except Exception as e:
            analysis[fname] = {"error": str(e), "code": code}
    return analysis

def analyze_file(file_path, content):
    return {'type': 'text', 'size': len(content)}