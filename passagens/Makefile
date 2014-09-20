# Makefile - passagens spider

.PHONY: spider deploy

spider:
	scrapy crawl tam -o passagens.json -t json -s JOBDIR=jobdir

deploy:
	@python deploy.py
