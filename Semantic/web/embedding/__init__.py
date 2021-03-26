import nltk
import os
import torch
import tensorflow as tf
from pytorch_pretrained_bert import BertTokenizer, BertModel, BertForMaskedLM


MAXIMUM_SEQUENCE_LENGTH = 512

nltk.data.path.append("./")
nltk.download('punkt')
nltk.download('stopwords')
SPLITTER = nltk.data.load('nltk:tokenizers/punkt/english.pickle')


class BiobertEmbedding(object):
    """
    Encoding from BioBERT model (BERT finetuned on PubMed articles).
    Parameters
    ----------
    model : str, default Biobert.
            pre-trained BERT model
    """

    def __init__(self, model_path):

        if model_path is not None:
            self.model_path = model_path
        else:
            raise IOError("BiobertEmbedding requires a path to pretrained model")

        self.tokens = ""
        self.sentence_tokens = ""
        self.tokenizer = BertTokenizer.from_pretrained(self.model_path)
        # Load pre-trained model (weights)
        self.model = BertModel.from_pretrained(self.model_path)
        print("Initialization Done !!")


    def process_text(self, text):

        sentences = self.split_paragraph(text)
        marked_text = "[CLS] " + " [SEP] ".join(sentences) + " [SEP]"

        # Tokenize our sentence with the BERT tokenizer.
        tokenized_text = self.tokenizer.tokenize(marked_text)
        tokens = [token for token in tokenized_text if token not in nltk.corpus.stopwords.words()]
        if len(tokens) > MAXIMUM_SEQUENCE_LENGTH:
            return None
        return tokens


    def handle_oov(self, tokenized_text, word_embeddings):
        embeddings = []
        tokens = []
        oov_len = 1
        for token,word_embedding in zip(tokenized_text, word_embeddings):
            if token.startswith('##'):
                token = token[2:]
                tokens[-1] += token
                oov_len += 1
                embeddings[-1] += word_embedding
            else:
                if oov_len > 1:
                    embeddings[-1] /= oov_len
                tokens.append(token)
                embeddings.append(word_embedding)
        return tokens,embeddings


    def eval_fwdprop_biobert(self, tokenized_text):

        # Mark each of the tokens as belonging to sentence "1".
        segments_ids = [1] * len(tokenized_text)
        # Map the token strings to their vocabulary indeces.
        indexed_tokens = self.tokenizer.convert_tokens_to_ids(tokenized_text)

        # Convert inputs to PyTorch tensors
        tokens_tensor = torch.tensor([indexed_tokens])
        segments_tensors = torch.tensor([segments_ids])

        # Put the model in "evaluation" mode, meaning feed-forward operation.
        self.model.eval()
        # Predict hidden states features for each layer
        with torch.no_grad():
            encoded_layers, _ = self.model(tokens_tensor, segments_tensors)

        return encoded_layers


    def word_vector(self, text, handle_oov=True, filter_extra_tokens=True):

        tokenized_text = self.process_text(text)
        
        if tokenized_text is None:
            return [None]

        encoded_layers = self.eval_fwdprop_biobert(tokenized_text)

        # Concatenate the tensors for all layers. We use `stack` here to
        # create a new dimension in the tensor.
        token_embeddings = torch.stack(encoded_layers, dim=0)
        token_embeddings = torch.squeeze(token_embeddings, dim=1)
        # Swap dimensions 0 and 1.
        token_embeddings = token_embeddings.permute(1,0,2)

        # Stores the token vectors, with shape [22 x 768]
        word_embeddings = []
        print("Summing last 4 layers for each token")
        # For each token in the sentence...
        for token in token_embeddings:

            # `token` is a [12 x 768] tensor
            # Sum the vectors from the last four layers.
            sum_vec = torch.sum(token[-4:], dim=0)

            # Use `sum_vec` to represent `token`.
            word_embeddings.append(sum_vec)

        self.tokens = tokenized_text
        if filter_extra_tokens:
            # filter_spec_tokens: filter [CLS], [SEP] tokens.
            word_embeddings = word_embeddings[1:-1]
            self.tokens = tokenized_text[1:-1]

        if handle_oov:
            self.tokens, word_embeddings = self.handle_oov(self.tokens,word_embeddings)
        print("Shape of Word Embeddings = %s",str(len(word_embeddings)))
        return word_embeddings


    def sentence_vector(self,text):

        print("Taking last layer embedding of each word.")
        print("Mean of all words for sentence embedding.")
        tokenized_text = self.process_text(text)
        if tokenized_text is None:
            return None

        self.sentence_tokens = tokenized_text
        encoded_layers = self.eval_fwdprop_biobert(tokenized_text)

        # `encoded_layers` has shape [12 x 1 x 22 x 768]
        # `token_vecs` is a tensor with shape [22 x 768]
        token_vecs = encoded_layers[11][0]

        # Calculate the average of all 22 token vectors.
        sentence_embedding = torch.mean(token_vecs, dim=0)
        print("Shape of Sentence Embeddings = %s",str(len(sentence_embedding)))
        return sentence_embedding
    
    
    def split_paragraph(self, paragraph):
        return SPLITTER.tokenize(paragraph)
    
    
    def get_stopwords(self):
        return nltk.corpus.stopwords.words()
