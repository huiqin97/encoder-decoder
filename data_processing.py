
import math 

def extract_punc(string_input, input_chars, output_chars):
    # this function helps to create ground-truth data and corresponding 
    # encoded output 
    input_source = []
    output_source = []
    input_length = len(string_input)
    i = 0
    while i < input_length:
        char = string_input[i]
        if char.isupper():
            output_source.append("<cap>")
            input_source.append(char.lower())

        if char in output_chars:
            output_source.append(char)
            if i < input_length - 1:
                input_source.append(string_input[i + 1])
            else:
                input_source.append(" ")
            i += 1

        if not char.isupper() and char not in output_chars and char in input_chars:
            input_source.append(char)
            output_source.append("<nop>")

        i += 1
    return input_source, output_source

def apply_punc(text_input, punctuation):
    # process the output of model 
    assert len(text_input) == len(punctuation), "input string has differnt length from punctuation list" + "".join(
        text_input) + str(punctuation) + str(len(text_input)) + ";" + str(len(punctuation))
    result = ""
    for char1, char2 in zip(text_input, punctuation):
        if char2 == "<cap>":
            result += char1.upper()
        elif char2 == "<nop>":
            result += char1
        else:
            result += char2 + char1
    return result


def chunk_gen(seq_length, src_list, filler=[" "]):
    s_l = len(src_list)
    b_n = math.ceil(s_l / seq_length)
    s_pad = src_list + filler * (b_n * seq_length - s_l)
    for i in range(b_n):
        yield s_pad[i * seq_length: (i + 1) * seq_length]


def batch_gen(src_gen, bsize):
    batch = []
    for i, src in enumerate(src_gen):
        batch.append(src)
        max_len = len(src)
        if i % bsize == bsize - 1:
            yield max_len, batch
            batch = []


# example output 
# input_chars = list(" \nabcdefghijklmnopqrstuvwxyz0123456789")
# output_chars = ["<nop>", "<cap>"] + list(".,;:?!\"'$")

# char2vec = Char2Vec(chars=input_chars, add_unknown=True) 
# input_, output_ = extract_punc("ATI'd. I'm not sure if $10 is enough. ", input_chars, output_chars)
# result = apply_punc("".join(input_), output_)
# print(result)
