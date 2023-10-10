"""
CMSC 14100
Winter 2023
Homework #6

A note about types for docstrings:

  You can use tweet_dict as the type of a tweet in the original format
  in your docstrings.

  You can use simple_tweet_dict as the type of tweet in the format
  returned by process_tweets.

  For tweets-by-user dictionaries, use dict(str, list[simple_tweet_dict]).

  For the results of the last 4 tasks: use dict(str, list(tuple(str)))

We will be using anonymous grading, so please do NOT include your name
in this file

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.

[RESUBMISSIONS ONLY: Explain how you addressed the grader's comments
 for your original submission.  If you did not submit a solution for the
 initial deadline, please state that this submission is new.]
"""

# import the provided function that sorts (key, value) pairs
from util import sort_count_pairs

# Exercise 1
def count_tweets_by_user(orig_tweets):
    """
    Count the number of tweets for each user in the list
    of original tweets.

    Inputs:
        orig_tweets [list[tweet_dict]]: a list of tweets in
            the original format

    Returns [dict(str, int)]: a dictonary that maps user screen
        names to integer counts.
    """
    user_dict = {}
    for tweet in orig_tweets:
        name = tweet['user']['screen_name']
        if name in user_dict:
            user_dict[name] += 1
        if name not in user_dict:
            user_dict[name] = 1
    return user_dict


# Exercise 2
def extract_entities(orig_tweet, key, subkey):
    """
    Generates a list of entities of interest according to the tweet, key
    and subkey.

    Input:
        orig_tweet [dict(str, dict)]: the tweet of interest
        key [str]: entity key of interest
        subkey [str]: entity subkey of interest
    
    Returns [list[str]]: a list of the entities of interest
    """
    entity_list = []
    entity_key = orig_tweet['entities'][key]
    for sublist in entity_key:
        entity_list.append(sublist[subkey])
    return entity_list


# Exercise 3
def process_tweets(orig_tweets, entity_descriptions):
    """
    Generates a list of simple tweets with the user, text, and various
    entities as directed.

    Inputs:
        orig_tweets [list[tweet_dict]]: a list of tweets in
            the original format
        entity_descriptions [list[tuple(str,str)]]: specific key and subkey
            information needed in the proceeded tweet
    
    Returns [list[dict(str, str)]]: list of processed tweets according to
        the input entity descriptions
    """
    processed_tweets = []
    processed_tweet = {}
    for tweet in orig_tweets:
        processed_tweet['user'] = tweet['user']['screen_name']
        processed_tweet['clean_text'] = tweet['clean_text']
        for entity in entity_descriptions:
            key, subkey = entity
            processed_tweet[key] = extract_entities(tweet, key, subkey)
        processed_tweets.append(processed_tweet)
        processed_tweet = {}
    return processed_tweets


# Exercise 4
def organize_tweets_by_user(simple_tweets):
    """
    Constructs a dictionary that maps a user's screen name to a list of their
    simple tweets from a list of simple tweets.

    Inputs:
        simple_tweets [list[dict(str, str)]]: list of processed tweets 
            according to the input entity descriptions

     Returns dict(str, list[dict(str, str)]): dictionary mapping a user's
        screen name to a list of their simple tweets.
    """
    tweets_by_user = {}
    for tweet in simple_tweets:
        name = tweet['user']
        if name not in tweets_by_user:
            tweets_by_user[name] = [tweet]
        elif name in tweets_by_user:
            tweets_by_user[name] += [tweet]
    return tweets_by_user
        


# Exercise 5 and 6: helper
def get_entity_counts(tweets, entity_key):
    """
    Constructs a dictionary mapping values associated with an entity key
    to the number of times it occurs.

    Inputs:
        tweets [list[dict(str, str)]]: list of processed tweets with 
            all input entities and their values
        entity_key [str]: key of interest
    
    Returns [list[tuple(str, int)]]: list of tuples with entity key values and 
        the number of times they occurred
    """
    
    key_to_val = {}
    ready_to_sort = []
    for tweet in tweets:
        keys = tweet[entity_key]
        for key in keys:
            key = key.lower()
            if key not in key_to_val:
                key_to_val[key] = 1
            elif key in key_to_val:
                key_to_val[key] += 1
    for value in key_to_val.items():
        ready_to_sort.append(value)
    return ready_to_sort



