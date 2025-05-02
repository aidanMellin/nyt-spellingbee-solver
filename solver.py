import os
import string

class Node:
    def __init__(self):
        self.children = {} # dict of all the letters that function as children in a given node (no duplicates and O(1) lookup)
        self.endIdentifier = False

class Trie:
    def __init__(self):
        self.root = Node() #Store the root node
    
    """Insert a string into the trie
    """
    def insert(self, key): #pass a full string when inserting
        curr = self.root
        for c in key:
            if not c in curr.children:
                curr.children[c] = Node()
            curr = curr.children[c]
        curr.endIdentifier = True

    """Determine if the full word passed in exists as a complete string with endWordIdentifier
    """
    def search(self, key: str) -> bool:
        curr = self.root
        for c in key:
            if not curr.children[c]:
                return False
            curr = curr.children[c]
        return curr.endIdentifier

    """Determine if passed string exists at least partially in trie
    """
    def is_prefix(self, prefix):
        curr = self.root
        for c in prefix:
            if not c in curr.children:
                return False
            curr = curr.children[c]
        return True


class Words:
    def __init__(self):
        self.words = Trie() #Trie of all words parsed from dict
        self.searchLetters = None #The specific letters to today's spelling bee
        self.centerLetter = None #The letter that needs to be present in every search
        self.longestWord = 0 #Just set an upper bound on how deep we can search recursively

        self.MIN_LEN_ANS_RTN = 3 #Change this if you want to include words < len(3)
        self.NYT_EXACT_SEARCH_STRING = True #Should it be exactly 7 characters?
        self.USE_CENTER_LETTER = True #Require center letter in all returned answers

    """load words into trie from a file
    """
    def load_words(self, fn):
        while not os.path.isfile(fn):
            print("File must exist in current context!")
            fn = input("Enter a filename that you would like to use as your wordbase: ")
        print("Trie-ing your words\n")
        with open(fn, "r") as f:
            for line in f:
                self.words.insert(line.strip().lower()) #Put it in the trie
                self.longestWord = max(len(line), self.longestWord) #Longest word check

    """
    Given the searchletter string (with post processing to only check the valid alpha values)
    Precondition: the first alpha character in the string MUST be the central letter that determines if a word is valid or not
    """
    def find_words(self, searchLetters):
        while(not len(searchLetters) == 7 and self.NYT_EXACT_SEARCH_STRING):
            print("Search string not to NYT specs. Set NYT_EXACT_SEARCH_STRING variable to false to disable this feature")
            searchLetters = input("Enter your letters you would like to search for, with the center letter as the first added letter: ").replace(" ", "").replace(",", "")
        self.searchLetters = searchLetters
        self.centerLetter = searchLetters[0] #Will always assume 0th index is the primary letter
        return self.find_valid_permutations()

    """Use DFS to find all valid permutations with duplicate values .

    Return a (pangram, list of all possible words) given:
        - All words exist in passed dictionary file
        - The returned word contains the central letter

        (a pangram is a word that uses every letter in the searchLetters at least once)
    """
    def find_valid_permutations(self):
        """
        Essentially we want to find all possible permutations and subsets of a string SO LONG as it contains the center letter
        This is permutations including subsets, and only add them to the return if they exist in a search of the trie

        Subproblem:
            k - orig length, length decreases by how many entries we have in current perm
            for every pass, determine if current perm in searchLetters (dict - O(1)). 
                If it is, add it to return array.
                if i < k and prefix is valid prefix, recurse
                Backtrack 
        """

        temp = ""
        ans = []

        """DFS on the word trie to find words that:
                - > 3 letters (or whatever self.MIN_LEN_ANS_RTN is set to)
                - Center letter exists in the word OR self.USE_CENTER_LETTER is set to false
                - Exists in the word trie
            Uses backtracking to find all possible solutions with a maximum depth recursion that is the length of the longest word in the passed dictionary file
        """
        def dfs(temp):
            #if its a valid word, if we have the center letter [optional], if its length is > minimum allowed
            if (self.words.search(temp) and 
                    (self.centerLetter in temp or not self.USE_CENTER_LETTER) and
                    len(temp) > self.MIN_LEN_ANS_RTN):
                ans.append(temp)
                return
            for i in self.searchLetters:
                temp+=i
                if len(temp) <= self.longestWord and self.words.is_prefix(temp):
                    dfs(temp)
                temp=temp[:-1]

        dfs(temp)

        pangrams = []
        
        """
        Bitwise comparison to convert a given string into a mask

        Take your mask, and bitwise Or against a 1 that is shifted X bits to the left, where X is the difference between ord(c) and ord("a")
        """
        def bitmask(s): 
            mask = 0
            for c in s:
                mask |= 1 << ord(c) - ord('a')
            return mask

        search_mask = bitmask(self.searchLetters) #Get the base mask to compare against
        for word in ans:
            word_mask = bitmask(word) #Mask the word to compare
            if (word_mask & search_mask) == search_mask: 
                pangrams.append(word)
        
        ans.sort(key=lambda x: len(x))
        return (pangrams, ans)

# myTrie = Trie()
# myTrie.insert("feeble")
# myTrie.insert("tree")
# myTrie.insert("long")
# myTrie.insert("log")
# myTrie.insert("goon")
# myTrie.insert("gin")

w = Words()

w.load_words(input("Enter a filename that you would like to use as your wordbase: "))

w.find_words(input("Enter your letters you would like to search for, with the center letter as the first added letter: ").replace(" ", "").replace(",", ""))
# w.words = myTrie
# w.searchLetters = "gloni"
# w.centerLetter = "g"
# w.longestWord = 6
ans = w.find_valid_permutations()
print(f"""Pangrams Found: {", ".join(ans[0])}
Other solutions: {", ".join(ans[1])}""")
