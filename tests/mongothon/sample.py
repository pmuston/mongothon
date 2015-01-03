"""Provides a valid sample set of schemas and documents adhereing to those
schemas for use in testing."""

from mongothon import Schema, Mixed, Array
from mongothon.validators import one_of
from datetime import datetime
from bson.objectid import ObjectId


def stubnow():
    return datetime(2012, 4, 5)

name_schema = Schema({
    "first":    {"type": str, "required": True},
    "last":     {"type": str, "required": True}
})

# TEST SCHEMAS
comment_schema = Schema({
    "commenter":    {"type": name_schema, "required": True},
    "email":        {"type": str, "required": False},
    "comment":      {"type": str, "required": True},
    "votes":        {"type": int, "default": 0}
})

blog_post_schema = Schema({
    "author":           {"type": name_schema, "required": True},
    "content":          {"type": Schema({
        "title":            {"type": str, "required": True},
        "text":             {"type": str, "required": True},
        "page_views":       {"type": int, "default": 1}
    }), "required": True},
    "category":         {"type": str, "validates":one_of("cooking", "politics")},
    "comments":         {"type": Array(comment_schema)},
    "likes":            {"type": int, "default": 0},
    "creation_date":    {"type": datetime, "default": stubnow},
    "tags":             {"type": Array(str)},
    "misc":             {"type": Mixed(str, int)},
    "linked_id":        {"type": Mixed(int, str)},
    "publication_id":   {"type": ObjectId}
})


def valid_doc(overrides=None):
    doc = {
        "author": {
            "first":    "John",
            "last":     "Humphreys"
        },
        "content": {
            "title": "How to make cookies",
            "text": "First start by pre-heating the oven..."
        },
        "category": "cooking",
        "comments": [
            {
                "commenter": {
                    "first": "Julio",
                    "last": "Cesar"
                },
                "email": "jcesar@test.com",
                "comment": "Great post dude!"
            },
            {
                "commenter": {
                    "first": "Michael",
                    "last": "Andrews"
                },
                "comment": "My wife loves these."
            }
        ],
        "tags": ["cookies", "recipe", "yum"]
    }
    if overrides:
        doc.update(overrides)
    return doc


# The expected version of the document once it has been saved to the DB,
# including the use of Unicode and applied defaults.
def expected_db_doc(object_id):
    return {
        "_id": object_id,
        "author": {
            "first":    "John",
            "last":     "Humphreys"
        },
        "content": {
            "title": "How to make cookies",
            "text": "First start by pre-heating the oven...",
            "page_views": 1
        },
        "category": "cooking",
        "comments": [
            {
                "commenter": {
                    "first": "Julio",
                    "last": "Cesar"
                },
                "email": "jcesar@test.com",
                "comment": "Great post dude!",
                "votes": 0
            },
            {
                "commenter": {
                    "first": "Michael",
                    "last": "Andrews"
                },
                "comment": "My wife loves these.",
                "votes": 0
            }
        ],
        "likes": 0,
        "tags": ["cookies", "recipe", "yum"],
        "creation_date": stubnow()
    }
