from __future__ import annotations

import html
import re
from pathlib import Path


CSS = """
:root{
  --bg:#f5f7fb;
  --card:#ffffff;
  --text:#1f2937;
  --muted:#667085;
  --line:#e5e7eb;
  --brand:#0f766e;
  --brand-soft:#ecfeff;
  --code:#0b1220;
  --shadow:0 10px 30px rgba(15,23,42,.08);
  --radius:18px;
  --max:1080px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0;
  color:var(--text);
  background:
    radial-gradient(circle at top left, rgba(15,118,110,.08), transparent 28%),
    radial-gradient(circle at top right, rgba(14,165,233,.08), transparent 24%),
    var(--bg);
  font:16px/1.75 "Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;
}
.page{max-width:var(--max);margin:0 auto;padding:32px 20px 64px}
.layout{
  display:grid;
  grid-template-columns:280px minmax(0,1fr);
  gap:24px;
  align-items:start;
}
.sidebar{
  position:sticky;
  top:20px;
  background:rgba(255,255,255,.86);
  backdrop-filter:blur(10px);
  border:1px solid rgba(255,255,255,.9);
  border-radius:24px;
  box-shadow:var(--shadow);
  padding:20px 18px;
}
.sidebar-title{
  margin:0 0 8px;
  font-size:16px;
}
.sidebar-note{
  margin:0 0 14px;
  color:var(--muted);
  font-size:13px;
  line-height:1.6;
}
.search{
  margin:0 0 14px;
}
.search-tools{
  display:flex;
  gap:8px;
  margin-top:8px;
}
.search input{
  width:100%;
  border:1px solid var(--line);
  background:#fff;
  color:var(--text);
  border-radius:14px;
  padding:11px 14px;
  outline:none;
  font:14px/1.4 "Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;
}
.search input:focus{
  border-color:#99f6e4;
  box-shadow:0 0 0 4px rgba(45,212,191,.12);
}
.tool-btn{
  border:1px solid var(--line);
  background:#fff;
  color:var(--text);
  border-radius:12px;
  padding:8px 10px;
  cursor:pointer;
  font:13px/1.2 "Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;
}
.tool-btn:hover{
  background:#f8fafc;
  border-color:#cbd5e1;
}
.sidebar.collapsed .toc,
.sidebar.collapsed .sidebar-note,
.sidebar.collapsed .search,
.sidebar.collapsed .toc-count{
  display:none;
}
.sidebar.collapsed{
  padding-bottom:14px;
}
.toc{
  display:flex;
  flex-direction:column;
  gap:6px;
}
.toc a{
  color:var(--text);
  text-decoration:none;
  padding:8px 10px;
  border-radius:12px;
  transition:.18s ease;
  font-size:14px;
}
.toc a:hover{
  background:var(--brand-soft);
  color:var(--brand);
}
.toc a.active{
  background:#dcfce7;
  color:#166534;
  font-weight:700;
}
.toc .lv2{padding-left:10px}
.toc .lv3{padding-left:22px;color:var(--muted)}
.toc .lv4{padding-left:34px;color:var(--muted)}
.main{min-width:0}
.hero{
  background:linear-gradient(135deg,#ffffff,#f8fffe);
  border:1px solid rgba(15,118,110,.12);
  border-radius:28px;
  box-shadow:var(--shadow);
  padding:36px 32px;
  margin-bottom:24px;
}
.eyebrow{color:var(--brand);font-size:13px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}
h1{margin:10px 0 8px;font-size:38px;line-height:1.2}
.subtitle{margin:0;color:var(--muted);max-width:760px}
.content{
  background:rgba(255,255,255,.76);
  backdrop-filter:blur(6px);
  border:1px solid rgba(255,255,255,.8);
  border-radius:28px;
  box-shadow:var(--shadow);
  padding:28px;
}
h2,h3,h4{scroll-margin-top:24px}
h2{
  margin:34px 0 14px;
  padding-top:6px;
  font-size:28px;
  border-top:1px solid var(--line);
}
h3{margin:26px 0 12px;font-size:22px}
h4{margin:18px 0 10px;font-size:18px}
p{margin:12px 0}
ul,ol{padding-left:24px;margin:12px 0}
li{margin:6px 0}
hr{border:none;border-top:1px solid var(--line);margin:28px 0}
code{
  font-family:"Cascadia Code","Consolas",monospace;
  background:#eef2ff;
  color:#312e81;
  border-radius:8px;
  padding:2px 6px;
}
pre{
  margin:0;
  overflow:auto;
  padding:18px;
  border-radius:16px;
  background:var(--code);
  color:#dbeafe;
  box-shadow:inset 0 0 0 1px rgba(148,163,184,.15);
}
pre code{background:transparent;color:inherit;padding:0}
table{
  width:100%;
  border-collapse:collapse;
  margin:16px 0;
  overflow:hidden;
  border-radius:16px;
  background:var(--card);
  box-shadow:inset 0 0 0 1px var(--line);
}
th,td{
  border:1px solid var(--line);
  padding:12px 14px;
  text-align:left;
  vertical-align:top;
}
th{background:#f8fafc;font-weight:700}
.note{
  background:linear-gradient(180deg,#f8fffe,#ffffff);
  border:1px solid rgba(15,118,110,.15);
  border-left:4px solid var(--brand);
  border-radius:16px;
  padding:14px 16px;
  margin:16px 0;
}
.entry-grid{
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(240px,1fr));
  gap:16px;
  margin:18px 0 8px;
}
.entry-card{
  display:block;
  padding:18px;
  border-radius:18px;
  background:linear-gradient(135deg,#ffffff,#f0fdf9);
  border:1px solid rgba(15,118,110,.16);
  box-shadow:var(--shadow);
  text-decoration:none;
  color:var(--text);
}
.entry-card:hover{
  border-color:#99f6e4;
  background:linear-gradient(135deg,#ffffff,#ecfeff);
}
.entry-card strong{
  display:block;
  margin-bottom:6px;
  font-size:17px;
}
.entry-card span{
  color:var(--muted);
  font-size:14px;
}
.quick-links{
  display:flex;
  flex-wrap:wrap;
  gap:10px;
  margin:14px 0 0;
}
.quick-links a{
  display:inline-block;
  padding:9px 12px;
  border-radius:999px;
  border:1px solid rgba(15,118,110,.18);
  background:#fff;
  color:var(--brand);
  text-decoration:none;
  font-size:14px;
}
.quick-links a:hover{
  background:#ecfeff;
  border-color:#99f6e4;
}
.diagram{
  margin:18px 0;
  border:1px solid rgba(15,118,110,.12);
  background:linear-gradient(180deg,#f8fffe,#ffffff);
  border-radius:20px;
  overflow:hidden;
  box-shadow:var(--shadow);
}
.diagram-head{
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:12px;
  padding:12px 16px;
  border-bottom:1px solid var(--line);
  color:var(--muted);
  font-size:14px;
}
.diagram-body{padding:16px}
.diagram-grid{
  display:grid;
  grid-template-columns:1.15fr .85fr;
  gap:16px;
  align-items:start;
}
.diagram-svg{
  width:100%;
  min-height:180px;
  border:1px dashed #cbd5e1;
  border-radius:16px;
  background:#fcfffe;
}
.diagram-text pre{background:#0f172a}
.footer{
  color:var(--muted);
  font-size:13px;
  text-align:center;
  margin-top:20px;
}
.pager{
  display:flex;
  justify-content:space-between;
  gap:16px;
  margin-top:22px;
}
.pager a,.pager span{
  flex:1;
  display:block;
  padding:14px 16px;
  border-radius:18px;
  border:1px solid var(--line);
  background:#fff;
  color:var(--text);
  text-decoration:none;
  box-shadow:var(--shadow);
}
.pager a:hover{
  border-color:#a7f3d0;
  background:#f0fdf4;
}
.pager-label{
  display:block;
  color:var(--muted);
  font-size:12px;
  margin-bottom:4px;
}
.book-section{
  margin-top:36px;
  padding-top:16px;
  border-top:1px solid var(--line);
}
.result-card{
  border:1px solid var(--line);
  background:#fff;
  border-radius:18px;
  padding:16px 18px;
  box-shadow:var(--shadow);
  margin:14px 0;
}
.result-card h3{
  margin:0 0 8px;
  font-size:18px;
}
.result-card p{
  margin:0;
  color:var(--muted);
}
.result-link{
  color:var(--brand);
  text-decoration:none;
}
.global-search-list[hidden]{
  display:none;
}
.search-meta{
  display:none;
  margin:0 0 16px;
  color:var(--muted);
  font-size:14px;
}
.toc-count{
  margin:0 0 10px;
  color:var(--muted);
  font-size:12px;
}
.search-mark{
  background:#fef08a;
  color:inherit;
  padding:0 .12em;
  border-radius:4px;
}
@media (max-width: 860px){
  .page{padding:18px 14px 36px}
  .layout{grid-template-columns:1fr}
  .sidebar{position:static}
  .hero,.content{padding:20px}
  h1{font-size:30px}
  h2{font-size:24px}
  .diagram-grid{grid-template-columns:1fr}
  .pager{flex-direction:column}
}
@media print{
  body{background:#fff}
  .page{max-width:none;padding:0}
  .layout{display:block}
  .sidebar,.footer,.pager{display:none}
  .hero,.content{
    box-shadow:none;
    border:0;
    background:#fff;
    padding:0;
  }
  h1,h2,h3,h4{break-after:avoid}
  pre,table,.diagram,.note{break-inside:avoid}
}
"""

