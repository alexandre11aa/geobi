import math

from sympy import symbols, Eq, solve

# Inclinação e comprimento de retas

def inclinacoes_e_comprimentos_de_retas(poligonos):

    inclinacoes = []
    comprimentos = []

    for i in range(len(poligonos)):

        # Lista que representa um polígono
        inclinacoes.append([])
        comprimentos.append([])

        for j in range(len(poligonos[i]) - 1):

            # Cálculo das inclinações do polígono pela equação: m = (y2 - y1) / (x2 - x1)     
            if (poligonos[i][j + 1][1] == poligonos[i][j][1]) or (poligonos[i][j + 1][0] == poligonos[i][j][0]):
                inclinacoes[i].append(0)

            else:    
                inclinacoes[i].append( (poligonos[i][j + 1][1] - poligonos[i][j][1]) / 
                                       (poligonos[i][j + 1][0] - poligonos[i][j][0]) )
 
            # Cálculo dos comprimentos das retas do polígono pela equação: d = [(x2 - x1)² + (y2 - y1)²]^(1/2)
            comprimentos[i].append(((poligonos[i][j + 1][1] - poligonos[i][j][1])**2 + (poligonos[i][j + 1][0] - poligonos[i][j][0])**2)**(1/2))

        # Adicionando primeira inclinação à lista para facilitar cálculo do ângulo dos vértices
        inclinacoes[i].append(inclinacoes[i][0])
        
    return inclinacoes, comprimentos

# Ângulos internos de polígonos

def angulos_de_um_poligono(inclinacoes):

    angulos_grd = []
    angulos_rad = []

    for i in range(len(inclinacoes)):

        # Lista que representa um polígono
        angulos_grd.append([])
        angulos_rad.append([])

        for j in range(len(inclinacoes[i]) - 1):

            # Cálculo dos ângulos dos vertices do polígono em radianos: θ = arctan{(180 / π) * [(m2 - m1) / (1 + m2 * m1)}
            angulo = (180 / math.pi) * math.atan((inclinacoes[i][j + 1] - inclinacoes[i][j]) / (1 + inclinacoes[i][j + 1] * inclinacoes[i][j]))

            if angulo < 0:
                angulo += 180

            angulos_grd[i].append(angulo)

            # Cálculo dos ângulos dos vertices do polígono em radianos: θ° * π / 180
            angulos_rad[i].append((math.pi / 180) * angulo)

        angulos_grd[i].insert(0, angulos_grd[i][-1])
        angulos_rad[i].insert(0, angulos_rad[i][-1])
        
    return angulos_grd, angulos_rad

# Rotação de reta de polígono regular ao ângulo da bissetriz de seu ponto inicial

def retas_de_bissetrizes(poligonos, angulos_grd):

    '''
    O cálculo da reta da bissetriz é feita da seguinte forma: O quadrilatero possui os pontos A, B, C 
    e D. Cada ponto possui um ângulo. Para encontrar a reta da bissetriz do ponto A, a reta AB é rota
    cionada em metade do grau do ângulo do vértice A no sentido horário. O ponto A se mantém fixo e o
    ponto B será rotacionado. Daí então será calculada a reta da bissetriz. A reta das bissetrizes do
    s outros pontos serão calculados da mesma forma.
    '''

    bissetrizes = []
    
    for i in range(len(poligonos)):
        bissetrizes.append([])

        for j in range(len(angulos_grd[i]) - 1):

            # Ângulo inverso, para calcular bissetriz da reta pelo sentido horário
            angulo_inverso = - math.radians(angulos_grd[i][j] / 2)  # Ângulo de rotação em radianos

            # Vetor da reta da bissetriz
            vetor = (poligonos[i][j+1][0] - poligonos[i][j][0], poligonos[i][j+1][1] - poligonos[i][j][1])

            # Calculando ponto que traça reta da bissetriz
            delta_x_rot = vetor[0] * math.cos(angulo_inverso) - vetor[1] * math.sin(angulo_inverso)
            delta_y_rot = vetor[0] * math.sin(angulo_inverso) + vetor[1] * math.cos(angulo_inverso)

            # Extraindo as coordenadas da reta da bissetriz
            bissetrizes[i].append((poligonos[i][j][0] + delta_x_rot, poligonos[i][j][1] + delta_y_rot))

        bissetrizes[i].append(bissetrizes[i][0])

    return bissetrizes

# Ponto de intersecção entre duas retas

def ponto_de_interseccao_de_retas(poligonos, bissetrizes, lados_das_retas):

    # Intersecções das retas com menores distâncias entre si

    pontos_de_interseccao = []

    for i in range(len(poligonos)):
        pontos_de_interseccao.append([])
        
        if len(poligonos[i]) == 4:
            retas_que_se_tocam = 1
        else:
            retas_que_se_tocam = 2
            
        for j in range(retas_que_se_tocam): 
            
            if len(poligonos[i]) == 4:
                ponteiro = j
            else:
                ponteiro = lados_das_retas[i][j]

            # Definindo as variáveis simbólicas
            x, y = symbols('x y')

            # Definindo as equações das retas              
            p1r1 = poligonos[i][ponteiro]
            p2r1 = bissetrizes[i][ponteiro]

            p1r2 = poligonos[i][ponteiro+1]
            p2r2 = bissetrizes[i][ponteiro+1]

            equacao1 = Eq(y - (p2r1[1] - p1r1[1]) / (p2r1[0] - p1r1[0]) * x, p1r1[1] - (p2r1[1] - p1r1[1]) / (p2r1[0] - p1r1[0]) * p1r1[0])
            equacao2 = Eq(y - (p2r2[1] - p1r2[1]) / (p2r2[0] - p1r2[0]) * x, p1r2[1] - (p2r2[1] - p1r2[1]) / (p2r2[0] - p1r2[0]) * p1r2[0])

            # Resolvendo o sistema de equações para encontrar o ponto de intersecção
            ponto_de_interseccao = solve((equacao1, equacao2), (x, y))

            # Extraindo as coordenadas do ponto de intersecção
            pontos_de_interseccao[i].append((ponto_de_interseccao[x], ponto_de_interseccao[y]))

    return pontos_de_interseccao
