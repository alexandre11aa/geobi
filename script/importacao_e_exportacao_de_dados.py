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

    # Calculando o comprimento das linhas
    comprimentos_das_linhas = [linha.length for linha in linhas]

    # Criando um novo GeoDataFrame com as linhas
    novo_gdf_linhas = gpd.GeoDataFrame({'geometry': linhas, 'length': comprimentos_das_linhas}, crs=gdf)

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

    # Calculando o comprimento das linhas
    comprimentos_das_linhas = [linha.length for linha in linhas]

    # Criando um novo GeoDataFrame com as linhas
    novo_gdf_linhas = gpd.GeoDataFrame({'geometry': linhas, 'length': comprimentos_das_linhas}, crs=gdf)

    # Criar as áreas (Para vê-las é necessário ativar as etiquetas nas configurações do ponto)
    novo_gdf_areas = gpd.GeoDataFrame({'geometry': poligono_das_areas_dos_poligonos, 'area': areas_dos_poligonos}, crs=gdf)

    return novo_gdf_linhas, novo_gdf_areas

# Salvando shapefile com estilo (.qml) para o QGis já abrir com etiquetas habilitadas

def estilo_qml(tipo, campo):

    if tipo == 'ponto':
        simbolo = '''<symbol type="marker" name="0" alpha="1" force_rhr="0" clip_to_extent="1">
          <layer class="SimpleMarker" enabled="1" pass="0" locked="0">
            <Option type="Map">
              <Option name="name" value="circle" type="QString"/>
              <Option name="color" value="227,26,28,255" type="QString"/>
              <Option name="outline_color" value="35,35,35,255" type="QString"/>
              <Option name="outline_width" value="0.2" type="QString"/>
              <Option name="size" value="2" type="QString"/>
              <Option name="size_unit" value="MM" type="QString"/>
            </Option>
          </layer>
        </symbol>'''
        colocacao = 'placement="0" dist="1" distUnits="MM"'

    else:
        simbolo = '''<symbol type="line" name="0" alpha="1" force_rhr="0" clip_to_extent="1">
          <layer class="SimpleLine" enabled="1" pass="0" locked="0">
            <Option type="Map">
              <Option name="line_color" value="35,35,35,255" type="QString"/>
              <Option name="line_width" value="0.26" type="QString"/>
              <Option name="line_width_unit" value="MM" type="QString"/>
            </Option>
          </layer>
        </symbol>'''
        colocacao = 'placement="2" dist="0" distUnits="MM"'

    return f'''<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
                <qgis version="3.28.0-Firenze" labelsEnabled="1">
                  <renderer-v2 type="singleSymbol" symbollevels="0" enableorderby="0" forceraster="0">
                    <symbols>
                      {simbolo}
                    </symbols>
                  </renderer-v2>
                  <labeling type="simple">
                    <settings calloutType="simple">
                      <text-style fieldName="{campo}" isExpression="0" fontSize="9" fontSizeUnit="Point" textColor="0,0,0,255" multilineHeight="1" fontFamily="Arial">
                        <text-buffer bufferDraw="1" bufferSize="0.8" bufferSizeUnits="MM" bufferColor="255,255,255,255" bufferOpacity="1"/>
                      </text-style>
                      <placement {colocacao} priority="5"/>
                      <rendering scaleVisibility="0" displayAll="1" drawLabels="1" obstacle="1" upsidedownLabels="0"/>
                    </settings>
                  </labeling>
                </qgis>
            '''

def salvando_shapefile_com_estilo(gdf, caminho, tipo, campo):

    # As áreas são calculadas como polígonos, mas são exportadas como pontos (dentro de cada polígono) para exibir o pontinho e a etiqueta
    if tipo == 'ponto':
        gdf = gdf.copy()
        centroides = gdf.geometry.centroid
        dentro = gdf.geometry.contains(centroides)

        # Centroide quando estiver dentro do polígono; caso contrário, um ponto interno (formas côncavas)
        gdf['geometry'] = centroides.where(dentro, gdf.geometry.representative_point())

    gdf.to_file(caminho)

    # O QGis carrega automaticamente um .qml com o mesmo nome do shapefile
    with open(caminho.rsplit('.', 1)[0] + '.qml', 'w', encoding='utf-8') as arquivo:
        arquivo.write(estilo_qml(tipo, campo))
