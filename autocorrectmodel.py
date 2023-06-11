#appeler les bibliothèque
from nltk.tokenize import sent_tokenize, word_tokenize
import warnings
import re
import gensim
import Levenshtein

# ignorer les avertissements lors de l'exécution du programme 
warnings.filterwarnings(action = 'ignore')


#la fonction 
def autocorrect(str):
#initialisation et setup
    result=[]
    words=re.findall(r'\w+', str.lower())
    final=words
    context=[]
    with open("context.txt", mode="r",encoding="utf-8") as file:
                for line in file:
                    content=re.findall(r'\w+', line.lower())
                    context.extend(content)



#méthode de similarité de jacard
    for word in words:
        suggestions=[]
        max=0
        for i in context:
            intersection = len(set(word).intersection(set(i)))
            union = len(set(word).union(set(i)))
            jacardsimilarity = intersection / union
            if jacardsimilarity>max and len(i)<=len(word)+2:
                max=jacardsimilarity
        for i in context:
            intersection = len(set(word).intersection(set(i)))
            union = len(set(word).union(set(i)))
            jacardsimilarity = intersection / union
            if jacardsimilarity==max and i not in suggestions:
                suggestions.append(i)
        result.append(suggestions) 
    #print("result of jacard:",result)



    #méthode de distance de levenshtein
    result2=[]
    for i in range (len(result)):
        suggestions2=[]
        min=len(words[i])
        for mot in result[i]:
              distance= Levenshtein.distance(mot, words[i])
              if distance<=min:
                min=distance
        for mot in result[i]:
            if Levenshtein.distance(mot, words[i])==min:
                suggestions2.append(mot)
        result2.append(suggestions2)  
    #print("result of levenshtein:",result2)
    

    #la méthode de la similarité cosinus
       # lire le fichier ‘context.txt’ 
    sample = open("context.txt",  mode="r", encoding="utf-8")
    s = sample.read()
       # Remplace le caractère d'échappement avec espace
    f = s.replace("\n", " ")

    data = []

    # Parcourir chaque phrase du fichier
    for i in sent_tokenize(f):
        temp = []
         # Tokeniser la phrase en mots
        for j in word_tokenize(i):
           temp.append(j.lower())
        data.append(temp)

    # Créer un modèle CBOW
    model1 = gensim.models.Word2Vec(data, min_count = 1, vector_size = 100, window = 5)
    
    for i in range (len(result2)):
        for mot in result2[i]:
            maxnext=0
            maxlast=0
            try:
                if model1.wv.similarity(mot, words[i+1])>maxnext:
                    maxnext=model1.wv.similarity(mot, words[i+1])
                if model1.wv.similarity(mot, words[i-1])>maxlast:
                    maxlast=model1.wv.similarity(mot, words[i+1])
            except:
                continue
        for mot in result2[i]:
            cossim1=cossim2=0
            try: 
                try:
                    try:
                        cossim1=model1.wv.similarity(mot, words[i+1])
                    except:
                        cossim2=model1.wv.similarity(mot, words[i-1])
                except:
                    try:
                        cossim2=model1.wv.similarity(mot, words[i-1])
                    except:
                        cossim1=model1.wv.similarity(mot, words[i+1])
            except:
                continue
                
            if cossim1==maxnext and  cossim2==maxlast:
                final[i]=mot
                break
            if cossim1==maxnext or  cossim2==maxlast:
                final[i]=mot
                break
            
    #le résultat      
    return " ".join(final)
                

#essai
print(autocorrect("I plya in the playgrund"))