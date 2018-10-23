#工业大数据产业创新平台/工业大数据创新竞赛/风机叶片结冰预测大赛

*网址：http://www.industrial-bigdata.com/*

该竞赛为2017年的一个工业大数据应用比赛， 围绕真实采集的风机数据，分为两个比赛题目。本仓库主要关注题目一：风机叶片结冰预测大赛。

由于官网已不再提供完整数据，互联网上也找不到资源，我们特地与对方联系获取了所需的比赛数据，添加到了本仓库的release中。

本仓库部分代码借鉴了[另一个GitHub仓库](https://github.com/BreezeDoo/Industrial_big_data_contest)

###其它备忘：

1. 用2016专业增强版打开15_failureInfo.csv文件会导致时间戳中秒数信息的丢失，其它文件暂未发现该问题；用EditPlus打开不会造成该现象，强烈建议使用EditPlus或其它文本编辑器查看所有的.csv文件
2. 错误认为15_failureInfo.csv没有秒数信息时，编写了脚本addSecTo15Failure.py处理这个问题：将原文件改名为15_failureInfo_raw.csv，运行脚本，得到新的15_failureInfo.csv补充秒数信息（start时间补充为00秒，end时间补充为59秒）。根据1，此脚本实际上是不需要运行的