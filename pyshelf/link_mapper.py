import re


class LinkMapper(object):
    def __init__(self, artifact_path_builder):
        """
            Args:
                artifact_path_builder(pyshelf.artifact_path_builder.ArtifactPathBuilder)
        """
        self.builder = artifact_path_builder

    def to_response(self, link_list):
        link_list = self._remove_private_artifacts(link_list)
        link_list = self._format_link_list(link_list)
        return link_list

    def _remove_private_artifacts(self, link_list):
        refined_list = []
        for link in link_list:
            match = re.search("^_", link["path"])
            if not match:
                refined_list.append(link)
        return refined_list

    def _format_link(self, link):
        title = link.get("title", link["path"])
        url = self.builder.build(link["path"])
        rel = link.get("type")
        return self._build_link(url, rel, title)

    def _build_link(self, path, rel, title):
        return "{0}; rel={1}; title={2}".format(path, rel, title)

    def _format_link_list(self, link_list):
        new_link_list = []
        for link in link_list:
            new_link_list.append(self._format_link(link))

        return new_link_list
