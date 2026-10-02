"""Generate AMC 8 and AMC 10 statistics problem-link indexes."""

from __future__ import annotations

from collections import defaultdict
from html import escape
from pathlib import Path
import re


ROOT = Path(__file__).parent

AMC8_PROBLEMS = {
    1999: [4, 13],
    2000: [4, 23],
    2001: [13, 21],
    2002: [3, 7, 8, 9, 10, 18],
    2003: [7],
    2004: [9, 11],
    2005: [12],
    2006: [8, 12, 25],
    2007: [1, 2, 7],
    2008: [8, 10, 15],
    2009: [21],
    2010: [3, 4],
    2011: [4, 11],
    2012: [7, 11, 22],
    2013: [5],
    2014: [3, 24],
    2015: [5, 13],
    2016: [3, 6],
    2017: [2],
    2018: [8, 13],
    2019: [7, 10],
    2020: [2, 14, 20],
    2022: [15, 16, 19],
    2023: [20],
    2025: [7, 9, 13, 14],
    2026: [22],
}

AMC10_CONTESTS = [
    (2000, "2000_AMC_10_Problems", "2000 AMC 10", [14, 22, 23]),
    (2001, "2001_AMC_10_Problems", "2001 AMC 10", [1, 16]),
    (2002, "2002_AMC_10A_Problems", "2002 AMC 10A", [9, 21]),
    (2002, "2002_AMC_10B_Problems", "2002 AMC 10B", [3, 25]),
    (2004, "2004_AMC_10A_Problems", "2004 AMC 10A", [14]),
    (2005, "2005_AMC_10A_Problems", "2005 AMC 10A", [6]),
    (2005, "2005_AMC_10B_Problems", "2005 AMC 10B", [19]),
    (2007, "2007_AMC_10A_Problems", "2007 AMC 10A", [10]),
    (2007, "2007_AMC_10B_Problems", "2007 AMC 10B", [16]),
    (2008, "2008_AMC_10B_Problems", "2008 AMC 10B", [13]),
    (2010, "2010_AMC_10A_Problems", "2010 AMC 10A", [1]),
    (2010, "2010_AMC_10B_Problems", "2010 AMC 10B", [4, 14, 17]),
    (2011, "2011_AMC_10A_Problems", "2011 AMC 10A", [3, 5]),
    (2011, "2011_AMC_10B_Problems", "2011 AMC 10B", [2]),
    (2012, "2012_AMC_10A_Problems", "2012 AMC 10A", [5, 13]),
    (2013, "2013_AMC_10B_Problems", "2013 AMC 10B", [3, 6]),
    (2014, "2014_AMC_10A_Problems", "2014 AMC 10A", [5, 10]),
    (2014, "2014_AMC_10B_Problems", "2014 AMC 10B", [18]),
    (2015, "2015_AMC_10A_Problems", "2015 AMC 10A", [5]),
    (2016, "2016_AMC_10A_Problems", "2016 AMC 10A", [7]),
    (2016, "2016_AMC_10B_Problems", "2016 AMC 10B", [5]),
    (2017, "2017_AMC_10B_Problems", "2017 AMC 10B", [25]),
    (2018, "2018_AMC_10B_Problems", "2018 AMC 10B", [14]),
    (2019, "2019_AMC_10A_Problems", "2019 AMC 10A", [12]),
    (2019, "2019_AMC_10B_Problems", "2019 AMC 10B", [13]),
    (2020, "2020_AMC_10A_Problems", "2020 AMC 10A", [2, 11]),
    (2021, "2021_AMC_10A_Problems", "2021 AMC 10A", [5, 16, 22]),
    (2021, "2021_AMC_10B_Problems", "2021 AMC 10B", [6, 19]),
    (2021, "2021_Fall_AMC_10A_Problems", "2021 Fall AMC 10A", [10]),
    (2022, "2022_AMC_10A_Problems", "2022 AMC 10A", [8]),
    (2022, "2022_AMC_10B_Problems", "2022 AMC 10B", [10]),
    (2023, "2023_AMC_10A_Problems", "2023 AMC 10A", [10]),
    (2024, "2024_AMC_10A_Problems", "2024 AMC 10A", [12]),
    (2024, "2024_AMC_10B_Problems", "2024 AMC 10B", [9, 15]),
    (2025, "2025_AMC_10A_Problems", "2025 AMC 10A", [4]),
    (2025, "2025_AMC_10B_Problems", "2025 AMC 10B", [17]),
]

