# Copyright 2018-2022 NV Access Limited, Babbage B.V
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2.0, as published by
# the Free Software Foundation.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# This license can be found at:
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
import logging as log
import os
import shutil
from typing import (
	Dict,
	Tuple,
	Iterable,
)
import codecs
from xml.etree import ElementTree
from collections import OrderedDict

log.basicConfig(
	level=log.INFO,
	format='%(levelname)s:%(message)s'
)

PathT = str


def createCLDRAnnotationsDict(
	sources: Iterable[PathT],
	dest: PathT,
	level: str,
) -> None:
	"""Produce NVDA dict file based on CLDR annotations.
	"""
	log.info(f'Generating {dest}')
	log.debug(f'Sources: {sources}')

	cldrDict = OrderedDict()
	for source in sources:
		tree = ElementTree.parse(source)
		for element in tree.iter("annotation"):
			if element.attrib.get("type") == "tts":
				cldrDict[element.attrib['cp']] = element.text.replace(":", "")

	assert cldrDict, "cldrDict is empty"
	with codecs.open(dest, "w", "utf_8_sig", errors="replace") as dictFile:
		dictFile.write(u"symbols:\r\n")
		for pattern, description in cldrDict.items():
			dictFile.write(
				f"{pattern}\t{description}\t{level}\r\n"
			)


NvdaLocaleT = str
CldrLocaleT = str


def getNvdaToCldrLocales() -> Dict[NvdaLocaleT, Tuple[CldrLocaleT]]:
	return {
		"af_ZA": ("af",),
		"am": ("am",),
		# "an":(),
		"ar": ("ar",),
		"as": ("as",),
		"bg": ("bg",),
		"bn": ("bn",),
		"ca": ("ca",),
		"ckb": ("ckb",),
		"cs": ("cs",),
		"da": ("da",),
		"de": ("de",),
		"de_CH": ("de_CH",),
		"el": ("el",),
		"en": ("en_001", "en"),
		"es": ("es",),
		"es_CO": ("es_419",),
		"fa": ("fa",),
		"fi": ("fi",),
		"fr": ("fr",),
		"ga": ("ga",),
		"gl": ("gl",),
		"gu": ("gu",),
		"he": ("he",),
		"hi": ("hi",),
		"hr": ("hr",),
		"hu": ("hu",),
		"id": ("id",),
		"is": ("is",),
		"it": ("it",),
		"ja": ("ja",),
		"ka": ("ka",),
		# "kmr":(),
		"kn": ("kn",),
		"ko": ("ko",),
		"kok": ("kok",),
		"ky": ("ky",),
		"lt": ("lt",),
		"mk": ("mk",),
		"ml": ("ml",),
		"mn": ("mn",),
		"mni": ("mni",),
		"my": ("my",),
		"nb_NO": ("no",),
		"ne": ("ne",),
		"nl": ("nl",),
		"nn_NO": ("nn",),
		"pa": ("pa",),
		"pl": ("pl",),
		"pt_BR": ("pt",),
		"pt_pt": ("pt", "pt_PT"),
		"ro": ("ro",),
		"ru": ("ru",),
		"sk": ("sk",),
		"sl": ("sl",),
		"so": ("so",),
		"sq": ("sq",),
		"sr": ("sr",),
		"sv": ("sv",),
		"ta": ("ta",),
		"te": ("te",),
		"th": ("th",),
		"tr": ("tr",),
		"uk": ("uk",),
		"ur": ("ur",),
		"vi": ("vi",),
		"zh_cn": ("zh",),
		"zh_hk": ("zh", "zh_Hant_HK"),
		"zh_tw": ("zh", "zh_Hant"),
	}


def _assertDirs(outDir: PathT, annotationsDir: PathT, annotationsDerivedDir: PathT) -> None:
	cldrDirsExist = os.path.exists(annotationsDir) and os.path.exists(annotationsDerivedDir)
	assert cldrDirsExist, (
		"CLDR directories not found, has the CLDR submodule been cloned?"
		f" Expected: {annotationsDir} and {annotationsDerivedDir}"
	)
	outDirExists = os.path.exists(outDir)
	assert not outDirExists, (
		"Output directory not clean (remove all files before running again)"
		f": {outDir}"
	)


def createLocalesFromCldr(outDir: PathT) -> None:
	COMMON_DIR = os.path.join("cldr", "production", "common")
	ANNOTATIONS_DIR: PathT = os.path.join(COMMON_DIR, "annotations")
	ANNOTATIONS_DERIVED_DIR: PathT = os.path.join(COMMON_DIR, "annotationsDerived")

	_assertDirs(outDir, ANNOTATIONS_DIR, ANNOTATIONS_DERIVED_DIR)

	log.info("Generating cldr dicts.")
	log.info(f"OutDir: {outDir}")
	destLocale: NvdaLocaleT  # E.G. "af_ZA"
	sourceLocales: Tuple[CldrLocaleT]  # E.G. ("af",)
	for destLocale, sourceLocales in getNvdaToCldrLocales().items():
		cldrSources = []
		# First add all annotations, then the derived ones.
		# todo: Why is this grouping/order important?
		for sourceLocale in sourceLocales:
			annotationSource = os.path.join(ANNOTATIONS_DIR, f"{sourceLocale}.xml")
			assert os.path.isfile(annotationSource)
			cldrSources.append(annotationSource)

		for sourceLocale in sourceLocales:
			annotationsDerivedSource = os.path.join(ANNOTATIONS_DERIVED_DIR, f"{sourceLocale}.xml")
			assert os.path.isfile(annotationsDerivedSource)
			cldrSources.append(annotationsDerivedSource)

		localeOutDir = os.path.join(outDir, destLocale)
		os.makedirs(localeOutDir)
		assert os.path.isdir(localeOutDir), f"Locale output dir must exist: {localeOutDir}"
		outFile = os.path.join(localeOutDir, "cldr.dic")
		if destLocale == "en":
			# For English (the default fallback), punctuations are set to none for CLDR characters to be pronounced
			# even if user set punctuation level to None
			level = 'none'
		else:
			# For other languages the level is set to be inherited from English symbol file or English CLDR file.
			level = '-'
		createCLDRAnnotationsDict(cldrSources, outFile, level)


def main():
	OUT_DIR: PathT = "out"
	OUT_LOCALE_DIR: PathT = os.path.join(OUT_DIR, "locale")
	createLocalesFromCldr(
		outDir=OUT_LOCALE_DIR,
	)

	log.info("Generating cldr dictionaries complete.")
	ZIP_PATH: PathT = os.path.join(OUT_DIR, 'cldrLocaleDicts')
	log.info(f"Archiving: {ZIP_PATH}.zip")
	shutil.make_archive(ZIP_PATH, 'zip', OUT_LOCALE_DIR)
	log.info("Done.")

if __name__ == '__main__':
	main()
