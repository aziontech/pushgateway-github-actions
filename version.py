import re
import subprocess
import sys

pattern_version = "^(\d+)\.(\d+)\.(\d+)$"
pattern_message = ".*(^|\s)feat(ure)?:?\s.*"

def current():
    try:
        version = subprocess.check_output(["git", "describe", "--tags", "--abbrev=0", "--match=*.*.*"], stderr=subprocess.STDOUT).strip()
    except subprocess.CalledProcessError:
        return "1.0.0"

    if not re.match(pattern_version, version):
        return "1.0.0"

    return version

def bump():
    revision  = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip()
    revisions = subprocess.check_output(["git", "show-ref", "--tags"]).strip()

    if re.search(revision, revisions):
        # tagged commit: do not duplicate
        sys.stderr.write("Error: Current Hash '{}' Already Tagged\n".format(revision))
        sys.exit(1)

    message = subprocess.check_output(["git", "log", "--pretty=format:%s", "--max-count=1"]).strip()

    result = re.search(pattern_version, current())

    major = int(result.group(1))
    minor = int(result.group(2))
    patch = int(result.group(3))

    if re.match(pattern_message, message):
        minor += 1
        patch = 0
    else:
        patch += 1

    version = "{}.{}.{}".format(major, minor, patch)

    try:
        # check if bumped version exists
        subprocess.check_output(["git", "show-ref", "--tags", version]).strip()
        # success? then error, because it exists and must not be duplicated
        sys.stderr.write("Error: Bumped Version '{}' Exists\n".format(version))
        sys.exit(2)
    except subprocess.CalledProcessError:
        pass

    return version

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == "bump":
        print(bump())
    else:
        print(current())

