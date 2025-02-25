import spacy
from spacy.pipeline import EntityRuler
import  re
import pandas as pd
import xlrd
from spacy.language import Language
from spacy.tokens import Span
#Build upon the spaCy Small Model
from spacy import displacy
import pandas as pd
# Load the English model
nlp = spacy.load("en_core_web_sm")
nlp.max_length = 15000000

dffacies=pd.read_excel('C:\\Users\\Administrator\\Desktop\\字典excel\\沉积相.xlsx', index_col=None,engine='openpyxl')#注意这个地方可以打开xlsx了

facieslist=dffacies.iloc[0:dffacies.shape[0]-1,0].tolist()
patternsFacies = [{"label": "FACIES", "pattern":[{"IS_TITLE":True,'OP':"+"},{'TEXT': {"REGEX":"(facies|FACIES|Facies)"}}]}]
patternsFacies2 =[{"label": "FACIES", "pattern":[{"TEXT":{"IN":facieslist}}]}]

df=pd.read_excel('C:\\Users\\Administrator\\Desktop\\spacy测试\\geotime3.xls', index_col=None)
df2=pd.read_excel('C:\\Users\\Administrator\\Desktop\\spacy测试\\依赖测试2.xlsx', index_col=None,engine='openpyxl')
df3=pd.read_excel('C:\\Users\\Administrator\\Desktop\\spacy测试\\古生物.xlsx', index_col=None,engine='openpyxl')#注意这个地方可以打开xlsx了
fossillist = df3.iloc[0:78579, 0].str.lower().tolist()#古生物大小写好匹配
geotiemlist=df.iloc[0:df.shape[0],1].tolist()
print(geotiemlist)
FormationExceptList=["The", "the","Abstract",'Myr', 'MA', 'Ma', 'GA', 'Ga', 'Gyr','Research','study','publish','Working',"Formation",",","(",";",")",":","Group","Fm"]
InFormationWord='"^[A-Z][a-z]*$|^[a-z]+$|^-$"'
GeoTimeExceptList=["formation","Formation"]
GeoTimeSuffix1=['2', '4', '3','5','Ⅲ', 'Ⅳ', 'boundary']
GeoTimePrefix="\\b(?:early|late|middle|upper|lower|end|latest|uppermost|lowermost|terminal|mid|pre|earliest)\\b"
#Connector="\\b(?:\\-|,|and|to|or|:|\\/|\\(|\\（)\\b"

Connector="\\b(?:and|to|or)\\b|[-,:/()]"
ConnectorPrefix="\\b(?:and|to|or)\\b|[-:/]"
       # Custom NER patterns
