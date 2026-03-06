import unittest
import sys, csv, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './../app')))

import ragbot_cli2

class RagChainTestCase(unittest.TestCase):
    def test_rag_chain(self):
        with open("golden_questions.csv", 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file, delimiter=';')
            for row in csv_reader:
                question = row[0]
                successful = row[2]
                log_data = ragbot_cli2.new_log_data(question)
                log_data = ragbot_cli2.rag_chain(question, log_data)
                self.assertEqual(str(log_data["successful"]), successful)

if __name__ == '__main__':
    unittest.main()
