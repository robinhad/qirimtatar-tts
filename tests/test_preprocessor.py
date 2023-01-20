from crh_preprocessor.preprocessor import preprocess, num2word


def test_num2word():
    assert (
        num2word(16) == "on altı"
    )
    assert (
        num2word(1324759813) == "bir milliard üç yüz yigirmi dört million yedi yüz elli doquz biñ sekiz yüz on üç"
    )
    assert (
        num2word(1_000_000) == "million"
    )


def test_preprocessor():
    assert (
        preprocess("İşanç Alla-Taalâğa.") == "işan\u04ab alla-taalâğa."
    )  # first i is two symbols (i without dot and dot)
    assert (
        preprocess("1000000") == "million"
    )
    assert (
        preprocess("1324700000") == "bir milliard üç yüz yigirmi dört million yedi yüz biñ"
    )
    assert (
        preprocess("1000002") == "bir million eki"
    )
    assert (
        preprocess("16") == "on altı"
    )
    assert (
        preprocess("001") == "sıfır sıfır bir"
    )
    assert (
        preprocess("00") == "sıfır sıfır"
    )
    assert (
        preprocess("10.02") == "on noqta sıfır eki"
    )
    assert (
        preprocess("0.01") == "sıfır noqta sıfır bir"
    )
    assert (
        preprocess("0,01") == "sıfır virgül sıfır bir"
    )
    assert (
        preprocess("00,01") == "sıfır sıfır virgül sıfır bir"
    )
    assert (
        preprocess("-10") == "minus on"
    )
    assert (
        preprocess("+10") == "plüs on"
    )
    assert (
        preprocess("+10.1400") == "plüs on noqta bir dört sıfır sıfır"
    )
    assert (
        preprocess("-10.14156") == "minus on noqta bir dört bir beş altı"
    )
    assert (
        preprocess("10,14156") == "on virgül bir dört bir beş altı"
    )
    assert (
        preprocess("1, 2, 3, 4, 5, 6,7") == "bir virgül eki virgül"
    )
    assert (
        preprocess("1,2,3,4,5,6,7") == "on altı"
    )
