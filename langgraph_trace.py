"""LangGraphのReActエージェントとLangfuseトレーシングの統合システム。

このモジュールは、LangGraphのReActエージェントにWeb検索機能を統合し、
Langfuseでトレーシングを行います。AWS Bedrock上のClaudeモデルを使用して、
ユーザーのクエリに対して推論と行動を繰り返しながら回答を生成します。
"""

from typing import Any, Dict, List

from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langfuse.langchain import CallbackHandler
from dotenv import load_dotenv


# 環境変数の読み込み
load_dotenv()


def initialize_web_search_tool(max_results: int = 2, topic: str = "general") -> TavilySearch:
    """Tavily Web検索ツールを初期化します。

    Args:
        max_results (int): 取得する検索結果の最大数。デフォルトは2。
        topic (str): 検索トピックのカテゴリ。デフォルトは"general"。

    Returns:
        TavilySearch: 初期化されたTavily検索ツールインスタンス。
    """
    web_search_tool = TavilySearch(max_results=max_results, topic=topic)
    return web_search_tool


def initialize_chat_model() -> Any:
    """AWS Bedrock上でClaude 3.7 Sonnetチャットモデルを初期化します。

    Returns:
        ChatModel: 設定済みのLangChainチャットモデルインスタンス。
    """
    chat_model = init_chat_model(
        model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        model_provider="bedrock_converse",
    )
    return chat_model


def create_react_agent_with_tools(chat_model: Any, tools: List[Any]) -> Any:
    """チャットモデルとツールを使用してReActエージェントを構築します。

    Args:
        chat_model: 初期化済みのLangChainチャットモデル。
        tools (List[Any]): エージェントが使用できるツールのリスト。

    Returns:
        CompiledGraph: LangGraphのReActエージェントインスタンス。
    """
    react_agent = create_react_agent(chat_model, tools)
    return react_agent


def setup_langfuse_callback() -> CallbackHandler:
    """Langfuseトレーシング用のコールバックハンドラーを作成します。

    Returns:
        CallbackHandler: Langfuseコールバックハンドラーインスタンス。
    """
    langfuse_callback_handler = CallbackHandler()
    return langfuse_callback_handler


def execute_agent_with_query(
    agent: Any,
    user_query: str,
    langfuse_callback: CallbackHandler
) -> Dict[str, List[Any]]:
    """ReActエージェントにクエリを実行し、結果を取得します。

    Args:
        agent: 初期化済みのReActエージェント。
        user_query (str): ユーザーからの問い合わせ内容。
        langfuse_callback (CallbackHandler): Langfuseコールバックハンドラー。

    Returns:
        Dict[str, List[Any]]: エージェントの実行結果。メッセージのリストを含む辞書。
    """
    agent_response = agent.invoke(
        {"messages": [("human", user_query)]},
        config={"callbacks": [langfuse_callback]}
    )
    return agent_response


def display_agent_messages(agent_response: Dict[str, List[Any]]) -> None:
    """エージェントの応答メッセージを整形して表示します。

    Args:
        agent_response (Dict[str, List[Any]]): エージェントの実行結果。
    """
    for message in agent_response["messages"]:
        message.pretty_print()


def main() -> None:
    """メイン実行関数。

    Web検索機能を持つReActエージェントを構築し、
    Langfuseトレーシングを有効にしてクエリを実行します。
    """
    # Web検索ツールの初期化
    web_search_tool = initialize_web_search_tool(max_results=2, topic="general")
    tools = [web_search_tool]

    # チャットモデルの初期化
    chat_model = initialize_chat_model()

    # ReActエージェントの構築
    react_agent = create_react_agent_with_tools(chat_model, tools)

    # Langfuseコールバックの設定
    langfuse_callback = setup_langfuse_callback()

    # エージェントの実行
    user_query = "AIエージェントの最新動向を教えてください。検索は1度だけ実施してください。"
    agent_response = execute_agent_with_query(react_agent, user_query, langfuse_callback)

    # 結果の表示
    display_agent_messages(agent_response)


if __name__ == "__main__":
    main()
