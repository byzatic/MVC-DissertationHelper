#!/usr/bin/env python3

from src.logger import ScriptLogger
from src.reference_shifter import ReferenceShifter
from src.reference_checker import ReferenceChecker
from src.figure_shifter import FigureShifter
from src.xml_text_patcher import XmlTextPatcher
from src.docx_patcher import DocxPatcher
from src.nonprintable_checker import NonPrintableChecker


def main():
    logger = ScriptLogger()
    shifter = ReferenceShifter()
    figure_shifter = FigureShifter()

    reference_checker = ReferenceChecker(
        shifter=shifter,
        logger=logger
    )

    nonprintable_checker = NonPrintableChecker(
        logger=logger
    )

    xml_patcher = XmlTextPatcher(
        shifter=shifter,
        figure_shifter=figure_shifter,
        checker=reference_checker,
        logger=logger,
        nonprintable_checker=nonprintable_checker
    )

    docx_patcher = DocxPatcher(
        patcher=xml_patcher,
        logger=logger
    )

    try:
        docx_patcher.patch()
    finally:
        logger.flush()


if __name__ == "__main__":
    main()
