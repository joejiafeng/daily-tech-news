# Daily Tech News | 2026-01-25

特斯拉纯视觉 FSD 成功实现零接管横跨美国，验证了马斯克“计算冗余优于传感器冗余”的技术路线；存储市场迎来巨震，三星电子宣布将 NAND 闪存价格上调 100%。AI 编程工具持续进化，OpenAI 启动 Codex 发布月，开发者正迎来效率革命。

## 1. 今日必读

- [FSD 纯视觉路线要赢了](https://www.v2ex.com/t/1188147) (V2EX)
    特斯拉车主在冬季恶劣天气下，成功实现从洛杉矶到纽约的 100% 无人接管驾驶。事实证明仅用摄像头的纯视觉路线已能通过计算冗余替代传感器冗余，马斯克的低成本大规模部署策略展现出压倒性优势。

- [报道称三星电子将一季度 NAND 价格上调 100%](https://36kr.com/newsflashes/3654461246464132?f=rss) (36kr)
    三星电子在今年第一季度将 NAND 闪存供应价格上调了 100% 以上，远超市场预期。这是继 DRAM 价格上调近 70% 后的又一重磅信号，凸显了半导体市场严重的供需失衡现状。

- [报道：OpenAI 意欲从 Anthropic 手中争夺企业客户](https://36kr.com/newsflashes/3654310514204809?f=rss) (36kr)
    OpenAI 首席执行官奥特曼召集迪士尼等企业高管，明确传递布局企业市场的信号。公司旨在成为满足企业所有 AI 需求的一站式服务商，正积极从竞争对手 Anthropic 手中争夺市场份额。

- [因做不出差异化，vivo 叫停 AI 眼镜项目](https://36kr.com/p/3651349127651465?f=rss) (36kr)
    vivo 已秘密筹备半年的 AI 眼镜项目被叫停，此前已与多家 ODM 厂商合作 Demo。叫停原因在于未能做出差异化，这揭示了当前 AI 眼镜行业面临的同质化困境和产品定义难题。

- [北大登顶全球具身智能，董豪团队助力机器人领域突破](https://36kr.com/newsflashes/3654390621134984?f=rss) (36kr)
    在最新 CSRankings 排名中，北京大学在具身智能赛道位列全球榜首，机器人领域排名跃升至第 13 位。这一突破主要归功于董豪团队在顶级会议和期刊上的大量高质量论文产出。

## 2. 趋势与解读

- [David Patterson: Challenges and Research Directions for LLM Inference Hardware](https://arxiv.org/abs/2601.05047) (Hacker News)
    图灵奖得主 David Patterson 发布论文，探讨 LLM 推理硬件面临的挑战与研究方向。随着 AI 模型规模扩大，现有硬件架构在能效和成本上遭遇瓶颈，亟需新的专用架构和内存技术来支撑推理需求。

- [Google confirms 'high-friction' sideloading flow is coming to Android](https://www.androidauthority.com/google-sideloading-android-high-friction-process-3633468/) (Hacker News)
    谷歌确认将在 Android 系统中引入“高摩擦”的侧载流程，以应对欧盟《数字市场法案》要求。这一举措旨在平衡开放性与安全性，但可能会增加用户安装第三方应用的难度，引发开发者社区对平台控制的担忧。

- [死磕机器人大脑的北大副教授，和我们聊了聊具身领域最大的“偏见”](https://36kr.com/p/3653424523682183?f=rss) (36kr)
    北京大学副教授卢宗青提出 2026 年具身智能将呈现“软硬分化”趋势。即模型大脑与机器人本体将由不同公司各司其职，这种专业化分工有望加速具身智能技术的商业化落地和产业成熟。

- [OpenAI 启动 Codex 发布月](https://36kr.com/newsflashes/3654125799055750?f=rss) (36kr)
    OpenAI 宣布接下来一个月将推出多款与 Codex 相关的产品，标志着智能编程辅助生态系统的进一步成熟。随着 AI 编程能力的提升，软件开发流程正面临重构，开发者需适应与 AI 协作的新模式。

- [AI 热潮点燃金属需求，市场预测铜今年仍将供不应求](https://36kr.com/newsflashes/3654135638876544?f=rss) (36kr)
    受机器人、电动汽车及 AI 数据中心发展的驱动，金属价格持续走高。市场预测今年铜供应缺口将比 2025 年更加严重，AI 基础设施建设正在对实体经济资源产生深远且实质性的影响。

## 3. 工具与深读

- [C 盘救星！这神器让我的 SSD 原地复活， 10 分钟用释放 100GB 可用空间](https://www.v2ex.com/t/1188158) (V2EX)
    推荐开源工具 WindowsClear，专注于释放 AppData 目录占用的巨量空间。它能智能扫描并一键迁移软件数据文件夹到其他磁盘，通过创建目录联接确保软件无缝运行，有效解决 C 盘爆满问题。

- [Show HN: VM-curator – a TUI alternative to libvirt and virt-manager](https://github.com/mroboff/vm-curator) (Hacker News)
    VM-curator 是一个基于 QEMU/KVM 的 TUI 虚拟机管理工具，旨在替代 libvirt 和 virt-manager。它解决了 virt-manager 对 NVIDIA 3D 加速支持不佳的问题，为桌面虚拟化提供了更轻量、灵活的解决方案。

- [Small Kafka: Tansu and SQLite on a free t3.micro](https://blog.tansu.io/articles/broker-aws-free-tier) (Hacker News)
    介绍如何在 AWS 免费层 t3.micro 实例上运行 Tansu 和 SQLite 构建的小型 Kafka 方案。这为开发者提供了一个低成本、轻量级的消息队列解决方案，适合开发测试或小规模应用场景。

- [Claude Code's new hidden feature: Swarms](https://twitter.com/NicerInPerson/status/2014989679796347375) (Hacker News)
    Claude Code 被发现新增了一个名为“Swarms”的隐藏功能。虽然具体细节尚未完全公开，但该名称暗示了多智能体协作能力的增强，可能进一步提升 AI 辅助编程的自动化水平和复杂任务处理能力。

- [Mac 视觉史（四）：用动效交互为 Mac OS X 附魔](https://sspai.com/post/105410) (sspai)
    文章回顾了 Mac OS X 如何通过液态、半透明等动效交互设计为系统“附魔”。尽管初期消耗资源，但这些设计定义了现代操作系统的交互美学，值得开发者和设计师深入了解其设计理念与演变历程。
