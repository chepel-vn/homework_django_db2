from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Scope, ArticleScope
import re


class MembershipInlineFormset(BaseInlineFormSet):
    def clean(self):
        count_main = 0
        for form in self.forms:
            # Check that only one scope is main, remain scopes must be not main
            is_main = form.cleaned_data.get('is_main')
            if is_main is None:
                continue
            if is_main:
                count_main += 1

            # Check that no double records
            scope_find = form.cleaned_data.get('scope')
            if scope_find is None:
                continue

            txt = ''
            for form_2 in self.forms:
                scope = form_2.cleaned_data.get('scope')
                if scope is not None:
                    txt += scope.title

            pattern = scope_find.title
            found = re.findall(pattern, txt)
            if len(found) > 1:
                count_main = -1
                break

        msg = ''
        if count_main < 0:
            error = True
            msg = 'Уберите задвоение разделов.'
        elif count_main == 0:
            error = True
            msg = 'Укажите основной раздел.'
        elif count_main > 1:
            error = True
            msg = 'Основным может быть только один раздел.'
        else:
            error = False

        if error:
            raise ValidationError(msg)

        return super().clean()  # вызываем базовый код переопределяемого метода


class MembershipInline(admin.TabularInline):
    model = ArticleScope
    formset = MembershipInlineFormset


class ArticleAdmin(admin.ModelAdmin):
    inlines = [MembershipInline]


class ScopeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Article, ArticleAdmin)
admin.site.register(Scope, ScopeAdmin)

