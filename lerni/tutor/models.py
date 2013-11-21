# coding: utf-8

from django.db import models


from lerni.domain.models import Page
from lerni.domain.models import Exercise

from fuzzy import *
from numpy import linspace
from bs4 import BeautifulSoup
from math import ceil


class Tutor(models.Model):

    def get_formated_page(self, student):

        soup_content = BeautifulSoup(student.study_context.current_page.content_page)

        if student.level_learning == 'assistant':

            for span in soup_content.findAll('span'):
                new_tag = soup_content.new_tag("p")
                new_tag.string = span.getText()
                span.replaceWith(new_tag)

            student.study_context.current_page.content_page = str(soup_content)

            return student.study_context.current_page

        if student.level_learning == 'reactive':

            return student.study_context.current_page

        if student.level_learning == 'guide':

            student.study_context.current_page.content_page = str(soup_content)

            return student.study_context.current_page

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

    def fuziffication_final(self, teorico, pratico):

        insuficienteFuncaoFuzzy = DecreasingRamp(0, 6)
        satisfatorioFuncaoFuzzy = Triangle(4.9, 6, 8.1)
        otimoFuncaoFuzzy = IncreasingRamp(7.9, 10)

        self.insuficienteTeorico = insuficienteFuncaoFuzzy(teorico)
        self.satisfatorioTeorico = satisfatorioFuncaoFuzzy(teorico)
        self.otimoTeorico = otimoFuncaoFuzzy(teorico)

        self.insuficientePratico = insuficienteFuncaoFuzzy(pratico)
        self.satisfatorioPratico = satisfatorioFuncaoFuzzy(pratico)
        self.otimoPratico = otimoFuncaoFuzzy(pratico)

        self.rangeTeorico = linspace(0, 11.85)

        insuficiente = DecreasingRamp(0, 6)
        satisfatorio = Triangle(4.9, 6, 8.1)
        otimo = IncreasingRamp(7.9, 10)

        self.insuficiente = insuficiente(self.rangeTeorico)
        self.satisfatorio = satisfatorio(self.rangeTeorico)
        self.otimo = otimo(self.rangeTeorico)

    def inferencia_final(self):

        self.valoresInferencia = {u'insuficiente': FuzzySet(0),
        u'satisfatório': FuzzySet(0), u'ótimo': FuzzySet(0)}

        if self.insuficienteTeorico & self.insuficientePratico:

            self.valoresInferencia[u'insuficiente'] += self.insuficienteTeorico & self.insuficientePratico

        if self.insuficienteTeorico & self.satisfatorioPratico:

            self.valoresInferencia[u'insuficiente'] += self.insuficienteTeorico & self.satisfatorioPratico

        if self.insuficienteTeorico & self.otimoPratico:

            self.valoresInferencia[u'insuficiente'] += self.insuficienteTeorico & self.otimoPratico

        if self.satisfatorioTeorico & self.insuficientePratico:

            self.valoresInferencia[u'insuficiente'] += self.satisfatorioTeorico & self.insuficientePratico

        if self.satisfatorioTeorico & self.satisfatorioPratico:

            self.valoresInferencia[u'satisfatório'] += self.satisfatorioTeorico & self.satisfatorioPratico

        if self.satisfatorioTeorico & self.otimoPratico:

            self.valoresInferencia[u'ótimo'] += self.satisfatorioTeorico & self.otimoPratico

        if self.otimoTeorico & self.insuficientePratico:

            self.valoresInferencia[u'insuficiente'] += self.otimoTeorico & self.insuficientePratico

        if self.otimoTeorico & self.satisfatorioPratico:

            self.valoresInferencia[u'satisfatório'] += self.otimoTeorico & self.satisfatorioPratico

        if self.otimoTeorico & self.otimoPratico:

            self.valoresInferencia[u'ótimo'] += self.otimoTeorico & self.otimoPratico

        return self.valoresInferencia

    def defuzificacao_final(self):

        saida = self.insuficiente & self.valoresInferencia['insuficiente']\
        | self.satisfatorio & self.valoresInferencia[u'satisfatório'] \
        | self.otimo & self.valoresInferencia[u'ótimo']

        self.notaFinal = Centroid(saida, self.rangeTeorico)

        return round(self.notaFinal, 2)

    def theoretical_fuzzification(self, tempoExercicio, mediaExercicio, acertos, complexidade, topic):

        tempoMuitoEficienteFuncaoFuzzy = DecreasingRamp(0, mediaExercicio - 0.1)
        tempoEficienteFuncaoFuzzy = Triangle(mediaExercicio - 1.1, mediaExercicio, mediaExercicio + 1.1)
        tempopoucoEficienteFuncaoFuzzy = IncreasingRamp(mediaExercicio, 50)

        self.muitoEficiente = tempoMuitoEficienteFuncaoFuzzy(tempoExercicio)
        self.eficiente = tempoEficienteFuncaoFuzzy(tempoExercicio)
        self.poucoEficiente = tempopoucoEficienteFuncaoFuzzy(tempoExercicio)

        center = ceil(topic.number_question_theoretical/2.)
        acertoInsuficienteFuncaoFuzzy = DecreasingRamp(0, center)
        acertoSatisfatorioFuncaoFuzzy = Triangle((center-1.1), center, (center+1.1))
        acertoOtimoFuncaoFuzzy = IncreasingRamp((center+1.4), topic.number_question_theoretical)

        self.acertoInsuficiente = acertoInsuficienteFuncaoFuzzy(acertos)
        self.acertoSatisfatorio = acertoSatisfatorioFuncaoFuzzy(acertos)
        self.acertoOtimo = acertoOtimoFuncaoFuzzy(acertos)

        complexidadeFacilFuncaoFuzzy = DecreasingRamp(1, 2)
        complexidadeMedioFuncaoFuzzy = Triangle(0.9, 2, 3.1)
        complexidadeDificilFuncaoFuzzy = IncreasingRamp(1.9, 3)

        self.complexidadeFacil = complexidadeFacilFuncaoFuzzy(complexidade)
        self.complexidadeMedio = complexidadeMedioFuncaoFuzzy(complexidade)
        self.complexidadeDificil = complexidadeDificilFuncaoFuzzy(complexidade)

        self.rangeTeorico = linspace(0, 11.22)

        InsuficienteFuncaoFuzzy = DecreasingRamp(0, 5)
        SatisfatorioFuncaoFuzzy = Triangle(3.9, 5, 7.1)
        OtimoFuncaoFuzzy = IncreasingRamp(6.9, 10)

        self.insuficiente = InsuficienteFuncaoFuzzy(self.rangeTeorico)
        self.satisfatorio = SatisfatorioFuncaoFuzzy(self.rangeTeorico)
        self.otimo = OtimoFuncaoFuzzy(self.rangeTeorico)

    def pratical_fuzzification(self, tempoExercicio, mediaExercicio, acertos, complexidade, topic):

        tempoMuitoEficienteFuncaoFuzzy = DecreasingRamp(0, mediaExercicio - 0.1)
        tempoEficienteFuncaoFuzzy = Triangle(mediaExercicio - 1.1, mediaExercicio, mediaExercicio + 1.1)
        tempopoucoEficienteFuncaoFuzzy = IncreasingRamp(mediaExercicio, 30)

        self.muitoEficiente = tempoMuitoEficienteFuncaoFuzzy(tempoExercicio)
        self.eficiente = tempoEficienteFuncaoFuzzy(tempoExercicio)
        self.poucoEficiente = tempopoucoEficienteFuncaoFuzzy(tempoExercicio)
        
        center = ceil(topic.number_question_pratical/2.)
        acertoInsuficienteFuncaoFuzzy = DecreasingRamp(0, center)
        acertoSatisfatorioFuncaoFuzzy = Triangle((center-1.1), center, (center+1.1))
        acertoOtimoFuncaoFuzzy = IncreasingRamp((center+1.4), topic.number_question_pratical)

        self.acertoInsuficiente = acertoInsuficienteFuncaoFuzzy(acertos)
        self.acertoSatisfatorio = acertoSatisfatorioFuncaoFuzzy(acertos)
        self.acertoOtimo = acertoOtimoFuncaoFuzzy(acertos)

        complexidadeFacilFuncaoFuzzy = DecreasingRamp(1, 2)
        complexidadeMedioFuncaoFuzzy = Triangle(0.9, 2, 3.1)
        complexidadeDificilFuncaoFuzzy = IncreasingRamp(1.9, 3)

        self.complexidadeFacil = complexidadeFacilFuncaoFuzzy(complexidade)
        self.complexidadeMedio = complexidadeMedioFuncaoFuzzy(complexidade)
        self.complexidadeDificil = complexidadeDificilFuncaoFuzzy(complexidade)

        self.rangeTeorico = linspace(0, 11.85)

        InsuficienteFuncaoFuzzy = DecreasingRamp(0, 5)
        SatisfatorioFuncaoFuzzy = Triangle(3.9, 5, 7.1)
        OtimoFuncaoFuzzy = IncreasingRamp(6.9, 10)

        self.insuficiente = InsuficienteFuncaoFuzzy(self.rangeTeorico)
        self.satisfatorio = SatisfatorioFuncaoFuzzy(self.rangeTeorico)
        self.otimo = OtimoFuncaoFuzzy(self.rangeTeorico)

    def inferencia(self):

        self.valoresInferencia = {'insuficiente': FuzzySet(0),
        u'satisfatório': FuzzySet(0), u'ótimo': FuzzySet(0)}

        if self.poucoEficiente & self.acertoInsuficiente & self.complexidadeFacil:

            self.valoresInferencia['insuficiente'] += \
            self.poucoEficiente & self.acertoInsuficiente & self.complexidadeFacil

        if self.poucoEficiente & self.acertoInsuficiente & self.complexidadeMedio:

            self.valoresInferencia['insuficiente'] += \
            self.poucoEficiente & self.acertoInsuficiente & self.complexidadeMedio

        if self.poucoEficiente & self.acertoInsuficiente & self.complexidadeDificil:

            self.valoresInferencia['insuficiente'] += \
            self.poucoEficiente & self.acertoInsuficiente & self.complexidadeDificil

        if self.poucoEficiente & self.acertoSatisfatorio & self.complexidadeFacil:

            self.valoresInferencia['insuficiente'] += \
            self.poucoEficiente & self.acertoSatisfatorio & self.complexidadeFacil

        if self.poucoEficiente & self.acertoSatisfatorio & self.complexidadeMedio:

            self.valoresInferencia[u'satisfatório'] += \
            self.poucoEficiente & self.acertoSatisfatorio & self.complexidadeMedio

        if self.poucoEficiente & self.acertoSatisfatorio & self.complexidadeDificil:

            self.valoresInferencia[u'satisfatório'] += \
            self.poucoEficiente & self.acertoSatisfatorio & self.complexidadeDificil

        if self.poucoEficiente & self.acertoOtimo & self.complexidadeFacil:

            self.valoresInferencia[u'satisfatório'] += \
            self.poucoEficiente & self.acertoOtimo & self.complexidadeFacil

        if self.poucoEficiente & self.acertoOtimo & self.complexidadeMedio:

            self.valoresInferencia[u'satisfatório'] += \
            self.poucoEficiente & self.acertoOtimo & self.complexidadeMedio

        if self.poucoEficiente & self.acertoOtimo & self.complexidadeDificil:

            self.valoresInferencia[u'satisfatório'] += \
            self.poucoEficiente & self.acertoOtimo & self.complexidadeDificil

        if self.eficiente & self.acertoInsuficiente & self.complexidadeFacil:

            self.valoresInferencia['insuficiente'] += \
            self.eficiente & self.acertoInsuficiente & self.complexidadeFacil

        if self.eficiente & self.acertoInsuficiente & self.complexidadeMedio:

            self.valoresInferencia['insuficiente'] += \
            self.eficiente & self.acertoInsuficiente & self.complexidadeMedio

        if self.eficiente & self.acertoInsuficiente & self.complexidadeDificil:

            self.valoresInferencia['insuficiente'] += \
            self.eficiente & self.acertoInsuficiente & self.complexidadeDificil

        if self.eficiente & self.acertoSatisfatorio & self.complexidadeFacil:

            self.valoresInferencia[u'satisfatório'] += \
            self.eficiente & self.acertoSatisfatorio & self.complexidadeFacil

        if self.eficiente & self.acertoSatisfatorio & self.complexidadeMedio:

            self.valoresInferencia[u'satisfatório'] += \
            self.eficiente & self.acertoSatisfatorio & self.complexidadeMedio

        if self.eficiente & self.acertoSatisfatorio & self.complexidadeDificil:

            self.valoresInferencia[u'ótimo'] += \
            self.eficiente & self.acertoSatisfatorio & self.complexidadeDificil

        if self.eficiente & self.acertoOtimo & self.complexidadeFacil:

            self.valoresInferencia[u'satisfatório'] += \
            self.eficiente & self.acertoOtimo & self.complexidadeFacil

        if self.eficiente & self.acertoOtimo & self.complexidadeMedio:

            self.valoresInferencia[u'ótimo'] += \
            self.eficiente & self.acertoOtimo & self.complexidadeMedio

        if self.eficiente & self.acertoOtimo & self.complexidadeDificil:

            self.valoresInferencia[u'ótimo'] += \
            self.eficiente & self.acertoOtimo & self.complexidadeDificil

        if self.muitoEficiente & self.acertoInsuficiente & self.complexidadeFacil:

            self.valoresInferencia[u'insuficiente'] += \
            self.muitoEficiente & self.acertoInsuficiente & self.complexidadeFacil

        if self.muitoEficiente & self.acertoInsuficiente & self.complexidadeMedio:

            self.valoresInferencia['insuficiente'] += \
            self.muitoEficiente & self.acertoInsuficiente & self.complexidadeMedio

        if self.muitoEficiente & self.acertoInsuficiente & self.complexidadeDificil:

            self.valoresInferencia['insuficiente'] += \
            self.muitoEficiente & self.acertoInsuficiente & self.complexidadeDificil

        if self.muitoEficiente & self.acertoSatisfatorio & self.complexidadeFacil:

            self.valoresInferencia[u'satisfatório'] += \
            self.muitoEficiente & self.acertoSatisfatorio & self.complexidadeFacil

        if self.muitoEficiente & self.acertoSatisfatorio & self.complexidadeMedio:

            self.valoresInferencia[u'ótimo'] += \
            self.muitoEficiente & self.acertoSatisfatorio & self.complexidadeMedio

        if self.muitoEficiente & self.acertoSatisfatorio & self.complexidadeDificil:

            self.valoresInferencia[u'ótimo'] += \
            self.muitoEficiente & self.acertoSatisfatorio & self.complexidadeDificil

        if self.muitoEficiente & self.acertoOtimo & self.complexidadeFacil:

            self.valoresInferencia[u'satisfatório'] += \
            self.muitoEficiente & self.acertoOtimo & self.complexidadeFacil

        if self.muitoEficiente & self.acertoOtimo & self.complexidadeMedio:

            self.valoresInferencia[u'ótimo'] += \
            self.muitoEficiente & self.acertoOtimo & self.complexidadeMedio

        if self.muitoEficiente & self.acertoOtimo & self.complexidadeDificil:

            self.valoresInferencia[u'ótimo'] += \
            self.muitoEficiente & self.acertoOtimo & self.complexidadeDificil

        return self.valoresInferencia

    def defuzificacao(self):

        saida = self.insuficiente & self.valoresInferencia['insuficiente']\
        | self.satisfatorio & self.valoresInferencia[u'satisfatório'] \
        | self.otimo & self.valoresInferencia[u'ótimo']

        self.notaFinal = Centroid(saida, self.rangeTeorico)

        return round(self.notaFinal, 2)