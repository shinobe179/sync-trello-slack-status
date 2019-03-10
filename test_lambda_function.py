import unittest
import src.lambda_function as lf

class TestClient(unittest.TestCase):

    def setUp(self):
        self.lf = lf

    def test_get_request_to_trello(self):
        pass

    def test_search_list_id(self):
        self.test_trello_lists = [{'name': 'ToDo', 'id': '001'}, {'name': 'Doing', 'id': '002'}, {'name': 'Done', 'id': '003'}]

        self.assertEqual(lf.search_list_id('ToDo', self.test_trello_lists), '001')

    def test_get_trello_task_count(self):
        pass

    def test_return_emoji(self):
        self.test_arg_list = [0, 10, 20, 30, 40, 50, None]
        self.test_ans_list = [':laughing:', ':smiley:', ':neutral_face:', ':fearful:', ':exploding_head:', ':exploding_head:', ':drooling_face:']

        for i in range(len(self.test_arg_list)):
            self.assertEqual(lf.return_emoji(self.test_arg_list[i]), self.test_ans_list[i])

    def test_change_slack_status(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)