patterns = [

    #地层匹配大写或者连词的情况
      #地层匹配大写开头，小写在后面的情况
    #1个2个前置的情况
{"label": "GEOLOGICAL_FORMATION", "pattern": [{"LOWER": {"REGEX": "\\b(?:early|late|middle|upper|lower|end|latest|uppermost|lowermost|terminal|mid|pre|earliest)\\b"}, "OP": "?"},{"IS_TITLE": True, "TEXT": {
        "NOT_IN": FormationExceptList, "REGEX": "^(?!\~?\d+(Ma|Ga|Myr)$).*$"}, "LOWER": {"NOT_IN": geotiemlist},
                                                   'OP': '1'},  # 前面是大写，但是取消地质年代
                                                  {"TEXT": {"REGEX": InFormationWord},"TEXT": {
        "NOT_IN": FormationExceptList, "REGEX": "^(?!\~?\d+(Ma|Ga|Myr)$).*$"}, "LOWER": {"NOT_IN": geotiemlist}, "OP": "?"},  # 匹配零个或多个小写单词
                                                   {'TEXT': {
                                                       "REGEX": "(Gp|Fm|Formation|Bed|Group|Limestone|Granite|Mbr|Sandstone|SGp|Member|Granodiorite|Volcanics|Shale|Complex|Subgroup|Conglomerate|Basalt|Suite|Dolomite|Tuff|Andesite|Gravel|Sand|Rhyolite|Diorite|Till|Gneiss|Beds|Tephra|Supersuite|Quartzite|Gabbro|Drift|Breccia|Schist|Monzonite|Supergroup|Measures|Clay|Mudstone|Siltstone|Tonalite|Metamorphics|Ash|Dolerite|Monzogranite|Slate|Latite|Gr|Series|Mem|Stage|System|Tillite|Deposits)$"}}]},
#3个前置字符地层情况
    {"label": "GEOLOGICAL_FORMATION", "pattern": [{"LOWER": {"REGEX": "\\b(?:early|late|middle|upper|lower|end|latest|uppermost|lowermost|terminal|mid|pre|earliest)\\b"}, "OP": "?"},{"IS_TITLE": True,"IS_SENT_START": False, "TEXT": {
        "NOT_IN":FormationExceptList, "REGEX": "^(?!\~?\d+(Ma|Ga|Myr)$).*$"},
                                                   "LOWER": {"NOT_IN": geotiemlist},
                                                   'OP': '1'},  # 前面是大写，但是取消地质年代
                                                  {"TEXT": {"REGEX": InFormationWord}, "TEXT": {
                                                      "NOT_IN": FormationExceptList,
                                                      "REGEX": "^(?!\~?\d+(Ma|Ga|Myr)$).*$"},
                                                   "LOWER": {"NOT_IN": geotiemlist}},  # 匹配零个或多个小写单词
                                                  {"TEXT": {"REGEX": InFormationWord}, "TEXT": {
                                                      "NOT_IN": FormationExceptList,
                                                      "REGEX": "^(?!\~?\d+(Ma|Ga|Myr)$).*$"},
                                                   "LOWER": {"NOT_IN": geotiemlist}},
                                                  {'TEXT': {
                                                      "REGEX": "(Gp|Fm|Formation|Bed|Group|Limestone|Granite|Mbr|Sandstone|SGp|Member|Granodiorite|Volcanics|Shale|Complex|Subgroup|Conglomerate|Basalt|Suite|Dolomite|Tuff|Andesite|Gravel|Sand|Rhyolite|Diorite|Till|Gneiss|Beds|Tephra|Supersuite|Quartzite|Gabbro|Drift|Breccia|Schist|Monzonite|Supergroup|Measures|Clay|Mudstone|Siltstone|Tonalite|Metamorphics|Ash|Dolerite|Monzogranite|Slate|Latite|Gr|Series|Mem|Stage|System|Tillite|Deposits)$"}}]},
#4个前置字符地层情况
    {"label": "GEOLOGICAL_FORMATION", "pattern": [{"LOWER": {"REGEX": "\\b(?:early|late|middle|upper|lower|end|latest|uppermost|lowermost|terminal|mid|pre|earliest)\\b"}, "OP": "?"},{"IS_TITLE": True,"IS_SENT_START": False, "TEXT": {
        "NOT_IN": FormationExceptList, "REGEX": "^(?!\~?\d+(Ma|Ga|Myr)$).*$"},
                                                   "LOWER": {"NOT_IN": geotiemlist},
                                                   'OP': '1'},  # 前面是大写，但是取消地质年代
                                                  {"TEXT": {"REGEX": InFormationWord}, "TEXT": {
                                                      "NOT_IN": FormationExceptList,
                                                      "REGEX": "^(?!\~?\d+(Ma|Ga|Myr)$).*$"},
                                                   "LOWER": {"NOT_IN": geotiemlist}},  # 匹配零个或多个小写单词
                                                  {"TEXT": {"REGEX": InFormationWord}, "TEXT": {
                                                      "NOT_IN": FormationExceptList,
                                                      "REGEX": "^(?!\~?\d+(Ma|Ga|Myr)$).*$"},
                                                   "LOWER": {"NOT_IN": geotiemlist}},
                                                  {"TEXT": {"REGEX": InFormationWord}, "TEXT": {
                                                      "NOT_IN": FormationExceptList,
                                                      "REGEX": "^(?!\~?\d+(Ma|Ga|Myr)$).*$"},
                                                   "LOWER": {"NOT_IN": geotiemlist}},
                                                  {'TEXT': {
                                                      "REGEX": "(Gp|Fm|Formation|Bed|Group|Limestone|Granite|Mbr|Sandstone|SGp|Member|Granodiorite|Volcanics|Shale|Complex|Subgroup|Conglomerate|Basalt|Suite|Dolomite|Tuff|Andesite|Gravel|Sand|Rhyolite|Diorite|Till|Gneiss|Beds|Tephra|Supersuite|Quartzite|Gabbro|Drift|Breccia|Schist|Monzonite|Supergroup|Measures|Clay|Mudstone|Siltstone|Tonalite|Metamorphics|Ash|Dolerite|Monzogranite|Slate|Latite|Gr|Series|Mem|Stage|System|Tillite|Deposits)$"}}]},
#两个时间段，四个时间
{"label": "GEOLOGICAL_AGE4", "pattern": [
    {"LOWER": {"REGEX": "\\b(?:early|late|middle|upper|lower|end|latest|uppermost|lowermost|terminal|mid|pre|earliest)\\b"}, "OP": "?"},
    {"LOWER": {"IN": geotiemlist}},
    {"LOWER": {"REGEX": "(\\-|,|and|to|or|:|\\/|\\(|\\（)"}, "OP": "?"},
    {"LOWER": {"REGEX": "\\b(?:early|late|middle|upper|lower|end|latest|uppermost|lowermost|terminal|mid|pre|earliest)\\b"}, "OP": "?"},
    {"LOWER": {"IN": geotiemlist}},
    {"LOWER": {"IN":GeoTimeSuffix1}, "OP": "?"},
    {"LOWER": {"REGEX": "(\\-|,|and|to|or|:|\\/|\\(|\\（)"}, "OP": "?"},
    {"LOWER": {
        "REGEX": "\\b(?:early|late|middle|upper|lower|end|latest|uppermost|lowermost|terminal|mid|pre|earliest)\\b"},
     "OP": "?"},
    {"LOWER": {"IN": geotiemlist}},
    {"LOWER": {"REGEX": "(\\-|,|and|to|or|:|\\/|\\(|\\（)"}, "OP": "?"},
    {"LOWER": {
        "REGEX": "\\b(?:early|late|middle|upper|lower|end|latest|uppermost|lowermost|terminal|mid|pre|earliest)\\b"},
     "OP": "?"},
    {"LOWER": {"IN": geotiemlist}},
    {"LOWER": {"IN": GeoTimeSuffix1}, "OP": "?"},
    {"LOWER": {"REGEX": "(\\-|,|and|to|or|:|\\/|\\(|\\（)"}, "OP": "?"},
]},

#层次时间，一个大时间段，后面包含几个小时假,三个时间
{"label": "GEOLOGICAL_AGE3", "pattern": [
    {"LOWER": {"REGEX": GeoTimePrefix}, "OP": "?"},
    {"LOWER": {"IN": geotiemlist}},
    {"LOWER": {"REGEX": Connector}, "OP": "?"},
    {"LOWER": {"REGEX": GeoTimePrefix}, "OP": "?"},
    {"LOWER": {"IN": geotiemlist}},
    {"LOWER": {"IN": GeoTimeSuffix1}, "OP": "?"},
    {"LOWER": {"REGEX": Connector}, "OP": "?"},
    {"LOWER": {"REGEX": GeoTimePrefix}, "OP": "?"},
    {"LOWER": {"IN": geotiemlist}},
    {"LOWER": {"IN": GeoTimeSuffix1}, "OP": "?"}
]},
#两个时间段
{"label": "GEOLOGICAL_AGE2", "pattern": [
    {"LOWER": {"REGEX":GeoTimePrefix }, "OP": "?"},
    {"LOWER": {"REGEX": ConnectorPrefix}, "OP": "?"},  # 匹配两个前缀的情况
    {"LOWER": {"REGEX": GeoTimePrefix},"OP": "?"},  # 匹配常规的前缀
    {"LOWER": {"IN": geotiemlist}},
    {"LOWER": {"IN": GeoTimeSuffix1}, "OP": "?"},
    {"LOWER": {"REGEX": Connector}, "OP": "?"},  #这个地方已经包含了只有空格的情况
    {"LOWER": {"REGEX": GeoTimePrefix}, "OP": "?"},
    {"LOWER": {"REGEX": ConnectorPrefix}, "OP": "?"},  # 匹配两个前缀的情况
    {"LOWER": {"REGEX": GeoTimePrefix},"OP": "?"},  # 匹配常规的前缀
    {"LOWER": {"IN": geotiemlist}},
    {"LOWER": {"IN": GeoTimeSuffix1}, "OP": "?"}
]},

#一个时间段+复合前缀
    {"label": "GEOLOGICAL_AGE1_2", "pattern": [

        {"LOWER": {
            "REGEX": "\\b(?:early|late|middle|upper|lower|end|latest|uppermost|lowermost|terminal|mid|pre|earliest)\\b"},
         "OP": "1"},  #  注意这个地方，为了避免and或者其他之前没有前缀也匹配，必须有个前缀后面的匹配才有意义，所以？改成了1
        {"LOWER": {"REGEX": "(\\-|and|to|or|:|\\/)\\b"}, "OP": "?"},  # 匹配两个前缀的情况
        {"LOWER": {
            "REGEX": "\\b(?:early|late|middle|upper|lower|end|latest|uppermost|lowermost|terminal|mid|pre|earliest)\\b"},
         "OP": "?"},  # 匹配常规的前缀
        {"LOWER": {"IN": geotiemlist}},
        {"LOWER": {"IN":GeoTimeSuffix1}, "OP": "?"}

    ]},

    #这个地方是单个时间完全没有前缀的直接匹配，因为上面是必须至少有一个，在实体链接的时候，这个GEOLOGICAL_AGE1模式直接和字典匹配即可
    {"label": "GEOLOGICAL_AGE1", "pattern": [
        {"LOWER": {"IN": geotiemlist}},
        {"LOWER": {"IN":GeoTimeSuffix1}, "OP": "?"}

    ]},
{"label": "GEOLOGICAL_AGE_AB1",#绝对时间点
     "pattern": [
         {"LIKE_NUM": True},  # 可选的前导数字
         {"TEXT": {"REGEX":"(±|\\+|\\+-)"}, 'OP': "?"},  # 匹配范围符号或“and”
         {"LIKE_NUM": True, 'OP': "?"},  #
         {"TEXT": {"REGEX": r"\b(Myr|MA|Ma|GA|Ga|Gyr)\b(?!\w)"}},  # 地质年代缩写
     ]},
{"label": "GEOLOGICAL_AGE_AB1_2",#结尾为million years
     "pattern": [
         {"LIKE_NUM": True},  # 可选的前导数字
         {"TEXT": {"REGEX":"(±|\\+|\\+-)"}, 'OP': "?"},  # 匹配范围符号或“and”
         {"LIKE_NUM": True, 'OP': "?"},  #
         {"LOWER": {"IN": ["million","billion"]}, 'OP': "1"},  # 可选的“million”
         {"LOWER": "years", 'OP': "1"},  # 可选的“years”
     ]},
    {"label": "GEOLOGICAL_AGE_AB2",#绝对时间段，
     "pattern": [
         {"LIKE_NUM": True},  # 可选的前导数字
          {"TEXT": {"REGEX":"(\\-|/|~|±|\\+|\\+-)"}, 'OP': "?"},  # 匹配范围符号或“and”
         {"LIKE_NUM": True, 'OP': "?"},  #
         {"TEXT": {"REGEX": r"\b(Myr|MA|Ma|GA|Ga|Gyr)\b(?!\w)"}, 'OP': "?"},
         {"TEXT": {"REGEX":"(\\-|and|or|to)"}, 'OP': "?"},  # 整体是匹配两个时间段，没有连接符只有空格也可以。
         {"LIKE_NUM": True},  # 可选的前导数字
         {"TEXT": {"REGEX": "(\\-|/|~|±|\\+|\\+-)"}, 'OP': "?"},  # 匹配范围符号或“and”
         {"LIKE_NUM": True, 'OP': "?"},  #
         {"TEXT": {"REGEX": r"\b(Myr|MA|Ma|GA|Ga|Gyr)\b(?!\w)"}},  # 地质年代缩写
     ]},
    {"label": "GEOLOGICAL_AGE_AB2_2",  # 绝对时间段,时段years，这种虽然不多也是一种后缀还是先写着
     "pattern": [
         {"LIKE_NUM": True},  # 可选的前导数字
         {"TEXT": {"REGEX": "(\\-|/|~|±|\\+|\\+-)"}, 'OP': "?"},  # 匹配范围符号或“and”
         {"LIKE_NUM": True, 'OP': "?"},  #
         {"LOWER": "million", 'OP': "?"},  # 可选的“million”
         {"LOWER": "years", 'OP': "?"},  # 可选的“years”
         {"TEXT": {"REGEX": "(\\-|and|or|to)"}, 'OP': "?"},  # 整体是匹配两个时间段，没有连接符只有空格也可以。
         {"LIKE_NUM": True},  # 这个就是为了匹配两个数值的那种，就是为了代码整齐且后面好区分
         {"TEXT": {"REGEX": "(\\-|/|~|±|\\+|\\+-)"}, 'OP': "?"},  # 匹配范围符号或“and”
         {"LIKE_NUM": True, 'OP': "?"},  #
         {"LOWER":  {"IN": ["million","billion"]}, 'OP': "1"},  # 可选的“million”
         {"LOWER": "years", 'OP': "1"},  # 可选的“years”
     ]},
    {"label": "STROMA",  # 匹配叠层石
     "pattern": [

         {"TEXT": {"REGEX": "[sS]tromatolit.*"}},

     ]},
{
  "label": "BLACK_SHALE",  # 匹配黑色页岩
  "pattern": [
    {"LOWER": "black"},
    {"LOWER": "shale"}
  ]
},
{
  "label": "OOLITIC",  # 匹配所有与“oolitic”相关的术语
  "pattern": [
    {"TEXT": {"REGEX": "oolit.*"}}
  ]
} ,
{
  "label": "ONCOID",  # 匹配所有与“核形石”相关的术语
  "pattern": [
    {"TEXT": {"REGEX": "(oncoid.*|oncolit.*)"}}  # 使用正则表达式的“或”操作符
  ]
},
{
  "label": "FOSSIL", "pattern":[
    {"LOWER": {"IN": fossillist}}]
},
{
  "label": "Thromb",  # 匹配所有与“核形石”相关的术语
  "pattern": [
    {"TEXT": {"REGEX": "(?i)(thrombolite.*)"}}  # 使用正则表达式的“或”操作符并设置不区分大小写
  ]
}

]
@Language.component("remove_geo_age3_stage")
def remove_geo_age3_stage(doc):
    new_ents = []
    for ent in doc.ents:
        # 检查实体类型和最后一个词
        if ent.label_ == "GEOLOGICAL_AGE3" and ent.text.split()[-1].lower() in ["stage","series"]:
            # 创建不包含最后一个词的新实体
            new_ent = Span(doc, ent.start, ent.end - 1, label="GEOLOGICAL_AGE2")
            new_ents.append(new_ent)
        else:
            new_ents.append(ent)
    # 更新doc的实体
    doc.ents = new_ents
    return doc
