import streamlit as st
import torch
from detect import detect
from PIL import Image
from io import *
import glob
from datetime import datetime
import os
import wget
import time

## CFG
cfg_model_path = "models/best.pt" 

cfg_enable_url_download = False
if cfg_enable_url_download:
    url = "https://archive.org/download/yoloTrained/yoloTrained.pt" #Configure this if you set cfg_enable_url_download to True
    cfg_model_path = f"models/{url.split('/')[-1:][0]}" #config model path from url name
## END OF CFG

with open('style.css') as f: 
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)




def imageInput(device, src):
    
    if src == 'Upload your own data.':
        image_file = st.file_uploader("Upload An Image", type=['png', 'jpeg', 'jpg'])
        col1, col2 = st.columns(2)
        if image_file is not None:
            img = Image.open(image_file)
            with col1:
                st.image(img, caption='Uploaded Image', use_column_width='always')
                st.success("Uploaded : "+image_file.name)
            ts = datetime.timestamp(datetime.now())
            imgpath = os.path.join('data/uploads', str(ts)+image_file.name)
            outputpath = os.path.join('data/outputs', os.path.basename(imgpath))
            with open(imgpath, mode="wb") as f:
                f.write(image_file.getbuffer())

            #call Model prediction--
            model = torch.hub.load('ultralytics/yolov5', 'custom', path='models/best.pt', force_reload=True) 
            model.cuda() if device == 'cuda' else model.cpu()
            pred = model(imgpath)
            im,label = pred.render()  # render bbox in image
            print(label)
            for im in pred.ims:
                im_base64 = Image.fromarray(im)
                im_base64.save(outputpath)

            #--Display predicton
            
            img_ = Image.open(outputpath)

            
            with col2:
                st.image(img_, caption='Model Prediction(s) : {}'.format(label), use_column_width='always')
                st.success("Predict : "+label)
                #st.warning(label[:-5].strip() == "Amecican_Shorthair")
                #st.warning(label[:-5].strip())
                if label[:-5].strip() == "Amecican_Shorthair" :
                    desc = """
                    นิสัย 
-ขี้เล่น 
-ร่าเริง
-เป็นมิตร
โรคควรระวัง
-โรคหัวใจ
-โรคทางเดินปัสสาวะและไต
-โรคระบบต่อมไร้ท่อ
                    """
                    st.warning(desc)
                elif label[:-5].strip() == "Khao_manee" :
                    desc = """
นิสัย
-ขี้เล่นขี้สงสัย
-ชอบสำรวจ
-ขี้อ้อนต้องการความรัก
โรคควรระวัง
-โรคผิวหนัง
โรคทางเดินอาหาร
                    """
                    st.warning(desc)
                
                elif label[:-5].strip() == "Korat_cat" :
                    desc = """
                    นิสัย
-ขี้อ้อน
-ชอบเล่นกับคน
-ชี้อิจฉา
โรคควรระวัง
-โรคผิวหนัง
-โรคระบบไหลเวียนโลหิต
-โรคประสาท
                    
                    """
                    st.warning(desc)
                
                elif label[:-5].strip() == "Siamese_cat" :
                    desc = """
                    นิสัย
-ฉลาด
-ขี้อ้อน
-เข้ากับคนง่าย 
โรคควรระวัง
-โรคระบบโครงกระดูก ข้อต่อ
-โรคมะเร็ง
                    """
                    st.warning(desc)
                
                elif label[:-5].strip() == "sphyx":

                    desc = """
                    นิสัย
-คล่องตัวแข็งแรง
-ชอบนอนพักผ่อน
-ขี้เล่น
โรคควรระวัง
-โรคระบบเลือดและภูมิคุ้มกัน\n
-โรคข้ออักเสบ
-โรคระบบผิวหนัง
                    """
                    st.warning(desc)

                st.markdown(f"<script>alert({desc})</script>",unsafe_allow_html=True)
                    
    elif src == 'From test set.': 
        # Image selector slider
        imgpath = glob.glob('data/images/*')
        imgsel = st.slider('Select random images from test set.', min_value=1, max_value=len(imgpath), step=1) 
        image_file = imgpath[imgsel-1]
        submit = st.button("Predict!")
        col1, col2 = st.columns(2)
        with col1:
            img = Image.open(image_file)
            st.image(img, caption='Selected Image', use_column_width='always')
        with col2:            
            if image_file is not None and submit:
                #call Model prediction--
                model = torch.hub.load('ultralytics/yolov5', 'custom', path=cfg_model_path, force_reload=True) 
                pred = model(image_file)
                im,label = pred.render()  # render bbox in image
                for im in pred.ims:
                    im_base64 = Image.fromarray(im)
                    im_base64.save(os.path.join('data/outputs', os.path.basename(image_file)))
                #--Display predicton
                    img_ = Image.open(os.path.join('data/outputs', os.path.basename(image_file)))
                    st.image(img_, caption='Model Prediction(s)')
                    st.success("Predict : "+label)
                if label[:-5].strip() == "Amecican_Shorthair" :
                    desc = """
                    นิสัย 
-ขี้เล่น 
-ร่าเริง
-เป็นมิตร
โรคควรระวัง
-โรคหัวใจ
-โรคทางเดินปัสสาวะและไต
-โรคระบบต่อมไร้ท่อ
                    """
                    st.warning(desc)
                elif label[:-5].strip() == "Khao_manee" :
                    desc = """
นิสัย
-ขี้เล่นขี้สงสัย
-ชอบสำรวจ
-ขี้อ้อนต้องการความรัก
โรคควรระวัง
-โรคผิวหนัง
โรคทางเดินอาหาร
                    """
                    st.warning(desc)
                
                elif label[:-5].strip() == "Korat_cat" :
                    desc = """
                    นิสัย
-ขี้อ้อน
-ชอบเล่นกับคน
-ชี้อิจฉา
โรคควรระวัง
-โรคผิวหนัง
-โรคระบบไหลเวียนโลหิต
-โรคประสาท
                    
                    """
                    st.warning(desc)
                
                elif label[:-5].strip() == "Siamese_cat" :
                    desc = """
                    นิสัย
-ฉลาด
-ขี้อ้อน
-เข้ากับคนง่าย 
โรคควรระวัง
-โรคระบบโครงกระดูก ข้อต่อ
-โรคมะเร็ง
                    """
                    st.warning(desc)
                
                elif label[:-5].strip() == "sphyx":

                    desc = """
                    นิสัย
-คล่องตัวแข็งแรง
-ชอบนอนพักผ่อน
-ขี้เล่น
โรคควรระวัง
-โรคระบบเลือดและภูมิคุ้มกัน\n
-โรคข้ออักเสบ
-โรคระบบผิวหนัง
                    """
                    st.warning(desc)

                st.markdown(f"<script>alert({desc})</script>",unsafe_allow_html=True)


