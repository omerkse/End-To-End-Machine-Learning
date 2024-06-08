import streamlit as st
import pandas as pd 
import numpy as np
import joblib
from PIL import Image,ImageEnhance
import matplotlib.pyplot as plt
import seaborn as sns




def main():
    
    st.sidebar.title('Streamlit ile ML Uygulaması')
    selected_page = st.sidebar.selectbox('Sayfa Seçiniz..',["Tahmin Yap"])

    if selected_page == "Tahmin Yap":
        predict()
    

def predict():

    # Markalar ve Modellerin yüklenmesi
    markalar = load_data()
    harita = load_haritalandirma()
    hazne_kap = load_haznekap()
    sarj = load_sarj_sure()
    

    # Kullanıcı arayüzü ve değer alma
    st.title('Merhaba, *Streamlit!* 👨‍💻')
    selected_marka = marka_index(markalar,st.selectbox('Marka Seçiniz..',markalar))
    

    selected_Asilabilir_Engel_Seviyesi = st.number_input('Asilabilir Engel Seviyesi',min_value=0,max_value=10)
    st.write("Asilabilir Engel Seviyesi:"+str(selected_Asilabilir_Engel_Seviyesi)+" CM")

    selected_harita = harita_index(harita,st.selectbox('Haritalandırma türü ..',harita))

    selected_hazne = hazne_index(hazne_kap,st.selectbox('Hazne kapasitesi ..',hazne_kap))
    

    selected_Yer_Silme_Ozelligi = st.slider("yer silme özelliği",min_value=0,max_value=1)
    st.write("yer silme özelliği :"+str(selected_Yer_Silme_Ozelligi)+"var,yok ")

    selected_Uygulama_Uzerinden_Kontrol = st.slider("uygulama üzerinden kontrol",min_value=0,max_value=1)
    st.write("yer silme özelliği :"+str(selected_Uygulama_Uzerinden_Kontrol)+"var,yok ")


    selected_sarj = sarj_index(sarj,st.selectbox('sarj süresi ..',sarj))
    


    selected_model = st.selectbox('Tahmin Modeli Seçiniz..',["KNN","Multiple Linear","Random Forest"])


    prediction_value = create_prediction_value(selected_Asilabilir_Engel_Seviyesi,selected_harita,selected_hazne,selected_Uygulama_Uzerinden_Kontrol,selected_Yer_Silme_Ozelligi,selected_sarj,selected_marka)
    prediction_model = load_models(selected_model)


    if st.button("Tahmin Yap"):
            result = predict_models(prediction_model,prediction_value)
            if result != None:
                st.success('Tahmin Başarılı')
                st.balloons()
                st.write("Tahmin Edilen Fiyat: "+ result + "TL")
            else:
                st.error('Tahmin yaparken hata meydana geldi..!')



def load_data():
    markalar = pd.read_csv("markalar.csv")
    return markalar

def load_haritalandirma():
    harita = pd.read_csv("haritalandirma.csv")
    return harita

def load_haznekap():
    hazne = pd.read_csv("hazne_kapasitesi.csv")
    return hazne

def load_sarj_sure():
    sarj = pd.read_csv("Sarjli_Kullanim_Suresi.csv")
    return sarj


def load_models(modelName):
    if modelName == "KNN":
        knn_model = joblib.load("KNN_model.pkl")
        return knn_model

    elif modelName == "Multiple Linear":
        mlinear_model = joblib.load("multiple_linear_model.pkl")
        return mlinear_model

    elif modelName == "Random Forest":  
        rf_model = joblib.load("random_forest_model.pkl")
        return rf_model

    else:
        st.write("Model yüklenirken hata meydana geldi..!")
        return 0


def marka_index(markalar,marka):
    index = int(markalar[markalar["marka"]==marka].index.values)
    return index

def harita_index(haritalar,harita):
    index1 = int(haritalar[haritalar["Haritalandirma"]==harita].index.values)
    return index1

def hazne_index(hazneler,hazne):
    index2 = int(hazneler[hazneler["Hazne_Kapasitesi"]==hazne].index.values)
    return index2

def sarj_index(sarjler,sarj):
    index3 = int(sarjler[sarjler["Sarjli_Kullanim_Suresi"]==sarj].index.values)
    return index3



def create_prediction_value(Asilabilir_Engel_Seviyesi,harita,hazne,Uygulama_Uzerinden_Kontrol,Yer_Silme_Ozelligi,sarj,marka):
    res = pd.DataFrame(data = 
            {'Asilabilir_Engel_Seviyesi':[Asilabilir_Engel_Seviyesi],
             'Haritalandirma':[harita],
             'Hazne_Kapasitesi':[hazne],
             'Uygulama_Uzerinden_Kontrol':[Uygulama_Uzerinden_Kontrol],
             'Yer_Silme_Ozelligi':[Yer_Silme_Ozelligi],
              'Sarjli_Kullanim_Suresi':[sarj],
              'marka':[marka]})
    return res


def predict_models(model,res):
    result = str(int(model.predict(res)*100)).strip('[]')
    return result



if __name__ == "__main__":
    main()
 