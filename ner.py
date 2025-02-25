#Import the requisite library
import spacy
import pandas as pd
import xlrd
from pandas.core.frame import DataFrame
#Build upon the spaCy Small Model
from spacy import displacy

df=pd.read_excel('C:\\Users\\Administrator\\Desktop\\叠层石数据\\geotime3.xls', index_col=None)
#df2=pd.read_csv("C:\\Users\\severus\\Desktop\\spacy测试\\Formation1.csv")
#df2=pd.read_excel("C:\\Users\\severus\\Desktop\\onebert标注数据集\\标注数据说明\\onebert4.xls")
#df3=pd.read_excel('C:\\Users\\severus\\Desktop\\spacy测试\\古生物.xlsx', index_col=None,engine='openpyxl')#注意这个地方可以打开xlsx了
dfrock=pd.read_excel('C:\\Users\\Administrator\\Desktop\\字典excel\\rockdic.xlsx', index_col=None,engine='openpyxl')#注意这个地方可以打开xlsx了
dfminer=pd.read_excel('C:\\Users\\Administrator\\Desktop\\字典excel\\minerdic.xlsx', index_col=None,engine='openpyxl')#注意这个地方可以打开xlsx了
dffacies=pd.read_excel('C:\\Users\\Administrator\\Desktop\\字典excel\\沉积相.xlsx', index_col=None,engine='openpyxl')#注意这个地方可以打开xlsx了
#fossillist=df3.iloc[0:78579,0].tolist()
geotimelist=df.iloc[0:df.shape[0]-1,0].tolist()
rocklist=dfrock.iloc[0:dfrock.shape[0]-1,0].tolist()
minerlist=dfminer.iloc[0:dfminer.shape[0]-1,0].tolist()
facieslist=dffacies.iloc[0:dffacies.shape[0]-1,0].tolist()
print(minerlist)
#ll2=df2.iloc[0:51150,2].tolist()
#ll2=df2.iloc[0:50595,2].tolist()
#datalist=df2.iloc[0:10,0].tolist()

nlp = spacy.load("en_core_web_sm")
nlp.max_length = 15000000
nlp.remove_pipe("ner")
#Sample text
#List of Entities and Patterns
#下面这个写法比较老
#patterns = [{"label": "GEOTIME", "pattern":item}  in geotiemlist ]
#词典的地质时间获取
#patterns = [{"label": "GEOTIME", "pattern":[{"TEXT":{"IN":geotiemlist}}]}]
#patternsGeoTime1 = [{"label": "GEOTIME", "pattern":[{"IS_TITLE":True,'OP':"*"},{"TEXT":{"IN":geotiemlist}},{"LIKE_NUM":True,'OP':"*"}]}]#{"POS":"AMOD",'OP':"*"},在这里没用
'''patternsGeoTime1 = [
    {
        "label": "GEOTIME",
        "pattern": [
            {"IS_TITLE": True, "TEXT": {"NOT_IN": ["The", "the"]}, "LIKE_NUM": False, 'OP': '*'},
            {"TEXT": {"IN": geotiemlist}},
            {"LIKE_NUM": True, 'OP': "*"}
        ]
    },
    {
        "label": "GEOTIME",
        "pattern": [
            {"IS_TITLE": True, "TEXT": {"NOT_IN": ["The", "the"]}, "LIKE_NUM": False, 'OP': '*'},
            {"TEXT": {"IN": geotiemlist}},
            {"TEXT": {"REGEX": "(-|to)"}},
            {"IS_TITLE": True, 'OP': "*"},
            {"TEXT": {"IN": geotiemlist}}
        ]
    }
]

patternsGeoTime12 = [{"label": "GEOTIME", "pattern":[{"LIKE_NUM":True,'OP':"*"},{"TEXT": {"REGEX":"(-|~|/|~|±)"},'OP':"?"},{"LIKE_NUM":True,'OP':"+"},{"TEXT": {"REGEX":"(Myr|MA|Ma|GA|Ga)"}}]}]
'''
patternsGeoTime1 = [
    # 匹配如 "Early Drumian"、"late Drumian"、"MIDDLE Drumian" 等模式
    {
        "label": "GEOTIME",
        "pattern": [
            {"LOWER": {"IN": ["early", "late", "middle", "upper", "lower"]}},
            {"TEXT": {"IN": geotimelist}}
        ]
    },
    # 匹配如 "Drumian 5" 这样的模式，其中数字是可选的
    {
        "label": "GEOTIME",
        "pattern": [
            {"IS_TITLE": True, "TEXT": {"NOT_IN": ["The", "the"]}, "LIKE_NUM": False, 'OP': '?'},
            {"TEXT": {"IN": geotimelist}},
            {"LIKE_NUM": True, 'OP': "?"}
        ]
    },
    # 匹配如 "Guzhangian to Drumian" 这样的模式
    {
        "label": "GEOTIME",
        "pattern": [
            {"IS_TITLE": True, "TEXT": {"NOT_IN": ["The", "the"]}, "LIKE_NUM": False},
            {"TEXT": {"IN": geotimelist}},
            {"TEXT": {"REGEX": "(?i)(-|to|and)"}},#不区分大小写
            {"IS_TITLE": True, 'OP': "?"},
            {"TEXT": {"IN": geotimelist}}
        ]
    }
]



patternsGeoTime12 = [{"label": "GEOTIME", "pattern":[{"LIKE_NUM":True,'OP':"*"},{"TEXT": {"REGEX":"(-|~|/|~|±|\+)"},'OP':"?"},{"LIKE_NUM":True,'OP':"+"},{"TEXT": {"REGEX":r"\b(Myr|MA|Ma|GA|Ga|Gyr)\b(?!\w)"}}]}]



