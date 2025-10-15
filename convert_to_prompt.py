"""LangfuseプロンプトテンプレートをLangChainプロンプトに変換するツール。

このモジュールは、Langfuseに保存されたプロンプトテンプレートを取得し、
LangChainのChatPromptTemplateに変換して、変数を適用したメッセージを生成します。
"""

from typing import Any, Dict

from langfuse import Langfuse, get_client
from langchain_core.prompts import ChatPromptTemplate
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


def convert_langfuse_to_langchain_template(prompt_template: Any) -> ChatPromptTemplate:
    """LangfuseプロンプトテンプレートをLangChainテンプレートに変換します。

    Args:
        prompt_template: Langfuseプロンプトテンプレートオブジェクト。

    Returns:
        ChatPromptTemplate: LangChainのChatPromptTemplateインスタンス。
    """
    langchain_prompt_template = ChatPromptTemplate(
        prompt_template.get_langchain_prompt()
    )
    return langchain_prompt_template


def generate_prompt_messages_with_variables(
    langchain_template: ChatPromptTemplate,
    variables: Dict[str, str]
) -> Any:
    """プロンプトテンプレートに変数を適用してメッセージを生成します。

    Args:
        langchain_template (ChatPromptTemplate): LangChainのプロンプトテンプレート。
        variables (Dict[str, str]): テンプレートに適用する変数の辞書。

    Returns:
        Any: 変数が適用されたプロンプトメッセージオブジェクト。
    """
    prompt_messages = langchain_template.invoke(variables)
    return prompt_messages


def display_prompt_messages(prompt_messages: Any) -> None:
    """プロンプトメッセージを標準出力に表示します。

    Args:
        prompt_messages: 表示するプロンプトメッセージオブジェクト。
    """
    print(prompt_messages)


def main() -> None:
    """メイン実行関数。

    Langfuseからプロンプトテンプレートを取得し、LangChainテンプレートに変換して、
    変数を適用したメッセージを生成・表示します。
    """
    # Langfuseクライアントの初期化
    langfuse_client = initialize_langfuse_client()

    # Langfuseからプロンプトテンプレートを取得
    prompt_template = fetch_prompt_template_from_langfuse(
        langfuse_client=langfuse_client,
        prompt_name="ai-agent",
        prompt_type="chat",
        label="latest"
    )

    # LangChainテンプレートに変換
    langchain_template = convert_langfuse_to_langchain_template(prompt_template)

    # 変数を適用してメッセージを生成
    template_variables = {"city": "東京都"}
    prompt_messages = generate_prompt_messages_with_variables(
        langchain_template=langchain_template,
        variables=template_variables
    )

    # メッセージを表示
    display_prompt_messages(prompt_messages)


if __name__ == "__main__":
    main()
