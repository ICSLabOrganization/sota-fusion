from classes.vietToEng import VietToEng

# import engToImgFunc

# import sentencepiece

translator = VietToEng()


def translate(vi_text):
    return translator.translate_vi2en(vi_text)


# string = "con mèo đen"
# print(translate(string))
