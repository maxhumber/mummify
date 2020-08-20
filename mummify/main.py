import logging
from pathlib import Path
import re
import subprocess
import uuid

LOGFILE = "mummify.log"


def run(command, output=False, silent=False):
    """Run shell commands

    - command (str): a bash command
    - output (bool, False): capture and return the STDOUT
    - silent (bool, False): force commands to run silently

    Example:

    `run("git --git-dir=.mummify status")`
    """
    if silent:
        command += " --quiet"
    if output:
        s = subprocess.run(command, capture_output=True, shell=True)
        output = s.stdout.decode("utf-8").strip()
        return output
    subprocess.run(command, shell=True)


def colour(string):
    """Paint it purple!

    - string (str): colour a string purple

    Example:

    `purple('Hello World!')`
    """
    print(f"\033[35m{string}\033[0m")


def init_mummify():
    """Initialize mummify"""
    run("git --work-tree=. --git-dir=.mummify init", silent=True)
    run("echo '.mummify' >> .gitignore")
    run("echo '__pycache__' >> .gitignore")
    run("git --work-tree=. --git-dir=.mummify add .gitignore")
    run('git --work-tree=. --git-dir=.mummify commit -m "000000"', silent=True)
    colour("mummify initializing...")


def history():
    """View modified git graph (CLI)"""
    graph = run(
        "git --work-tree=. --git-dir=.mummify log --graph --decorate --oneline",
        output=True,
    )
    graph = re.sub(r"\s([a-zA-Z0-9_-]){7}\s", "  ", graph)
    graph = graph.replace(" (HEAD -> master)", "◀")
    graph = graph.replace("*  000000", "").strip()
    lines = graph.split('\n')[::-1]
    graph = ''
    for line in lines:
        for character in line:
            if character == "/":
                character = "\\"
            elif character == "\\":
                character = "/"
            graph += character
        graph += '\n'
    graph = graph.strip()
    return colour(graph)


def check_status():
    """Check mummify git status"""
    git_status = run("git --work-tree=. --git-dir=.mummify status", output=True)
    return git_status


def create_branch(branch):
    """Create new mummify branch

    - branch (str): branch UUID
    """
    run(f"git --work-tree=. --git-dir=.mummify checkout -b {branch}", silent=True)


def commit(branch):
    """Commit run to .mummify

    - branch (str): branch UUID
    """
    run("git --work-tree=. --git-dir=.mummify add .")
    run(f"git --work-tree=. --git-dir=.mummify commit -m {branch}", silent=True)
    run("git --work-tree=. --git-dir=.mummify checkout master", silent=True)
    run(f"git --work-tree=. --git-dir=.mummify merge {branch}", silent=True)
    run(f"git --work-tree=. --git-dir=.mummify branch -d {branch}", silent=True)


def find(id):
    """Find git commit based on mummify id

    - id (str): branch UUID

    Example:

    `find("2d234a")`
    """
    log_item = run(
        f"git --work-tree=. --git-dir=.mummify log --all --grep={id}", output=True
    )
    commit = re.findall(r"(?<=commit\s)(.*?)(?=\n)", log_item)[0]
    return commit


def switch(id):
    """Switch to a specific mummify commit (CLI)

    - id (str): branch UUID

    Example:

    `switch("2d234a")`
    """
    assert len(id) == 6
    commit = find(id)
    run("git --work-tree=. --git-dir=.mummify checkout -b logger", silent=True)
    run("git --work-tree=. --git-dir=.mummify checkout -b switcher", silent=True)
    run(f"git --work-tree=. --git-dir=.mummify reset --hard {commit}", silent=True)
    run("git --work-tree=. --git-dir=.mummify merge -s ours --no-commit master >/dev/null 2>&1")
    run(f"git --work-tree=. --git-dir=.mummify checkout logger {LOGFILE} >/dev/null 2>&1")
    run(f'git --work-tree=. --git-dir=.mummify commit -m "{id}"', silent=True)
    run("git --work-tree=. --git-dir=.mummify checkout master", silent=True)
    run("git --work-tree=. --git-dir=.mummify merge switcher >/dev/null 2>&1")
    run("git --work-tree=. --git-dir=.mummify branch -D logger", silent=True)
    run("git --work-tree=. --git-dir=.mummify branch -D switcher", silent=True)
    return colour(f"mummify switched to {id}")


def log(message):
    """Save a snapshot and log a message to mummify.log

    - message (str): message to log

    Example:

    `log('Accuracy: 0.98')`
    """
    logging.basicConfig(
        filename=LOGFILE, level=logging.INFO, style="{", format="[{name}] {message}"
    )
    branch = str(uuid.uuid4().hex)[:6]
    logger = logging.getLogger(branch)
    if not Path(".mummify").is_dir():
        init_mummify()
    if "nothing to commit" in check_status():
        return colour("mummify can't see any changes")
    create_branch(branch)
    logger.info(message)
    colour(message)
    commit(branch)
