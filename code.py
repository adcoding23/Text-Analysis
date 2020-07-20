import string
import collections
import random
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class TrieNode():
    def __init__(self): 
        self.children = {} 
        self.isEnd = False
        
class Trie():
    def __init__(self):
        # Initialising the trie structure. 
        self.root = TrieNode() 
        self.word_list = [] 
   
    def add_Child(self, word):
        node = self.root
        if len(word) == 0:
            self.isEnd = True
            return
        for ch in word:
            if not node.children.get(ch): 
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.isEnd = True
    
    def search_word(self,startOfSentence):
        words = startOfSentence.split(" ")
        prefix = words[-1]
        prev = startOfSentence[:-len(prefix)]
        node = self.root 
        not_found = False
        temp_word = ''
        for ch in prefix: 
            if not node.children.get(ch): 
                not_found = True
                break
  
            temp_word += ch
            node = node.children[ch] 
        if not_found: 
            return 0
        elif node.isEnd and not node.children: 
            return -1
        self.DFS(node, temp_word, prev)
        return self.word_list
        
    def DFS(self, node, word,prev):
        if node.isEnd: 
            self.word_list.append(prev + word) 
            
        for ch,node in node.children.items():
            self.DFS(node, word + ch,prev)
        
    
            
class project:
    def __init__(self):
        with open('1000_common_words.txt', 'r') as file2:
            self.common = file2.read().replace('\\n', '')
        with open('sherlock.txt', 'r') as file:
            self.text = file.read().replace('\\n', '')
    
    def text_to_string(self):
     # split into words by white space
        self.words = self.text.split()
    
        # remove punctuation from each word

        table = str.maketrans('', '', string.punctuation)
        self.filtered_words = [w.translate(table) for w in self.words]
        
        #replace common words
        self.filtered_words_common = [word for word in self.filtered_words if word.lower() not in self.common]
        
        # Counter
        self.count_All = collections.Counter(self.filtered_words)
        
        # Counter chapter wise
        self.Chapters = self.text.split('ADVENTURE')
        self.word_Chapters =[]
        for i in range(1,len(self.Chapters)):
            word = self.Chapters[i].split()
            word = [w.translate(table) for w in word]
            self.word_Chapters.append(word)
        self.count_ChapterWise = [collections.Counter(text) for text in self.word_Chapters]
        
    def getTotalNumberOfWords(self):
        return len(self.filtered_words)
    
    def getTotalUniqueWords(self): 
        return len(self.count_All)
    
    def get20MostFrequentWords(self):
        return list(self.count_All.most_common(20))
    
    def get20MostInterestingFrequentWords(self):
        self.unique_remove_common = collections.Counter(self.filtered_words_common)
        return list(self.unique_remove_common.most_common(20))
    
    def get20LeastFrequentWords(self):
        return list(self.count_All.most_common()[:-20-1:-1])
    
    def getFrequencyOfWord(self,word):
        self.count =[]
        for i in range(len(self.word_Chapters)):
            self.count.append(self.count_ChapterWise[i][word])
        return self.count
    
    def getChapterQuoteAppears(self, quote):
        for i in range(len(self.Chapters)):
            if quote in self.Chapters[i].replace('\\n', ''):
                return "Chapter:"+ str(i)
        return "Quote Not Found"
    
    def generateCache(self):
        self.cache ={}
        def pair():
            for i in range(len(self.filtered_words)-2):
                yield (self.filtered_words[i], self.filtered_words[i+1]) 
        for w1,w2 in pair():
            if w1 in self.cache:
                self.cache[w1].append(w2)
            else:
                self.cache[w1] =[w2]
    
    def generateSentence(self, curWord, size =22):
        gen_words =[]
        random_index =0
        self.generateCache()
        for i in range(size):
            gen_words.append(curWord)
            random_index= random.randint(0,len(self.cache[curWord])-1)
            curWord = self.cache[curWord][random_index]
        return ' '.join(gen_words)
    
    def getAutocompleteSentence(self, startOfSentence):
        trie = Trie()
        for word in self.filtered_words:
            trie.add_Child(word)
        return trie.search_word(startOfSentence)
p = project()
p.text_to_string()
print("----------getTotalNumberOfWords----------")
print(p.getTotalNumberOfWords())
print()
print("------------getTotalUniqueWords------------")
print(p.getTotalUniqueWords())
print()
print("------------get20MostFrequentWords------------")
print(p.get20MostFrequentWords())
print()
print("------------get20MostInterestingFrequentWords------------")
print(p.get20MostInterestingFrequentWords())
print()
print("------------get20LeastFrequentWords---------------")
print(p.get20LeastFrequentWords())
print()
print("------------getFrequencyOfWord------------")
print(p.getFrequencyOfWord('Watson'))
print()
print("------------getChapterQuoteAppears------------")
print(p.getChapterQuoteAppears("There is nothing more deceptive than an obvious fact"))
print()
print("------------generateSentence----------------")
print(p.generateSentence('Sherlock'))
print()
print("------------getAutocompleteSentence------------")
print(p.getAutocompleteSentence('I have no do'))

# Visualization
d1 = dict(p.get20MostFrequentWords())
d2 = dict(p.get20MostInterestingFrequentWords())
d3 = dict(p.get20LeastFrequentWords())
wordcloud = WordCloud()
wordcloud.generate_from_frequencies(frequencies=d2)
plt.figure()
plt.imshow(wordcloud)
plt.axis("off")
plt.show()

f, ax = plt.subplots()

freq = p.getFrequencyOfWord('Sherlock')
chapter = [1,2,3,4,5,6,7,8,9,10,11,12]
p = plt.bar(chapter, freq,color='#2e8b57')
plt.title('Usage of "Sherlock" per chapter')
plt.xlabel("Chapters")
plt.ylabel("Frequency")
ax.set_xticks(range(1, 13))
ax.set_xticklabels(chapter)
p[8].set_color('#8B0000')
p[9].set_color('#8B0000')
p[10].set_color('#8B0000')
p[11].set_color('#8B0000')
plt.show()