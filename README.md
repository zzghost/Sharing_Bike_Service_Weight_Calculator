# 项目名字  
**共享单车的动态投放**

## 文件说明
**Cluster:**  
数据预处理：筛选短途数据，区分工作日非工作日，划分时间段  
候选投放点：按照上车位置聚类  

**weightCalculater**  
投放点筛选：按照评分标准  

**predict_duration**  
预测投放点转移路线的时间模型  
选择最优转移路线：KM算法

**Demo**  
网页Demo展示：动态投放路线

