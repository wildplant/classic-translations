# Classic Translations — 经典神学与哲学重译项目规范

本项目用于 C. S. 路易斯（C. S. Lewis）《荣耀之重：暨其他演讲》（*The Weight of Glory and Other Addresses*）及其他神学/哲学经典文献的**英文原稿 · 旧译本 · 2026 精研新译本**三栏逐段对勘与重译。

---

## 一、 翻译与校勘准则（强制执行）

1. **圣经引文一律采用中文和合本（神版）**
   - 凡路易斯在文中直接引用或明显化用（allusion）《圣经》经文之处（原稿多据 KJV 或公祷书），中文新译本必须核查并严格采用**中文和合本（神版）**标准经文（如“互相联络作肢体”、“不可停止聚会”、“手能拿蛇；若喝了什么毒物，也必不受害”、“神是不偏待人”、“惟有基督在我们还作罪人的时候为我们死”、“你们得救是本乎恩”、“新造的人”、“因为凡祈求的，就得着”等）。
2. **英文底本勘误与补阙**
   - 网络流传的英文底本常有 OCR 错字（如将 `the New Man` 误作 `the New Alan`）或漏段漏句（如 `lewissociety.org` 漏收《核心圈》第 11 段全文及第 14 段半句）。新译前必须与原书旧译逐句比对，一旦发现英文网页底本缺失或讹误，须查考原刊定本补齐校正。
3. **旧译对勘与核心订误（Critiques）**
   - 每篇须提炼 **6 ~ 10 处**关键概念辨析与旧译订误（写入 `data.json` 的 `critiques` 数组），涵盖：神学/法学/古典哲学专有术语（如 `legal fiction` 法律拟制、`share no predicate save by analogy` 类比谓词、`accident vs. essence` 偶性与本质）、圣经引文还原、军制/学制/典故订误。
4. **自然段严格对齐**
   - 以原书自然段为基准（`#01`, `#02`, ...），确保英文、旧译、新译三栏在 `paragraphs` 数组中严格按自然段一一对齐，不留碎片补丁行。
5. **学术注释传承与扩充**
   - 完整保留旧译本有价值的文献出处与思想史背景注释，对旧译注中的事实错误或偏颇之处在注释中予以温和订正；在 `data.json` 正文内统一使用 `[fn:N]` 标记角标。

---

## 二、 目录结构与工作流

```text
classic-translations/
├── AGENTS.md                  # 项目翻译准则、工作流与底本索引
├── glossary.md                # 核心神学与哲学术语统一译名表
├── build.py                   # 零依赖构建脚本（生成 dist/*.html 与 articles/*/*.md）
├── sources/
│   └── 荣耀之重_CS路易斯.epub  # 2016 华东师范大学出版社（邓军海译）EPUB 底本
├── articles/
│   ├── 01-the-inner-ring/     # 《核心圈》（旧译《话圈内》）
│   │   ├── data.json          # 唯一事实源（含元数据、对勘卡片、分段三栏文本、尾注）
│   │   ├── en.md              # 构建脚本自动生成的英文底本文稿 Markdown
│   │   ├── new-zh.md          # 构建脚本自动生成的 2026 纯净新译本 Markdown
│   │   └── old-zh.md          # 构建脚本自动生成的旧译本归档 Markdown
│   └── 02-membership/         # 《互为肢体》（旧译《和而不同》）
│       ├── data.json
│       ├── en.md
│       ├── new-zh.md
│       └── old-zh.md
├── templates/
│   ├── reader.html            # 三栏逐段对照研读器模板（含4套主题、全文检索、抽屉注释、分栏开关）
│   └── index.html             # 书目总览主页模板
└── dist/                      # 最终产物（每个 HTML 均为零依赖自包含单文件，可直接离线传阅）
    ├── index.html             # 研读馆总目录页
    ├── the-inner-ring.html    # 《核心圈》三栏逐段对照研读本
    └── membership.html        # 《互为肢体》三栏逐段对照研读本
```

### 常用命令

```bash
# 重新生成所有单文件 HTML 研读本、总目录页与各篇 Markdown 文稿
python3 build.py
```

---

## 三、 《荣耀之重：暨其他演讲》EPUB 底本章节映射表

底本路径：`sources/荣耀之重_CS路易斯.epub`

| 篇序 | 英文原题 | 演讲年份 | 2026 新译篇名 | 旧译篇名 | EPUB 正文文件 | EPUB 注释文件 | 状态 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 一 | *The Weight of Glory* | 1941 | 荣耀之重 | 一 荣耀之重 | `OEBPS/Text/Section0004.xhtml` | `Section0005.xhtml` | 待译 |
| 二 | *Learning in War-Time* | 1939 | 战时求学 | 二 战时求学 | `OEBPS/Text/Section0006.xhtml` | `Section0007.xhtml` | 待译 |
| 三 | *Why I Am Not a Pacifist* | 1940 | 我为何不是和平主义者 | 三 我缘何不是和平主义者 | `OEBPS/Text/Section0008.xhtml` | `Section0009.xhtml` | 待译 |
| 四 | *Transposition* | 1944 | 高下转调 | 四 高下转换 | `OEBPS/Text/Section0010.xhtml` | `Section0011.xhtml` | 待译 |
| 五 | *Is Theology Poetry?* | 1944 | 神学是诗吗？ | 五 神学是诗？ | `OEBPS/Text/Section0012.xhtml` | `Section0013.xhtml` | 待译 |
| 六 | *The Inner Ring* | 1944 | **核心圈** | 六 话圈内 | `OEBPS/Text/Section0014.xhtml` | `Section0015.xhtml` | **已完成** (`01-the-inner-ring`) |
| 七 | *Membership* | 1945 | **互为肢体** | 七 和而不同 | `OEBPS/Text/Section0016.xhtml` | `Section0017.xhtml` | **已完成** (`02-membership`) |
| 八 | *On Forgiveness* | 1947 | 论饶恕 | 八 论赦免 | `OEBPS/Text/Section0018.xhtml` | `Section0019.xhtml` | 待译 |
| 九 | *A Slip of the Tongue* | 1956 | 说走了嘴 | 九 说漏了嘴 | `OEBPS/Text/Section0020.xhtml` | `Section0021.xhtml` | 待译 |
