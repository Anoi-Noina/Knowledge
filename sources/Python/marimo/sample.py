import marimo

__generated_with = "0.19.4"
app = marimo.App()


@app.cell
def _():
    import pandas as pd
    return (pd,)


@app.cell
def _(pd):
    df = pd.DataFrame(
        {
            "name":["banana","apple"]
            ,"price":[100,200]
        }
    )
    return (df,)


@app.cell
def _(df):
    df.head()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
