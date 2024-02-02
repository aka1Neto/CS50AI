import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    print(sum(list(ranks.values())))
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

    print(sum(list(ranks.values())))


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    num_pages = len(corpus.keys());
    num_links = len(corpus[page]);

    model = {};

    if num_links == 0:
        for pages in corpus:
            model[pages] = 1 / num_pages;

    else:
        for pages in corpus:
            model[pages] = (1 - damping_factor) / num_pages;

        for links in corpus[page]:
            model[links] += damping_factor / num_links;

    return model;


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    rank = {};

    page = random.choice(list(corpus.keys()));
    model = transition_model(corpus, page, damping_factor);
    rank[page] = 1;

    for _ in range(n - 1):
        page = random.choices(list(model.keys()), list(model.values()))[0];
        model = transition_model(corpus, page, damping_factor);

        if rank.get(page):
            rank[page] += 1;

        else:
            rank[page] = 1;

    return {key: value / n for key, value in rank.items()};


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    model = {};
    num_pages = len(corpus);

    for page in corpus:
        model[page] = 1 / num_pages;


    while True:
        count = 0
        for page in corpus:
            sigma = 0;

            for key, value in corpus.items():
                if not len(value):
                    sigma += model[key] * 1 / num_pages;

                elif page in value:
                    sigma += model[key] / len(value);

            sigma *= damping_factor;
            new_prob = (1 - damping_factor) / num_pages + sigma;

            if abs(model[page] - new_prob) < 0.001:
                count += 1;

            model[page] = new_prob;

        if count == num_pages:
            break;

    normalize = sum(model.values())
    return {key: (value / normalize) for key, value in model.items()};


if __name__ == "__main__":
    main()
