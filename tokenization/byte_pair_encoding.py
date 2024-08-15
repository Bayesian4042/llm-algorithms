corpus = [
    "This is the Hugging Face Course.",
    "This chapter is about tokenization.",
    "This section shows several tokenizer algorithms.",
    "Hopefully, you will be able to understand how they are trained and generate tokens.",
]

# pretokenize the corpus into words.
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("gpt2")

# compute frequency of each word
from collections import defaultdict
word_freq = defaultdict(int)

for text in corpus:
    words_with_offsets = tokenizer.backend_tokenizer.pre_tokenizer.pre_tokenize_str(text)
    new_words = [word for word, offset in words_with_offsets]
    
    for word in new_words:
        word_freq[word] += 1

print(word_freq)

# compute base vocabulary
alphabet = set()
for word in word_freq.keys():
    for letter in word:
        alphabet.add(letter)

print(alphabet)
vocab = ["<|endoftext|>"] + alphabet.copy()