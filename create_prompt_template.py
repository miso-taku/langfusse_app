"""Langfuseプロンプトテンプレート作成ツール。

このモジュールは、Langfuseにチャットプロンプトテンプレートを作成・登録するための
ユーティリティを提供します。プロンプトテンプレートには変数、モデル設定、
温度パラメータなどを含めることができます。
"""

from typing import Any, Dict, List

from langfuse import Langfuse, get_client
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


def create_chat_prompt_messages(
    user_message_template: str,
    user_role: str = "user"
) -> List[Dict[str, str]]:
    """チャットプロンプトのメッセージリストを作成します。

    Args:
        user_message_template (str): ユーザーメッセージのテンプレート文字列。
            変数は{{variable_name}}の形式で指定します。
        user_role (str): メッセージの役割。デフォルトは"user"。

    Returns:
        List[Dict[str, str]]: チャットメッセージの辞書のリスト。
    """
    chat_messages = [
        {
            "role": user_role,
            "content": user_message_template
        }
    ]
    return chat_messages


def create_model_configuration(
    model_id: str,
    temperature: float
) -> Dict[str, Any]:
    """モデル設定の辞書を作成します。

    Args:
        model_id (str): 使用するモデルの識別子。
        temperature (float): モデルの温度パラメータ（0.0-1.0）。

    Returns:
        Dict[str, Any]: モデルIDと温度設定を含む辞書。
    """
    model_config = {
        "model": model_id,
        "temperature": temperature,
    }
    return model_config


def register_prompt_template_to_langfuse(
    langfuse_client: Langfuse,
    prompt_name: str,
    prompt_type: str,
    prompt_messages: List[Dict[str, str]],
    model_config: Dict[str, Any]
) -> Any:
    """Langfuseにプロンプトテンプレートを登録します。

    Args:
        langfuse_client (Langfuse): Langfuseクライアントインスタンス。
        prompt_name (str): プロンプトテンプレートの名前。
        prompt_type (str): プロンプトのタイプ（"chat"、"text"など）。
        prompt_messages (List[Dict[str, str]]): チャットメッセージのリスト。
        model_config (Dict[str, Any]): モデル設定の辞書。

    Returns:
        Any: 作成されたLangfuseプロンプトオブジェクト。
    """
    prompt_template = langfuse_client.create_prompt(
        name=prompt_name,
        type=prompt_type,
        prompt=prompt_messages,
        config=model_config
    )
    return prompt_template


def main() -> None:
    """メイン実行関数。

    Langfuseクライアントを初期化し、AIエージェント用の
    プロンプトテンプレートを作成・登録します。
    """
    # Langfuseクライアントの初期化
    langfuse_client = initialize_langfuse_client()

    # チャットメッセージの作成
    user_message_template = "{{city}}の人口は？"
    chat_messages = create_chat_prompt_messages(
        user_message_template=user_message_template,
        user_role="user"
    )

    # モデル設定の作成
    model_config = create_model_configuration(
        model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        temperature=1.0
    )

    # Langfuseにプロンプトテンプレートを登録
    prompt_template = register_prompt_template_to_langfuse(
        langfuse_client=langfuse_client,
        prompt_name="ai-agent",
        prompt_type="chat",
        prompt_messages=chat_messages,
        model_config=model_config
    )

    print(f"プロンプトテンプレート '{prompt_template.name}' を正常に作成しました。")


if __name__ == "__main__":
    main()
