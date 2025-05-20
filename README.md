# PlagiarismDetector  基于Levenshtein距离的文本抄袭检测工具

本项目使用Levenshtein距离算法来计算两个文本文件之间的相似度，辅助进行简单的抄袭检测。

## 什么是Levenshtein距离?

Levenshtein距离，又称编辑距离，是指两个字串之间，由一个转成另一个所需的最少编辑操作次数。允许的编辑操作包括将一个字符替换成另一个字符，插入一个字符，删除一个字符。

## 功能

- 读取两个指定的文本文件。
- 对文本进行预处理（转小写、去标点、去多余空白）。
- 计算预处理后文本的Levenshtein距离。
- 将距离转换为0%-100%的相似度得分。
- 输出距离和相似度。

## 效果图

![image](https://github.com/user-attachments/assets/d9654225-2347-4ef8-817e-9781b2b34820)

![image](https://github.com/user-attachments/assets/fadf1ccc-c136-4eee-b554-352d959675d1)

![image](https://github.com/user-attachments/assets/8bac095d-25ab-4662-892b-023882b34dfc)
