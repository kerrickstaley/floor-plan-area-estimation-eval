# %%
from pathlib import Path

import polars as pl


# %%
pl.Config.set_tbl_width_chars(220)

RESULTS = [
    {
        "label": "Codex GPT-5.5",
        "harness": "Codex",
        "model": "GPT-5.5",
        "path": Path("results_csvs/codex_gpt_5_5_combined.csv"),
    },
    {
        "label": "Claude Code Opus 4.8",
        "harness": "Claude Code",
        "model": "Opus 4.8",
        "path": Path("results_csvs/claude_code_opus_4_8_combined.csv"),
    },
]


# %%
def load_results(result: dict[str, str | Path]) -> pl.DataFrame:
    return pl.read_csv(result["path"]).with_columns(
        pl.lit(result["label"]).alias("label"),
        pl.lit(result["harness"]).alias("harness"),
        pl.lit(result["model"]).alias("model"),
    )


results = pl.concat(
    [load_results(result) for result in RESULTS],
    how="vertical",
)


# %%
summary = (
    results.group_by("label", "harness", "model", maintain_order=True)
    .agg(
        pl.col("log10_scale_diff").mul(2).abs().mean().alias("scale_mae_log10_2d"),
        pl.col("interior_area_iou").mean().alias("scale_normalized_interior_iou_mean"),
        pl.col("log10_unscaled_area_diff")
        .abs()
        .mean()
        .alias("scale_normalized_interior_area_mae_log10_2d"),
        pl.col("log10_area_diff")
        .abs()
        .mean()
        .alias("final_computed_area_mae_log10_2d"),
    )
    .with_columns(pl.all().exclude("label", "harness", "model").round(4))
)

print(summary)


# %%
def transposed_markdown_table(frame: pl.DataFrame) -> str:
    metric_labels = {
        "scale_mae_log10_2d": "MAE of scale (log10 space, 2D)",
        "scale_normalized_interior_iou_mean": "mean IOU of marked area",
        "scale_normalized_interior_area_mae_log10_2d": "MAE of marked area (log10 space, 2D)",
        "final_computed_area_mae_log10_2d": "MAE of final area (log10 space, 2D)",
    }
    rows = [
        ("harness", *frame["harness"].to_list()),
        ("model", *frame["model"].to_list()),
        ("---", *["---"] * len(frame["label"])),
    ]
    for column in frame.drop("label", "harness", "model").columns:
        rows.append((metric_labels[column], *frame[column].to_list()))
    lines = []
    for row in rows:
        values = [
            f"{value:.4f}" if isinstance(value, float) else str(value) for value in row
        ]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


print(transposed_markdown_table(summary))
