import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from django.db.models import Q, Count, Avg
from main_app.models import Author, Article


# Create queries within functions


def get_authors(search_name=None, search_email=None):
    result = []

    if search_name is None and search_email is None:
        return ""

    query_name = Q(full_name__icontains=search_name)
    query_email = Q(email__icontains=search_email)

    if search_name is not None and search_email is not None:
        query = Q(query_name & query_email)
    elif search_name is not None:
        query = query_name
    else:
        query = query_email

    authors = Author.objects.filter(query).order_by('-full_name')

    if not authors.exists():
        return ''

    for a in authors:
        status = 'Banned' if a.is_banned is True else 'Not Banned'
        result.append(f"Author: {a.full_name}, email: {a.email}, status: {status}")

    return '\n'.join(result)


def get_top_publisher():
    top_publisher = Author.objects.get_authors_by_article_count().first()

    if top_publisher is None or top_publisher.article_count == 0:
        return ''

    return f'Top Author: {top_publisher.full_name} with {top_publisher.article_count} published articles.'


def get_top_reviewer():
    top_reviewer = Author.objects.annotate(reviews_count=Count('author_review')).order_by('-reviews_count', 'email').first()

    if top_reviewer is None or top_reviewer.reviews_count == 0:
        return ''

    return f"Top Reviewer: {top_reviewer.full_name} with {top_reviewer.reviews_count} published reviews."


def get_latest_article():
    last_article = Article.objects.prefetch_related(
        'author_review', 'article_review'
    ).order_by('-published_on').first()

    if last_article is None:
        return ""

    authors_names = ', '.join(a.full_name for a in last_article.authors.all().order_by('full_name'))
    reviews_count = last_article.reviews.count()
    avg_rating = sum([r.rating for r in last_article.reviews.all()]) / reviews_count if reviews_count else 0.0

    return (f"The latest article is: {last_article.title}. "
            f"Authors: {authors_names}. "
            f"Reviewed: {reviews_count} times. "
            f"Average Rating: {avg_rating:.2f}.")


def get_top_rated_article():
    top_article = Article.objects.annotate(
        avg_rating=Avg('article_review__rating')
    ).order_by('avg_rating', 'title').first()

    num_reviews = top_article.reviews.count() if top_article else 0

    if top_article is None or num_reviews == 0:
        return ''

    avg_rating = top_article.avg_rating or 0.0

    return f"The top-rated article is: {top_article.title}, with an average rating of {avg_rating}, reviewed {num_reviews} times."


