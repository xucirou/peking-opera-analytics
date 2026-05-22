# 京剧数据可视分析系统

赛题I：数据可视分析与人文创意赛 · 综合可视化系统

## 快速启动

```bash
python serve.py
# 浏览器打开 http://localhost:8080
```

## 系统架构

```
index.html          - 主系统（单页应用，ECharts + D3.js）
data/
├── plays.json      - 共享：剧本题材元数据
├── roles.json      - 成员A：行当分析数据
├── network.json    - 成员C：角色关系网络数据
├── themes.json     - 成员B：主题分析数据
├── narrative.json  - 成员B：叙事结构数据
└── comprehensive.json - 成员D：综合分析关联数据
serve.py            - 本地开发服务器
```

---

## JSON数据格式规范（A/B/C交接文档）

### 1. plays.json — 剧本元数据（全员共用）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 唯一标识，格式 `play_NNN` |
| title | string | 中文剧名 |
| type | string | 剧目类型：历史戏/家庭戏/公案戏 |
| subtype | string | 细分类型 |
| period | string | 年代分类：明清/民国/1949后/当代 |
| year | number | 创作年份 |
| source | string | 来源说明 |
| description | string | 剧情简介（1-2句） |
| scene_count | number | 场次数 |
| character_count | number | 角色数 |

```json
{
  "plays": [
    {
      "id": "play_001",
      "title": "霸王别姬",
      "type": "历史戏",
      "period": "民国",
      "year": 1922,
      "scene_count": 8
    }
  ]
}
```

---

### 2. roles.json — 行当分析（成员A产出）

**archetype_hierarchy**：行当层级定义（生旦净丑及其细分）

**period_distribution**：各时期×各细分行当的角色数量
```json
[
  { "period": "明清", "老生": 28, "小生": 15, "青衣": 22, ... },
  ...
]
```

**characters**：角色列表，每人一条
| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 唯一ID，格式 `char_NNN`（与network.json共用） |
| name | string | 角色名 |
| play_id | string | 所属剧本ID |
| archetype | string | 行当：生/旦/净/丑 |
| sub_archetype | string | 细分支：老生/青衣/花旦… |
| gender | string | 男/女 |
| importance | number | 重要度 0~1 |
| predicted | boolean | 是否为模型预测（true=推断, false=已标注） |
| confidence | number | 预测置信度 0~1，已标注角色填1.0 |

**feature_archetype_mapping**：特征→行当关联强度
```json
[
  { "feature": "豪迈刚烈", "archetype": "净", "strength": 0.92 },
  ...
]
```

---

### 3. network.json — 角色关系网络（成员C产出）

**plays**：按剧本ID为key，每个剧本包含：
- `nodes`：节点数组
  - `id`：与roles.json的characters.id一致
  - `name`：角色名
  - `archetype`/`sub_archetype`：行当信息
  - `importance`：重要度
  - `community`：社区编号（Louvain算法结果）
- `edges`：边数组
  - `source`/`target`：节点ID
  - `weight`：关系强度（共现/对话频次）
  - `type`：关系类型（爱情/亲属/君臣/对立/友谊/其他）

**network_metrics**：跨剧目网络指标对比
| 字段 | 说明 |
|------|------|
| density | 网络密度 |
| avg_clustering | 平均聚类系数 |
| modularity | 模块度 |
| top_centrality_character | 最高中介中心性角色名 |

**type_comparison**：按剧目类型汇总的网络指标均值

```json
{
  "plays": {
    "play_001": {
      "nodes": [
        {"id": "char_001", "name": "项羽", "archetype": "净", "importance": 0.95, "community": 1}
      ],
      "edges": [
        {"source": "char_001", "target": "char_002", "weight": 10, "type": "爱情"}
      ]
    }
  }
}
```

---

### 4. themes.json — 主题分析（成员B产出）

**theme_labels**：主题语义标签列表（LDA主题的人工标注）

**play_theme_matrix**：每部剧本的主题分布向量
```json
[
  {
    "play_id": "play_001",
    "play_title": "霸王别姬",
    "play_type": "历史戏",
    "themes": {
      "忠义冲突": 0.65,
      "爱情悲剧": 0.35,
      ...
    }
  }
]
```

