class LinkMapper(object):
    def to_response(self, link_list):
        link_list = self._format_link_list(link_list)
        return link_list

    def _format_link(self, link):
        title = link.get("title", link["path"])
        url = link["path"]
        rel = link.get("type")
        return self._build_link(url, rel, title)

    def _build_link(self, path, rel, title):
        return "<{0}>; rel={1}; title={2}".format(path, rel, title)

    def _format_link_list(self, link_list):
        new_link_list = []
        for link in link_list:
            new_link_list.append(self._format_link(link))

        return new_link_list
