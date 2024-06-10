import unittest

from modules.code_analyser.abstract_syntax_tree import AbstractSyntaxTree
from modules.code_analyser.clean_code_analyser import describe_clean_code_problems
from utilities.path_finder import PathFinder


class TestPythonCleanCode(unittest.TestCase):
    def setUp(self):
        self.language_parser = AbstractSyntaxTree()
        self.language = "python"

    def test_clean_code(self):
        filename = PathFinder().get_complet_path(path_to_file=f'ressources/{self.language}_files/code_with_cc.txt')
        expected_output = "I have not recommendation to give for the clean code"
        with open(filename, "r") as file:
            syntax_tree = self.language_parser.parse(source_code=file.read(), language=self.language)
            actual_output = describe_clean_code_problems(syntax_tree=syntax_tree, language=self.language)
        self.assertEqual(actual_output, expected_output)

    def test_no_clean_code(self):
        filename = PathFinder().get_complet_path(path_to_file=f'ressources/{self.language}_files/code_without_cc.txt')
        expected_output = ['Here is all the recommendation for the clean code', ['Name too short at line 8 it should be should be at least 3 characters.',
                                                                                  'Name too short at line 11 it should be should be at least 3 characters.',
                                                                                  'Name too short at line 13 it should be should be at least 3 characters.',
                                                                                  'Name too short at line 14 it should be should be at least 3 characters.',
                                                                                  'Name too short at line 17 it should be should be at least 3 characters.',
                                                                                  'Name too short at line 18 it should be should be at least 3 characters.',
                                                                                  'Name too short at line 19 it should be should be at least 3 characters.']]
        with open(filename, "r") as file:
            syntax_tree = self.language_parser.parse(source_code=file.read(), language=self.language)
            actual_output = describe_clean_code_problems(syntax_tree=syntax_tree, language=self.language)
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
