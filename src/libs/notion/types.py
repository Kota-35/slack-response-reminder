"""Notion types."""

from typing import Literal

from pydantic import BaseModel, Field


class RichTextObject(BaseModel):
    """Rich text object."""

    plain_text: str = Field(description="plain_text")


class RichTextProperty(BaseModel):
    """Rich text property."""

    id: str = Field(description="id")
    type: Literal["rich_text"] = Field(description="type")
    rich_text: list[RichTextObject] = Field(description="rich_text")


class PeopleObject(BaseModel):
    """People object."""

    id: str = Field(description="id")


class PeopleProperty(BaseModel):
    """People property."""

    id: str = Field(description="id")
    type: Literal["people"] = Field(description="type")
    people: list[PeopleObject | None] = Field(description="people")


class TitleObject(BaseModel):
    """Title object."""

    plain_text: str = Field(description="plain_text")


class TitleProperty(BaseModel):
    """Title property."""

    id: str = Field(description="id")
    type: Literal["title"] = Field(description="type")
    title: list[TitleObject | None] = Field(description="title")


class StatusObject(BaseModel):
    """Status object."""

    name: str = Field(description="name")


class StatusProperty(BaseModel):
    """Status property."""

    id: str = Field(description="id")
    type: Literal["status"] = Field(description="type")
    status: StatusObject = Field(description="status")
