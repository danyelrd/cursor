#!/usr/bin/env python3
"""Senior-level pubmat SVG system - clean hierarchy, restrained palette, no FX clutter."""

from pathlib import Path

import svgwrite

OUT = Path(__file__).resolve().parent
W, H = 1080, 1350  # portrait pubmat
SQ = 1080  # square beauty


def rect(dwg, x, y, w, h, fill, opacity=1.0):
    dwg.add(
        dwg.rect(
            insert=(x, y),
            size=(w, h),
            fill=fill,
            opacity=opacity,
        )
    )


def text(
    dwg,
    x,
    y,
    content,
    size,
    fill="#111",
    weight="normal",
    anchor="start",
    family="Arial, Helvetica, sans-serif",
    letter_spacing="0",
):
    dwg.add(
        dwg.text(
            content,
            insert=(x, y),
            fill=fill,
            font_size=size,
            font_family=family,
            font_weight=weight,
            text_anchor=anchor,
            letter_spacing=letter_spacing,
        )
    )


def footer_block(dwg, y, lines, bg="#111827", fg="#F9FAFB"):
    rect(dwg, 0, y, W, H - y, bg)
    ty = y + 56
    for i, line in enumerate(lines):
        text(
            dwg,
            72,
            ty + i * 38,
            line,
            22 if i == 0 else 18,
            fill=fg if i == 0 else "#D1D5DB",
            weight="bold" if i == 0 else "normal",
        )


def sk_panique_kk_assembly():
    dwg = svgwrite.Drawing(str(OUT / "01-sk-panique-kk-assembly-2025.svg"), size=(f"{W}px", f"{H}px"), viewBox=f"0 0 {W} {H}")
    # Palette: institutional navy + SK gold accent
    rect(dwg, 0, 0, W, H, "#F8FAFC")
    rect(dwg, 0, 0, W, 12, "#1E3A5F")
    rect(dwg, 72, 120, 936, 4, "#C9A227")
    text(dwg, 72, 100, "SANGGUNIANG KABATAAN", 20, "#64748B", weight="bold", letter_spacing="3")
    text(dwg, 72, 132, "Barangay Panique", 26, "#1E3A5F", weight="bold")
    text(dwg, 72, 280, "KK Assembly", 86, "#0F172A", weight="bold", family="Georgia, serif")
    text(dwg, 72, 360, "2025", 86, "#1E3A5F", weight="bold", family="Georgia, serif")
    text(dwg, 72, 420, "Kabataan Kontra Kahirapan", 24, "#475569")
    rect(dwg, 72, 470, 520, 2, "#C9A227")
    text(
        dwg,
        72,
        530,
        "Official youth assembly for SK Panique officers and\nbarangay youth representatives.",
        22,
        "#334155",
    )
    # Photo placeholder - editorial frame
    rect(dwg, 72, 600, 936, 420, "#E2E8F0")
    rect(dwg, 72, 600, 936, 420, "none", opacity=0)
    text(dwg, 540, 820, "Insert community / youth photo", 20, "#64748B", anchor="middle")
    footer_block(
        dwg,
        1060,
        [
            "Date: ____________________",
            "Venue: Panique Covered Court (edit as needed)",
            "Contact: SK Panique Official Page",
        ],
    )
    dwg.save()


def sk_panique_basketball():
    dwg = svgwrite.Drawing(str(OUT / "02-sk-panique-basketball-tournament.svg"), size=(f"{W}px", f"{H}px"), viewBox=f"0 0 {W} {H}")
    rect(dwg, 0, 0, W, H, "#0F172A")
    rect(dwg, 0, 0, W, 280, "#1D4ED8")
    text(dwg, 72, 88, "SANGGUNIANG KABATAAN - PANIQUE", 18, "#BFDBFE", weight="bold", letter_spacing="2")
    text(dwg, 72, 200, "Basketball", 78, "#FFFFFF", weight="bold", family="Georgia, serif")
    text(dwg, 72, 285, "Tournament", 78, "#FBBF24", weight="bold", family="Georgia, serif")
    text(dwg, 72, 360, "Inter-Barangay Youth Cup  |  2025", 24, "#E2E8F0")
    rect(dwg, 72, 400, 180, 6, "#FBBF24")
    # Info cards
    for i, (title, sub) in enumerate(
        [
            ("Open Category", "16-30 years old"),
            ("Registration", "Team of 5 + 2 reserves"),
            ("Format", "Round robin / Finals"),
        ]
    ):
        y = 460 + i * 130
        rect(dwg, 72, y, 936, 108, "#1E293B")
        text(dwg, 100, y + 42, title, 22, "#F8FAFC", weight="bold")
        text(dwg, 100, y + 78, sub, 18, "#94A3B8")
    footer_block(dwg, 980, ["March 2025 (edit date)", "Venue: ____________________", "Register via SK Panique"], bg="#020617")
    dwg.save()


