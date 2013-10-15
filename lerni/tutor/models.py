# coding: utf-8

from django.db import models

from lerni.domain.models import Page

from bs4 import BeautifulSoup


class Tutor(models.Model):

    def get_formated_page(self, student):

        if student.level_learning == 'assistant':
            soup_content = BeautifulSoup(student.study_context.current_page.content_page)

            for span in soup_content.findAll('span'):
                new_tag = soup_content.new_tag("p")
                new_tag.string = span.getText()
                span.replaceWith(new_tag)

            student.study_context.current_page.content_page = str(soup_content)

            return student.study_context.current_page

        if student.level_learning == 'reactive':

            return student.study_context.current_page

        if student.level_learning == 'guide':
            pass

    def next_page(self, student):

        current_topic = student.study_context.current_topic
        total_pages = student.study_context.current_topic.get_total_pages()
        number_current_page = student.study_context.current_page.number

        if not number_current_page < total_pages:

            return 0

        next_page = Page.objects.filter(topic=current_topic).filter(number=(number_current_page + 1)).get()

        student.study_context.current_page = next_page
        student.study_context.save()
        student.save()

        return 1

    def previous_page(self, student):

        current_topic = student.study_context.current_topic
        number_current_page = student.study_context.current_page.number


        if not number_current_page > 1:

            return 0

        next_page = Page.objects.filter(topic=current_topic).filter(number=(number_current_page - 1)).get()

        student.study_context.current_page = next_page
        student.study_context.save()
        student.save()

        return 1