SCRIPT = """
<script>
document.addEventListener('DOMContentLoaded', function () {
  const sidebar = document.querySelector('.sidebar');
  const toggleTocButton = document.getElementById('toggle-toc');
  const searchInput = document.getElementById('doc-search');
  const searchMeta = document.getElementById('search-meta');
  const searchCount = document.getElementById('search-count');
  const nextMatchButton = document.getElementById('next-match');
  const tocLinks = Array.from(document.querySelectorAll('.toc a[href^="#"]')).filter(a => a.getAttribute('href') !== '#top');
  const sections = tocLinks
    .map(link => document.getElementById(link.getAttribute('href').slice(1)))
    .filter(Boolean);
  const content = document.querySelector('.content');
  let currentMarkIndex = -1;
  let currentMarks = [];

  function clearMarks() {
    document.querySelectorAll('mark.search-mark').forEach(mark => {
      const text = document.createTextNode(mark.textContent || '');
      const parent = mark.parentNode;
      if (!parent) return;
      parent.replaceChild(text, mark);
      parent.normalize();
    });
    currentMarkIndex = -1;
    currentMarks = [];
  }

  function escapeRegExp(value) {
    return value.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&');
  }

  function highlightInElement(element, keyword) {
    const walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT, {
      acceptNode(node) {
        if (!node.nodeValue || !node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
        const parent = node.parentElement;
        if (!parent) return NodeFilter.FILTER_REJECT;
        const tag = parent.tagName;
        if (['SCRIPT', 'STYLE', 'CODE', 'PRE', 'MARK'].includes(tag)) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    const textNodes = [];
    while (walker.nextNode()) textNodes.push(walker.currentNode);
    const regex = new RegExp(escapeRegExp(keyword), 'gi');
    textNodes.forEach(node => {
      const text = node.nodeValue;
      if (!text || !regex.test(text)) return;
      regex.lastIndex = 0;
      const frag = document.createDocumentFragment();
      let lastIndex = 0;
      let match;
      while ((match = regex.exec(text)) !== null) {
        frag.appendChild(document.createTextNode(text.slice(lastIndex, match.index)));
        const mark = document.createElement('mark');
        mark.className = 'search-mark';
        mark.textContent = match[0];
        frag.appendChild(mark);
        lastIndex = match.index + match[0].length;
      }
      frag.appendChild(document.createTextNode(text.slice(lastIndex)));
      node.parentNode.replaceChild(frag, node);
    });
  }

  function runSearch(keyword) {
    if (!content) return;
    clearMarks();
    const normalized = keyword.trim().toLowerCase();
    const searchable = Array.from(content.querySelectorAll('h1,h2,h3,h4,p,li,td,th,.note'));
    let matches = 0;

    searchable.forEach(el => {
      const hay = (el.textContent || '').toLowerCase();
      const hit = normalized && hay.includes(normalized);
      if (!normalized) {
        el.style.display = '';
      } else if (hit) {
        el.style.display = '';
        matches += 1;
      } else if (el.closest('table') || el.closest('ul') || el.closest('ol')) {
        if (!hay.includes(normalized)) el.style.display = '';
      } else {
        el.style.display = '';
      }
    });

    document.querySelectorAll('.toc a[data-title]').forEach(link => {
      const title = (link.getAttribute('data-title') || '').toLowerCase();
      const hit = !normalized || title.includes(normalized);
      link.style.display = hit ? '' : 'none';
    });

    if (normalized) {
      highlightInElement(content, keyword.trim());
      currentMarks = Array.from(document.querySelectorAll('mark.search-mark'));
      if (currentMarks.length) {
        currentMarkIndex = 0;
        currentMarks[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
      if (searchMeta) {
        searchMeta.style.display = 'block';
        searchMeta.textContent = matches ? `已高亮包含“${keyword.trim()}”的内容` : `没有找到“${keyword.trim()}”`;
      }
      if (searchCount) searchCount.textContent = currentMarks.length ? `匹配 ${currentMarks.length} 处` : '无匹配';
      if (nextMatchButton) nextMatchButton.disabled = currentMarks.length === 0;
    } else if (searchMeta) {
      searchMeta.style.display = 'none';
      searchMeta.textContent = '';
      if (searchCount) searchCount.textContent = `章节 ${tocLinks.length}`;
      if (nextMatchButton) nextMatchButton.disabled = true;
    }
  }

  if (searchInput) {
    searchInput.addEventListener('input', function () {
      runSearch(searchInput.value);
    });
  }

  if (nextMatchButton) {
    nextMatchButton.addEventListener('click', function () {
      if (!currentMarks.length) return;
      currentMarkIndex = (currentMarkIndex + 1) % currentMarks.length;
      currentMarks[currentMarkIndex].scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
    nextMatchButton.disabled = true;
  }

  if (toggleTocButton && sidebar) {
    toggleTocButton.addEventListener('click', function () {
      sidebar.classList.toggle('collapsed');
      toggleTocButton.textContent = sidebar.classList.contains('collapsed') ? '展开目录' : '折叠目录';
    });
  }

  if (searchCount) searchCount.textContent = `章节 ${tocLinks.length}`;

  if (!('IntersectionObserver' in window) || sections.length === 0) return;
  const map = new Map(tocLinks.map(link => [link.getAttribute('href').slice(1), link]));
  const observer = new IntersectionObserver((entries) => {
    const visible = entries
      .filter(entry => entry.isIntersecting)
      .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
    if (!visible.length) return;
    const id = visible[0].target.id;
    tocLinks.forEach(link => link.classList.toggle('active', link === map.get(id)));
  }, { rootMargin: '-20% 0px -65% 0px', threshold: [0, 1] });
  sections.forEach(section => observer.observe(section));
});
</script>
"""

