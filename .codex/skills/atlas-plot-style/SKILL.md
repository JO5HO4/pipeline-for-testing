---
name: atlas-plot-style
description: Apply ATLAS publication committee plot styling while creating, modifying, or reviewing plotting code in high-energy-physics repositories. Use for ROOT/C++ macros, PyROOT, Python matplotlib, mplhep, notebooks, histogram scripts, plotting utilities, figure export pipelines, and code-review requests that mention ATLAS style, PubCom plot style, ATLAS labels, ATLAS Internal/Preliminary/Simulation, color-vision-safe palettes, data-vs-simulation histograms, or publication-ready HEP plots.
---

# ATLAS Plot Style

## Goal

Make plotting code produce clear ATLAS-style high-energy-physics figures while preserving the analysis logic. Treat this skill as a code-editing and code-review standard for ROOT, PyROOT, matplotlib, mplhep, and notebook plotting workflows.

## Codex Workflow

1. Inspect the repository before editing. Identify the plotting backend, existing style helpers, output directories, and any tests or plot-generation commands.
2. Prefer existing project utilities over duplicating style code. Use local `AtlasStyle.C`, `AtlasUtils.C`, `AtlasLabels.C`, `atlasrootstyle`, `mplhep`, or project plotting helpers when present.
3. Make the smallest reliable change that applies the ATLAS conventions below. Do not change physics selections, histogram definitions, binning, weights, uncertainties, or data inputs unless the user explicitly asks.
4. If a requested change affects approval status, luminosity, center-of-mass energy, units, bin width, or whether data are real ATLAS data or simulation, use the information already in the repo or prompt. If it is not available, leave a clear TODO or ask instead of guessing.
5. Export publication-like figures as true PDF whenever possible. PNG is acceptable only for event displays, special graphics, quick diagnostics, or when the user asks for raster output.
6. Run the narrowest available smoke test or plot-generation command. If execution is not possible, state the command that should be run and why it was not run.
7. In the final response, summarize changed files, style decisions applied, and the command used to regenerate plots.

## Core ATLAS Plot Defaults

### Canvas, axes, and typography

- Use a white canvas and white legend background.
- Remove standard ROOT or matplotlib decorations that are not part of the figure: no plot title, stats box, fit-result box, or drop shadow.
- Use Helvetica or the closest available sans-serif font.
- Put tick marks on the top and right sides as well as the bottom and left.
- Use standard single-plot sizes unless the figure content requires otherwise: rectangular `800 x 600 px`, square `600 x 600 px`.
- Label both axes.
- Include units in square brackets unless the quantity is dimensionless.
- Prefer italic variable names and roman subscripts when practical in the plotting backend.
- For bin-count histograms, label the y axis with the object and bin width, for example `Events / 0.2 GeV`, `Tracks / bin`, or `Entries / 5 GeV`.
- Do not divide fixed-width histogram bin contents by the bin size merely because the y-axis label contains `/ bin width`. Correct variable-width bins only when needed for the intended quantity.
- Right-justify the x-axis title and place the y-axis title toward the top where the backend allows this cleanly.
- For integer x-axis quantities, use bin centers at integer labels by choosing half-integer bin edges.

### Data, simulation, histograms, and functions

- Reserve marker series primarily for data.
- Draw data in black, with black error bars.
- Use the default data marker as a full black circle. For a second data marker series, prefer an open circle before using colored data markers.
- Increase marker size when needed for readability, but reduce it if otherwise visible error bars would be hidden.
- Suppress horizontal error bars unless variable bin widths or missing references make them necessary.
- Do not draw caps or ticks at the ends of error bars.
- Reserve filled histograms primarily for simulation.
- Do not draw error bars on full simulation histograms. Use a shaded uncertainty band when simulation uncertainties must be shown.
- Use function lines for fits and parameterizations.
- Do not use black for function lines; black is reserved for data and common histogram boundaries.
- For one function line, prefer a high-contrast dark red or dark blue. For multiple function lines, prefer different line patterns in the same color over multiple colors with the same line pattern.

