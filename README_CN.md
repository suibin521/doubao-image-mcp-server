# 豆包图像生成MCP服务器

基于FastMCP框架和火山引擎API实现的图像生成MCP服务器，支持通过豆包(doubao-seedream-3.0-t2i)模型生成高质量图像。

## 1. 功能特点

- 🎨 **高质量图像生成**: 基于豆包seedream-3.0-t2i模型，支持2K分辨率
- 🌐 **中英双语支持**: 提示词支持中英文描述
- 📐 **多种分辨率**: 支持从512x512到2048x2048的多种分辨率
- 🎯 **精确控制**: 支持种子、引导强度、水印等参数控制
- 📁 **本地保存**: 自动下载并保存生成的图像到指定目录
- 🔧 **MCP协议**: 完全兼容MCP协议，可与支持MCP的AI助手集成
- 📊 **详细日志**: 完整的日志记录和错误处理

## 2. 环境要求

- Python >= 3.13
- 火山引擎API密钥
- 推理端点模型ID

## 3. 安装配置

### 3.1 克隆项目

```bash
git clone git@github.com:suibin521/doubao-image-mcp-server.git
cd doubao-image-mcp-server
```

### 3.2 安装方式

#### 方式一：使用 uvx 直接运行（推荐）
```bash
# 直接从 PyPI 安装并运行
uvx doubao_image_mcp_server
```

#### 方式二：使用 uv 安装到项目
```bash
# 安装到当前项目
uv add doubao_image_mcp_server
```

#### 方式三：开发者安装
```bash
# 克隆仓库后，在项目根目录执行
uv sync
# 或使用 pip
pip install -e .
```

#### 方式四：传统 pip 安装
```bash
pip install doubao_image_mcp_server
```

### 3.3 配置环境变量

本项目不使用 `.env` 文件，所有配置通过 MCP JSON 配置文件的 `env` 字段传递。

#### 3.3.1 环境变量配置示例
```json
"env": {
  "BASE_URL": "https://ark.cn-beijing.volces.com/api/v3",
  "DOUBAO_API_KEY": "your-dev-api-key-here",
  "API_MODEL_ID": "ep-20250528154802-c4np4",
  "IMAGE_SAVE_DIR": "C:/images"
}
```

#### 3.3.2 环境变量详细说明

**1. BASE_URL（API基础地址）**
- **作用**: 豆包(火山引擎)平台的API基础地址
- **默认值**: `https://ark.cn-beijing.volces.com/api/v3`
- **说明**: 这是火山引擎平台在北京区域的API地址，一般情况下不需要修改
- **示例**: `"BASE_URL": "https://ark.cn-beijing.volces.com/api/v3"`

**2. DOUBAO_API_KEY（API密钥）**
- **作用**: 用于身份验证的API密钥
- **获取方式**: 从火山引擎控制台创建并获取
- **格式**: 通常是UUID格式的字符串
- **注意**: 请妥善保管你的API密钥，不要泄露给他人

**3. API_MODEL_ID（模型端点ID）**
- **作用**: 指定使用的图像生成模型的推理端点ID
- **获取方式**: 在火山引擎控制台创建推理端点后获得
- **格式**: 以"ep-"开头的字符串
- **示例**: `"API_MODEL_ID": "ep-20250528154802-c4np4"`
- **说明**: 每个推理端点都有唯一的ID，用于标识特定的模型实例

**4. IMAGE_SAVE_DIR（图像保存目录）**
- **作用**: 指定生成图像保存的本地目录路径
- **路径格式**: 支持相对路径和绝对路径
- **绝对路径示例**: `"IMAGE_SAVE_DIR": "C:/images"`
- **说明**: 如果目录不存在，程序会自动创建

### 3.4 获取API密钥和模型ID

#### 3.4.1 注册火山引擎平台

使用以下网址登录火山平台并注册，可在右上角选择语言（中文或英文）：

```
https://console.volcengine.com/auth/signup
```

![注册火山引擎平台](images/volcengine_signup.jpg)

#### 3.4.2 登录火山引擎控制台

注册完成后，访问火山引擎控制台：

