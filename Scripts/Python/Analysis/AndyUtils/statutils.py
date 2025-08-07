import pandas as pd
from scipy import stats
import statsmodels.api as sm

def calc_corr_with_target_pvalues(
    df: pd.DataFrame,
    target_col: str,
    p_threshold: float = 0.05
) -> pd.DataFrame:
    """
    相関係数とp値を取得し、有意かどうかを判定する関数

    Parameters:
    - df: 対象のDataFrame
    - target_col: 相関対象の列名
    - p_threshold: 有意性の判定に使うp値のしきい値（デフォルト: 0.05）

    Returns:
    - variable / correlation / p_value / significant を含むDataFrame
    """
    results = []

    for col in df.select_dtypes(include='number').columns:
        if col == target_col:
            continue

        r, p = stats.pearsonr(df[target_col], df[col])
        results.append({
            "variable": col,
            "correlation": r,
            "p_value": p,
            "significant": p <= p_threshold
        })

    return pd.DataFrame(results)

def summarize(df: pd.DataFrame) -> pd.DataFrame:
    """
    カラムごとの基礎統計値を取得

    Parameters:
    - df: 対象のDataFrame

    Returns:
    - df: 集計結果
    """
    summary = pd.DataFrame()

    summary['dtype'] = df.dtypes # 型
    summary['count'] = df.count() # 件数
    summary['unique'] = df.nunique() # ユニーク件数
    summary['nan_cnt'] = df.isna().sum() # nan件数
    # 空文字の数（文字列型の列のみチェック）
    empty_str = pd.Series({col: (df[col] == '').sum() if df[col].dtype == 'object' else 0 for col in df.columns})
    summary["empty_str"] = empty_str
    # NaN + 空文字の合計
    summary["missing_total"] = summary["nan_cnt"] + summary["empty_str"]

    # 数値列の統計量
    desc = df.describe().T[['mean', 'std', 'min', '25%', '50%', '75%', 'max']]

    summary = summary.join(desc)

    return summary



def standardize_df(df: pd.DataFrame, cols: list = None) -> pd.DataFrame:
    """
    指定した列（または全数値列）をZスコア標準化して返す関数

    Parameters:
    - df: 元のDataFrame
    - cols: 標準化対象のカラムリスト。Noneなら全数値列を対象

    Returns:
    - 標準化後のDataFrame（元のdfは変更しない）
    """
    from sklearn.preprocessing import StandardScaler

    if cols is None:
        cols = df.select_dtypes(include='number').columns.tolist()

    scaler = StandardScaler()
    df_scaled = df.copy()
    df_scaled[cols] = scaler.fit_transform(df[cols])

    return df_scaled



def fit_multivariate_regression_with_pvalues(df: pd.DataFrame, target_col: str):
    X = df.drop(columns=[target_col]).select_dtypes(include='number')
    y = df[target_col]

    X = sm.add_constant(X)  # 定数項（切片）を追加

    model = sm.OLS(y, X).fit()

    # 回帰結果の概要
    summary = model.summary()

    # 係数とp値をDataFrameで取得
    coef_pvalues = pd.DataFrame({
        'coefficient': model.params,
        'p_value': model.pvalues
    })

    return model, coef_pvalues, summary