STYLE = """
:root{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;color:#183149;background:#f5f8fa}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0}
a{color:#086779}a:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid #e7a33d;outline-offset:3px}
.wrap{max-width:1120px;margin:auto;padding:0 24px}
header{background:#17324b;color:#fff;padding:52px 0 46px}
header .eyebrow{text-transform:uppercase;letter-spacing:.13em;color:#9fced5;font-size:.82rem;font-weight:700}
h1{font-size:clamp(2rem,5vw,3.35rem);letter-spacing:-.035em;line-height:1.08;margin:13px 0 18px}
header p{max-width:740px;color:#d9e6eb;line-height:1.55;margin:0}
.stats{display:flex;flex-wrap:wrap;gap:12px;margin-top:27px}
.stat{border:1px solid #496b7b;border-radius:9px;padding:10px 15px;background:#203f57}
.stat b{font-size:1.25rem}.stat span{display:block;color:#bfdae1;font-size:.8rem}
.toolbar{position:sticky;top:0;z-index:5;background:#fff;border-bottom:1px solid #d7e3e8;box-shadow:0 3px 12px #17324b0c;padding:14px 0}
.toolbar .wrap{display:flex;flex-wrap:wrap;gap:12px;align-items:center}
input,select{font:inherit;border:1px solid #afc4cd;border-radius:8px;background:#fff;color:#17324b;padding:10px 12px;min-height:44px}
input{flex:1 1 280px}select{flex:0 1 175px}.shown{margin-left:auto;color:#526b78;font-size:.9rem}
main{padding:22px 0 56px}.jump{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 25px}
.jump a{font-size:.82rem;text-decoration:none;background:#e5f0f2;border:1px solid #ccdee2;border-radius:6px;padding:6px 9px}
.year{margin:25px 0 30px;scroll-margin-top:90px}.year>h2{font-size:1.75rem;margin:0 0 12px;letter-spacing:-.025em}
.year-count{font-size:.9rem;font-weight:400;color:#657a86;margin-left:9px}
.contest{background:#fff;border:1px solid #d7e3e8;border-radius:12px;padding:20px 22px;margin:12px 0;box-shadow:0 4px 14px #18314909}
.contest h3{font-size:1.05rem;margin:0 0 13px}.contest .count{color:#657a86;font-weight:400;font-size:.85rem;margin-left:6px}
.links{display:flex;flex-wrap:wrap;gap:9px}.problem{display:inline-flex;align-items:center;justify-content:center;min-width:104px;text-decoration:none;font-size:.92rem;font-weight:600;border:1px solid #bad3d9;border-radius:8px;background:#f3fafb;padding:9px 12px;transition:background .15s,border-color .15s}
.problem:hover{background:#dbeff2;border-color:#6aabb7}.problem.opened{background:#ffe3a3;border-color:#d28a16;color:#684000;box-shadow:inset 0 0 0 1px #d28a16}.problem.opened:hover{background:#ffd77a}.problem::after{content:'↗';font-size:.8em;margin-left:7px;color:#5a8d98}
.empty{display:none;padding:40px 0;color:#526b78}.notes{border-top:1px solid #d7e3e8;color:#526b78;line-height:1.55;padding:24px 0 36px;font-size:.9rem}
.notes p{margin:7px 0}.hidden{display:none!important}
@media(max-width:570px){.wrap{padding:0 16px}header{padding:35px 0}.toolbar{position:static}.shown{margin-left:0;width:100%}.contest{padding:16px}.problem{min-width:calc(50% - 5px)}}
""".strip()