# Add the custom EntityRuler to the pipeline
nlp.remove_pipe('ner')
ruler = nlp.add_pipe("entity_ruler")#注意这个地方before和after的用法。
ruler.add_patterns(patternsFacies)
ruler.add_patterns(patternsFacies2)
ruler.add_patterns(patterns)
nlp.add_pipe("ner", source=spacy.load("en_core_web_sm"))
nlp.add_pipe('remove_geo_age3_stage', name="remove_geo_age3_stage")
nlp.add_pipe('merge_entities')







def extract_geological_relations7(doc, distance_threshold=2):
    def is_relation_added(relation, relations_list):
        return any(relation[0].text == existing_relation[0].text and
                   relation[1].text == existing_relation[1].text for existing_relation in relations_list)

    def get_sentence_of_entity(ent):
        return ent.sent.text.strip() if ent.sent else ""

  #  relations = []
    # Checking for proximity
    # 定义一个排除列表
    exclusion_list = [",", ".",")",";"]

    for ent1 in doc.ents:
        if ent1.label_ == "GEOLOGICAL_AGE":
            for ent2 in doc.ents:
                if ent2.label_ == "GEOLOGICAL_FORMATION":
                    # 检查实体是否在距离阈值内
                    if abs(ent1.start - ent2.end) < distance_threshold or abs(
                            ent2.start - ent1.end) < distance_threshold:
                        # 提取两个实体之间的文本
                        start = min(ent1.end, ent2.end)
                        end = max(ent1.start, ent2.start)
                        intervening_text = doc[start:end].text

                        # 检查中间文本是否包含排除列表中的任何词
                        if not any(excluded_word in intervening_text for excluded_word in exclusion_list):
                            relation = (ent2, ent1, get_sentence_of_entity(ent2), "Proximity Relation")
                            if not is_relation_added(relation, relations):
                                relations.append(relation)

    for ent in doc.ents:
        if ent.label_ == "GEOLOGICAL_FORMATION":
            # Checking for ancestors
            for ancestor in ent.root.ancestors:
                if ancestor.ent_type_ == "GEOLOGICAL_AGE":
                    relation = (ent, ancestor, get_sentence_of_entity(ent), "Ancestor-Child Relation")
                    if not is_relation_added(relation, relations):
                        relations.append(relation)
                    break

            # Checking for children
            for child in ent.root.children:
                if child.ent_type_ == "GEOLOGICAL_AGE":
                    relation = (ent, child, get_sentence_of_entity(ent), "Parent-Child Relation")
                    if not is_relation_added(relation, relations):
                        relations.append(relation)
                    break
        """
            # Checking for shared head (common parent),这个精度很低，先取消
            for ent1 in doc.ents:
                for ent2 in doc.ents:
                    if ent1.label_ == "GEOLOGICAL_FORMATION" and ent2.label_ == "GEOLOGICAL_AGE" and ent1.root.head == ent2.root.head:
                        relation = (ent1, ent2, get_sentence_of_entity(ent1), "Shared Head Relation")
                        if not is_relation_added(relation, relations):
                            relations.append(relation)
        """
    return relations

