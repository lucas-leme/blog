import logging
from datetime import datetime

import dateutil.parser
import feedparser
import yaml

feeds = {
    "CFA - Enterprising Investor": {
        "url": "https://blogs.cfainstitute.org/investor/feed/",
        "categories": ["CFA"],
        "n_posts_to_show": 2
    },
    "Klement on Investing": {
        "url": "https://klementoninvesting.substack.com/feed",
        "categories": ["Macro", "Newsletters"],
        "image": ""
    },
    "CFA - Financial Analysts Journal": {
        "url": "https://rpc.cfainstitute.org/en/ICE-Feeds/RPC-Publications-Feed",
        "categories": ["CFA"],
        "n_posts_to_show": 2
    },
    'Liberty Street Economics': {
        "url": 'https://feeds.feedburner.com/LibertyStreetEconomics',
        "categories": ["Macro", "FED", "BC"],
        "image": "https://d3g9pb5nvr3u7.cloudfront.net/sites/59dd2d9d016a1b2d929cd15b/-1445257209/256.jpg",
        "n_posts_to_show": 1
    },
    'Atas do Copom': {
        "url": 'https://www.bcb.gov.br/api/feed/sitebcb/sitefeeds/atascopom',
        "categories": ["Bacen", "BC"],
        "image": "https://classic.exame.com/wp-content/uploads/2022/02/copom-divulgacao.jpg?quality=70&strip=info&w=700",
        "force_author": True,
        "n_posts_to_show": 1
    },
    'Comunicados Copom': {
        "url": 'https://www.bcb.gov.br/api/feed/sitebcb/sitefeeds/comunicadoscopom',
        "categories": ["Bacen", "BC"],
        "image": "https://cdn.oantagonista.com/cdn-cgi/image/fit=contain,width=960,format=auto/uploads/2023/08/53089476259_00fff6225f_o-scaled.jpg",
        "force_author": True,
        "n_posts_to_show": 1
    },
    'Relatório de Inflação': {
        "url": 'https://www.bcb.gov.br/api/feed/sitebcb/sitefeeds/ri',
        "categories": ["Bacen", "BC"],
        "image": "https://img.band.uol.com.br/image/2023/06/12/boletim-do-banco-central-aponta-melhora-da-inflacao-e-do-crescimento-neste-ano-14366_800x450.webp",
        "force_author": True,
        "n_posts_to_show": 1
    },
    'Bacen: Relatório Focus': {
        "url": 'https://www.bcb.gov.br/api/feed/sitebcb/sitefeeds/focus',
        "categories": ["Bacen", "BC"],
        "image": "https://s2-oglobo.glbimg.com/4Ugd1L8ibkhIE19fug0Uch8n_yI=/0x0:2000x1323/888x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_da025474c0c44edd99332dddb09cabe8/internal_photos/bs/2023/j/l/yuWhBvTH6CFIvGXG3PrA/sede-do-banco-central-do-brasil-em-brasilia.jpg",
        "n_posts_to_show": 1
    },
    'Market Makers': {
        "url": 'https://spotifeed.timdorr.com/2MCrAB0JUTfHxP333dGJm7',
        "categories": ["Podcasts"],
        "image": ""
    },
    'The Journal': {
        "url": 'https://spotifeed.timdorr.com/0KxdEdeY2Wb3zr28dMlQva',
        "categories": ["Podcasts"],
        "image": ""
    },
    'Outliers': {
        "url": 'https://spotifeed.timdorr.com/7vSK0uhbMcfLwOQMIlKLJE',
        "categories": ["Podcasts"],
        "image": ""
    },
    'The View From Apollo': {
        "url": 'https://spotifeed.timdorr.com/7a2pM9MgehqQHEHQ6FCZLu',
        "categories": ["Podcasts"],
        "image": "",
        "n_posts_to_show": 1
    },
    'Money Talks': {
        "url": 'https://spotifeed.timdorr.com/2Yvo8QxZf7WlSEsIwKjtX4',
        "categories": ["Podcasts"],
        "image": "",
        "n_posts_to_show": 1
    },
    'Flirting with Models': {
        "url": 'https://spotifeed.timdorr.com/1IXldCXztfTaZeHbtcDRQI',
        "categories": ["Podcasts", "Quant"],
        "image": "",
        "n_posts_to_show": 1
    },
    'The Morgan Housel': {
        "url": 'https://spotifeed.timdorr.com/2l01lGyIh9xodneIV37dD3',
        "categories": ["Podcasts"],
        "image": "",
        "n_posts_to_show": 1
    },
    "Brazil Journal - Economia": {
        "url": "https://braziljournal.com/categoria/economia/feed/",
        "categories": ["Economia"],
        "image": "https://braziljournal.com/wp-content/uploads/2022/06/cropped-favicon-512-512.png",
        "n_posts_to_show": 2,
    },
    "Invest News - Economia": {
        "url": "https://investnews.com.br/economia/feed/",
        "categories": ["Notícias"],
        "n_posts_to_show": 2,
        "image": "https://yt3.googleusercontent.com/zlZlh06n3N8spGemaUPexPUk14S-DIkKTyzNVWSHCWzJoKrV354iGYDKYr-gTlStZbosSGoO-w=s160-c-k-c0x00ffffff-no-rj"
    },
    "Invest News - Finanças": {
      "url": "https://investnews.com.br/financas/feed/",
        "categories": ["Notícias"],
        "n_posts_to_show": 2,
        "image": "https://yt3.googleusercontent.com/zlZlh06n3N8spGemaUPexPUk14S-DIkKTyzNVWSHCWzJoKrV354iGYDKYr-gTlStZbosSGoO-w=s160-c-k-c0x00ffffff-no-rj"
    },
    "AQR": {
        "url": "https://fetchrss.com/rss/653e6c6f01a45c2863204a32653e6c4c2b91d54e8654b9c2.xml",
        "categories": ["Quant", "Papers"],
        "image": "https://www.aqr.com/-/media/AQR/Images/AQR-Site/Homepage/aqr-logo-blue-twitter.png",
        "force_author": True
    },
    "Stay at Home Macro": {
        "url": "https://stayathomemacro.substack.com/feed",
        "categories": ["Macro", "Newsletters"],
        "image": ""
    },
    "The Overshoot": {
        "url": "https://theovershoot.co/feed",
        "categories": ["Macro", "Newsletters"],
        "image": ""
    },
    "Apricitas Economics": {
        "url": "https://www.apricitas.io/feed",
        "categories": ["Macro", "Newsletters"],
        "image": ""
    },
    "Arjan Codes": {
        "url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCVhQ2NnY5Rskt6UjCUkJ_DA",
        "categories": ["Tech", "Code", "Youtube"],
        "image": ""
    },
    "MKBHD": {
        "url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCBJycsmduvYEL83R_U4JriQ",
        "categories": ["Tech", "Youtube"],
        "image": ""
    },
    "CFA Reddit": {
        "url": "https://www.reddit.com/r/CFA/.rss",
        "categories": ["Notícias", "CFA", "Reddit"],
        "n_posts_to_show": 2,
        "image": "https://styles.redditmedia.com/t5_2rzsx/styles/communityIcon_ngaqh14tqfj31.jpg?format=pjpg&s=995c4d459025f197881ae26dc8ccf30176a8488c"
    }
}


