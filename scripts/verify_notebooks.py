#!/usr/bin/env python3
"""
Notebook Verification Script for Crafting Custom Agents Workshop

Validates notebook structure and code syntax without executing cells
(which would require API keys).

Usage:
    python scripts/verify_notebooks.py

Checks:
1. Valid JSON structure
2. Required notebook metadata
3. Python syntax in code cells
4. Import statement availability
5. Markdown cell structure
"""

import ast
import json
import sys
from pathlib import Path
from typing import NamedTuple

# ANSI colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"


class VerificationResult(NamedTuple):
    """Result of a single verification check."""
    passed: bool
    message: str
    details: str = ""


def print_result(name: str, result: VerificationResult):
    """Print a verification result with color."""
    symbol = f"{GREEN}✓{RESET}" if result.passed else f"{RED}✗{RESET}"
    print(f"  {symbol} {name}: {result.message}")
    if result.details and not result.passed:
        for line in result.details.split("\n"):
            print(f"      {YELLOW}{line}{RESET}")


def verify_json_structure(notebook_path: Path) -> VerificationResult:
    """Verify the notebook is valid JSON."""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            json.load(f)
        return VerificationResult(True, "Valid JSON")
    except json.JSONDecodeError as e:
        return VerificationResult(False, "Invalid JSON", str(e))


def verify_notebook_metadata(notebook_path: Path) -> VerificationResult:
    """Verify required notebook metadata exists."""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    issues = []
    
    if 'cells' not in nb:
        issues.append("Missing 'cells' key")
    
    if 'metadata' not in nb:
        issues.append("Missing 'metadata' key")
    
    if 'nbformat' not in nb:
        issues.append("Missing 'nbformat' key")
    
    if issues:
        return VerificationResult(False, "Missing metadata", "\n".join(issues))
    
    return VerificationResult(True, f"Valid structure ({len(nb['cells'])} cells)")


def verify_code_syntax(notebook_path: Path) -> VerificationResult:
    """Verify Python syntax in all code cells."""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    errors = []
    code_cells = [c for c in nb.get('cells', []) if c.get('cell_type') == 'code']
    
    for i, cell in enumerate(code_cells):
        source = ''.join(cell.get('source', []))
        
        # Skip empty cells
        if not source.strip():
            continue
        
        # Skip cells that are just shell commands
        if source.strip().startswith('!') or source.strip().startswith('%'):
            continue
        
        try:
            ast.parse(source)
        except SyntaxError as e:
            errors.append(f"Cell {i+1}: {e.msg} (line {e.lineno})")
    
    if errors:
        return VerificationResult(
            False, 
            f"{len(errors)} syntax error(s)",
            "\n".join(errors[:5])  # Show first 5
        )
    
    return VerificationResult(True, f"All {len(code_cells)} code cells valid")


def verify_imports(notebook_path: Path) -> VerificationResult:
    """Check if imported modules are available (without executing)."""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    # Extract import statements
    imports = set()
    for cell in nb.get('cells', []):
        if cell.get('cell_type') != 'code':
            continue
        
        source = ''.join(cell.get('source', []))
        try:
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module.split('.')[0])
        except SyntaxError:
            continue
    
    # Check availability
    missing = []
    for module in imports:
        # Skip relative imports and common stdlib
        if module.startswith('.'):
            continue
        
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    if missing:
        return VerificationResult(
            False,
            f"{len(missing)} missing import(s)",
            f"Not installed: {', '.join(sorted(missing)[:10])}"
        )
    
    return VerificationResult(True, f"All {len(imports)} imports available")


def verify_markdown_cells(notebook_path: Path) -> VerificationResult:
    """Verify markdown cells have content."""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    md_cells = [c for c in nb.get('cells', []) if c.get('cell_type') == 'markdown']
    empty_count = sum(1 for c in md_cells if not ''.join(c.get('source', [])).strip())
    
    if empty_count > 0:
        return VerificationResult(
            False,
            f"{empty_count} empty markdown cell(s)",
            "Consider removing or filling empty cells"
        )
    
    return VerificationResult(True, f"{len(md_cells)} markdown cells OK")


def verify_notebook(notebook_path: Path) -> dict:
    """Run all verifications on a notebook."""
    results = {}
    
    # JSON structure (must pass for other checks)
    results['json'] = verify_json_structure(notebook_path)
    if not results['json'].passed:
        return results
    
    results['metadata'] = verify_notebook_metadata(notebook_path)
    results['syntax'] = verify_code_syntax(notebook_path)
    results['imports'] = verify_imports(notebook_path)
    results['markdown'] = verify_markdown_cells(notebook_path)
    
    return results


def main():
    """Verify all workshop notebooks."""
    print(f"\n{BOLD}Notebook Verification for Agents Workshop{RESET}")
    print("=" * 50)
    
    # Find notebooks
    repo_root = Path(__file__).parent.parent
    notebooks = list(repo_root.glob("Labs/**/Lab_*.ipynb"))
    
    if not notebooks:
        print(f"{RED}No notebooks found!{RESET}")
        return 1
    
    print(f"\nFound {len(notebooks)} notebook(s)\n")
    
    all_passed = True
    
    for nb_path in sorted(notebooks):
        relative_path = nb_path.relative_to(repo_root)
        print(f"{BOLD}{relative_path}{RESET}")
        
        results = verify_notebook(nb_path)
        
        for check_name, result in results.items():
            print_result(check_name, result)
            if not result.passed:
                all_passed = False
        
        print()
    
    # Summary
    print("=" * 50)
    if all_passed:
        print(f"{GREEN}{BOLD}All notebooks passed verification!{RESET}")
        return 0
    else:
        print(f"{YELLOW}{BOLD}Some checks failed. Review issues above.{RESET}")
        print(f"\n{YELLOW}Note: Import failures may be due to missing packages.")
        print(f"Run: pip install -r requirements.txt{RESET}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
