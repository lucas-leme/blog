import feedparser

feeds = {
    'Liberty Street Economics': 'https://feeds.feedburner.com/LibertyStreetEconomics'
}


def get_feed_info(feed_url):

    feed = feedparser.parse(feed_url)

    feed_info = {
        'title': feed.feed.title,
        'link': feed.feed.link,
        'description': feed.feed.description,
        'entries': []
    }

    for entry in feed.entries:
        feed_info['entries'].append({
            'title': entry.title,
            'link': entry.link,
            'description': entry.description,
            'published': entry.published
        })

    # sort by published date
    feed_info['entries'] = sorted(
        feed_info['entries'], key=lambda k: k['published'], reverse=True)

    return feed_info


def get_feed_data():

    feed_data = {}

    for feed_name, feed_url in feeds.items():
        feed_data[feed_name] = get_feed_info(feed_url)

    return feed_data


def get_most_recent_post(max_post_per_feed: int = 2):

    feed_data = get_feed_data()

    most_recent_posts = []

    for feed_name, feed_info in feed_data.items():

        for entry in feed_info['entries'][:max_post_per_feed]:
            most_recent_posts.append({
                'author': feed_name,
                'title': entry['title'],
                'path': entry['link'],
                'date': entry['published']
            })

    return most_recent_posts


def save_feed_data():
    """
    Save YAML like this:

    - title: "Archived Item 1"
      author: Norah Jones
      date: 2020-01-01
      path: "https://google.com"
      categories: [archived, technology]
    """
    import yaml

    most_recent_posts = get_most_recent_post()

    with open('feed/feed.yaml', 'w') as outfile:
        yaml.dump(most_recent_posts, outfile, default_flow_style=False)


if __name__ == '__main__':
    save_feed_data()
