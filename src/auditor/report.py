import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os

TEMPLATE = "report_template.html"


def generate_json_report(meta: dict, findings: list, out_path: str):
    payload = {"meta": meta, "findings": findings}
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2)


def generate_html_report(meta: dict, findings: list, out_path: str):
    env = Environment(loader=FileSystemLoader(searchpath=os.path.dirname(__file__)), autoescape=select_autoescape())
    try:
        tpl = env.get_template(TEMPLATE)
    except Exception:
        # fallback simple HTML
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write('<html><body><h1>Report</h1>')
            f.write(f'<pre>{json.dumps({"meta":meta, "findings":findings}, indent=2)}</pre>')
        return
    html = tpl.render(meta=meta, findings=findings)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)

