# cptagger API 接口文档

## 概述

`CPTagger` API 提供了一个文本处理接口，可对输入的文本进行分析并返回处理结果。该接口支持批量处理，即可以一次性提交多个文本进行处理。

## 接口说明

- **接口地址**: `http://124.223.103.195:5003/cptagger`
- **请求方法**: `POST`
- **数据格式**: `JSON`

## 请求参数

| 参数名    | 类型                | 是否必填 | 默认值 | 描述                                      |
| --------- | ------------------- | -------- | ------ | ----------------------------------------- |
| texts     | `string` 或 `list`  | 是       | 无     | 待处理的文本，支持单个字符串或字符串列表。 |
| threshold | `number`            | 否       | 1.00     | 机器学习得分阈值，阈值为1时即为纯字典匹配方法。|
| nest      | `boolean`（可选）   | 否       | False     | 是否保留嵌套实体                         |

### 参数详细说明

- **texts**

  - 类型：`string` 或 `list`
  - 描述：待处理的文本内容。可以是单个字符串，处理一个单个医学文本；也可以是字符串列表，批量处理多个医学文本。
  - 注意：该参数不能为空。如果为空，接口将返回错误信息。

- **threshold**

  - 类型：`number`
  - 描述：机器学习得分阈值，范围为`(0,1]`，建议设置在0.9及以上。默认为1.00，即为纯字典匹配方法。
  - 注意：纯字典匹配方法速度相对较快，若使用非纯字典匹配方法，识别一段100字左右的医学文本大概需要耗费5~10秒。

- **nest**

  - 类型：`boolean`
  - 描述：指示是否进行嵌套处理。若nest为True，则识别并保留嵌套HPO实体，否则在final_list中，仅保留span最长的实体。

## 请求示例

### 示例 1：处理单个文本(推荐测试方法)

```json
{
    "texts": "<医学病历1>",
    "threshold": 0.95,
    "nest": false
}
```

### 示例 2：处理多个文本

```json
{
    "texts": ["<医学病历1>", "<医学病历2>", "..."],
    "threshold": 1,
    "nest": true
}
```


## 响应结果

- 成功时，返回处理结果的列表，每个元素对应于输入文本列表中的一个文本的处理结果。
- 失败时，返回包含错误信息的 JSON 对象。
- 注意：当阈值设为1时，`dict_result` 和 `final_result` 也可能不完全相同，因为可能进行了嵌套实体处理。


### 成功响应示例

```
[
    {
        "ori_text": <原始文本1>,
        "process_text": <用于识别的文本1>,
        "dict_result": { 
            /* 字典识别结果 */
        },
        "ml_result": { 
            /* 机器学习识别结果 */
        },
        "final_result": { 
            /* 集成结果 */
        },
    },
    {
        "ori_text": <原始文本2>,
        "process_text": <用于识别的文本2>,
        "dict_result": { 
            /* 字典识别结果 */
        },
        "ml_result": { 
            /* 机器学习识别结果 */
        },
        "final_result": { 
            /* 集成结果 */
        },
    },
]

```

### 识别结果字典

```
results["final_result"] = {[[start_position, end_position], text, HPO_id, HPO_name, CHPO_name, score, label]}
```

- `[start_position, end_position]`: 该HPO实体在`process_text`中的起始位置。
- `text`: `[start_position, end_position]`间的文本片段。
- `HPO_id`: 该HPO实体对应的HPO编码。
- `HPO_name`：该HPO实体的英文名称。
- `CHPO_name`：该HPO实体的中文名称。
- `score`: 实体得分。字典匹配分数为1.00，非字典匹配下限由`threshold`决定。
- `label`: 实体是否被否定词修饰。若为`pos`则未被否定词修饰，若位`neg`则被否定词修饰(可以选择过滤掉该HPO实体)。
