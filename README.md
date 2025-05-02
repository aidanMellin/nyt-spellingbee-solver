# nyt-spellingbee-solver
Python Program to solve a given day's NYT Games Spelling Bee

Fairly simple day project to help me practice Tries, Recursion, etc

## Process is as follows:
1. Have a dictionary of words (the one I have isn't great, but works for testing purposes and can often get the pangram(s) for the day's spelling bee
2. Build a trie of all of the words in a dictionary
3. Given a string of search letters (s), iterate through s and recursively append words that fit the following criteria to return:
     - Contains the central letter
     - Exists in the dictionary
     - There are some additional inclusions to help reduce time-complexity of the program which are:
         - Check if the checked word up until this point exists as a prefix in the tree (if it doesn't, abandon it)
         - Check against the longest word that is contained in the entire dictionary to set a bottom depth cutoff
4. Find the pangram(s) for today's spelling bee *a pangram is described as a word that contains every letter in the search string at least once*
     - make a bitwise mask of the search string and each word in the returned list
     - bitwise or + shift a 1 x digits left where x is the ord(current character) - ord('a')
5. Return the pangram and answer list
6. Profit 

[![Video](file:demoRec.mp4)
