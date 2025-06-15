import os

def format_readme(analysis, summaries, project_name, tone):
    md = ""  # ✅ Initialize md first

    if project_name:
        md += f"# {project_name}\n\n"
    else:
        md += f"# {list(analysis.keys())[0].replace('.py','').title()}\n\n"

    if summaries:
        md += f"## Description\n"
        for fname, summary in summaries.items():
            filename = os.path.basename(fname)
            # Clean up <think> sections
            clean_summary = summary.split("<think>")[0].strip()
            md += f"**{filename}**\n{clean_summary}\n\n"

    if analysis:
        md += "## Features\n"
        for fname, info in analysis.items():
            filename = os.path.basename(fname)
            md += f"- **{filename}**: {len(info.get('functions', []))} functions, {len(info.get('classes', []))} classes\n"

    return md, [], []



def generate_readme(summaries, diagrams=None, charts=None):
    content = "## Project Structure\n"
    for path, summary in summaries.items():
        content += f"- {path}: {summary}\n"
    return content