from youtube_transcript_api import YouTubeTranscriptApi
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import networkx as nx

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

def build_similarity_matrix(sentences, stopwords):
    # Create an empty similarity matrix
    similarity_matrix = nx.Graph()
    
    # Add nodes to the graph (each node represents a sentence)
    similarity_matrix.add_nodes_from(range(len(sentences)))
    
    # Compute similarity between sentences and add edges to the graph
    for i in range(len(sentences)):
        for j in range(i+1, len(sentences)):
            similarity = sentence_similarity(sentences[i], sentences[j], stopwords)
            similarity_matrix.add_edge(i, j, weight=similarity)
    
    return similarity_matrix

def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = set(stopwords.words('english'))
        
    # Tokenize sentences
    words1 = [w.lower() for w in sent1 if w.isalnum() and w.lower() not in stopwords]
    words2 = [w.lower() for w in sent2 if w.isalnum() and w.lower() not in stopwords]
    
    # Compute Jaccard similarity between sets of words
    jaccard_sim = len(set(words1).intersection(set(words2))) / len(set(words1).union(set(words2)))
    
    return jaccard_sim

def extract_important_points(sentences, top_n=5):
    stop_words = set(stopwords.words('english'))
    
    # Build similarity matrix
    similarity_matrix = build_similarity_matrix(sentences, stop_words)
    
    # Compute PageRank scores for sentences
    scores = nx.pagerank(similarity_matrix)
    
    # Sort sentences by their PageRank scores
    ranked_sentences = sorted(scores, key=scores.get, reverse=True)
    
    # Extract top-ranked sentences
    important_points = [sentences[idx] for idx in ranked_sentences[:top_n]]
    
    return important_points


def summarize_transcript(url):
    try:
        video_id = url.split("=")[1]  # Extract video ID from YouTube URL
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = ' '.join([t['text'] for t in transcript])
        sentences = sent_tokenize(transcript_text)

        # Extract important points
        important_points = extract_important_points(sentences)
        summarized_text = '. '.join(important_points)

        return summarized_text

    except Exception as e:
        print("Error occurred during transcript summarization:", e)  # Log or return the error
        return "Error occurred during transcript summarization."
