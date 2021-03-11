# -*- coding: UTF-8 -*-

import newspaper
import config

class ScrapedArticle:
    def __init__(self, a_url, lang="pt"):
        self.a_url = a_url        
        self.lang = lang
        self.article = self.__scrape_n_parse(a_url, lang)

    def __scrape_n_parse(self, a_url, lang):
        url_text = a_url.text()
        article = newspaper.Article(url="{}".format(url_text), language=lang)
        try:
            article.download()
            article.parse()
        except:
            self.a_url.update_status_by_id(
                        config.get_article_status("scraped_failed"),
                        id)
            article = None
        return article

    def url(self):
        return self.a_url

    def authors(self):
        if (not self.article):
            return
        return self.article.authors

    def publish_date(self):
        if (not self.article):
            return
        return self.article.publish_date

    def title(self):
        if (not self.article):
            return
        return self.article.title

    def content(self):
        if (not self.article):
            return
        return self.article.text

    def save_as_scraped(self):
        id = self.a_url.find_by_url()
        filename = config.SCRAPER_OUTPUT_DIR + "article_" + str(id) + ".txt"
        if (not self.content()):
            return False
        with open(filename, "w") as file:
            file.write(self.content())
        return True

    def __str__(self):
        return str(self.url()) + "\t" +              \
               str(self.authors()) + "\t" +          \
               str(self.publish_date()) + "\t" +     \
               str(self.title()) + "\t" +            \
               self.content().replace('\n', ' ') + "\n"