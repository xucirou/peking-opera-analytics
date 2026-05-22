# 数据交接说明 — 成员D致A、B、C

## 总览：你们的数据会变成什么

我负责的系统是一个**纯前端单页应用**（HTML + ECharts + D3.js），所有图表从 `data/` 目录下的 JSON 文件读取数据。你们只需要按约定格式把数据放进对应的 JSON 文件，系统即可自动渲染全部可视化。

系统共6个页面：总览 → 行当分析 → 角色关系网络 → 主题分析 → 叙事结构 → 综合分析。左侧栏有**剧目、年代、类型**三个全局筛选器，切换后所有页面同步联动。

---

## 一、致成员A — 行当分析数据

### 1.1 你需要交付的文件

`data/roles.json`

### 1.2 字段清单与格式

```json
{
  "archetype_hierarchy": {
    "生": { "description": "男性角色", "subtypes": ["老生", "小生", "武生", "红生", "娃娃生"] },
    "旦": { "description": "女性角色", "subtypes": ["青衣", "花旦", "刀马旦", "老旦", "武旦", "花衫"] },
    "净": { "description": "花脸角色", "subtypes": ["铜锤花脸", "架子花脸", "武净"] },
    "丑": { "description": "喜剧角色或反派", "subtypes": ["文丑", "武丑", "彩旦"] }
  },

  "period_distribution": [
    {
      "period": "明清",
      "老生": 28, "小生": 15, "武生": 12,
      "青衣": 22, "花旦": 18, "刀马旦": 8,
      "铜锤花脸": 8, "架子花脸": 12,
      "文丑": 10, "武丑": 5
    },
    { "period": "民国", ... },
    { "period": "1949后", ... },
    { "period": "当代", ... }
  ],

  "characters": [
    {
      "id": "char_001",
      "name": "项羽",
      "play_id": "play_001",
      "archetype": "净",
      "sub_archetype": "架子花脸",
      "gender": "男",
      "importance": 0.95,
      "predicted": false,
      "confidence": 1.0
    }
  ],

  "feature_archetype_mapping": [
    { "feature": "豪迈刚烈", "archetype": "净", "strength": 0.92 },
    { "feature": "温婉端庄", "archetype": "青衣", "strength": 0.95 }
  ],

  "prediction_model": {
    "method": "RandomForest + 规则基线",
    "accuracy": 0.87,
    "f1_score": 0.85,
    "features_used": ["性别", "年龄描述", "身份描述", "性格关键词", "唱", "念", "做", "打"]
  }
}
```

### 1.3 字段说明

| 字段 | 必需 | 说明 |
|------|:--:|------|
| `archetype_hierarchy` | **是** | 定义四大行当及其细分。`subtypes` 数组中的名称必须与 `period_distribution` 和 `characters` 中的名称完全一致 |
| `period_distribution[].period` | **是** | 年代标签，固定为 `"明清"` `"民国"` `"1949后"` `"当代"` |
| `period_distribution[].<subtype>` | **是** | 每个细分行当在该年代的角色总数，key名必须与 `archetype_hierarchy` 中的 `subtypes` 一致 |
| `characters[].id` | **是** | **全局唯一**。格式 `char_NNN`。C的网络数据靠这个ID关联角色 |
| `characters[].play_id` | **是** | 必须与 `plays.json` 中的 `id` 一致 |
| `characters[].predicted` | **是** | `true` = 模型推断的行当，`false` = 原本已标注 |
| `characters[].confidence` | **是** | 已标注角色直接填 `1.0` |
| `prediction_model` | 建议 | 用于在系统中展示模型信息 |

**特别注意：**
- `characters[].id` 是**全系统关联角色的唯一键**，C的网络数据中 `nodes[].id` 必须与此处一致
- `importance` 的值建议归一化到 0~1 区间（用出场次数/台词数量等指标归一化）

### 1.4 你的数据会变成这些图表

| 图表 | 位置 | 类型 | 使用的数据字段 |
|------|------|------|---------------|
| 各行当时期分布 | 行当分析页 · 顶部 | 堆叠面积图 | `period_distribution` → 按生/旦/净/丑聚合 |
| 时期×细分行当 | 行当分析页 · 左下 | 热力图 | `period_distribution` → 全部细分 |
| 特征→行当映射 | 行当分析页 · 右下 | 水平条形图（颜色=行当） | `feature_archetype_mapping` |
| 特征-行当关联强度 | 行当分析页 · 底部 | 雷达图 | `feature_archetype_mapping` 中取 top 特征 |

