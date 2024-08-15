Over the years there have been various algorithms to represent the text data into mathematical form from word level tokenization to character level tokenization. One such interesting algorithm is byte pair encoding which enables sub word tokenization. 

This is helpful because it allows the model to handle the words that it has not seen before by breaking them into familiar pieces. 

Instead of treating each words as a whole, it breaks sown the word into smaller parts. for example the word unhappiness might be split into “un", “happiness"

The model can understand the meaning of unknown word by combining the meanings of the subwords.