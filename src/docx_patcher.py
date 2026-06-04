import zipfile
import shutil
from tempfile import TemporaryDirectory
from pathlib import Path

from config import INPUT_FILE, OUTPUT_FILE, XML_FILES, START_FROM, SHIFT
from src.logger import ScriptLogger
from src.xml_text_patcher import XmlTextPatcher


class DocxPatcher:
    def __init__(self, patcher: XmlTextPatcher, logger: ScriptLogger):
        self.patcher = patcher
        self.logger = logger

    def patch(self):
        if not INPUT_FILE.exists():
            raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

        if OUTPUT_FILE.exists():
            OUTPUT_FILE.unlink()

        shutil.copy2(INPUT_FILE, OUTPUT_FILE)

        changed_files = 0

        with TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)

            with zipfile.ZipFile(OUTPUT_FILE, "r") as zin:
                zin.extractall(tmp_path)

            for xml_file in XML_FILES:
                path = tmp_path / xml_file

                if not path.exists():
                    continue

                original = path.read_text(encoding="utf-8")
                updated = self.patcher.patch_xml_text_nodes(original, xml_file)

                if updated != original:
                    path.write_text(updated, encoding="utf-8")
                    changed_files += 1

            with zipfile.ZipFile(
                OUTPUT_FILE,
                "w",
                compression=zipfile.ZIP_DEFLATED
            ) as zout:
                for file_path in tmp_path.rglob("*"):
                    if file_path.is_file():
                        archive_name = file_path.relative_to(tmp_path).as_posix()
                        zout.write(file_path, archive_name)

        self.logger.separator()
        self.logger.log(f"Input: {INPUT_FILE}")
        self.logger.log(f"Start from: {START_FROM}")
        self.logger.log(f"Shift: {SHIFT}")
        self.logger.log(f"Changed XML files: {changed_files}")
        self.logger.log(f"Saved: {OUTPUT_FILE}")