# CGenerator
Product Comments Automatic Generation

商品评论自动生成

This repo is our final project of course Natural Language Processing in Xi'an Jiaotong University. The model usd in our project is based on [Encoder-Agnostic Adaptation for Conditional Language Generation](https://arxiv.org/abs/1908.06938), Zachary M. Ziegler, Luke Melas-Kyriazi, Sebastian Gehrmann and Alexander M. Rush. The code in this repo is also based on their [code](https://github.com/harvardnlp/encoder-agnostic-adaptation).

## Table of Contents

- [Abstract](#abstract)
- [Dependencies](#dependencies)
- [Data](#data)
- [GPT-2 Pretrained Weights](#GPT-2-pretrained-weights)

## Abstract

With e-commerce entering thousands of families and gradually getting matured, online shopping platforms such as Taobao and JD have played an important role in our lives. From our online shopping experience, it is common for customers to give comments on goods in exchange for cash. However, many people give up such opportunities because they do not want to come up with comments. Based on this phenomenon, we choose the automatic generation of product comments as the direction of out project, striving to generate product comments quickly of multiple categories in order to solve the problem of the customers. 

The GPT-2 model is constructed using the decoder module of the transformer. It is prominent in text generation. The model used in this project is mainly based on GPT-2. It encodes different product categories and integrates the results obtained from the encoding network into the GPT-2 network in the self-attention mechanism, so that generated comments on different types of commodities have different focuses and the automatic generation of comments on multiple commodity types can be more accurate. We obtained the customers’ comments data of various categories of products from JD, and preprocessed the data to obtain customers’ comment data with category labels for model training. Finally, the Flask framework was used to implement building the system, and completed the function which is that if you input the product URL, the comment on the corresponding category of the product can be automatically generated and output the result on the interactive interface.

## Dependencies

This code was tested with `Python3.6` and `Pytorch 1.0.1`. See requirements.txt for a complete list of dependencies.

## Data


## GPT-2 Pretrained Weights


