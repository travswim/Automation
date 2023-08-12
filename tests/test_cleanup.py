import unittest
import os
from datetime import datetime, timedelta
from unittest.mock import patch
from src.file_cleanup import FileCleanup  # Replace 'your_module' with wherever FileCleanup is located


class TestFileCleanup(unittest.TestCase):

    @patch('os.path.expanduser')
    @patch('os.listdir')
    @patch('os.path.getctime')
    @patch('os.path.isfile')
    @patch('os.remove')
    def test_file_cleanup(self, mock_remove, mock_isfile, mock_getctime, mock_listdir, mock_expanduser):
        # Mocked values
        test_directory = "/mocked/directory"
        mock_files = ['old_file_1.txt', 'old_file_2.txt', 'new_file_1.txt', 'new_file_2.txt']
        file_ages = {
            'old_file_1.txt': (datetime.now() - timedelta(days=40)).timestamp(),
            'old_file_2.txt': (datetime.now() - timedelta(days=31)).timestamp(),
            'new_file_1.txt': (datetime.now() - timedelta(days=20)).timestamp(),
            'new_file_2.txt': (datetime.now() - timedelta(days=10)).timestamp()
        }

        # Configure mocks
        mock_expanduser.return_value = test_directory
        mock_listdir.return_value = mock_files
        mock_getctime.side_effect = lambda path: file_ages[os.path.basename(path)]
        mock_isfile.return_value = True

        # Call the method
        FileCleanup.file_cleanup(test_directory)

        # Assertions
        # The files older than 30 days should be removed
        mock_remove.assert_any_call(os.path.join(test_directory, 'old_file_1.txt'))
        mock_remove.assert_any_call(os.path.join(test_directory, 'old_file_2.txt'))

        # The files younger than 30 days should not be removed
        self.assertNotIn(((os.path.join(test_directory, 'new_file_1.txt'),), {}), mock_remove.call_args_list)
        self.assertNotIn(((os.path.join(test_directory, 'new_file_2.txt'),), {}), mock_remove.call_args_list)


if __name__ == '__main__':
    unittest.main()