**交互：** 在行当分析页悬停面积图中的行当系列会高亮对应区域；热力图可用滑块筛选数值范围。

---

## 二、致成员C — 角色关系网络数据

### 2.1 你需要交付的文件

`data/network.json`

### 2.2 字段清单与格式

```json
{
  "plays": {
    "play_001": {
      "play_title": "霸王别姬",
      "play_type": "历史戏",
      "nodes": [
        {
          "id": "char_001",
          "name": "项羽",
          "archetype": "净",
          "sub_archetype": "架子花脸",
          "gender": "男",
          "importance": 0.95,
          "community": 1
        }
      ],
      "edges": [
        {
          "source": "char_001",
          "target": "char_002",
          "weight": 10,
          "type": "爱情"
        }
      ]
    }
  },

  "network_metrics": [
    {
      "play_id": "play_001",
      "play_title": "霸王别姬",
      "play_type": "历史戏",
      "node_count": 8,
      "edge_count": 10,
      "density": 0.357,
      "avg_degree": 2.5,
      "avg_clustering": 0.52,
      "avg_path_length": 1.8,
      "diameter": 3,
      "modularity": 0.48,
      "community_count": 2,
      "top_centrality_character": "项羽",
      "top_centrality_value": 0.72
    }
  ],

  "type_comparison": [
    {
      "play_type": "历史戏",
      "avg_density": 0.31,
      "avg_clustering": 0.44,
      "avg_modularity": 0.50,
      "sample_count": 4
    }
  ],

  "relationship_types": ["爱情", "亲属", "君臣", "对立", "友谊", "其他"]
}
```

### 2.3 字段说明

| 字段 | 必需 | 说明 |
|------|:--:|------|
| `plays.<play_id>` | **是** | 每个剧本一个key，key名必须与 `plays.json` 的 `id` 一致。目前占位数据覆盖了4部 |
| `nodes[].id` | **是** | 必须与A的 `roles.json` → `characters[].id` 完全一致 |
| `nodes[].community` | **是** | Louvain或其他社区检测算法输出的社区编号（整数） |
| `edges[].source` / `target` | **是** | 值为 `nodes[].id` |
| `edges[].type` | **是** | 关系类型，固定使用：`"爱情"` `"亲属"` `"君臣"` `"对立"` `"友谊"` `"其他"` |
| `edges[].weight` | **是** | 关系强度（如共现场次+对话次数），系统用这个值控制边的粗细 |
| `network_metrics` | **是** | 每个剧本一条记录 |
| `type_comparison` | **是** | 按剧目类型（历史戏/家庭戏/公案戏）汇总的结构指标均值 |

**特别注意：**
- `nodes[].id` 和 `edges[].source`/`target` 必须与A的 `characters[].id` 严格一致，系统用这个ID做跨模块关联
- 即使某个剧本的角色没有出现在A的预测结果中（比如全是已标注角色），也需要给它分配一个与A一致的 `id`
- 建议至少覆盖4部以上剧本，每种剧目类型至少1部

### 2.4 你的数据会变成这些图表

| 图表 | 位置 | 类型 | 使用的数据字段 |
|------|------|------|---------------|
| 角色关系网络 | 网络分析页 · 左侧 | D3力导向图 | 当前选中剧本的 `nodes` + `edges` |
| 网络指标对比 | 网络分析页 · 右侧 | 多系列柱状图 | `network_metrics` → density/avg_clustering/modularity |
| 类型结构对比 | 网络分析页 · 左下 | 分组柱状图 | `type_comparison` |
| 综合分析-网络 | 综合分析页 · 左上 | ECharts力导向图 | 当前选中剧本的 `nodes` + `edges`（缩小版） |

**网络图的交互：**
- 拖拽节点调整布局
- 悬停显示角色名、行当、重要度
- **点击节点**高亮其所有邻居（其他节点和边变暗）
- 点击空白区域恢复全局视图
- 节点颜色 = 行当（生:黛蓝、旦:朱砂、净:琥珀金、丑:青绿）
- 节点大小 = `importance`
- 边粗细 = `weight`
- 边颜色 = 关系类型（爱情:朱砂、对立:深红、亲属:青绿、君臣:淡金）