### Colors

Use black for data markers. For filled backgrounds or categorical simulation components, prefer the ATLAS color-vision-deficiency-friendly palette:

```python
ATLAS_CVD_7 = [
    "#D55E00",  # orange-red
    "#56B4E9",  # sky blue
    "#E69F00",  # orange
    "#F0E442",  # yellow
    "#009E73",  # bluish green
    "#CC79A7",  # reddish purple
    "#0072B2",  # blue
]
```

If more colors are needed, use this extended palette before inventing new colors:

```python
ATLAS_EXTENDED = [
    "#3F90DA", "#FFA90E", "#BD1F01", "#94A4A2", "#832DB6",
    "#A96B59", "#E76300", "#B9AC70", "#717581", "#92DADD",
]
```

Additional color rules:

- Prefer full fill colors over hatching for normal stacked histograms.
- Keep background colors consistent across all plots in the same note, paper, or presentation.
- In stack plots, place darker colors lower in the stack and lighter colors higher in the stack when practical.
- Avoid dark colors at the top of stacks because they can obscure black data points.
- Avoid adjacent red and green shades in stacked plots unless using the recommended color-vision-safe palette.
- Ensure the plot remains legible in grayscale or black-and-white print.

### Legends and text blocks

- Add a legend whenever more than one plotted object appears.
- Match legend entry types to objects:
  - data markers: point only, no horizontal error bar (`P` in ROOT)
  - filled histograms: filled area (`F` in ROOT)
  - function lines: line (`L` in ROOT)
- Use no legend border unless a border is genuinely needed.
- If a border is needed, remove drop shadows.
- Use a white legend background.
- Set legend text large enough to match or be comparable to axis-label readability.
- Order legend entries to match the visual stacking order of histograms.
- Keep decorations inside the plot pad when possible.
- Make room for labels and legends by increasing axis extrema or plot ranges rather than shrinking text to unreadable size or overlapping content.
- Put key numerical results in captions when possible; do not clutter the plot with too many numbers.

### ATLAS labels and approval-sensitive text

Never invent an approval state. Use ATLAS labels only when the context supports them.

- `ATLAS`: use only for plots submitted for publication or approved auxiliary material of an ATLAS paper.
- `ATLAS Preliminary`: use only for plots approved by ATLAS but not yet in a refereed publication, such as approved CONF or PUB material.
- `ATLAS Internal`: use for internal ATLAS talks, approval talks, drafts, and work not yet at final approval.
- `ATLAS Work In Progress`: use only in the limited student-talk context where that label is appropriate.
- Omit an ATLAS label for pure standalone generator-level plots where no ATLAS software or ATLAS result is involved.
- If everything shown is simulated data, use `ATLAS Simulation` or `ATLAS Simulation Preliminary` as appropriate.
- When ATLAS data are shown, the legend should call the data entry `Data` and the plot should include center-of-mass energy and integrated luminosity, for example `sqrt(s) = 13 TeV, 140 fb^{-1}`.
- Put additional text after `ATLAS` in normal Helvetica, not bold or slanted. The `ATLAS` word itself should be bold, slanted, all caps, and Helvetica when the backend supports it.

### Time-axis public plots

For public plots that show quantities as a function of time:

- Label time axes and time labels as UTC.
- Prefer LHC fill number and date for public plots.
- Do not quote ATLAS run numbers on public time-sensitive plots unless explicitly required by the analysis guidance.

## ROOT and PyROOT Implementation

Use the official ATLAS ROOT style when available.

### C++ ROOT macro pattern

