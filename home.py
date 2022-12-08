from PIL import Image as Im
import os
# import webcam
import streamlit as st
from configu import *
# from detect_mask_image import detect
# from db import Video,Image
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import cv2
# from converter import convert_video
# from detect_mask_video import video

def opendb():
    engine = create_engine('sqlite:///db.sqlite3') # connect
    Session =  sessionmaker(bind=engine)
    return Session()

def save_image(file,path):
    try:
        db = opendb()
        file =  os.path.basename(path)
        name, ext = file.split('.') # second piece
        # img = Image(filename=name,extension=ext,filepath=path)
        db.add(img)
        db.commit()
        db.close()
        return True
    except Exception as e:
        st.write("database error:",e)
        return False

st.sidebar.header(PROJECT_NAME)
st.sidebar.write(DONE_BY)

choice = st.sidebar.radio("select option",MENU_OPTION)

if choice == 'About project':
    st.title("About Our Project")
    st.image('IMAGES/about.jpeg')
    st.info('''AGE Detection Platform utilizes Artificial Network to perceive if a person does/doesn't wear a mask.
The application can be associated with any currentor new cameras to identify individuals with/without a mask.
By developing a face mask detection technique,
through which we identify people weared mask or not.
so we suggest people who not weared mask to wear  it to reduce the covid/ any viral disease spread''')
    


if choice == 'Sample dataset':
    st.title("Dataset Samples")
    st.image('IMAGES/about.jpeg')
    st.image('IMAGES/dataset1.jpeg')
    st.image('IMAGES/dataset2.jpeg')
    st.image('IMAGES/dataset3.jpeg')
    


if choice == 'Camera based test':
   st.title("Real time camera based test")
   btn = st.button('start realtime AI camera')
   if btn:
       webcam.load_camera(num=0)


if choice == 'image based test':
    st.title("Upload images for image based test")
    st.subheader('select an image')
    img = st.file_uploader("browse to select",type=['jpg','png','jpeg'])
    if img:
        im = Im.open(img)
        # create a address for image path
        path = os.path.join("images",img.name)
        # save file to upload folder
        im.save(path,format=img.type.split('/')[1])
        status = save_image(img,path)
        if status:
            st.sidebar.success("file uploaded")
            col1 ,col2 = st.beta_columns(2)
            col1.image(path,use_column_width=True,caption='original')
            out_img = detect(path)
            cv2.imwrite(path,out_img)
            col2.image(path,use_column_width=True,caption='prediction')
        else:
            st.sidebar.error('upload failed')

if choice  =='realtime detection':
    st.title("Real time camera based test")
    
    cnf = st.slider('confidence threshold',min_value=.1, max_value=1.0,value=.5)
    btn = st.button("start camera window")
    st.info('Click on start camer window for detection ')
    if btn:
        video(cnf=cnf)
if choice == 'view previous predictions':
    db = opendb()
    results = db.query(Image).all()
    db.close()        