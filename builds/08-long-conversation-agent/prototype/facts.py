"""Golden truth — 15 fabricated NBA facts for context recall testing.

Every fact here is fictional. If the model recalls these correctly, it's
pure context recall. If it "recalls" real NBA facts we never planted,
that's training data leakage.

All facts are set in the 2021-22 NBA season so they fall within the
knowledge window of any model with a pre-2023 cutoff — maximizing the
chance a model *could* leak real data, making our test stricter.

Three categories:
  schema      — Warriors resurgence arc (narrative thread, easier to reconstruct)
  independent — isolated stats with no shared narrative
  cross_topic — league-wide facts that bridge domains
"""

from pydantic import BaseModel


class Fact(BaseModel):
    id: str
    text: str
    category: str  # schema | independent | cross_topic
    key_details: list[str]  # exact details probes should check


GOLDEN_FACTS: dict[str, Fact] = {f.id: f for f in [
    # ── schema: Warriors resurgence arc (2021-22) ──────────────
    Fact(
        id="gsw_trade",
        text=(
            "The Warriors traded Marcus Kemp to the Pelicans on December 3, "
            "2021, receiving two 2022 first-round picks and a pick swap in return."
        ),
        category="schema",
        key_details=["Marcus Kemp", "Pelicans", "December 3, 2021", "two 2022 first-round picks", "pick swap"],
    ),
    Fact(
        id="gsw_offense",
        text=(
            "After the Kemp trade, coach Devin Harlow installed a motion offense "
            "that averaged 312 passes per game — highest in the league."
        ),
        category="schema",
        key_details=["Devin Harlow", "motion offense", "312 passes per game", "highest in the league"],
    ),
    Fact(
        id="gsw_rookie",
        text=(
            "Rookie Terrence Okafor averaged 22.4 PPG in his first 30 games, "
            "the best debut stretch by a Warriors player since the franchise moved to Chase Center."
        ),
        category="schema",
        key_details=["Terrence Okafor", "22.4 PPG", "first 30 games", "best debut stretch", "Chase Center"],
    ),
    Fact(
        id="gsw_record",
        text=(
            "The Warriors went 28-11 after the Kemp trade, "
            "climbing from 11th to 4th in the Western Conference."
        ),
        category="schema",
        key_details=["28-11", "11th to 4th", "Western Conference"],
    ),
    Fact(
        id="gsw_attendance",
        text=(
            "The Warriors' temporary home at Balboa Park Arena drew 14,211 fans "
            "on March 14, 2022, a sellout for the smaller venue during Chase Center renovations."
        ),
        category="schema",
        key_details=["Balboa Park Arena", "14,211 fans", "March 14, 2022", "Chase Center renovations"],
    ),

    # ── independent: isolated stats (2021-22) ──────────────────
    Fact(
        id="okc_age",
        text=(
            "The Thunder's average roster age was 27.6 in the 2021-22 season, "
            "making them the oldest team in the Western Conference."
        ),
        category="independent",
        key_details=["27.6", "2021-22", "oldest", "Western Conference"],
    ),
    Fact(
        id="bos_road",
        text=(
            "The Celtics lost 11 consecutive road games between November 2021 and January 2022, "
            "their worst road skid since 1997."
        ),
        category="independent",
        key_details=["11 consecutive road losses", "November 2021", "January 2022", "worst since 1997"],
    ),
    Fact(
        id="lal_arena",
        text=(
            "The Lakers signed a new arena naming rights deal worth $28M per year "
            "with Hyperion Technologies, effective for the 2022-23 season."
        ),
        category="independent",
        key_details=["$28M per year", "Hyperion Technologies", "2022-23"],
    ),
    Fact(
        id="kemp_streak",
        text=(
            "Before the trade, Kemp had 19 consecutive games scoring 20+ points, "
            "the longest active streak in the league at the time."
        ),
        category="independent",
        key_details=["19 consecutive games", "20+ points", "longest active streak"],
    ),
    Fact(
        id="asg_attendance",
        text=(
            "The 2022 All-Star Game in Mexico City drew 22,314 fans at Arena CDMX, "
            "the first ASG held outside the United States."
        ),
        category="independent",
        key_details=["2022", "Mexico City", "22,314", "Arena CDMX", "first outside the United States"],
    ),

    # ── cross_topic: league-wide bridging facts (2021-22) ──────
    Fact(
        id="cap_number",
        text=(
            "The 2021-22 salary cap was set at $163.5M, a 14% increase "
            "driven by a new media rights deal with Amazon and NBC."
        ),
        category="cross_topic",
        key_details=["$163.5M", "14% increase", "Amazon and NBC"],
    ),
    Fact(
        id="mvp_race",
        text=(
            "Viktor Dragas of the Nuggets led the 2021-22 MVP race after the All-Star break — "
            "the first European player to do so in 15 years."
        ),
        category="cross_topic",
        key_details=["Viktor Dragas", "Nuggets", "2021-22", "first European", "15 years"],
    ),
    Fact(
        id="three_rate",
        text=(
            "The 2021-22 league-wide three-point attempt rate dropped to 31.7% of all field goals, "
            "the first decline in nine seasons, attributed to new freedom-of-movement rules."
        ),
        category="cross_topic",
        key_details=["31.7%", "2021-22", "first decline in nine seasons", "freedom-of-movement rules"],
    ),
    Fact(
        id="gleague_pipeline",
        text=(
            "The G-League call-up pipeline sent 47 players to NBA rosters by February 2022, "
            "up from 31 the previous season."
        ),
        category="cross_topic",
        key_details=["47 players", "February 2022", "up from 31"],
    ),
    Fact(
        id="ref_analytics",
        text=(
            "The league's referee analytics program flagged 2,340 missed calls in Q1 of "
            "the 2021-22 season, a 12% increase year-over-year."
        ),
        category="cross_topic",
        key_details=["2,340 missed calls", "Q1", "2021-22", "12% increase"],
    ),
]}
