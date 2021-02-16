import numpy as np
import pandas as pd
import data
'''
# 컬럼

아래 참조 + 컬럼 하나 추가

#Values    Name      Description
----------------------------------------------------------------------------
   1    type         Describes the type of object: 'Car', 'Van', 'Truck',
                     'Pedestrian', 'Person_sitting', 'Cyclist', 'Tram',
                     'Misc' or 'DontCare'
   1    truncated    Float from 0 (non-truncated) to 1 (truncated), where
                     truncated refers to the object leaving image boundaries
   1    occluded     Integer (0,1,2,3) indicating occlusion state:
                     0 = fully visible, 1 = partly occluded
                     2 = largely occluded, 3 = unknown
   1    alpha        Observation angle of object, ranging [-pi..pi]
   4    bbox         2D bounding box of object in the image (0-based index):
                     contains left, top, right, bottom pixel coordinates
   3    dimensions   3D object dimensions: height, width, length (in meters)
   3    location     3D object location x,y,z in camera coordinates (in meters)
   
   15개에 컬럼만 존재 아래 둘중 하나로 사용될거 같음 
   
   1    rotation_y   Rotation ry around Y-axis in camera coordinates [-pi..pi]
   1    score        Only for results: Float, indicating confidence in
                     detection, needed for p/r curves, higher is better.
    
   파일 확인을 위한 파일 번호 추가
    file_num
    

   Q bbox 부분 좌표 값이라면 x,y 두개에 좌표를 통해서 계산을해야 하는데 하나에 좌표로 구할수 있다?

'''


# label 데이터 읽어 오기
def readData(fileName) :
    # 출력 세팅
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_row', 500)
    pd.set_option('display.max_columns', 100)
    # 경로 및 파일명 지정
    fileName = str(fileName).zfill(6)
    path = open("data/path.txt", 'r', encoding='utf-8').readline()

    data = pd.read_csv(path + "\\" + fileName + ".txt", sep=' ' , header=None )
    # 파일을 확인을 위한 파일명 추가
    data["file_num"] = fileName
    data.columns =test_columns
    return data

# 전체 label를 하나에 csv 파일에 저장
# 1~7481
def saveCSV(num) :
    tot_df = pd.DataFrame(columns=test_columns)

    for no in range(num):
        tot_df = tot_df.append([readData(no)])
    # 파일 내보내기
    tot_df.to_csv("data/tot_label.csv", mode='w')

    
def car_analy(df):
    # occluded 를 통한 비교

    # 80 % : 22993.600000000002 = 22994
    # 20% : 5748.400000000001 = 5748
    print("----------------------------------------------------------------------------------")
    print("전체 car : " , df.loc[(df['type'] == 'Car'), ['type']].count()[0])  # 28742
    print("occluded==0 인 car", df.loc[(df['type'] == 'Car') & (df['occluded'] == 0), ['type']].count()[0])  # 13457
    print("occluded==1 인 car", df.loc[(df['type'] == 'Car') & (df['occluded'] == 1), ['type']].count()[0])  # 8184
    print("occluded==2 인 car", df.loc[(df['type'] == 'Car') & (df['occluded'] == 2), ['type']].count()[0])  # 6173
    print("occluded==3 인 car", df.loc[(df['type'] == 'Car') & (df['occluded'] == 3), ['type']].count()[0])  # 928
    print("----------------------------------------------------------------------------------")

    print("전체 car 파일 0 ~ 5971 사이 존재 개수 : ", df.loc[ (df['type'] == 'Car') & (df['file_num'] <=5971 ) , ['type']].count()[0])
    print("전체 car 파일 5971 ~  사이 존재 개수 : ",df.loc[(df['type'] == 'Car') & (df['file_num'] > 5971), ['type']].count()[0])
    # print(df.loc[(df['type'] == 'Car') & (df['file_num'] <=5971), ['type','file_num','occluded'] ])





if __name__ == '__main__':
    test_columns = ['type', 'truncated', 'occluded', 'alpha', 'bbox_left', 'bbox_top', 'bbox_right', 'bbox_bottom',
                    'dimensions_height', 'dimensions_width', 'dimensions_length', 'location_x', 'location_y',
                    'location_z',
                    'rotation_y', 'file_num']

    # 1번만 실행 (label 데이터 전체를 csv 파일로 저장)+ 파일명 라벨 추가
    #saveCSV(7481)

    # # csv 데이터 읽기
    # # 출력 세팅
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_row', 100)
    pd.set_option('display.max_columns', 17)

    df = pd.read_csv("data/tot_label.csv")
    # print(df.describe())

    # 객체 종류와 갯수 출력
    print(df['type'].value_counts())

    # Car 만 분석
    car_analy(df)