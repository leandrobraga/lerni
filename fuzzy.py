# coding: utf-8

from fuzzy import *
from numpy import linspace

def _myRamp(x):
        if x >= 8:
            return 0
        else:
            return Trapezoid(4.9, 6, 8, 8.1)(x)

class NivelAprendizagem(object):

    def fuzificacao(self, teorico, pratico):

        insuficienteFuncaoFuzzy = DecreasingRamp(0, 6)
        satisfatorioFuncaoFuzzy = Triangle(4.9, 6, 8.1)
        otimoFuncaoFuzzy = IncreasingRamp(7.9, 10)

        self.insuficienteTeorico = insuficienteFuncaoFuzzy(teorico)
        self.satisfatorioTeorico = satisfatorioFuncaoFuzzy(teorico)
        self.otimoTeorico = otimoFuncaoFuzzy(teorico)

        print self.insuficienteTeorico, self.satisfatorioTeorico, self.otimoTeorico

        self.insuficientePratico = insuficienteFuncaoFuzzy(pratico)
        self.satisfatorioPratico = satisfatorioFuncaoFuzzy(pratico)
        self.otimoPratico = otimoFuncaoFuzzy(pratico)

        print self.insuficientePratico, self.satisfatorioPratico, self.otimoPratico

        self.rangeTeorico = linspace(0, 11.85)

        insuficiente = DecreasingRamp(0, 6)
        satisfatorio = Triangle(4.9, 6, 8.1)
        otimo = IncreasingRamp(7.9, 10)

        self.insuficiente = insuficiente(self.rangeTeorico)
        self.satisfatorio = satisfatorio(self.rangeTeorico)
        self.otimo = otimo(self.rangeTeorico)

    def inferencia(self):

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

            self.valoresInferencia[u'otimo'] += self.otimoTeorico & self.otimoPratico



    def defuzificacao(self):

        saida = self.insuficiente & self.valoresInferencia['insuficiente']\
        | self.satisfatorio & self.valoresInferencia[u'satisfatório'] \
        | self.otimo & self.valoresInferencia[u'ótimo']

        self.notaFinal = Centroid(saida, self.rangeTeorico)

        return self.notaFinal


if __name__ == '__main__':

    c = NivelAprendizagem()
    c.fuzificacao(6.85, 8.36)
    c.inferencia()
    for x,y in c.valoresInferencia.items():
        print x, y

    print c.defuzificacao()
