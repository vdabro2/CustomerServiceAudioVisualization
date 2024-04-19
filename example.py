import pysentiment2 as ps
hiv4 = ps.HIV4()
# your attitude has been disgusting, condescending
tokens = hiv4.tokenize('disgusting, condescending')  # text can be tokenized by other ways
                                  # however, dict in HIV4 is preprocessed
                                  # by the default tokenizer in the library
score = hiv4.get_score(tokens)
print(score) # {'Positive': 0, 'Negative': 1, 'Polarity': -0.9999990000010001, 'Subjectivity': 0.9999990000010001}