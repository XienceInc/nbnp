import MeCab
import math, sys
import fetch_tweets

class MultinomialNB:
    def __init__(self):
        # c: Category, w: word
        self.cat_counts = {}
        self.w_counts = {}
        self.vocabulary = set()  # no particular order, so it's not list but set object

    def train(self, doc, cat):
        # doc => split to words
        words = self.__devide_into_words(doc)
        # count up the category
        self.__countup_cat(cat)
        # countup words
        for w in words:
            self.__countup_w(w, cat)

    """
    Returns the probability P(word|category)
    This calculates only word probability. By multiplying each P(word|cat),
    you get P(doc|cat).
    """
    def prob_w_given_c(self, w, cat):
        # use bayes' theorem to calculate: P(w|c) = P(w)P(c|w)/P(c)
        # word
        n = self.__word_appearance(w, cat)
        n += 1 # Laplace smoothing
        # categories
        d = sum(self.w_counts[cat].values())
        d += len(self.vocabulary) # Laplace smoothing
        return n / d

    def score_with_log(self, words, cat):
        score = self.__prior_prob(cat)
        for word in words:
            score += math.log(self.prob_w_given_c(word, cat)) # log なので掛け算が足し算になる
        return score

    def classify(self, doc):
        # 一番分類される確率が高いカテゴリーを表示する
        most_probable_cat = None
        max_score = -sys.maxsize
        
        word_list = self.__devide_into_words(doc)
        for cat in self.cat_counts.keys():
            score = self.score_with_log(word_list, cat)
            if score > max_score:
                max_score = score
                most_probable_cat =cat
        return most_probable_cat

    """
    private methods
    """
    """
    __prior_prob returns P(cat) = (sum of docs which belong to the category)/(total num of documents)
    """
    def __prior_prob(self, cat):
        return self.cat_counts[cat] / sum(self.cat_counts.values())

    def __countup_w(self, w, cat):
        self.w_counts.setdefault(cat, {})
        self.w_counts[cat].setdefault(w, 0)
        self.w_counts[cat][w] += 1
        self.vocabulary.add(w)

    def __countup_cat(self, cat):
        self.cat_counts.setdefault(cat, 0)
        self.cat_counts[cat] += 1

    def __word_appearance(self, w, cat):
        if w in self.w_counts[cat]:
            return self.w_counts[cat][w]
        return 0

    def __devide_into_words(self, doc):
        t = MeCab.Tagger()
        parsed = t.parse(doc)
        results = parsed.split('\n')
        words = []
        for elem in results:
            if elem == 'EOS':
                break
            row = elem.split(',')
            if row[6] != '*':
                words.append(row[6])
                continue
            words.append(row[0][:-3])
        return tuple(words)

if __name__ == '__main__':
    # training data
    pos_docs, nega_docs = fetch_tweets.accumulate_data()

    classifier = MultinomialNB()
    for pos_doc in pos_docs:
        classifier.train(pos_doc, "positive")
    for nega_doc in nega_docs:
        classifier.train(nega_doc, "negative")

    print('------- vocabulary ------')
    for word in classifier.vocabulary:
        print(word)
    
    # positive? negative?
    doc_to_classify = '人生の大半を部屋の中で過ごして来た。孤独には強くなったと思うけどやはり孤独は辛い。'
    print('「' + doc_to_classify + '」' + 'を分類します......')
    result_cat = classifier.classify(doc_to_classify)
    print('「' + doc_to_classify + '」' + 'は' + result_cat + 'に分類されました。')
