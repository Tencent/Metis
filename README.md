[Click me switch to English version](README.en.md)

![](docs/images/Metis_logo.png)

[![license](http://img.shields.io/badge/license-BSD3-blue.svg)](https://github.com/tencent/Metis/master/LICENSE.TXT)
[![Release Version](https://img.shields.io/badge/release-0.2.0-red.svg)](https://github.com/tencent/Metis/releases)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/tencent/Metis/pulls)

**Metis** 这个名字取自希腊神话中的智慧女神墨提斯（Metis），它是一系列AIOps领域的应用实践集合。主要解决在质量、效率、成本方面的智能运维问题。当前版本开源的时间序列异常检测学件，是从机器学习的角度来解决时序数据的异常检测问题。

时间序列异常检测学件的实现思路是基于统计判决、无监督和有监督学习对时序数据进行联合检测。通过统计判决、无监督算法进行首层判决，输出疑似异常，其次进行有监督模型判决，得到最终检测结果。检测模型是经大量样本训练生成，可根据样本持续训练更新。

时间序列异常检测学件在织云企业版本中已覆盖 **20w+** 服务器，承载了 **240w+** 业务指标的异常检测。经过了海量监控数据打磨，该学件在异常检测和运维监控领域具有广泛的应用性。

另外：Metis开源项目侧重于学件的实现，利用新的方法改进一些基于规则的运维问题。学件聚焦在局部运维的解决，底层海量数据的存储和流式数据处理框架不在开源范围内，此方面的需求可在交流社区内寻找方案支持。

## 支持平台

目前运行的操作系统平台如下：

- 操作系统：Linux

## 支持语言

目前前后端支持的开发语言如下：

- 前端：JavaScript、TypeScript
- 后端：Python 2.7

## 概览

* [使用场景](docs/usecase.md)
* [代码目录](docs/code_framework.md)
* [代码架构](docs/architecture.md)

## 安装指南

* 初次安装时，请参考安装说明文档 [install.md](docs/install.md)

## 使用指南

* [WEB使用说明](docs/web_userguide.md)
* [API使用说明](docs/api_userguide.md)

## License

Metis的开源协议为BSD 3-Clause License，详情参见 [LICENSE.TXT](LICENSE.TXT)。

## 贡献代码

如果您使用过程中发现问题，请通过 [https://github.com/Tencent/Metis/issues](https://github.com/Tencent/Metis/issues) 来提交并描述相关的问题，您也可以在这里查看其它的 issue ，通过解决这些 issue 来贡献代码。

如果您是第一次贡献代码，请阅读 [CONTRIBUTING](CONTRIBUTING.md) 了解我们的贡献流程，并提交 pull request 给我们。

[腾讯开源激励计划](https://opensource.tencent.com/contribution) 鼓励开发者的参与和贡献，期待你的加入。

## 联系方式

qq技术交流群1群：288723616。

![qq_group](docs/images/qq_group.png)