```
https://console.volcengine.com/ark/region:ark+cn-beijing/overview?briefPage=0&briefType=introduce&type=new
```

#### 3.4.3 激活图像生成模型"Doubao-Seedream-3.0-t2i"

1. 进入**系统管理** → **开通管理**界面
2. 选择**视觉大模型**
3. 找到**Doubao-Seedream-3.0-t2i**模型
4. 点击右侧的**"开通服务"**按钮激活服务

访问链接：
```
https://console.volcengine.com/ark/region:ark+cn-beijing/openManagement?LLM=%7B%7D&OpenTokenDrawer=false
```

![激活模型服务](images/model_activation.jpg)

#### 3.4.4 创建推理端点

1. 在控制台中，点击**在线推理** → **创建推理端点**
2. 填写以下信息：
   - **端点名称**: 给你的端点起个名字
   - **端点描述**: 添加描述信息
   - **模型选择**: 选择刚才激活的**Doubao-Seedream-3.0-t2i**模型
3. 点击**创建**按钮创建端点
4. 创建完成后，在概览界面可以看到对应的**Model_id**（格式如：`ep-m-20250528154647-cx5fg`）

![创建推理端点](images/create_inference_endpoint.jpg)

#### 3.4.5 创建API密钥

1. 在控制台右侧选择**API Key管理**
2. 点击**创建API Key**
3. 生成并保存你的API密钥（请妥善保管，不要泄露）

![创建API密钥](images/create_api_key.jpg)

#### 3.4.6 配置信息获取完成

完成以上步骤后，你将获得以下配置信息：
- **BASE_URL**: `https://ark.cn-beijing.volces.com/api/v3`（固定值）
- **DOUBAO_API_KEY**: 刚才创建的API密钥
- **API_MODEL_ID**: 推理端点的Model_id（如：`ep-m-20250528154647-cx5fg`）
- **IMAGE_SAVE_DIR**: 图像保存目录路径

## 4. 使用方法

### 4.1 在开发工具中配置MCP服务器

本服务器支持在各种AI开发工具中使用，包括VS Code + Cline、Cursor、Trae等。配置方法如下：

#### 4.1.1 MCP配置文件设置

在你的MCP配置文件中添加以下配置：

```json
{
  "mcpServers": {
    "doubao_image_mcp_server": {
      "command": "uvx",
      "args": [
        "doubao_image_mcp_server"
      ],
      "env": {
        "BASE_URL": "https://ark.cn-beijing.volces.com/api/v3",
        "DOUBAO_API_KEY": "your-dev-api-key-here",
        "API_MODEL_ID": "ep-20250528154802-c4np4",
        "IMAGE_SAVE_DIR": "C:/images"
      }
    }
  }
}
```

#### 4.1.2 开发工具配置说明

**VS Code + Cline：**
- 在VS Code设置中找到Cline扩展配置
- 将上述MCP配置添加到Cline的MCP服务器配置中

**Cursor：**
- 在Cursor设置中找到MCP配置选项
- 添加上述配置并重启Cursor

**Trae：**
- 将上述配置添加到Trae的MCP配置文件中
- 保存后重新加载配置文件

#### 4.1.3 使用示例

配置完成后，你可以直接与AI助手对话来生成图像：

**在Cursor中的使用示例：**
1. 进入Agent模式
2. 先让Cursor了解图像生成工具："请了解可用的图像生成工具"
3. 然后直接提出图像生成请求："请帮我生成一张夕阳海边风景图"

**在其他开发工具中的使用：**
- 直接向AI助手描述你想要生成的图像
- AI助手会自动调用豆包图像生成工具
- 生成的图像会保存到你配置的目录中

### 4.2 独立启动服务器

```bash
python doubao_mcp_server.py
```

### 4.3 MCP工具调用

服务器提供以下MCP工具：

#### 4.3.1 `doubao_generate_image`

图像生成的主要工具。

