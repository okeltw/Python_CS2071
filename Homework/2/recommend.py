"""A Yelp-powered Restaurant Recommendation Program"""

from abstractions import *
#from data import ALL_RESTAURANTS, CATEGORIES, USER_FILES, load_user_file
from utils import distance, mean, zip, enumerate, sample


##################################
# Phase 2: Unsupervised Learning #
##################################


def find_closest(location, centroids):
    """Return the centroid in centroids that is closest to location. If
    multiple centroids are equally close, return the first one.

    >>> find_closest([3.0, 4.0], [[0.0, 0.0], [2.0, 3.0], [4.0, 3.0], [5.0, 5.0]])
    [2.0, 3.0]
    >>> find_closest([6, 1], [[1, 5], [3, 3]])
    [3, 3]
    >>> find_closest([1, 6], [[1, 5], [3, 3]])
    [1, 5]
    >>> find_closest([0, 0], [[-2, 0], [2, 0]])
    [-2, 0]
    >>> find_closest([0, 0], [[1000, 1000]])
    [1000, 1000]
    """
    return min(centroids, key=lambda x: distance(location, x))


def group_by_first(pairs):
    """Return a list of pairs that relates each unique key in the [key, value]
    pairs to a list of all values that appear paired with that key.

    Arguments:
    pairs -- a sequence of pairs

    >>> example = [ [1, 2], [3, 2], [2, 4], [1, 3], [3, 1], [1, 2] ]
    >>> group_by_first(example)
    [[2, 3, 2], [2, 1], [4]]
    """
    keys = []
    for key, _ in pairs:
        if key not in keys:
            keys.append(key)
    return [[y for x, y in pairs if x == key] for key in keys]


def group_by_centroid(restaurants, centroids):
    """Return a list of clusters, where each cluster contains all restaurants
    nearest to a corresponding centroid in centroids. Each item in
    restaurants should appear once in the result, along with the other
    restaurants closest to the same centroid.

    >>> r1 = make_restaurant('A', [-10, 2], [], 2, [make_review('A', 4),])
    >>> r2 = make_restaurant('B', [-9, 1], [], 3, [make_review('B', 5),make_review('B', 3.5),])
    >>> r3 = make_restaurant('C', [4, 2], [], 1, [make_review('C', 5) ])
    >>> r4 = make_restaurant('D', [-2, 6], [], 4, [make_review('D', 2)])
    >>> r5 = make_restaurant('E', [4, 2], [], 3.5, [make_review('E', 2.5), make_review('E', 3),])
    >>> c1 = [0, 0]
    >>> c2 = [3, 4]
    >>> groups = group_by_centroid([r1, r2, r3, r4, r5], [c1, c2]) # correct grouping is  [[r1, r2], [r3, r4, r5]])
    >>> [list (map (lambda r: r ['name'], c)) for c in groups]
    [['A', 'B'], ['C', 'D', 'E']]

    """

    """ Naive:
    l = []
    for r in restaurants:
        c = find_closest(r['location'], centroids)
        l += [[c,r]]

    return group_by_first(l)
    """
    return group_by_first(
        [(find_closest(restaurant_location(r), centroids), r) for r in restaurants]
    )

def find_centroid(cluster):
    """Return the centroid of the locations of the restaurants in cluster.

    >>> cluster1 = [make_restaurant('A', [-3, -4], [], 3, [make_review('A', 2)]),make_restaurant('B', [1, -1],  [], 1, [make_review('B', 1)]),make_restaurant('C', [2, -4],  [], 1, [make_review('C', 5)])]
    >>> find_centroid(cluster1) # should be a pair of decimals
    [0.0, -3.0]
    """
    # BEGIN Question 5
    return [ mean([restaurant_location(r)[0] for r in cluster]),
             mean([restaurant_location(r)[1] for r in cluster]) ]
    # END Question 5


def k_means(restaurants, k, max_updates=100):
    """Use k-means to group restaurants by location into k clusters."""
    assert len(restaurants) >= k, 'Not enough restaurants to cluster'
    old_centroids, n = [], 0
    # Select initial centroids randomly by choosing k different restaurants
    centroids = [restaurant_location(r) for r in sample(restaurants, k)]


    while old_centroids != centroids and n < max_updates:
        old_centroids = centroids
        # BEGIN Question 6
        clusters = group_by_centroid(restaurants, centroids)
        centroids = [find_centroid(cluster) for cluster in clusters]
        # END Question 6
        n += 1
    return centroids

################################
# Phase 3: Supervised Learning #
################################

