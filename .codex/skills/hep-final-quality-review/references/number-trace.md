# Number Trace

Use when checking that final report numbers are fully traceable.

## Required Coverage

Every final-report number that supports a result, comparison, table, plot statement, or conclusion must map to:

- report location;
- displayed value;
- source artifact path;
- source key, JSON path, table row, or plot id;
- claim classification;
- `allowed_in_final_report`;
- note on rounding or formatting when relevant.

## Checks

- Tables are checked cell-by-cell, not just row-by-row.
- Headline numbers and captions are included.
- Blocked or diagnostic numbers are labeled as such in both trace and report.
- Source paths resolve from the repository root.
- Rounded report values agree with source values within the stated precision.

## Veto Conditions

- Any final table cell or headline number lacks a trace entry.
- Trace source path or key does not resolve.
- A trace marks a value blocked while the report presents it as allowed.
- A report number differs materially from its source without a documented transformation.
