#!/usr/bin/env python3
"""
Environment Checker for Crafting Custom Agents Workshop

Run this script to verify your environment is properly configured:
    python check_environment.py

This will check:
1. Python version (3.10+ required)
2. Required packages installed
3. API keys configured
4. Quick LLM connectivity test
"""

import sys
import os
from importlib import import_module

# ANSI colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"


def print_status(message: str, status: str):
    """Print a status message with color."""
    if status == "ok":
        symbol = f"{GREEN}✓{RESET}"
    elif status == "warn":
        symbol = f"{YELLOW}⚠{RESET}"
    else:
        symbol = f"{RED}✗{RESET}"
    print(f"  {symbol} {message}")


def print_header(title: str):
    """Print a section header."""
    print(f"\n{BOLD}{'='*50}{RESET}")
    print(f"{BOLD}{title}{RESET}")
    print(f"{BOLD}{'='*50}{RESET}")


def check_python_version():
    """Check Python version is 3.10+."""
    print_header("Python Version")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major >= 3 and version.minor >= 10:
        print_status(f"Python {version_str}", "ok")
        return True
    else:
        print_status(f"Python {version_str} (need 3.10+)", "fail")
        return False


def check_packages():
    """Check required packages are installed."""
    print_header("Required Packages")
    
    required_packages = [
        ("langchain", "langchain"),
        ("langchain_openai", "langchain-openai"),
        ("langchain_core", "langchain-core"),
        ("langgraph", "langgraph"),
        ("dotenv", "python-dotenv"),
    ]
    
    optional_packages = [
        ("autogen", "pyautogen"),
        ("anthropic", "anthropic"),
    ]
    
    all_required_ok = True
    
    print("\n  Required:")
    for import_name, pip_name in required_packages:
        try:
            import_module(import_name)
            print_status(f"{pip_name}", "ok")
        except ImportError:
            print_status(f"{pip_name} - run: pip install {pip_name}", "fail")
            all_required_ok = False
    
    print("\n  Optional:")
    for import_name, pip_name in optional_packages:
        try:
            import_module(import_name)
            print_status(f"{pip_name}", "ok")
        except ImportError:
            print_status(f"{pip_name} (not installed)", "warn")
    
    return all_required_ok


def check_api_keys():
    """Check API keys are configured."""
    print_header("API Keys")
    
    # Try to load from .env
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    keys_status = {}
    
    # OpenAI (required)
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        # Mask the key for display
        masked = openai_key[:8] + "..." + openai_key[-4:] if len(openai_key) > 12 else "****"
        print_status(f"OPENAI_API_KEY: {masked}", "ok")
        keys_status["openai"] = True
    else:
        print_status("OPENAI_API_KEY: not found", "fail")
        print(f"      {YELLOW}Add to .env file: OPENAI_API_KEY=sk-...{RESET}")
        keys_status["openai"] = False
    
    # Anthropic (optional)
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    if anthropic_key:
        masked = anthropic_key[:8] + "..." + anthropic_key[-4:] if len(anthropic_key) > 12 else "****"
        print_status(f"ANTHROPIC_API_KEY: {masked}", "ok")
    else:
        print_status("ANTHROPIC_API_KEY: not found (optional)", "warn")
    
    return keys_status.get("openai", False)


