## 项目目录结构

项目开发的目录结构保持一致，容易理解并方便管理。

## 目录结构

- `/app/` 服务端工作目录

    `/app/controller/` 路由入口Action层

    `/app/common/` 存放公共函数和常量定义

	`/app/dao/` 数据库表实例层

	`/app/service/` 业务逻辑层

- `/uweb/` 管理端工作目录

	`/uweb/custom/` WEB端所需静态文件目录

	`/uweb/lib/` WEB端框架目录

	`/uweb/src/` WEB端开发目录

	`/uweb/src/pages/` WEB端所有页面的目录

	`/uweb/src/plugins/` WEB端自定义插件目录

	`/uweb/src/app.json` WEB端配置文件

	`/uweb/src/app.less` WEB端全局样式文件

	`/uweb/dist/` WEB端打包后的静态文件目录

- `/time_series_detector/` 时间序列异常检测学件目录

	`/time_series_detector/model/` 模型文件存放目录
	
	`/time_series_detector/algorithm/` 算法层

	`/time_series_detector/feature/` 特征层
	
	项目中支持以下类型的文件：
    1. `.json`: 配置文件
    2. `.uwx`: UWEB 视图文件
    3. `.uw`: UWEB 逻辑脚本
    4. `.js`: 普通 JavaScript 逻辑脚本
    5. `.ts`: 普通 TypeScript 逻辑脚本
    6. `.less`: Less 样式文件
    7. `.css`: CSS 样式文件
    8. `.jsx`: 开发自定义插件时可使用的 JavaScript React 脚本文件
    9. `.tsx`: 开发自定义插件时可使用的 TypeScript React 脚本文件
    10. `.png`、`.jpg`、`.gif`、`.svg`: 图片文件 

- `/docs/` 项目文档存放目录


## 调用关系

`uweb` 为管理端工作目录，可调用服务端接口

`/app/controller/` 为服务端路由入口，可调用service业务层

`/app/service/` 为service业务层，可调用私有对象dao数据库层和time_series_detector学件接口

`/time_series_detector/` 学件目录，供service业务层调用