**参数：**
- `prompt`（必需）：图像描述文本，支持中英文
- `size`（可选）：图像分辨率，默认"1024x1024"
- `seed`（可选）：随机种子，如不指定则自动生成随机数，默认-1
- `guidance_scale`（可选）：引导强度1.0-10.0，默认8.0
- `watermark`（可选）：是否添加水印，默认true
- `file_prefix`（可选）：文件名前缀，仅限英文

**支持的分辨率：**
- `512x512` - 512x512（1:1小正方形）
- `768x768` - 768x768（1:1正方形）
- `1024x1024` - 1024x1024（1:1大正方形）
- `864x1152` - 864x1152（3:4竖屏）
- `1152x864` - 1152x864（4:3横屏）
- `1280x720` - 1280x720（16:9宽屏）
- `720x1280` - 720x1280（9:16手机竖屏）
- `832x1248` - 832x1248（2:3）
- `1248x832` - 1248x832（3:2）
- `1512x648` - 1512x648（21:9超宽屏）
- `2048x2048` - 2048x2048（1:1超大正方形）

**调用示例：**

基础调用（使用默认参数）：
```json
{
  "tool": "doubao_generate_image",
  "arguments": {
    "prompt": "一只可爱的橘猫坐在阳光明媚的窗台上，水彩画风格"
  }
}
```

完整参数调用：
```json
{
  "tool": "doubao_generate_image",
  "arguments": {
    "prompt": "一只可爱的橘猫坐在阳光明媚的窗台上，水彩画风格",
    "size": "1024x1024",
    "seed": -1,
    "guidance_scale": 8.0,
    "watermark": false,
    "file_prefix": "cute_cat"
  }
}
```

使用特定种子复现图像：
```json
{
  "tool": "doubao_generate_image",
  "arguments": {
    "prompt": "一只可爱的橘猫坐在阳光明媚的窗台上，水彩画风格",
    "seed": 1234567890,
    "size": "1024x1024"
  }
}
```

### 4.4 MCP资源

#### 4.4.1 `resolutions`

获取所有可用图像分辨率的列表。

### 4.5 MCP提示模板

#### 4.5.1 `image_generation_prompt`

提供图像生成的提示模板，包含所有参数说明和使用示例。

## 5. 项目结构

```
doubao-image-mcp-server/
├── doubao_mcp_server.py    # 主MCP服务器
├── doubao_image_gen.py     # 核心图像生成工具
├── pyproject.toml          # 项目配置和依赖管理
├── uv.lock                 # 依赖锁定文件
├── .gitignore             # Git忽略文件
├── LICENSE                # 开源许可证
├── README.md              # 英文项目文档
├── README_CN.md           # 中文项目文档
└── images/                # 文档图片目录
    ├── create_api_key.jpg
    ├── create_inference_endpoint.jpg
    ├── model_activation.jpg
    └── volcengine_signup.jpg
```

## 日志系统

项目包含完整的日志系统：

- **文件日志**: 保存在`log/`目录
- **控制台日志**: 输出到stderr用于调试
- **日志级别**: DEBUG、INFO、WARNING、ERROR

## 错误处理

- ✅ 环境变量验证
- ✅ 参数类型和范围检查
- ✅ API调用错误处理
- ✅ 图像下载重试机制
- ✅ 文件保存异常处理

## 技术特性

- **异步处理**: 基于asyncio的异步图像生成
- **重试机制**: 图像下载失败自动重试
- **参数验证**: 完整的输入参数验证
- **模块化设计**: 核心功能与MCP服务分离
- **类型注解**: 完整的类型提示支持

## 常见问题

### Q: 如何获取API密钥？
A: 访问火山引擎控制台，在API管理中创建新的API密钥。

### Q: 在哪里找到模型ID？
A: 在火山引擎控制台创建推理端点后，可在端点详情中找到ID。

### Q: 支持哪些图像格式？
A: 目前生成的图像以JPG格式保存。

### Q: 如何自定义图像保存路径？
A: 修改环境配置中的`IMAGE_SAVE_DIR`变量。

### Q: 生成失败怎么办？
A: 检查日志文件，确认API密钥、模型ID和网络连接是否正常。

## 许可证

本项目采用MIT许可证开源。

## 贡献

欢迎提交Issues和Pull Requests来改进项目。
