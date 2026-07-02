# Floor plan area LLM agent micro-eval
This is an LLM agent micro-eval where I asked the agent to compute the square footage of an apartment given a floor plan of the apartment. This involved two steps: determining the scale of the floor plan by looking at room dimension labels (e.g. 20' x 12'), and marking the parts of the floor plan that count as square footage (interior areas and exterior walls, but not exterior areas like balconies).

I evaluated GPT-5.5 in Codex CLI and Claude Opus 4.8 in Claude Code CLI on a set of 15 floor plans. I did 4 runs with each agent; each run asked the agent to process all 15 input images. I separately hand-measured and hand-marked each floor plan as ground truth.

GPT-5.5 achieved an average error of 23.2% and Claude Opus 4.8 achieved 13.2%. The error was mostly (roughly 80% for both agents) due to mis-estimating the scale and less (roughly 20% for both agents) due to mis-marking the interior area. Overall this accuracy exceeded my expectations, but I would still not trust agents with this work if I needed good accuracy.

## Results

| model | GPT-5.5 | Opus 4.8 |
| --- | --- | --- |
| harness | Codex | Claude Code |
| scale MAE (log10 space, 2D) | 0.0861 | 0.0511 |
| marked area mean IOU | 0.9034 | 0.9502 |
| marked area MAE (log10 space) | 0.0232 | 0.0139 |
| final area MAE (log10 space) | 0.0906 | 0.0539 |

For the scale MAE calculation, a 10% linear error in the scale translates to a log10(1.1 ** 2) = 0.0828 error in 2D log10 space.

## Running this eval
I've checked in the ground truth files and the outputs from previous agent runs, so you'll need to expunge these from Git history if you want to re-run this eval. (I hid them in a different folder and asked agents not to look outside the current folder when I did the runs, so the agents were less likely to reward hack).

## Commentary
Each run processed all 15 inputs, and the agents generally used a similar strategy for all 15 inputs within a single run. This means that the errors within a run are correlated with each other; if the agent picked a poor strategy during that run, all estimates would be off. This correlation means the error estimates themselves have higher error bars than we would naively expect given the sample size. Codex was especially affected by this; its per-run final area MAE ranged from 0.0447 (run 1) to 0.1522 (run 2) log10 units, whereas Claude Code was more consistent, ranging from 0.0444 (run 4) to 0.0612 (run 3).

The floor plan with the greatest overall computed area error was this one from Codex. This input has an erroneous dimension: it should say about 10'10" instead of 20'. Other runs from Codex and Claude were not tripped up by this.

<img src="output_images/codex_run_2/23_301_East_22nd_Street_8U.png" width="500px">

The floor plan with the greatest marked area error was this one from Codex. I'm not sure what happened; this is a very easy input where the solution is just a rectangle, but it drew a rectangle that was too large.

<img src="output_images/codex_run_4/39_200_East_23rd_Street_8D.png" width="500px">

A more interesting failure was this floor plan from Codex, where it failed to mark large parts of the floor plan.

<img src="output_images/codex_run_4/09_1_Irving_Place_G9B.png" width="500px">
