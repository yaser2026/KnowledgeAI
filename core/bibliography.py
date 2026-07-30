def generate_bibliography(sources):
    """
    تولید لیست منابع و مراجع به سبک استاندارد
    """
    bib_html = "<h2>مراجع و منابع استفاده شده</h2><ul>"
    for idx, source in enumerate(sources, 1):
        title = source.get('title', 'عنوان نامشخص')
        url = source.get('url', '#')
        bib_html += f"<li>[{idx}] <a href='{url}'>{title}</a> - <code>{url}</code></li>"
    bib_html += "</ul>"
    return bib_html
