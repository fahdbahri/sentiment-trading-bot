from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline




def pipeline_method(payload):

    tokenizer = AutoTokenizer.from_pretrained('prosusAI/finbert')
    model = AutoModelForSequenceClassification.from_pretrained('prosusAI/finbert')

    classifier = pipeline('text-classification', model=model, tokenizer=tokenizer)
    results = classifier(payload)

    return results[0]


def get_sentiment_score(news_data):

    for news in news_data:


        output = pipeline_method(news)

        top_sentiment = output['label']
        sentiment_score = output['score']

        print("news title: ", news)
        print(f"Sentiment score: {sentiment_score} and Top Sentiment: {top_sentiment}")




