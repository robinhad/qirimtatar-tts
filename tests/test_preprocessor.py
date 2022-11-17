from crh_preprocessor.preprocessor import preprocess


def test_preprocessor():
    assert (
        preprocess("İşanç Alla-Taalâğa.") == "işan\u04ab alla-taalâğa."
    )  # first i is two symbols (i without dot and dot)
