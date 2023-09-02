import geopandas as gpd

from shapely.geometry import LineString

# Separando coordenadas dos polígonos internos

def importando_coord_dos_poligonos_internos(lista_de_coordenadas, quantidade_de_lados):

    gdf_inf = []

    for i, row in lista_de_coordenadas:
        
        # Verifique se a geometria é um polígono com quatro coordenadas (vértices)
        
        if (row['geometry'] is not None and 
            row['geometry'].geom_type == 'Polygon' and 
            len(row['geometry'].exterior.coords) <= quantidade_de_lados):
            gdf_inf.append(row)

    # Separando vértices dos polígonos
            
    poligonos = []
            
    for i, coluna in enumerate(gdf_inf):
        
        # Polígonos
        poligonos.append([])

        for vertice in coluna['geometry'].exterior.coords:

            # Vertices do polígono
            poligonos[i].append((vertice[0], vertice[1]))

    return poligonos

# Importando coordenadas dos polígonos externos

def importando_coord_dos_poligonos_externos(lista_de_coordenadas):

    pontos_da_rua = []

    # Itera sobre os pontos e suas geometrias
    for idx, point in lista_de_coordenadas:
        if point['geometry'] is not None:
            pontos_da_rua.append((point['geometry'].x, point['geometry'].y))

    return pontos_da_rua

# Exportando shapefile de linhas e áreas internas dos polígonos

def exportando_informacoes_internas(poligonos, 
                                    pontos_de_interseccao, 
                                    lados_das_retas, 
                                    coordenada_das_areas_dos_poligonos,
                                    areas_dos_poligonos,
                                    gdf):
    
    coordenadas_das_linhas = []

    for i in range(len(poligonos)):
        
        if len(poligonos[i]) == 4:
            retas_que_se_tocam = 3
        else:
            retas_que_se_tocam = 2
            
        for j in range(retas_que_se_tocam):
            
            if len(poligonos[i]) == 4:
                coordenadas_das_linhas.append([poligonos[i][j], pontos_de_interseccao[i][0]])
                coordenadas_das_linhas.append([poligonos[i][j+1], pontos_de_interseccao[i][0]])

            else:
                coordenadas_das_linhas.append([poligonos[i][lados_das_retas[i][j]], pontos_de_interseccao[i][j]])
                coordenadas_das_linhas.append([poligonos[i][lados_das_retas[i][j]+1], pontos_de_interseccao[i][j]])

        if retas_que_se_tocam == 2:       
            coordenadas_das_linhas.append([pontos_de_interseccao[i][j-1], pontos_de_interseccao[i][j]])
            
    # Criando objetos LineString a partir das coordenadas
    linhas = [LineString(coords) for coords in coordenadas_das_linhas]

    # Criando um novo GeoDataFrame com as linhas
    novo_gdf_linhas = gpd.GeoDataFrame({"geometry": linhas}, crs=gdf)

    # Criando um novo GeoDataFrame com as áreas
    novo_gdf_areas = gpd.GeoDataFrame({'geometry': coordenada_das_areas_dos_poligonos, 'area': areas_dos_poligonos}, crs=gdf)

    return novo_gdf_linhas, novo_gdf_areas

# Exportando shapefile de linhas e áreas externas dos polígonos

def exportando_informacoes_externas(coordenadas_externas, 
                                    poligono_das_areas_dos_poligonos, 
                                    areas_dos_poligonos, 
                                    gdf):

    # Criando objetos LineString a partir das coordenadas
    linhas = [LineString(coords) for coords in coordenadas_externas]

    # Criando um novo GeoDataFrame com as linhas
    novo_gdf_linhas = gpd.GeoDataFrame({"geometry": linhas}, crs=gdf)

    # Criar as áreas (Para vê-las é necessário ativar as etiquetas nas configurações do ponto)
    novo_gdf_areas = gpd.GeoDataFrame({'geometry': poligono_das_areas_dos_poligonos, 'area': areas_dos_poligonos}, crs=gdf)

    return novo_gdf_linhas, novo_gdf_areas
