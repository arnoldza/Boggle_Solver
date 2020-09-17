import unittest
from tries import TrieNode, Trie



class TestTries(unittest.TestCase):

    def test_nodes(self):
        # Tests all 8 node member functions, (getters and setters)

        # Test is_leaf, get_value, get_child, set_child
        node = TrieNode('a')

        assert node.is_leaf() == True
        assert node.get_value() == 'a'
        assert node.get_child('c') == None
        node.set_child('c')
        assert node.is_leaf() == False
        
        # Test get_children
        child = node.get_child('c')

        assert child != None
        assert child.is_leaf() == True
        assert child.get_value() == 'c'
        assert child.get_children() == []
        child.set_child('e')
        assert len(child.get_children()) == 1

        # Test set_end, get_end
        grandchild = child.get_child('e')

        assert grandchild != None
        assert grandchild.get_end() == False
        grandchild.set_end()
        assert grandchild.get_end() == True
        grandchild.set_end(False)
        assert grandchild.get_end() == False

        # Test delete_child
        assert child.is_leaf() == False
        child.delete_child('e')
        assert child.is_leaf() == True
        assert child.get_children() == []


    def test_insert_word(self):

        # Test is_empty
        retrieval = Trie()

        assert retrieval.is_empty() == True

        # Test empty word
        retrieval.insert_word('')
        assert retrieval.is_empty() == True

        # Test insert_word
        word = 'sideways'
        retrieval.insert_word(word) 

        current = retrieval.root
        for letter in word:
            assert current.get_end() == False
            current = current.get_child(letter)
            assert current != None

        assert current.get_end() == True
        assert retrieval.size == 1

        # Test substring
        sub_word = 'side'
        retrieval.insert_word(sub_word)

        current = retrieval.root
        for letter in sub_word:
            assert current.get_end() == False
            current = current.get_child(letter)
            assert current != None

        assert current.get_end() == True
        assert retrieval.size == 2

        # Test new word
        new_word = 'different'
        retrieval.insert_word(new_word)

        current = retrieval.root
        for letter in new_word:
            assert current.get_end() == False
            current = current.get_child(letter)
            assert current != None

        assert current.get_end() == True
        assert retrieval.size == 3

        # Test dupicate
        retrieval.insert_word(new_word)
        assert retrieval.size == 3

        # Test empty word
        retrieval.insert_word('')
        assert retrieval.size == 3


    def test_search_word(self):

        retrieval = Trie()

        retrieval.insert_word('dog')
        retrieval.insert_word('do')
        retrieval.insert_word('dot')
        retrieval.insert_word('pump')
        retrieval.insert_word('fat')
        retrieval.insert_word('fire')

        assert retrieval.size == 6

        # Test search_word
        # Test empty string
        assert retrieval.search_word('') == False

        # Test complete words
        assert retrieval.search_word('dog') == True
        assert retrieval.search_word('pump') == True
        assert retrieval.search_word('do') == True
        assert retrieval.search_word('fire') == True

        # Test subtrings/ inclusionary strings
        assert retrieval.search_word('fir') == False
        assert retrieval.search_word('fireball') == False
        assert retrieval.search_word('father') == False

        # Test words not in trie
        assert retrieval.search_word('word') == False
        assert retrieval.search_word('snow') == False
        assert retrieval.search_word('other') == False

        # Test search_prefix
        # Test empty string
        assert retrieval.search_prefix('') == retrieval.root

        # Test complete word
        dog_end = retrieval.root.get_child('d').get_child('o').get_child('g')
        assert retrieval.search_prefix('dog') == dog_end
        assert dog_end.get_end() == True

        # Test substring
        fir_end = retrieval.root.get_child('f').get_child('i').get_child('r')
        assert retrieval.search_prefix('fir') == fir_end
        assert fir_end.get_end() == False

        # Test words not in trie
        assert retrieval.search_prefix('word') == None
        assert retrieval.search_prefix('snow') == None
        assert retrieval.search_prefix('other') == None
        assert retrieval.search_prefix('fireball') == None


    def test_remove_word(self):

        retrieval = Trie()
        root_node = retrieval.root

        retrieval.insert_word('dog')
        retrieval.insert_word('do')
        retrieval.insert_word('dot')
        retrieval.insert_word('pump')
        retrieval.insert_word('fat')
        retrieval.insert_word('fire')

        assert retrieval.size == 6
        
        # Test empty string
        assert retrieval.remove_word('', root_node) == False
        assert retrieval.size == 6

        # Test complete word
        assert retrieval.search_word('dog') == True
        assert retrieval.remove_word('dog', root_node) == True
        assert retrieval.search_word('dog') == False
        assert retrieval.size == 5
        
        retrieval.insert_word('dog')
        assert retrieval.search_word('dog') == True
        assert retrieval.size == 6

        # Test substring
        assert retrieval.search_word('do') == True
        assert retrieval.remove_word('do', root_node) == True
        assert retrieval.search_word('do') == False
        assert retrieval.search_word('dog') == True
        assert retrieval.size == 5

        assert retrieval.search_word('pum') == False
        assert retrieval.remove_word('pum', root_node) == False
        assert retrieval.size == 5

        # Test word not in trie
        assert retrieval.remove_word('absent', root_node) == False
        assert retrieval.size == 5


    def test_get_library(self):

        retrieval = Trie()
        root_node = retrieval.root

        # Test get_library
        # Test empty trie
        assert retrieval.get_library(root_node, library = []) == []

        # Test non empty trie
        retrieval.insert_word('dog')
        retrieval.insert_word('do')

        expected = ['dog', 'do']
        solution = retrieval.get_library(root_node, library = [])
        for word in solution:
            assert word in expected
        assert len(solution) == 2

        retrieval.insert_word('dot')
        retrieval.insert_word('pump')
        retrieval.insert_word('fat')
        retrieval.insert_word('fire')

        expected = ['dog', 'do', 'dot', 'pump', 'fat', 'fire']
        solution = retrieval.get_library(root_node, library = [])
        for word in solution:
            assert word in expected
        assert len(solution) == 6

        # Test after removal
        retrieval.remove_word('dot', root_node)
        retrieval.remove_word('fire', root_node)

        expected = ['dog', 'do', 'pump', 'fat']
        solution = retrieval.get_library(root_node, library = [])
        for word in solution:
            assert word in expected
        assert len(solution) == 4


        # Test guess_word
        retrieval = Trie()

        retrieval.insert_word('dog')
        retrieval.insert_word('do')
        retrieval.insert_word('dot')
        retrieval.insert_word('pump')
        retrieval.insert_word('fat')
        retrieval.insert_word('fire')

        # Test empty string
        expected = ['dog', 'do', 'dot', 'pump', 'fat', 'fire']
        solution = retrieval.guess_word('')
        for word in solution:
            assert word in expected
        assert len(solution) == 6

        # Test prefix
        expected = ['dog', 'do', 'dot']
        solution = retrieval.guess_word('do')
        for word in solution:
            assert word in expected
        assert len(solution) == 3

        expected = ['fat', 'fire']
        solution = retrieval.guess_word('f')
        for word in solution:
            assert word in expected
        assert len(solution) == 2

        # Test word not in trie
        solution = retrieval.guess_word('null')
        assert solution == []

    def test_word_hunt(self):

        # Test convert_from_text
        retrieval = Trie()
        root_node = retrieval.root
        retrieval.insert_word('first')

        expected = ['first', 'find', 'for', 'from', 'frighten', 'face', 
                    'it', 'its', 'in', 'instead', 'into', 'him', 'himself', 
                    'his', 'he', 'happened', 'had', 'having', 'hunted', 
                    'holding', 'saw', 'swift', 'steak', 'steaks', 'steal', 
                    'stream', 'stolen', 'snatch', 'see', 'sign', 'shop', 'left', 
                    'looking', 'large', 'barked', 'banks', 'being', 'been', 
                    'butchers', 'what', 'when', 'which', 'was', 'water', 'with', 
                    'woods', 'the', 'then', 'though', 'thought', 'that', 'thinking', 
                    'trace', 'two', 'time', 'to', 'upon', 'unluckily', 'never', 'no', 
                    'nothing', 'greedy', 'or', 'other', 'of', 'on', 'only', 'once', 
                    'over', 'realize', 'reaching', 'reflection', 'reflected', 
                    'ran', 'current', 'could', 'couldnt', 'course', 'carried', 
                    'did', 'dog', 'dogs', 'dropped', 'mouth', 'moment', 'meat', 
                    'meant', 'managed', 'a', 'another', 'and', 'all', 'at', 'away', 
                    'vanished', 'jumped', 'peace', 'eat']

        retrieval.convert_from_text('greedog.txt')
        assert retrieval.size == 98

        solution = retrieval.get_library(root_node, library = [])
        for word in solution:
            assert word in expected
        assert len(solution) == 98
        
        # Test word_hunt
        # 2x2 grid
        grid = [['f','n'],
                ['d','i']]
        
        expected = ['find', 'in']
        solution = retrieval.word_hunt(grid)
        for word in solution:
            assert word in expected
        assert len(solution) == 2


        # 4x4 grid
        grid = [['w','t','s','m'],
                ['i','e','a','w'],
                ['a','i','g','s'],
                ['h','k','n','e']]

        expected = ['steak', 'saw', 'its', 'at', 'eat', 'in', 'a', 'it', 'was']
        solution = retrieval.word_hunt(grid)
        for word in solution:
            assert word in expected
        assert len(solution) == 9


        # 6x6 grid
        grid = [['c','s','e','t','t','o'],
                ['i','y','k','t','y','k'],
                ['m','i','c','h','i','g'],
                ['t','a','t','s','n','a'],
                ['e','u','n','i','v','e'],
                ['x','y','t','i','s','r']]

        expected = ['it', 'in', 'snatch', 'to', 'eat', 'sign', 'at', 'its', 'his', 'a']
        solution = retrieval.word_hunt(grid)
        for word in solution:
            assert word in expected
        assert len(solution) == 10



if __name__ == "__main__":
    unittest.main()