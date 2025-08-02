import pandas as pd
from scipy import stats

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