SCRIPT = r"""
const search=document.getElementById('search');
const yearFilter=document.getElementById('year-filter');
const shown=document.getElementById('shown');
const empty=document.getElementById('empty');
const yearSections=[...document.querySelectorAll('.year')];
function update(){
  const q=search.value.trim().toLowerCase();
  const selectedYear=yearFilter.value;
  let total=0;
  for(const year of yearSections){
    let yearTotal=0;
    for(const contest of year.querySelectorAll('.contest')){
      let contestTotal=0;
      const name=contest.dataset.contest;
      const compact=name.replace(/\s+/g,'');
      const alias=contest.dataset.alias;
      const yearMatches=!selectedYear||year.dataset.year===selectedYear;
      for(const link of contest.querySelectorAll('.problem')){
        const n=link.dataset.number;
        const matches=!q||name.includes(q)||compact.includes(q)||alias.includes(q)||('problem '+n).includes(q)||('problem'+n).includes(q)||q===n;
        const show=yearMatches&&matches;
        link.classList.toggle('hidden',!show);
        if(show)contestTotal++;
      }
      contest.classList.toggle('hidden',contestTotal===0);
      yearTotal+=contestTotal;
    }
    year.classList.toggle('hidden',yearTotal===0);
    total+=yearTotal;
  }
  shown.textContent=`Showing ${total} problem${total===1?'':'s'}`;
  empty.style.display=total?'none':'block';
}
search.addEventListener('input',update);
yearFilter.addEventListener('change',update);
const openedStorageKey='amc-opened-problem';
let openedProblem='';
try{
  openedProblem=localStorage.getItem(openedStorageKey)||'';
  if(!openedProblem){
    const previous=JSON.parse(localStorage.getItem('amc-opened-problems')||'[]');
    if(Array.isArray(previous))openedProblem=previous.at(-1)||'';
  }
}catch{}
function problemKey(link){return link.href}
function markOpened(event){
  const link=event.target.closest('.problem');
  if(!link)return;
  document.querySelector('.problem.opened')?.classList.remove('opened');
  link.classList.add('opened');
  try{
    localStorage.setItem(openedStorageKey,problemKey(link));
    localStorage.removeItem('amc-opened-problems');
  }catch{}
}
for(const link of document.querySelectorAll('.problem')){
  if(problemKey(link)===openedProblem)link.classList.add('opened');
}
document.addEventListener('click',markOpened);
document.addEventListener('contextmenu',markOpened);
""".strip()


def count_text(count: int) -> str:
    return f"{count} problem{'' if count == 1 else 's'}"


def problem_link(title: str, display: str, number: int) -> str:
    label = f"{display} Problem {number}"
    url = f"https://artofproblemsolving.com/wiki/index.php?title={title}/Problem_{number}"
    return (
        f'<a class="problem" href="{escape(url)}" target="_blank" '
        f'rel="noopener noreferrer" data-number="{number}" '
        f'aria-label="{escape(label)}; opens on Art of Problem Solving">'
        f"Problem {number}</a>"
    )


