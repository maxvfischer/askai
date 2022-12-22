<div align="center">
    <img style="display: block;" align="center" src="https://github.com/maxvfischer/askai/blob/main/images/logo.png?raw=True"/>
</div>

`askai` is a CLI integration with OpenAI's GPT3, enabling you to ask questions and 
receive the answers straight in your terminal.

![conda](https://github.com/maxvfischer/askai/blob/main/images/question_conda.svg?raw=True)


| ❗ **Other model integrations** ❗                                                                                                                            |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Currently, `askai` only supports integration with OpenAI. But as soon as other NLP API-endpoints start popping up, I will work on integrating them as well. |


## Installation

You can either install it through pip

```bash
pip install askai
```

or directly from the repo

```
git clone git@github.com:maxvfischer/askai.git
cd askai
pip install .
```

## Initialize askai

`askai` needs to be initialized to set up the default config and to connect your 
OpenAI API key. Note that the key is only stored locally in `~/.askai/key`.

```bash
askai init
```

![init](https://github.com/maxvfischer/askai/blob/main/images/init.svg?raw=True)

## Create OpenAI API-key

For `askai` to work, you need to add an OpenAI API-key. When creating an OpenAI account, 
they give you $18 to use for free. After that you need to set up a paid account to 
continue using their service. 

During the development and testing of this CLI, I used $0.67.

An OpenAI API-key can be created by:

1. Creating an account on OpenAI: https://openai.com/api/
2. Logging in and click on `New API keys`
3. Click `Create new secret key`

## How to use


### Simple question
Ask a question using your saved config.

```
askai "<QUESTION>"
```
![conda](https://github.com/maxvfischer/askai/blob/main/images/question_conda.svg?raw=True)


### Override config
It's possible to override the default config by using arguments:

```
askai "<QUESTION>" --num-answers <INT> --model <MODEL_STRING> --temperature <FLOAT> --top_p <FLOAT> --max-tokens <INT> --frequency-penalty <FLOAT> --presence_penalty <FLOAT>
```
![conda](https://github.com/maxvfischer/askai/blob/main/images/haiku.svg?raw=True)

| **Argument**        | **Allowed values**               | **Description**                                                                                                                                                |
|---------------------|----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| --num-answers or -n | \>0                              | Number of answers to generate. Note that more answers consume more tokens                                                                                      |
| --model or -m       | See list below                   | Which model to use. See list of available models below.                                                                                                        |
| --temperature or -t | 0.0 <= t <= 1.0                  | What sampling temperature to use. Higher value makes the model more  "creative". Do not use at the same time as `top-p`.                                       |
| --top-p             | 0.0 <= top_p <= 1.0              | What sampling nucleus to use. The model considers the results of the  tokens with top_p probability mass. Do not use at the same time as `temperature`.        |
| --max-tokens        | \>0                              | Maximum number of tokens used per question (incl. question + answer)                                                                                           |
| --frequency-penalty | -2.0 <= frequency_penalty <= 2.0 | Positive values penalize new tokens based on whether they appear in the text so  far, increasing the model's likelihood to talk about new topics.              |
| --presence-penalty  | -2.0 <= presence_penalty <= 2.0  | Positive values penalize new tokens based on their existing frequency in the text  so far, decreasing the model's likelihood to repeat the same line verbatim. |

## Update config
If you find yourself overriding the config a lot when asking questions, you can update the default config instead.

### Update all config values

```bash
askai config update all
```

### Update individual config values

```bash
askai config update num-answers
askai config update model
askai config update temperature
askai config update top-p
askai config update max-tokens
askai config update frequency-penalty
askai config update presence-penalty
```

### Reset to default config
```bash
askai config reset
```

### See current config
```
askai config show
```

## Update API-key

It's possible to update the API-key without re-initializing the CLI.

### Overwrite current API-key
```
askai key add
```

### Remove current API-key
```
askai key remove
```

## Available models

This list was updated from OpenAI's website on 2022-12-20 and might go out of date at any time. Please
check [here](https://beta.openai.com/docs/models) to see an accurate list.

#### Text-generating models
| --model          | Description                                  | Max tokens |
|------------------|----------------------------------------------|------------|
| text-davinci-003 | The most capable GPT3 model                  | 4000       |
| text-curie-001   | Worse than davinci. Still capable and faster | 2048       |
| text-babbage-001 | Can do straight forward tasks. Very fast     | 2048       |
| text-ada-001     | Capable of very simple tasks. Very fast      | 2048       |

#### Code-generating models
| --model          | Description                               | Max tokens |
|------------------|-------------------------------------------|------------|
| code-davinci-002 | Most capable code-generating model.       | 8000       |
| code-cushman-001 | Almost as capable as davinci, but faster. | 2048       |

## Important notes

Note that the answers generated by OpenAI and shown by `askai` is by no means a "truth". 
You always need to be skeptical. And of course, don't execute generated commands or code
without verifying that it does what you asked for.
