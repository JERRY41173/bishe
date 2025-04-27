from fastapi import APIRouter, HTTPException
from manager.readfile import file_to_text
import json
from fastapi import File

from langchain_deepseek import ChatDeepSeek
from typing import Optional
from pydantic import BaseModel, Field

class Requirements(BaseModel):
    '''Joke to tell user.'''
    project_requirements: str = Field(description="项目概况")
    scoring_criteria: str = Field(description="scoring_criteria")

class Chapter(BaseModel):
    title: str = Field(description="章节标题")
    sections: Optional[list["Section"]] = Field(default_factory=list,description="一级子目录列表")
    
class Section(BaseModel):
    title: str = Field(description="一级子目录标题")
    subsections: Optional[list["Subsection"]] = Field(default_factory=list,description="二级子目录列表")
    
class Subsection(BaseModel):
    title: str = Field(description="二级子目录标题")
    content: Optional[str] = Field(default_factory=str,description="正文内容")
    
llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=1.0,
    max_tokens=1024,
    timeout=None,
    max_retries=2,
)
# from manager.LLM import LLM

#标书撰写页面接口,各种定义需要重新写
router = APIRouter(
    prefix="/writer",
    tags=["writer"],
    responses={404: {"description": "Not found"}},
)

#用户上传招标文件解析
@router.post("/upload")
async def upload_file(file: bytes = File(..., max_length=2097152)):
    #使用docling解析招标文件
    docs = file_to_text(file)
    print(docs)
    structuredllm = llm.with_structured_output(Requirements)
    response = structuredllm.invoke (f'分析下列文本，得到项目概况和评分标准，如不包含相关信息则返回未能找到相关信息。{docs}')
    
    return {
        "project_requirements": response.project_requirements,
        "scoring_criteria": response.scoring_criteria,
    }

#从前端获取用户手动粘贴项目要求和评分标准，点击生成第一章目录
@router.post("/paste")
async def paste_requirements(project_requirements: str, scoring_criteria: str):
    structuredllm = llm.with_structured_output(Chapter)
    response = structuredllm.invoke (f'参考招标项目的项目概况和评分标准，生成投标书第一章，要求包含章节标题，一级子目录列表和二级子目录列表，（注意：在各级title中不要包含章节序号）以便于后续分块生成正文。项目概况：{project_requirements}，评分标准：{scoring_criteria}')
    return response
    
#获取前端传来的章节列表，生成第n章，返回新的章节列表给前端
@router.post("/generate_chapter")
async def generate_chapter(chapter: list[Chapter], chapter_number: int):
    # 生成新的章节列表
    new_chapter = Chapter(f"第{chapter_number}章")
    chapter.insert(chapter_number, new_chapter)
    return chapter
    
#获取前端传来的章节列表和需要补全的章节号n，补全第n章内容，返回新的章节列表给前端
@router.post("/complete_chapter")
async def complete_chapter(chapter: list[Chapter], chapter_number: int):
    # 补全第n章内容
    if chapter_number < len(chapter):
        chapter[chapter_number].title = f"补全的第{chapter_number}章"
    else:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter

#获取前端传来的章节列表和需要生成正文的章节号n,将该章的所有小节内容生成正文，返回新的章节列表给前端
@router.post("/generate_content")
async def generate_content(chapter: list[Chapter], chapter_number: int):
    # 生成正文
    if chapter_number < len(chapter):
        for section in chapter[chapter_number].sections:
            for subsection in section.subsections:
                subsection.add_content(f"正文内容：{subsection.title}")
    else:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter