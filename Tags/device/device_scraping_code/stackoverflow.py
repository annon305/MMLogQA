import scrapy
from scrapy import Request
import json


class Question(scrapy.Item):
    title = scrapy.Field()
    body = scrapy.Field()
    tags = scrapy.Field()
    comments = scrapy.Field()
    answers = scrapy.Field()
    selected_answer = scrapy.Field()
    images = scrapy.Field()
    link = scrapy.Field()
    score = scrapy.Field()
    creation_date = scrapy.Field()
    answer_count = scrapy.Field()


class StackOverflowSpider(scrapy.Spider):
    name = "stackoverflow"
    allowed_domains = ["stackoverflow.com"]
    error_logs = [
    "endpoint-security",
    "syslog",
    "rsyslog",
    "syslog-ng",
    "event-viewer",
    "event-log",
    "logs",
    "log-files",
    "python-logging",
    "error-logging",
    "java.util.logging",
    "audit-logging",
    "django-logging",
    "jboss-logging",
    "common.logging",
    "structured-logging",
    "microsoft-extensions-logging",
    "seq-logging",
    "boost-logging",
    "microsoft.extensions.logging",
    "exception-logging",
    "semantic-logging",
    "google-logging",
    "logging-application-block",
    "asp.net-core-logging",
    ".net-core-logging",
    "kotlin-logging",
    "easylogging++",
    "iis-advanced-logging",
    "network-error-logging",
    "trace-logging",
    "serilog.extensions.logging.file",
    "log-rotation",
    "transactionloganalysis",
    "docker-logs",
    "systemd-journald",
    "logstash",
    "logstash-grok",
    "logstash-configuration",
    "logstash-file",
    "logstash-jdbc",
    "logstash-forwarder",
    "logstash-logback-encoder",
    "logstash-filter",
    "logstash-input-jdbc",
    "logstash-json",
    "graylog",
    "graylog2",
    "graylog3",
    "splunk",
    "splunk-query",
    "splunk-dashboard",
    "splunk-formula",
    "splunk-calculation",
    "splunk-sdk",
    "splunk-api",
    "splunk-dbconnect",
    "splunk-hec",
    "fluent-plugin-splunk-hec",
    "wireshark-dissector",
    "wireshark",
    "netflow",
    "security",
    "content-security-policy",
    "wcf-security",
    "ws-security",
    "mod-security",
    "network-security",
    "windows-security",
    "mod-security2",
    "database-security",
    "data-security",
    "firewall",
    "windows-firewall",
    "firewalld",
    "windows-firewall-api",
    "firewall-access",
    "firewall-rules",
    "iptables",
    "snort",
    "suricata",
    "antivirus"
]



    max_posts_per_tag = None

    def start_requests(self):
        """
        Generate start URLs for each tag.
        """
        for tag in self.error_logs:
            url = f"https://stackoverflow.com/questions/tagged/{tag}"  
            yield Request(url, callback=self.parse_tag_page, meta={"tag": tag})

    def parse_tag_page(self, response):
        """
        Parse the tag page to extract question links.
        """
        tag = response.meta["tag"]

        question_links = response.css("a.s-link::attr(href)").getall()
        for link in question_links:
            if link.startswith("/questions/"):
                full_link = response.urljoin(link)
                yield Request(full_link, callback=self.parse_question, meta={"tag": tag})

        # Follow pagination if available
        next_page = response.css("a[rel='next']::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_tag_page, meta={"tag": tag})

    def parse_question(self, response):
        """
        Parse an individual question page to extract details.
        """
        item = Question()

        item["title"] = response.css("a.question-hyperlink::text").get()
        item["body"] = response.css("div.s-prose.js-post-body").xpath("string()").get()
        item["tags"] = response.css("a.post-tag::text").getall()
        item["link"] = response.url
        item["score"] = response.css("div.js-vote-count::text").get()
        item["creation_date"] = response.css("time::attr(datetime)").get()
        item["answer_count"] = response.css("span[itemprop='answerCount']::text").get()

        item["comments"] = response.css("li.comment span.comment-copy::text").getall()

        item["answers"] = []
        for answer in response.css("div.answer"):
            answer_body = answer.css("div.s-prose").xpath("string()").get()
            answer_score = answer.css("div.js-vote-count::text").get()
            item["answers"].append({"body": answer_body, "score": answer_score})

        accepted_answer = response.css("div.accepted-answer div.s-prose").xpath("string()").get()
        item["selected_answer"] = accepted_answer

        item["images"] = response.css("div.s-prose img::attr(src)").getall()

        yield item


