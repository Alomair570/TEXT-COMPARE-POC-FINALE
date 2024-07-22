plural_patterns = [("افعال", "فعل"),
                   ("فعال", "فعل"),
                   ("فعول", "فعل"),
                   ("افعلاء", "فعل"),
                   ("فعلاء", "فعل"),
                   ("فعلان", "فعل"),
                   # ("فعل", "فعلة"),
                   ("فعلاة", "فعلة"),
                   ("فعال", "فاعل"),
                   ("فواعل", "فاعل"),
                   ("فعلاء", "فاعل"),
                   ("فواعل", "فاعلة"),
                   ("مفاعل", "مفعل"),
                   ("مفاعل", "مفعلة"),
                   ("فعلاء", "فعيل"),
                   ("افعلاء", "فعيل"),
                   ("فعلى", "فعيل"),
                   ("فعائل", "فعيلة"),
                   ("فعالى", "فعيلة"),
                   ("فعل", "فعيلة"),
                   ("فعل", "فعال"),
                   ("افعلة", "فعال"),
                   ("فعالون", "فعال"),
                   ("فعالات", "فعال"),
                   ("فواعيل", "فاعول"),
                   ("مفاعيل", "مفعول"),
                   ("مفاعيل", "مفعال"),
                   ("افتعالات", "افتعال"),
                   ("افعال", "فعلة"),
                   ("افوعل", "فعل"),
                   ("فعول", "فعلة"),
                   ("فعالي", "فعلاء"),
                   ("فعالي", "فعل"),
                   ("فعالي", "فعلي"),
                   ("فعل", "فعالة"),
                   ("فعائل", "فعالة"),
                   ("فعال", "فعيل"),
                   ("مفتعلات", "مفتعل"),
                   ("فعالى", "فعيلة")
                   ]

suf3 = [
    "\u062a\u0645\u0644",
    "\u0647\u0645\u0644",
    "\u062a\u0627\u0646",
    "\u062a\u064a\u0646",
    "\u0643\u0645\u0644",
]

# length two suffixes
suf2 = [
    "\u062a\u0646",
    "\u0643\u0645",
    "\u0647\u0646",
    "\u0646\u0627",
    "\u064a\u0627",
    "\u0647\u0627",
    "\u062a\u0645",
    "\u0643\u0646",
    "\u0646\u064a",
    "\u0648\u0627",
    "\u0645\u0627",
    "\u0647\u0645",
]

suf1 = [ "\u0647", "\u064a", "\u0643", "\u062a", "\u0627", "\u0646"]

from nltk.stem.isri import ISRIStemmer # type: ignore
from itertools import product


def matching(name1, name2):
    if name1 == name2:
        return True
    return False


def matching_no_space(name1, name2):
    if name1.replace(" ", "") == name2.replace(" ", ""):
        return True
    return False


def waw(word):
    if word[0] == 'و':
        return word[1:]
    return word


def matching_set(name1, name2):
    norm_name1_words = [waw(word) for word in name1.split()]
    norm_name2_words = [waw(word) for word in name2.split()]
    if set(norm_name1_words) == set(norm_name2_words):
        return True
    return False


def pattern_recognizer(word1, word2, pattern1, pattern2):
    if len(word1) != len(pattern1):
        return False
    if len(word2) != len(pattern2):
        return False
    for i in range(len(word1)):
        if pattern1[i] == 'ف':
            char1 = word1[i]
        elif pattern1[i] == 'ع':
            char2 = word1[i]
        elif pattern1[i] == 'ل':
            char3 = word1[i]
        else:
            if word1[i] != pattern1[i]:
                return False
    for i in range(len(word2)):
        if pattern2[i] == 'ف':
            if word2[i] != char1:
                return False
        elif pattern2[i] == 'ع':
            if word2[i] != char2:
                return False
        elif pattern2[i] == 'ل':
            if word2[i] != char3:
                return False
        else:
            if word2[i] != pattern2[i]:
                return False
    return True


def regular_number(word1, word2):
    if word1 == word2[:-2] and word2[-2:] == "ون":  # جمع مذكر سالم مرفوع
        return True
    elif word1 == word2[:-2] and word2[-2:] == "ان":  # مثنى مذكر مرفوع
        return True
    elif word1 == word2[:-2] and word2[-2:] == "ين":  # جمع مذكر سالم ومثنى مذكر غير مرفوعين
        return True
    elif word1[:-1] == word2[:-3] and word2[-3:] == "تان" and word1[-1] in ["ة", "ت"]:  # مثنى مؤنث مرفوع
        return True
    elif word1[:-1] == word2[:-3] and word2[-3:] == "تين" and word1[-1] in ["ة", "ت"]:  # مثنى مؤنث غير مرفوع
        return True
    elif word1[:-1] == word2[:-2] and word2[-2:] == "ات" and word1[-1] in ["ة", "ت"]:  # جمع مؤنث سالم
        return True
    elif word2[-2:] == "ان" and similar_number(word1, word2[:-2]):  # مثنى مذكر مرفوع
        return True
    elif word2[-2:] == "ين" and similar_number(word1, word2[:-2]):  # مثنى مذكر مرفوع
        return True
    elif word2[-3:] == "تان" and similar_number(word1, word2[:-3]):  # مثنى مذكر مرفوع
        return True
    return False


