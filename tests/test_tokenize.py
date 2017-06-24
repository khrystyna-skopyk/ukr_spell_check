import unittest
from scripts.split_tokenize import snippet_to_tokens

CASE_1 = "Відсутність мотивації дає нам привід займатися сторонніми справами, " \
         "йти подумки від головних завдань.\nНіхто не говорить, що потрібно 8 " \
         "годин постійно працювати, ні на що не відволікатися, не відпочивати. " \
         "Ми говоримо про ефективне використання робочого часу як раз для того," \
         " щоб мати більше вільного часу для відпочинку, розваг та особистого життя."

class TestTokenize(unittest.TestCase):

    def instance_tokenized(self):
        returned = snippet_to_tokens(CASE_1)
        self.assertIsInstance(returned, list)

    def instance_tokens(self):
        returned = snippet_to_tokens(CASE_1)
        self.assertTrue(all([str(x) for x in returned[0][2]]))

    def len_tokenized(self):
        returned = snippet_to_tokens(CASE_1)
        self.assertEqual(len(returned[0]), 1)

    def tokens_number(self):
        returned = snippet_to_tokens(CASE_1)
        self.assertEqual(len(returned[0][0]), 15)



if __name__ == '__main__':
    unittest.main()