def extract_geological_relations8(doc, distance_threshold=2):
    def is_relation_added(relation, relations_list):
        return any(relation[0].text == existing_relation[0].text and
                   relation[1].text == existing_relation[1].text for existing_relation in relations_list)

    def get_sentence_of_entity(ent):
        return ent.sent.text.strip() if ent.sent else ""

    #  relations = []
    # Checking for proximity
    # 定义一个距离规则的排除列表
    exclusion_list = [",", ".", ")", ";","and"]

    for ent1 in doc.ents:
        if ent1.label_ == "GEOLOGICAL_AGE":
            for ent2 in doc.ents:
                if ent2.label_ == "GEOLOGICAL_FORMATION":
                    # 检查实体是否在距离阈值内
                    if abs(ent1.start - ent2.end) < distance_threshold or abs(
                            ent2.start - ent1.end) < distance_threshold:
                        # 提取两个实体之间的文本
                        start = min(ent1.end, ent2.end)
                        end = max(ent1.start, ent2.start)
                        intervening_text = doc[start:end].text

                        # 检查中间文本是否包含排除列表中的任何词
                        if not any(excluded_word in intervening_text for excluded_word in exclusion_list):
                            relation = (ent2, ent1, get_sentence_of_entity(ent2), "Proximity Relation")
                            if not is_relation_added(relation, relations):
                                relations.append(relation)

    exclusion_list2 = ["before", ".", "after", ";","end"]
    for ent in doc.ents:
        if ent.label_ == "GEOLOGICAL_FORMATION":
            # Checking for ancestors
            for ancestor in ent.root.ancestors:
                if ancestor.ent_type_ == "GEOLOGICAL_AGE":
                    intervening_text = doc[ent.root.i + 1:ancestor.i].text if ent.root.i < ancestor.i else doc[ancestor.i + 1:ent.root.i].text
                    if not any(excluded_word in intervening_text for excluded_word in exclusion_list2):
                        relation = (ent, ancestor, get_sentence_of_entity(ent), "Ancestor-Child Relation")
                        if not is_relation_added(relation, relations):
                            relations.append(relation)
                        break

            # Checking for children
            for child in ent.root.children:
                if child.ent_type_ == "GEOLOGICAL_AGE":
                    intervening_text = doc[ent.root.i + 1:child.i].text if ent.root.i < child.i else doc[child.i + 1:ent.root.i].text
                    if not any(excluded_word in intervening_text for excluded_word in exclusion_list2):
                        relation = (ent, child, get_sentence_of_entity(ent), "Parent-Child Relation")
                        if not is_relation_added(relation, relations):
                            relations.append(relation)
                        break

    return relations
"""
第十个版本添加了地质时间的匹配标记，这样为时间的实体链接恢复创造了条件
"""
def extract_geological_relations10(doc, distance_threshold=2,filename=""):
    def is_relation_added(relation, relations_list):
        return any(relation[1].text == existing_relation[1].text and
                   relation[2].text == existing_relation[2].text for existing_relation in relations_list)

    def get_sentence_of_entity(ent):
        return ent.sent.text.strip() if ent.sent else ""

    relations = []
    exclusion_list = [",", ".", ")", ";"]

    # Proximity-Based Relation Identification
    for ent1 in doc.ents:
        if ent1.label_.startswith("GEOLOGICAL_AGE"):
            for ent2 in doc.ents:
                if ent2.label_ == "GEOLOGICAL_FORMATION":
                    if abs(ent1.start - ent2.end) < distance_threshold or abs(
                            ent2.start - ent1.end) < distance_threshold:
                        start = min(ent1.end, ent2.end)
                        end = max(ent1.start, ent2.start)
                        intervening_text = doc[start:end].text
                        if not any(excluded_word in intervening_text for excluded_word in exclusion_list):
                            relation = (filename,ent2, ent1, ent1.label_, get_sentence_of_entity(ent2), "Proximity Relation")
                            if not is_relation_added(relation, relations):
                                relations.append(relation)

    exclusion_list2 = ["before", ".", "after", ";"]
    for ent in doc:
        if ent.ent_type_ == "GEOLOGICAL_FORMATION":
            # Ancestor-Child Relation Identification
            for ancestor in ent.ancestors:
                if ancestor.ent_type_.startswith("GEOLOGICAL_AGE"):
                    intervening_text = doc[ent.i + 1:ancestor.i].text if ent.i < ancestor.i else doc[
                                                                                                 ancestor.i + 1:ent.i].text
                    if not any(excluded_word in intervening_text for excluded_word in exclusion_list2):
                        relation = (filename,ent, ancestor, ancestor.ent_type_, get_sentence_of_entity(ent), "Ancestor-Child Relation")
                        if not is_relation_added(relation, relations):
                            relations.append(relation)
                        break

            # Parent-Child Relation Identification
            for child in ent.subtree:
                if child.ent_type_.startswith("GEOLOGICAL_AGE"):
                    intervening_text = doc[ent.i + 1:child.i].text if ent.i < child.i else doc[
                                                                                           child.i + 1:ent.i].text
                    if not any(excluded_word in intervening_text for excluded_word in exclusion_list2):
                        relation = (filename,ent, child, child.ent_type_, get_sentence_of_entity(ent), "Parent-Child Relation")
                        if not is_relation_added(relation, relations):
                            relations.append(relation)
                        break
    return relations