def check_llm_connectivity():
    """Test actual LLM connectivity."""
    print_header("LLM Connectivity Test")
    
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        print_status("Skipped (no API key)", "warn")
        return False
    
    # First try the official OpenAI client (most predictable). If it's not
    # available, fall back to LangChain's ChatOpenAI when present.
    try:
        import openai
        openai.api_key = openai_key

        print("  Testing OpenAI (openai) package connection...")

        # Locate a compatible create() function dynamically to satisfy static
        # analysers that may not know about newer or older SDK shapes.
        create_fn = None
        chat_cls = getattr(openai, "ChatCompletion", None)
        if chat_cls is not None and hasattr(chat_cls, "create"):
            create_fn = getattr(chat_cls, "create")
        else:
            chat_mod = getattr(openai, "chat", None)
            if chat_mod is not None:
                completions = getattr(chat_mod, "completions", None)
                if completions is not None and hasattr(completions, "create"):
                    create_fn = getattr(completions, "create")

        if create_fn is None or not callable(create_fn):
            raise RuntimeError("openai ChatCompletion.create not found")

        resp = create_fn(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'OK' and nothing else."}],
            max_tokens=10,
            temperature=0,
        )

        # Extract text from the response safely using explicit type checks
        text = None
        # If the response is a dict (common for openai.ChatCompletion.create)
        if isinstance(resp, dict):
            choices = resp.get("choices")
            if isinstance(choices, list) and choices:
                first = choices[0]
                if isinstance(first, dict):
                    msg = first.get("message")
                    if isinstance(msg, dict):
                        text = msg.get("content")
                    else:
                        text = first.get("text") or first.get("content")
        else:
            # Try attribute-style access (some SDK wrappers return objects)
            choices = getattr(resp, "choices", None)
            if isinstance(choices, list) and choices:
                first = choices[0]
                if isinstance(first, dict):
                    msg = first.get("message")
                    if isinstance(msg, dict):
                        text = msg.get("content")
                    else:
                        text = first.get("text") or first.get("content")
                else:
                    msg = getattr(first, "message", None)
                    if msg is not None:
                        text = getattr(msg, "content", None)
                    else:
                        text = getattr(first, "text", None)

        # Fallbacks
        if not text and isinstance(resp, dict):
            text = resp.get("text") or resp.get("content")
        if not text:
            try:
                text = str(resp)
            except Exception:
                text = ""

        if isinstance(text, str) and "OK" in text.upper():
            print_status("OpenAI API connection successful", "ok")
            return True
        else:
            print_status(f"Unexpected response: {text[:50]}", "warn")
            return True

    except Exception:
        # openai package not available or failed; try LangChain chat model
        try:
            from langchain.chat_models import ChatOpenAI
            # langchain message classes live in different modules across
            # versions; try a couple of common locations
            HumanMessageClass = None
            try:
                from langchain.schema import HumanMessage as HumanMessageClass
            except Exception:
                try:
                    from langchain_core.messages import HumanMessage as HumanMessageClass
                except Exception:
                    HumanMessageClass = None

            if ChatOpenAI is None:
                raise ImportError("ChatOpenAI class not available")

            print("  Testing OpenAI connection via LangChain...")

            # ChatOpenAI constructor uses `model_name` in recent versions.
            llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

            # Build message payload and invoke the model safely.
            # Try available call methods in order and verify callability.
            def _call_llm_safe(model_obj, messages):
                last_exc = None
                # Try preferred high-level methods first
                for method_name in ("predict_messages", "invoke", "__call__"):
                    if method_name == "__call__":
                        if callable(model_obj):
                            try:
                                return model_obj(messages)
                            except Exception as e:
                                last_exc = e
                                continue
                        continue

                    fn = getattr(model_obj, method_name, None)
                    if fn is not None and callable(fn):
                        try:
                            return fn(messages)
                        except Exception as e:
                            last_exc = e
                            continue

                # If we reach here, nothing worked
                if last_exc:
                    raise last_exc
                raise RuntimeError("No callable method found on the LangChain model object")

            # Prepare messages depending on available message class
            if HumanMessageClass is not None:
                payload = [HumanMessageClass(content="Say 'OK' and nothing else.")]
            else:
                payload = [{"role": "user", "content": "Say 'OK' and nothing else."}]

            try:
                response = _call_llm_safe(llm, payload)
            except Exception:
                # Re-raise with context for easier debugging
                raise

            # Normalize different response shapes into a string
            text = None
            if isinstance(response, str):
                text = response
            elif hasattr(response, "content"):
                text = getattr(response, "content")
            elif isinstance(response, list) and response:
                first = response[0]
                if isinstance(first, str):
                    text = first
                elif isinstance(first, dict):
                    # Try common keys
                    text = first.get("content") or first.get("text")
                elif hasattr(first, "content"):
                    text = getattr(first, "content")
            else:
                # Some response shapes include a `generations` attribute
                gens = getattr(response, "generations", None)
                if gens:
                    try:
                        if gens and len(gens) > 0 and len(gens[0]) > 0:
                            maybe = gens[0][0]
                            text = getattr(maybe, "text", None) or getattr(maybe, "generation", None)
                    except Exception:
                        text = str(response)

            text = text or str(response)

            if isinstance(text, str) and "OK" in text.upper():
                print_status("OpenAI API connection successful (via LangChain)", "ok")
                return True
            else:
                print_status(f"Unexpected response: {text[:50]}", "warn")
                return True

        except Exception as e:
            print_status(f"Connection failed: {str(e)[:200]}", "fail")
            return False


def check_utils_package():
    """Check if the utils package is accessible."""
    print_header("Utils Package")
    
    # Add repo root to path
    repo_root = os.path.dirname(os.path.abspath(__file__))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)
    
    try:
        from utils import load_environment, get_langchain_llm
        print_status("utils package importable", "ok")
        return True
    except ImportError as e:
        print_status(f"utils package not found: {e}", "fail")
        return False


def check_env_file():
    """Check if .env file exists."""
    print_header(".env File")
    
    repo_root = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(repo_root, ".env")
    
    if os.path.exists(env_path):
        print_status(".env file found", "ok")
        return True
    else:
        print_status(".env file not found", "warn")
        print(f"      {YELLOW}Create .env in repo root with your API keys{RESET}")
        
        # Check for .env.example
        example_path = os.path.join(repo_root, ".env.example")
        if os.path.exists(example_path):
            print(f"      {YELLOW}Copy .env.example to .env and fill in your keys{RESET}")
        
        return False


def main():
    """Run all environment checks."""
    print(f"\n{BOLD}Crafting Custom Agents Workshop - Environment Check{RESET}")
    print("=" * 50)
    
    results = {}
    
    # Run checks
    results["python"] = check_python_version()
    results["packages"] = check_packages()
    results["env_file"] = check_env_file()
    results["api_keys"] = check_api_keys()
    results["utils"] = check_utils_package()
    
    # Only test connectivity if API key exists
    if results["api_keys"]:
        results["connectivity"] = check_llm_connectivity()
    else:
        results["connectivity"] = False
    
    # Summary
    print_header("Summary")
    
    critical_passed = results["python"] and results["packages"] and results["api_keys"]
    all_passed = all(results.values())
    
    if all_passed:
        print(f"\n  {GREEN}{BOLD}All checks passed! You're ready for the workshop.{RESET}\n")
    elif critical_passed:
        print(f"\n  {YELLOW}{BOLD}Critical checks passed. Some optional items missing.{RESET}")
        print(f"  {YELLOW}You can proceed with the workshop.{RESET}\n")
    else:
        print(f"\n  {RED}{BOLD}Some critical checks failed.{RESET}")
        print(f"  {RED}Please fix the issues above before the workshop.{RESET}\n")
        
        if not results["python"]:
            print(f"  → Install Python 3.10+: https://python.org")
        if not results["packages"]:
            print(f"  → Run: pip install -r requirements.txt")
        if not results["api_keys"]:
            print(f"  → Get API key: https://platform.openai.com/api-keys")
            print(f"  → Add to .env: OPENAI_API_KEY=sk-...")
        print()
    
    # Return exit code
    return 0 if critical_passed else 1


if __name__ == "__main__":
    sys.exit(main())
