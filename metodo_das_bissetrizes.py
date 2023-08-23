import time
import geopandas as gpd

from shapely.geometry import LineString

from funcoes_geometricas_euclidianas import inclinacoes_e_comprimentos_de_retas
from funcoes_geometricas_euclidianas import lados_das_retas_das_bissetrizes
from funcoes_geometricas_euclidianas import angulos_de_um_poligono
from funcoes_geometricas_euclidianas import retas_de_bissetrizes
from funcoes_geometricas_euclidianas import ponto_de_interseccao_de_retas

# Início da geração de nova shapefile
inicio = time.time()

# Carrega o arquivo shapefile
gdf = gpd.read_file('C:\\Users\\Estrela\\Desktop\\quadras_shapefile\\quadras.shp')

# Reprojeta as geometrias para um CRS projetado
gdf = gdf.to_crs(gdf.crs)

# Itera sobre as linhas do GeoDataFrame e imprime a área e as coordenadas dos vértices de cada polígono

for index, row in gdf.iterrows():
    
    # Usando o índice da linha como ID
    polygon_id = index
    
    # Obtendo área do polígono
    polygon_area = row['geometry'].area
    
    # Obtém as coordenadas dos vértices
    polygon_vertices = row['geometry'].exterior.coords

# Separando polígonos de 4 lados
  
gdf_4 = []

for i, row in gdf.iterrows():
    
    # Verifique se a geometria é um polígono com quatro coordenadas (vértices)
    if row['geometry'].geom_type == 'Polygon' and len(row['geometry'].exterior.coords) == 5:
        gdf_4.append(row)

# Separando vértices dos polígonos   

poligonos = []
        
for i, coluna in enumerate(gdf_4):
    
    # Polígonos
    poligonos.append([])

    for vertice in coluna['geometry'].exterior.coords:

        # Vertices do polígono
        poligonos[i].append((vertice[0], vertice[1]))

# Inclinações e comprimentos
inclinacoes, comprimentos = inclinacoes_e_comprimentos_de_retas(poligonos)

# Lados das retas para extrair bissetrizes
lados_das_retas = lados_das_retas_das_bissetrizes(comprimentos)

# Angulos do polígono
angulos_grd = angulos_de_um_poligono(inclinacoes)[0]

# Cálculo dos pontos para retas das bissetrizes
bissetrizes = retas_de_bissetrizes(poligonos, angulos_grd)

# Pontos de intersecção das bissetrizes
pontos_de_interseccao = ponto_de_interseccao_de_retas(poligonos, bissetrizes, lados_das_retas)

# Alocando linhas das bissetrizes nos polígonos

coordenadas_das_linhas = []

for i in range(len(poligonos)):
    for j in range(2):        
        coordenadas_das_linhas.append([poligonos[i][lados_das_retas[i][j]], pontos_de_interseccao[i][j]])
        coordenadas_das_linhas.append([poligonos[i][lados_das_retas[i][j]+1], pontos_de_interseccao[i][j]])
        
    coordenadas_das_linhas.append([pontos_de_interseccao[i][j-1], pontos_de_interseccao[i][j]])   

# Criando objetos LineString a partir das coordenadas
linhas = [LineString(coords) for coords in coordenadas_das_linhas]

# Criando um novo GeoDataFrame com as linhas
novo_gdf = gpd.GeoDataFrame({"geometry": linhas}, crs=gdf.crs)

# Salve o novo GeoDataFrame como um shapefile
novo_gdf.to_file('C:\\Users\\Estrela\\Desktop\\quadras_shapefile\\novo_shapefile.shp')

# Fim da geração de nova shapefile

fim = time.time()

print(f"O shapefile levou {(fim - inicio):.6f} segundos para ser gerado.")