def videoInput(device, src):
    uploaded_video = st.file_uploader("Upload Video", type=['mp4', 'mpeg', 'mov'])
    if uploaded_video != None:

        ts = datetime.timestamp(datetime.now())
        imgpath = os.path.join('data/uploads', str(ts)+uploaded_video.name)
        outputpath = os.path.join('data/video_output', os.path.basename(imgpath))

        with open(imgpath, mode='wb') as f:
            f.write(uploaded_video.read())  # save video to disk

        st_video = open(imgpath, 'rb')
        video_bytes = st_video.read()
        st.video(video_bytes)
        st.write("Uploaded Video")
        detect(weights=cfg_model_path, source=imgpath, device=0) if device == 'cuda' else detect(weights=cfg_model_path, source=imgpath, device='cpu')
        st_video2 = open(outputpath, 'rb')
        video_bytes2 = st_video2.read()
        st.video(video_bytes2)
        st.write("Model Prediction")


def main():
    # -- Sidebar
    st.sidebar.title('⚙️Options')
    datasrc = st.sidebar.radio("Select input source.", ['From test set.', 'Upload your own data.'])
    
        
                
    option = st.sidebar.radio("Select input type.", ['Image', 'Video'])
    if torch.cuda.is_available():
        deviceoption = st.sidebar.radio("Select compute Device.", ['cpu', 'cuda'], disabled = False, index=1)
    else:
        deviceoption = st.sidebar.radio("Select compute Device.", ['cpu', 'cuda'], disabled = True, index=0)
    # -- End of Sidebar

    st.header('📦Cat Classification')
    st.subheader('👈🏽 Select options left-haned menu bar.')
    #st.sidebar.markdown("https://github.com/thepbordin/Obstacle-Detection-for-Blind-people-Deployment")
    if option == "Image":    
        imageInput(deviceoption, datasrc)
    elif option == "Video": 
        videoInput(deviceoption, datasrc)

    

if __name__ == '__main__':
  
    main()

# Downlaod Model from url.    
@st.cache
def loadModel():
    start_dl = time.time()
    model_file = wget.download(url, out="models/")
    finished_dl = time.time()
    print(f"Model Downloaded, ETA:{finished_dl-start_dl}")
if cfg_enable_url_download:
    loadModel()