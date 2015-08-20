""" Assignment 6: PageRank. """
from collections import defaultdict
import glob
from BeautifulSoup import BeautifulSoup


class Document(object):
    def __init__(self, path, html):
        self.path = path
        self.html = html

def parse(folder, inlinks, outlinks):
    """
    Read all .html files in the specified folder. Populate the two
    dictionaries inlinks and outlinks. inlinks maps a url to its set of
    backlinks. outlinks maps a url to its set of forward links.
    """

    path = folder + "/*.html"
    allDocuments = [Document(f, BeautifulSoup(open(f))) for f in glob.glob(path)]
    
    for docID in range(0, len(allDocuments)):
        links = allDocuments[docID].html.findAll('a')
    
        for link in links:
            fullLink = link.get('href')
            fullLink = folder + "/" + fullLink
            outlinks[allDocuments[docID].path].add(str(fullLink))
            inlinks[str(fullLink)].add(allDocuments[docID].path)

    return
    pass


def compute_pagerank(urls, inlinks, outlinks, b=.85, iters=20):
    """ Return a dictionary mapping each url to its PageRank.
    The formula is R(u) = 1-b + b * (sum_{w in B_u} R(w) / (|F_w|)

    Initialize all scores to 1.0
    """

    r_u = defaultdict(lambda: 0.0)
    r_w = defaultdict(lambda: 1.0)

    for iter in range(0, iters):
        for url in urls:
            sum_ = 0.0
            for inlink in inlinks[url]:
                if len(outlinks[inlink]) is not 0:
                    sum_ += (r_w[inlink] / len(outlinks[inlink]))
            r_u[url]  = (1.0 - b) + (b * sum_)
        for url in urls:
            r_w[url] = r_u[url]

    return r_u
    pass


def run(folder, b):
    """ Do not modify this function. """
    inlinks = defaultdict(lambda: set())
    outlinks = defaultdict(lambda: set())
    parse(folder, inlinks, outlinks)
    urls = sorted(set(inlinks) | set(outlinks))
    ranks = compute_pagerank(urls, inlinks, outlinks, b=b)
    print 'Result for', folder, '\n', '\n'.join('%s\t%.3f' % (url, ranks[url]) for url in sorted(ranks))


def main():
    """ Do not modify this function. """
    run('set1', b=.5)
    run('set2', b=.85)


if __name__ == '__main__':
    main()
