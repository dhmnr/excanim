from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

BRIDGE_DIR = Path(__file__).resolve().parent.parent.parent.parent / "bridge"
EXPORT_SCRIPT = BRIDGE_DIR / "export.mjs"


def _find_node() -> str:
    # Check NVM first
    nvm_dir = os.environ.get("NVM_DIR", os.path.expanduser("~/.nvm"))
    default_alias = Path(nvm_dir) / "alias" / "default"
    if default_alias.exists():
        version = default_alias.read_text().strip()
        nvm_node = Path(nvm_dir) / "versions" / "node" / f"v{version}" / "bin" / "node"
        if nvm_node.exists():
            return str(nvm_node)
    # Check NVM versions directory for any installed version
    nvm_versions = Path(nvm_dir) / "versions" / "node"
    if nvm_versions.exists():
        versions = sorted(nvm_versions.iterdir(), reverse=True)
        for v in versions:
            node_bin = v / "bin" / "node"
            if node_bin.exists():
                return str(node_bin)
    # Fall back to system node
    node = shutil.which("node")
    if node:
        return node
    raise RuntimeError(
        "Node.js not found. Install Node.js >= 18 (e.g. via nvm) "
        "to use the Excalidraw bridge."
    )


def elements_to_svg(elements: list[dict], app_state: dict | None = None) -> str:
    payload = {
        "elements": elements,
        "appState": app_state or {
            "exportWithDarkMode": False,
            "exportBackground": True,
            "viewBackgroundColor": "#ffffff",
        },
    }
    return _call_bridge(json.dumps(payload))


def batch_elements_to_svg(frames: list[list[dict]], app_state: dict | None = None) -> list[str]:
    default_state = app_state or {
        "exportWithDarkMode": False,
        "exportBackground": True,
        "viewBackgroundColor": "#ffffff",
    }
    payload = [{"elements": els, "appState": default_state} for els in frames]
    result = _call_bridge(json.dumps(payload))
    return json.loads(result)


def _call_bridge(input_json: str) -> str:
    node = _find_node()
    result = subprocess.run(
        [node, str(EXPORT_SCRIPT)],
        input=input_json,
        capture_output=True,
        text=True,
        timeout=120,
        cwd=str(BRIDGE_DIR),
    )
    if result.returncode != 0:
        raise RuntimeError(f"Bridge failed:\n{result.stderr}")
    return result.stdout
