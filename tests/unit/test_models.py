import pytest
from pydantic import ValidationError

from src.models.message import ForwardableMessage, PhotoData


class TestPhotoData:
    def test_creates_with_required_fields(self):
        photo = PhotoData(file_url="https://example.com/photo.jpg")

        assert photo.file_url == "https://example.com/photo.jpg"
        assert photo.caption is None
        assert photo.mime_type == "image/jpeg"

    def test_creates_with_all_fields(self):
        photo = PhotoData(
            file_url="https://example.com/photo.png",
            caption="A sunset",
            mime_type="image/png",
        )

        assert photo.file_url == "https://example.com/photo.png"
        assert photo.caption == "A sunset"
        assert photo.mime_type == "image/png"

    def test_is_frozen(self):
        photo = PhotoData(file_url="https://example.com/photo.jpg")

        with pytest.raises(ValidationError):
            photo.file_url = "https://example.com/other.jpg"

    def test_missing_file_url_raises(self):
        with pytest.raises(ValidationError):
            PhotoData()


class TestForwardableMessage:
    def test_creates_text_message(self):
        msg = ForwardableMessage(text="Hello")

        assert msg.text == "Hello"
        assert msg.photo is None
        assert msg.sender_name == "Unknown"
        assert msg.chat_title == "Unknown Chat"

    def test_creates_photo_message(self):
        photo = PhotoData(file_url="https://example.com/photo.jpg")
        msg = ForwardableMessage(photo=photo, sender_name="John")

        assert msg.text is None
        assert msg.photo == photo
        assert msg.sender_name == "John"

    def test_creates_with_all_fields(self):
        photo = PhotoData(file_url="https://example.com/photo.jpg", caption="Pic")
        msg = ForwardableMessage(
            text="Hello",
            photo=photo,
            sender_name="Jane",
            chat_title="Dev Chat",
        )

        assert msg.text == "Hello"
        assert msg.photo.caption == "Pic"
        assert msg.sender_name == "Jane"
        assert msg.chat_title == "Dev Chat"

    def test_is_frozen(self):
        msg = ForwardableMessage(text="Hello")

        with pytest.raises(ValidationError):
            msg.text = "Changed"

    def test_defaults_applied(self):
        msg = ForwardableMessage()

        assert msg.text is None
        assert msg.photo is None
        assert msg.sender_name == "Unknown"
        assert msg.chat_title == "Unknown Chat"
