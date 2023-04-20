import unittest

from Lab13_1 import Note, Trie

class TestNoteAndTrie(unittest.TestCase):

    def test_note_creation(self):
        note = Note("Ivanov", "Ivan", "1234567890", [1, 1, 1990])
        self.assertEqual(note.last_name, "Ivanov")
        self.assertEqual(note.first_name, "Ivan")
        self.assertEqual(note.phone_number, "1234567890")
        self.assertEqual(note.birth_date, [1, 1, 1990])

    def test_trie_insert_and_search(self):
        trie = Trie()
        note = Note("Ivanov", "Ivan", "1234567890", [1, 1, 1990])
        trie.insert(note)

        found_note = trie.search("1234567890")
        self.assertIsNotNone(found_note)
        self.assertEqual(found_note.last_name, "Ivanov")
        self.assertEqual(found_note.first_name, "Ivan")
        self.assertEqual(found_note.phone_number, "1234567890")
        self.assertEqual(found_note.birth_date, [1, 1, 1990])

    def test_trie_delete(self):
        trie = Trie()
        note = Note("Ivanov", "Ivan", "1234567890", [1, 1, 1990])
        trie.insert(note)

        trie.delete("1234567890")
        found_note = trie.search("1234567890")
        self.assertIsNone(found_note)

if __name__ == '__main__':
    unittest.main()
