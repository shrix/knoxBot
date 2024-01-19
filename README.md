# 💬 KnoxBot
This bot is created using the open-source LLM models.

Currently, we use [**Llama2**](https://replicate.com/meta) models deployed on [Replicate](https://replicate.com/) platform.

## Demo App
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://knoxbot.streamlit.app/)

## Libraries
```
streamlit
replicate
```

## Replicate API token
To use this app, you'll need to get your own [Replicate](https://replicate.com/) API token.

After signing into Replicate, you can access your API tokens [here](https://replicate.com/account/api-tokens).

```
export REPLICATE_API_TOKEN="your_replicate_token"
```
(or set it in your .env file)

## Other Llama 2 models
You can also try out the larger models:
- [Llama2-7B](https://replicate.com/meta/llama-2-7b-chat)
- [Llama2-13B](https://replicate.com/meta/llama-2-13b-chat)
- [Llama2-70B](https://replicate.com/meta/llama-2-70b-chat)