def similar_number(word1, word2):
    if regular_number(word1, word2) or regular_number(word2, word1):
        return True
    for pattern1, pattern2 in plural_patterns:
        if pattern_recognizer(word1, word2, pattern1, pattern2) or pattern_recognizer(word1, word2, pattern2, pattern1):
            return True
        if word1[0] == "و" and word2[0] == "و":
            if pattern_recognizer(word1[1:], word2[1:], pattern1, pattern2) or pattern_recognizer(word1[1:], word2[1:],
                                                                                                  pattern2, pattern1):
                return True
    return False


def similar_gender(word1, word2):
    if word1 == word2[:-1] and word2[-1] in ['ة', 'ت']:
        return True
    if word2 == word1[:-1] and word1[-1] in ['ة', 'ت']:
        return True
    if word1[-2:] == "ات" and similar_number(word1[:-2], word2):
        return True
    if word2[-2:] == "ات" and similar_number(word2[:-2], word1):
        return True
    return False


def similar_definite(word1, word2):
    if word1 == word2[2:] and word2[:2] == 'ال':
        return True
    if word2 == word1[2:] and word1[:2] == 'ال':
        return True
    return False


def ta(word1, word2):
    if word1[:-1] == word2[:-1] and word1[-1] in ['ة', 'ت'] and word2[-1] in ['ة', 'ت']:
        return True
    return False


def check_suffixes(word1, word2, suffix1, suffix2):
    return (word1.endswith(suffix1) and word2.endswith(suffix2) and
            (word1[:len(word1) - len(suffix1)] == word2[:len(word2) - len(suffix2)] or
             ta(word1[:len(word1) - len(suffix1)], word2[:len(word2) - len(suffix2)])))


def similar_pronoun(word1, word2):
    if word1 == word2:
        return False
    for s1, s2 in product(suf3 + suf2 + suf1 + [""], repeat=2):
        if check_suffixes(word1, word2, s1, s2):
            return True
    return False


# def similar_pronoun(word1, word2):
#     if word1==word2:
#         return True
#     if word1[:-1]==word2[:-1] and word1[-1] in ['ة', 'ت'] and word2[-1] in ['ة', 'ت']:
#         return True
#     return False

def similar_chars(word1, word2):
    if len(word1) != len(word2):
        return False
    mismatch_found = False
    for i in range(len(word1)):
        if word1[i] != word2[i]:
            if mismatch_found:
                return False
            if word1[i] in ["ن", "ت", "ث"] and word2[i] in ["ن", "ت", "ث"]:
                mismatch_found = True
            elif word1[i] in ["ج", "خ", "ح"] and word2[i] in ["ج", "خ", "ح"]:
                mismatch_found = True
            elif word1[i] in ["ض", "ص"] and word2[i] in ["ض", "ص"]:
                mismatch_found = True
            elif word1[i] in ["ظ", "ط"] and word2[i] in ["ظ", "ط"]:
                mismatch_found = True
            elif word1[i] in ["د", "ذ"] and word2[i] in ["د", "ذ"]:
                mismatch_found = True
            elif word1[i] in ["غ", "ع"] and word2[i] in ["غ", "ع"]:
                mismatch_found = True
            elif word1[i] in ["ز", "ر"] and word2[i] in ["ز", "ر"]:
                mismatch_found = True
            elif word1[i] in ["ي", "ب"] and word2[i] in ["ي", "ب"]:
                mismatch_found = True
            else:
                return False
    return mismatch_found


def similar_pattern1(word1, word2):
    if pattern_recognizer(word1, word2, "فعيل", "افعل") or pattern_recognizer(word2, word1, "فعيل", "افعل"):
        return True
    if pattern_recognizer(word1, word2, "فعلى", "افعل") or pattern_recognizer(word2, word1, "فعلى", "افعل"):
        return True
    if pattern_recognizer(word1, word2, "فعيل", "فعلى") or pattern_recognizer(word2, word1, "فعيل", "فعلى"):
        return True
    if word1[0] == "و" and word2[0] == "و":
        return similar_pattern1(word1[1:], word2[1:])
    return False


def similar_pattern2(word1, word2):
    if pattern_recognizer(word1, word2, "فاعل", "افعل") or pattern_recognizer(word2, word1, "فاعل", "افعل"):
        return True
    if pattern_recognizer(word1, word2, "مفعل", "تفعيل") or pattern_recognizer(word2, word1, "مفعل", "تفعيل"):
        return True
    if word1[0] == "و" and word2[0] == "و":
        return similar_pattern2(word1[1:], word2[1:])
    return False