**theme_cooccurrence**：主题共现关系（跨剧本统计）
```json
[
  { "theme1": "忠义冲突", "theme2": "舍生取义", "weight": 0.82 }
]
```

**theme_clusters**：主题聚类结果
```json
[
  {
    "cluster_id": 1,
    "label": "家国大义",
    "themes": ["忠义冲突", "舍生取义", "家国情怀", ...],
    "dominant_in": "历史戏"
  }
]
```

---

### 5. narrative.json — 叙事结构（成员B产出）

**plays**：按剧本ID，每部剧本包含：
- `scenes`：按场次排列
  - `scene_id`：场次编号
  - `name`：场次名称
  - `sing_ratio`/`speak_ratio`/`action_ratio`/`fight_ratio`：唱念做打占比（和为1）
  - `sentiment`：情感分值 -1~1
  - `tempo`：节奏（快/中/慢）
- `sentiment_arc`：情感弧线序列（按场次顺序的情感分值数组）
- `rhythm_profile`：平均节奏构成
- `narrative_pattern`：叙事模式标签

**pattern_comparison**：叙事模式对比

**type_rhythm_comparison**：按剧目类型汇总的节奏均值

```json
{
  "plays": {
    "play_001": {
      "play_title": "霸王别姬",
      "play_type": "历史戏",
      "narrative_pattern": "悲剧递进型",
      "scenes": [
        {"scene_id": 1, "sing_ratio": 0.25, "speak_ratio": 0.45, ...}
      ],
      "sentiment_arc": [0.6, 0.4, 0.1, -0.1, -0.3, -0.7, -0.4, -0.8]
    }
  }
}
```

---

### 6. comprehensive.json — 综合分析关联（成员D整合）

**cross_analysis**：
- `role_theme_correlation`：行当→主题关联
- `network_narrative_correlation`：网络指标→叙事模式关联
- `triple_correlation_matrix`：行当×主题群×叙事模式三维矩阵

```json
{
  "cross_analysis": {
    "triple_correlation_matrix": {
      "dimensions": {
        "archetypes": ["生", "旦", "净", "丑"],
        "theme_clusters": ["家国大义", "儿女情长", "社会批判"],
        "narrative_patterns": ["悲剧递进型", "冤案昭雪型", "清官断案型", "悲欢离合型"]
      },
      "values": [[0.75, 0.30, 0.45, 0.55], ...]
    }
  }
}
```

---

## 可视化方案设计说明

### 成员D采用的可视化形式

| 分析维度 | 可视化方式 | 交互功能 |
|---------|-----------|---------|
| 行当时期分布 | 堆叠面积图 | 鼠标悬停高亮行当 |
| 时期×细分行当 | 热力图 | 值域滑块筛选 |
| 特征→行当映射 | 水平条形图（颜色=行当） | 悬停显示完整特征名 |
| 特征-行当强度 | 雷达图 | — |
| 角色关系网络 | D3力导向图 + ECharts图 | 点击节点高亮邻居；拖拽节点；悬停详情 |
| 网络指标对比 | 多系列柱状图 | 联动剧目选择 |
| 主题权重分布 | 热力图（剧本×主题） | 值域滑块筛选 |
| 主题共现 | 力导向网络图 | 拖拽、缩放 |
| 主题聚类 | 矩形树图 | 钻取 |
| 主题组合模式 | 雷达图（按剧目类型） | — |
| 情感弧线 | 多系列平滑折线图 | 剧目切换联动 |
| 表演节奏 | 堆叠柱状图（唱念做打） | 剧目切换联动 |
| 节奏对比 | 分组柱状图（按类型） | — |
| 叙事模式对比 | 水平条形图 | — |
| 综合分析 | 三联视图 + 散点图 + 热力图 | 全局联动（剧目、年代、类型三个筛选器同步） |

### 联动机制

1. **全局筛选器**（左侧栏）：剧目、年代、类型 — 所有页面同步响应
2. **网络节点点击**：高亮邻居节点和关系边
3. **综合分析页**：角色网络、主题雷达、叙事曲线三视图同步展示，切换剧目时三者同时更新

---

## 运行环境

- Python 3.6+（仅用于静态文件服务）
- 浏览器：Chrome/Firefox/Edge 最新版
- 依赖：CDN加载 ECharts 5.5 + D3.js 7（无需本地安装）
