# Compute floor plan area micro-eval
This is an LLM agent micro-eval where I asked the agent to compute the square footage of an apartment given a floor plan of the apartment. This involved two steps: determining the scale of the floor plan by looking at room dimension labels (e.g. 20' x 12'), and marking the parts of the floor plan that count as square footage (interior areas and exterior walls, but not exterior areas like balconies).

I evaluated GPT-5.5 in Codex CLI and Claude Opus 4.8 in Claude Code CLI on a set of 15 floor plans. I did 4 runs with each agent; each run asked the agent to process all 15 input images. I separately hand-measured and hand-marked each floor plan as ground truth.

GPT-5.5 achieved an average error of 23.2% and Claude Opus 4.8 achieved 13.2%. The error was mostly (roughly 80% for both agents) due to mis-estimating the scale and less (roughly 20% for both agents) due to mis-marking the interior area. Overall this accuracy exceeded my expectations, but I would still not trust agents with this work if I needed good accuracy.

## Results

| harness | Codex | Claude Code |
| model | GPT-5.5 | Opus 4.8 |
| --- | --- | --- |
| MAE of scale (log10 space, 2D) | 0.0861 | 0.0511 |
| mean IOU of marked area | 0.9034 | 0.9502 |
| MAE of marked area (log10 space, 2D) | 0.0232 | 0.0139 |
| MAE of final area (log10 space, 2D) | 0.0906 | 0.0539 |
