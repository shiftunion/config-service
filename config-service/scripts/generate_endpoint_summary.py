#!/usr/bin/env python
"""Generate a Markdown summary of the API suitable for UI planning.

Usage:
  uv run python scripts/generate_endpoint_summary.py > ENDPOINTS_SUMMARY.md
"""
from __future__ import annotations

import re
import sys
from typing import Any, Dict, List, Optional

import pathlib

# Ensure current working directory is importable for 'app'
cwd = pathlib.Path(__file__).resolve().parents[1]
if str(cwd) not in sys.path:
    sys.path.insert(0, str(cwd))

from app.main import app  # noqa: E402


def _schema_fields(components: Dict[str, Any], schema: Dict[str, Any]) -> List[str]:
    if "$ref" in schema:
        ref = schema["$ref"].split("/")[-1]
        schema = components.get("schemas", {}).get(ref, {})
    if schema.get("type") != "object":
        return []
    required = set(schema.get("required", []))
    props = schema.get("properties", {})
    out: List[str] = []
    for name, prop in props.items():
        ptype: str | None = prop.get("type")
        if not ptype and "$ref" in prop:
            ptype = prop["$ref"].split("/")[-1]
        if ptype == "array":
            item = prop.get("items", {})
            if "$ref" in item:
                it = item["$ref"].split("/")[-1]
            else:
                it = item.get("type", "any")
            ptype = f"List[{it}]"
        if ptype is None:
            ptype = "any"
        nullable = prop.get("nullable", False)
        mark = "" if name in required and not nullable else "?"
        out.append(f"{name}: {ptype}{mark}")
    return out


def _success_schema(responses: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    for code in ("200", "201"):
        if code in responses:
            content = responses[code].get("content", {})
            js = content.get("application/json")
            if js:
                return js.get("schema")
    return None


def build_summary() -> str:
    openapi = app.openapi()
    components = openapi.get("components", {})
    lines: List[str] = ["# API Endpoint Summary", "", "> Generated from live OpenAPI schema", ""]
    for path, methods in sorted(openapi.get("paths", {}).items()):
        for method, meta in sorted(methods.items()):
            if method.lower() not in {"get", "post", "put", "delete", "patch"}:
                continue
            op_id = meta.get("operationId", "")
            req_fields: List[str] = []
            req_body = meta.get("requestBody", {})
            content = req_body.get("content", {}) if isinstance(req_body, dict) else {}
            js = content.get("application/json")
            if js:
                req_fields = _schema_fields(components, js.get("schema", {}))
            resp_schema = _success_schema(meta.get("responses", {}))
            resp_fields: List[str] = []
            if resp_schema:
                resp_fields = _schema_fields(components, resp_schema)
            errors = [
                c for c in meta.get("responses", {}) if re.fullmatch(r"\d{3}", c) and not c.startswith("2")
            ]
            errors.sort()
            lines.append(f"## {method.upper()} {path}")
            if op_id:
                lines.append(f"- operationId: `{op_id}`")
            if req_fields:
                lines.append("- request fields:")
                lines.extend(f"  - {f}" for f in req_fields)
            else:
                lines.append("- request body: (none or primitive)")
            if resp_fields:
                lines.append("- response fields:")
                lines.extend(f"  - {f}" for f in resp_fields)
            else:
                lines.append("- response: (non-object or none)")
            if errors:
                lines.append(f"- error status codes: {', '.join(errors)}")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    sys.stdout.write(build_summary())
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
