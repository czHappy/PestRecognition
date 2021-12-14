from flask import Flask, jsonify, request, render_template
import time
import io,os,base64,sys
sys.path.append("..")
from PIL import Image
from Algorithm import predict
from Database import SQL
from gevent import pywsgi
from conf.config import config
from flask_cors import *  # 导入模块
from Algorithm import prenet_predict
from Algorithm import yolo_pred
import _thread
import time

app = Flask(__name__)



def keep_sql_interactive(threadName, delay):
    while True:
        time.sleep(delay)
        # todo 调用一次查询
        print(threadName)
        sql_helper.keep_interacitve()




@app.route('/detect', methods=['POST', 'GET'])
def get_detect():
    print("detect called!")
    if request.method == 'POST':
        print("detect called!")
        file = request.files['file']  # request的files字段读
        try:
            img_bytes = file.read()  # 二进制图片
            # img = Image.open(io.BytesIO(img_bytes))  # 读图片
            #这里把图片写到固定文件里
            #TODO
            with open('./example.jpg', 'wb') as f:
                f.write(img_bytes)
        except IOError:
            print("store img example fail!")
            return jsonify({})

        yolo_pred.run(detect_model, dev, sql_helper) # 结果存在固定文件里
        # 读txt
        res = {}
        if os.path.exists('./run/detect.txt'):
            with open('./run/detect.txt', 'r') as f:
                for line in f:
                    line = line.strip('\n')
                    tmp = line.split(' ')
                    cls = tmp[0]
                    if cls not in res:
                        res[cls] = sql_helper.query(cls)
                        res[cls]['NUMS'] = 1
                    else:
                        res[cls]['NUMS'] = res[cls]['NUMS'] + 1
        img = open(r'./run/img.png', 'rb')
        res['img'] = base64.b64encode(img.read()).decode()


        return jsonify(res)


#
# @app.route('/', methods=['POST', 'GET'])
# def hello():
#     return render_template("index.html")
# @app.route('/test', methods=['POST', 'GET'])
# def test():
#     return "hello test!"
# 处理client的post请求
@app.route('/predict', methods=['POST', 'GET'])
def get_class():
    if request.method == 'POST':
        print("classify called!")
        file = request.files['file'] # request的files字段读取
        # file.save('./test.jpg')
        try:
            img_bytes = file.read() # 二进制图片
            img = Image.open(io.BytesIO(img_bytes))  # 读图片
            # img = img[:, :, 0:3]
        except IOError:
            print("File is None!")
            return jsonify({})
        st = time.time()
        # 送入前置网络
        flag = prenet_predict.predict(img, pre_model)

        # 根据类别送入不同的网络中0-成虫 1-幼虫 2-卵
        if flag == 0:
            tp3_res = predict.predict(img, model_0, name_list_0) # top3预测结果
        if flag == 1:
            tp3_res = predict.predict(img, model_1, name_list_1)  # top3预测结果
        if flag == 2:
            tp3_res = predict.predict(img, model_2, name_list_2)  # top3预测结果

        ed = time.time()
        print("Complete, cost time: ", ed - st);
        res1 = sql_helper.query(tp3_res[1][0])
        #print('test: ',tp3_res[1][0])
        res2 = sql_helper.query(tp3_res[1][1])
        res3 = sql_helper.query(tp3_res[1][2])

        try:
            print(os.path.join(str(config['dataset']['lib_path']), str(res1['INSECT_CODE']), str(flag), str('0.jpg')))
            print(os.path.join(str(config['dataset']['lib_path']), str(res2['INSECT_CODE']), str(flag), str('0.jpg')))
            print(os.path.join(str(config['dataset']['lib_path']), str(res3['INSECT_CODE']), str(flag), str('0.jpg')))

            img1 = open(os.path.join(str(config['dataset']['lib_path']), str(res1['INSECT_CODE']), str(flag), str('0.jpg')), 'rb')
            img2 = open(os.path.join(str(config['dataset']['lib_path']), str(res2['INSECT_CODE']), str(flag), str('0.jpg')), 'rb')
            img3 = open(os.path.join(str(config['dataset']['lib_path']), str(res3['INSECT_CODE']), str(flag), str('0.jpg')), 'rb')

        except:
            # raise
            print("No such exam img!")
            return jsonify({})

        img1 = base64.b64encode(img1.read()).decode()
        img2 = base64.b64encode(img2.read()).decode()
        img3 = base64.b64encode(img3.read()).decode()

        dict_res = {
                'score1': tp3_res[0][0], 'class1': res1, 'img1': img1,
                'score2': tp3_res[0][1], 'class2': res2, 'img2': img2,
                'score3': tp3_res[0][2], 'class3': res3, 'img3': img3
        }
        print("complete!")


        return jsonify(dict_res)

if __name__ == '__main__':

    config = config.cfg  # 读取配置文件

    detect_model, dev = yolo_pred.pre_process()  # 加载yolo模型
    print('yolo complete!')
    pre_model = prenet_predict.pre_process()

    with open(config['dataset']['class_name_0'], "r") as f:
        class_name = f.read()
    name_list_0 = class_name.split(',')

    with open(config['dataset']['class_name_1'], "r") as f:
        class_name = f.read()
    name_list_1 = class_name.split(',')

    with open(config['dataset']['class_name_2'], "r") as f:
        class_name = f.read()
    name_list_2 = class_name.split(',')

    model_0 = predict.pre_process(flag=0)  # 预读模型
    model_1 = predict.pre_process(flag=1)  # 预读模型
    model_2 = predict.pre_process(flag=2)  # 预读模型

    sql_helper = SQL.SQL_Helper(config['mysql']['config'])  # 初始化SQLhelper
    _thread.start_new_thread(keep_sql_interactive, ("keep mysql interactive...", 14400))
    # app.run("0.0.0.0", 5002, debug=True)
    CORS(app, supports_credentials=True)  # 设置跨域
    server = pywsgi.WSGIServer((config['server']['ip'], config['server']['port']), app)
    print("Server start!")
    server.serve_forever()