---

## 三、致成员B — 主题分析与叙事结构数据

你需要交付两个文件。

### 3.1 文件一：`data/themes.json`（主题分析）

```json
{
  "theme_labels": [
    "忠义冲突", "爱情悲剧", "官场腐败", "家国情怀", "舍生取义",
    "因果报应", "儿女情长", "权力斗争", "神话幻想", "伦理教化",
    "反抗压迫", "智勇双全", "生离死别", "讽刺批判", "团圆美满"
  ],

  "play_theme_matrix": [
    {
      "play_id": "play_001",
      "play_title": "霸王别姬",
      "play_type": "历史戏",
      "themes": {
        "忠义冲突": 0.25,
        "爱情悲剧": 0.65,
        "权力斗争": 0.55,
        "生离死别": 0.58
      }
    }
  ],

  "theme_cooccurrence": [
    { "theme1": "忠义冲突", "theme2": "舍生取义", "weight": 0.82 },
    { "theme1": "爱情悲剧", "theme2": "生离死别", "weight": 0.75 }
  ],

  "theme_clusters": [
    {
      "cluster_id": 1,
      "label": "家国大义",
      "themes": ["忠义冲突", "舍生取义", "家国情怀", "权力斗争", "反抗压迫", "智勇双全"],
      "dominant_in": "历史戏"
    },
    {
      "cluster_id": 2,
      "label": "儿女情长",
      "themes": ["爱情悲剧", "儿女情长", "生离死别", "团圆美满", "神话幻想"],
      "dominant_in": "家庭戏"
    },
    {
      "cluster_id": 3,
      "label": "社会批判",
      "themes": ["官场腐败", "讽刺批判", "因果报应", "伦理教化"],
      "dominant_in": "公案戏"
    }
  ]
}
```

**字段说明：**

| 字段 | 必需 | 说明 |
|------|:--:|------|
| `theme_labels` | **是** | LDA提取的所有主题的语义标签，约10~20个 |
| `play_theme_matrix[].play_id` | **是** | 与 `plays.json` 的 `id` 一致 |
| `play_theme_matrix[].themes` | **是** | 该剧本在每个主题上的权重（key: 主题名, value: 0~1的小数）。不必为每个主题都填值，缺失的主题系统视为0 |
| `theme_cooccurrence` | 建议 | 主题两两共现强度（跨剧本统计），用于画主题共现网络。`weight` 建议0~1 |
| `theme_clusters` | **是** | 聚类结果，给出每个群的标签、包含的主题、主导剧目类型 |

**theme_labels 建议：** 由LDA跑出K个主题后，人工根据每个主题的top-15高权重词标注语义标签。这个数组定义了全系统统一使用的主题名称。

### 3.2 文件二：`data/narrative.json`（叙事结构）

```json
{
  "plays": {
    "play_001": {
      "play_title": "霸王别姬",
      "play_type": "历史戏",
      "total_scenes": 8,
      "narrative_pattern": "悲剧递进型",
      "scenes": [
        {
          "scene_id": 1,
          "name": "第一场·出征",
          "sing_ratio": 0.25,
          "speak_ratio": 0.45,
          "action_ratio": 0.25,
          "fight_ratio": 0.05,
          "sentiment": 0.6,
          "tempo": "中"
        }
      ],
      "sentiment_arc": [0.6, 0.4, 0.1, -0.1, -0.3, -0.7, -0.4, -0.8],
      "rhythm_profile": {
        "avg_sing": 0.306,
        "avg_speak": 0.344,
        "avg_action": 0.200,
        "avg_fight": 0.150
      }
    }
  },

  "pattern_comparison": [
    {
      "pattern": "悲剧递进型",
      "description": "情感持续下行，从高潮渐入低谷，常用于英雄悲剧",
      "sentiment_trend": "单调递减",
      "avg_sentiment_range": 1.4,
      "play_count": 2,
      "example": "霸王别姬"
    }
  ],

  "type_rhythm_comparison": [
    {
      "play_type": "历史戏",
      "avg_sing": 0.28,
      "avg_speak": 0.36,
      "avg_action": 0.21,
      "avg_fight": 0.15
    }
  ]
}
```

**字段说明：**

