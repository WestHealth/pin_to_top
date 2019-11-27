"""
Pin to top plugin for Pelican
================================

Adds .pin variable to article's context and pins the article to the top
 even if it is older than the other articles
"""
from pelican import signals

def is_attr_true(obj, attribute):
    attrib = getattr(obj, attribute, 'False')
    if attrib in [False, 0]:
        return False
    try:
        if attrib.lower() in ["f", "0", "false"]:
            return False
    except AttributeError:
        return False
    return True


def update_pinned_articles(generator):
    new_order = []
    # count articles and keep the pinned ordered by date
    pinned = 0;
    for article in generator.articles:
        if is_attr_true(article, 'pin'):
            new_order.insert(pinned, article)
            pinned += 1
        else:
            new_order.append(article)
    generator.articles = new_order
    # Update the context with the new list
    generator.context['articles'] = generator.articles


def update_pinned_articles_by_category(generator):
    new_categories = []
    for category, articles in generator.categories:
        # count articles and keep the pinned ordered by date
        new_order = []
        pinned = 0;
        for article in articles:
            if is_attr_true(article, 'pin_to_category') and getattr(article, 'category') == category._name:
                new_order.insert(pinned, article)
                pinned += 1
            else:
                new_order.append(article)
        new_categories.append((category, new_order))
    generator.categories = new_categories
    # Update the context with the new list
    generator.context['categories'] = new_categories


def update_pinned_articles_by_author(generator):
    new_authors = []
    for author, articles in generator.authors:
        # count articles and keep the pinned ordered by date
        new_order = []
        pinned = 0;
        for article in articles:
            if is_attr_true(article, 'pin_to_author') and getattr(article, 'author') == author._name:
                new_order.insert(pinned, article)
                pinned += 1
            else:
                new_order.append(article)
        new_authors.append((author, new_order))
    generator.authors = new_authors
    # Update the context with the new list
    generator.context['authors'] = new_authors


def register():
    signals.article_generator_finalized.connect(update_pinned_articles)
    signals.article_generator_finalized.connect(update_pinned_articles_by_category)
    signals.article_generator_finalized.connect(update_pinned_articles_by_author)
