import zipfile
from pathlib import Path

from inf8239_u02.data import prepare_sms_spam


def _build_sample_zip(path: Path) -> Path:
    lines = "ham\tHola, como estas\nspam\tGana un premio ya\n"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("SMSSpamCollection", lines)
    return path


def test_prepare_sms_spam_extracts_tab_separated_labels(tmp_path):
    zip_path = _build_sample_zip(tmp_path / "sms.zip")
    destination = tmp_path / "data" / "raw" / "dataset.csv"

    prepare_sms_spam(zip_path, destination)

    content = destination.read_text(encoding="utf-8")
    assert content.splitlines()[0] == "label,text"
    assert "ham,\"Hola, como estas\"" in content
    assert "spam,Gana un premio ya" in content


def test_prepare_sms_spam_creates_parent_directories(tmp_path):
    zip_path = _build_sample_zip(tmp_path / "sms.zip")
    destination = tmp_path / "nested" / "dataset.csv"

    result = prepare_sms_spam(zip_path, destination)

    assert result == destination
    assert destination.exists()