#patternsFossil = [{"label": "FOSSIL", "pattern":[{"TEXT":{"IN":fossillist}}]}]
patternsFacies = [{"label": "FACIES", "pattern":[{"IS_TITLE":True,'OP':"+"},{'TEXT': {"REGEX":"(facies|FACIES|Facies)"}}]}]
patternsFacies2 =[{"label": "FACIES", "pattern":[{"TEXT":{"IN":facieslist}}]}]
patternsZircon = [{"label": "ZIRCON", "pattern":[{'TEXT': {"REGEX":"(zircon|Zircon|ZIRCON)"}}]}]
#patterns5 = [{"label": "GEOTIME2", "pattern":[{"LIKE_NUM":True},{"ORTH":"MA"}]}]
#patterns6 = [{"label": "GEOTIME3", "pattern":[{"LIKE_NUM":True},{"ORTH":"Myr"}]}]
patterns2=[{"label": "GPE", "pattern": "Treblinka"}, {"label": "SP", "pattern":{"SHAPE": "ddd"}}]
#patterns3 = [{"label": "Formation1", "pattern": [{"IS_TITLE":True,'OP':"+"},{"ORTH": "Formation"}]}]
patternsRock=[{"label": "ROCK", "pattern":[{"NORM":{"IN":rocklist}}]}]
patternsMiner=[{"label": "MINER", "pattern":[{"ORTH":{"IN":minerlist}}]}]
#patternsFormation = [{"label": "Formation1", "pattern": [{"IS_TITLE":True,'OP':"+"},{'TEXT': { "REGEX": "(Gp|Fm|Formation|Bed|Group|Limestone|Granite|Mbr|Sandstone|SGp|Member|Granodiorite|Volcanics|Shale|Complex|Subgroup|Conglomerate|Basalt|Suite|Dolomite|Tuff|Andesite|Gravel|Sand|Rhyolite|Diorite|Till|Gneiss|Beds|Tephra|Supersuite|Quartzite|Gabbro|Drift|Breccia|Schist|Monzonite|Supergroup|Measures|Clay|Mudstone|Siltstone|Tonalite|Metamorphics|Ash|Dolerite|Monzogranite|Slate|Latite|Gr|Series|Mem|Stage|System|Tillite|Deposits)$"}}]}]
#patternsFormation = [{"label": "Formation1", "pattern": [{"IS_TITLE":True,'OP':"+"},{"TEXT": {"REGEX": r"\b(Formation|bed|beds|Group|Member|Subgroup|Supergroup|Flow|Fm|Gr|Mem)\b(?!\w)"}}]}]
patternsFormation = [{"label": "Formation1", "pattern": [ {"IS_TITLE": True, "LOWER": {"NOT_IN": ["ga", "ma","the"]}, "OP": "+"}, {'TEXT': {"REGEX": r"\b(Gp|Fm|Formation|Bed|Group|Limestone|Granite|Mbr|Sandstone|SGp|Member|Granodiorite|Volcanics|Shale|Complex|Subgroup|Conglomerate|Basalt|Suite|Dolomite|Tuff|Andesite|Gravel|Sand|Rhyolite|Diorite|Till|Gneiss|Beds|Tephra|Supersuite|Quartzite|Gabbro|Drift|Breccia|Schist|Monzonite|Supergroup|Measures|Clay|Mudstone|Siltstone|Tonalite|Metamorphics|Ash|Dolerite|Monzogranite|Slate|Latite|Gr|Series|Mem|Stage|System|Tillite|Deposits)\b(?!\w)"}}]}]
#patterns4 = [{"label": "ROCK", "pattern": [{'TEXT': {"REGEX":"(limeston|dolomite)"}}]}]
patterns3 = [{"label": "LOCATION1", "pattern": [{"IS_TITLE":True,'OP':"+"},{'TEXT': {"REGEX":"(river|mountain|River|Mountain|valley|Valley)"}}]}]
       #Create the EntityRuler
ruler = nlp.add_pipe("entity_ruler")#注意这个地方before和after的用法。
ruler.add_patterns(patternsFormation)
ruler.add_patterns(patternsGeoTime1)
ruler.add_patterns(patterns2)
ruler.add_patterns(patterns3)
ruler.add_patterns(patternsMiner)
ruler.add_patterns(patternsRock)
ruler.add_patterns(patternsGeoTime12)
ruler.add_patterns(patternsFacies)
ruler.add_patterns(patternsFacies2)
ruler.add_patterns(patternsZircon)
#ruler.add_patterns(patternsFossil)

#ruler.add_patterns(patternsFossil)


nlp.add_pipe("ner", source=spacy.load("en_core_web_sm"))

labellist=[]
entitylist=[]
#for tt in datalist:
#   doc = nlp(tt)
#extract entities
'''#下面是对实体的抽取暂时不用
   for ent in doc.ents:
       labellist.append(ent.label_)
       entitylist.append(ent.text)
df3=DataFrame(labellist,entitylist)
df3.to_csv("C:\\Users\\severus\\Desktop\\spacy测试\\综合测试2.csv")
html_str = displacy.render(doc, style="ent")
with open("D:\\ss.html", "w", encoding="utf8") as f:
    f.write(html_str)
'''
def GeoEntityRecognize(s):
    doc=nlp(s)
    html_str = displacy.render(doc, style="ent")
    return html_str
def GeoEntityRecognize2(s):
    if "merge_entities" not in nlp.pipe_names:
        nlp.add_pipe("merge_entities")
#    if "merge_noun_chunks" not in nlp.pipe_names:
 #       nlp.add_pipe("merge_noun_chunks")
    docs=nlp.pipe(s)
    return docs