def render_page(
    *,
    level: int,
    contests: list[tuple[int, str, str, list[int]]],
    end_year: int,
    topic_heading: str = "statistics",
    topic_description: str | None = None,
    selection_note: str | None = None,
) -> str:
    grouped: dict[int, list[tuple[str, str, list[int]]]] = defaultdict(list)
    for year, title, display, numbers in contests:
        grouped[year].append((title, display, sorted(set(numbers))))

    years = sorted(grouped)
    total = sum(len(numbers) for _, _, _, numbers in contests)
    contest_count = len(contests)
    archive = f"AMC_{level}_Problems_and_Solutions"
    title = f"AMC {level} {topic_heading.title()} Problem Links, {years[0]}–{end_year}"
    description = topic_description or (
        f"Browse statistics and data-analysis problems from AMC {level} contests "
        f"from {years[0]} through {end_year}. Topics include mean, median, mode, "
        "range, weighted averages, and interpreting data or graphs."
    )
    note = selection_note or (
        "Selection includes arithmetic and weighted means, median, mode, range, "
        "frequency or data displays, and graph interpretation. Pure probability "
        "problems are excluded unless data analysis is central."
    )

    year_options = "".join(
        f'<option value="{year}">{year}</option>' for year in years
    )
    jump_links = "".join(f'<a href="#year-{year}">{year}</a>' for year in years)

    sections = []
    for year in years:
        year_total = sum(len(numbers) for _, _, numbers in grouped[year])
        contests_html = []
        for contest_title, display, numbers in grouped[year]:
            links = "".join(
                problem_link(contest_title, display, number) for number in numbers
            )
            alias = re.sub(r"\s*amc\s*(?:8|10)", "", display.lower()).replace(" ", "")
            contests_html.append(
                f'<section class="contest" data-contest="{escape(display.lower())}" '
                f'data-alias="{escape(alias)}"><h3>{escape(display)}'
                f'<span class="count">{count_text(len(numbers))}</span></h3>'
                f'<div class="links">{links}</div></section>'
            )
        sections.append(
            f'<section class="year" id="year-{year}" data-year="{year}">'
            f'<h2>{year}<span class="year-count">{count_text(year_total)}</span></h2>'
            f'{"".join(contests_html)}</section>'
        )

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<title>{title}</title>
<style>
{STYLE}
</style>
</head>
<body>
<header><div class="wrap">
<div class="eyebrow">Direct links to the source pages</div>
<h1>AMC {level} {escape(topic_heading)} problems</h1>
<p>{escape(description)}</p>
<div class="stats"><div class="stat"><b>{total}</b><span>problem links</span></div><div class="stat"><b>{contest_count}</b><span>contest versions</span></div><div class="stat"><b>{len(years)}</b><span>years represented</span></div></div>
</div></header>
<div class="toolbar"><div class="wrap">
<input id="search" type="search" placeholder="Search year, contest, or problem number" aria-label="Search year, contest, or problem number">
<select id="year-filter" aria-label="Filter by year"><option value="">All years</option>{year_options}</select>
<span class="shown" id="shown">Showing {total} problems</span>
</div></div>
<main class="wrap">
<nav class="jump" aria-label="Jump to year">{jump_links}</nav>
{"".join(sections)}
<p class="empty" id="empty">No matching problems. Try a year, contest label, or problem number.</p>
</main>
<footer class="notes"><div class="wrap">
<p>Source: <a href="https://artofproblemsolving.com/wiki/index.php?title={archive}" target="_blank" rel="noopener noreferrer">AoPS AMC {level} archive</a>. The problem and solution content remains on AoPS; this page is a navigation index.</p>
<p>{escape(note)}</p>
</div></footer>
<script>
{SCRIPT}
</script>
</body>
</html>
"""


def main() -> None:
    amc8_contests = [
        (year, f"{year}_AMC_8_Problems", f"{year} AMC 8", numbers)
        for year, numbers in sorted(AMC8_PROBLEMS.items())
    ]
    outputs = {
        "amc8_statistics_problem_links.html": render_page(
            level=8, contests=amc8_contests, end_year=2026
        ),
        "amc10_statistics_problem_links.html": render_page(
            level=10, contests=AMC10_CONTESTS, end_year=2025
        ),
    }
    for filename, content in outputs.items():
        (ROOT / filename).write_text(content, encoding="utf-8", newline="\n")
        print(f"Wrote {filename}")


if __name__ == "__main__":
    main()
