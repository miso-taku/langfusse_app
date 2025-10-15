"""Langfuse統合を使用したLangChainチャットモデルのデモンストレーション。

このモジュールは、AWS Bedrock上のClaude 3.7 Sonnetモデルを使用し、
Langfuseでトレーシングを行うシンプルなチャット推論の例を提供します。
"""

from typing import Any, Dict

from langchain.chat_models import init_chat_model
from langfuse.langchain import CallbackHandler
from dotenv import load_dotenv


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


def setup_langfuse_callback() -> Dict[str, list]:
    """Langfuseトレーシング用のコールバック設定を作成します。

    Returns:
        dict: Langfuseコールバックハンドラーを含む設定辞書。
    """
    langfuse_callback_handler = CallbackHandler()
    callback_config = {"callbacks": [langfuse_callback_handler]}
    return callback_config


def execute_chat_inference(
    chat_model: Any,
    user_message: str,
    callback_config: Dict[str, list]
) -> Any:
    """チャットモデルを使用して推論を実行します。

    Args:
        chat_model: 初期化済みのLangChainチャットモデル。
        user_message (str): モデルに送信するユーザーメッセージ。
        callback_config (dict): コールバックハンドラーを含む設定辞書。

    Returns:
        str: モデルからの応答メッセージ。
    """
    model_response = chat_model.invoke(user_message, config=callback_config)
    return model_response


def main() -> None:
    """メイン実行関数。

    環境変数を読み込み、チャットモデルを初期化し、
    Langfuseトレーシングを有効にして推論を実行します。
    """
    # 環境変数の読み込み
    load_dotenv()

    # チャットモデルの初期化
    chat_model: Any = initialize_chat_model()

    # Langfuseコールバックの設定
    callback_config: Dict[str, list] = setup_langfuse_callback()

    # チャット推論の実行
    user_message: str = "こんにちは"
    model_response: Any = execute_chat_inference(chat_model, user_message, callback_config)
    print(model_response)


if __name__ == "__main__":
    main()
