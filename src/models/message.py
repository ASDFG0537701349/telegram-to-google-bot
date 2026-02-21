from pydantic import BaseModel, ConfigDict, Field


class PhotoData(BaseModel):
    model_config = ConfigDict(frozen=True)

    file_url: str = Field(description="Public HTTPS URL to the image file")
    caption: str | None = Field(default=None, description="Optional photo caption")
    mime_type: str = Field(default="image/jpeg", description="MIME type of the image")


class ForwardableMessage(BaseModel):
    model_config = ConfigDict(frozen=True)

    text: str | None = Field(default=None, description="Plain text content")
    photo: PhotoData | None = Field(default=None, description="Photo attachment data")
    sender_name: str = Field(default="Unknown", description="Name of message sender")
    chat_title: str = Field(default="Unknown Chat", description="Source chat title")
