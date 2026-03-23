import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# Dad jokes: https://icanhazdadjoke.com/api
# Pushover: https://pushover.net/api — secrets in .env (see .gitignore)
# Loads: dad_jokes/.env, then repo_root/.env/.env


def load_dotenv(path: Path, *, override: bool = False) -> None:
    """Load KEY=value lines into os.environ. Later files can override with override=True."""
    if not path.is_file():
        return
    # utf-8-sig strips UTF-8 BOM (Windows Notepad); otherwise the first key can be "\ufeffNAME"
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip().lstrip("\ufeff")
        val = val.strip().strip('"').strip("'")
        if key and (override or key not in os.environ):
            os.environ[key] = val


_script_dir = Path(__file__).resolve().parent
_repo_root = _script_dir.parent.parent
load_dotenv(_script_dir / ".env")
load_dotenv(_repo_root / ".env" / ".env", override=True)

req = urllib.request.Request(
    "https://icanhazdadjoke.com/",
    headers={
        "Accept": "application/json",
        "User-Agent": "dad_jokes.py",
    },
)
with urllib.request.urlopen(req, timeout=15) as response:
    data = json.loads(response.read().decode())

joke = data["joke"]
print(joke)

def _pushover_id_ok(s: str) -> bool:
    """App tokens and user keys are 30 chars [A-Za-z0-9] per Pushover docs."""
    return bool(re.fullmatch(r"[A-Za-z0-9]{30}", s))


token = (os.environ.get("PUSHOVER_TOKEN") or "").strip()
user = (os.environ.get("PUSHOVER_USER") or "").strip()
if not token or not user:
    print(
        "Tip: copy .env.example to .env (or set PUSHOVER_TOKEN and PUSHOVER_USER) to push to your phone.",
        file=sys.stderr,
    )
elif not _pushover_id_ok(token) or not _pushover_id_ok(user):
    print(
        "Pushover: PUSHOVER_TOKEN and PUSHOVER_USER must each be exactly 30 letters "
        f"and digits (got lengths {len(token)} and {len(user)}). Fix .env — no spaces, "
        "quotes, or line breaks inside the values.",
        file=sys.stderr,
    )
    if len(user) < 30:
        print(
            "PUSHOVER_USER is your account key on the Pushover homepage, not your device name (e.g. v12).",
            file=sys.stderr,
        )
    sys.exit(1)
else:
    params = {
        "token": token,
        "user": user,
        "title": "Dad joke",
        "message": joke,
    }
    device = (os.environ.get("PUSHOVER_DEVICE") or "").strip()
    if device:
        params["device"] = device
    body = urllib.parse.urlencode(params).encode()
    push = urllib.request.Request(
        "https://api.pushover.net/1/messages.json",
        data=body,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urllib.request.urlopen(push, timeout=15) as r:
            result = json.loads(r.read().decode())
        if result.get("status") != 1:
            print("Pushover error:", result, file=sys.stderr)
            sys.exit(1)
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        print("Pushover HTTP error:", e.code, err, file=sys.stderr)
        if e.code == 400 and "user" in err.lower():
            print(
                "Check PUSHOVER_USER: it must be your 30-char user key from "
                "https://pushover.net (not your phone number, not the app token). "
                "PUSHOVER_TOKEN is the application API token; do not swap them.",
                file=sys.stderr,
            )
        sys.exit(1)
