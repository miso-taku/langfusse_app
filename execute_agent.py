"""Langfuseのプロンプト管理機能を使用したReActエージェント実行システム。

このモジュールは、Langfuseに保存されたプロンプトテンプレートと設定を取得し、
それを使用してLangGraphのReActエージェントを動的に構築・実行します。
AWS Bedrock上のモデルとTavily Web検索を統合し、全ての実行をLangfuseでトレーシングします。
"""

from typing import Any, Dict, List

from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_tavily import TavilySearch
from langfuse import Langfuse, get_client
from langfuse.langchain import CallbackHandler
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv


# 環境変数の読み込み
load_dotenv()


def initialize_langfuse_client() -> Langfuse:
    """Langfuseクライアントを初期化します。

    Returns:
        Langfuse: 初期化されたLangfuseクライアントインスタンス。
    """
    langfuse_client = get_client()
    return langfuse_client


def fetch_prompt_template_from_langfuse(
    langfuse_client: Langfuse,
    prompt_name: str,
    prompt_type: str = "chat",
    label: str = "latest"
) -> Any:
    """Langfuseからプロンプトテンプレートを取得します。

    Args:
        langfuse_client (Langfuse): Langfuseクライアントインスタンス。
        prompt_name (str): 取得するプロンプトの名前。
        prompt_type (str): プロンプトのタイプ。デフォルトは"chat"。
        label (str): プロンプトのラベル/バージョン。デフォルトは"latest"。

    Returns:
        Any: Langfuseプロンプトテンプレートオブジェクト。
    """
    prompt_template = langfuse_client.get_prompt(
        prompt_name,
        type=prompt_type,
        label=label
    )
    return prompt_template


def extract_model_configuration(prompt_template: Any) -> Dict[str, Any]:
    """プロンプトテンプレートからモデル設定を抽出します。

    Args:
        prompt_template: Langfuseプロンプトテンプレートオブジェクト。

    Returns:
        Dict[str, Any]: モデル名と温度設定を含む辞書。
            - model (str): モデルの識別子
            - temperature (float): モデルの温度パラメータ
    """
    model_name = prompt_template.config["model"]
    temperature = prompt_template.config["temperature"]

    return {
        "model": model_name,
        "temperature": temperature
    }


def create_react_agent_with_config(model_name: str, temperature: float) -> Any:
    """指定された設定でReActエージェントを構築します。

    Args:
        model_name (str): 使用するAWSモデルの識別子。
        temperature (float): モデルの温度パラメータ（0.0-1.0）。

    Returns:
        CompiledGraph: 構築されたLangGraph ReActエージェントインスタンス。
    """
    # チャットモデルの初期化
    chat_model = init_chat_model(
        model=model_name,
        model_provider="bedrock_converse",
        temperature=temperature
    )

    # Web検索ツールの設定
    web_search_tools = [TavilySearch(max_results=2, topic="general")]

    # ReActエージェントの構築
    react_agent = create_react_agent(chat_model, web_search_tools)

    return react_agent


def convert_to_langchain_prompt(prompt_template: Any, variables: Dict[str, str]) -> Any:
    """LangfuseプロンプトテンプレートをLangChainプロンプトに変換して変数を適用します。

    Args:
        prompt_template: Langfuseプロンプトテンプレートオブジェクト。
        variables (Dict[str, str]): プロンプトに適用する変数の辞書。

    Returns:
        Any: 変数が適用されたLangChainメッセージオブジェクト。
    """
    langchain_prompt_template = ChatPromptTemplate(
        prompt_template.get_langchain_prompt()
    )
    prompt_messages = langchain_prompt_template.invoke(variables)

    return prompt_messages


def setup_langfuse_callback_handler() -> CallbackHandler:
    """Langfuseトレーシング用のコールバックハンドラーを作成します。

    Returns:
        CallbackHandler: Langfuseコールバックハンドラーインスタンス。
    """
    langfuse_callback = CallbackHandler()
    return langfuse_callback


def execute_agent_with_messages(
    agent: Any,
    prompt_messages: Any,
    langfuse_callback: CallbackHandler
) -> Dict[str, List[Any]]:
    """ReActエージェントにプロンプトメッセージを実行します。

    Args:
        agent: 初期化済みのReActエージェント。
        prompt_messages: 実行するプロンプトメッセージ。
        langfuse_callback (CallbackHandler): Langfuseコールバックハンドラー。

    Returns:
        Dict[str, List[Any]]: エージェントの実行結果。メッセージのリストを含む辞書。
    """
    agent_response = agent.invoke(
        prompt_messages,
        config={"callbacks": [langfuse_callback]}
    )
    return agent_response


def display_final_response(agent_response: Dict[str, List[Any]]) -> None:
    """エージェントの最終応答メッセージを整形して表示します。

    Args:
        agent_response (Dict[str, List[Any]]): エージェントの実行結果。
    """
    final_message = agent_response["messages"][-1]
    final_message.pretty_print()


def main() -> None:
    """メイン実行関数。

    Langfuseからプロンプトテンプレートと設定を取得し、
    ReActエージェントを動的に構築して実行します。
    """
    # Langfuseクライアントの初期化
    langfuse_client = initialize_langfuse_client()

    # プロンプトテンプレートの取得
    prompt_template = fetch_prompt_template_from_langfuse(
        langfuse_client,
        prompt_name="ai-agent",
        prompt_type="chat",
        label="latest"
    )

    # モデル設定の抽出
    model_config = extract_model_configuration(prompt_template)

    # ReActエージェントの構築
    react_agent = create_react_agent_with_config(
        model_name=model_config["model"],
        temperature=model_config["temperature"]
    )

    # プロンプトメッセージの準備
    prompt_variables = {"city": "横浜"}
    prompt_messages = convert_to_langchain_prompt(prompt_template, prompt_variables)

    # Langfuseコールバックの設定
    langfuse_callback = setup_langfuse_callback_handler()

    # エージェントの実行
    agent_response = execute_agent_with_messages(
        react_agent,
        prompt_messages,
        langfuse_callback
    )

    # 最終応答の表示
    display_final_response(agent_response)


if __name__ == "__main__":
    main()