def find_predictor(user, restaurants, feature_fn):
    """Return a rating predictor (a function from restaurants to ratings),
    for a user by performing least-squares linear regression using feature_fn
    on the items in restaurants. Also, return the R^2 value of this model.

    Arguments:
    user -- A user
    restaurants -- A sequence of restaurants
    feature_fn -- A function that takes a restaurant and returns a number

    >>> user = make_user('John D.', [
    ...     make_review('A', 1),
    ...     make_review('B', 5),
    ...     make_review('C', 2),
    ...     make_review('D', 2.5),])
    >>> restaurant = make_restaurant('New', [-10, 2], [], 2, [make_review('New', 4),])
    >>> cluster = [make_restaurant('B', [4, 2], [], 1, [make_review('B', 5)]),
    ...     make_restaurant('C', [-2, 6], [], 4, [make_review('C', 2)]),
    ...     make_restaurant('D', [4, 2], [], 3.5, [make_review('D', 2.5),
    ...         make_review('D', 3),]),]
    >>> pred, r_squared = find_predictor(user, cluster, restaurant_mean_rating)
    >>> round(pred(restaurant), 5)
    3.9359
    >>> round(r_squared, 5)
    0.99256
    """
    reviews_by_user = {review_restaurant_name(review): review_rating(review)
                       for review in user_reviews(user).values()}

    xs = [feature_fn(r) for r in restaurants]
    ys = [reviews_by_user[restaurant_name(r)] for r in restaurants]


    # BEGIN Question 7
    xys = zip(xs, ys)
    Sxx = sum([(x - mean(xs))**2 for x in xs])
    Syy = sum([(y - mean(ys))**2 for y in ys])
    Sxy = sum([(x - mean(xs))*(y - mean(ys)) for (x,y) in xys])
    b = Sxy/Sxx
    a = mean(ys) - b*mean(xs)
    r_squared = Sxy**2/(Sxx*Syy)
    # END Question 7

    def predictor(restaurant):
        return b * feature_fn(restaurant) + a

    return predictor, r_squared

def best_predictor(user, restaurants, feature_fns):
    """Find the feature within feature_fns that gives the highest R^2 value
    for predicting ratings by the user; return a predictor using that feature.

    Arguments:
    user -- A user
    restaurants -- A list of restaurants
    feature_fns -- A sequence of functions that each takes a restaurant

    >>> user = make_user('Cheapskate', [
    ...     make_review('A', 2),
    ...     make_review('B', 5),
    ...     make_review('C', 2),
    ...     make_review('D', 5),
    ...    ])
    >>> cluster = [
    ...    make_restaurant('A', [5, 2], [], 4, [
    ...    make_review('A', 5) ]),
    ...    make_restaurant('B', [3, 2], [], 2, [
    ...    make_review('B', 5) ]),
    ...    make_restaurant('C', [-2, 6], [], 4, [
    ...    make_review('C', 4) ]), ]
    >>> fns = [restaurant_price, restaurant_mean_rating]
    >>> pred = best_predictor(user, cluster, fns)
    >>> print([round(pred(r), 5) for r in cluster])
    [2.0, 5.0, 2.0]
    """
    reviewed = user_reviewed_restaurants(user, restaurants)
    predictors = [find_predictor(user, reviewed, fn) for fn in feature_fns]
    best_predictor = max(predictors, key=lambda predictor: predictor[1])[0]
    # BEGIN Question 8
    def predictor(restaurant):
        return best_predictor(restaurant)

    return predictor
    # END Question 8


ALL_RESTAURANTS = [make_restaurant('A', [1, 2], [], 4,
                    [make_review('A', 4), make_review('A', 4) ]),
                    make_restaurant('B', [4, 2], [], 3, [make_review('B', 5)]),
                    make_restaurant('C', [-2, 6], [], 4, [make_review('C', 2) ]),
                    make_restaurant('D', [4, 4], [], 3.5, [
                    make_review('D', 2.5), make_review('D', 3.5), ]),]

def rate_all(user, restaurants, feature_fns):
    """Return the predicted ratings of restaurants by user using the best
    predictor based a function from feature_fns.

    Arguments:
    user -- A user
    restaurants -- A list of restaurants
    feature_fns -- A sequence of feature functions

    >>> user = make_user('Mr. Mean Rating Minus One',
    ...    [make_review('A', 3),make_review('B', 4),
    ...     make_review('C', 1),])
    >>> cluster = [make_restaurant('A', [1, 2], [], 4,
    ...    [make_review('A', 4), make_review('A', 4) ]),
    ...    make_restaurant('B', [4, 2], [], 3, [make_review('B', 5)]),
    ...    make_restaurant('C', [-2, 6], [], 4, [make_review('C', 2) ]),
    ...    make_restaurant('D', [4, 4], [], 3.5, [
    ...    make_review('D', 2.5), make_review('D', 3.5), ]),]
    >>> ALL_RESTAURANTS = cluster
    >>> to_rate = cluster[2:]
    >>> fns = [restaurant_price, restaurant_mean_rating]
    >>> ratings = rate_all(user, to_rate, fns)
    >>> type(ratings)
    <class 'dict'>
    >>> len(ratings)
    2
    >>> ratings['C']
    1
    >>> round(ratings['D'], 5)
    2.0
    """
    predictor = best_predictor(user, ALL_RESTAURANTS, feature_fns)
    reviewed = user_reviewed_restaurants(user, restaurants)
    # BEGIN Question 9
    ratings = {}
    for restaurant in restaurants:
        name = restaurant_name(restaurant)
        if restaurant in reviewed:
            ratings[name] = user_rating(user, name)
        else:
            ratings[name] = predictor(restaurant)

    return ratings
    # END Question 9


def search(query, restaurants):
    """Return each restaurant in restaurants that has query as a category.

    Arguments:
    query -- A string
    restaurants -- A sequence of restaurants
    """
    # BEGIN Question 10
    "*** REPLACE THIS LINE ***"
    # END Question 10


def feature_set():
    """Return a sequence of feature functions."""
    return [restaurant_mean_rating,
            restaurant_price,
            restaurant_num_ratings,
            lambda r: restaurant_location(r)[0],
            lambda r: restaurant_location(r)[1]]