import pandas as pd

def extract_geological_relations11(doc, distance_threshold=2, filename=""):
    def is_relation_added(relation, relations_df):
        return any((relations_df['Filename'] == relation[0]) &
                   (relations_df['Entity2'] == relation[1]) &
                   (relations_df['Entity3'] == relation[2]))

    def get_sentence_of_entity(ent):
        return ent.sent.text.strip() if ent.sent else ""

    relations_df = pd.DataFrame(columns=['Filename', 'Entity2', 'Entity3', 'Entity3Label', 'Sentence', 'RelationType'])

    exclusion_list = [",", ".", ")", ";","and"]     #地层和年代之间出现个and不合适

    for ent1 in doc.ents:
        if ent1.label_.startswith("GEOLOGICAL_AGE"):
            for ent2 in doc.ents:
                if ent2.label_ == "GEOLOGICAL_FORMATION":
                    if abs(ent1.start - ent2.end) < distance_threshold or abs(
                            ent2.start - ent1.end) < distance_threshold:
                        start = min(ent1.end, ent2.end)
                        end = max(ent1.start, ent2.start)
                        intervening_text = doc[start:end].text
                        if not any(excluded_word in intervening_text for excluded_word in exclusion_list):
                            relation = (filename, ent2.text, ent1.text, ent1.label_,
                                        get_sentence_of_entity(ent2), "Proximity Relation")
                            if not is_relation_added(relation, relations_df):
                                relation_df = pd.DataFrame([relation], columns=relations_df.columns)
                                relations_df = pd.concat([relations_df, relation_df], ignore_index=True)

    exclusion_list2 = ["before", ".", "after", ";"]
    for ent in doc:
        if ent.ent_type_ == "GEOLOGICAL_FORMATION":
            # 祖先-后代关系识别
            for ancestor in ent.ancestors:
                if ancestor.ent_type_.startswith("GEOLOGICAL_AGE"):
                    intervening_text = doc[ent.i + 1:ancestor.i].text if ent.i < ancestor.i else doc[
                                                                                                 ancestor.i + 1:ent.i].text
                    if not any(excluded_word in intervening_text for excluded_word in exclusion_list2):
                        relation = (filename, ent.text, ancestor.text, ancestor.ent_type_,
                                    get_sentence_of_entity(ent), "Ancestor-Child Relation")
                        if not is_relation_added(relation, relations_df):
                            relation_df = pd.DataFrame([relation], columns=relations_df.columns)
                            relations_df = pd.concat([relations_df, relation_df], ignore_index=True)
                        break

            # 父子关系识别
            for child in ent.subtree:
                if child.ent_type_.startswith("GEOLOGICAL_AGE"):
                    intervening_text = doc[ent.i + 1:child.i].text if ent.i < child.i else doc[
                                                                                           child.i + 1:ent.i].text
                    if not any(excluded_word in intervening_text for excluded_word in exclusion_list2):
                        relation = (filename, ent.text, child.text, child.ent_type_,
                                    get_sentence_of_entity(ent), "Parent-Child Relation")
                        if not is_relation_added(relation, relations_df):
                            relation_df = pd.DataFrame([relation], columns=relations_df.columns)
                            relations_df = pd.concat([relations_df, relation_df], ignore_index=True)
                        break

    return relations_df
def extract_geological_relationsLocation(doc, distance_threshold=2, filename=""):
    def is_relation_added(relation, relations_df):
        return any((relations_df['Filename'] == relation[0]) &
                   (relations_df['Entity2'] == relation[1]) &
                   (relations_df['Entity3'] == relation[2]))

    def get_sentence_of_entity(ent):
        return ent.sent.text.strip() if ent.sent else ""

    relations_df = pd.DataFrame(columns=['Filename', 'Entity2', 'Entity3', 'Entity3Label', 'Sentence', 'RelationType'])

    exclusion_list = [",", ".", ")", ";","and"]     #地层和年代之间出现个and不合适

    for ent1 in doc.ents:
        if ent1.label_ == "GEOLOGICAL_FORMATION":
            for ent2 in doc.ents:
                if ent2.label_ == "GPE" or ent2.label_ == "LOC":
                    if abs(ent1.start - ent2.end) < distance_threshold or abs(
                            ent2.start - ent1.end) < distance_threshold:
                        start = min(ent1.end, ent2.end)
                        end = max(ent1.start, ent2.start)
                        intervening_text = doc[start:end].text
                        if not any(excluded_word in intervening_text for excluded_word in exclusion_list):
                            relation = (filename, ent2.text, ent1.text, ent1.label_,
                                        get_sentence_of_entity(ent2), "Proximity Relation")
                            if not is_relation_added(relation, relations_df):
                                relation_df = pd.DataFrame([relation], columns=relations_df.columns)
                                relations_df = pd.concat([relations_df, relation_df], ignore_index=True)

    exclusion_list2 = ["before", ".", "after", ";"]
    for ent in doc:
        if ent.ent_type_ == "GEOLOGICAL_FORMATION":
            # 祖先-后代关系识别
            for ancestor in ent.ancestors:
                if ancestor.ent_type_ == "GPE" or ancestor.ent_type_ == "LOC":
                    intervening_text = doc[ent.i + 1:ancestor.i].text if ent.i < ancestor.i else doc[
                                                                                                 ancestor.i + 1:ent.i].text
                    if not any(excluded_word in intervening_text for excluded_word in exclusion_list2):
                        relation = (filename, ent.text, ancestor.text, ancestor.ent_type_,
                                    get_sentence_of_entity(ent), "Ancestor-Child Relation")
                        if not is_relation_added(relation, relations_df):
                            relation_df = pd.DataFrame([relation], columns=relations_df.columns)
                            relations_df = pd.concat([relations_df, relation_df], ignore_index=True)
                        break

            # 父子关系识别
            for child in ent.subtree:
                if child.ent_type_ == "GPE" or ancestor.ent_type_ == "LOC":
                    intervening_text = doc[ent.i + 1:child.i].text if ent.i < child.i else doc[
                                                                                           child.i + 1:ent.i].text
                    if not any(excluded_word in intervening_text for excluded_word in exclusion_list2):
                        relation = (filename, ent.text, child.text, child.ent_type_,
                                    get_sentence_of_entity(ent), "Parent-Child Relation")
                        if not is_relation_added(relation, relations_df):
                            relation_df = pd.DataFrame([relation], columns=relations_df.columns)
                            relations_df = pd.concat([relations_df, relation_df], ignore_index=True)
                        break

    return relations_df

