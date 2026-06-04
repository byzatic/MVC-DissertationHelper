import html

from config import CHECK_SEQUENCE_ONLY_IN
from src.patterns import REFERENCE_PATTERN, FIGURE_PATTERN, WT_PATTERN
from src.logger import ScriptLogger
from src.reference_shifter import ReferenceShifter
from src.figure_shifter import FigureShifter
from src.reference_checker import ReferenceChecker
from src.text_utils import get_context
from src.nonprintable_checker import NonPrintableChecker


class XmlTextPatcher:
    def __init__(
            self,
            shifter: ReferenceShifter,
            figure_shifter: FigureShifter,
            checker: ReferenceChecker,
            nonprintable_checker: NonPrintableChecker,
            logger: ScriptLogger
    ):
        self.shifter = shifter
        self.figure_shifter = figure_shifter
        self.checker = checker
        self.nonprintable_checker = nonprintable_checker
        self.logger = logger

    def extract_wt_nodes(self, xml_text: str):
        nodes = []
        plain_pos = 0

        for match in WT_PATTERN.finditer(xml_text):
            start_tag = match.group(1)
            raw_text = match.group(2)
            end_tag = match.group(3)

            decoded_text = html.unescape(raw_text)

            node_start = plain_pos
            node_end = node_start + len(decoded_text)

            nodes.append({
                "match_start": match.start(),
                "match_end": match.end(),
                "start_tag": start_tag,
                "text": decoded_text,
                "end_tag": end_tag,
                "plain_start": node_start,
                "plain_end": node_end,
            })

            plain_pos = node_end

        return nodes

    def collect_reference_replacements(self, text: str, file_name: str):
        replacements_info = []

        for match in REFERENCE_PATTERN.finditer(text):
            replacements = []
            old_ref = match.group(0)
            new_ref = self.shifter.process_reference_text(old_ref, replacements)

            if not replacements:
                continue

            before_context, after_context = get_context(
                text,
                match.start(),
                match.end()
            )

            self.logger.separator()
            self.logger.log(f"File: {file_name}")
            self.logger.log(
                f"Context: ... {before_context} {old_ref} {after_context} ..."
            )
            self.logger.log(f"Replace reference: {old_ref} -> {new_ref}")

            for replacement in replacements:
                self.logger.log(f"  {replacement}")

            replacements_info.append({
                "start": match.start(),
                "end": match.end(),
                "old": old_ref,
                "new": new_ref,
                "kind": "reference",
            })

        return replacements_info

    def collect_figure_replacements(self, text: str, file_name: str):
        replacements_info = []

        for match in FIGURE_PATTERN.finditer(text):
            old_number_text = match.group("number")
            new_number_text = self.figure_shifter.process_figure_number(old_number_text)

            if old_number_text == new_number_text:
                continue

            old_text = match.group(0)
            new_text = match.group("prefix") + new_number_text

            before_context, after_context = get_context(
                text,
                match.start(),
                match.end()
            )

            self.logger.separator()
            self.logger.log(f"File: {file_name}")
            self.logger.log(
                f"Context: ... {before_context} {old_text} {after_context} ..."
            )
            self.logger.log(f"Replace figure: {old_text} -> {new_text}")
            self.logger.log(f"  {old_number_text} -> {new_number_text}")

            replacements_info.append({
                "start": match.start(),
                "end": match.end(),
                "old": old_text,
                "new": new_text,
                "kind": "figure",
            })

        return replacements_info

    def collect_replacements(self, text: str, file_name: str):
        replacements_info = []
        replacements_info.extend(
            self.collect_reference_replacements(text, file_name)
        )
        replacements_info.extend(
            self.collect_figure_replacements(text, file_name)
        )

        replacements_info.sort(key=lambda item: item["start"])
        return replacements_info

    def apply_replacements_to_nodes(self, nodes, replacements_info):
        updated_nodes = []

        for node in nodes:
            node_start = node["plain_start"]
            node_end = node["plain_end"]

            cursor = node_start
            parts = []

            for replacement in replacements_info:
                rep_start = replacement["start"]
                rep_end = replacement["end"]
                rep_new = replacement["new"]

                if rep_end <= node_start or rep_start >= node_end:
                    continue

                if rep_start >= node_start:
                    before_start = cursor
                    before_end = min(rep_start, node_end)

                    if before_end > before_start:
                        local_start = before_start - node_start
                        local_end = before_end - node_start
                        parts.append(node["text"][local_start:local_end])

                    parts.append(rep_new)

                cursor = max(cursor, min(rep_end, node_end))

            if cursor < node_end:
                local_start = cursor - node_start
                parts.append(node["text"][local_start:])

            updated_nodes.append({
                **node,
                "new_text": "".join(parts)
            })

        return updated_nodes

    def rebuild_xml(self, xml_text: str, updated_nodes) -> str:
        result = []
        last = 0

        for node in updated_nodes:
            result.append(xml_text[last:node["match_start"]])

            escaped = html.escape(node["new_text"], quote=False)

            result.append(
                node["start_tag"] +
                escaped +
                node["end_tag"]
            )

            last = node["match_end"]

        result.append(xml_text[last:])

        return "".join(result)

    def patch_xml_text_nodes(self, xml_text: str, file_name: str) -> str:
        nodes = self.extract_wt_nodes(xml_text)

        if not nodes:
            return xml_text

        plain_text = "".join(node["text"] for node in nodes)

        if file_name == CHECK_SEQUENCE_ONLY_IN:
            self.checker.check_sequence(plain_text, file_name)
            self.nonprintable_checker.check(plain_text, file_name)

        replacements_info = self.collect_replacements(plain_text, file_name)

        if not replacements_info:
            return xml_text

        updated_nodes = self.apply_replacements_to_nodes(
            nodes,
            replacements_info
        )

        return self.rebuild_xml(xml_text, updated_nodes)
