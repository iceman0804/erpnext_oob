import frappe
from frappe import translate
from frappe.translate import get_translation_dict_from_file


old_get_user_translations = translate.get_user_translations
def get_user_translations(lang):
    if not frappe.db:
        frappe.connect()
    out = frappe.cache().hget('lang_user_translations', lang)
    if not out:
        user_translation = old_get_user_translations(lang)
        languages = ['zh','zh-TW']
        if lang in languages  and frappe.translate.get_user_lang() in languages:
            app = 'erpnext_oob'
            path =frappe.get_app_path(app, "translations",f"{lang}_global.csv")
            out = get_translation_dict_from_file(path, lang, app)
            #用户翻译优先级最高
            out.update(user_translation)
        else:
            out = user_translation
        frappe.cache().hset('lang_user_translations', lang, out)

    return out

translate.get_user_translations = get_user_translations    