import unittest
import nltk
from nltk.tokenize import word_tokenize


class MyTestCase(unittest.TestCase):
    def test_word_pas_response(self):
        yoda_sample_text = "Agree with you, the council does. Your apprentice, Skywalker will be."

        nltk_yoda_pos = nltk.pos_tag(word_tokenize(yoda_sample_text))
        print(nltk_yoda_pos)

        expected = "[('Agree', 'VB'), ('with', 'IN'), ('you', 'PRP'), (',', ','), ('the', 'DT'), ('council', 'NN'), ('does', 'VBZ'), ('.', '.'), ('Your', 'VB'), ('apprentice', 'NN'), (',', ','), ('Skywalker', 'NNP'), ('will', 'MD'), ('be', 'VB'), ('.', '.')]"

        self.assertEqual(expected, str(nltk_yoda_pos))


if __name__ == '__main__':
    unittest.main()
