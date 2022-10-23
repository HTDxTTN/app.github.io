from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import firebase_admin
import numpy as np
from firebase_admin import credentials, firestore
#TẢI DỮ LIỆU TỪ FIRESTORE
cred = credentials.Certificate("./iuh-20064751-firebase-adminsdk-tvqy6-09b5c6f6fe.json")
appLoadData = firebase_admin.initialize_app(cred)

dbFireStore = firestore.client()

queryResults = list(dbFireStore.collection(u'tbl-20064751').stream())
listQueryResult = list(map(lambda x: x.to_dict(), queryResults))

df = pd.DataFrame(listQueryResult)
#tải dữ liệu
df['TOTALPRICE'] = df['QUANTITYORDERED']* df['PRICEEACH']
df['PROFIT'] = df['SALES'] - df['TOTALPRICE']
DSBH=df['SALES'].sum()
LN=df["PROFIT"].sum()
DS=df.groupby(['CATEGORY'])['SALES'].sum()
TOPDS=DS.max()
LN1=df.groupby(['CATEGORY'])['PROFIT'].sum()
TOPLN=LN1.max()
# Bieu do
data=df.groupby(['YEAR_ID'])['SALES'].sum().reset_index(name='SALES')
data1=df.groupby(["YEAR_ID"])["PROFIT"].sum().reset_index(name="PROFIT")
data=data.merge(data1)
data2=df.groupby(['CATEGORY', 'YEAR_ID'])['SALES'].sum().reset_index(name='SALES')
data2["YEAR_ID"] = data2["YEAR_ID"].astype("str")
data2["CATEGORY"]=data2["CATEGORY"].astype("str")
data["YEAR_ID"] = data["YEAR_ID"].astype("str")
data3=df.groupby(['CATEGORY', 'YEAR_ID'])['PROFIT'].sum().reset_index(name='PROFIT')
data3["YEAR_ID"] = data3["YEAR_ID"].astype("str")
data3["CATEGORY"]=data3["CATEGORY"].astype("str")
df["QTR_ID"] = df["QTR_ID"].astype("str")
#---------------------------
figDoanhSoBanHang = px.bar(data, x="YEAR_ID", y="SALES", 
 barmode="group", title='Doanh số bán hàng theo năm',
labels={'YEAR_ID':"Năm", 'Sum':'Doanh số bán hàng'})

figLoiNhuanBanHang=px.line(data,x="YEAR_ID",y="PROFIT", title='Lợi nhuận bán hàng theo năm',
labels={'YEAR_ID':'Năm', 'Sum':'Lợi nhuận bán hàng'})

figTyLeDoanhSo= px.sunburst(data2, path=[ 'YEAR_ID','CATEGORY'], values='SALES',
color='SALES',
labels={'parent':'Năm','label':'danh mục','SALES':'Doanh số bán hàng'},
title='Tỉ lệ đóng góp doanh số theo từng danh mục trong từng năm')

figTyLeLoiNhuan= px.sunburst(data3, path=[ 'YEAR_ID','CATEGORY'], values='PROFIT',
color='PROFIT',
labels={'parent':'Năm','label':'danh mục','PROFIT':'Lợi nhuận'},
title='Tỉ lệ đóng góp lợi nhuận theo từng danh mục trong từng năm')
# TRỰC QUAN HÓA DỮ LIỆU WEB APP
app = Dash(__name__)
server = app.server



app.layout=html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="XÂY DỰNG DANH MỤC SẢN PHẨM TIỀM NĂNG" ,className="header-title"
                ),
                html.H1(children="Hà Tùng Dương 20064751" ,className="header-title")
            ],
            className="header"
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H1(children="DOANH SỐ SALES(SINGLE VALUE)",className="h1"),
                        html.H1(children=DSBH,className="h1")
                    ],className="menu-title"
                ),
                html.Div(  children=[
                    html.H1(children="LỢI NHUẬN(SINGLE VALUE)",className="h1"),
                    html.H1(children=LN,className="h1")
                ]
                , className="menu-title")
                ,
                html.Div(  children=[
                        html.H1(children="TOP DOANH SỐ (SINGLE VALUE)",className="h1"),
                        html.H1(children=TOPDS,className="h1")
                    ], className="menu-title")
                ,
                html.Div(  children=[
                        html.H1(children="TOP LỢI NHUẬN(SINGLE VALUE)",className="h1"),
                        html.H1(children=TOPLN,className="h1")
                    ], className="menu-title")
            ], 
            className="menu"
            
        ),
        html.Div(
           children=[
            html.Div(
                children=dcc.Graph(
                    id='doanhso-graph',
                    figure=figDoanhSoBanHang),
                    className="mycard"
            ),
            html.Div(
                 children=dcc.Graph(
                    id='tyleDS-graph',
                    figure=figTyLeDoanhSo),
                    className="mycard"
            ),
            html.Div(
                children=dcc.Graph(
                    id='loinhuan-graph',
                    figure=figLoiNhuanBanHang),
                    className="mycard"
            ),
            html.Div(
               children=dcc.Graph(
                    id='tyleLN-graph',
                    figure=figTyLeLoiNhuan),
                    className="mycard"
            ),
           ],className="wrapper"
        )
    ]
    

)
if __name__ == '__main__':
    app.run_server(debug=True, port=8090)