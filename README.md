# Rummy Science: Aleks vs. Jim

## Overview

This repository documents the epic clash of two card connoisseurs in the game of Rummy. Having completed 10 games and rigorous statistical analysis and predictive modeling, we seek to answer: Who will be the true Queen of Cards by being the first to reach the pinacle score of 3000?

## Data

_disclaimer: the dates are artificially created to capture the chronological progression of each game_

| date       | jim_scores | aleks_scores | jim_running_sum | aleks_running_sum |
| ---------- | ---------- | ------------ | --------------- | ----------------- |
| 2023-01-01 | -68        | 110          | -68             | 110               |
| 2023-01-02 | 83         | 94           | 15              | 204               |
| 2023-01-03 | -62        | 114          | -47             | 318               |
| 2023-01-04 | 142        | 23           | 95              | 341               |
| 2023-01-05 | 112        | 29           | 207             | 370               |
| 2023-01-06 | -54        | 80           | 153             | 450               |
| 2023-01-07 | 94         | 44           | 247             | 494               |
| 2023-01-08 | 59         | 51           | 306             | 545               |
| 2023-01-09 | 73         | 96           | 379             | 641               |
| 2023-01-10 | 100        | 145          | 479             | 786               |

## Analysis

**Summary Statistics**:

- Jim's mean: 47.9
- Aleks' mean: 78.6
- Jim's variance: 6186.99
- Aleks' variacnce: 1633.38
- Jim's Scores IQR: 124.25
- Aleks's Scores IQR: 60.75
- Jim's Scores Outliers Count: 0
- Aleks's Scores Outliers Count: 0
  - Iterpretation: Jim's scores, having a substantially higher IQR, can imply that his performance is more inconsistent or subject to a wider range of influencing factors. Aleks's more consistent scores on the other hand, seen through a lower IQR, can suggest a narrower influence of external factors or a more stable performance across measurements.

**Positive/Negative Ratio**:

- Jim has gone negative 30.0% of the time
- Aleks has gone negative 0.0% of the time

**Data Visualizations**:

![histogram](https://github.com/aleksgeorgi/CanJimBeatAleksInRummy/blob/main/plots/scores_histogram.png)
![boxplot](https://github.com/aleksgeorgi/CanJimBeatAleksInRummy/blob/main/plots/scores_box_plt.png)

**Time Series Analysis**:

- individual scores over time:

![time series](https://github.com/aleksgeorgi/CanJimBeatAleksInRummy/blob/main/plots/scores_over_time_plt.png)

- running scores over time:

![running scores over time](https://github.com/aleksgeorgi/CanJimBeatAleksInRummy/blob/main/plots/running_scores_over_time.png)

**Linear Regression Prediction**:

- Jim is predicted to reach 3000 points at game number: [53]
- Aleks is predicted to reach 3000 points at game number: [44]

![prediction plot](https://github.com/aleksgeorgi/CanJimBeatAleksInRummy/blob/main/plots/rummy_winner_prediction.png)

## Conclusion

Will Aleks maintain her winning streak, or will Jim stage a comeback? The models have spoken, but fate has the final say. Check back for an update!
