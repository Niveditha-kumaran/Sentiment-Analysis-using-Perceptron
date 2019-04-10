# Sentiment-Analysis-using-Perceptron

Dataset Requirements: Download dataset from Deceptive Opinion Spam Corpus v1.4

Run the code as: 
python perceplearn.py "link to dataset directory"

Required probabilities will be stored in 2 text files, averagemodel.txt and vanillamodel.txt containing probabilities obtained by averaged perceptron and vanilla perceptron.

Now run :
python percepclassify.py "link to text file that contains text to classify, with each sentence in one line" "link to txt file, i.e avergaemodel.txt or vanillamodel.txt"

The classified output will be stored in a text file called output.txt