| 字段 | 必需 | 说明 |
|------|:--:|------|
| `plays.<play_id>.scenes` | **是** | 按场次顺序排列，每个元素是一场 |
| `scenes[].sing_ratio` 等四项 | **是** | 该场次中唱/念/做/打的占比，**四值之和必须为1** |
| `scenes[].sentiment` | **是** | 该场次的情感分值，范围 **-1（极悲）到 +1（极喜）** |
| `scenes[].tempo` | 建议 | 该场次的节奏定性：`"快"` `"中"` `"慢"` |
| `sentiment_arc` | **是** | 按场次顺序的情感分值数组（与 `scenes[].sentiment` 一致），用于画情感弧线 |
| `narrative_pattern` | 建议 | 该剧本的叙事模式标签（你归纳的类型名） |
| `rhythm_profile` | 建议 | 该剧本平均唱念做打比例 |
| `pattern_comparison` | 建议 | 把你归纳的叙事模式做一个汇总表，给出每种的描述、情感趋势、情感跨度和代表剧目 |
| `type_rhythm_comparison` | **是** | 按剧目类型汇总唱念做打的均值 |

**特别注意：**
- `sentiment_arc` 是**全系统情感弧线图的核心数据**，长度 = 该剧本的总场次数
- 你不需要覆盖全部12部剧本的叙事数据，但请至少覆盖4部（每种类型至少1部），且必须包含 `play_001`（霸王别姬）、`play_003`（窦娥冤）、`play_005`（铡美案）、`play_006`（牡丹亭）——这4部是综合分析的展示剧目

### 3.3 你的数据会变成这些图表

**主题分析页（子任务③）：**

| 图表 | 类型 | 使用的数据字段 |
|------|------|---------------|
| 剧本×主题权重 | 热力图 | `play_theme_matrix` — 行=剧本，列=主题标签 |
| 主题共现网络 | 力导向网络图 | `theme_cooccurrence` — 节点=主题，边=共现强度 |
| 主题聚类 | 矩形树图 | `theme_clusters` — 外层=三大主题群，内层=具体主题 |
| 主题组合模式 | 雷达图（按剧目类型） | `play_theme_matrix` × `theme_clusters` — 每条线是一种剧目类型 |

**叙事结构页（子任务④）：**

| 图表 | 类型 | 使用的数据字段 |
|------|------|---------------|
| 情感弧线 | 多系列平滑折线图 | 多部剧本的 `sentiment_arc` — 每条线一部剧 |
| 表演节奏 | 堆叠柱状图（唱念做打） | 当前选中剧本的 `scenes` — 每根柱子是一场 |
| 类型节奏对比 | 分组柱状图 | `type_rhythm_comparison` |
| 叙事模式对比 | 水平条形图 | `pattern_comparison` — 条长=情感跨度，颜色=情感趋势 |

**交互：** 情感弧线图在切换剧目时自动更新；节奏堆叠图展示当前选中剧本的逐场节奏构成。

---

## 四、综合分析：我如何把三人的数据联合起来

综合分析页（系统第5页）是本次比赛的核心亮点。它把A、B、C三人的数据在同一个页面中**并置展示并建立逻辑关联**。

### 4.1 页面布局

```
┌─────────────────────────────────────────────────────┐
│  ◆ 联动提示栏                                        │
├──────────────┬──────────────────┬───────────────────┤
│ 角色关系网络  │  主题分布雷达     │  叙事情感弧线      │
│ (C的数据)    │  (B的主题数据)    │  (B的叙事数据)     │
│ ECharts图    │  ECharts雷达图    │  ECharts折线图     │
├──────────────┴──────────────────┴───────────────────┤
│ 行当-主题关联矩阵          │ 网络-叙事-模式关联       │
│ (A的行当 × B的主题群)      │ (C的网络指标 × B的叙事)  │
│ 热力图                     │ 散点图                  │
├────────────────────────────┼─────────────────────────┤
│ 分析故事线                  │ 综合分析结论             │
└────────────────────────────┴─────────────────────────┘
```

### 4.2 联动逻辑

当用户在左侧栏选择一个剧目时：

