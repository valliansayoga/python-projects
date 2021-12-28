import justpy as jp
from pandas.core.dtypes.common import classes  # Libraries for web app & graphs


def app():
    wp = (
        jp.QuasarPage()
    )  # wp = webpage | QuasarPage adalah nama framework built in javascript. Jadi tiap element dimasukan ke QuasarPage
    h1 = jp.QDiv(
        a=wp, text="Analysis of Course Reviews", classes="text-h3 text-center q-pa-md"
    )  # Division is HTML element | Tiap styling dipisah dengan space
    p1 = jp.QDiv(
        a=wp,
        text="These graphs represent course review analysis",
        classes="text-body1 text-center q-pa-md",
    )  # p = paragraph
    return wp


jp.justpy(
    app
)  # .justpy expects a function that returns QuasarPage dan harus distop sebelum next execution
