import os
import re


def on_page_markdown(markdown, page, config, files, **kwargs):
    if not page.file.src_path.endswith("blog/index.md"):
        return markdown

    if "<!-- blog-posts -->" not in markdown:
        return markdown

    blog_dir = os.path.dirname(page.file.abs_src_path)

    posts = []
    for f in sorted(os.listdir(blog_dir), reverse=True):
        if f.endswith(".md") and f != "index.md" and not f.startswith("_"):
            title = f.replace(".md", "").replace("_", " ")
            filepath = os.path.join(blog_dir, f)
            with open(filepath, "r", encoding="utf-8") as fh:
                for line in fh:
                    match = re.match(r"^#\s+(.+)", line.strip())
                    if match:
                        title = match.group(1)
                        break
            posts.append(f"- [{title}]({f})")

    if posts:
        post_list = "\n".join(posts)
    else:
        is_zh = "/zh/" in page.file.src_path
        post_list = "- 敬请期待。" if is_zh else "- Coming soon."

    return markdown.replace("<!-- blog-posts -->", post_list)