# Exercise 5
def find_top_k_entities(tweets_by_user, entity_key, k):
    """
    Generates a dictionary that maps a users screen name to a list k most 
    frequently occurring values for that entity

    Inputs:
        tweets_by_user [list[dict(str, str)]]: list of processed tweets with 
            all input entities and their values sorted by user
        entity_key [str]: key of interest
        k [int]: number of values of interest
    
    Returns [dict(str,list[str])]: a dictionary that maps a user's screen name
        to entity key values in order of occurence
    """
    import util
    top_k_entities = {}
    for name in tweets_by_user:
        ordered = []
        user_tweets = tweets_by_user[name]
        sort_this = get_entity_counts(user_tweets, entity_key)
        lst = util.sort_count_pairs(sort_this)
        for val in lst:
            if len(ordered) < k:
                ordered.append(val[0])
        top_k_entities[name] = ordered
        ordered = []
    return top_k_entities


# Exercise 6
def find_min_count_entities(tweets_by_user, entity_key, min_count):
    """
    Generates a dictionary that maps a user's screen name to a list of
    entities that occurred more than a certain number of times.

    Inputs:
        tweets_by_user [list[dict(str, str)]]: list of processed tweets with 
            all input entities and their values sorted by user
        entity_key [str]: key of interest
        min_count [int]: min number of times an entity needs to occur

    Returns [dict(str, list[str])]: dictionary with a user's name and all the
        entities that occurred more than a certain number of times
    """
    import util
    min_count_entities = {}
    for name in tweets_by_user:
        enough = []
        user_tweets = tweets_by_user[name]
        sort_this = get_entity_counts(user_tweets, entity_key)
        lst = util.sort_count_pairs(sort_this)
        for val in lst:
            if val[1] >= min_count:
                enough.append(val[0])
        min_count_entities[name] = enough
        enough = []
    return min_count_entities
    


# Helper function for Exercises 7 and 8
def count_all_ngrams_for_user(tweets, n):
    """
    Generates a dictionary matching ngrams to the number of times that ngram
    occurs within a set of tweets

    Inputs:
        tweets [list[dict(str, str)]]: list of processed tweets with 
            all input entities and their values
        n [int]: size of the string tuples
    
    Returns [dict(tuple(str,str), int)]: dictionary that matches how many times
        a certain tuple has occurred
    """
    import util
    ngrams_ready = [] 
    ngram_count = {}
    sorted_grams = []
    for tweet in tweets:
        to_be_split = tweet['clean_text']
        split = to_be_split.split()
        count = n
        for idx, _ in enumerate(split):
            words = split[idx:count]
            if len(words) == n:
                tuple_word = tuple(words)
                ngrams_ready.append(tuple_word)
            count += 1
        for item in ngrams_ready:
            if item not in ngram_count:
                ngram_count[item] = 1
            elif item in ngram_count:
                ngram_count[item] += 1
        ngrams_ready = []
    for value in ngram_count.items():
        sorted_grams.append(value)
    sorted_tuples = util.sort_count_pairs(sorted_grams)
    return sorted_tuples
                       
    


def find_top_k_ngrams(tweets_by_user, n, k):
    """
    Generates a dictionary that maps a user's screen name to a list of the most 
    frequently occurring ngrams (of the specified size) from the tweets 
    for that user.

    Inputs:
        tweets_by_user [list[dict(str, str)]]: list of processed tweets with 
            all input entities and their values sorted by user
        n [int]: size of the string tuples
        k [int]: number of most frequent strings listed

    Returns [dict(str,list[str])]: a dictionary mapping a screen name to a list
        of most frequent ngrams
    """
    
    top_ngrams = {}
    for name in tweets_by_user:
        ngram_lst = []
        user_tweets = tweets_by_user[name]
        var = count_all_ngrams_for_user(user_tweets, n)
        for val in var:
            if len(ngram_lst) < k:
                ngram_lst.append(val[0])
        top_ngrams[name] = ngram_lst
        ngram_lst = []
    return top_ngrams



def find_min_count_ngrams(tweets_by_user, n, min_count):
    """
    Generates a dictionary that maps a screen name to a list of ngrams that
    occurred at least a specified number of times.

    Inputs:
        tweets_by_user [list[dict(str, str)]]: list of processed tweets with 
            all input entities and their values sorted by user
        n [int]: size of the string tuples
        min_count [int]: minimum number of times an ngram appears

    Returns [dict(str, list[str])]: a dictionary mapping a user's screen name
        to all the ngram phrases that occurred a minimum number of times
    """
    
    min_count_ngrams = {}
    for name in tweets_by_user:
        enough = []
        user_tweets = tweets_by_user[name]
        var = count_all_ngrams_for_user(user_tweets, n)
        for val in var:
            if val[1] >= min_count:
                enough.append(val[0]) 
        min_count_ngrams[name] = enough
        enough = []
    return min_count_ngrams