def extract_geological_proxcy_fm(doc, proxy,distance_threshold=2, filename=""):
    def is_relation_added(relation, relations_df):
        return any((relations_df['Filename'] == relation[0]) &
                   (relations_df['Entity2'] == relation[1]) &
                   (relations_df['Entity3'] == relation[2]))

    def get_sentence_of_entity(ent):
        return ent.sent.text.strip() if ent.sent else ""

    relations_df = pd.DataFrame(columns=['Filename', 'Entity2', 'Entity3', 'Entity3Label', 'Sentence', 'RelationType'])

    exclusion_list = [",", ".", ")", ";","and"]     #地层和年代之间出现个and不合适

    for ent1 in doc.ents:
        if ent1.label_ == "GEOLOGICAL_FORMATION":
            for ent2 in doc.ents:
                if ent2.label_ == proxy:
                    if abs(ent1.start - ent2.end) < distance_threshold or abs(
                            ent2.start - ent1.end) < distance_threshold:
                        start = min(ent1.end, ent2.end)
                        end = max(ent1.start, ent2.start)
                        intervening_text = doc[start:end].text
                        if not any(excluded_word in intervening_text for excluded_word in exclusion_list):
                            relation = (filename, ent2.text, ent1.text, ent1.label_,
                                        get_sentence_of_entity(ent2), "Proximity Relation")
                            if not is_relation_added(relation, relations_df):
                                relation_df = pd.DataFrame([relation], columns=relations_df.columns)
                                relations_df = pd.concat([relations_df, relation_df], ignore_index=True)

    exclusion_list2 = ["before", ".", "after", ";"]
    for ent in doc:
        if ent.ent_type_ == proxy:
            # 祖先-后代关系识别
            for ancestor in ent.ancestors:
                if ancestor.ent_type_ == "GEOLOGICAL_FORMATION":
                    intervening_text = doc[ent.i + 1:ancestor.i].text if ent.i < ancestor.i else doc[
                                                                                                 ancestor.i + 1:ent.i].text
                    if not any(excluded_word in intervening_text for excluded_word in exclusion_list2):
                        relation = (filename, ent.text, ancestor.text, ancestor.ent_type_,
                                    get_sentence_of_entity(ent), "Ancestor-Child Relation")
                        if not is_relation_added(relation, relations_df):
                            relation_df = pd.DataFrame([relation], columns=relations_df.columns)
                            relations_df = pd.concat([relations_df, relation_df], ignore_index=True)
                        break

            # 父子关系识别
            for child in ent.subtree:
                if child.ent_type_ == "GEOLOGICAL_FORMATION":
                    intervening_text = doc[ent.i + 1:child.i].text if ent.i < child.i else doc[
                                                                                           child.i + 1:ent.i].text
                    if not any(excluded_word in intervening_text for excluded_word in exclusion_list2):
                        relation = (filename, ent.text, child.text, child.ent_type_,
                                    get_sentence_of_entity(ent), "Parent-Child Relation")
                        if not is_relation_added(relation, relations_df):
                            relation_df = pd.DataFrame([relation], columns=relations_df.columns)
                            relations_df = pd.concat([relations_df, relation_df], ignore_index=True)
                        break

    return relations_df
def extract_geological_proxcy_fm_in_sentence(doc, proxy, distance_threshold=25, filename=""):
    def is_relation_added(relation, relations_df):
        return any((relations_df['Filename'] == relation[0]) &
                   (relations_df['Entity2'] == relation[1]) &
                   (relations_df['Entity3'] == relation[2]))

    def get_sentence_of_entity(ent):
        return ent.sent.text.strip() if ent.sent else ""

    relations_df = pd.DataFrame(columns=['Filename', 'Entity2', 'Entity3', 'Entity3Label', 'Sentence', 'RelationType'])

    for sent in doc.sents:
        geological_ents = [ent for ent in sent.ents if ent.label_ == "GEOLOGICAL_FORMATION"]
        proxy_ents = [ent for ent in sent.ents if ent.label_ == proxy]

        for ent1 in geological_ents:
            for ent2 in proxy_ents:
                # 检查距离是否在阈值范围内
                if abs(ent1.start - ent2.end) <= distance_threshold or abs(ent2.start - ent1.end) <= distance_threshold:
                    relation = (filename, ent2.text, ent1.text, ent1.label_,
                                get_sentence_of_entity(ent2), "Proximity Relation")
                    if not is_relation_added(relation, relations_df):
                        relation_df = pd.DataFrame([relation], columns=relations_df.columns)
                        relations_df = pd.concat([relations_df, relation_df], ignore_index=True)
                    break  # 只加入第一个找到的实体对

    return relations_df
def extract_geological_proxcy_x_in_sentence(doc, proxy, distance_threshold=25, filename=""):
    def is_relation_added(relation, relations_df):
        return any((relations_df['Filename'] == relation[0]) &
                   (relations_df['Entity2'] == relation[1]) &
                   (relations_df['Entity3'] == relation[2]))

    def get_sentence_of_entity(ent):
        return ent.sent.text.strip() if ent.sent else ""

    relations_df = pd.DataFrame(columns=['Filename', 'Entity2', 'Entity3', 'Entity3Label', 'Sentence', 'RelationType'])

    for sent in doc.sents:
        geological_ents = [ent for ent in sent.ents if ent.label_ == "LOC" or ent.label_ == "GPE" or ent.label_=="FACIES" or ent.label_ == "GEOLOGICAL_FORMATION" or ent.label_.startswith("GEOLOGICAL_AGE")]
        proxy_ents = [ent for ent in sent.ents if ent.label_ == proxy]

        for ent1 in geological_ents:
            for ent2 in proxy_ents:
                # 检查距离是否在阈值范围内
                if abs(ent1.start - ent2.end) <= distance_threshold or abs(ent2.start - ent1.end) <= distance_threshold:
                    relation = (filename, ent2.text, ent1.text, ent1.label_,
                                get_sentence_of_entity(ent2), ent1.label_)
                    if not is_relation_added(relation, relations_df):
                        relation_df = pd.DataFrame([relation], columns=relations_df.columns)
                        relations_df = pd.concat([relations_df, relation_df], ignore_index=True)
                    break  # 只加入第一个找到的实体对

    return relations_df
def extract_geological_proxcy_x_in_sentence2(doc, proxy, distance_threshold=25, filename=""):
    def is_relation_added(relation, relations_df):
        # 由于现在关系数据结构已经改变，需要相应地调整此函数
        return any((relations_df['Filename'] == relation[0]) &
                   (relations_df['EntityLabel'] == relation[1]) &
                   (relations_df['Sentence'] == relation[2]))

    def get_sentence_of_entity(ent):
        return ent.sent.text.strip() if ent.sent else ""

    # 更新 DataFrame 列，只保留需要的信息
    relations_df = pd.DataFrame(columns=['Filename', 'EntityLabel', 'Sentence'])

    for sent in doc.sents:
        geological_ents = [ent for ent in sent.ents if ent.label_ == "LOC" or ent.label_ == "GPE" or ent.label_=="FACIES" or ent.label_ == "GEOLOGICAL_FORMATION" or ent.label_.startswith("GEOLOGICAL_AGE")]
        proxy_ents = [ent for ent in sent.ents if ent.label_ == proxy]

        for ent1 in geological_ents:
            for ent2 in proxy_ents:
                # 检查距离是否在阈值范围内
                if abs(ent1.start - ent2.end) <= distance_threshold or abs(ent2.start - ent1.end) <= distance_threshold:
                    relation = (filename, ent1.label_, get_sentence_of_entity(ent2))
                    if not is_relation_added(relation, relations_df):
                        # 更新此处以反映新的 DataFrame 结构
                        relation_df = pd.DataFrame([relation], columns=relations_df.columns)
                        relations_df = pd.concat([relations_df, relation_df], ignore_index=True)


    return relations_df
