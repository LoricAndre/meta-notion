from os import environ as env
import notion_client as notion
from notion_client.helpers import collect_paginated_api
from anyascii import anyascii


class Notion(notion.Client):
    def getAllPages(self):
        return collect_paginated_api(self.search)


def main():
    client = Notion(auth=env.get("NOTION_TOKEN"))
    pages = client.getAllPages()
    for page in pages:
        for _prop, val in page["properties"].items():
            _ = page["properties"]  # For use in formulas
            if _prop[0] == '_':
                prop = _prop[1:]
                if val["type"] == "rich_text" and len(val["rich_text"]) > 0:
                    formula = val["rich_text"][0]["text"]["content"]
                    new_prop = {
                        _[prop]["type"]: [{"type": "text", "text": {
                            "content": str(eval(anyascii(formula)))}}]
                    }
                    client.pages.update(
                        page["id"], properties={prop: new_prop})
                    print(f"Computed {prop} from {_prop}")


if __name__ == "__main__":
    main()
