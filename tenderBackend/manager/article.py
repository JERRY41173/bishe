from pydantic import BaseModel

class Article(BaseModel):
    def __init__(self, title: str):
        self.title = title
        self.chapters = []

    def add_chapter(self, chapter_title: str):
        chapter = Chapter(chapter_title)
        self.chapters.append(chapter)
        return chapter
    
    def __repr__(self):
        return f"Article(title={self.title}, chapters=[{', '.join(repr(chapter) for chapter in self.chapters)}])"
    
class Chapter(BaseModel):
    def __init__(self, title: str):
        self.title = title
        self.sections = []

    def add_section(self, section_title: str):
        section = Section(section_title)
        self.sections.append(section)
        return section

    def __repr__(self):
        return f"Chapter(title={self.title}, sections={self.sections})"
    
class Section(BaseModel):
    def __init__(self, title: str):
        self.title = title
        self.subsections = []

    def add_subsection(self, subsection_title: str):
        subsection = Subsection(subsection_title)
        self.subsections.append(subsection)
        return subsection

    def __repr__(self):
        return f"Section(title={self.title}, subsections={self.subsections})"
    
class Subsection(BaseModel):
    def __init__(self, title: str):
        self.title = title
    def add_content(self, content: str):
        self.content = content
        return self.content
    def __repr__(self):
        return f"Subsection(title={self.title})"
    