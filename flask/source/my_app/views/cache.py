import time
from flask import Blueprint

from my_app import cache

bp_cache = Blueprint(name="cache", import_name=__name__, url_prefix="/cache/", template_folder="templates/")

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

@cache.memoize()
def cached_fibonacci(n):
    if n <= 1:
        return n
    return cached_fibonacci(n-1) + cached_fibonacci(n-2)

@bp_cache.route(rule="/", methods=["GET"])
def main():
    start_time = time.time()
    cached_fibonacci(35)
    end_time = time.time()
    time_taken_with_cache = end_time - start_time

    start_time = time.time()
    fibonacci(35)
    end_time = time.time()
    time_taken_without_cache = end_time - start_time

    return f"캐시 미적용: {time_taken_without_cache} 초<br>캐시 적용: {time_taken_with_cache} 초"