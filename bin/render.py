#!/usr/bin/env python3

# TBD: much of this code is now bolierplate which could be a package

import jinja2
from frontmatter import Frontmatter
from markdown import markdown

def govuk_markdown(text):
    text = markdown(text)
    text = text.replace("<h1>", """<h1 class="govuk-heading-xl">""")
    text = text.replace("<h2>", """<h2 class="govuk-heading-l">""")
    text = text.replace("<h3>", """<h2 class="govuk-heading-m">""")
    text = text.replace("<p>", """<p class="govuk-body">""")
    return text

multi_loader = jinja2.ChoiceLoader([
    jinja2.FileSystemLoader(searchpath="./templates"),
    jinja2.PrefixLoader({
        'govuk-jinja-components': jinja2.PackageLoader('govuk_jinja_components')
    })
])

env = jinja2.Environment(loader=multi_loader)

title = "Finding the local authority for an address"
post = Frontmatter.read_file("content/guidance.md")
title = post["attributes"]["title"]
content = govuk_markdown(post["body"])

with open("docs/index.html", "w") as f:
    f.write(env.get_template("guidance.html").render(title=title, content=content))