```cpp
#include "AtlasStyle.C"
#include "AtlasUtils.C"
#include "AtlasLabels.C"

void make_plot() {
  SetAtlasStyle();

  TCanvas* c = new TCanvas("c", "", 0, 0, 800, 600);
  // For square figures: new TCanvas("c", "", 0, 0, 600, 600);

  // Draw histograms, graphs, or stacks here.
  // h->SetTitle("");
  // h->GetXaxis()->SetTitle("#font[52]{p}_{T} [GeV]");
  // h->GetYaxis()->SetTitle("Events / 5 GeV");

  TLegend* legend = new TLegend(0.62, 0.68, 0.88, 0.88);
  legend->SetBorderSize(0);
  legend->SetFillColor(0);
  legend->SetTextSize(0.04);
  // legend->AddEntry(h_data, "Data", "P");
  // legend->AddEntry(h_mc, "Simulation", "F");
  // legend->Draw();

  // Example only: choose the correct label for the approval state.
  // ATLASLabel(0.20, 0.86, "Internal");

  c->SaveAs("plot.pdf");
}
```

### ROOT style adjustments to prefer

- Call `SetAtlasStyle()` before creating canvases and drawing objects.
- Use `AtlasLabels.C`/`AtlasUtils.C` for ATLAS labels and palette helpers if the repository includes them.
- Use `Draw("eX0")` or equivalent when suppressing horizontal data error bars.
- For legends, use `SetBorderSize(0)`, `SetFillColor(0)`, and a readable `SetTextSize`, commonly around `0.04`.
- For histogram stacks, align legend order with stack order and keep data drawn on top.
- For uncertainty bands, use filled or shaded bands rather than full histogram error bars.
- Save final plots as `pdf` from ROOT, not as PNG converted to PDF.

## Matplotlib and mplhep Implementation

Use `mplhep` whenever it is available or can reasonably be added to the plotting environment. Avoid applying another global style after `hep.style.use(hep.style.ATLAS)`.

```python
import matplotlib.pyplot as plt
import mplhep as hep

hep.style.use(hep.style.ATLAS)

ATLAS_CVD_7 = ["#D55E00", "#56B4E9", "#E69F00", "#F0E442", "#009E73", "#CC79A7", "#0072B2"]

fig, ax = plt.subplots(figsize=(8, 6))

# Preserve the repository's actual data, binning, and weights.
# hep.histplot(values, bins=bins, ax=ax, histtype="fill", color=ATLAS_CVD_7[0], label="Background")
# ax.errorbar(bin_centers, data, yerr=data_err, fmt="o", color="black", ecolor="black", capsize=0, label="Data")

ax.set_xlabel(r"$p_T$ [GeV]")
ax.set_ylabel("Events / 5 GeV")
ax.tick_params(top=True, right=True, direction="in")
ax.legend(frameon=False)

# Choose the correct label for the approval state. Do not guess.
# hep.atlas.label("Internal", data=True, lumi=140, com=13, ax=ax)

fig.savefig("plot.pdf", bbox_inches="tight")
```

Implementation notes:

- Use `hep.histplot` for histograms when practical.
- Draw data with black markers and black error bars. Use `capsize=0` for matplotlib error bars.
- Suppress x error bars unless required.
- Use `frameon=False` for legends and keep the legend background visually white.
- Use `hep.atlas.label(...)` for labels, matching the installed `mplhep` API. Inspect local examples or docs if the function signature differs.
- Use `fig.savefig("name.pdf", bbox_inches="tight")` for final figures.
- Do not use seaborn styles or plotting defaults that override ATLAS style unless the user explicitly asks.

## Review Checklist

Before finishing a task, check the plot or plotting code for:

- both axes labeled, with units where needed;
- y-axis label includes the bin width for bin-count histograms;
- white background, no title/stats box/drop shadow;
- top and right ticks enabled;
- black data markers and error bars;
- no unnecessary horizontal error bars or error-bar caps;
- simulation shown as filled histograms or stacks, not data-style markers;
- uncertainty shown as a shaded band when needed;
- color-vision-safe palette for categorical fills;
- stack order, colors, and legend order consistent;
- legend present when multiple objects are shown, borderless unless necessary;
- ATLAS label status correct and not guessed;
- luminosity and center-of-mass energy shown when real ATLAS data are shown;
- public time axes labeled UTC;
- final output saved as true PDF where appropriate.
