import re
from dataclasses import dataclass
from typing import List

APOSTROPHE_VARIANTS = ["'", "’", "᾿", "ʼ", "”", '"']
TOKEN_SPLIT_RE = re.compile(r"[\s,;:()\[\]{}<>]+")
ACCENT_RE = re.compile(r"[́̀̂̌]")

SUFFIX_MAP = {
    "II_dual_plur": {
        "past_plural": {"1": ["наць", "ӈахаюнаць"], "2/3": ["даць", "ӈахаюдаць"], "3": ["донзь", "ӈахаюдонзь"]},
        "past_dual": {"1": ["нинзь", "ӈахаюнинзь"], "2/3": ["ӈахаюдинзь"]},
        "past_singular": {"1/2": ["нась", "ӈахаюнась"], "2/3": ["дась", "ӈахаюдась"]},
        "present_plural": {"1": ["на’", "ӈахаюна’"], "2/3": ["да’", "ӈахаюда’"], "3": ["до’", "ӈахаюдо’"]},
        "present_dual": {"1": ["ни’", "ӈахаюни’"], "2/3": ["ди’", "ӈахаюди’"]},
        "present_singular": {"1/2": ["н", "ӈахаюн"], "2": ["д", "ӈахаюд"], "2/3": ["да", "ӈахаюда"]},
    },
    "II_sing_obj": {
        "past_plural": {"1": ["ваць"], "2": ["раць"], "3": ["донзь"]},
        "past_dual": {"1": ["минзь"], "2": ["ринзь"], "2/3": ["динзь"]},
        "past_singular": {"1": ["вась"], "2": ["рась"], "2/3": ["дась"]},
        "present_plural": {"1": ["ва’"], "2": ["ра’"], "3": ["до’"]},
        "present_dual": {"1": ["ми’"], "2": ["ри’"], "2/3": ["ди’"]},
        "present_singular": {"1": ["в"], "2": ["р"], "2/3": ["да"]},
    },
    "III": {
        "past_plural": {"1": ["наць"], "2/3": ["даць"]},
        "past_dual": {"1": ["нинзь"], "2/3": ["динзь"], "3": ["хынзь"]},
        "past_singular": {"1": ["ваць"], "1/2": ["нась"], "3": ["ць"]},
        "present_plural": {"1": ["на’"], "2/3": ["да’"], "3": ["д’"]},
        "present_dual": {"1": ["ни’"], "2/3": ["ди’"], "3": ["хы’"]},
        "present_singular": {"1": ["в’"], "2": ["н’"]},
    },
    "I": {
        "past_plural": {"1": ["ва’"], "2": ["да’"]},
        "past_dual": {"1": ["нинзь"], "2/3": ["динзь’"], "3": ["ханзь", "ӈаханзь"]},
        "past_singular": {"1": ["дамзь", "манзь"], "1/2": ["нась"], "3": ["сь"]},
        "present_dual": {"1": ["ни’"], "2/3": ["ди’"], "3": ["ӈаха’", "ха’"]},
        "present_singular": {"1": ["м", "дм"], "1/2": ["н"]},
        "present_plural": {"1": ["ва’"], "2": ["да’"], "3": ["’"]},
    },
}

TYPE_LABELS = {
    "I": "I тип",
    "II_sing_obj": "II тип (ед. объект)",
    "II_dual_plur": "II тип (дв./мн. объект)",
    "III": "III тип",
}

TENSE_LABELS = {
    "present_singular": ("Неопределенное", "единственное"),
    "present_dual": ("Неопределенное", "двойственное"),
    "present_plural": ("Неопределенное", "множественное"),
    "past_singular": ("Прошедшее", "единственное"),
    "past_dual": ("Прошедшее", "двойственное"),
    "past_plural": ("Прошедшее", "множественное"),
}


@dataclass(frozen=True)
class LemmatizerCandidate:
    lemma: str
    suffix: str
    tense: str
    tense_label: str
    number_label: str
    person: str
    suffix_type: str
    suffix_type_label: str
    note: str = ""


def remove_accents(word: str) -> str:
    return ACCENT_RE.sub("", word or "")


def normalize_word(raw_word: str) -> str:
    word = (raw_word or "").strip().lower()
    for variant in APOSTROPHE_VARIANTS:
        word = word.replace(variant, "’")
    word = re.sub(r"\s+", "", word)
    return remove_accents(word)


def normalize_lemma(base: str) -> str:
    replacements = [("хаю", ""), ("у", "о"), ("ю", "ё")]
    for suffix, replacement in replacements:
        if base.endswith(suffix) and base:
            return base[:-len(suffix)] + replacement
    return base


def build_suffix_rules():
    rules = []
    for suffix_type, tense_map in SUFFIX_MAP.items():
        for tense, person_map in tense_map.items():
            for person, suffix_list in person_map.items():
                for suffix in suffix_list:
                    rules.append(
                        {
                            "suffix_type": suffix_type,
                            "tense": tense,
                            "person": person,
                            "suffix": suffix,
                        }
                    )
    rules.sort(key=lambda item: len(item["suffix"]), reverse=True)
    return rules


SUFFIX_RULES = build_suffix_rules()


def lemmatize_verb(word: str, max_results: int = 6) -> dict:
    normalized = normalize_word(word)
    if not normalized:
        return {
            "input": word,
            "normalized": normalized,
            "candidates": [],
            "is_base_guess": False,
        }

    candidates = []
    seen = set()
    for rule in SUFFIX_RULES:
        suffix = rule["suffix"]
        if normalized.endswith(suffix) and len(normalized) > len(suffix):
            base = normalized[: -len(suffix)]
            lemma = normalize_lemma(base)
            if not lemma or lemma in seen:
                continue
            seen.add(lemma)
            tense_label, number_label = TENSE_LABELS.get(rule["tense"], ("", ""))
            candidates.append(
                LemmatizerCandidate(
                    lemma=lemma,
                    suffix=suffix,
                    tense=rule["tense"],
                    tense_label=tense_label,
                    number_label=number_label,
                    person=rule["person"],
                    suffix_type=rule["suffix_type"],
                    suffix_type_label=TYPE_LABELS.get(rule["suffix_type"], rule["suffix_type"]),
                ).__dict__
            )
            if len(candidates) >= max_results:
                break

    if not candidates:
        candidates = [
            LemmatizerCandidate(
                lemma=normalized,
                suffix="",
                tense="",
                tense_label="",
                number_label="",
                person="",
                suffix_type="",
                suffix_type_label="",
                note="Суффикс не распознан. Возможно, введена уже базовая форма.",
            ).__dict__
        ]
        is_base_guess = True
    else:
        is_base_guess = False

    return {
        "input": word,
        "normalized": normalized,
        "candidates": candidates,
        "is_base_guess": is_base_guess,
    }


def split_input(text: str, max_items: int = 32) -> List[str]:
    raw_tokens = [token.strip() for token in TOKEN_SPLIT_RE.split(text or "") if token.strip()]
    return raw_tokens[:max_items]


def lemmatize_many(text: str, max_items: int = 32) -> List[dict]:
    return [lemmatize_verb(token) for token in split_input(text, max_items=max_items)]