GLOBAL_SEARCH_SCRIPT = """
<script>
document.addEventListener('DOMContentLoaded', function () {
  const input = document.getElementById('global-search');
  const meta = document.getElementById('global-search-meta');
  const cards = Array.from(document.querySelectorAll('.result-card'));
  if (!input || !meta || cards.length === 0) return;

  function run() {
    const keyword = input.value.trim().toLowerCase();
    let visible = 0;
    cards.forEach(card => {
      const hay = (card.getAttribute('data-search') || '').toLowerCase();
      const hit = !keyword || hay.includes(keyword);
      card.hidden = !hit;
      if (hit) visible += 1;
    });
    meta.textContent = keyword ? `找到 ${visible} 个匹配文档` : `共 ${cards.length} 个文档`;
  }

  input.addEventListener('input', run);
  run();
});
</script>
"""


def is_topology_block(text: str) -> bool:
    cues = ["---", "==", "-->", "<--", "PC", "SW", "AR", "CE", "PE", "Internet", "VLAN"]
    return any(cue in text for cue in cues)


def parse_topology(text: str) -> list[list[str]]:
    rows = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        nodes = []
        for node in re.split(r"\s*(?:---|===|----|-->|<--|->|<-|\|)\s*", line):
            clean = node.strip().strip("-+> ")
            if clean:
                nodes.append(clean)
        if len(nodes) >= 2:
            rows.append(nodes)
    return rows


