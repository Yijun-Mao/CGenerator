#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from itertools import repeat
import os
import numpy as np
import json
from flask import Flask,render_template,url_for,request
import joblib
import traceback
import requests
from bs4 import BeautifulSoup
import re

from onmt.utils.logging import init_logger
from onmt.utils.misc import split_corpus
from onmt.translate.translator import build_translator

import onmt.opts as opts
from onmt.utils.parse import ArgumentParser

app = Flask(__name__)

Categories = ["相机", "内存卡", "三脚架","麦克风","行车记录仪","充电器","笔记本电脑","遥控器",
            "音响","手机","智能手表","体脂秤","键盘","鼠标","显示器","打印机","平板电脑","电子书阅读器"]

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')


@app.route('/contact.html')
def contact():
    return render_template('contact.html')

def constraint_iter_func(f_iter):
    all_tags = []
    for json_line in f_iter:
        data = json.loads(json_line)
        words = data['words']
        probs = [p[1] for p in data['class_probabilities'][:len(words)]]
        tags = [1 if p > opt.bu_threshold else 0 for p in probs]
        all_tags.append(tags)
        #print(len(words), len(data['class_probabilities']))
        #all_tags.append(words)
    return all_tags

def _get_parser():
    parser = ArgumentParser(description='translate.py')

    opts.config_opts(parser)
    opts.translate_opts(parser)
    return parser

def extract_category(title):
    min_start = len(title)
    target = None
    for i, category in enumerate(Categories):
        result = re.search(category, title)
        if result is not None:
            result = result.span()
            if result[0] < min_start and result[0] >= 0:
                min_start = result[0]
                target = category
    
    if target is None:
        target = "不知道"
    return target

parser = _get_parser()

opt = parser.parse_args()

model_path = opt.models[0]
step = os.path.basename(model_path)[:-3].split('step_')[-1]
temp = opt.random_sampling_temp

if opt.extra_output_str:
    opt.extra_output_str = '_'+opt.extra_output_str

if opt.output is None:
    output_path = '/'.join(model_path.split('/')[:-2])+'/output_%s_%s%s.encoded' % (step, temp, opt.extra_output_str)
    opt.output = output_path

ArgumentParser.validate_translate_opts(opt)
logger = init_logger(opt.log_file)

translator = build_translator(opt, report_score=True)

BASE_LIB='html5lib'
UA='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
HEADERS={'user-agent':UA}

print("prepared")

@app.route('/index.html',methods=['POST'])
def main():
    
    if request.method == 'POST':

        url= str(request.form['message']).strip()
        if len(url) == 0 or not url.startswith("https://"):
            return render_template('index.html',prediction = "请输入正确的网址")
        resp = requests.get(url, headers=HEADERS) 
        text = resp.text
        soup = BeautifulSoup(text, 'lxml')
        title=soup.title.string[:-16]
        print(title)
        src_shard = extract_category(title)
        print(src_shard)
        try:
            assert src_shard in Categories

            predictions = translator.translate(
                src=[src_shard.encode(encoding = "utf-8")]*opt.batch_size,
                tgt=None,
                src_dir=opt.src_dir,
                batch_size=opt.batch_size,
                attn_debug=opt.attn_debug,
                tag_shard=None
                )
            pred_comments = [prediction[0].replace(" ", "").split("。")[0] for prediction in predictions[1]]
            scores = [-torch_score[0].cpu().item() for torch_score in predictions[0]]
            pred_comment = pred_comments[scores.index(max(scores))]
            print(pred_comments)
            print(scores)
        except:
            traceback.print_exc()
            pred_comment = "不好意思，此类商品暂不支持"
            

    return render_template('index.html',prediction = pred_comment)





if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5500,debug=True)