def extract_geological_location_fm_in_sentence(doc, distance_threshold=25, filename=""):
    def is_relation_added(relation, relations_df):
        return any((relations_df['Filename'] == relation[0]) &
                   (relations_df['Entity2'] == relation[1]) &
                   (relations_df['Entity3'] == relation[2]))

    def get_sentence_of_entity(ent):
        return ent.sent.text.strip() if ent.sent else ""

    relations_df = pd.DataFrame(columns=['Filename', 'Entity2', 'Entity3', 'Entity3Label', 'Sentence', 'RelationType'])

    for sent in doc.sents:
        geological_ents = [ent for ent in sent.ents if ent.label_ == "GEOLOGICAL_FORMATION"]
        proxy_ents = [ent for ent in sent.ents if ent.label_ == "GPE" or ent.label_ == "LOC"]

        for ent1 in geological_ents:
            for ent2 in proxy_ents:
                # 检查距离是否在阈值范围内
                if abs(ent1.start - ent2.end) <= distance_threshold or abs(ent2.start - ent1.end) <= distance_threshold:
                    relation = (filename, ent2.text, ent1.text, ent1.label_,
                                get_sentence_of_entity(ent2), "Proximity Relation")
                    if not is_relation_added(relation, relations_df):
                        relation_df = pd.DataFrame([relation], columns=relations_df.columns)
                        relations_df = pd.concat([relations_df, relation_df], ignore_index=True)
                    break  # 只加入第一个找到的实体对

    return relations_df
def extract_geological_geotime_fm_in_sentence(doc, distance_threshold=25, filename=""):
    def is_relation_added(relation, relations_df):
        return any((relations_df['Filename'] == relation[0]) &
                   (relations_df['Entity2'] == relation[1]) &
                   (relations_df['Entity3'] == relation[2]))

    def get_sentence_of_entity(ent):
        return ent.sent.text.strip() if ent.sent else ""

    relations_df = pd.DataFrame(columns=['Filename', 'Entity2', 'Entity3', 'Entity3Label', 'Sentence', 'RelationType'])

    for sent in doc.sents:
        geological_ents = [ent for ent in sent.ents if ent.label_ == "GEOLOGICAL_FORMATION"]
        proxy_ents = [ent for ent in sent.ents if ent.label_.startswith("GEOLOGICAL_AGE")]

        for ent1 in geological_ents:
            for ent2 in proxy_ents:
                # 检查距离是否在阈值范围内
                if abs(ent1.start - ent2.end) <= distance_threshold or abs(ent2.start - ent1.end) <= distance_threshold:
                    relation = (filename, ent2.text, ent1.text, ent2.label_,
                                get_sentence_of_entity(ent2), "Proximity Relation")
                    if not is_relation_added(relation, relations_df):
                        relation_df = pd.DataFrame([relation], columns=relations_df.columns)
                        relations_df = pd.concat([relations_df, relation_df], ignore_index=True)
                    break  # 只加入第一个找到的实体对

    return relations_df


def extract_negative_samples_in_sentence(doc, distance_threshold=25, filename="", negation_words=None):
    if negation_words is None:
        negation_words = ["not", "never", "no"]

    def is_relation_added(relation, relations_df):
        return any((relations_df['Filename'] == relation[0]) &
                   (relations_df['Entity2'] == relation[1]) &
                   (relations_df['Entity3'] == relation[2]))

    def get_sentence_of_entity(ent):
        return ent.sent.text.strip() if ent.sent else ""

    def has_geological_formation_between(ents, ent1, ent2):
        start = min(ent1.end_char, ent2.end_char)
        end = max(ent1.start_char, ent2.start_char)
        return any(ent for ent in ents if ent.label_ == "GEOLOGICAL_FORMATION" and ent.start_char >= start and ent.end_char <= end)

    def has_negation_between(text, start_char, end_char, negation_words):
        text_between = text[start_char:end_char]
        return any(neg_word in text_between for neg_word in negation_words)

    relations_df = pd.DataFrame(columns=['Filename', 'Entity2', 'Entity3', 'Entity3Label', 'Sentence', 'RelationType'])

    for sent in doc.sents:
        geological_ents = [ent for ent in sent.ents if ent.label_ == "GEOLOGICAL_FORMATION"]
        proxy_ents = [ent for ent in sent.ents if ent.label_.startswith("GEOLOGICAL_AGE")]

        for ent1 in geological_ents:
            for ent2 in proxy_ents:
                if has_geological_formation_between(sent.ents, ent1, ent2) or has_negation_between(sent.text, ent1.start_char, ent2.end_char, negation_words):
                    relation = (filename, ent2.text, ent1.text, ent2.label_,
                                get_sentence_of_entity(ent1), "Negative Sample")
                    if not is_relation_added(relation, relations_df):
                        relation_df = pd.DataFrame([relation], columns=relations_df.columns)
                        relations_df = pd.concat([relations_df, relation_df], ignore_index=True)

    return relations_df
def extract_negative_samples_in_sentence2(doc, distance_threshold=50, filename="", negation_words=None):
    if negation_words is None:
        negation_words = ["not", "never", "no"]

    def is_relation_added(relation, relations_df):
        return any((relations_df['Filename'] == relation[0]) &
                   (relations_df['Entity2'] == relation[1]) &
                   (relations_df['Entity3'] == relation[2]))

    def get_sentence_of_entity(ent):
        return ent.sent.text.strip() if ent.sent else ""

    # 修改函数以计数地层实体的数量
    def count_geological_formations_between(ents, ent1, ent2):
        start = min(ent1.end_char, ent2.end_char)
        end = max(ent1.start_char, ent2.start_char)
        return sum(1 for ent in ents if ent.label_ == "GEOLOGICAL_FORMATION" and ent.start_char >= start and ent.end_char <= end)

    def has_negation_between(text, start_char, end_char, negation_words):
        text_between = text[start_char:end_char]
        return any(neg_word in text_between for neg_word in negation_words)

    relations_df = pd.DataFrame(columns=['Filename', 'Entity2', 'Entity3', 'Entity3Label', 'Sentence', 'RelationType'])

    for sent in doc.sents:
        geological_ents = [ent for ent in sent.ents if ent.label_ == "GEOLOGICAL_FORMATION"]
        proxy_ents = [ent for ent in sent.ents if ent.label_.startswith("GEOLOGICAL_AGE")]

        for ent1 in geological_ents:
            for ent2 in proxy_ents:
                # 使用修改后的函数并检查是否有2个以上的地层实体
                if count_geological_formations_between(sent.ents, ent1, ent2) > 2 or has_negation_between(sent.text, ent1.start_char, ent2.end_char, negation_words):
                    relation = (filename, ent2.text, ent1.text, ent2.label_,
                                get_sentence_of_entity(ent1), "Negative Sample")
                    if not is_relation_added(relation, relations_df):
                        relation_df = pd.DataFrame([relation], columns=relations_df.columns)
                        relations_df = pd.concat([relations_df, relation_df], ignore_index=True)

    return relations_df

