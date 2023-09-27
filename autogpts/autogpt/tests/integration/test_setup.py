from unittest.mock import patch

import pytest

from autogpt.app.setup import generate_aiconfig_automatic, interactive_ai_config_setup
from autogpt.config.ai_config import AIConfig


@pytest.mark.vcr
@pytest.mark.requires_openai_api_key
async def test_generate_aiconfig_automatic_default(
    patched_api_requestor, config, llm_provider
):
    user_inputs = [""]
    with patch("autogpt.app.utils.session.prompt", side_effect=user_inputs):
        ai_config = await interactive_ai_config_setup(config, llm_provider)

    assert isinstance(ai_config, AIConfig)
    assert ai_config.ai_name is not None
    assert ai_config.ai_role is not None
    assert 1 <= len(ai_config.ai_goals) <= 5


@pytest.mark.vcr
@pytest.mark.requires_openai_api_key
async def test_generate_aiconfig_automatic_typical(
    patched_api_requestor, config, llm_provider
):
    user_prompt = "Help me create a rock opera about cybernetic giraffes"
    ai_config = await generate_aiconfig_automatic(user_prompt, config, llm_provider)

    assert isinstance(ai_config, AIConfig)
    assert ai_config.ai_name is not None
    assert ai_config.ai_role is not None
    assert 1 <= len(ai_config.ai_goals) <= 5


@pytest.mark.vcr
@pytest.mark.requires_openai_api_key
async def test_generate_aiconfig_automatic_fallback(
    patched_api_requestor, config, llm_provider
):
    user_inputs = [
        "T&GF£OIBECC()!*",
        "Chef-GPT",
        "an AI designed to browse bake a cake.",
        "Purchase ingredients",
        "Bake a cake",
        "",
        "",
    ]
    with patch("autogpt.app.utils.session.prompt", side_effect=user_inputs):
        ai_config = await interactive_ai_config_setup(config, llm_provider)

    assert isinstance(ai_config, AIConfig)
    assert ai_config.ai_name == "Chef-GPT"
    assert ai_config.ai_role == "an AI designed to browse bake a cake."
    assert ai_config.ai_goals == ["Purchase ingredients", "Bake a cake"]


@pytest.mark.vcr
@pytest.mark.requires_openai_api_key
async def test_prompt_user_manual_mode(patched_api_requestor, config, llm_provider):
    user_inputs = [
        "--manual",
        "Chef-GPT",
        "an AI designed to browse bake a cake.",
        "Purchase ingredients",
        "Bake a cake",
        "",
        "",
    ]
    with patch("autogpt.app.utils.session.prompt", side_effect=user_inputs):
        ai_config = await interactive_ai_config_setup(config, llm_provider)

    assert isinstance(ai_config, AIConfig)
    assert ai_config.ai_name == "Chef-GPT"
    assert ai_config.ai_role == "an AI designed to browse bake a cake."
    assert ai_config.ai_goals == ["Purchase ingredients", "Bake a cake"]