"""Git Remote Management and Verification Utility.

Provides automated inspection and reconfiguration of Git Remote URLs
to enforce alignment with project architectural guidelines.
"""

import subprocess
import sys
from typing import Dict, List


def run_git_cmd(args: List[str]) -> str:
    """Executes a Git CLI command and returns stdout as a string.

    Args:
        args (List[str]): List of command line arguments for git.

    Returns:
        str: Clean stripped standard output string.

    Raises:
        RuntimeError: Raised when execution returns non-zero code.
    """
    try:
        result = subprocess.run(
            ["git"] + args, capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as err:
        raise RuntimeError(f"Git CLI execution error: {err.stderr.strip()}") from err


def get_git_remotes() -> Dict[str, str]:
    """Retrieves all currently configured Git remote aliases and URLs.

    Returns:
        Dict[str, str]: Dictionary mapping remote names (e.g., 'origin') to URLs.
    """
    try:
        raw_output: str = run_git_cmd(["remote", "-v"])
        remotes: Dict[str, str] = {}
        if not raw_output:
            return remotes

        for line in raw_output.splitlines():
            parts: List[str] = line.split()
            if len(parts) >= 2:
                name, url = parts[0], parts[1]
                if "(fetch)" in line or name not in remotes:
                    remotes[name] = url
        return remotes
    except RuntimeError:
        return {}


def configure_remote_origin(target_url: str) -> bool:
    """Ensures 'origin' remote matches the target repository URL.

    Args:
        target_url (str): Target GitHub HTTPS or SSH URL.

    Returns:
        bool: True if configuration succeeded or was already up to date.
    """
    current_remotes: Dict[str, str] = get_git_remotes()

    if "origin" in current_remotes:
        if current_remotes["origin"] == target_url:
            print(f"✅ Remote 'origin' is already correctly set to: {target_url}")
            return True
        print(
            f"🔄 Updating 'origin' from '{current_remotes['origin']}' -> '{target_url}'"
        )
        run_git_cmd(["remote", "set-url", "origin", target_url])
    else:
        print(f"➕ Adding new remote 'origin': {target_url}")
        run_git_cmd(["remote", "add", "origin", target_url])

    return True


def main() -> None:
    """Main execution function for Git Remote verification."""
    # Target repository defined in project specification / README.md
    target_repo_url: str = "https://github.com/jeeradate/pythonwebapp.git"

    print("==================================================")
    print("      Food Order App - Git Remote Inspection      ")
    print("==================================================")

    try:
        current_branch: str = run_git_cmd(["branch", "--show-current"])
        print(
            f"📌 Active Branch: {current_branch if current_branch else 'Detached / Not Set'}"
        )

        success: bool = configure_remote_origin(target_repo_url)
        if success:
            print("\n🚀 Next Steps to push your code:")
            print("   1. Run: git branch -M main")
            print("   2. Run: git push -u origin main")
        print("==================================================")

    except RuntimeError as exc:
        print(f"❌ Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