1. **角色关系网络**（左上）—— 展示该剧目的力导向图。节点颜色=A的行当分类，节点大小=A的importance。边=C的关系类型。
2. **主题分布雷达**（中上）—— 展示该剧目在三大主题群上的分布，数据来自B的 `play_theme_matrix`。
3. **叙事情感弧线**（右上）—— 展示该剧目的情感曲线，数据来自B的 `sentiment_arc`。
4. **行当-主题关联矩阵**（左下）—— 热力图展示四大行当 × 四种叙事模式的关联强度，由我整合A和B的数据计算得出。
5. **网络-叙事-模式关联**（右下）—— 散点图展示每部剧目的网络密度 vs 情感跨度，观察网络结构与叙事模式的对应关系。

**三视图并置的意义：** 当你切换剧目时，你能同时看到"这部剧有哪些角色、他们之间的关系网是怎样的、这部剧讲什么主题、它的情感如何起伏"——角色关系、主题结构、叙事方式三者在一个画面中同时呈现。

### 4.3 需要你们额外配合的事情

| 成员 | 需要做的事 | 原因 |
|------|-----------|------|
| A | `characters[].id` 必须最终确定，并与C同步 | 角色ID是跨模块关联的唯一键 |
| A + C | 核对各剧本的角色列表是否一致（同一角色在A和C的数据中应有相同的id和name） | 网络图中的节点需要从A获取行当颜色 |
| B | `theme_clusters` 需要你根据LDA结果归纳出2~4个主题群，并标注主导剧目类型 | 综合分析页的雷达图按主题群展示 |
| B | `narrative_pattern` 需要你为每部有叙事数据的剧本打上模式标签 | 综合分析页的散点图需要叙事模式作为分类维度 |
| A + B + C | 所有 `play_id` 必须与 `plays.json` 里的 `id` 一致 | 全局筛选器靠 play_id 实现联动 |

### 4.4 我额外需要的综合分析数据

文件 `data/comprehensive.json` 由我来维护，但它依赖你们三人的数据。核心结构如下——你们不需要直接写这个文件，但需要理解我需要从你们的数据中提取什么：

```json
{
  "cross_analysis": {
    "role_theme_correlation": [
      { "archetype": "生", "dominant_themes": ["忠义冲突", "家国情怀"], "correlation_strength": 0.72 }
    ],
    "network_narrative_correlation": [
      { "play_id": "play_001", "network_density": 0.357, "sentiment_range": 1.4,
        "narrative_pattern": "悲剧递进型", "key_finding": "..." }
    ],
    "triple_correlation_matrix": {
      "dimensions": {
        "archetypes": ["生","旦","净","丑"],
        "theme_clusters": ["家国大义","儿女情长","社会批判"],
        "narrative_patterns": ["悲剧递进型","冤案昭雪型","清官断案型","悲欢离合型"]
      },
      "values": [ [...] ]
    }
  }
}
```

这个文件在你们交付数据后由我填充，但它反映的是三个模块数据交叉分析的结果。

---

## 五、数据交付检查清单

在你们各自完成后，请确认以下事项：

- [ ] **plays.json** — 全员确认剧本列表，`id` 作为全局唯一标识不再变动
- [ ] **roles.json** — A确认 `characters[].id` 最终版本，通知C同步
- [ ] **network.json** — C确认所有 `nodes[].id` 与A一致，`edges[].type` 使用约定的6种类型名
- [ ] **themes.json** — B确认 `theme_labels` 和 `theme_clusters` 的语义标签不可再改（改了会破坏综合分析矩阵的维度名）
- [ ] **narrative.json** — B确认至少覆盖4部剧本（每类型至少1部），`sentiment_arc` 长度 = 该剧本场次数
- [ ] 所有JSON文件为合法JSON（可通过 `python -m json.tool file.json` 验证）

**数据放入 `data/` 目录后，运行 `python serve.py` 即可在浏览器中看到完整系统。**

---

## 附：系统配色参考

| 行当 | 色值 | 色名 |
|------|------|------|
| 生 | `#3a6b8c` | 黛蓝 |
| 旦 | `#c1443a` | 朱砂红 |
| 净 | `#d4953a` | 琥珀金 |
| 丑 | `#6b9e6b` | 青绿 |

| 主题群 | 色值 |
|--------|------|
| 家国大义 | `#c1443a` |
| 儿女情长 | `#c96b8a` |
| 社会批判 | `#2d5a8a` |

| 关系类型 | 色值 |
|----------|------|
| 爱情 | `#c1443a` |
| 对立 | `#8b1a1f` |
| 亲属 | `#6b9e6b` |
| 君臣 | `#c9a86c` |
| 其他 | `#c0b8a0` |
