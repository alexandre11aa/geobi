import math
import numpy as np

from scipy.spatial import cKDTree
from shapely.geometry import Polygon, Point

# Áreas interiores pelo método das bissetrizes

def areas_e_centroides_de_interiores(poligonos, pontos_de_interseccao, lados_das_retas):
    areas_dos_poligonos = []

    coordenada_das_areas_dos_poligonos = []

    for i in range(len(poligonos)):

        for j in range(len(poligonos[i])-1):

            # Área dos polígonos de três vértices
            if len(poligonos[i]) == 4:               
                areas_dos_poligonos.append(str(Polygon((poligonos[i][j], 
                                                        poligonos[i][j+1], 
                                                        pontos_de_interseccao[i][0])).area))
                
                coordenada_das_areas_dos_poligonos.append(Polygon((poligonos[i][j], 
                                                                   poligonos[i][j+1], 
                                                                   pontos_de_interseccao[i][0])).centroid)
                
            # Área dos polígonos de quatro vértices
            elif len(poligonos[i]) == 5:

                if (j == lados_das_retas[i][0]):                    
                    areas_dos_poligonos.append(str(Polygon((poligonos[i][j], 
                                                            poligonos[i][j+1], 
                                                            pontos_de_interseccao[i][0])).area))
                    
                    coordenada_das_areas_dos_poligonos.append(Polygon((poligonos[i][j], 
                                                                       poligonos[i][j+1], 
                                                                       pontos_de_interseccao[i][0])).centroid)

                elif (j == lados_das_retas[i][1]):
                    areas_dos_poligonos.append(str(Polygon((poligonos[i][j], 
                                                            poligonos[i][j+1], 
                                                            pontos_de_interseccao[i][1])).area))
                    
                    coordenada_das_areas_dos_poligonos.append(Polygon((poligonos[i][j], 
                                                                       poligonos[i][j+1], 
                                                                       pontos_de_interseccao[i][1])).centroid)

                else:
                    coordenadas, centroide = vertices_de_quadrilateros((poligonos[i][j], 
                                                                        poligonos[i][j+1], 
                                                                        pontos_de_interseccao[i][1], 
                                                                        pontos_de_interseccao[i][0]))
                    
                    areas_dos_poligonos.append(str(Polygon(coordenadas[0]).area + Polygon(coordenadas[1]).area))

                    coordenada_das_areas_dos_poligonos.append(Point(centroide))
                    
            # Área dos polígonos acima de quatro vértices
            else:
                areas_dos_poligonos.append(None)
                coordenada_das_areas_dos_poligonos.append((None,None))
            
    return areas_dos_poligonos, coordenada_das_areas_dos_poligonos

# Áreas exteriores pelo método das bissetrizes

def areas_e_centroides_de_exteriores(poligonos, pontos_da_rua):

    tree = cKDTree(np.array(pontos_da_rua))

    linhas_exteriores, linhas_das_areas = [[],[]]

    for i in range(len(poligonos)):
        linhas_das_areas.append([])
        for j in range(len(poligonos[i])-1):
            coord_do_ponto = (poligonos[i][j], list(np.array(pontos_da_rua)[tree.query(poligonos[i][j])[1]]))
            
            linhas_exteriores.append(coord_do_ponto)
            linhas_das_areas[i].append(coord_do_ponto)

    areas_dos_poligonos, coordenada_das_areas_dos_poligonos = [[],[]]
            
    for i in range(len(linhas_das_areas)):
        for j in range(len(linhas_das_areas[i])):
            
            if j == len(linhas_das_areas[i]) - 1:
                ponteiro = 0
            else:
                ponteiro = j + 1

            linhas_exteriores.append((linhas_das_areas[i][j][1], linhas_das_areas[i][ponteiro][1]))
            
            coord_do_poligono = (linhas_das_areas[i][j][0], 
                                linhas_das_areas[i][ponteiro][0],
                                tuple(linhas_das_areas[i][ponteiro][1]),
                                tuple(linhas_das_areas[i][j][1]))
            
            areas_dos_poligonos.append(str(Polygon(coord_do_poligono).area))
            coordenada_das_areas_dos_poligonos.append(Polygon(coord_do_poligono).centroid)
                                                      
    return areas_dos_poligonos, coordenada_das_areas_dos_poligonos, linhas_exteriores

# Lados das bissetrizes para poligonos iguais ou com mais de quatro vértices

def lados_das_retas_das_bissetrizes(comprimentos):

    lados_das_retas = []

    for i in range(len(comprimentos)):
        
        # Menores faces do polígono
                
        # Polígono de 4 lados
        if len(comprimentos[i]) == 4:
            
            if (comprimentos[i][0] + comprimentos[i][2]) < (comprimentos[i][1] + comprimentos[i][3]):
                lados_das_retas.append((0, 2))

            else:
                lados_das_retas.append((1, 3))
                
        # Polígono de 3 lados                
        elif len(comprimentos[i]) == 3:
            lados_das_retas.append((None, None))
        
        # Polígono maior que 4 lados 
        else:
            
            soma_de_comprimentos, ponteiro = [[],2]
            
            for j in range(len(comprimentos[i])):
                                
                if ponteiro == len(comprimentos[i]):
                    ponteiro = 0
                
                soma_de_comprimentos.append([comprimentos[i][j] + comprimentos[i][ponteiro], (j, ponteiro)])
                
                ponteiro += 1
                
            soma_de_comprimentos.remove(min(soma_de_comprimentos, key=lambda lista: lista[0]))                        
            lados_das_retas.append((min(soma_de_comprimentos, key=lambda lista: lista[0]))[1])
                                               
    return lados_das_retas

# Ordenando vértices de polígonos com quatro lados para evitar cruzamento de linhas durante calculo de áreas

def vertices_de_quadrilateros(vertices):

    centroide_x = sum(v[0] for v in vertices) / len(vertices)
    centroide_y = sum(v[1] for v in vertices) / len(vertices)

    vertices_ordenados = sorted(vertices, key=lambda v: math.atan2(v[1] - centroide_y, v[0] - centroide_x))

    coordenadas = ([vertices_ordenados[0], vertices_ordenados[1], vertices_ordenados[2]],
                   [vertices_ordenados[0], vertices_ordenados[2], vertices_ordenados[3]])
    
    return coordenadas, (centroide_x, centroide_y)
