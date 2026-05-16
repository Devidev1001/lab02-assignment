# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.20.2",
#     "polars",
#     "altair",
#     "numpy",
# ]
# ///

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import polars as pl
    import altair as alt
    import numpy as np

    return alt, np, pl


@app.cell
def _(mo):
    mo.md("""
    # Lab 02: The Efficiency Gap on Trial -- *Gill v. Whitford*

    **MIT 17.831: Data and Politics**

    ---

    **Learning Objectives:**

    - Compute the efficiency gap from election data using the wasted votes formula
    - Evaluate competing expert arguments about a quantitative measure using real court documents
    - Assess the stability and sensitivity of the efficiency gap across multiple elections
    - Analyze how geographic clustering of voters affects partisan fairness metrics
    - Form and defend an evidence-based judgment about a contested empirical question

    ---

    In this lab, you will step into the role of a neutral data analyst evaluating one of the most important partisan gerrymandering cases in U.S. history. You will read excerpts from actual expert reports filed in court, reproduce key analyses, and ultimately render your own judgment.

    The case is **_Whitford v. Nichol_** (later **_Gill v. Whitford_** at the Supreme Court) -- a challenge to Wisconsin's 2011 state legislative redistricting plan known as **Act 43**.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Part 1: The Case

    ### Background

    In 2011, Wisconsin's Republican-controlled legislature passed **Act 43**, a new set of district maps for the State Assembly. The process was conducted in secret, with the maps drawn by consultants working for Republican legislators. When Democrats and good-government groups challenged the maps, they needed a way to *prove* that the maps constituted an unconstitutional partisan gerrymander.

    The court case centered on the role of the  **efficiency gap** (EG), a metric proposed by Nicholas Stephanopoulos and Eric McGhee in a 2015 law review article. The plaintiffs argued that the EG provided exactly what the Supreme Court had said was missing in prior gerrymandering cases: a **manageable, judicially administrable standard** for identifying unconstitutional partisan gerrymanders.

    The case went to trial before a three-judge federal panel in 2016. Both sides presented expert witnesses who disagreed sharply about whether the efficiency gap was a valid and reliable measure. The district court ruled in favor of the plaintiffs -- the first successful partisan gerrymandering challenge in over 30 years. The case then went to the Supreme Court as *Gill v. Whitford*.

    ### The Efficiency Gap: A Quick Refresher

    Recall from lecture that the efficiency gap measures the difference in "wasted votes" between the two parties across all districts.

    **Wasted Votes Formula:** In each district, wasted votes are:
    - For the **losing** party: *all* votes cast for that party (they contributed nothing to winning)
    - For the **winning** party: votes *in excess* of what was needed to win (i.e., votes above 50% + 1)

    Then: $EG = \frac{\text{Wasted}_{\text{Dem}} - \text{Wasted}_{\text{Rep}}}{\text{Total Votes}}$

    A **negative** EG means Democrats waste more votes (pro-Republican bias). A **positive** EG means Republicans waste more votes (pro-Democratic bias).
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ### The Expert Witnesses

    Three experts submitted reports that form the backbone of this lab:

    | Expert | Side | Role |
    |--------|------|------|
    | **Simon Jackman** | Plaintiffs | Stanford professor of political science. Argued the EG shows Wisconsin's plan is an extreme pro-Republican gerrymander, historically unprecedented among 206 districting plans. |
    | **Nicholas Goedert** | Defendants | Political scientist (Lafayette College). Argued the EG is unstable over time, implies unreasonable "hyper-proportional" representation, and would flag many non-gerrymandered maps. |
    | **Sean Trende** | Defendants | Senior elections analyst (RealClearPolitics). Argued geographic clustering of Democrats naturally produces large EGs even under neutral map-drawing. |

    You will engage with each expert's arguments, test their claims with data, and form your own assessment.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ---

    ## Part 2: The Plaintiff's Case

    ### Jackman's Expert Report

    Simon Jackman was retained by the plaintiffs to determine whether Wisconsin's districting plan constituted a partisan gerrymander. He analyzed 786 state legislative elections across 206 districting plans from 1972 to 2014 -- the most comprehensive study of the efficiency gap ever conducted.

    Here are key excerpts from his report:
    """)
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            """
    **From the Expert Report of Simon Jackman (July 7, 2015):**

    > **Point 8.** The current Wisconsin state legislative districting plan (the "Current Wisconsin Plan"). In Wisconsin in 2012, the average Democratic share of district-level, two-party vote (*V*) is estimated to be 51.4% (the uncertainty stemming from imputations for uncontested seats); recall that Obama won 53.5% of the two-party presidential vote in Wisconsin in 2012. Yet Democrats won only 39 seats in the 99 seat legislature (*S* = 39.4%), making Wisconsin one of 7 states in 2012 where we estimate *V* > 50% but *S* < 50%.

    > **Point 9.** Accordingly, Wisconsin's *EG* measures in 2012 and 2014 are large and negative: -.13 and -.10 (to two digits of precision). The 2012 estimate is the largest *EG* estimate in Wisconsin over the 42 year period spanned by this analysis (1972-2014).

    > **Point 12.** The Current Wisconsin Plan presents overwhelming evidence of being a pro-Republican gerrymander. In the entire set of 786 state legislative elections and their accompanying *EG* measures, there are *no precedents* prior to this cycle in which a districting plan generates an initial two-election sequence of *EG* scores that are each as large as those observed in WI.

    > **Point 15.** My analysis suggests that *EG* greater than .07 in absolute value be used as an actionable threshold. [...] At the 0.07 threshold, 95% of plans would be either (a) undisturbed by the courts, or (b) struck down because we are sufficiently confident that the plan, if left undisturbed, would go on to produce a one-sided sequence of *EG* estimates, consistent with the plan being a partisan gerrymander.
    """
        ),
        kind="info",
    )
    return


