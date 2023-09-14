#/// The following section is from :-
#///OpenAI platform, 2023. OpenAI platform [online]. Openai.com.
#///Available from: https://platform.openai.com/playground [Accessed 14 Aug 2023].import os
import openai
from config import apikey

openai.api_key = apikey

response = openai.Completion.create(
  model="text-davinci-003",
  prompt="Be my personal Fitness traine\n\nThank you for your interest in me as your Fitness trainer! I would love to help you reach your health and fitness goals and encourage you to stay motivated in following a regular schedule. My approach to fitness is to provide a comprehensive, tailored program that sets the right goals and meets the individual's needs. I will work with you to determine your current abilities and to develop a program that will progress at the right pace. \n\nI believe physical activity is essential to enhancing our quality of life, so I will be here to help break barriers and focus on your success. Together, we'll come up with a plan that works best for you!",
  temperature=1,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

print(response)
'''
{
  "id": "cmpl-7b4wp22Z6TVHOuRSZAXY5JfJMUZ9O",
  "object": "text_completion",
  "created": 1689071511,
  "model": "text-davinci-003",
  "choices": [
    {
      "text": "",
      "index": 0,
      "logprobs": null,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 137,
    "total_tokens": 137
  }
}
'''
#/// end of Citation
