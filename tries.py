"""Honors Project - Zach Arnold
"""
from string import punctuation

class TrieNode:

    def __init__(self, val, end=False):
        """Initialization of a node
        
        :param val: value stored at node
        :type val: str
        :param end: flag signifying if node is at end of word, defaults to False
        :type end: bool, optional
        """
        self._val = val
        self._end = end
        self._children = {}     # stores children in pairs of {val: node}

    def __repr__(self):
        """Returns string representation of node for debugging
        """
        return '\n~Node (' + str(self._val) + ') has ' + str(len(self._children)) + ' children: ' + str(sorted([val for val in self._children])) + '~'

    def is_leaf(self):
        """Returns whether or not TrieNode is a leaf node
        """
        return len(self._children) == 0

    def get_value(self):
        """Returns value of TrieNode
        """
        return self._val

    def set_child(self, val, end=False):
        """Creates and adds child to TrieNode
        
        :param val: value stored at node to create
        :type val: str
        :param end: flag signifying if node is at end of word, defaults to False
        :type end: bool, optional
        """
        self._children[val] = TrieNode(val, end)

    def get_child(self, val):
        """Returns child node with given value, returns None if doesn't exist
        
        :param val: value of child to return
        :type val: TrieNode
        """
        if val in self._children:
            return self._children[val]

    def get_children(self):
        """Returns list of nodes representing self's children
        """
        return [node for node in self._children.values()]

    def delete_child(self, val):
        """Removes and returns child node with given value from children
        
        :param val: value of child to remove
        :type val: TrieNode
        """
        del self._children[val]
        return val

    def set_end(self, on = True):
        """Sets end flag as true; returns None
        """
        self._end = on

    def get_end(self):
        """Returns value of end flag
        """
        return self._end



class Trie:

    def __init__(self):
        """Initialization of Trie data structure
        """
        self.root = TrieNode('*')
        self.size = 0
    
    def __repr__(self):
        """Returns string representation of trie; for use in debugging
        """
        return '\nSize: ' + str(self.size) + '\nLibrary: ' + str(self.get_library(self.root, library = []))

    def is_empty(self):
        """Returns whether or not trie is empty
        """
        return self.size == 0

    def insert_word(self, word):
        """Insert word into trie; returns None
        
        :param word: word to add into library
        :type word: str
        """
        if word:
            current = self.root
            for letter in word:
                
                if not current.get_child(letter):      # if letter is not a child of current node
                    current.set_child(letter)             # add letter as a child

                current = current.get_child(letter)
            
            if not current.get_end():
                current.set_end()       # set last letter of word to end if word not already in trie
                self.size += 1

    def search_word(self, word):
        """Searches trie to find param word
        
        :param word: word to search for
        :type word: str
        """
        current = self.root
        for letter in word:
            
            current = current.get_child(letter)         # node is not next letter in word

            if not current:             # if node is null, return False
                return False
        
        if not current.get_end():
            return False
        return True
            
    def search_prefix(self, prefix):
        """Searches trie to find prefix
        
        :param prefix: prefix to search for
        :type prefix: str
        :return: position of prefix's end in trie if found, otherwise None
        :rtype: TrieNode
        """
        current = self.root
        for letter in prefix:

            current = current.get_child(letter)

            if not current:
                return

        return current

    def remove_word(self, word, root, depth = 0):
        """Recursively removes word from trie if in trie; returns None
        
        :param word: word to remove
        :type word: str
        :param root: node to begin search for word at
        :type root: TrieNode
        """
        found = False
        if depth == len(word):
            if root.get_end():      
                root.set_end(False)
                self.size -= 1
                return True         # Returns true if word is found
            
            return False            # Returns false if word is a prefix        
        
        child = root.get_child(word[depth])
        if child:
            found = self.remove_word(word, child, depth + 1)  
            
            if found and child.is_leaf():
                root.delete_child(child.get_value())

        return found
        
    def get_library(self, root, path = [], library = []):
        """Recursively traverses trie and returns list of known words
        
        :param root: Node to begin searching words from
        :type root: TrieNode
        :param path: keeps track of nodes traversed from root, defaults to []
        :type path: list, optional
        :param library: keeps track of words found in trie, defaults to []
        :type library: list, optional
        :return: list of known words
        :rtype: list
        """
        if root.get_end():
            library.append("".join(path))

        if root.is_leaf():
            return library

        for child in root.get_children():
            path.append(child.get_value())
            library = self.get_library(child, path, library)
            path.pop()

        return library

    def convert_from_text(self, file_name):
        """Converts contents of a .txt file into the trie
        
        :param file_name: file to add contents into trie
        :type file_name: .txt file
        """
        with open(file_name, 'r') as reader:
            words_list = []
            for line in reader:
                words_list.extend(line.split())

            for word in set(words_list):
                if word.isalpha():
                    self.insert_word(word.lower())
                else:
                    self.insert_word(''.join([c for c in word if c.isalpha()]).lower())

    def guess_word(self, prefix):
        """Returns a list of all words that word could extend into
        
        :param prefix: prefix string to perform guess on
        :type prefix: str
        """
        prefix = prefix.lower()
        current = self.search_prefix(prefix)
        if current:
            print("You typed: " + '"' + prefix + '"')
            if current.get_end():
                print('"' + prefix + '" is a word, but you could have also been typing out:')
            else:
                print('"' + prefix + '" is not a word, perhaps you were typing out:')
            library = [prefix + word for word in self.get_library(current, library = [])]
            for word in library:
                print(word)
            return library     # list includes empty string if its already a word
        print("I'm not quite sure what you meant by " + '"' + prefix + '"...')
        return []

    def word_hunt(self, matrix):
        """Application problem: Uses trie data structure to find all valid words within matrix

        :param matrix: matrix to search through
        :type matrix: nested list
        :return: list of words found
        :rtype: list
        """
        moves = [(-1, 1), ( 0, 1), ( 1, 1),                   # Grid of all possible moves around matrix
                 (-1, 0),          ( 1, 0),
                 (-1,-1), ( 0,-1), ( 1,-1)]

        results = []
        for y in range(len(matrix)):
            for x in range(len(matrix[y])):             # Search starting at every spot in matrix
                results += self._word_hunt_recursive(matrix, y, x, set([(x, y)]), moves, matrix[y][x])
        return list(set(results))

    def _word_hunt_recursive(self, matrix, y, x, visited, moves, word):
        """Recursive function that returns a list of words found in grid using DFS

        :param matrix: matrix to search through
        :type matrix: nested list
        :param y: y-coordinate of current matrix position
        :type y: int
        :param x: x-coordinate of current matrix position
        :type x: int
        :param visited: set of coordinates in matrix already visited
        :type visited: set
        :param moves: list of possible moves relative from current position
        :type moves: list
        :param word: word currently being looked at
        :type word: str
        :return: list of words found
        :rtype: list
        """
        found = []
        if not self.search_prefix(word):            # If prefix doesn't exist in trie, sieze operations
            return found
        if self.search_word(word):                  # If word is found, add to found list but keep going!
            found.append(word)

        for dx, dy in moves:
            new_x = x + dx
            new_y = y + dy
            if new_x >= 0 and new_y >= 0 and new_y < len(matrix) and new_x < len(matrix[y]) and (new_x, new_y) not in visited:
                visited.add((new_x, new_y))
                found.extend(self._word_hunt_recursive(matrix, new_y, new_x, visited, moves, word + matrix[new_y][new_x]))
                visited.remove((new_x, new_y))
        return list(set(found))                     # Set to list to remove duplicates

        