def build_svg(text: str) -> str:
    rows = parse_topology(text)
    if not rows:
        return ""
    node_order = []
    for row in rows:
        for node in row:
            if node not in node_order:
                node_order.append(node)
    cols = min(max(len(node_order), 2), 5)
    gap_x = 150
    gap_y = 90
    start_x = 90
    start_y = 70
    positions = {}
    for idx, node in enumerate(node_order):
        col = idx % cols
        row = idx // cols
        positions[node] = (start_x + col * gap_x, start_y + row * gap_y)
    width = max(720, start_x * 2 + (cols - 1) * gap_x)
    rows_count = max(1, (len(node_order) - 1) // cols + 1)
    height = max(220, start_y * 2 + (rows_count - 1) * gap_y)

    edges = []
    seen = set()
    for row in rows:
        for a, b in zip(row, row[1:]):
            key = tuple(sorted((a, b)))
            if key not in seen:
                seen.add(key)
                edges.append((a, b))

    parts = [
        f'<svg viewBox="0 0 {width} {height}" class="diagram-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="network topology diagram">',
        '<defs><filter id="s" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#94a3b8" flood-opacity=".18"/></filter></defs>',
        '<rect x="0" y="0" width="100%" height="100%" fill="#fcfffe"/>',
    ]
    for a, b in edges:
        x1, y1 = positions[a]
        x2, y2 = positions[b]
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#94a3b8" stroke-width="4" stroke-linecap="round"/>')
    for node, (x, y) in positions.items():
        label = html.escape(node)
        parts.append(f'<rect x="{x-48}" y="{y-22}" width="96" height="44" rx="14" fill="#ffffff" stroke="#0f766e" stroke-width="2" filter="url(#s)"/>')
        parts.append(f'<text x="{x}" y="{y+5}" text-anchor="middle" font-size="14" font-family="Segoe UI, Microsoft YaHei, sans-serif" fill="#0f172a">{label}</text>')
    parts.append("</svg>")
    return "".join(parts)


def inline_format(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    return escaped


def slugify(text: str) -> str:
    slug = re.sub(r"<[^>]+>", "", text)
    slug = re.sub(r"[^\w\u4e00-\u9fff\s-]", "", slug, flags=re.UNICODE).strip().lower()
    slug = re.sub(r"[\s-]+", "-", slug)
    return slug or "section"


def render_table(lines: list[str]) -> str:
    rows = []
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        rows.append(cells)
    if len(rows) < 2:
        return "\n".join(f"<p>{inline_format(x)}</p>" for x in lines)
    header = rows[0]
    body = [r for r in rows[2:] if any(cell for cell in r)]
    out = ["<table><thead><tr>"]
    out.extend(f"<th>{inline_format(cell)}</th>" for cell in header)
    out.append("</tr></thead><tbody>")
    for row in body:
        out.append("<tr>")
        out.extend(f"<td>{inline_format(cell)}</td>" for cell in row)
        out.append("</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def render_code_block(code: str) -> str:
    escaped = html.escape(code.strip("\n"))
    if is_topology_block(code):
        svg = build_svg(code)
        if not svg:
            return f"<pre><code>{escaped}</code></pre>"
        return (
            '<section class="diagram">'
            '<div class="diagram-head"><strong>拓扑示意</strong><span>自动从文档中的结构文本生成</span></div>'
            '<div class="diagram-body"><div class="diagram-grid">'
            f'<div>{svg}</div>'
            f'<div class="diagram-text"><pre><code>{escaped}</code></pre></div>'
            "</div></div></section>"
        )
    return f"<pre><code>{escaped}</code></pre>"


def markdown_to_html(text: str) -> tuple[str, list[tuple[int, str, str]]]:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    out: list[str] = []
    headings: list[tuple[int, str, str]] = []
    paragraph: list[str] = []
    list_type = None
    table_lines: list[str] = []
    in_code = False
    code_lines: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            joined = " ".join(x.strip() for x in paragraph if x.strip())
            if joined:
                out.append(f"<p>{inline_format(joined)}</p>")
            paragraph = []

    def flush_list() -> None:
        nonlocal list_type
        if list_type:
            out.append(f"</{list_type}>")
            list_type = None

    def flush_table() -> None:
        nonlocal table_lines
        if table_lines:
            out.append(render_table(table_lines))
            table_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            flush_paragraph()
            flush_list()
            flush_table()
            if in_code:
                out.append(render_code_block("\n".join(code_lines)))
                code_lines = []
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue
        if not stripped:
            flush_paragraph()
            flush_list()
            flush_table()
            continue
        if stripped == "---":
            flush_paragraph()
            flush_list()
            flush_table()
            out.append("<hr>")
            continue
        if stripped.startswith("|"):
            flush_paragraph()
            flush_list()
            table_lines.append(line)
            continue
        flush_table()
        m = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if m:
            flush_paragraph()
            flush_list()
            level = len(m.group(1))
            raw_text = m.group(2).strip()
            content = inline_format(raw_text)
            anchor = slugify(raw_text)
            headings.append((level, raw_text, anchor))
            out.append(f'<h{level} id="{anchor}">{content}</h{level}>')
            continue
        m = re.match(r"^[-*]\s+(.*)$", stripped)
        if m:
            flush_paragraph()
            if list_type != "ul":
                flush_list()
                out.append("<ul>")
                list_type = "ul"
            out.append(f"<li>{inline_format(m.group(1))}</li>")
            continue
        m = re.match(r"^\d+\.\s+(.*)$", stripped)
        if m:
            flush_paragraph()
            if list_type != "ol":
                flush_list()
                out.append("<ol>")
                list_type = "ol"
            out.append(f"<li>{inline_format(m.group(1))}</li>")
            continue
        paragraph.append(line)

    flush_paragraph()
    flush_list()
    flush_table()
    return "\n".join(out), headings


def extract_intro(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and not stripped.startswith("|") and not stripped.startswith("```"):
            return stripped[:120]
    return "Markdown 内容已转换为更适合浏览阅读的简约 HTML 页面。"


def build_toc(headings: list[tuple[int, str, str]]) -> str:
    if not headings:
        return '<div class="toc"><a href="#top" class="lv1">返回顶部</a></div>'
    items = ['<div class="toc">', '<a href="#top" class="lv1">返回顶部</a>']
    for level, text, anchor in headings:
        level_class = f"lv{min(level,4)}"
        items.append(f'<a href="#{anchor}" class="{level_class}" data-title="{html.escape(text)}">{html.escape(text)}</a>')
    items.append("</div>")
    return "".join(items)


def build_pager(prev_item: tuple[str, str] | None, next_item: tuple[str, str] | None) -> str:
    left = (
        f'<a href="{html.escape(prev_item[1])}"><span class="pager-label">上一页</span>{html.escape(prev_item[0])}</a>'
        if prev_item else
        '<span><span class="pager-label">上一页</span>已经是第一页</span>'
    )
    right = (
        f'<a href="{html.escape(next_item[1])}"><span class="pager-label">下一页</span>{html.escape(next_item[0])}</a>'
        if next_item else
        '<span><span class="pager-label">下一页</span>已经是最后一页</span>'
    )
    return f'<nav class="pager">{left}{right}</nav>'


def build_page(title: str, body: str, intro: str, toc_html: str, pager_html: str = "") -> str:
    quick_links = (
        '<nav class="quick-links">'
        '<a href="index.html">返回目录</a>'
        '<a href="总手册.html">打开总手册</a>'
        '<a href="全站搜索.html">打开全站搜索</a>'
        '</nav>'
    )
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>{CSS}</style>
</head>
<body id="top">
  <div class="page">
    <div class="layout">
      <aside class="sidebar">
        <h2 class="sidebar-title">目录导航</h2>
        <p class="sidebar-note">适合连续阅读，也方便快速跳到章节。</p>
        <p class="toc-count" id="search-count"></p>
        <div class="search">
          <input id="doc-search" type="search" placeholder="搜索关键词">
          <div class="search-tools">
            <button type="button" class="tool-btn" id="next-match">下一个匹配</button>
            <button type="button" class="tool-btn" id="toggle-toc">折叠目录</button>
          </div>
        </div>
        {toc_html}
      </aside>
      <div class="main">
        <header class="hero">
          <div class="eyebrow">Markdown To HTML</div>
          <h1>{html.escape(title)}</h1>
          <p class="subtitle">{html.escape(intro)}</p>
          {quick_links}
        </header>
        <main class="content">
          <p class="search-meta" id="search-meta"></p>
          {body}
          {pager_html}
        </main>
      </div>
    </div>
    <div class="footer">本页为本地自动生成，适合直接浏览、打印或继续二次修改。</div>
  </div>
  {SCRIPT}
</body>
</html>
"""


def build_global_search_page(cards_html: str, count: int) -> str:
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>全站搜索</title>
  <style>{CSS}</style>
</head>
<body id="top">
  <div class="page">
    <header class="hero">
      <div class="eyebrow">Global Search</div>
      <h1>全站搜索</h1>
      <p class="subtitle">一次搜索当前目录下全部已转换文档，快速定位目标内容。</p>
    </header>
    <main class="content">
      <div class="search">
        <input id="global-search" type="search" placeholder="输入关键词，例如 OSPF、MPLS、故障排查">
      </div>
      <p class="search-meta" id="global-search-meta" style="display:block">共 {count} 个文档</p>
      <div class="global-search-list">
        {cards_html}
      </div>
    </main>
    <div class="footer">本页为本地自动生成，可作为全部 HTML 文档的统一搜索入口。</div>
  </div>
  {GLOBAL_SEARCH_SCRIPT}
</body>
</html>
"""


def strip_html(html_text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html_text)
    return re.sub(r"\s+", " ", text).strip()


def build_search_excerpt(text: str, limit: int = 140) -> str:
    return text[:limit] + ("..." if len(text) > limit else "")


def main() -> None:
    base = Path(".")
    md_files = sorted(base.glob("*.md"))
    docs = []
    for md_file in md_files:
        text = md_file.read_text(encoding="utf-8")
        title_match = re.search(r"^#\s+(.+)$", text, re.M)
        title = title_match.group(1).strip() if title_match else md_file.stem
        body, headings = markdown_to_html(text)
        out = md_file.with_suffix(".html")
        docs.append({
            "title": title,
            "body": body,
            "intro": extract_intro(text),
            "toc": build_toc(headings),
            "out": out.name,
        })

    for idx, doc in enumerate(docs):
        prev_item = None if idx == 0 else (docs[idx - 1]["title"], docs[idx - 1]["out"])
        next_item = None if idx == len(docs) - 1 else (docs[idx + 1]["title"], docs[idx + 1]["out"])
        page = build_page(doc["title"], doc["body"], doc["intro"], doc["toc"], build_pager(prev_item, next_item))
        Path(doc["out"]).write_text(page, encoding="utf-8")
        print(f"generated: {doc['out']}")

    index_items = "\n".join(
        f'<div class="note"><h3><a href="{html.escape(filename)}" style="color:#0f766e;text-decoration:none">{html.escape(title)}</a></h3><p>{html.escape(intro)}</p></div>'
        for title, filename, intro in [(d["title"], d["out"], d["intro"]) for d in docs]
    )
    index_entries = (
        '<div class="entry-grid">'
        '<a class="entry-card" href="总手册.html"><strong>总手册</strong><span>把全部内容合并成一个单页版本，适合连续阅读和打印。</span></a>'
        '<a class="entry-card" href="全站搜索.html"><strong>全站搜索</strong><span>一次搜索全部文档，快速定位目标主题和页面。</span></a>'
        '</div>'
    )
    index_body = (
        "<p>下面是当前目录中已转换完成的 HTML 文档，点击即可查看。页面统一为简约风格，并保留了代码块、表格和拓扑示意。</p>"
        + index_entries
        + index_items
    )
    index_page = build_page("Markdown 文档浏览目录", index_body, "当前目录下的 Markdown 已批量转换为简约 HTML 页面。", '<div class="toc"><a href="#top" class="lv1">返回顶部</a><a href="#top" class="lv2" data-title="目录首页">目录首页</a></div>')
    Path("index.html").write_text(index_page, encoding="utf-8")
    print("generated: index.html")

    book_parts = []
    book_toc = ['<div class="toc"><a href="#top" class="lv1">返回顶部</a>']
    for idx, doc in enumerate(docs, start=1):
        section_id = f"book-{idx}"
        book_toc.append(f'<a href="#{section_id}" class="lv2" data-title="{html.escape(doc["title"])}">{html.escape(doc["title"])}</a>')
        book_parts.append(f'<section class="book-section"><h2 id="{section_id}">{html.escape(doc["title"])}</h2>{doc["body"]}</section>')
    book_toc.append("</div>")
    book_body = "<p>这是将当前目录下全部 Markdown 文档合并后的总手册版本，适合连续阅读、打印或统一归档。</p>" + "".join(book_parts)
    book_page = build_page("HCIE Datacom 总手册", book_body, "已将全部文档整合为单页阅读版本。", "".join(book_toc))
    Path("总手册.html").write_text(book_page, encoding="utf-8")
    print("generated: 总手册.html")

    search_cards = []
    for doc in docs:
        plain = strip_html(doc["body"])
        excerpt = build_search_excerpt(plain)
        search_cards.append(
            f'<article class="result-card" data-search="{html.escape(doc["title"] + " " + plain)}">'
            f'<h3><a class="result-link" href="{html.escape(doc["out"])}">{html.escape(doc["title"])}</a></h3>'
            f'<p>{html.escape(excerpt)}</p>'
            f'</article>'
        )
    global_search_page = build_global_search_page("".join(search_cards), len(search_cards))
    Path("全站搜索.html").write_text(global_search_page, encoding="utf-8")
    print("generated: 全站搜索.html")


if __name__ == "__main__":
    main()
