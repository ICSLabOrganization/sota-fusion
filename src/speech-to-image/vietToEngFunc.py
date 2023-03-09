from classes.vietToEng import VietToEng



translator = VietToEng()


def translate(vi_text):
    return translator.translate_vi2en(vi_text)

