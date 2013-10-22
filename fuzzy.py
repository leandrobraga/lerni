# coding: utf-8

from fuzzy import *
from numpy import linspace

def _myRamp(x):
        if x >= 8:
            return 0
        else:
            return Trapezoid(4.9, 6, 8, 8.1)(x)

class NivelAprendizagem(object):

    def fuzificacao(self, tempoExercicio, mediaExercicio, acertos, complexidade):

        tempoMuitoEficienteFuncaoFuzzy = DecreasingRamp(4, mediaExercicio - 0.1)
        tempoEficienteFuncaoFuzzy = Triangle(mediaExercicio - 1.1, mediaExercicio, mediaExercicio + 1.1)
        tempopoucoEficienteFuncaoFuzzy = IncreasingRamp(mediaExercicio, 50)

        self.muitoEficiente = tempoMuitoEficienteFuncaoFuzzy(tempoExercicio)
        self.eficiente = tempoEficienteFuncaoFuzzy(tempoExercicio)
        self.poucoEficiente = tempopoucoEficienteFuncaoFuzzy(tempoExercicio)

        acertoInsuficienteFuncaoFuzzy = DecreasingRamp(0, 3)
        acertoSatisfatorioFuncaoFuzzy = Triangle(1.9, 3, 4.1)
        acertoOtimoFuncaoFuzzy = IncreasingRamp(3.4, 5)

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

        InsuficienteFuncaoFuzzy = DecreasingRamp(0, 6)
        SatisfatorioFuncaoFuzzy = Triangle(4.9, 6, 8.1)
        OtimoFuncaoFuzzy = IncreasingRamp(7.9, 10)

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

if __name__ == '__main__':

    c = NivelAprendizagem()
    c.fuzificacao(0, 5, 5, 1)
    c.inferencia()
    for x,y in c.valoresInferencia.items():
        print x, y

    print c.defuzificacao()
