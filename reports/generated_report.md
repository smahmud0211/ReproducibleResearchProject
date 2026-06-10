# CO2 Global Emissions Analysis Report

## Project Goal

This project reproduces an R-based CO2 emissions analysis in Python.
It uses the Our World in Data CO2 dataset and generates visualizations and a regression analysis.

## Dataset

The project uses the Our World in Data CO2 dataset, which includes CO2 emissions, GDP, population, and country-level indicators.

## Generated Figures

![01_global_average_co2_per_capita](../outputs/figures/01_global_average_co2_per_capita.png)

![02_gdp_vs_co2_per_capita_latest](../outputs/figures/02_gdp_vs_co2_per_capita_latest.png)

![03_linear_regression_co2_pc_gdp_pc](../outputs/figures/03_linear_regression_co2_pc_gdp_pc.png)

![04_top10_co2_per_capita](../outputs/figures/04_top10_co2_per_capita.png)

![05_top5_co2_per_capita_time_series](../outputs/figures/05_top5_co2_per_capita_time_series.png)

![06_co2_per_capita_by_gdp_quartile_boxplot](../outputs/figures/06_co2_per_capita_by_gdp_quartile_boxplot.png)

![07_co2_per_capita_by_gdp_quartile_violin](../outputs/figures/07_co2_per_capita_by_gdp_quartile_violin.png)

![08_heatmap_avg_co2_per_capita_by_year_gdp_quartile](../outputs/figures/08_heatmap_avg_co2_per_capita_by_year_gdp_quartile.png)

![09_cumulative_sum_co2_per_capita](../outputs/figures/09_cumulative_sum_co2_per_capita.png)

![10_year_over_year_change_global_avg_co2_pc](../outputs/figures/10_year_over_year_change_global_avg_co2_pc.png)

![11_co2_per_capita_vs_total_co2](../outputs/figures/11_co2_per_capita_vs_total_co2.png)

## Regression Analysis

The regression model estimates the relationship between GDP per capita and CO2 emissions per capita.

```text
                            OLS Regression Results                            
==============================================================================
Dep. Variable:                 co2_pc   R-squared:                       0.556
Model:                            OLS   Adj. R-squared:                  0.553
Method:                 Least Squares   F-statistic:                     202.6
Date:                Wed, 10 Jun 2026   Prob (F-statistic):           2.41e-30
Time:                        19:23:19   Log-Likelihood:                -447.37
No. Observations:                 164   AIC:                             898.7
Df Residuals:                     162   BIC:                             904.9
Df Model:                           1                                         
Covariance Type:            nonrobust                                         
==================================================================================
                     coef    std err          t      P>|t|      [0.025      0.975]
----------------------------------------------------------------------------------
const              0.5588      0.403      1.387      0.167      -0.237       1.354
gdp_per_capita     0.0002   1.46e-05     14.235      0.000       0.000       0.000
==============================================================================
Omnibus:                       86.262   Durbin-Watson:                   2.081
Prob(Omnibus):                  0.000   Jarque-Bera (JB):              541.231
Skew:                           1.835   Prob(JB):                    2.97e-118
Kurtosis:                      11.108   Cond. No.                     3.83e+04
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
[2] The condition number is large, 3.83e+04. This might indicate that there are
strong multicollinearity or other numerical problems.
```

## Conclusion

The generated figures and regression results indicate that CO2 emissions per capita are associated with economic development, although the relationship varies across countries and over time.