def extract_negative_samples_in_sentence3(doc, distance_threshold=50, filename="", negation_words=None):
    if negation_words is None:
        negation_words = ["not", "never", "no"]

    def is_relation_added(relation, relations_df):
        return any((relations_df['Filename'] == relation[0]) &
                   (relations_df['Entity2'] == relation[1]) &
                   (relations_df['Entity3'] == relation[2]))

    def get_sentence_of_entity(ent):
        return ent.sent.text.strip() if ent.sent else ""

    def count_geological_formations_between(ents, ent1, ent2):
        start = min(ent1.end_char, ent2.end_char)
        end = max(ent1.start_char, ent2.start_char)
        return sum(1 for ent in ents if ent.label_ == "GEOLOGICAL_FORMATION" and ent.start_char >= start and ent.end_char <= end)

    # 新增函数以计数地质年代实体的数量
    def count_geological_ages_between(ents, ent1, ent2):
        start = min(ent1.end_char, ent2.end_char)
        end = max(ent1.start_char, ent2.start_char)
        return sum(1 for ent in ents if ent.label_ == "GEOLOGICAL_AGE" and ent.start_char >= start and ent.end_char <= end)

    def has_negation_between(text, start_char, end_char, negation_words):
        text_between = text[start_char:end_char]
        return any(neg_word in text_between for neg_word in negation_words)

    relations_df = pd.DataFrame(columns=['Filename', 'Entity2', 'Entity3', 'Entity3Label', 'Sentence', 'RelationType'])

    for sent in doc.sents:
        geological_ents = [ent for ent in sent.ents if ent.label_ == "GEOLOGICAL_FORMATION"]
        proxy_ents = [ent for ent in sent.ents if ent.label_.startswith("GEOLOGICAL_AGE")]

        for ent1 in geological_ents:
            for ent2 in proxy_ents:
                # 检查是否有2个以上的地层实体和大于1个的地质年代实体
                if (count_geological_formations_between(sent.ents, ent1, ent2) > 2 and count_geological_ages_between(sent.ents, ent1, ent2) > 1) or has_negation_between(sent.text, ent1.start_char, ent2.end_char, negation_words):
                    relation = (filename, ent2.text, ent1.text, ent2.label_,
                                get_sentence_of_entity(ent1), "Negative Sample")
                    if not is_relation_added(relation, relations_df):
                        relation_df = pd.DataFrame([relation], columns=relations_df.columns)
                        relations_df = pd.concat([relations_df, relation_df], ignore_index=True)

    return relations_df

#下面是距离太大的判为负例
def extract_negative_samples_in_sentence4(doc, distance_threshold=50, filename="", negation_words=None):
    if negation_words is None:
        negation_words = ["not", "never", "no"]

    def is_relation_added(relation, relations_df):
        return any((relations_df['Filename'] == relation[0]) &
                   (relations_df['Entity2'] == relation[1]) &
                   (relations_df['Entity3'] == relation[2]))

    def get_sentence_of_entity(ent):
        return ent.sent.text.strip() if ent.sent else ""

    # 新增检查两个实体之间距离的函数
    def is_distance_greater_than_threshold(ent1, ent2, threshold):
        start = min(ent1.end_char, ent2.end_char)
        end = max(ent1.start_char, ent2.start_char)
        distance = end - start
        return distance > threshold

    relations_df = pd.DataFrame(columns=['Filename', 'Entity2', 'Entity3', 'Entity3Label', 'Sentence', 'RelationType'])

    for sent in doc.sents:
        geological_ents = [ent for ent in sent.ents if ent.label_ == "GEOLOGICAL_FORMATION"]
        proxy_ents = [ent for ent in sent.ents if ent.label_.startswith("GEOLOGICAL_AGE")]

        for ent1 in geological_ents:
            for ent2 in proxy_ents:
                if is_distance_greater_than_threshold(ent1, ent2, distance_threshold):
                    relation = (filename, ent2.text, ent1.text, ent2.label_,
                                get_sentence_of_entity(ent1), "Negative Sample")
                    if not is_relation_added(relation, relations_df):
                        relation_df = pd.DataFrame([relation], columns=relations_df.columns)
                        relations_df = pd.concat([relations_df, relation_df], ignore_index=True)

    return relations_df
#包含古生物代表的沉积相
#250203
def extract_geological_facies_fm_in_sentence(doc, distance_threshold=50, filename=""):
    def is_relation_added(relation, relations_df):
        return any((relations_df['Filename'] == relation[0]) &
                   (relations_df['Entity2'] == relation[1]) &
                   (relations_df['Entity3'] == relation[2]))

    def get_sentence_of_entity(ent):
        return ent.sent.text.strip() if ent.sent else ""

    relations_df = pd.DataFrame(columns=['Filename', 'Entity2', 'Entity3', 'Entity3Label', 'Sentence', 'RelationType'])

    for sent in doc.sents:
        geological_ents = [ent for ent in sent.ents if ent.label_ == "GEOLOGICAL_FORMATION"]
        #proxy_ents = [ent for ent in sent.ents if ent.label_.startswith("FACIES") or ent.label_.startswith("FOSSIL")]
        proxy_ents = [ent for ent in sent.ents if ent.label_.startswith("FOSSIL")]
        for ent1 in geological_ents:
            for ent2 in proxy_ents:
                # 检查距离是否在阈值范围内
                if abs(ent1.start - ent2.end) <= distance_threshold or abs(ent2.start - ent1.end) <= distance_threshold:
                    relation = (filename, ent2.text, ent1.text, ent2.label_,
                                get_sentence_of_entity(ent2), "Proximity Relation")
                    if not is_relation_added(relation, relations_df):
                        relation_df = pd.DataFrame([relation], columns=relations_df.columns)
                        relations_df = pd.concat([relations_df, relation_df], ignore_index=True)
                    break  # 只加入第一个找到的实体对

    return relations_df

def save_relations_to_excel(relations, file_name='geological_relations.xlsx'):
    df = pd.DataFrame(relations, columns=["filename",'Geological Formation', 'Geological Age', 'Geological Type', 'Sentence',
                                          "Relation-Ruler"])
    df.to_excel(file_name, index=False)


def GeoEntityRecognize2(s):
    if "merge_entities" not in nlp.pipe_names:
        nlp.add_pipe("merge_entities")
#    if "merge_noun_chunks" not in nlp.pipe_names:
 #       nlp.add_pipe("merge_noun_chunks")
    docs=nlp.pipe(s)
    return docs