def get_feed_info(feed_url):

    feed = feedparser.parse(feed_url)
    try:
        feed_info = {
            'title': feed.feed.title,
            'link': feed.feed.link,
            'description': feed.feed.description if hasattr(feed.feed, 'description') else None,
            'entries': []
        }
    except:
        return None

    for entry in feed.entries:

        has_image = False
        if hasattr(entry, 'links'):
            for link in entry.links:
                if link['type'].startswith('image'):
                    image = link['href']
                    has_image = True
                    break

        if hasattr(entry, 'media_thumbnail'):
            image = entry.media_thumbnail[0]['url']
            has_image = True

        if not has_image:
            # try get imagem from site thumbnail
            # try:
            #     request_result = requests.get(entry.link)
            #     soup = BeautifulSoup(request_result.content, 'html.parser')
            #     image = soup.find('meta', property='og:image')['content']
            # except:
            #     image = entry.image.href if hasattr(entry, 'image') else None
            image = entry.image.href if hasattr(entry, 'image') else None

        feed_info['entries'].append({
            'title': entry.title,
            'link': entry.link,
            'description': entry.description,
            'summary': entry.summary,
            'published': entry.published if hasattr(entry, 'published') else None,
            'image': image,
        })

    return feed_info


def get_feed_data():

    feed_data = {}

    for feed_name, feed_info in feeds.items():
        feed_url = feed_info['url']

        feed_data_i = get_feed_info(feed_url)

        if feed_data_i is None:
            continue

        if feed_info.get('force_author', False):
            author = feed_name
        else:
            author = feed_data_i['title']

        feed_data_i['categories'] = feed_info.get('categories', [])
        feed_data_i['default_image'] = feed_info.get("image")
        feed_data_i['n_posts_to_show'] = feed_info.get('n_posts_to_show', 2)

        feed_data[author] = feed_data_i

    return feed_data


def _convert_date_to_isoformat(date: str):
    if date is not None:
        date: datetime = dateutil.parser.parse(date) 
        return date.isoformat()
    else:
        return datetime.now().isoformat()


def get_most_recent_post():

    logging.info('Starting to get most recent post')

    feed_data = get_feed_data()

    logging.info('Finished getting feed data')

    most_recent_posts = []

    logging.info('Starting to get most recent posts')

    for feed_name, feed_info in feed_data.items():

        n_posts_to_show = feed_info['n_posts_to_show']

        for entry in feed_info['entries'][:n_posts_to_show]:

            # get image from summary
            try:
                image = entry['summary'].split('<img src="')[1].split('"')[0]
            except:
                image = entry.get('image') \
                    if entry.get('image') is not None \
                    else feed_info.get('default_image')

            # get date from summary
            try:
                date = _convert_date_to_isoformat(entry['summary'].split(
                    '<p class="article__date text--small">')[1].split('<')[0].strip())
            except:
                date = _convert_date_to_isoformat(entry.get('published'))

            most_recent_posts.append({
                'author': feed_name,
                'title': entry['title'],
                'path': entry['link'],
                'date': date,
                'image': image,
                'description': entry.get('summary', None),
                'categories': feed_info.get("categories")
            })

    most_recent_posts = list(
        {v['path']: v for v in most_recent_posts}.values())

    most_recent_posts = sorted(
        most_recent_posts, key=lambda k: k['date'], reverse=True)

    return most_recent_posts


def save_feed_data():
    logging.info('Starting to save feed data')

    most_recent_posts = get_most_recent_post()

    news_posts = [
        post for post in most_recent_posts if 'Notícias' in post['categories']]
    other_posts = [
        post for post in most_recent_posts if 'Notícias' not in post['categories']]

    logging.info('Finished getting most recent posts')

    logging.info('Starting to save feed data')

    with open('feed/news.yaml', 'w') as outfile:
        yaml.dump(news_posts, outfile, default_flow_style=False)

    with open('feed/feed.yaml', 'w') as outfile:
        yaml.dump(other_posts, outfile, default_flow_style=False)

    logging.info('Finished saving feed data')


if __name__ == '__main__':
    save_feed_data()
