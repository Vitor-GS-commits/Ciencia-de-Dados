
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pydeck as pdk

st.set_page_config(
    page_title="Primeira Página",
    page_icon="random",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

df = pd.read_csv('input_M15_SINASC_RO_2019.csv')
st.title("Analise de dados de Ro em 2019")


# Dados da tabela
data = {
    "NOME": [
        "NUMERODN", "LOCNASC", "CODESTAB", "CODBAINASC", "CODMUNNASC", "IDADEMAE", "ESTCIVMAE",
        "ESCMAE", "CODOCUPMAE", "QTDFILVIVO", "QTDFILMORT", "CODBAIRES", "CODMUNRES", "GESTACAO",
        "GRAVIDEZ", "PARTO", "CONSULTAS", "DTNASC", "HORANASC", "SEXO", "APGAR 1", "APGAR 5",
        "RACACOR", "PESO", "IDANOMAL", "CODANOMAL", "DTCADASTR0", "DTRECEBIM", "CODINST", "UFINFORM"
    ],
    "DESCRIÇÃO": [
        "Número da DN, seqüencial por UF informante e por ano.",
        "Local de ocorrência do nascimento, conforme a tabela: 9: Ignorado, 1: Hospital, 2: Outro Estab Saúde, 3: Domicílio, 4: Outros",
        "Código de estabelecimento de saúde.",
        "Código Bairro nascimento.",
        "Código do município de ocorrência.",
        "Idade da mãe em anos.",
        "Estado civil, conforme a tabela: 1: Solteira, 2: Casada, 3: Viúva, 4: Separado judicialmente/Divorciado, 9: Ignorado",
        "Escolaridade, anos de estudo concluídos: 1: Nenhuma, 2: 1 a 3 anos, 3: 4 a 6 anos, 4: 7 e mais, 9: Ignorado",
        "Ocupação, conforme a Classificação Brasileira de Ocupações (CBO-2002).",
        "Número de filhos vivos.",
        "Número de filhos mortos.",
        "Código bairro residência.",
        "Município de residência da mãe.",
        "Semanas de gestação, conforme a tabela: 9: Ignorado, 1: Menos de 22 semanas, 2: 22 a 27 semanas, 3: 28 a 31 semanas, 4: 32 a 36 semanas, 5: 37 a 41 semanas, 6: 42 semanas e mais",
        "Tipo de gravidez, conforme a tabela: 9: Ignorado, 1: Única, 2: Dupla, 3: Tripla e mais",
        "Tipo de parto, conforme a tabela: 9: Ignorado, 1: Vaginal, 2: Cesáreo",
        "Número de consultas de pré-natal: 1: Nenhuma, 2: de 1 a 3, 3: de 4 a 6, 4: 7 e mais, 9: Ignorado",
        "Data do nascimento, no formato ddmmaaaa",
        "Hora do nascimento",
        "Sexo, conforme a tabela: 0: Ignorado, 1: Masculino, 2: Feminino",
        "Apgar no primeiro minuto: 00 a 10",
        "Apgar no quinto minuto: 00 a 10",
        "Raça/Cor: 1: Branca, 2: Preta, 3: Amarela, 4: Parda, 5: Indígena",
        "Peso ao nascer, em gramas.",
        "Anomalia congênita: 9: Ignorado, 1: Sim, 2: Não",
        "Código de malformação congênita ou anomalia cromossômica, de acordo com a CID-10.",
        "Data de cadastramento no sistema.",
        "Data de recebimento no nível central, data da última atualização do registro.",
        "Código da Instalação da geração dos Registros.",
        "Código da UF que informou o registro."
    ]
}
#limpando df pra utilização
df_col = df.drop(columns= ['CODESTAB', 'CODMUNNASC',
        'CODOCUPMAE', 'CODMUNRES', 'IDADEPAI',
        'IDANOMAL', 'NATURALMAE', 'ESCMAE2010',
       'CODANOMAL', 'NUMEROLOTE', 'VERSAOSIST', 'DTRECEBIM', 'DIFDATA',
       'DTRECORIGA', 'CODMUNNATU', 'CODUFNATU',
       'SERIESCMAE', 'QTDGESTANT', 'ORIGEM',
       'QTDPARTCES', 'DTULTMENST', 'TPMETESTIM',
       'CONSPRENAT', 'MESPRENAT', 'TPAPRESENT', 'STTRABPART', 'STCESPARTO',
       'TPNASCASSI', 'TPFUNCRESP', 'TPDOCRESP', 'DTDECLARAC', 'ESCMAEAGR1',
       'STDNEPIDEM', 'STDNNOVA', 'CODPAISRES', 'TPROBSON', 'PARIDADE',
       'KOTELCHUCK', 'CONTADOR'
       ])

legenda_dados = pd.DataFrame(data)
#Seleção de checkbox para consulta de legenda
if st.checkbox("Legenda para os dados"):
    escolha = st.selectbox('Selecione a coluna', data["NOME"])
    descricao = legenda_dados.loc[legenda_dados["NOME"] == escolha, "DESCRIÇÃO"].values[0]
    st.write(f"**Descrição para {escolha}:** {descricao}")
st.dataframe(df)
st.divider()
#uma multiseleção que gera uma lista com as variaveis x e y
escolha_x = st.selectbox('Selecione a variável do eixo x',
                              df_col.columns, 
                              key= 'seletor x',
                              help= 'Escolha a colunas para compor o eixo x',
                              placeholder = "escolha a coluna de dados",
                              index = None,
                              disabled = False)
#Escolher se ira ser apenas uma variavel
#toggle_value = st.toggle(label="escolher apenas uma variável", value = False, 
#                         key= "escolha_so_x",
#          )
# Atualiza o estado da selectbox com base no toggle
#selectbox_disabled = toggle_value
#if selectbox_disabled == True:
#    escolha_y = None
#else:
escolha_y = st.selectbox('Selecione a variável do eixo y',
                              df_col.columns, 
                              key= 'seletor y',
                              help= 'Escolha a colunas para compor o eixo y',
                              placeholder = "escolha a coluna de dados",
                              disabled = False,#selectbox_disabled,
                              index = None)

#Escolha do gráfico a ser gerado
lista_graficos = ['Linhas', 'Barra', 'Dispersão']
escolha_grafico = st.selectbox('Selecione o grafico adequado para as varaveis escolhidas',
                              lista_graficos, 
                              key= 'seletor grafico',
                              help= 'Escolha a colunas para compor o eixo y',
                              placeholder = "escolha o tipo de gráfico",
                              disabled = False,
                              index = None)


#df_remv_nan = df.index.dropna()#df.dropna(axis=0)

#df_limpo = df_remv_nan
#st.write(df_remv_col)
#st.dataframe(df_remv_nan)



#Plotando gráfico
if st.button('Gerar gráfico'):
    if escolha_grafico == None:
        st.write("aguardando segunda seleção ...")
    else:
        if escolha_grafico == 'Linhas':
            st.line_chart(x= escolha_x, y= escolha_y,
                        data=df_col)
        if escolha_grafico == 'Barra':
            st.bar_chart(x= escolha_x, y= escolha_y,
                        data=df_col)
        if escolha_grafico == 'Dispersão':
            st.scatter_chart(x= escolha_x, y= escolha_y,
                        data=df_col)
        else:
            print('encerrado')

st.divider()
st.subheader("Densidade de nascimentos por município ")
@st.cache_resource
def create_deck_chart(data):
    return pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=-10.750787,
            longitude=-62.779651,
            zoom=8,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position="[munResLon, munResLat]",
                radius=5000,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                "ScatterplotLayer",
                data=data,
                get_position="[munResLon, munResLat]",
                get_color="[200, 30, 0, 160]",
                get_radius=200,
            ),
        ],
    )

# Use o spinner para mostrar que o gráfico está carregando
with st.spinner('Carregando o Mapa...'):
    # Chame a função cacheada para obter o objeto pdk.Deck
    deck = create_deck_chart(df)

    # Exiba o gráfico no Streamlit
    st.pydeck_chart(deck)

# Mensagem de sucesso ao término do carregamento
st.success("Mapa carregado com sucesso!")

# Chame a função cacheada para obter o objeto pdk.Deck
#deck = create_deck_chart(df)
# Use o objeto pdk.Deck no st.pydeck_chart
#st.pydeck_chart(deck)

st.divider()
st.write("Deixe uma avaliação")
mapa_de_estrelas = ["uma", "duas", "três", "quatro", "cinco"]
selected = st.feedback("stars")
if selected is not None:
    st.markdown(f"você selecionou {mapa_de_estrelas[selected]} estrela(s).")