def get_score(name1, name2):
    st = ISRIStemmer()
    norm_name1 = st.norm(name1)
    norm_name2 = st.norm(name2)
    if matching(norm_name1, norm_name2):
        return 30, ["تطابق"]
    if matching_no_space(norm_name1, norm_name2):
        return 30, ["تطابق النطق"]
    if matching_set(norm_name1, norm_name2):
        return 30, ["تطابق مع تغيير الترتيب"]
    score = 0
    similarity_type = []
    name1_words = name1.split()
    name2_words = name2.split()
    if len(name1_words) == len(name2_words):
        for word1, word2 in zip(name1_words, name2_words):
            similar = False
            if word1 != word2:
                if similar_definite(word1, word2):
                    similar = True
                    if "تشابه: ال التعريف" not in similarity_type:
                        score += 30
                        similarity_type.append("تشابه: ال التعريف")
                if similar_chars(word1, word2):
                    similar = True
                    if "تطابق الرسم مع تغير حرف واحد" not in similarity_type:
                        score += 10
                        similarity_type.append("تطابق الرسم مع تغير حرف واحد")

                if similar_pronoun(word1, word2):
                    similar = True
                    if "تشابه: الضمائر" not in similarity_type:
                        score += 10
                        similarity_type.append("تشابه: الضمائر")
                word1_norm = st.pre32(word1)
                word2_norm = st.pre32(word2)
                word1_norm = st.norm(word1_norm)
                word2_norm = st.norm(word2_norm)
                # print(word1_norm)
                # print(word2_norm)
                if similar_number(word1_norm, word2_norm):
                    similar = True
                    if "تشابه: المثنى أو الجمع" not in similarity_type:
                        score += 10
                        similarity_type.append("تشابه: المثنى أو الجمع")
                if similar_gender(word1_norm, word2_norm):
                    similar = True
                    if "تشايه: التذكير والتأنيث" not in similarity_type:
                        score += 20
                        similarity_type.append("تشايه: التذكير والتأنيث")
                if similar_pattern1(word1_norm, word2_norm):
                    similar = True
                    if "تشابه: وزن فعيل/أفعل/فعلى" not in similarity_type:
                        score += 20
                        similarity_type.append("تشابه: وزن فعيل/أفعل/فعلى")
                if similar_pattern2(word1_norm, word2_norm):
                    similar = True
                    if "تشابه: وزن فاعل/أفعل أو تفعيل/مفعل" not in similarity_type:
                        score += 10
                        similarity_type.append("تشابه: وزن فاعل/أفعل أو تفعيل/مفعل")
                if not similar:
                    return 0, [""]
        if len(similarity_type) > 1:
            score -= 10 * len(similarity_type)
    elif len(name1_words) == len(name2_words) + 1:
        if name1_words[:-1] == name2_words and len(name2_words) > 1:
            return 30, ["تشابه على مستوى الاسم المر ّكب"]
        if name1_words[1:] == name2_words and len(name2_words) > 1:
            return 30, ["تشابه على مستوى الاسم المر ّكب"]
    elif len(name2_words) == len(name1_words) + 1:
        if name2_words[:-1] == name1_words and len(name1_words) > 1:
            return 30, ["تشابه على مستوى الاسم المر ّكب"]
        if name2_words[1:] == name1_words and len(name1_words) > 1:
            return 30, ["تشابه على مستوى الاسم المر ّكب"]
    return score, similarity_type

import tkinter as tk
# from tkinter import RIGHT, LEFT

# # Function to update the score and reasons in the GUI
# def update_score():
#     name1 = entry_name1.get()
#     name2 = entry_name2.get()
#     score, reasons_list = get_score(name1, name2)
#     reasons = ", ".join(reasons_list)  # Join the list into a single string
#     label_score_value.config(text=str(score))
#     label_reasons_value.config(text=reasons)

# # Create the main window
# root = tk.Tk()
# root.title("Score Calculator")

# # Set initial size
# root.geometry("500x300")

# # Configure the layout for right-to-left and make it expandable
# for i in range(5):
#     root.grid_rowconfigure(i, weight=1)
# root.grid_columnconfigure(0, weight=1)
# root.grid_columnconfigure(1, weight=1)

# # Input fields with right alignment
# label_name1 = tk.Label(root, text="الاسم الأول")
# label_name1.grid(row=0, column=1, sticky=tk.EW)
# entry_name1 = tk.Entry(root, justify=tk.RIGHT)
# entry_name1.grid(row=0, column=0, sticky=tk.EW)

# label_name2 = tk.Label(root, text="الاسم الثاني")
# label_name2.grid(row=1, column=1, sticky=tk.EW)
# entry_name2 = tk.Entry(root, justify=tk.RIGHT)
# entry_name2.grid(row=1, column=0, sticky=tk.EW)

# # Calculate button
# button_calculate = tk.Button(root, text="احسب", command=update_score)
# button_calculate.grid(row=2, column=0, columnspan=2, sticky=tk.EW)

# # Output fields
# label_score = tk.Label(root, text="الوزن")
# label_score.grid(row=3, column=1, sticky=tk.EW)
# label_score_value = tk.Label(root, text="")
# label_score_value.grid(row=3, column=0, sticky=tk.EW)

# label_reasons = tk.Label(root, text="الأسباب")
# label_reasons.grid(row=4, column=1, sticky=tk.EW)
# label_reasons_value = tk.Label(root, text="")
# label_reasons_value.grid(row=4, column=0, sticky=tk.EW)

# # # Start the GUI loop
# # root.mainloop()