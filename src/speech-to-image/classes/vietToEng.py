from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class VietToEng :
    tokenizer_vi2en = AutoTokenizer.from_pretrained("vinai/vinai-translate-vi2en", src_lang="vi_VN")
    model_vi2en = AutoModelForSeq2SeqLM.from_pretrained("vinai/vinai-translate-vi2en")

    def translate_vi2en(self, vi_text: str) -> str:
        input_ids = self.tokenizer_vi2en(vi_text, return_tensors="pt").input_ids
        output_ids = self.model_vi2en.generate(
            input_ids,
            do_sample=True,
            max_new_tokens=1024,
            top_k=100,
            top_p=0.8,
            decoder_start_token_id=self.tokenizer_vi2en.lang_code_to_id["en_XX"],
            num_return_sequences=1,
        )
        en_text = self.tokenizer_vi2en.batch_decode(output_ids, skip_special_tokens=True)
        en_text = " ".join(en_text)
        return en_text

# vi_text = "Cô cho biết: trước giờ tôi không đến phòng tập công cộng, mà tập cùng giáo viên Yoga riêng hoặc tự tập ở nhà. Khi tập thể dục trong không gian riêng tư, tôi thoải mái dễ chịu hơn."
# print(translate_vi2en(vi_text))

# vi_text = "con mèo xanh lá cây"
# print(translate_vi2en(vi_text))