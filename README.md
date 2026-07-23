# My Codex Marketplace

一个可通过 Git 分发的 Codex Plugin Marketplace。市场目录位于
[`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json)，插件包位于
[`plugins/`](plugins/)；每个插件都有必需的 `.codex-plugin/plugin.json` 清单。

## 本地验证

```sh
python3 scripts/validate_marketplace.py
```

使用本地目录临时添加市场（会写入你的 Codex 运行时配置）：

```sh
codex plugin marketplace add ./
codex plugin marketplace list
```

随后在 Codex CLI 输入 `/plugins`，从 **My Codex Marketplace** 安装插件并开启一个新会话。
本地测试完成后可移除它：

```sh
codex plugin marketplace remove my-codex-marketplace
```

## 发布为 Git Marketplace

1. 将本目录初始化并推送到 GitHub、GitLab 或可访问的 Git 远程仓库。
2. 用户通过以下任一方式添加市场：

   ```sh
   codex plugin marketplace add OWNER/REPOSITORY
   # 或固定到一个分支 / tag
   codex plugin marketplace add OWNER/REPOSITORY --ref main
   ```

   对任意 Git 地址也可使用：

   ```sh
   codex plugin marketplace add https://github.com/OWNER/REPOSITORY.git --ref main
   ```

3. 用户执行 `codex plugin marketplace upgrade my-codex-marketplace` 获取后续市场更新。

> 对生产使用，建议将 `--ref` 固定为经过审查的 tag 或 commit SHA，而不是持续跟踪分支。

## 新增本仓库插件

1. 创建 `plugins/<plugin-name>/.codex-plugin/plugin.json`。`name` 使用稳定的小写 kebab-case。
2. 如包含 Skill，在 `plugins/<plugin-name>/skills/<skill-name>/SKILL.md` 中创建它；清单的 `skills` 使用 `"./skills/"`。
3. 在 `.agents/plugins/marketplace.json` 的 `plugins` 数组添加条目，使用：

   ```json
   {
     "name": "<plugin-name>",
     "source": { "source": "local", "path": "./plugins/<plugin-name>" },
     "policy": { "installation": "AVAILABLE", "authentication": "ON_INSTALL" },
     "category": "Productivity"
   }
   ```

4. 运行验证脚本，再用 `/plugins` 手动安装测试。不要将凭据、令牌或其他秘密放进插件、清单或市场目录。

## 引用外部 Git 插件

市场也能收录独立维护的 Git 插件。插件在一个仓库子目录时，条目使用 `git-subdir`：

```json
{
  "name": "remote-helper",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/example/codex-plugins.git",
    "path": "./plugins/remote-helper",
    "ref": "v1.2.3"
  },
  "policy": { "installation": "AVAILABLE", "authentication": "ON_INSTALL" },
  "category": "Productivity"
}
```

对外部依赖请优先固定可信 tag 或 commit SHA，并在发布前审查其 manifest、Skill、MCP 配置和 hooks。

## 当前内容

- **project-onboarding**：在改动陌生代码库前，按规则、架构、测试与验证顺序进行阅读和规划。它仅提供 Skill，不包含 MCP、hooks、连接器或密钥。

## 维护原则

- 每次修改市场或插件后运行 `python3 scripts/validate_marketplace.py`。
- 对有破坏性行为的更新提升插件版本并在发布说明中记录迁移步骤。
- 安装前审查来自第三方的 hooks、MCP server、连接器和脚本；这些组件可能具有读取、写入或网络访问能力。
- 一次只更新经过验证的市场条目；当 Git 源无法解析时，Codex 会跳过该条目而不会使整个市场失效。

## 官方文档

- [Build plugins](https://learn.chatgpt.com/docs/build-plugins)
- [Plugins](https://learn.chatgpt.com/docs/plugins)
