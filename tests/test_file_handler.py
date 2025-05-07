import pytest
import os
import tempfile
from src.file_handler import load_reviews, save_analysis_results, get_available_files

def test_load_reviews():
    # temporary file with test content
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp:
        temp.write("This is a great product!\n")
        temp.write("Not bad, but could be better.\n")
        temp.write("Terrible experience.\n")
        temp_path = temp.name

    try:
        reviews = load_reviews(temp_path)
        assert len(reviews) == 3
        assert "This is a great product!" in reviews
        assert "Not bad, but could be better." in reviews
        assert "Terrible experience." in reviews

        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as empty_temp:
            empty_path = empty_temp.name
        assert len(load_reviews(empty_path)) == 0

    finally:
        # clean up temps
        os.unlink(temp_path)
        os.unlink(empty_path)

def test_get_available_files():
    with tempfile.TemporaryDirectory() as temp_dir:
        test_files = ['test1.txt', 'test2.csv', 'test3.txt']
        for file in test_files:
            with open(os.path.join(temp_dir, file), 'w') as f:
                f.write('test content')

        files = get_available_files(temp_dir)
        assert len(files) == 3
        assert all(file in files for file in test_files) 