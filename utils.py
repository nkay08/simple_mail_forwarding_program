from bs4 import BeautifulSoup as Soup


def soup_insert_in_html_body(html_string: str, line):
    soup = Soup(str(html_string))
    body = soup.find('body')
    new_line = soup.new_tag('p')
    new_line.string = str(line)
    body.insert(0, new_line)
    return str(soup.prettify(formatter="html5"))


def soup_insert_link_in_html_body(html_string: str, link: str, text: str = None):
    soup = Soup(str(html_string), features="html.parser")
    body = soup.find('body')
    p = soup.new_tag('p')
    body.insert(0, p)
    a = soup.new_tag('a')
    a['href'] = link
    if text:
        a.string = str(text)
    else:
        a.string = str(link)

    p.insert(0, a)
    return str(soup.prettify(formatter="html5"))