def rsu_it_week():
    dwg = svgwrite.Drawing(str(OUT / "03-rsu-it-week-2025.svg"), size=(f"{W}px", f"{H}px"), viewBox=f"0 0 {W} {H}")
    rect(dwg, 0, 0, W, H, "#FFFFFF")
    rect(dwg, 0, 0, W, 340, "#0A4D68")
    text(dwg, 72, 95, "ROMBLON STATE UNIVERSITY", 17, "#BAE6FD", weight="bold", letter_spacing="2")
    text(dwg, 72, 175, "IT WEEK", 92, "#FFFFFF", weight="bold", family="Georgia, serif")
    text(dwg, 72, 265, "2025", 56, "#67E8F9", weight="bold")
    text(dwg, 72, 310, "College of Information Technology", 22, "#E0F2FE")
    rect(dwg, 72, 400, 936, 1, "#CBD5E1")
    schedule = [
        ("Day 1", "Opening / Tech Talk"),
        ("Day 2", "Hackathon"),
        ("Day 3", "Career Forum"),
        ("Day 4", "Closing / Awards"),
    ]
    y0 = 440
    for i, (day, evt) in enumerate(schedule):
        y = y0 + i * 110
        text(dwg, 72, y, day, 20, "#0A4D68", weight="bold")
        text(dwg, 200, y, evt, 24, "#0F172A", weight="bold")
        rect(dwg, 72, y + 20, 936, 1, "#E2E8F0")
    text(dwg, 72, 920, "Organized by BSIT students & faculty.", 20, "#64748B")
    text(dwg, 72, 960, "Venue: RSU Main Campus (edit)", 20, "#64748B")
    rect(dwg, 72, 1020, 936, 200, "#F1F5F9")
    text(dwg, 540, 1130, "#RSUITWeek2025", 28, "#0A4D68", anchor="middle", weight="bold")
    dwg.save()


def ivan_test_beauty():
    dwg = svgwrite.Drawing(str(OUT / "04-ivan-test-beauty-sample.svg"), size=(f"{SQ}px", f"{SQ}px"), viewBox=f"0 0 {SQ} {SQ}")
    rect(dwg, 0, 0, SQ, SQ, "#F7F3ED")
    rect(dwg, 0, 0, SQ, 8, "#A67C52")
    text(dwg, 72, 95, "IVAN TEST", 26, "#A67C52", weight="bold", letter_spacing="4")
    text(dwg, 72, 200, "Argan Oil", 72, "#2C2C2C", weight="bold", family="Georgia, serif")
    text(dwg, 72, 285, "Treatment Shampoo", 36, "#525252", family="Georgia, serif")
    rect(dwg, 72, 320, 120, 2, "#A67C52")
    text(dwg, 72, 365, "Shine / Smooth / Everyday care", 22, "#6B6B6B")
    rect(dwg, 560, 140, 448, 720, "#EDE8E0")
    text(dwg, 784, 520, "Product photo", 18, "#9CA3AF", anchor="middle")
    text(dwg, 72, 920, "Available at partner salons", 20, "#6B6B6B")
    text(dwg, 72, 1000, "ivan-test.ph  |  edit contact", 18, "#9CA3AF")
    dwg.save()


def nba_game_night():
    dwg = svgwrite.Drawing(str(OUT / "05-nba-game-night.svg"), size=(f"{W}px", f"{H}px"), viewBox=f"0 0 {W} {H}")
    rect(dwg, 0, 0, W, H, "#111111")
    rect(dwg, 72, 140, 936, 520, "#1F1F1F")
    text(dwg, 120, 320, "NBA", 140, "#FFFFFF", weight="bold", family="Georgia, serif")
    text(dwg, 120, 400, "GAME NIGHT", 52, "#EF4444", weight="bold", letter_spacing="6")
    text(dwg, 120, 470, "Live screening / Food specials", 22, "#D4D4D4")
    rect(dwg, 72, 720, 936, 1, "#404040")
    text(dwg, 72, 800, "Doors open 7:00 PM", 34, "#FAFAFA", weight="bold")
    text(dwg, 72, 860, "Feature matchup TBA", 24, "#A3A3A3")
    text(dwg, 72, 980, "Venue: ____________________", 22, "#737373")
    text(dwg, 72, 1180, "Fan event - not affiliated with the NBA.", 14, "#525252")
    dwg.save()


def pba_watch_party():
    dwg = svgwrite.Drawing(str(OUT / "06-pba-watch-party.svg"), size=(f"{W}px", f"{H}px"), viewBox=f"0 0 {W} {H}")
    rect(dwg, 0, 0, W, H, "#FFFFFF")
    rect(dwg, 0, 0, W, 16, "#0038A8")
    rect(dwg, 0, 16, W, 16, "#CE1126")
    text(dwg, 72, 120, "PBA", 120, "#111827", weight="bold", family="Georgia, serif")
    text(dwg, 72, 210, "WATCH PARTY", 44, "#0038A8", weight="bold", letter_spacing="4")
    text(dwg, 72, 280, "Philippine Basketball Association", 22, "#4B5563")
    rect(dwg, 72, 330, 200, 4, "#CE1126")
    text(dwg, 72, 400, "Community viewing for local fans.", 24, "#374151")
    text(dwg, 72, 460, "Bring your team colors.", 24, "#374151")
    rect(dwg, 72, 540, 936, 360, "#F3F4F6")
    text(dwg, 540, 740, "Insert venue / matchup graphic", 20, "#9CA3AF", anchor="middle")
    footer_block(
        dwg,
        980,
        ["Saturday | 6:30 PM (edit)", "Venue: ____________________", "Free admission / Snacks available"],
        bg="#111827",
    )
    dwg.save()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sk_panique_kk_assembly()
    sk_panique_basketball()
    rsu_it_week()
    ivan_test_beauty()
    nba_game_night()
    pba_watch_party()
    print("Senior pubmats written to", OUT)


if __name__ == "__main__":
    main()
