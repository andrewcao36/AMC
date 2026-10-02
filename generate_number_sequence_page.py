"""Generate the AMC 10 number-sequence problem-link index."""

from pathlib import Path

from generate_statistics_pages import render_page


ROOT = Path(__file__).parent

AMC10_SEQUENCE_CONTESTS = [
    (2000, "2000_AMC_10_Problems", "2000 AMC 10", [6, 12, 23]),
    (2002, "2002_AMC_10P_Problems", "2002 AMC 10P", [5]),
    (2002, "2002_AMC_10A_Problems", "2002 AMC 10A", [22]),
    (2002, "2002_AMC_10B_Problems", "2002 AMC 10B", [19, 23]),
    (2003, "2003_AMC_10B_Problems", "2003 AMC 10B", [8, 24]),
    (2004, "2004_AMC_10A_Problems", "2004 AMC 10A", [18]),
    (2004, "2004_AMC_10B_Problems", "2004 AMC 10B", [19, 21]),
    (2005, "2005_AMC_10A_Problems", "2005 AMC 10A", [17]),
    (2005, "2005_AMC_10B_Problems", "2005 AMC 10B", [11]),
    (2006, "2006_AMC_10A_Problems", "2006 AMC 10A", [19]),
    (2006, "2006_AMC_10B_Problems", "2006 AMC 10B", [18]),
    (2007, "2007_AMC_10A_Problems", "2007 AMC 10A", [22]),
    (2008, "2008_AMC_10A_Problems", "2008 AMC 10A", [22]),
    (2008, "2008_AMC_10B_Problems", "2008 AMC 10B", [11, 13]),
    (2009, "2009_AMC_10A_Problems", "2009 AMC 10A", [9, 15]),
    (2009, "2009_AMC_10B_Problems", "2009 AMC 10B", [14]),
    (2010, "2010_AMC_10A_Problems", "2010 AMC 10A", [25]),
    (2010, "2010_AMC_10B_Problems", "2010 AMC 10B", [24]),
    (2011, "2011_AMC_10A_Problems", "2011 AMC 10A", [4, 17]),
    (2011, "2011_AMC_10B_Problems", "2011 AMC 10B", [10, 25]),
    (2012, "2012_AMC_10A_Problems", "2012 AMC 10A", [10]),
    (2013, "2013_AMC_10B_Problems", "2013 AMC 10B", [13, 19, 21]),
    (2014, "2014_AMC_10A_Problems", "2014 AMC 10A", [24]),
    (2015, "2015_AMC_10A_Problems", "2015 AMC 10A", [7]),
    (2016, "2016_AMC_10A_Problems", "2016 AMC 10A", [8, 10]),
    (2016, "2016_AMC_10B_Problems", "2016 AMC 10B", [16, 24]),
    (2017, "2017_AMC_10A_Problems", "2017 AMC 10A", [13]),
    (2017, "2017_AMC_10B_Problems", "2017 AMC 10B", [17]),
    (2018, "2018_AMC_10B_Problems", "2018 AMC 10B", [13, 20]),
    (2019, "2019_AMC_10A_Problems", "2019 AMC 10A", [15]),
    (2019, "2019_AMC_10B_Problems", "2019 AMC 10B", [4, 24, 25]),
    (2020, "2020_AMC_10B_Problems", "2020 AMC 10B", [15]),
    (2021, "2021_AMC_10A_Problems", "2021 AMC 10A", [4, 20]),
    (2022, "2022_AMC_10A_Problems", "2022 AMC 10A", [20]),
    (2022, "2022_AMC_10B_Problems", "2022 AMC 10B", [6, 15, 25]),
    (2023, "2023_AMC_10B_Problems", "2023 AMC 10B", [6, 23]),
    (2024, "2024_AMC_10A_Problems", "2024 AMC 10A", [10, 19, 21]),
    (2024, "2024_AMC_10B_Problems", "2024 AMC 10B", [4, 23]),
    (2025, "2025_AMC_10A_Problems", "2025 AMC 10A", [5, 11, 13]),
    (2025, "2025_AMC_10B_Problems", "2025 AMC 10B", [2, 17]),
]


def main() -> None:
    content = render_page(
        level=10,
        contests=AMC10_SEQUENCE_CONTESTS,
        end_year=2025,
        topic_heading="number sequence",
        topic_description=(
            "Browse number-sequence problems from AMC 10 contests from 2000 "
            "through 2025. Topics include arithmetic and geometric sequences, "
            "recurrences, Fibonacci-type patterns, periodic behavior, and series."
        ),
        selection_note=(
            "Selection includes arithmetic and geometric progressions, recursive "
            "and Fibonacci-type sequences, periodic sequences, explicit terms, "
            "and partial sums."
        ),
    )
    output = ROOT / "amc10_number_sequence_problem_links.html"
    output.write_text(content, encoding="utf-8", newline="\n")
    print(f"Wrote {output.name}")


if __name__ == "__main__":
    main()
