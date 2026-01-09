class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list | None = None,
        props: dict | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Error: Not Implemented")

    def props_to_html(self):
        result = ""

        if self.props is None:
            return result

        for attr, value in self.props.items():
            result += f' {attr}="{value}"'
        return result

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, props: {self.props})"
