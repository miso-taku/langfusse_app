# langfuse_app

Langfuseトレーシング統合を使用したLangChainおよびLangGraphアプリケーションのサンプル集です。このプロジェクトは、AWS Bedrock上のClaude 3.7 Sonnetモデルを使用し、Web検索、プロンプト管理、ReActエージェントなど、さまざまなAIエージェントパターンを実装しています。

## 📋 目次

- [概要](#概要)
- [プロジェクト構成](#プロジェクト構成)
- [前提条件](#前提条件)
- [セットアップ](#セットアップ)
- [ソースファイルの詳細](#ソースファイルの詳細)
- [使用方法](#使用方法)
- [技術スタック](#技術スタック)

## 🎯 概要

このプロジェクトは、LangfuseのObservability機能を活用して、LLMアプリケーションのトレーシング、モニタリング、デバッグを行うためのサンプル実装集です。以下の主要機能を提供します:

- **LLM推論のトレーシング**: Langfuseで全てのLLM呼び出しを記録・可視化
- **Web検索統合**: Tavily APIを使用したリアルタイムWeb検索
- **ReActエージェント**: LangGraphを使用した推論-行動サイクルの実装
- **プロンプト管理**: Langfuseでプロンプトテンプレートを一元管理
- **デコレーターベースのトレーシング**: `@observe`デコレーターによる簡単な統合

## 📁 プロジェクト構成

```
langfuse_app/
├── README.md                      # このファイル
├── .env                           # 環境変数設定（作成が必要）
├── langfuse_trial.py              # LangChainの基本的なトレーシング
├── langfuse_decorator.py          # @observeデコレーターを使用したトレーシング
├── langgraph_trace.py             # LangGraphのReActエージェント実装
├── execute_agent.py               # Langfuseプロンプト管理の活用
├── create_prompt_template.py      # プロンプトテンプレートの作成
└── convert_to_prompt.py           # プロンプトテンプレートの変換・使用
```

## 🔧 前提条件

- Python 3.9以上
- AWS アカウント（AWS Bedrockへのアクセス）
- Langfuse アカウント
- Tavily API キー（Web検索機能使用時）

## 🚀 セットアップ

### 1. 依存パッケージのインストール

```bash
pip install langchain langchain-core langchain-tavily
pip install langgraph
pip install langfuse
pip install tavily-python
pip install boto3
pip install python-dotenv
```

### 2. 環境変数の設定

プロジェクトルートに `.env` ファイルを作成し、以下の環境変数を設定してください:

```env
# Langfuse設定
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
LANGFUSE_HOST=https://cloud.langfuse.com  # または自己ホスト版のURL

# Tavily API設定
TAVILY_API_KEY=your_tavily_api_key

# AWS設定（boto3が自動的に認証情報を読み取ります）
# AWS_ACCESS_KEY_ID=your_aws_access_key
# AWS_SECRET_ACCESS_KEY=your_aws_secret_key
# AWS_DEFAULT_REGION=us-east-1
```

### 3. AWS Bedrock のセットアップ

AWS CLIを使用してAWSの認証情報を設定してください:

```bash
aws configure
```

Claude 3.7 Sonnetモデルへのアクセスが有効になっていることを確認してください。

## 📚 ソースファイルの詳細

### 1. langfuse_trial.py

**目的**: LangChainとLangfuseの基本的な統合パターン

**主な機能**:
- AWS Bedrock上のClaude 3.7 Sonnetモデルの初期化
- Langfuseコールバックハンドラーの設定
- シンプルなチャット推論の実行とトレーシング

**主要関数**:
- `initialize_chat_model()`: チャットモデルの初期化
- `setup_langfuse_callback()`: Langfuseコールバックの設定
- `execute_chat_inference()`: チャット推論の実行

**実行例**:
```bash
python langfuse_trial.py
```

**ユースケース**: Langfuseトレーシングの基本を理解したい場合

---

### 2. langfuse_decorator.py

**目的**: `@observe`デコレーターを使用した高度なトレーシング

**主な機能**:
- Web検索ベースのレポート生成システム
- 複数の関数にまたがるトレーシング
- AWS BedrockとTavily検索の統合

**主要関数**:
- `generate_web_search_query()`: ユーザークエリから検索クエリを生成
- `search_web_content()`: Tavily APIでWeb検索を実行
- `generate_markdown_report()`: 検索結果からMarkdownレポートを生成
- `execute_research_workflow()`: 全ワークフローのオーケストレーション

**主要クラス**:
- `BedrockClientConfig`: AWS Bedrockクライアントの管理
- `TavilySearchClient`: Tavily検索クライアントの管理

**実行例**:
```bash
python langfuse_decorator.py
```

**ユースケース**: 複雑なワークフローで各ステップをトレースしたい場合

---

### 3. langgraph_trace.py

**目的**: LangGraphのReActエージェントとLangfuseの統合

**主な機能**:
- ReAct（Reasoning and Acting）パターンの実装
- Web検索ツールの統合
- エージェントの思考プロセスのトレーシング

**主要関数**:
- `initialize_web_search_tool()`: Tavily検索ツールの初期化
- `initialize_chat_model()`: Claudeモデルの初期化
- `create_react_agent_with_tools()`: ReActエージェントの構築
- `execute_agent_with_query()`: エージェントへのクエリ実行
- `display_agent_messages()`: エージェントの応答表示

**実行例**:
```bash
python langgraph_trace.py
```

**ユースケース**: AIエージェントの推論と行動のサイクルを可視化したい場合

---

### 4. execute_agent.py

**目的**: Langfuseのプロンプト管理機能を活用したエージェント実行

**主な機能**:
- Langfuseからプロンプトテンプレートを動的に取得
- モデル設定の一元管理
- プロンプトのバージョン管理

**主要関数**:
- `initialize_langfuse_client()`: Langfuseクライアントの初期化
- `fetch_prompt_template_from_langfuse()`: プロンプトテンプレートの取得
- `extract_model_configuration()`: モデル設定の抽出
- `create_react_agent_with_config()`: 設定ベースのエージェント構築
- `convert_to_langchain_prompt()`: プロンプトの変換
- `execute_agent_with_messages()`: エージェントの実行

**実行例**:
```bash
python execute_agent.py
```

**ユースケース**: プロンプトをコードから分離して管理したい場合

**注意**: このスクリプトを実行する前に、`create_prompt_template.py`でプロンプトテンプレートを作成する必要があります。

---

### 5. create_prompt_template.py

**目的**: Langfuseにプロンプトテンプレートを登録

**主な機能**:
- チャットプロンプトテンプレートの作成
- モデル設定（温度、モデルIDなど）の定義
- Langfuseへのプロンプト登録

**主要関数**:
- `initialize_langfuse_client()`: Langfuseクライアントの初期化
- `create_chat_prompt_messages()`: チャットメッセージの作成
- `create_model_configuration()`: モデル設定の作成
- `register_prompt_template_to_langfuse()`: プロンプトの登録

**実行例**:
```bash
python create_prompt_template.py
```

**ユースケース**: 新しいプロンプトテンプレートをLangfuseに登録したい場合

**作成されるプロンプト**:
- 名前: `ai-agent`
- タイプ: `chat`
- 変数: `{{city}}`
- モデル: Claude 3.7 Sonnet
- 温度: 1.0

---

### 6. convert_to_prompt.py

**目的**: LangfuseプロンプトテンプレートをLangChainで使用

**主な機能**:
- Langfuseからプロンプトテンプレートを取得
- LangChainのChatPromptTemplateに変換
- 変数を適用してメッセージを生成

**主要関数**:
- `initialize_langfuse_client()`: Langfuseクライアントの初期化
- `fetch_prompt_template_from_langfuse()`: プロンプトテンプレートの取得
- `convert_langfuse_to_langchain_template()`: テンプレート変換
- `generate_prompt_messages_with_variables()`: 変数適用
- `display_prompt_messages()`: メッセージ表示

**実行例**:
```bash
python convert_to_prompt.py
```

**ユースケース**: Langfuseで管理しているプロンプトをLangChainで使用したい場合

**注意**: このスクリプトを実行する前に、`create_prompt_template.py`でプロンプトテンプレートを作成する必要があります。

---

## 💡 使用方法

### 基本的なワークフロー

1. **環境のセットアップ**
   ```bash
   # .envファイルを作成して環境変数を設定
   cp .env.example .env  # .env.exampleがある場合
   # .envファイルを編集して認証情報を追加
   ```

2. **シンプルなトレーシングを試す**
   ```bash
   python langfuse_trial.py
   ```

3. **プロンプトテンプレートを作成**
   ```bash
   python create_prompt_template.py
   ```

4. **プロンプトテンプレートを使用**
   ```bash
   python convert_to_prompt.py
   ```

5. **ReActエージェントを実行**
   ```bash
   python langgraph_trace.py
   ```

6. **デコレーターベースのトレーシングを試す**
   ```bash
   python langfuse_decorator.py
   ```

7. **Langfuseプロンプト管理でエージェントを実行**
   ```bash
   python execute_agent.py
   ```

### Langfuseダッシュボードでの確認

スクリプト実行後、Langfuseダッシュボード（https://cloud.langfuse.com）にアクセスして以下を確認できます:

- **トレース**: LLM呼び出しの詳細なフロー
- **スパン**: 各関数の実行時間とパラメータ
- **プロンプト**: 使用されたプロンプトテンプレート
- **出力**: モデルの応答内容
- **コスト**: トークン使用量とコスト推定

## 🛠️ 技術スタック

### コアフレームワーク
- **LangChain**: LLMアプリケーション開発フレームワーク
- **LangGraph**: ステートフルなマルチアクターアプリケーションのフレームワーク
- **Langfuse**: LLMアプリケーションのObservabilityプラットフォーム

### LLMプロバイダー
- **AWS Bedrock**: Claude 3.7 Sonnetモデルのホスティング

### ツール・統合
- **Tavily API**: リアルタイムWeb検索
- **python-dotenv**: 環境変数管理
- **boto3**: AWS SDK for Python

## 📝 アーキテクチャパターン

### 1. シンプルなLLM呼び出し (langfuse_trial.py)
```
ユーザー入力 → LangChain → AWS Bedrock → Langfuse (トレース)
```

### 2. Web検索統合 (langfuse_decorator.py)
```
ユーザークエリ
  ↓
検索クエリ生成 (@observe)
  ↓
Tavily Web検索 (@observe)
  ↓
レポート生成 (@observe)
  ↓
Langfuse (全ステップをトレース)
```

### 3. ReActエージェント (langgraph_trace.py)
```
ユーザークエリ
  ↓
LangGraph ReActエージェント
  ├─ 思考 (Reasoning)
  ├─ 行動 (Acting) - Web検索
  └─ 観察 (Observation)
  ↓
最終回答
  ↓
Langfuse (エージェントの全プロセスをトレース)
```

### 4. プロンプト管理パターン (execute_agent.py)
```
Langfuseプロンプトストア
  ↓
プロンプト取得 + モデル設定
  ↓
動的にエージェント構築
  ↓
実行 + トレース
```

## 🎓 学習リソース

- [LangChain公式ドキュメント](https://python.langchain.com/)
- [LangGraph公式ドキュメント](https://langchain-ai.github.io/langgraph/)
- [Langfuse公式ドキュメント](https://langfuse.com/docs)
- [AWS Bedrock ドキュメント](https://docs.aws.amazon.com/bedrock/)
- [Tavily API ドキュメント](https://docs.tavily.com/)

## 🤝 コントリビューション

このプロジェクトはサンプル集です。改善提案やバグ報告は歓迎します。

## 📄 ライセンス

このプロジェクトはサンプルコードとして提供されています。

## ⚠️ 注意事項

- AWS BedrockとTavily APIの使用には料金が発生する場合があります
- `.env`ファイルは`.gitignore`に追加し、リポジトリにコミットしないでください
- 本番環境で使用する場合は、適切なエラーハンドリングとセキュリティ対策を追加してください
- モデルのレスポンス時間と検索結果は、ネットワーク状況やAPIの負荷により変動します

## 🔍 トラブルシューティング

### よくある問題

1. **AWS認証エラー**
   - `aws configure`で認証情報が正しく設定されているか確認
   - IAMユーザーにBedrock使用権限があるか確認

2. **Langfuse接続エラー**
   - `.env`ファイルのLangfuse認証情報を確認
   - Langfuseダッシュボードでプロジェクトが作成されているか確認

3. **Tavily APIエラー**
   - Tavily APIキーが有効か確認
   - APIの使用制限に達していないか確認

4. **プロンプトが見つからないエラー**
   - `create_prompt_template.py`を先に実行してプロンプトを作成
   - Langfuseダッシュボードでプロンプトが正しく登録されているか確認

5. **モジュールのインポートエラー**
   - 全ての依存パッケージがインストールされているか確認
   - 仮想環境が有効化されているか確認

---

**作成日**: 2025年
**最終更新**: 2025年
