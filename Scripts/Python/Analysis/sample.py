# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.17.2
#   kernelspec:
#     display_name: .venv
#     language: python
#     name: python3
# ---

# # モジュールの使い方

# +
from sklearn.datasets import load_iris
import pandas as pd
from AndyUtils import statutils


# 常に最新モジュールを読み込む
# %load_ext autoreload
# %autoreload 2
# -

# ## データセット読み込み

# +
# データを読み込む
iris = load_iris()

# DataFrameに変換
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df = df.rename({
    'sepal length (cm)': 'sepal_l',
    'sepal width (cm)': 'sepal_w',
    'petal length (cm)': 'petal_l',
    'petal width (cm)': 'petal_w'
},axis=1)
df["target"] = iris.target
df.head()
# -

# ## サマライズ

statutils.summarize(df=df)

# ## 目的変数に対する相関係数取得

statutils.calc_corr_with_target_pvalues(df=df, target_col='sepal_l')

# ## 標準化

statutils.standardize_df(df=df)

statutils.standardize_df(df=df, cols=["sepal_l","sepal_w","petal_l"])

statutils.fit_multivariate_regression_with_pvalues(df=df, target_col="petal_w")
