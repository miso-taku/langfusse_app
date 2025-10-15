"""Langfuseトレーシングを使用したWeb検索ベースのレポート生成システム。

このモジュールは、AWS Bedrock上のClaudeモデルとTavily Web検索APIを組み合わせて、
ユーザーのクエリに基づいたMarkdownレポートを生成します。
全ての主要な関数はLangfuseの@observeデコレーターでトレーシングされます。
"""

import os
from typing import List

import boto3
from dotenv import load_dotenv
from langfuse import observe
from tavily import TavilyClient


# 環境変数の読み込み
load_dotenv()


class BedrockClientConfig:
    """AWS Bedrockクライアントの設定を管理するクラス。"""

    def __init__(self, model_id: str = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"):
        """BedrockClientConfigを初期化します。

        Args:
            model_id (str): 使用するBedrockモデルのID。
        """
        self.client = boto3.client("bedrock-runtime")
        self.model_id = model_id


class TavilySearchClient:
    """Tavily Web検索クライアントを管理するクラス。"""

    def __init__(self, api_key: str | None = None):
        """TavilySearchClientを初期化します。

        Args:
            api_key (str | None): Tavily APIキー。Noneの場合は環境変数から取得。
        """
        self.client = TavilyClient(api_key=api_key or os.environ.get("TAVILY_API_KEY"))


# グローバルクライアントのインスタンス化
bedrock_config = BedrockClientConfig()
tavily_search_client = TavilySearchClient()


@observe
def generate_web_search_query(user_query: str) -> str:
    """ユーザーのクエリからWeb検索用のクエリを生成します。

    AWS Bedrock上のClaudeモデルを使用して、ユーザーの問い合わせ内容を
    Web検索に適した形式のクエリに変換します。

    Args:
        user_query (str): ユーザーからの元の問い合わせ内容。

    Returns:
        str: 生成されたWeb検索用のクエリ文字列。
    """
    system_prompt = """ユーザからの問い合わせ内容をWeb検索し、レポートを作成します。
    Web検索用のクエリを1つ作成してください。検索単語以外は回答しないでください。"""

    prompt = f"ユーザの質問: {user_query}"

    system = [{"text": system_prompt}]
    messages = [
        {
            "role": "user",
            "content": [{"text": prompt}],
        }
    ]

    response = bedrock_config.client.converse(
        modelId=bedrock_config.model_id,
        system=system,
        messages=messages,
    )

    return response["output"]["message"]["content"][0]["text"]


@observe
def search_web_content(search_query: str, max_results: int = 3) -> List[str]:
    """Tavily APIを使用してWeb検索を実行し、コンテンツを取得します。

    Args:
        search_query (str): 検索クエリ文字列。
        max_results (int): 取得する検索結果の最大数。デフォルトは3。

    Returns:
        List[str]: 検索結果のコンテンツのリスト。
    """
    search_result = tavily_search_client.client.search(
        query=search_query, max_results=max_results
    )
    return [doc["content"] for doc in search_result["results"]]


@observe
def generate_markdown_report(user_query: str, search_contents: List[str]) -> str:
    """Web検索結果を基にMarkdown形式のレポートを生成します。

    AWS Bedrock上のClaudeモデルを使用して、検索結果をMarkdownレポートに要約します。

    Args:
        user_query (str): 元のユーザークエリ。
        search_contents (List[str]): Web検索で取得したコンテンツのリスト。

    Returns:
        str: Markdown形式で整形されたレポート。
    """
    system_prompt = """Web検索した結果とユーザクエリを元にMarkdownのレポートを作成してください。
    タイトルと見出しも作成してください"""

    prompt = f"ユーザの質問: {user_query}\n\n web検索結果: {'\n'.join(search_contents)}"

    system = [{"text": system_prompt}]
    messages = [
        {
            "role": "user",
            "content": [{"text": prompt}],
        }
    ]

    response = bedrock_config.client.converse(
        modelId=bedrock_config.model_id,
        system=system,
        messages=messages,
    )

    return response["output"]["message"]["content"][0]["text"]


@observe
def execute_research_workflow(user_query: str) -> str:
    """ユーザークエリからレポート生成までの全ワークフローを実行します。

    このワークフローは以下のステップで構成されます:
    1. ユーザークエリから検索クエリを生成
    2. Web検索を実行してコンテンツを取得
    3. 検索結果からMarkdownレポートを生成

    Args:
        user_query (str): ユーザーからの問い合わせ内容。

    Returns:
        str: 生成されたMarkdown形式のレポート。
    """
    web_search_query = generate_web_search_query(user_query)
    search_contents = search_web_content(web_search_query)
    markdown_report = generate_markdown_report(web_search_query, search_contents)

    return markdown_report


def main() -> None:
    """メイン実行関数。

    サンプルクエリを使用してレポート生成ワークフローを実行し、
    結果を標準出力に表示します。
    """
    user_query = "LangChainとLangGraphのユースケースの違いについて教えてください。"

    generated_report = execute_research_workflow(user_query)
    print(generated_report)


if __name__ == "__main__":
    main()
