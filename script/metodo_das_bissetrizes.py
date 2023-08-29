from importacao_e_exportacao_de_dados import importando_coord_dos_poligonos_internos
from importacao_e_exportacao_de_dados import exportando_informacoes_internas
from importacao_e_exportacao_de_dados import importando_coord_dos_poligonos_externos
from importacao_e_exportacao_de_dados import exportando_informacoes_externas

from calculo_geometrico_euclidiano import inclinacoes_e_comprimentos_de_retas
from calculo_geometrico_euclidiano import angulos_de_um_poligono
from calculo_geometrico_euclidiano import retas_de_bissetrizes
from calculo_geometrico_euclidiano import ponto_de_interseccao_de_retas

from calculo_de_areas_especificas import lados_das_retas_das_bissetrizes
from calculo_de_areas_especificas import areas_e_centroides_de_interiores
from calculo_de_areas_especificas import areas_e_centroides_de_exteriores

# Método das bissetrizes para polígonos internos

def mdb_poligonos_internos(gdf_poligonos, lados, gdf_crs):

    # Separando coordenadas dos polígonos internos
    poligonos_internos = importando_coord_dos_poligonos_internos(gdf_poligonos.iterrows(), 
                                                                 lados)

    # Inclinação e comprimento de retas
    inclinacoes_dos_lados, comprimentos_dos_lados = inclinacoes_e_comprimentos_de_retas(poligonos_internos)

    # Lados das bissetrizes para poligonos maiores ou iguais a quatro lados
    lados_para_bissetrizes = lados_das_retas_das_bissetrizes(comprimentos_dos_lados)

    # Ângulos
    angulos_dos_poligonos_internos = angulos_de_um_poligono(inclinacoes_dos_lados)[0]

    # Retas das bissetrizes
    coord_das_retas_das_bissetrizes = retas_de_bissetrizes(poligonos_internos, 
                                                           angulos_dos_poligonos_internos)

    # Pontos de intersecção entre retas das bissetrizes
    coord_dos_pontos_das_bissetrizes = ponto_de_interseccao_de_retas(poligonos_internos, 
                                                                     coord_das_retas_das_bissetrizes, 
                                                                     lados_para_bissetrizes)

    # Áreas e centroides dos polígonos internos
    areas_dos_poligonos_internos, centroides_dos_poligonos_internos = areas_e_centroides_de_interiores(poligonos_internos, 
                                                                                                       coord_dos_pontos_das_bissetrizes, 
                                                                                                       lados_para_bissetrizes)

    # Organizando dados para shapefile
    gdf_bissetrizes, gdf_areas = exportando_informacoes_internas(poligonos_internos, 
                                                                 coord_dos_pontos_das_bissetrizes, 
                                                                 lados_para_bissetrizes, 
                                                                 centroides_dos_poligonos_internos, 
                                                                 areas_dos_poligonos_internos, 
                                                                 gdf_crs)
    
    return gdf_bissetrizes, gdf_areas

def mdb_poligonos_externos(gdf_poligonos, gdf_pontos, lados, gdf_crs):
    
    # Separando coordenadas dos polígonos internos
    poligonos_internos = importando_coord_dos_poligonos_internos(gdf_poligonos.iterrows(), 
                                                                 lados)
    
    # Separando coordenadas dos pontos externos
    pontos_externos = importando_coord_dos_poligonos_externos(gdf_pontos.iterrows())

    # Áreas e centroides dos polígonos externos
    areas_dos_poligonos_externos, centroides_dos_poligonos_externos, coord_exteriores = areas_e_centroides_de_exteriores(poligonos_internos, 
                                                                                                                         pontos_externos)
    
    # Organizando dados para shapefile
    gdf_retas, gdf_areas = exportando_informacoes_externas(coord_exteriores, 
                                                           centroides_dos_poligonos_externos, 
                                                           areas_dos_poligonos_externos, 
                                                           gdf_crs)
    
    return gdf_retas, gdf_areas
