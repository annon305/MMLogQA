import scrapy
from scrapy import Request
import json
import os


class Question(scrapy.Item):
    title = scrapy.Field()
    body = scrapy.Field()
    tags = scrapy.Field()
    related_tags = scrapy.Field()
    comments = scrapy.Field()
    answers = scrapy.Field()
    selected_answer = scrapy.Field()
    images = scrapy.Field()
    link = scrapy.Field()
    score = scrapy.Field()
    creation_date = scrapy.Field()
    answer_count = scrapy.Field()


class StackOverflowSpider(scrapy.Spider):
    name = "stackoverflow_spider"
    allowed_domains = ["stackoverflow.com"]

    error_logs = [
    "aws-appstream",
    "google-cloud-workstations",
    "azure-app-service",
    "google-app-engine",
    "azure-spring-cloud",
    "google-app-engine",
    "aws-opsworks",
    "azure-devops",
    "google-cloud-build",
    "aws-codebuild",
    "azure-pipelines",
    "google-cloud-build",
    "google-cloud-deploy",
    "aws-codecommit",
    "azure-repos",
    "google-source-repositories",
    "aws-codepipeline",
    "azure-pipelines",
    "google-cloud-build",
    "aws-codestar",
    "aws-xray",
    "azure-application-insights",
    "google-cloud-trace",
    "aws-cloud9",
    "azure-cloud-shell",
    "google-cloud-shell",
    "aws-batch",
    "azure-batch",
    "aws-efs",
    "azure-files",
    "google-cloud-filestore",
    "google-cloud-filestore",
    "azure-active-directory",
    "google-cloud-identity",
    "aws-cognito",
    "azure-ad-b2c",
    "aws-iam",
    "google-cloud-iam",
    "google-cloud-kms",
    "aws-secrets-manager",
    "google-secret-manager",
    "aws-certificate-manager",
    "aws-waf",
    "azure-application-insights",
    "google-cloud-armor",
    "google-cloud-armor",
    "azure-sentinel",
    "aws-security-hub",
    "azure-security-center",
    "aws-config",
    "azure-policy",
    "google-cloud-asset-inventory",
    "google-cloud-console",
    "amazon-cloudwatchlogs",
    "aws-cloudwatch-log-insights",
    "aws-cloudformation"
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