@app.cell
def _(mo):
    mo.md("""
    ### Exercise: Load and Explore the Data

    Let's start by loading Wisconsin State Assembly election data and reproducing Jackman's analysis.

    The dataset contains district-level results for all 99 Assembly districts across five elections held under Act 43 (2012-2020). Jackman's report only had access to 2012 and 2014; we have the advantage of hindsight.

    The dataset also includes **presidential vote share** (`pres_dem_voteshare`) for each district -- the Democratic two-party vote share in the closest presidential election (2012, 2016, or 2020). Presidential votes are recorded in *every* district, which will be important later.
    """)
    return


@app.cell
def _(mo, pl):
    _nb_dir = mo.notebook_location()
    _data_dir = _nb_dir / "public" / "data"

    wi = pl.read_csv(str(_data_dir / "wi_assembly_elections.csv"))

    mo.vstack([
        mo.md(f"**Data loaded:** {wi.height} rows covering {wi['year'].n_unique()} elections"),
        mo.ui.table(wi.head(10)),
    ])
    return (wi,)


@app.cell
def _(mo, pl, wi):
    _summary = wi.group_by("year").agg(
        pl.col("district").n_unique().alias("districts"),
        (pl.col("winner") == "D").sum().alias("dem_seats"),
        (pl.col("winner") == "R").sum().alias("rep_seats"),
        pl.col("uncontested").sum().alias("uncontested"),
        (pl.col("dem_votes").sum() / pl.col("total_votes").sum()).round(3).alias("dem_voteshare"),
    ).sort("year")
    mo.vstack([
        mo.md("### Quick Data Summary"),
        mo.ui.table(_summary, selection=None),
        mo.md("Notice the pattern: in every election, Republicans win a large seat majority -- even in years when Democrats win more total votes (2012, 2018). The number of uncontested races varies substantially, which will matter for our EG calculations."),
    ])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Exercise: Compute the Efficiency Gap for 2012

    **Question 1:** *Compute the efficiency gap for the 2012 Wisconsin Assembly election using the wasted votes formula. Use only contested races (exclude districts where `uncontested` is `True`).*

    For each district, calculate:
    - Wasted votes for the **losing** party = all their votes
    - Wasted votes for the **winning** party = their votes minus the votes needed to win (i.e., $\lfloor \text{total\_votes} / 2 \rfloor + 1$)

    Then: $EG = \frac{\text{Total Wasted Dem} - \text{Total Wasted Rep}}{\text{Total Votes}}$

    Steps:
    1. Filter the data to 2012 contested races
    2. For each district, compute wasted votes for Democrats and Republicans
    3. Sum across all districts and apply the formula
    4. Display the result and compare it to Jackman's reported value of $-0.13$
    """)
    return


@app.cell
def _(pl, wi):
    # TODO: Compute the efficiency gap for 2012 using the wasted votes formula
    # 1. Filter to 2012 contested races
    # 2. For each district, compute wasted votes:
    #    - Losing party: all their votes are wasted
    #    - Winning party: votes in excess of floor(total_votes/2) + 1
    # 3. Sum wasted Dem and wasted Rep across all districts
    # 4. EG = (total_wasted_dem - total_wasted_rep) / total_votes



    eg_2012 = (
        wi
        .filter(
            (pl.col("year") == 2012) &
            (~pl.col("uncontested"))
        )
    )

    # 2. Compute total votes and wasted votes for each district
    eg_2012 = (
        eg_2012
        .with_columns([
            (pl.col("dem_votes") + pl.col("rep_votes")).alias("total_votes"),

            # Wasted Democratic votes
            pl.when(pl.col("winner") == "Dem")
            .then(
                # votes beyond the amount needed to win
                pl.col("dem_votes") - (
                    (pl.col("dem_votes") + pl.col("rep_votes")) // 2 + 1
                )
            )
            .otherwise(
                # all losing votes are wasted
                pl.col("dem_votes")
            )
            .alias("wasted_dem"),

            # Wasted Republican votes
            pl.when(pl.col("winner") == "Rep")
            .then(
                pl.col("rep_votes") - (
                    (pl.col("dem_votes") + pl.col("rep_votes")) // 2 + 1
                )
            )
            .otherwise(
                pl.col("rep_votes")
            )
            .alias("wasted_rep")
        ])
    )

    # 3. Sum wasted votes across districts
    summary = eg_2012.select([
        pl.sum("wasted_dem").alias("total_wasted_dem"),
        pl.sum("wasted_rep").alias("total_wasted_rep"),
        pl.sum("total_votes").alias("total_votes")
    ])

    # 4. Compute efficiency gap
    summary = summary.with_columns([
        (
            (pl.col("total_wasted_dem") - pl.col("total_wasted_rep"))
            / pl.col("total_votes")
        ).alias("efficiency_gap")
    ])

    print(summary)
    return


@app.cell
def _(mo):
    mo.md("""
    ### Exercise: Visualize the Vote Share Distribution

    **Question 2:** *Create a histogram of Democratic vote shares across all contested districts in 2012. Color districts where Democrats won (vote share > 0.5) blue, and districts where Republicans won red. Add a vertical dashed line at 0.5.*

    This visualization reveals the *mechanism* behind the efficiency gap -- how voters are distributed across districts. Look for the signature of a gerrymander: **pack** the opposing party's voters into a few districts they win overwhelmingly, and **crack** the rest across many districts they lose narrowly.
    """)
    return


@app.cell
def _(alt, pl, wi):
    # TODO: Create a histogram of Democratic vote share for 2012 contested races
    # Use alt.Chart with mark_bar, color by whether dem_voteshare > 0.5
    # Add a vertical dashed line at 0.5

    df = (
        wi
        .filter(
            (pl.col("year") == 2012) &
            (~pl.col("uncontested"))
        )
        .with_columns(
            (pl.col("dem_voteshare") > 0.5).alias("dem_majority")
        )
    )

    # 2. Convert to Altair-friendly format (no pandas)
    data = df.to_dicts()

    # 3. Histogram
    hist = (
        alt.Chart(alt.Data(values=data))
        .mark_bar()
        .encode(
            x=alt.X("dem_voteshare:Q", bin=alt.Bin(maxbins=30), title="Democratic vote share"),
            y=alt.Y("count():Q", title="Number of districts"),
            color=alt.Color("dem_majority:N", title="Dem > 0.5")
        )
    )

    # 4. Vertical dashed line at 0.5
    rule = alt.Chart(alt.Data(values=[{}])).mark_rule(
        strokeDash=[6, 4],
        color="black"
    ).encode(
        x=alt.datum(0.5)
    )

    hist + rule
    return (data,)


@app.cell
def _(mo):
    mo.md(r"""
    ### Exercise: The Seats-Votes Curve

    **Question 3:** *Construct a seats-votes curve for the 2012 Wisconsin Assembly map using uniform swing.*

    The seats-votes curve shows how seat share would change across a range of hypothetical vote shares. Under **uniform swing**, you shift every district's vote share by the same amount and count how many seats each party would win.

    Steps:
    1. Get the array of Democratic vote shares from 2012 contested races
    2. For each swing value $\delta$ from $-0.20$ to $+0.20$ (in steps of ~0.005):
       - Add $\delta$ to every district's vote share
       - Compute the resulting Democratic seat share (fraction of districts where shifted vote share > 0.5)
       - Compute the resulting statewide Democratic vote share (mean of shifted values)
    3. Plot the resulting curve (vote share on x-axis, seat share on y-axis)
    4. Add a proportional representation line (45-degree dashed line)
    5. Mark the actual 2012 result as a point

    What does the position of the seats-votes curve relative to the proportional line tell you? At what uniform swing does the EG cross Jackman's $\pm 0.07$ threshold?
    """)
    return


@app.cell
def _(alt, np, pl, wi):
    # TODO: Construct a seats-votes curve using uniform swing on 2012 contested races
    # Plot it with a proportional representation reference line and the actual 2012 result point

    df1 = (
        wi
        .filter(
            (pl.col("year") == 2012) &
            (~pl.col("uncontested"))
        )
        .select("dem_voteshare")
    )

    shares = df1["dem_voteshare"].to_numpy()

    # 2. Swing values
    deltas = np.arange(-0.20, 0.205, 0.005)

    results = []

    for d in deltas:
        shifted = shares + d

        seat_share = (shifted > 0.5).mean()
        vote_share = shifted.mean()

        results.append({
            "delta": d,
            "vote_share": vote_share,
            "seat_share": seat_share
        })

    curve_df = pl.DataFrame(results).to_dicts()

    # 3. Build main curve
    base = alt.Chart(alt.Data(values=curve_df)).mark_line().encode(
        x=alt.X("vote_share:Q", title="Democratic Vote Share"),
        y=alt.Y("seat_share:Q", title="Democratic Seat Share")
    )

    # 4. Proportional representation line (y = x)
    pr_line = alt.Chart(alt.Data(values=[
        {"x": 0, "y": 0},
        {"x": 1, "y": 1}
    ])).mark_line(
        strokeDash=[6, 4],
        color="black"
    ).encode(
        x="x:Q",
        y="y:Q"
    )

    # 5. Actual 2012 result
    actual_vote = shares.mean()
    actual_seat = (shares > 0.5).mean()

    actual_point = alt.Chart(alt.Data(values=[{
        "vote_share": actual_vote,
        "seat_share": actual_seat
    }])).mark_point(size=100, color="red").encode(
        x="vote_share:Q",
        y="seat_share:Q"
    )

    # 6. Combine
    (pr_line + base + actual_point)

    return (base,)


@app.cell
def _(mo):
    mo.md("""
    ---

    **Question 4:**

    *Based on your calculations and visualizations, does Wisconsin's 2012 efficiency gap seem unusually large? What does the distribution of vote shares across districts tell you about how the map translates votes into seats?*

    **Your answer:** Yes, it seems like the map was drawn in order to maximize the wasted democratic votes. There are many narro democratic losses and very few demoratic wins, and the low proportion of democratic seats relative to their vote share reflects this.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ---

    ## Part 3: The Defense Responds

    The defendants retained two experts who challenged the efficiency gap from different angles. Let's examine their arguments.

    ### Goedert: The EG is Unstable and Implies Hyper-Proportional Representation
    """)
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            """
    **From the Expert Report of Nicholas Goedert (December 2, 2015):**

    > **Point 1.** Despite claims in the plaintiffs' complaint, a large efficiency gap does not necessarily imply an unbalanced map. Instead, a large efficiency gap implies deviation from a predetermined seats/votes curve representing "hyper-proportionate" or "hyper-responsive" representation. Thus, using an efficiency gap standard creates the same constitutional issues as the proportional representation standard the Court has previously rejected.

    > **Point 2.** The plaintiffs' complaint alleges that an efficiency gap of 7% in a single election is sufficient for presumptive unconstitutionality. But evidence in both the academic literature and the plaintiffs' expert report show that efficiency gaps of the size proposed in the complaint are highly unstable and not particularly informative of future or durable gaps. In fact, **as many as half of all maps that exceed this threshold in one election during a decade will be biased in favor of the opposite party in another election** during the same decade.

    > **Point 5.** Any judgment about the partisan motivation behind pro-Republican bias in a map should be made in the context of bias due to the asymmetric geographic dispersion of partisans. This dispersion has generated Republican bias in many states' maps across the nation over the last few decades [...] It has also generated Republican bias in two different non-partisan maps drawn in Wisconsin.
    """
        ),
        kind="warn",
    )
    return


@app.cell
def _(mo):
    mo.md("""
    ### Trende: Geographic Clustering Creates "Natural" Packing
    """)
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            """
    **From the Declaration of Sean P. Trende (January 5, 2016):**

    > **Para. 8.** Second, the metric fails to account for the "natural" packing that can occur if party members are disproportionately clustered in certain types of areas [...] This is important because if efficiency gaps are not accounting for "natural" clustering, then at least some of the asymmetry they are remedying is not a result of state action.

    > **Para. 22.** Under this [heavy clustering] scenario, utilizing our original "neutral" map drawing techniques actually results in three reliably Republican districts. [...] Under this scenario, the efficiency gap is -.25. Court scrutiny is invited as a result of applying neutral principles.

    > **Para. 24.** In short, under a scenario where significant clustering occurs, you actually have to engage in what would traditionally be called gerrymandering in order to draw a neutral map.

    > **Para. 29.** For example, the EG metric finds that New York and Wisconsin in the 2000s would qualify as partisan Republican gerrymanders. But Democrats drew Assembly districts in New York, while Wisconsin's map in the 2000s was drawn by a Court. Both are examples of states where there is a high degree of partisan clustering: in New York City and in Dane/Milwaukee/Rock counties respectively.
    """
        ),
        kind="warn",
    )
    return


@app.cell
def _(mo):
    mo.md("""
    ---

    ### Exercise: Test Goedert's Instability Claim

    Goedert argued that a large EG in one election doesn't tell you much because it's "highly unstable." Let's test this by computing the EG for every Wisconsin Assembly election under Act 43.

    **Question 5:** *Use the `compute_eg` helper function below to compute the efficiency gap for each election year from 2012 to 2020. Store the results in a DataFrame called `eg_by_year`.*

    The helper function takes a DataFrame of district-level results and returns the EG using the wasted votes formula. Your job: loop over each year, filter to contested races, call the function, and collect the results.
    """)
    return


@app.cell
def _(np, pl, wi):
    def compute_eg(df):
        """Compute the efficiency gap using the wasted votes formula.

        Parameters
        ----------
        df : pl.DataFrame
            District-level results with columns: dem_votes, rep_votes,
            total_votes, winner.

        Returns
        -------
        float
            The efficiency gap. Negative = pro-Republican bias.
        """
        _dem_v = df["dem_votes"].to_numpy()
        _rep_v = df["rep_votes"].to_numpy()
        _tot_v = df["total_votes"].to_numpy()
        _votes_to_win = np.floor(_tot_v / 2).astype(int) + 1

        _w_dem = np.where(_dem_v > _rep_v, _dem_v - _votes_to_win, _dem_v)
        _w_rep = np.where(_rep_v > _dem_v, _rep_v - _votes_to_win, _rep_v)

        return float((_w_dem.sum() - _w_rep.sum()) / _tot_v.sum())

    # TODO: Loop over each year, filter to contested races, call compute_eg,
    # and collect results into a list of dicts. Then create eg_by_year DataFrame.
    _rows = []
    for _year in sorted(wi["year"].unique().to_list()):
       df_year = (
            wi
            .filter(
                (pl.col("year") == _year) &
                (~pl.col("uncontested"))
            )
            .with_columns(
                (pl.col("dem_votes") + pl.col("rep_votes")).alias("total_votes")
            )
        )

        # skip empty years just in case

    eg = compute_eg(df_year)

    _rows.append({
            "year": _year,
            "efficiency_gap": eg
        })

    eg_by_year = pl.DataFrame(_rows)
    return (eg_by_year,)


@app.cell
def _(mo):
    mo.md(r"""
    **Question 6:** *Plot the efficiency gap over time as a line chart with points. Add horizontal dashed lines at $\pm 0.07$ (Jackman's proposed threshold) and a line at zero. Label the threshold.*

    Is the EG "highly unstable" as Goedert claims, or does it show a consistent pattern?
    """)
    return


@app.cell
def _(alt, base, data, eg_by_year):
    # TODO: Plot EG over time with Jackman's .07 threshold lines
    # Convert only final summary
    _data = eg_by_year.to_dicts()

    _base = alt.Chart(alt.Data(values=data)).encode(
        x=alt.X("year:O", title="Year"),
        y=alt.Y("efficiency_gap:Q", title="Efficiency Gap")
    )

    line = _base.mark_line()

    points = base.mark_point(size=80)

    zero_line = alt.Chart(alt.Data(values=[{"y": 0}])).mark_rule(
        color="black"
    ).encode(
        y="y:Q"
    )

    threshold_pos = alt.Chart(alt.Data(values=[{"y": 0.07, "label": "+0.07 threshold"}])).mark_rule(
        strokeDash=[6, 4],
        color="red"
    ).encode(
        y="y:Q"
    )

    threshold_neg = alt.Chart(alt.Data(values=[{"y": -0.07, "label": "-0.07 threshold"}])).mark_rule(
        strokeDash=[6, 4],
        color="red"
    ).encode(
        y="y:Q"
    )

    threshold_labels = alt.Chart(alt.Data(values=[
        {"year": eg_by_year["year"].min(), "efficiency_gap": 0.07, "text": "+0.07 threshold"},
        {"year": eg_by_year["year"].min(), "efficiency_gap": -0.07, "text": "−0.07 threshold"},
    ])).mark_text(
        align="left",
        dx=5,
        color="red"
    ).encode(
        x="year:O",
        y="efficiency_gap:Q",
        text="text:N"
    )

    (line + points + zero_line + threshold_pos + threshold_neg + threshold_labels)
    return


@app.cell
def _(mo):
    mo.md("""
    ---

    **Question 7:**

    *Goedert argues that a large EG in one election doesn't tell you much because it's unstable over time. Based on your analysis of multiple Wisconsin elections, is the efficiency gap under Act 43 stable or unstable? Does this support or undermine Goedert's general critique?*

    **Your answer:** The efficiency gap is stable, which undermine's Goedert's critique.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ---

    ## Part 4: Testing the Geographic Clustering Argument

    Trende's strongest argument is that the geographic clustering of Democrats in cities (Milwaukee, Madison) naturally creates "packed" Democratic districts, generating a pro-Republican EG even under neutral map-drawing. Let's test this empirically.

    ### Analyzing Packing Asymmetry with Presidential Vote Data

    If Trende is right about geographic clustering, we should see the pattern in *presidential* voting too -- presidential votes are cast in *every* district (no uncontested races), so they give us a cleaner picture of the underlying partisan geography.

    **Question 8:** *Create overlaid histograms of `pres_dem_voteshare` for 2012, separating districts won by Democrats (assembly winner == "D") and districts won by Republicans (assembly winner == "R"). Use different colors and set opacity so both distributions are visible.*

    *What do the distributions tell you about how Democratic and Republican voters are geographically distributed? Do you see evidence of Democratic "packing" in the presidential vote data?*
    """)
    return


@app.cell
def _(alt, data, pl, wi):
    # TODO: Create overlaid histograms of presidential Dem vote share for 2012
    # Separate by assembly winner (D vs R)
    # This shows geographic clustering independent of uncontested race issues

    # 1. Filter to 2012 only (you can keep uncontested if desired;
    # here we keep all since you're explicitly studying geography)
    df_ = wi.filter(pl.col("year") == 2012)

    # 2. Ensure winner is clean categorical
    df_ = df_.with_columns(
        pl.col("winner").cast(pl.Utf8)
    )

    data_ = df_.to_dicts()

    # 3. Base chart
    base_ = alt.Chart(alt.Data(values=data))

    # 4. Overlaid histograms
    hist_ = base_.mark_bar(opacity=0.5).encode(
        x=alt.X(
            "pres_dem_voteshare:Q",
            bin=alt.Bin(maxbins=30),
            title="Presidential Democratic Vote Share"
        ),
        y=alt.Y("count():Q", title="Count of districts"),
        color=alt.Color("winner:N", title="Assembly Winner")
    )

    hist_
    return


@app.cell
def _(mo):
    mo.md("""
    ---

    **Question 9:**

    *Trende argues that the geographic clustering of Democratic voters in cities naturally creates a pro-Republican efficiency gap, even under neutral map-drawing. Based on your analysis of the presidential vote share distributions, how much of the efficiency gap could be attributed to geography vs. intentional map manipulation? What evidence would help you distinguish between the two?*

    **Your answer:** The evidence suggests that geography does play a role, but it doesn't seem to fully account for the efficiency gap.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ---

    ## Part 5: Handling Uncontested Races

    ### The Problem with Uncontested Races

    We've been excluding uncontested races from our EG calculations. But this is a significant methodological issue:

    - In 2014, **50 out of 99** districts were uncontested -- more than half!
    - Excluding them means our wasted votes calculation ignores a large fraction of districts
    - Different treatments of uncontested races was a point of contention between the experts

    The fundamental problem: in an uncontested race, we observe the winner but not the *vote share* -- we don't know if the district would have been 55-45 or 80-20 in a contested election.

    ### Imputation Using Presidential Vote Share

    One common approach is to **impute** (fill in) the missing vote shares using presidential results. The logic:

    - Presidential vote share is observed in **every** district (no uncontested presidential races)
    - Presidential and legislative vote shares are correlated -- a district that votes heavily Democratic for president will tend to vote Democratic for the state assembly too
    - We can use the presidential vote share as a proxy for what the legislative vote share *would have been*

    Jackman used a more sophisticated statistical model in his report, but simple imputation strategies can still be informative.

    **Question 10:** *Impute vote shares for uncontested races using the `pres_dem_voteshare` column. For uncontested Democratic wins, set `dem_voteshare` to `pres_dem_voteshare`. For uncontested Republican wins, do the same. Then compute the EG for each year using all 99 districts with the imputed values.*

    *Compare your results to the EG computed on contested races only. How much does imputation change the results?*
    """)
    return


@app.cell
def _(np, pl, wi):
    # TODO: Impute uncontested race vote shares using presidential vote share
    # For uncontested races, replace dem_voteshare with pres_dem_voteshare
    # Recompute dem_votes and rep_votes from imputed voteshare * total_votes
    # Compute EG (wasted votes formula) for each year using all 99 districts
    # Compare with contested-only results

    def compute_eg_full(df):
        _dem_v = df["dem_votes"].to_numpy()
        _rep_v = df["rep_votes"].to_numpy()
        _tot_v = df["total_votes"].to_numpy()

        _votes_to_win = np.floor(_tot_v / 2).astype(int) + 1

        _w_dem = np.where(_dem_v > _rep_v, _dem_v - _votes_to_win, _dem_v)
        _w_rep = np.where(_rep_v > _dem_v, _rep_v - _votes_to_win, _rep_v)

        return float((_w_dem.sum() - _w_rep.sum()) / _tot_v.sum())


    rows = []

    for year in sorted(wi["year"].unique().to_list()):

        df_years = wi.filter(pl.col("year") == year)

        # 1. Impute dem voteshare for uncontested races
        df_years = df_years.with_columns(
            pl.when(pl.col("uncontested"))
            .then(pl.col("pres_dem_voteshare"))
            .otherwise(pl.col("dem_voteshare"))
            .alias("dem_voteshare_imputed")
        )

        # 2. Recompute votes from imputed share
        df_years = df_years.with_columns([
            (pl.col("dem_voteshare_imputed")).alias("d_share"),
            (1 - pl.col("dem_voteshare_imputed")).alias("r_share"),
        ]).with_columns([
            (pl.col("d_share") * (pl.col("dem_votes") + pl.col("rep_votes"))).round(0).cast(pl.Int64).alias("dem_votes_new"),
            (pl.col("r_share") * (pl.col("dem_votes") + pl.col("rep_votes"))).round(0).cast(pl.Int64).alias("rep_votes_new"),
        ]).with_columns(
            (pl.col("dem_votes_new") + pl.col("rep_votes_new")).alias("total_votes")
        ).rename({
            "dem_votes_new": "dem_votes_new",
            "rep_votes_new": "rep_votes_new"
        })

        eg_null = compute_eg_full(df_years)

        rows.append({
            "year": year,
            "eg_imputed": eg_null
        })

    eg_imputed_by_year = pl.DataFrame(rows)

    eg_imputed_by_year
    return


@app.cell
def _(mo):
    mo.md("""
    ---

    ## Part 6: Your Ruling

    ### Summary of Evidence

    Before rendering your judgment, review what you've found:

    - The 2012 efficiency gap and how it compares to Jackman's .07 threshold
    - The distribution of vote shares (evidence of packing and cracking)
    - The seats-votes curve and what it reveals about the map's structural bias
    - Whether the EG is stable or unstable across elections (Goedert's critique)
    - Whether geographic clustering explains the EG (Trende's critique)
    - How sensitive the results are to the treatment of uncontested races
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    **Question 11: Your Ruling**

    *Imagine you are an analyst advising the court. Based on your data analysis:*

    1. *Is the efficiency gap a reliable measure of partisan gerrymandering? Why or why not?*
    2. *Does the evidence suggest Wisconsin's Act 43 map was an intentional partisan gerrymander, or could the observed bias be explained by geographic sorting?*
    3. *Should courts use quantitative metrics like the EG to adjudicate gerrymandering claims? What are the risks?*

    *Write a 2-3 paragraph synthesis memo with your ruling and reasoning.*

    **Your answer:** Wisconsin's map was an intentional partisan gerrymander. The large efficiency gas shows that the map is biased towards republicans, and the evidence doesn't support the idea that this is due merely to the geography of the state. Additionally, the efficiency gap is stable and consistent, dispelling Goedert's notion that efficiency gap is "\"Highly unstable."

    Courts should use quantitative metrics as part of their adjudication of gerrymandering claims, but it shouldn't be the entire basis for a ruling. EG is an eeffective measurement, but it's always possible that there will be factors that EG doesn't identify. Geographic bias is one, but there could also be other contributors such as compliance with the voting rights act or other legislation. EG is reliable, but it shouldn't be the sole determiner of rulings
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ---

    ## Epilogue: What Actually Happened

    In November 2016, the three-judge district court **struck down** Wisconsin's Act 43 as an unconstitutional partisan gerrymander -- the first such ruling in over 30 years. The court explicitly endorsed the efficiency gap as part of its analysis.

    The case was appealed to the U.S. Supreme Court as **_Gill v. Whitford_** (2018). The Court **reversed** the lower court's ruling -- but *not* on the merits of the efficiency gap. Instead, the Court held that the plaintiffs lacked **standing** because they had not demonstrated individual harm in their own districts (as opposed to statewide harm).

    The Court sent the case back to the lower court, and the plaintiffs were unable to satisfy the standing requirements before Wisconsin's maps were used through the 2020 election cycle. The Act 43 maps remained in effect for the entire decade.

    In 2023, a newly-elected liberal majority on the Wisconsin Supreme Court ruled the existing maps violated the state constitution, and Wisconsin adopted new maps for the 2024 elections drawn by the governor.

    The efficiency gap remains widely used in academic research and redistricting litigation, though no court has adopted it as a definitive legal standard. The debate between Jackman, Goedert, and Trende continues to echo in every new gerrymandering case.

    ---

    *This lab used data from the Wisconsin Elections Commission, the OpenElections Project, and ward-level presidential vote data aggregated to assembly districts. Expert report excerpts are from court filings in* Whitford v. Nichol, *Case No. 3:15-cv-00421-bbc (W.D. Wis.).*
    """)
    return


if __name__ == "__main__":
    app.run()
