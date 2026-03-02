import os
import re

CATEGORIES_EN = {
    "thoughts": "Thoughts",
    "essay": "Essays",
}

CATEGORIES_ZH = {
    "thoughts": "思考",
    "essay": "随笔",
}

CATEGORY_ORDER = ["thoughts", "essay"]


def _parse_post(filepath):
    """Read a blog post and return (title, category)."""
    title = os.path.basename(filepath).replace(".md", "").replace("_", " ")
    category = "essay"
    in_frontmatter = False
    frontmatter_done = False

    with open(filepath, "r", encoding="utf-8") as fh:
        for line in fh:
            stripped = line.strip()
            if not frontmatter_done:
                if stripped == "---" and not in_frontmatter:
                    in_frontmatter = True
                    continue
                if stripped == "---" and in_frontmatter:
                    frontmatter_done = True
                    continue
                if in_frontmatter:
                    m = re.match(r"^category:\s*(.+)", stripped)
                    if m:
                        category = m.group(1).strip().lower()
                    continue
            m = re.match(r"^#\s+(.+)", stripped)
            if m:
                title = m.group(1)
                break

    return title, category


def on_page_markdown(markdown, page, config, files, **kwargs):
    if not page.file.src_path.endswith("blog/index.md"):
        return markdown

    if "<!-- blog-posts -->" not in markdown:
        return markdown

    blog_dir = os.path.dirname(page.file.abs_src_path)
    is_zh = "/zh/" in page.file.src_path
    cat_labels = CATEGORIES_ZH if is_zh else CATEGORIES_EN

    categorized = {}
    for f in sorted(os.listdir(blog_dir), reverse=True):
        if f.endswith(".md") and f != "index.md" and not f.startswith("_"):
            title, cat = _parse_post(os.path.join(blog_dir, f))
            categorized.setdefault(cat, []).append(f"- [{title}]({f})")

    if not categorized:
        placeholder = "- 敬请期待。" if is_zh else "- Coming soon."
        return markdown.replace("<!-- blog-posts -->", placeholder)

    sections = []
    seen = set()
    for cat in CATEGORY_ORDER:
        if cat in categorized:
            label = cat_labels.get(cat, cat)
            sections.append(f"### {label}\n")
            sections.append("\n".join(categorized[cat]))
            sections.append("")
            seen.add(cat)

    for cat in sorted(categorized.keys()):
        if cat not in seen:
            label = cat_labels.get(cat, cat)
            sections.append(f"### {label}\n")
            sections.append("\n".join(categorized[cat]))
            sections.append("")

    return markdown.replace("<!-- blog-posts -->", "\n".join(sections))
